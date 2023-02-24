"""hover service"""

from dataclasses import dataclass
from html import escape
from io import StringIO
from pathlib import Path
from typing import List, Dict, Any

from jedi import Script, Project
from jedi.api.classes import Name

from pyserver.services import Services


@dataclass
class HoverParams:
    root_path: Path
    file_path: Path
    text: str
    line: int
    character: int

    def jedi_rowcol(self):
        # jedi use one based line index
        return self.line + 1, self.character


class HoverService(Services):
    def __init__(self, params: HoverParams):
        self.params = params
        self.script = Script(
            self.params.text,
            path=self.params.file_path,
            project=Project(self.params.root_path),
        )
        self.identifier_leaf = self.script._module_node.get_leaf_for_position(
            self.params.jedi_rowcol()
        )

    def execute(self) -> List[Name]:
        # only show documentation for keyword and identifier
        if self.identifier_leaf.type not in {"keyword", "name"}:
            return []

        row, col = self.params.jedi_rowcol()
        return self.script.help(row, col)

    def build_item(self, name: Name):
        buffer = StringIO()

        if (mod := name.module_name) != "__main__":
            buffer.write(f"module: `{mod}`\n\n")

        if name.type in {"class", "function"}:
            buffer.write(f"### {name.type} `{name.name}`\n\n")

        if name.type != "module":
            content = name._get_docstring_signature() or name.name
            buffer.write(f"```python\n{content}\n```\n\n")

        if description := name._get_docstring():
            buffer.write(f"<pre>{escape(description, quote=False)}</pre>\n\n")

        return buffer.getvalue()

    def get_result(self) -> Dict[str, Any]:
        candidates = self.execute()

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
