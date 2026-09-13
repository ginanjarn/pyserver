from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Union

import black

from . import diffutils
from ...base_server import BaseServer
from ...lsprotocol.server import DocumentFormattingParams, TextEdit
from ...uri import uri_to_path


@dataclass
class Params:
    file_path: Path
    text: str


class FormattingProvider:
    def __init__(self, params: Params):
        self.params = params

    def execute(self) -> str:
        text = self.params.text
        try:
            return black.format_str(text, mode=black.Mode())

        except (black.NothingChanged, black.InvalidInput):
            return text

    def get_formatted(self) -> List[Dict[str, Any]]:
        formatted_str = self.execute()

        if formatted_str == self.params.text:
            return None
        return diffutils.get_text_changes(self.params.text, formatted_str)


class DocumentFormattingMixin(BaseServer):
    def handle_document_formatting_request(
        self, context: dict, params: DocumentFormattingParams
    ) -> Union[List[TextEdit], None]:

        file_name = uri_to_path(params.textDocument.uri)
        document = self.session.get_document(file_name)

        params = Params(
            document.file_name,
            document.text,
        )
        service = FormattingProvider(params)
        return service.get_formatted()
