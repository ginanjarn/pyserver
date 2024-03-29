"""formatting service"""

from dataclasses import dataclass
from typing import Dict, Any, List

import black

from pyserver.services import diffutils
from pyserver.workspace import Document


@dataclass
class FormattingParams:
    document: Document

    def text(self):
        return self.document.text


class FormattingService:
    def __init__(self, params: FormattingParams):
        self.params = params

    def execute(self) -> str:
        text = self.params.text()
        try:
            new_str = black.format_str(text, mode=black.FileMode())
        except black.NothingChanged:
            return text
        else:
            return new_str

    def get_result(self) -> List[Dict[str, Any]]:
        formatted_str = self.execute()
        return diffutils.get_text_changes(self.params.text(), formatted_str)
