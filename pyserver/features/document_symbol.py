"""document symbol"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Iterator

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
        return self.script.get_names()

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

    def _build_items(self, names: List[Name]) -> Iterator[dict]:
        for name in names:
            name_str = name.name
            name_type = name.type
            start = name.line, name.column
            end = name.line, name.column + len(name_str)

            yield {
                "name": name_str,
                "kind": self.SYMBOL_KIND[name_type],
                "range": {
                    "start": {"line": start[0] - 1, "character": start[1]},
                    "end": {"line": end[0] - 1, "character": end[1]},
                },
            }

            # get symbol defined in a class
            if not name.get_line_code().strip().startswith("class"):
                continue

            for subname in name.defined_names():
                sn_str = subname.name
                sn_type = subname.type
                sn_start = subname.line, subname.column
                sn_end = subname.line, subname.column + len(sn_str)

                yield {
                    "name": f"{name_str}.{sn_str}",
                    "kind": self.SYMBOL_KIND[sn_type],
                    "range": {
                        "start": {"line": sn_start[0] - 1, "character": sn_start[1]},
                        "end": {"line": sn_end[0] - 1, "character": sn_end[1]},
                    },
                }

    def get_symbols(self) -> Dict[str, Any]:
        try:
            candidates = self.execute()
        except Exception:
            candidates = []

        if not candidates:
            return None

        # transform as rpc
        return list(self._build_items(candidates))


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
