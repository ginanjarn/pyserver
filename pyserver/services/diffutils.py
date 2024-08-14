"""text diff helper"""

import difflib
from typing import Iterator, List


def _get_text_changes(old: str, new: str, group_size: int = 3) -> Iterator[dict]:
    """get text changes"""

    line_separator = "\n"

    # SequenceMatcher requires old and new to be a list
    old = old.split(line_separator)
    new = new.split(line_separator)

    # See implementation reference in 'difflib.unified_diff'
    for group in difflib.SequenceMatcher(None, old, new).get_grouped_opcodes(
        group_size
    ):
        first, last = group[0], group[-1]
        start_removed_line_index, end_remove_line_index = first[1], last[2] - 1

        removed_lines = []
        add_lines = []

        for tag, i1, i2, j1, j2 in group:
            if tag == "equal":
                for line in old[i1:i2]:
                    removed_lines.append(line)
                    add_lines.append(line)
                continue
            if tag in {"replace", "delete"}:
                for line in old[i1:i2]:
                    removed_lines.append(line)
            if tag in {"replace", "insert"}:
                for line in new[j1:j2]:
                    add_lines.append(line)

        removed_text = line_separator.join(removed_lines)
        added_text = line_separator.join(add_lines)

        yield {
            "range": {
                "start": {"line": start_removed_line_index, "character": 0},
                "end": {
                    "line": end_remove_line_index,
                    "character": len(removed_lines[-1]),
                },
            },
            "newText": added_text,
            "rangeLength": len(removed_text),
        }


def get_text_changes(old: str, new: str) -> List[dict]:
    """get text changes"""
    return list(_get_text_changes(old, new, group_size=1))
