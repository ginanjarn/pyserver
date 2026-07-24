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


def apply_document_changes(document: Document, content_change: List[dict], /) -> None:
    """"""

    line_end = "\n"
    lines = document.text.split(line_end)

    for change in content_change:
        try:
            range_ = change["range"]
            start = LineCharacter(**range_["start"])
            end = LineCharacter(**range_["end"])
            new_text = change["text"]
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params {err}") from err

        srow, scol = start
        erow, ecol = end

        insert = "".join([lines[srow][:scol], new_text, lines[erow][ecol:]])
        lines = lines[:srow] + insert.split(line_end) + lines[erow + 1 :]

    document.text = line_end.join(lines)
    document.is_saved = False
