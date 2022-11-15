"""rename service"""

import re
from dataclasses import dataclass
from difflib import unified_diff
from typing import Dict, Any

from jedi import Script, Project
from jedi.api.refactoring import Refactoring, RefactoringError

from pyserver import errors
from pyserver.services import Services
from pyserver.workspace import Workspace, Document


@dataclass
class RenameParams:
    workspace: Workspace
    file_name: str
    line: int
    character: int
    new_name: str

    def jedi_rowcol(self):
        return (self.line + 1, self.character)

    def jedi_project(self):
        return Project(self.workspace.root_path)

    @property
    def document(self):
        return self.workspace.get_document(self.file_name)

    @property
    def text(self):
        return self.document.text


class RenameService(Services):
    def __init__(self, params: RenameParams):
        self.params = params

    def execute(self) -> Refactoring:
        script = Script(
            self.params.text,
            path=self.params.file_name,
            project=self.params.jedi_project(),
        )
        row, col = self.params.jedi_rowcol()
        try:
            return script.rename(row, col, new_name=self.params.new_name)
        except RefactoringError as err:
            raise errors.InvalidRequest(repr(err)) from err

    signature_regex = re.compile(r"@@\ \-(\d+)(?:,(\d+))?\ \+(\d+)(?:,(\d+))? @@")

    @staticmethod
    def build_diff_items(diff_text: str, origin: str):
        origin_lines = origin.split("\n")
        diff_lines = diff_text.split("\n")

        item_range = None
        buffer = []

        for line in diff_lines:

            if line.startswith("---") or line.startswith("+++"):
                continue

            if line.startswith("-"):
                continue

            if line.startswith("+"):
                buffer.append(line[1:])
                continue

            if line.startswith(" "):
                buffer.append(line[1:])
                continue

            if line.startswith("@@"):
                if item_range:
                    yield {"range": item_range, "newText": "\n".join(buffer)}

                match = RenameService.signature_regex.match(line)
                if not match:
                    raise ValueError("unable parse diff signature")

                rem_start_line = int(match.group(1)) - 1  # diff use 1-based line index
                # add_start_line = int(match.group(3)) - 1  # diff use 1-based line index

                rem_changed_line = int(match.group(2)) - 1 if match.group(2) else 0
                # add_changed_line = int(match.group(4)) - 1 if match.group(4) else 0
                rem_end_line = rem_start_line + rem_changed_line
                # add_end_line = add_start_line + add_changed_line

                # set block
                item_range = {
                    "start": {"line": rem_start_line, "character": 0},
                    "end": {
                        "line": rem_end_line,
                        "character": len(origin_lines[rem_end_line]),
                    },
                }
                buffer = []

        # yield last block
        if item_range:
            yield {"range": item_range, "newText": "\n".join(buffer)}

    def build_item(self, refactor: Refactoring):

        for file_path, change in refactor.get_changed_files().items():

            origin_text = file_path.read_text()
            if str(file_path) == self.params.file_name:
                # use buffered text
                origin_text = self.params.text

            new_text = change.get_new_code()
            # normalize newlines
            new_text = new_text.replace("\r\n", "\n").replace("\r", "\n")

            # 'Refactoring.get_diff' method return inconsistent newline result
            # Use builtin difflib
            udiff = unified_diff(
                origin_text.split("\n"),
                new_text.split("\n"),
                str(file_path),
                str(file_path),
            )
            diff_text = "\n".join(udiff)

            try:
                document = self.params.workspace.get_document(str(file_path))
            except errors.InvalidResource:
                document = Document.from_file(file_path)

            yield {
                "textDocument": {
                    "version": document.version,
                    "uri": document.document_uri,
                },
                "edits": list(self.build_diff_items(diff_text, origin_text)),
            }

    def get_result(self) -> Dict[str, Any]:
        refactored = self.execute()
        return {"documentChanges": list(self.build_item(refactored))}
