"""formatting service"""

import sys
from dataclasses import dataclass
from typing import Dict, Any, List

import black

from pyserver.services import diffutils
from pyserver import errors
from pyserver.workspace import (
    Document,
    Workspace,
    VersionedDocument,
    uri_to_path,
)


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

        except Exception as err:
            print(err, file=sys.stderr)
            return text

        else:
            return new_str

    def get_result(self) -> List[Dict[str, Any]]:
        formatted_str = self.execute()
        return diffutils.get_text_changes(self.params.text(), formatted_str)


def textdocument_formatting(workspace: Workspace, params: dict) -> None:
    try:
        file_path = uri_to_path(params["textDocument"]["uri"])
    except KeyError as err:
        raise errors.InvalidParams(f"invalid params: {err}") from err

    with VersionedDocument(workspace.get_document(file_path)) as document:
        params = FormattingParams(document)
        service = FormattingService(params)
        return service.get_result()
