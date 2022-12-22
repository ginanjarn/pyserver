"""hover service"""

import re
from dataclasses import dataclass
from html import escape
from io import StringIO
from typing import List, Dict, Any

from jedi import Script, Project
from jedi.api.classes import Name

from pyserver.services import Services


@dataclass
class HoverParams:
    root_path: str
    file_name: str
    text: str
    line: int
    character: int

    def jedi_rowcol(self):
        # jedi use one based line index
        return self.line + 1, self.character


class HoverService(Services):
    def __init__(self, params: HoverParams):
        self.params = params

    def execute(self) -> List[Name]:
        project = Project(self.params.root_path)
        script = Script(self.params.text, path=self.params.file_name, project=project)
        row, col = self.params.jedi_rowcol()
        return script.help(row, col)

    def build_item(self, name: Name):
        buffer = StringIO()

        if mod := name.module_name:
            if mod != "__main__":
                buffer.write(f"module: `{mod}`\n\n")

        if name.type in {"class", "function"}:
            buffer.write(f"### {name.type} `{name.name}`\n\n")

        if name.type != "module":
            content = name._get_docstring_signature() or name.name
            buffer.write(f"```python\n{content}\n```\n\n")

        if description := name._get_docstring():
            buffer.write(f"<pre>{escape(description, quote=False)}</pre>\n\n")

        return buffer.getvalue()

    name_regex = re.compile(r"\w+$")

    def get_result(self) -> Dict[str, Any]:
        candidates = self.execute()

        if not candidates:
            return None

        # transform as rpc
        name_object = candidates[0]
        line_occurence = self.params.text.splitlines()[self.params.line]
        if found := self.name_regex.search(line_occurence[: self.params.character]):
            column = found.start()
        else:
            column = self.params.character

        result = {
            "contents": {
                "kind": "markdown",
                "value": self.build_item(name_object),
            },
            "range": {
                "start": {"line": self.params.line, "character": column},
                "end": {
                    "line": self.params.line,
                    "character": column + len(name_object.name),
                },
            },
        }
        return result
