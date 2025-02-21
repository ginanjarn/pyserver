"""Session"""

from enum import Enum
from pathlib import Path
from typing import Dict

from pyserver.document import Document
from pyserver.errors import InvalidResource


class SessionStatus(Enum):
    ShuttingDown = -1
    NotInitialized = 0
    Initializing = 1
    Initialized = 2


class Session:
    """Session"""

    def __init__(self):
        self.status: SessionStatus = SessionStatus.NotInitialized

        self.root_path: Path = None
        self.working_documents: Dict[Path, Document] = {}

    def add_document(self, file_path: Path, language_id: str, version: int, text: str):
        workspace_path = self.root_path
        self.working_documents[file_path] = Document(
            workspace_path, file_path, language_id, version, text
        )

    def remove_document(self, file_path: Path):
        try:
            del self.working_documents[file_path]
        except KeyError:
            pass

    def get_document(self, file_path: Path) -> Document:
        try:
            return self.working_documents[file_path]
        except KeyError as err:
            raise InvalidResource(f"{file_path!r} not opened") from err
