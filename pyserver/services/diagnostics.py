"""completion service"""

import re
from collections import namedtuple
from dataclasses import dataclass
from io import StringIO
from typing import Dict, Any, Iterator, Iterable

from pyflakes import api as pyflakes_api
from pyflakes.reporter import Reporter

from pyserver.workspace import Workspace, Document, path_to_uri


@dataclass
class DiagnosticParams:
    document: Document

    def file_path(self):
        return self.document.path

    def text(self):
        return self.document.text

    def workspace(self) -> Workspace:
        return self.document.workspace

    def version(self):
        return self.document.version


KIND_ERROR = 1
KIND_WARNING = 2


Diagnostic = namedtuple(
    "Diagnostic", ["severity", "file_name", "line", "column", "message", "source"]
)


class PyflakesDiagnostic:
    def __init__(self, file_name: str, text: str, /):
        self.file_name = file_name
        self.text = text

    # pattern '<file_name>:<line>:<column>:? <message>'
    report_pattern = re.compile(r"^(.+):(\d+):(\d+):?\ (.+)")

    def get_diagnostic(self) -> Iterator[Diagnostic]:
        # Pyflakes reporter
        warning_buffer = StringIO()
        error_buffer = StringIO()
        reporter = Reporter(warning_buffer, error_buffer)

        pyflakes_api.check(self.text, self.file_name, reporter)

        yield from self.parse_report(KIND_ERROR, error_buffer)
        yield from self.parse_report(KIND_WARNING, warning_buffer)

    def parse_report(
        self, severity_kind: int, buffer: StringIO
    ) -> Iterator[Diagnostic]:
        # Seek offset to beginnig of buffer
        buffer.seek(0)

        while line := buffer.readline():
            if match := self.report_pattern.match(line):
                file_name, line, column, message = match.groups()
                yield Diagnostic(
                    severity_kind,
                    file_name,
                    int(line) - 1,  # Pyflakes use 1 based line index
                    int(column),
                    message,
                    "pyflakes",
                )


class DiagnosticService:
    def __init__(self, params: DiagnosticParams):
        self.params = params

    def execute(self) -> Diagnostic:
        diagnostic = PyflakesDiagnostic(self.params.file_path(), self.params.text())
        return diagnostic.get_diagnostic()

    def build_items(
        self, diagnostics: Iterable[Diagnostic]
    ) -> Iterator[Dict[str, Any]]:
        lines = self.params.text().split("\n")

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
            "uri": path_to_uri(self.params.file_path()),
            "version": self.params.version(),
            "diagnostics": list(self.build_items(diagnostics)),
        }
