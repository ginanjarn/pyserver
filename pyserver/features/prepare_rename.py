"""document prepare rename"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional

from jedi import Script, Project

from pyserver import errors
from pyserver.uri import uri_to_path
from pyserver.session import Session


@dataclass
class PrepareRenameParams:
    workspace_path: Path
    file_path: Path
    text: str
    line: int
    character: int

    def jedi_rowcol(self):
        # jedi use one based line index
        return self.line + 1, self.character


@dataclass
class Identifier:
    start_line: int
    start_character: int
    end_line: int
    end_character: int
    text: str


class PrepareRenameProvider:
    def __init__(self, params: PrepareRenameParams):
        self.params = params
        self.script = Script(
            self.params.text,
            path=self.params.file_path,
            project=Project(self.params.workspace_path),
        )

    def execute(self) -> Optional[Identifier]:
        # get leaf position
        leaf = self.script._module_node.get_leaf_for_position(self.params.jedi_rowcol())

        # only rename identifier
        if (not leaf) or (leaf.type != "name"):
            return None

        # check object reference
        names = self.script.goto(*self.params.jedi_rowcol(), follow_imports=True)
        for name in names:
            if name.in_builtin_module():
                raise ValueError("unable rename 'builtin'")

            path = Path(self.params.workspace_path, name.module_path).resolve()
            if not path.is_file():
                # only rename object inside of project
                raise ValueError("unable rename object referenced to external project")

        start_line, start_col = leaf.start_pos
        end_line, end_col = leaf.end_pos
        return Identifier(start_line - 1, start_col, end_line - 1, end_col, leaf.value)

    def get_rename_target(self) -> Optional[Dict[str, Any]]:
        candidate = self.execute()
        if not candidate:
            return None

        return {
            "range": {
                "start": {
                    "line": candidate.start_line,
                    "character": candidate.start_character,
                },
                "end": {
                    "line": candidate.end_line,
                    "character": candidate.end_character,
                },
            },
            "placeholder": candidate.text,
        }


def textdocument_preparerename(session: Session, params: dict) -> None:
    try:
        file_path = uri_to_path(params["textDocument"]["uri"])
        line = params["position"]["line"]
        character = params["position"]["character"]
    except KeyError as err:
        raise errors.InvalidParams(f"invalid params: {err}") from err

    document = session.get_document(file_path)
    params = PrepareRenameParams(
        document.workspace_path,
        document.file_path,
        document.text,
        line,
        character,
    )
    service = PrepareRenameProvider(params)
    return service.get_rename_target()
