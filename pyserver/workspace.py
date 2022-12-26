"""workspace objects"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Union

from pyserver import errors
from pyserver import message


@dataclass
class Document:
    """Document object"""

    path: Path
    language_id: str
    version: int
    text: str

    @classmethod
    def from_file(cls, file_path: Union[Path, str]):
        text = Path(file_path).read_text()
        return cls(file_path, "", 0, text)

    @property
    def document_uri(self) -> str:
        """document uri"""
        return message.path_to_uri(self.path)

    def did_change(self, content_changes: List[dict]):
        lines = self.text.split("\n")
        for change in content_changes:
            try:
                start = change["range"]["start"]
                end = change["range"]["end"]
                new_text = change["text"]

                start_line, start_character = start["line"], start["character"]
                end_line, end_character = end["line"], end["character"]

            except KeyError as err:
                raise errors.InvalidParams(f"invalid params {err}")

            new_lines = []
            # pre change line
            new_lines.extend(lines[:start_line])
            # line changed
            prefix = lines[start_line][:start_character]
            suffix = lines[end_line][end_character:]
            line = f"{prefix}{new_text}{suffix}"
            new_lines.extend(line.split("\n"))
            # post change line
            new_lines.extend(lines[end_line + 1 :])
            # update
            lines = new_lines

        self.text = "\n".join(lines)


class Workspace:
    """workspace handler"""

    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.documents: Dict[str, Document] = {}

        if not self.root_path.is_dir():
            raise errors.InternalError(f"{root_path!r} is not directory")

    def __repr__(self):
        return f"Workspace(root_path={self.root_path!r},documents={self.documents!r})"

    def open_document(self, file_path: Path, language_id: str, version: int, text: str):
        self.documents[file_path] = Document(
            Path(file_path), language_id, version, text
        )

    def close_document(self, file_path: Path):
        try:
            del self.documents[file_path]
        except KeyError:
            pass

    def get_document(self, file_path: Path) -> Document:
        try:
            return self.documents[file_path]
        except KeyError as err:
            raise errors.InvalidResource(f"{file_path!r} not opened") from err
