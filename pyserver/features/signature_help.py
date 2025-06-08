"""document signature help"""

import time
from dataclasses import dataclass
from pathlib import Path
from textwrap import indent
from typing import List, Dict, Any, Iterator

from jedi import Script, Project
from jedi.api.classes import Signature

from pyserver import errors
from pyserver.uri import uri_to_path
from pyserver.session import Session


@dataclass
class SignatureHelpParams:
    workspace_path: Path
    file_path: Path
    text: str
    line: int
    character: int

    def jedi_rowcol(self):
        # jedi use one based line index
        return self.line + 1, self.character


class SignatureHelpProvider:
    def __init__(self, params: SignatureHelpParams):
        self.params = params
        self.script = Script(
            self.params.text,
            path=self.params.file_path,
            project=Project(self.params.workspace_path),
        )

    def execute(self) -> List[Signature]:
        row, col = self.params.jedi_rowcol()
        return self.script.get_signatures(row, col)

    @staticmethod
    def signature_to_string(signature: Signature) -> str:
        signature_string = signature.to_string()
        if len(signature_string) < 80:
            return signature_string

        # Flatten long signature
        name = signature.name
        params = ",\n".join([p.to_string() for p in signature.params])
        annotation = ""
        if return_type := getattr(signature._signature, "annotation_string"):
            annotation = f" -> {return_type}"

        return f"{name}(\n{indent(params, prefix='  ')}\n){annotation}"

    def build_item(self, signatures: List[Signature]) -> Iterator[dict]:
        for signature in signatures:
            label = self.signature_to_string(signature)
            yield {
                "label": label,
                "documentation": signature.docstring(raw=True),
                "parameters": [
                    {"label": param.name, "documentation": param.description}
                    for param in signature.params
                ],
            }

    def get_signature(self) -> Dict[str, Any]:
        try:
            candidates = self.execute()
        except Exception:
            candidates = []

        return {
            "signatures": list(self.build_item(candidates)),
            "activeSignature": 0,
            "activeParameters": 0,
        }


def textdocument_signaturehelp(session: Session, params: dict) -> None:
    # Improve completion result if called after request completion
    time.sleep(0.5)

    try:
        file_path = uri_to_path(params["textDocument"]["uri"])
        line = params["position"]["line"]
        character = params["position"]["character"]
    except KeyError as err:
        raise errors.InvalidParams(f"invalid params: {err}") from err

    document = session.get_document(file_path)
    params = SignatureHelpParams(
        document.workspace_path,
        document.file_path,
        document.text,
        line,
        character,
    )
    service = SignatureHelpProvider(params)
    return service.get_signature()
