"""document rename"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

from jedi import Script, Project
from jedi.api.refactoring import ChangedFile, Refactoring, RefactoringError

from pyserver import errors
from pyserver.uri import uri_to_path, path_to_uri
from pyserver.features import diffutils
from pyserver.document import Document
from pyserver.session import Session


@dataclass
class RenameParams:
    session: Session
    workspace_path: Path
    file_path: Path
    text: str
    line: int
    character: int
    new_name: str

    def jedi_rowcol(self):
        return (self.line + 1, self.character)


class RenameProvider:
    def __init__(self, params: RenameParams):
        self.params = params
        self.script = Script(
            self.params.text,
            path=self.params.file_path,
            project=Project(self.params.workspace_path),
        )

    def execute(self) -> Refactoring:
        row, col = self.params.jedi_rowcol()
        try:
            return self.script.rename(row, col, new_name=self.params.new_name)
        except RefactoringError as err:
            raise errors.InvalidRequest(repr(err)) from err


    def build_item(self, path: Path, changed_file: ChangedFile) -> Dict[str, Any]:
        # File Resource Changes
        old = changed_file._from_path
        new = changed_file._to_path
        if old != new:
            return {
                "kind": "rename",
                "oldUri": path_to_uri(old),
                "newUri": path_to_uri(new),
            }

        # TextEdit changes

        # 'new_text' from jedi has variance on newline.
        # Normalize newline to '\n'.
        new_text = changed_file.get_new_code()
        new_text = new_text.replace("\r\n", "\n").replace("\r", "\n")

        try:
            document = self.params.session.get_document(path)
        except errors.InvalidResource:
            temp_text = path.read_text()
            document = Document(self.params.workspace_path, path, "", 0, temp_text)

        return {
            "textDocument": {
                "version": document.version,
                "uri": path_to_uri(document.file_path),
            },
            "edits": diffutils.get_text_changes(document.text, new_text),
        }

    def get_changes(self) -> Dict[str, Any]:
        refactored = self.execute()
        changed_files = refactored.get_changed_files()
        if not changed_files:
            return None

        changes = [
            self.build_item(path, changed_file)
            for path, changed_file in changed_files.items()
        ]
        return {"documentChanges": changes}


def textdocument_rename(session: Session, params: dict) -> None:
    try:
        file_path = uri_to_path(params["textDocument"]["uri"])
        line = params["position"]["line"]
        character = params["position"]["character"]
        new_name = params["newName"]
    except KeyError as err:
        raise errors.InvalidParams(f"invalid params: {err}") from err

    document = session.get_document(file_path)
    params = RenameParams(
        session,
        document.workspace_path,
        document.file_path,
        document.text,
        line,
        character,
        new_name,
    )
    service = RenameProvider(params)
    return service.get_changes()
