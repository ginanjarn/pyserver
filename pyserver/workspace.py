"""workspace objects"""

from dataclasses import dataclass
from typing import List, Dict

from pyserver import errors
from pyserver import message


@dataclass
class Document:
    """Document object"""

    file_name: str
    language_id: str
    version: int
    text: str

    @classmethod
    def from_file(cls, file_name: str):
        with open(file_name) as file:
            text = file.read()

        return cls(file_name, "", 0, text)

    @property
    def document_uri(self) -> str:
        """document uri"""
        return message.path_to_uri(self.file_name)

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

    def __init__(self, root_path: str):
        self.root_path = root_path
        self.documents: Dict[str, Document] = {}

    def __repr__(self):
        return f"Workspace(root_path={self.root_path!r},documents={self.documents!r})"

    def open_document(self, file_name: str, language_id: str, version: int, text: str):
        self.documents[file_name] = Document(file_name, language_id, version, text)

    def close_document(self, file_name: str):
        try:
            del self.documents[file_name]
        except KeyError:
            pass

    def get_document(self, file_name: str) -> Document:
        try:
            return self.documents[file_name]
        except KeyError:
            raise errors.InvalidResource(f"{file_name!r} not opened")
