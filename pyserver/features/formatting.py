"""formatting service"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List

import black

from pyserver.features import diffutils
from pyserver import errors
from pyserver.uri import uri_to_path
from pyserver.session import Session


@dataclass
class FormattingParams:
    file_path: Path
    text: str


class FormattingService:
    def __init__(self, params: FormattingParams):
        self.params = params

    def execute(self) -> str:
        text = self.params.text
        try:
            return black.format_str(text, mode=black.Mode())

        except (black.NothingChanged, black.InvalidInput):
            return text

    def get_result(self) -> List[Dict[str, Any]]:
        formatted_str = self.execute()
        return diffutils.get_text_changes(self.params.text, formatted_str)


def textdocument_formatting(session: Session, params: dict) -> None:
    try:
        file_path = uri_to_path(params["textDocument"]["uri"])
    except KeyError as err:
        raise errors.InvalidParams(f"invalid params: {err}") from err

    document = session.get_document(file_path)
    params = FormattingParams(
        document.file_path,
        document.text,
    )
    service = FormattingService(params)
    return service.get_result()
