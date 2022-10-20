"""prepare rename service"""

import re
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

from jedi import Script, Project
from jedi.api.refactoring import RefactoringError

from pyserver.services import Services


@dataclass
class PrepareRenameParams:
    root_path: str
    file_name: str
    text: str
    line: int
    character: int

    def lines(self) -> List[str]:
        return self.text.split("\n")

    def jedi_rowcol(self):
        return (self.line + 1, self.character)


@dataclass
class Identifier:
    start_line: int
    start_character: int
    end_line: int
    end_character: int
    text: str


class PrepareRenameService(Services):
    def __init__(self, params: PrepareRenameParams):
        self.params = params

    ident_pattern = re.compile(r"([a-zA-Z_][\w+]*)")

    def execute(self) -> Optional[Identifier]:
        try:
            Script(
                self.params.text,
                path=self.params.file_name,
                project=Project(self.params.root_path),
            )
        except RefactoringError:
            return None

        lines = self.params.lines()
        line_occurence = lines[self.params.line]
        for found in self.ident_pattern.finditer(line_occurence):
            start_line = end_line = self.params.line
            start_char = found.start()
            end_char = found.end()
            if start_char <= self.params.character <= end_char:
                return Identifier(
                    start_line, start_char, end_line, end_char, found.group(1)
                )

        return None

    def get_result(self) -> Optional[Dict[str, Any]]:
        candidate = self.execute()
        if not candidate:
            return None

        return {
            "range": {
                "start": {
                    "line": candidate.start_line,
                    "character": candidate.start_character,
                },
                "end": {
                    "line": candidate.end_line,
                    "character": candidate.end_character,
                },
            },
            "placeholder": candidate.text,
        }
