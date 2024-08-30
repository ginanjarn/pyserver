"""completion service"""

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional

from jedi import Script, Project
from jedi.api.classes import Completion
from parso.tree import Leaf

from pyserver import errors
from pyserver.workspace import (
    Workspace,
    uri_to_path,
)


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

        self.leaf = self.script._module_node.get_leaf_for_position(
            self.params.jedi_rowcol()
        )
        self.text_edit_range = self._get_replaced_text_range()
        self.is_append_bracket = self._check_can_append_bracket(self.leaf)

    def execute(self) -> List[Completion]:
        if not self.can_fetch_completion():
            return []

        row, col = self.params.jedi_rowcol()
        return self.script.complete(row, col)

    def can_fetch_completion(self) -> bool:
        leaf = self.leaf

        if not leaf:
            return True

        leaf_type = leaf.type

        if leaf_type in {"string", "fstring_string", "number"}:
            return False

        # closing operator
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

    def _check_can_append_bracket(self, leaf: Optional[Leaf]) -> bool:
        trigger_line = self.script._code_lines[self.params.line].lstrip()
        if any(
            [
                trigger_line.startswith("@"),  # decorator
                trigger_line.startswith("import"),  # import
                trigger_line.startswith("from"),  # from .. import
            ]
        ):
            return False

        if not leaf:
            return False

        if next_leaf := leaf.get_next_leaf():
            if next_leaf.value == "(":
                return False

        return True

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

    def _get_replaced_text_range(self) -> dict:
        """get replaced text range"""

        linepos = self.params.line
        start_char = end_char = self.params.character

        if (leaf := self.leaf) and leaf.type == "name":
            start_char = leaf.start_pos[1]
            end_char = leaf.end_pos[1]

        return {
            "start": {"line": linepos, "character": start_char},
            "end": {"line": linepos, "character": end_char},
        }

    def build_items(self, completions: List[Completion]) -> List[dict]:
        def build_item(completion: Completion):
            text = completion.name
            signature = ""
            insert_text = text
            completion_type = None

            try:
                completion_type = completion.type
            except Exception:
                pass

            if (
                self.is_append_bracket
                and bool(completion_type)
                and completion_type == "function"
            ):
                insert_text = f"{text}(${{0}})"

            # only show signature for class and function
            if completion_type in {"class", "function"}:
                try:
                    signatures = completion._get_signatures(for_docstring=True)
                except Exception:
                    pass

                if signatures:
                    signature = signatures[0].to_string()

            item = {
                "label": text,
                "labelDetails": {},
                "kind": self.kind_map[completion_type],
                "preselect": False,
                "sortText": text,
                "filterText": text,
                "detail": signature,
                "insertTextFormat": 1,  # insert format = text
                "textEdit": {
                    "range": self.text_edit_range,
                    "newText": insert_text,
                },
            }

            return item

        return [build_item(completion) for completion in completions]

    def get_result(self) -> Dict[str, Any]:
        try:
            candidates = self.execute()
        except Exception:
            candidates = []

        # transform as rpc
        result = {
            "isIncomplete": True,
            "itemDefaults": {
                "editRange": {
                    "start": {"line": 0, "character": 0},
                    "end": {"line": 0, "character": 0},
                }
            },
            "items": self.build_items(candidates),
        }
        return result


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
