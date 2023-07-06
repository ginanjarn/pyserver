"""formatting service"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List

import black

from pyserver.services import diffutils


@dataclass
class FormattingParams:
    file_path: Path
    text: Path


class FormattingService:
    def __init__(self, params: FormattingParams):
        self.params = params

    def execute(self) -> str:
        try:
            new_str = black.format_str(self.params.text, mode=black.FileMode())
        except black.NothingChanged:
            return self.params.text
        else:
            return new_str

    def get_result(self) -> List[Dict[str, Any]]:
        formatted_str = self.execute()
        return diffutils.get_text_changes(self.params.text, formatted_str)
