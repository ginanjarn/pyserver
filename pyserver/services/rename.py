"""rename service"""

from dataclasses import dataclass
from typing import Dict, Any

from jedi import Script, Project
from jedi.api.refactoring import Refactoring, RefactoringError

from pyserver import errors
from pyserver.services import diffutils
from pyserver.workspace import (
    Document,
    Workspace,
    uri_to_path,
    path_to_uri,
)


@dataclass
class RenameParams:
    document: Document
    line: int
    character: int
    new_name: str

    def jedi_rowcol(self):
        return (self.line + 1, self.character)

    def file_path(self):
        return self.document.path

    def text(self):
        return self.document.text

    def workspace(self) -> Workspace:
        return self.document.workspace


class RenameService:
    def __init__(self, params: RenameParams):
        self.params = params
        self.script = Script(
            self.params.text(),
            path=self.params.file_path(),
            project=Project(self.params.workspace().root_path),
        )

    def execute(self) -> Refactoring:
        row, col = self.params.jedi_rowcol()
        try:
            return self.script.rename(row, col, new_name=self.params.new_name)
        except RefactoringError as err:
            raise errors.InvalidRequest(repr(err)) from err

    def build_item(self, refactor: Refactoring):
        for file_path, change in refactor.get_changed_files().items():
            # File Resource Changes
            old = change._from_path
            new = change._to_path
            if old != new:
                yield {
                    "kind": "rename",
                    "oldUri": path_to_uri(old),
                    "newUri": path_to_uri(new),
                }
                continue

            # TextEdit changes

            # 'new_text' from jedi has variance on newline.
            # Normalize newline to '\n'.
            new_text = change.get_new_code()
            new_text = new_text.replace("\r\n", "\n").replace("\r", "\n")

            try:
                document = self.params.workspace().get_document(file_path)
            except errors.InvalidResource:
                temp_text = file_path.read_text()
                document = Document(
                    self.params.workspace(), file_path, "", 0, temp_text
                )

            yield {
                "textDocument": {
                    "version": document.version,
                    "uri": document.document_uri,
                },
                "edits": diffutils.get_text_changes(document.text, new_text),
            }

    def get_result(self) -> Dict[str, Any]:
        refactored = self.execute()
        return {"documentChanges": list(self.build_item(refactored))}


def textdocument_rename(workspace: Workspace, params: dict) -> None:
    try:
        file_path = uri_to_path(params["textDocument"]["uri"])
        line = params["position"]["line"]
        character = params["position"]["character"]
        new_name = params["newName"]
    except KeyError as err:
        raise errors.InvalidParams(f"invalid params: {err}") from err

    document = workspace.get_document(file_path)
    params = RenameParams(document, line, character, new_name)
    service = RenameService(params)
    return service.get_result()
