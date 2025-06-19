"""Document object"""

from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path
from typing import List

from pyserver import errors


@dataclass
class Document:
    """Document object"""

    workspace_path: Path
    file_path: Path
    language_id: str
    version: int
    text: str = ""
    is_saved: bool = False


LineCharacter = namedtuple("LineCharacter", ["line", "character"])


class OffsetCalculator:
    def __init__(self, text: str) -> None:
        self.lines = text.splitlines(keepends=True)
        self.text_len = len(text)

    def get_offset(self, row: int, column: int) -> int:
        line_offset = sum([len(l) for l in self.lines[:row]])
        return line_offset + column

    def get_rowcolumn(self, offset: int) -> tuple[int, int]:
        calculated_len = 0
        for index, line in enumerate(self.lines):
            if (temp := calculated_len + len(line)) and temp < offset:
                calculated_len = temp
                continue
            return index, offset - calculated_len
        return 0, 0


def _update_text(old_text: str, changes: List[dict]) -> str:
    temp = old_text

    for change in changes:
        try:
            start = LineCharacter(**change["range"]["start"])
            end = LineCharacter(**change["range"]["end"])
            new_text = change["text"]

        except KeyError as err:
            raise errors.InvalidParams(f"invalid params {err}") from err

        calculator = OffsetCalculator(temp)
        start_offset = calculator.get_offset(*start)
        end_offset = calculator.get_offset(*end)

        temp = f"{temp[:start_offset]}{new_text}{temp[end_offset:]}"

    return temp


def apply_document_changes(document: Document, content_change: List[dict], /) -> None:
    """"""
    new_text = _update_text(document.text, content_change)
    document.text = new_text
    document.is_saved = False
