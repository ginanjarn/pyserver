"""formatting service"""

import re
from dataclasses import dataclass
from difflib import unified_diff
from pathlib import Path
from typing import Dict, Any, List

import black

from pyserver.services import Services


@dataclass
class FormattingParams:
    file_path: Path
    text: Path


class FormattingService(Services):
    def __init__(self, params: FormattingParams):
        self.params = params

    def execute(self) -> str:
        try:
            new_str = black.format_str(self.params.text, mode=black.FileMode())
        except black.NothingChanged:
            return self.params.text
        else:
            return new_str

    signature_regex = re.compile(r"@@\ \-(\d+)(?:,(\d+))?\ \+(\d+)(?:,(\d+))? @@")

    @staticmethod
    def build_items(diff_text: str, origin: str):
        origin_lines = origin.split("\n")
        diff_lines = diff_text.split("\n")

        item_range = None
        buffer = []

        for line in diff_lines:

            if line.startswith("---") or line.startswith("+++"):
                continue

            if line.startswith("-"):
                continue

            if line.startswith("+"):
                buffer.append(line[1:])
                continue

            if line.startswith(" "):
                buffer.append(line[1:])
                continue

            if line.startswith("@@"):
                if item_range:
                    yield {"range": item_range, "newText": "\n".join(buffer)}

                match = FormattingService.signature_regex.match(line)
                if not match:
                    raise ValueError("unable parse diff signature")

                rem_start_line = int(match.group(1)) - 1  # diff use 1-based line index
                # add_start_line = int(match.group(3)) - 1  # diff use 1-based line index

                rem_changed_line = int(match.group(2)) - 1 if match.group(2) else 0
                # add_changed_line = int(match.group(4)) - 1 if match.group(4) else 0
                rem_end_line = rem_start_line + rem_changed_line
                # add_end_line = add_start_line + add_changed_line

                # set block
                item_range = {
                    "start": {"line": rem_start_line, "character": 0},
                    "end": {
                        "line": rem_end_line,
                        "character": len(origin_lines[rem_end_line]),
                    },
                }
                buffer = []

        # yield last block
        if item_range:
            yield {"range": item_range, "newText": "\n".join(buffer)}

    def get_result(self) -> List[Dict[str, Any]]:
        formatted_str = self.execute()
        if formatted_str == self.params.text:
            return []

        udiff = unified_diff(
            self.params.text.split("\n"),
            formatted_str.split("\n"),
            str(self.params.file_path),
            str(self.params.file_path),
        )
        diff_text = "\n".join(udiff)
        return list(self.build_items(diff_text, self.params.text))
