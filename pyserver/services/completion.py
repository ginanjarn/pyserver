"""completion service"""

from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Any

from jedi import Script, Project
from jedi.api.classes import Completion

from pyserver.services import Services


@dataclass
class CompletionParams:
    root_path: str
    file_name: str
    text: str
    line: int
    character: int

    def jedi_rowcol(self):
        # jedi use one based line index
        return self.line + 1, self.character


class CompletionService(Services):
    def __init__(self, params: CompletionParams):
        self.params = params
        self._text_edit_range = None

    def execute(self) -> List[Completion]:
        project = Project(self.params.root_path)
        script = Script(self.params.text, path=self.params.file_name, project=project)
        row, col = self.params.jedi_rowcol()
        return script.complete(row, col)

    kind_map = defaultdict(
        lambda: 1,  # default 'text'
        {
            "module": 9,
            "class": 7,
            "instance": 5,
            "function": 3,
            "params": 5,
            "path": 17,
            "keyword": 14,
            "property": 10,
            "statement": 6,
        },
    )

    def build_items(self, completions: List[Completion]):
        for completion in completions:

            if self._text_edit_range is None:
                prefix_len = completion.get_completion_prefix_length()
                self._text_edit_range = {
                    "start": {
                        "line": self.params.line,
                        "character": self.params.character - prefix_len,
                    },
                    "end": {
                        "line": self.params.line,
                        "character": self.params.character,
                    },
                }

            text = completion.name
            try:
                name_type = completion.type
            except Exception:
                name_type = None

            item = {
                "label": text,
                "labelDetails": {},
                "kind": self.kind_map[name_type],
                "preselect": False,
                "sortText": text,
                "filterText": text,
                "insertTextFormat": 1,  # insert format = text
                "textEdit": {"range": self._text_edit_range, "newText": text,},
            }

            if name_type in {"class", "function", "property"}:
                try:
                    if signature := completion._get_docstring_signature():
                        item["detail"] = signature
                except Exception:
                    pass
            yield item

    def get_result(self) -> Dict[str, Any]:
        candidates = self.execute()

        # transform as rpc
        result = {
            "isIncomplete": True,
            "itemDefaults": {
                "editRange": {
                    "start": {"line": 0, "character": 0},
                    "end": {"line": 0, "character": 0},
                }
            },
            "items": list(self.build_items(candidates)),
        }
        return result
