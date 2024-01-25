"""workspace objects"""

__all__ = ["DocumentURI", "Document", "Workspace", "path_to_uri", "uri_to_path"]

import logging
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List, Dict, Union

from urllib.parse import urlparse, urlunparse, quote, unquote
from urllib.request import pathname2url, url2pathname

from pyserver import errors

DEV_LOGGER = logging.getLogger("pyserver-dev")


class DocumentURI(str):
    """document uri"""

    @classmethod
    def from_path(cls, path: Path):
        """from file name"""
        return cls(urlunparse(("file", "", quote(pathname2url(str(path))), "", "", "")))

    def to_path(self) -> Path:
        """convert to path"""
        parsed = urlparse(self)
        if parsed.scheme != "file":
            raise ValueError("url scheme must be 'file'")

        return Path(url2pathname(unquote(parsed.path)))


@lru_cache(128)
def path_to_uri(path: str) -> Path:
    return DocumentURI.from_path(path)


@lru_cache(128)
def uri_to_path(uri: Path) -> DocumentURI:
    return DocumentURI(uri).to_path()


@dataclass
class Document:
    """Document object"""

    path: Path
    language_id: str
    version: int
    text: str

    __slots__ = ["path", "language_id", "version", "text"]

    @classmethod
    def from_file(cls, file_path: Union[Path, str]):
        text = Path(file_path).read_text()
        return cls(file_path, "", 0, text)

    @property
    def document_uri(self) -> str:
        """document uri"""
        return path_to_uri(self.path)

    def did_change(self, content_changes: List[dict]):
        for change in content_changes:
            try:
                start = change["range"]["start"]
                end = change["range"]["end"]
                new_text = change["text"]

                start_line, start_character = start["line"], start["character"]
                end_line, end_character = end["line"], end["character"]

            except KeyError as err:
                raise errors.InvalidParams(f"invalid params {err}") from err

            lines = self.text.split("\n")
            temp_lines = []

            # pre change line
            temp_lines.extend(lines[:start_line])
            # line changed
            prefix = lines[start_line][:start_character]
            suffix = lines[end_line][end_character:]
            line = f"{prefix}{new_text}{suffix}"
            temp_lines.append(line)
            # post change line
            temp_lines.extend(lines[end_line + 1 :])

            self.text = "\n".join(temp_lines)


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

    def open_document(self, file_path: Path, language_id: str, version: int, text: str):
        if file_path in self.documents:
            self.close_document(file_path)

        self.documents[file_path] = Document(
            Path(file_path), language_id, version, text
        )
        DEV_LOGGER.debug("documents: %s", self.documents)

    def close_document(self, file_path: Path):
        try:
            del self.documents[file_path]
        except KeyError:
            pass
        DEV_LOGGER.debug("documents: %s", self.documents)

    def change_document(self, file_path: Path, version: int, changes: List[dict]):
        document = self.get_document(file_path)
        if version > document.version:
            document.version = version
            document.did_change(changes)

    def get_document(self, file_path: Path) -> Document:
        DEV_LOGGER.debug("documents: %s", self.documents)
        try:
            return self.documents[file_path]
        except KeyError as err:
            raise errors.InvalidResource(f"{file_path!r} not opened") from err
