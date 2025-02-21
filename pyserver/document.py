"""Document object"""

from dataclasses import dataclass
from pathlib import Path
from typing import List

from pyserver import errors
from pyserver.uri import path_to_uri


@dataclass
class Document:
    """Document object"""

    workspace_path: Path
    file_path: Path
    language_id: str
    version: int
    text: str = ""
    is_saved: bool = False

    @property
    def document_uri(self) -> str:
        """document uri"""
        return path_to_uri(self.file_path)

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
