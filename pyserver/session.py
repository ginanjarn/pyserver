"""Session data"""

import logging
from dataclasses import dataclass
from pathlib import Path
from threading import RLock
from typing import Dict, List

LOGGER = logging.getLogger(__name__)


@dataclass
class WorkspaceFolder:
    path: Path
    name: str


@dataclass
class Document:
    file_name: Path
    text: str
    version: int


class DocumentNotFound(KeyError):
    """Document Not Found"""


class Session:
    def __init__(self) -> None:
        self.root_path: Path = None
        self.working_documents: Dict[Path, Document] = dict()
        self.workspace_folders: List[WorkspaceFolder] = list()
        self.is_initialized: bool = False

        self._lock = RLock()

    def add_document(self, document: Document) -> None:
        with self._lock:
            self.working_documents[document.file_name] = document

    def get_document(self, file_name: Path) -> Document:
        with self._lock:
            try:
                return self.working_documents[file_name]
            except KeyError as err:
                raise DocumentNotFound(str(err)) from err

    def delete_document(self, file_name: Path) -> None:
        with self._lock:
            try:
                del self.working_documents[file_name]
            except KeyError as err:
                LOGGER.warning("Document not found %s", err)
