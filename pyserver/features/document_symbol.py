"""document symbol"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

from jedi import Script, Project
from jedi.api.classes import Name

from pyserver import errors
from pyserver.uri import uri_to_path
from pyserver.session import Session


@dataclass
class SymbolParams:
    workspace_path: Path
    file_path: Path
    text: str


class DocumentSymbolProvider:
    def __init__(self, params: SymbolParams):
        self.params = params
        self.script = Script(
            self.params.text,
            path=self.params.file_path,
            project=Project(self.params.workspace_path),
        )

    def execute(self) -> List[Name]:
        return self.script.get_names(all_scopes=True, definitions=True)

    SYMBOL_KIND = {
        "module": 2,
        "class": 5,
        "instance": 5,
        "function": 12,
        "param": 13,
        "path": 1,
        "keyword": 25,
        "property": 13,
        "statement": 13,
    }

    def _build_item(self, name: Name) -> dict:
        name_str = name.name
        start = name.line, name.column
        end = name.line, name.column + len(name_str)

        return {
            "name": name.name,
            "kind": self.SYMBOL_KIND[name.type],
            "range": {
                "start": {"line": start[0] - 1, "character": start[1]},
                "end": {"line": end[0] - 1, "character": end[1]},
            },
        }

    def get_symbols(self) -> Dict[str, Any]:
        try:
            candidates = self.execute()
        except Exception:
            candidates = []

        # transform as rpc
        return [self._build_item(symbol) for symbol in candidates]


def textdocument_symbol(session: Session, params: dict) -> None:
    try:
        file_path = uri_to_path(params["textDocument"]["uri"])
    except KeyError as err:
        raise errors.InvalidParams(f"invalid params: {err}") from err

    document = session.get_document(file_path)
    params = SymbolParams(
        document.workspace_path,
        document.file_path,
        document.text,
    )
    service = DocumentSymbolProvider(params)
    return service.get_symbols()
