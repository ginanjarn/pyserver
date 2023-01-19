"""completion service"""

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

from jedi import Script, Project
from jedi.api.classes import Completion

from pyserver.services import Services


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


class CompletionService(Services):
    def __init__(self, params: CompletionParams):
        self.params = params
        self._text_edit_range = None

    def execute(self) -> List[Completion]:
        project = Project(self.params.root_path)
        script = Script(self.params.text, path=self.params.file_path, project=project)
        row, col = self.params.jedi_rowcol()
        return script.complete(row, col)

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

    # indentifier started by alphabet or understrip followed by alphanumeric
    identifier_pattern = re.compile(r"[_a-zA-Z]\w*")

    def get_text_edit_range(self):
        if self._text_edit_range:
            return self._text_edit_range

        linepos = self.params.line
        lines = self.params.text.split("\n")
        trigger_line = lines[linepos]

        trigger_character = self.params.character
        start_char = end_char = trigger_character

        # text range wraps word where trigger located
        for found in self.identifier_pattern.finditer(trigger_line):
            start, end = found.start(), found.end()
            if start <= self.params.character <= end:
                start_char = start
                end_char = end
                break

        # else:
        # change only happen at trigger location

        self._text_edit_range = {
            "start": {"line": linepos, "character": start_char},
            "end": {"line": linepos, "character": end_char},
        }
        return self._text_edit_range

    def build_items(self, completions: List[Completion]):
        for completion in completions:

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
                "textEdit": {
                    "range": self.get_text_edit_range(),
                    "newText": text,
                },
            }

            if name_type in {"class", "function", "property"}:
                try:
                    if signature := completion._get_docstring_signature():
                        # a function may contain multiple signature
                        item["detail"] = max(signature.split("\n"))
                except Exception:
                    pass
            yield item

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
            "items": list(self.build_items(candidates)),
        }
        return result
