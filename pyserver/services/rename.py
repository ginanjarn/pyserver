"""rename service"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

from jedi import Script, Project
from jedi.api.refactoring import Refactoring, RefactoringError

from pyserver import errors
from pyserver.workspace import Workspace, Document
from pyserver.services import diffutils


@dataclass
class RenameParams:
    workspace: Workspace
    file_path: Path
    line: int
    character: int
    new_name: str

    def jedi_rowcol(self):
        return (self.line + 1, self.character)

    def jedi_project(self):
        return Project(self.workspace.root_path)

    @property
    def document(self):
        return self.workspace.get_document(self.file_path)

    @property
    def text(self):
        return self.document.text


class RenameService:
    def __init__(self, params: RenameParams):
        self.params = params
        self.script = Script(
            self.params.text,
            path=self.params.file_path,
            project=self.params.jedi_project(),
        )

    def execute(self) -> Refactoring:
        row, col = self.params.jedi_rowcol()
        try:
            return self.script.rename(row, col, new_name=self.params.new_name)
        except RefactoringError as err:
            raise errors.InvalidRequest(repr(err)) from err

    def build_item(self, refactor: Refactoring):

        for file_path, change in refactor.get_changed_files().items():

            origin_text = file_path.read_text()
            if file_path == self.params.file_path:
                # use buffered text
                origin_text = self.params.text

            new_text = change.get_new_code()
            # normalize newlines
            new_text = new_text.replace("\r\n", "\n").replace("\r", "\n")

            try:
                document = self.params.workspace.get_document(file_path)
            except errors.InvalidResource:
                document = Document.from_file(file_path)

            yield {
                "textDocument": {
                    "version": document.version,
                    "uri": document.document_uri,
                },
                "edits": diffutils.get_text_changes(origin_text, new_text),
            }

    def get_result(self) -> Dict[str, Any]:
        refactored = self.execute()
        return {"documentChanges": list(self.build_item(refactored))}
