"""document completion"""

import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional

from jedi import Script, Project
from jedi.api.classes import Completion
from parso.tree import Leaf

from pyserver import errors
from pyserver.uri import uri_to_path
from pyserver.session import Session


@dataclass
class CompletionParams:
    workspace_path: Path
    file_path: Path
    text: str
    line: int
    character: int

    def jedi_rowcol(self):
        # jedi use one based line index
        return self.line + 1, self.character


IDENTIFIER_TYPE = frozenset({"name", "keyword"})
CALLABLE_TYPE = frozenset({"class", "function"})
LITERAL_TYPE = frozenset({"string", "fstring_string", "number"})
ENDMARKER_TYPE = frozenset({"endmarker", "newline"})
CLOSING_PUNCTUATION = frozenset({":", ")", "]", "}"})
# 1st element of sys.path is working directory
LIBRARY_PATH = tuple(sys.path[1:])


class CompletionItem:
    __slots__ = ["text", "signature_params", "signature_returns", "kind"]

    def __init__(
        self,
        text: str,
        signature_params: str,
        signature_returns: str,
        kind: str,
    ):
        self.text = text
        self.signature_params = signature_params
        self.signature_returns = signature_returns
        self.kind = kind

    def signature(self) -> str:
        if self.kind not in CALLABLE_TYPE:
            return ""
        returns = f" -> {self.signature_returns}" if self.signature_returns else ""
        return f"{self.text}({self.signature_params}){returns}"

    def insert_text(self, append_bracket: bool = False) -> str:
        if self.kind != "function":
            return self.text
        if not append_bracket:
            return self.text
        if not self.signature_params:
            return f"{self.text}()"
        # inherited method
        if self.signature_params.startswith("self"):
            return self.signature()
        return f"{self.text}(${{1}})"


class CompletionProvider:
    def __init__(self, params: CompletionParams):
        self.params = params
        self.script = Script(
            self.params.text,
            path=self.params.file_path,
            project=Project(self.params.workspace_path),
        )
        self.text_edit_range = {}
        self.is_append_bracket = False

    def execute(self) -> List[Completion]:
        jedi_rowcol = self.params.jedi_rowcol()
        cursor_leaf = self.script._module_node.get_leaf_for_position(jedi_rowcol)

        self.text_edit_range = self._get_replaced_text_range(jedi_rowcol, cursor_leaf)

        self.is_append_bracket = self._check_is_append_bracket(
            self.script._code_lines[self.params.line],  # Text line at cursor location
            cursor_leaf,
        )

        if not self._is_return_completion(cursor_leaf):
            return []

        return self.script.complete(*jedi_rowcol)

    @staticmethod
    def _is_return_completion(leaf: Optional[Leaf]) -> bool:
        """check if return completion
        For example if leaf is literal or number, completion is unavailable.
        """

        if not leaf:
            return True

        leaf_type = leaf.type
        if leaf_type in IDENTIFIER_TYPE:
            return True

        if leaf_type in LITERAL_TYPE:
            return False

        if leaf_type in ENDMARKER_TYPE:
            prev = leaf.get_previous_leaf()
            if not prev:
                return False

            # after keyword eg: 'import <cursor>'
            if prev.type == "keyword":
                return True

            # after closing operator eg: 'def fn()<cursor>'
            if prev.value in CLOSING_PUNCTUATION:
                return False
            return True

        if leaf.value in CLOSING_PUNCTUATION:
            return False
        return True

    def _check_is_append_bracket(self, cursor_line: str, leaf: Optional[Leaf]) -> bool:
        if not leaf:
            return False

        if leaf.value == "(":
            return False

        # followed by open bracket
        if (next_leaf := leaf.get_next_leaf()) and next_leaf.value == "(":
            return False
        # import statement
        if (parent := leaf.parent) and parent.type.startswith("import"):
            return False

        if (line := cursor_line.lstrip()) and line.startswith(
            (
                "@",  # decorator
                "import ",  # import
                "from ",  # from .. import
            )
        ):
            return False

        return True

    def _get_replaced_text_range(
        self, cursor_location: tuple, leaf: Optional[Leaf]
    ) -> dict:
        """get replaced text range"""

        if leaf and leaf.type == "name":
            start = leaf.start_pos
            end = leaf.end_pos
        else:
            start = end = cursor_location

        # jedi use 1-based line index
        return {
            "start": {"line": start[0] - 1, "character": start[1]},
            "end": {"line": end[0] - 1, "character": end[1]},
        }

    kind_map = defaultdict(
        lambda: 1,  # default 'text'
        {
            "module": 9,
            "class": 7,
            "instance": 5,
            "function": 3,
            "param": 5,
            "path": 17,
            "keyword": 14,
            "property": 10,
            "statement": 6,
        },
    )

    cached_items = dict()

    def get_completion_item(self, completion: Completion) -> CompletionItem:
        text = completion.name
        kind = completion.type
        params = ""
        annotation = ""

        # only get signatures for class and function
        if kind in CALLABLE_TYPE:
            try:
                signatures = completion.get_signatures()
                visible_signature = signatures[0]
                signature_params = [p.to_string() for p in visible_signature.params]
            except Exception:
                pass

            else:
                params = ", ".join(signature_params)
                try:
                    annotation_string = visible_signature._signature.annotation_string
                    # normalize to one line
                    annotation = " ".join(annotation_string.split())
                except Exception:
                    annotation = ""

        return CompletionItem(text, params, annotation, kind)

    def _build_item(self, completion: Completion) -> dict:
        name = completion.name
        module_path = str(completion.module_path)

        if module_path.startswith(LIBRARY_PATH):
            # store library item into cache
            try:
                # load
                item = self.cached_items[(module_path, name)]

            except (KeyError, AttributeError):
                item = self.get_completion_item(completion)
                # store
                if item.kind in CALLABLE_TYPE:
                    self.cached_items[(module_path, name)] = item
        else:
            item = self.get_completion_item(completion)

        return {
            "label": item.text,
            "labelDetails": {},
            "kind": self.kind_map[item.kind],
            "preselect": False,
            "sortText": item.text,
            "filterText": item.text,
            "detail": item.signature(),
            "insertTextFormat": 2,  # insert format = snippet
            "textEdit": {
                "range": self.text_edit_range,
                "newText": item.insert_text(self.is_append_bracket),
            },
        }

    def get_completions(self) -> Dict[str, Any]:
        try:
            candidates = self.execute()
        except Exception:
            candidates = []

        # transform as rpc
        return {
            "isIncomplete": True,
            "itemDefaults": {
                "editRange": {
                    "start": {"line": 0, "character": 0},
                    "end": {"line": 0, "character": 0},
                }
            },
            "items": [self._build_item(completion) for completion in candidates],
        }


def textdocument_completion(session: Session, params: dict) -> None:
    try:
        file_path = uri_to_path(params["textDocument"]["uri"])
        line = params["position"]["line"]
        character = params["position"]["character"]
    except KeyError as err:
        raise errors.InvalidParams(f"invalid params: {err}") from err

    document = session.get_document(file_path)
    params = CompletionParams(
        document.workspace_path,
        document.file_path,
        document.text,
        line,
        character,
    )
    service = CompletionProvider(params)
    return service.get_completions()
