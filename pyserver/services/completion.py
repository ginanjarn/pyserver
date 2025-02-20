"""completion service"""

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional

from jedi import Script, Project
from jedi.api.classes import Completion
from parso.tree import Leaf

from pyserver import errors
from pyserver.uri import uri_to_path
from pyserver.workspace import Workspace


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


class CompletionService:
    def __init__(self, params: CompletionParams):
        self.params = params
        self.script = Script(
            self.params.text,
            path=self.params.file_path,
            project=Project(self.params.workspace_path),
        )

        cursor_leaf = self.script._module_node.get_leaf_for_position(
            params.jedi_rowcol()
        )
        cursor_line = self.script._code_lines[params.line]

        self.text_edit_range = self._get_replaced_text_range(
            params.jedi_rowcol(), cursor_leaf
        )
        self.is_valid_scope = self._check_is_valid_scope(cursor_leaf)
        self.is_append_bracket = self._check_is_append_bracket(cursor_line, cursor_leaf)

    def execute(self) -> List[Completion]:
        if not self.is_valid_scope:
            return []

        row, col = self.params.jedi_rowcol()
        return self.script.complete(row, col)

    def _check_is_valid_scope(self, leaf: Optional[Leaf]) -> bool:
        if not leaf:
            return True

        leaf_type = leaf.type

        if leaf_type in {"name", "keyword"}:
            return True

        if leaf_type in {"string", "fstring_string", "number"}:
            return False

        closing_operator = {":", ")", "]", "}"}
        if leaf.value in closing_operator:
            return False

        if leaf_type in {"endmarker", "newline"}:
            prev = leaf.get_previous_leaf()
            if not prev:
                return False

            # after keyword eg: 'import <cursor>'
            if prev.type == "keyword":
                return True

            # after closing operator eg: 'def fn()<cursor>'
            if prev.value in closing_operator:
                return False

            return True

        return True

    def _check_is_append_bracket(self, cursor_line: str, leaf: Optional[Leaf]) -> bool:
        cursor_line = cursor_line.lstrip()
        if any(
            [
                cursor_line.startswith("@"),  # decorator
                cursor_line.startswith("import"),  # import
                cursor_line.startswith("from"),  # from .. import
            ]
        ):
            return False

        if not leaf:
            return False

        if (next_leaf := leaf.get_next_leaf()) and next_leaf.value == "(":
            return False

        if (parent := leaf.parent) and "import" in parent.type:
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

    def _build_item(self, completion: Completion) -> dict:
        text = completion.name
        signature_text = ""
        insert_text = text
        completion_type = completion.type

        # only get signatures for class and function
        if completion_type in {"class", "function"}:
            signatures = completion.get_signatures()
            visible_signature = None

            if signatures:
                visible_signature = signatures[0]
                signature_text = visible_signature.to_string()

            # append bracket for function
            if all(
                [
                    self.is_append_bracket,
                    visible_signature,
                    completion_type == "function",
                ]
            ):
                if params := visible_signature.params:
                    # overriden method
                    if params[0].name == "self":
                        insert_text = signature_text
                    else:
                        insert_text = f"{text}(${{1}})"
                else:
                    insert_text = f"{text}()"

        return {
            "label": text,
            "labelDetails": {},
            "kind": self.kind_map[completion_type],
            "preselect": False,
            "sortText": text,
            "filterText": text,
            "detail": signature_text,
            "insertTextFormat": 2,  # insert format = snippet
            "textEdit": {
                "range": self.text_edit_range,
                "newText": insert_text,
            },
        }

    def get_result(self) -> Dict[str, Any]:
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


def textdocument_completion(workspace: Workspace, params: dict) -> None:
    try:
        file_path = uri_to_path(params["textDocument"]["uri"])
        line = params["position"]["line"]
        character = params["position"]["character"]
    except KeyError as err:
        raise errors.InvalidParams(f"invalid params: {err}") from err

    document = workspace.get_document(file_path)
    params = CompletionParams(
        workspace.root_path,
        document.path,
        document.text,
        line,
        character,
    )
    service = CompletionService(params)
    return service.get_result()
