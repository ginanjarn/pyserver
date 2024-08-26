"""signature help service"""

from dataclasses import dataclass
from typing import List, Dict, Any

from jedi import Script, Project
from jedi.api.classes import Signature

from pyserver import errors
from pyserver.workspace import (
    Document,
    Workspace,
    uri_to_path,
)


@dataclass
class SignatureHelpParams:
    document: Document
    line: int
    character: int

    def jedi_rowcol(self):
        # jedi use one based line index
        return self.line + 1, self.character

    def file_path(self):
        return self.document.path

    def text(self):
        return self.document.text

    def workspace(self) -> Workspace:
        return self.document.workspace


class SignatureHelpService:
    def __init__(self, params: SignatureHelpParams):
        self.params = params
        self.script = Script(
            self.params.text(),
            path=self.params.file_path(),
            project=Project(self.params.workspace().root_path),
        )

    def execute(self) -> List[Signature]:
        row, col = self.params.jedi_rowcol()
        return self.script.get_signatures(row, col)

    def build_item(self, signatures: List[Signature]) -> List[dict]:
        # prevent generate signature with same label
        current_label = None

        # for signature in signatures:
        def build_signature(signature: Signature):
            nonlocal current_label

            label = signature.to_string()
            if label == current_label:
                return {}
            # else
            current_label = label

            return {
                "label": label,
                "documentation": signature.docstring(raw=True),
                "parameters": [
                    {"label": param.name, "documentation": param.description}
                    for param in signature.params
                ],
            }

        return [build_signature(signature) for signature in signatures]

    def get_result(self) -> Dict[str, Any]:
        try:
            candidates = self.execute()
        except Exception:
            candidates = []

        signatures = self.build_item(candidates)
        # on duplication signatures return empty dict
        signatures = [s for s in signatures if s]  # remove the empty dict

        result = {
            "signatures": signatures,
            "activeSignature": 0,
            "activeParameters": 0,
        }
        return result


def textdocument_signaturehelp(workspace: Workspace, params: dict) -> None:
    try:
        file_path = uri_to_path(params["textDocument"]["uri"])
        line = params["position"]["line"]
        character = params["position"]["character"]
    except KeyError as err:
        raise errors.InvalidParams(f"invalid params: {err}") from err

    document = workspace.get_document(file_path)
    params = SignatureHelpParams(document, line, character)
    service = SignatureHelpService(params)
    return service.get_result()
