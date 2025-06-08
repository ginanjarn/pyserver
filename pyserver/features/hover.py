"""document hover"""

from dataclasses import dataclass
from html import escape
from io import StringIO
from pathlib import Path
from textwrap import indent
from typing import List, Dict, Any

from jedi import Script, Project
from jedi.api.classes import Name, Signature
from parso.tree import Leaf

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


class HoverProvider:
    def __init__(self, params: HoverParams):
        self.params = params
        self.script = Script(
            self.params.text,
            path=self.params.file_path,
            project=Project(self.params.workspace_path),
        )
        self.leaf_range = {}

    def execute(self) -> List[Name]:
        leaf = self.script._module_node.get_leaf_for_position(self.params.jedi_rowcol())

        # only show documentation for keyword and identifier
        if (not leaf) or leaf.type not in {"keyword", "name"}:
            return []

        self.leaf_range = self._get_leaf_range(leaf)

        row, col = self.params.jedi_rowcol()
        return self.script.help(row, col)

    @staticmethod
    def _get_leaf_range(leaf: Leaf) -> Dict[str, Any]:
        start, end = leaf.start_pos, leaf.end_pos
        return {
            "start": {"line": start[0] - 1, "character": start[1]},
            "end": {"line": end[0] - 1, "character": end[1]},
        }

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

    def build_content(self, name: Name) -> str:
        buffer = StringIO()
        buffer.write(f"### {name.type} `{name.name}`\n\n")

        if (module_name := name.module_name) and module_name != "__main__":
            buffer.write(f"module: `{module_name}`\n\n")

        if name.type in {"class", "function"}:
            if signatures := name.get_signatures():
                signatures = [self.signature_to_string(s) for s in signatures]
                signatures = "\n".join(signatures)
                buffer.write(f"```python\n{signatures}\n```\n\n")

        if docstring := name._get_docstring():
            buffer.write(f"<pre>{escape(docstring, quote=False)}</pre>\n\n")

        return buffer.getvalue()

    def get_documentation(self) -> Dict[str, Any]:
        try:
            candidates = self.execute()
        except Exception:
            candidates = []

        if not candidates:
            return None

        # transform as rpc
        name_object = candidates[0]

        result = {
            "contents": {
                "kind": "markdown",
                "value": self.build_content(name_object),
            },
            "range": self.leaf_range,
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
    service = HoverProvider(params)
    return service.get_documentation()
