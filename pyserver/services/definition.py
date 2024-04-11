"""completion service"""

from dataclasses import dataclass
from typing import List, Dict, Any

from jedi import Script, Project
from jedi.api.classes import Name

from pyserver import errors
from pyserver.workspace import (
    Document,
    Workspace,
    VersionedDocument,
    uri_to_path,
    path_to_uri,
)


@dataclass
class DefinitionParams:
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


class DefinitionService:
    def __init__(self, params: DefinitionParams):
        self.params = params
        self.script = Script(
            self.params.text(),
            path=self.params.file_path(),
            project=Project(self.params.workspace().root_path),
        )
        self.identifier_leaf = self.script._module_node.get_leaf_for_position(
            self.params.jedi_rowcol()
        )

    def execute(self) -> List[dict]:
        # only show definition for identifier
        if (not self.identifier_leaf) or self.identifier_leaf.type != "name":
            return []

        row, col = self.params.jedi_rowcol()
        return self.script.goto(row, col, follow_imports=True)

    def build_items(self, names: List[Name]):
        # jedi rows start with 1, columns start with 0
        default = (1, 0)

        for name in names:
            try:
                path = name.module_path
                start = name.get_definition_start_position() or default
                end = name.get_definition_end_position() or default
            except Exception:
                continue

            # may be path unknown
            if not path:
                continue

            item = {
                "uri": path_to_uri(str(path)),
                "range": {
                    "start": {"line": start[0] - 1, "character": start[1]},
                    "end": {"line": end[0] - 1, "character": end[1]},
                },
            }
            yield item

    def get_result(self) -> Dict[str, Any]:
        candidates = self.execute()

        # transform as rpc
        result = list(self.build_items(candidates))
        return result


def textdocument_definition(workspace: Workspace, params: dict) -> None:
    try:
        file_path = uri_to_path(params["textDocument"]["uri"])
        line = params["position"]["line"]
        character = params["position"]["character"]
    except KeyError as err:
        raise errors.InvalidParams(f"invalid params: {err}") from err

    with VersionedDocument(workspace.get_document(file_path)) as document:
        params = DefinitionParams(document, line, character)
        service = DefinitionService(params)
        return service.get_result()
