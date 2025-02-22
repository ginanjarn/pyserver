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


def _get_offset(lines: List[str], row: int, column: int) -> int:
    line_offset = sum([len(l) for l in lines[:row]])
    return line_offset + column


def _update_text(old_text: str, changes: List[dict]) -> str:
    temp = old_text

    for change in changes:
        try:
            start = LineCharacter(**change["range"]["start"])
            end = LineCharacter(**change["range"]["end"])
            new_text = change["text"]

        except KeyError as err:
            raise errors.InvalidParams(f"invalid params {err}") from err

        lines = temp.splitlines(keepends=True)
        start_offset = _get_offset(lines, start.line, start.character)
        end_offset = _get_offset(lines, end.line, end.character)
        temp = f"{temp[:start_offset]}{new_text}{temp[end_offset:]}"

    return temp


def apply_document_changes(document: Document, content_change: List[dict], /) -> None:
    """"""
    new_text = _update_text(document.text, content_change)
    document.text = new_text
    document.is_saved = False
