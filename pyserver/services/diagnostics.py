"""completion service"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Iterator, Iterable, List

from pyflakes import api as pyflakes_api
from pyflakes import reporter as pyflakes_reporter
from pyflakes import messages as pyflakes_messages

from pyserver import errors
from pyserver.workspace import (
    Workspace,
    uri_to_path,
    path_to_uri,
)


@dataclass
class DiagnosticParams:
    workspace_path: Path
    file_path: Path
    text: str
    version: int


KIND_ERROR = 1
KIND_WARNING = 2


@dataclass
class Diagnostic:
    severity: int
    file_name: str
    line: int
    column: int
    message: str
    source: str


class PyflakesReporter(pyflakes_reporter.Reporter):
    """Custom Reporter adapted from 'pyflakes.Reporter'"""

    def __init__(self):
        self.reports: List[Diagnostic] = []

    def unexpectedError(self, filename, msg):
        pass

    def syntaxError(self, filename, msg, lineno, offset, text):
        # lineno might be None if the error was during tokenization
        # lineno might be 0 if the error came from stdin
        lineno = lineno or 1
        offset = offset or 1

        # some versions of python emit an offset of -1 for certain encoding errors
        offset = max(offset, 1)

        # python ast use 1-based index
        lineno -= 1
        offset -= 1
        self.reports.append(
            Diagnostic(KIND_ERROR, filename, lineno, offset, msg, "pyflakes")
        )

    def flake(self, message: pyflakes_messages.Message):
        # look at the '__str__' of 'pyflakes.Message'
        filename = message.filename
        lineno = message.lineno - 1  # use 0-based index
        offset = message.col  # has already use 0-based index
        msg = message.message % message.message_args
        self.reports.append(
            Diagnostic(KIND_WARNING, filename, lineno, offset, msg, "pyflakes")
        )


class PyflakesDiagnostic:
    def __init__(self, file_name: str, text: str, /):
        self.file_name = file_name
        self.text = text

    def get_diagnostic(self) -> Iterator[Diagnostic]:
        reporter = PyflakesReporter()
        n_report = pyflakes_api.check(self.text, self.file_name, reporter)
        if not n_report:
            return

        yield from iter(reporter.reports)


class DiagnosticService:
    def __init__(self, params: DiagnosticParams):
        self.params = params

    def execute(self) -> Diagnostic:
        diagnostic = PyflakesDiagnostic(self.params.file_path, self.params.text)
        return diagnostic.get_diagnostic()

    def build_items(
        self, diagnostics: Iterable[Diagnostic]
    ) -> Iterator[Dict[str, Any]]:
        lines = self.params.text.split("\n")

        def build_line_item(item: Diagnostic):
            return {
                # unable determine error location correctly
                # put the line as range
                "range": {
                    "start": {"line": item.line, "character": 0},
                    "end": {"line": item.line, "character": len(lines[item.line])},
                },
                "severity": item.severity,
                "source": item.source,
                "message": item.message,
            }

        for item in diagnostics:
            yield build_line_item(item)

    def get_result(self) -> Dict[str, Any]:
        diagnostics = self.execute()
        return {
            "uri": path_to_uri(self.params.file_path),
            "version": self.params.version,
            "diagnostics": list(self.build_items(diagnostics)),
        }


def textdocument_publishdiagnostics(workspace: Workspace, params: dict):
    try:
        file_path = uri_to_path(params["textDocument"]["uri"])
    except KeyError as err:
        raise errors.InvalidParams(f"invalid params: {err}") from err

    document = workspace.get_document(file_path)
    params = DiagnosticParams(
        workspace.root_path,
        document.path,
        document.text,
        document.version,
    )
    service = DiagnosticService(params)
    return service.get_result()
