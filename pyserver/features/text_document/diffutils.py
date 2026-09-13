"""text diff helper"""

import difflib
from typing import Iterator, List


def _get_text_changes(old: str, new: str, delta: int = 3) -> Iterator[dict]:
    """get text changes"""

    line_separator = "\n"

    # SequenceMatcher requires old and new to be a list
    old = old.split(line_separator)
    new = new.split(line_separator)

    # See implementation reference in 'difflib.unified_diff'
    for groups in difflib.SequenceMatcher(None, old, new).get_grouped_opcodes(delta):
        first_group, last_group = groups[0], groups[-1]
        start_removed_line, end_remove_line = (first_group[1], last_group[2] - 1)

        removed_lines = []
        insert_lines = []

        for tag, i1, i2, j1, j2 in groups:
            if tag == "equal":
                for line in old[i1:i2]:
                    removed_lines.append(line)
                    insert_lines.append(line)
                continue
            if tag in {"replace", "delete"}:
                for line in old[i1:i2]:
                    removed_lines.append(line)
            if tag in {"replace", "insert"}:
                for line in new[j1:j2]:
                    insert_lines.append(line)

        removed_text = line_separator.join(removed_lines)
        insert_text = line_separator.join(insert_lines)

        yield {
            "range": {
                "start": {"line": start_removed_line, "character": 0},
                "end": {
                    "line": end_remove_line,
                    "character": len(removed_lines[-1]),
                },
            },
            "newText": insert_text,
            "rangeLength": len(removed_text),
        }


def get_text_changes(old: str, new: str) -> List[dict]:
    """get text changes"""
    return list(_get_text_changes(old, new, delta=1))
