"""completion service"""

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

from jedi import Script, Project
from jedi.api.classes import Completion


@dataclass
class CompletionParams:
    root_path: Path
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
            project=Project(self.params.root_path),
        )

        self.leaf = self.script._module_node.get_leaf_for_position(
            self.params.jedi_rowcol()
        )
        self.text_edit_range = self._get_replaced_text_range()

    def execute(self) -> List[Completion]:

        if leaf := self.leaf:
            if leaf.type in {
                "newline",
                "string",
                "fstring_string",
                "number",
            }:
                return []

            if leaf.type == "operator" and leaf.value in ":)]}":
                return []

        row, col = self.params.jedi_rowcol()
        return self.script.complete(row, col)

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
            signature = None

            try:
                type_name = completion.type

                # only show signature for class and function
                if type_name in {"class", "function"}:
                    if signatures := completion._get_signatures(for_docstring=True):
                        # get first signature
                        signature = signatures[0].to_string()

            except Exception:
                type_name = None

            item = {
                "label": text,
                "labelDetails": {},
                "kind": self.kind_map[type_name],
                "preselect": False,
                "sortText": text,
                "filterText": text,
                "insertTextFormat": 1,  # insert format = text
                "textEdit": {
                    "range": self.text_edit_range,
                    "newText": text,
                },
            }

            if signature:
                item["detail"] = signature

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
