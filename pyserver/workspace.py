"""workspace objects"""

__all__ = ["DocumentURI", "Document", "Workspace", "path_to_uri", "uri_to_path"]

from functools import lru_cache
from pathlib import Path
from typing import List, Dict
from urllib.parse import urlparse, unquote_plus
from urllib.request import url2pathname

from pyserver import errors


DocumentURI = str
"""Uniform Resource Identifier.
See 'RFC 3986' specification.
"""


@lru_cache(128)
def path_to_uri(path: Path) -> DocumentURI:
    """convert path to uri"""
    return Path(path).as_uri()


@lru_cache(128)
def uri_to_path(uri: DocumentURI) -> Path:
    """convert uri to path"""
    parsed = urlparse(uri)
    if parsed.scheme != "file":
        raise ValueError("url scheme must be 'file'")

    return Path(url2pathname(unquote_plus(parsed.path)))


class Document:
    """Document object"""

    __slots__ = ["workspace", "path", "language_id", "version", "text", "is_saved"]

    def __init__(
        self,
        workspace: "Workspace",
        path: Path,
        language_id: str,
        version: int,
        text: str,
    ):
        self.workspace = workspace
        self.path = path
        self.language_id = language_id
        self.version = version
        self.text = text
        self.is_saved = True

    def __repr__(self) -> str:
        return f"Document({self.path!r})"

    @property
    def document_uri(self) -> str:
        """document uri"""
        return path_to_uri(self.path)

    def save(self):
        self.is_saved = True

    def apply_changes(self, content_changes: List[dict]):
        self.text = self._update_text(self.text, content_changes)
        self.is_saved = False

    @staticmethod
    def get_offset(lines: List[str], row: int, column: int) -> int:
        line_offset = sum([len(l) for l in lines[:row]])
        return line_offset + column

    @staticmethod
    def _update_text(text: str, changes: List[dict]) -> str:
        temp = text

        for change in changes:
            try:
                start = change["range"]["start"]
                end = change["range"]["end"]
                new_text = change["text"]

                start_line, start_character = start["line"], start["character"]
                end_line, end_character = end["line"], end["character"]

            except KeyError as err:
                raise errors.InvalidParams(f"invalid params {err}") from err

            lines = temp.splitlines(keepends=True)
            start_offset = Document.get_offset(lines, start_line, start_character)
            end_offset = Document.get_offset(lines, end_line, end_character)
            temp = f"{temp[:start_offset]}{new_text}{temp[end_offset:]}"

        return temp

    def did_change(self, version: int, content_changes: List[dict], /):
        if version > self.version:
            self.apply_changes(content_changes)
            self.version = version


class Workspace:
    """workspace handler"""

    __slots__ = ["root_path", "documents"]

    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.documents: Dict[str, Document] = {}

        if not self.root_path.is_dir():
            raise errors.InternalError(f"{root_path!r} is not directory")

    def __repr__(self):
        return f"Workspace(root_path={self.root_path!r},documents={self.documents!r})"

    def add_document(self, file_path: Path, language_id: str, version: int, text: str):
        self.documents[file_path] = Document(
            self, Path(file_path), language_id, version, text
        )

    def remove_document(self, file_path: Path):
        try:
            del self.documents[file_path]
        except KeyError:
            pass

    def get_document(self, file_path: Path) -> Document:
        try:
            return self.documents[file_path]
        except KeyError as err:
            raise errors.InvalidResource(f"{file_path!r} not opened") from err
