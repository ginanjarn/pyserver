"""hover service"""

from dataclasses import dataclass
from html import escape
from io import StringIO
from pathlib import Path
from typing import List, Dict, Any

from jedi import Script, Project
from jedi.api.classes import Name

from pyserver import errors
from pyserver.uri import uri_to_path
from pyserver.session import Session


@dataclass
class HoverParams:
    workspace_path: Path
    file_path: Path
    text: str
    line: int
    character: int

    def jedi_rowcol(self):
        # jedi use one based line index
        return self.line + 1, self.character


class HoverService:
    def __init__(self, params: HoverParams):
        self.params = params
        self.script = Script(
            self.params.text,
            path=self.params.file_path,
            project=Project(self.params.workspace_path),
        )
        self.identifier_leaf = self.script._module_node.get_leaf_for_position(
            self.params.jedi_rowcol()
        )

    def execute(self) -> List[Name]:
        # only show documentation for keyword and identifier
        if (leaf := self.identifier_leaf) and leaf.type in {"keyword", "name"}:
            row, col = self.params.jedi_rowcol()
            return self.script.help(row, col)

        return []

    def build_item(self, name: Name):
        buffer = StringIO()
        buffer.write(f"### {name.type} `{name.name}`\n\n")

        if (module_name := name.module_name) and module_name != "__main__":
            buffer.write(f"module: `{module_name}`\n\n")

        if name.type in {"class", "function"}:
            if signature := name._get_docstring_signature():
                buffer.write(f"```python\n{signature}\n```\n\n")

        if docstring := name._get_docstring():
            buffer.write(f"<pre>{escape(docstring, quote=False)}</pre>\n\n")

        return buffer.getvalue()

    def get_result(self) -> Dict[str, Any]:
        try:
            candidates = self.execute()
        except Exception:
            candidates = []

        if not candidates:
            return None

        # transform as rpc
        name_object = candidates[0]

        start = self.identifier_leaf.start_pos
        end = self.identifier_leaf.end_pos

        result = {
            "contents": {
                "kind": "markdown",
                "value": self.build_item(name_object),
            },
            "range": {
                "start": {"line": start[0] - 1, "character": start[1]},
                "end": {
                    "line": end[0] - 1,
                    "character": end[1],
                },
            },
        }
        return result


def textdocument_hover(session: Session, params: dict) -> None:
    try:
        file_path = uri_to_path(params["textDocument"]["uri"])
        line = params["position"]["line"]
        character = params["position"]["character"]
    except KeyError as err:
        raise errors.InvalidParams(f"invalid params: {err}") from err

    document = session.get_document(file_path)
    params = HoverParams(
        document.workspace_path,
        document.file_path,
        document.text,
        line,
        character,
    )
    service = HoverService(params)
    return service.get_result()
