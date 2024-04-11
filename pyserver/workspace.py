"""workspace objects"""

__all__ = ["DocumentURI", "Document", "Workspace", "path_to_uri", "uri_to_path"]

from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import List, Dict

from urllib.parse import urlparse, urlunparse, quote, unquote
from urllib.request import pathname2url, url2pathname

from pyserver import errors


# DocumentURI based on 'str' to make it JSON serializable
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
def path_to_uri(path: Path) -> DocumentURI:
    return DocumentURI.from_path(path)


@lru_cache(128)
def uri_to_path(uri: DocumentURI) -> Path:
    return DocumentURI(uri).to_path()


class Document:
    """Document object"""

    __slots__ = ["workspace", "path", "language_id", "version", "text"]

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

    def __repr__(self) -> str:
        return f"Document({self.path!r})"

    @property
    def document_uri(self) -> str:
        """document uri"""
        return path_to_uri(self.path)

    def apply_changes(self, content_changes: List[dict]):
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
        if file_path in self.documents:
            self.remove_document(file_path)

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


@contextmanager
def VersionedDocument(document: Document):
    """VersionedDocument check version changes pre and post execution.

    Raises ContentModified if version is changed.
    """
    try:
        pre_version = document.version
        yield document

    finally:
        post_version = document.version
        # check version changes
        if pre_version != post_version:
            raise errors.ContentModified(
                f"version changed. want:{pre_version}, expected:{post_version}"
            )
