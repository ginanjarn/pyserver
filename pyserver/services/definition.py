"""completion service"""

from dataclasses import dataclass
from typing import List, Dict, Any

from jedi import Script, Project
from jedi.api.classes import Name

from pyserver.message import path_to_uri
from pyserver.services import Services


@dataclass
class DefinitionParams:
    root_path: str
    file_name: str
    text: str
    line: int
    character: int

    def jedi_rowcol(self):
        # jedi use one based line index
        return self.line + 1, self.character


class DefinitionService(Services):
    def __init__(self, params: DefinitionParams):
        self.params = params
        self._text_edit_range = None

    def execute(self) -> List[dict]:
        project = Project(self.params.root_path)
        script = Script(self.params.text, path=self.params.file_name, project=project)
        row, col = self.params.jedi_rowcol()
        return script.goto(row, col, follow_imports=True)

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
