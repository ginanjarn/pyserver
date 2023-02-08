"""completion service"""

import re
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Dict, Any, Iterator

from pyflakes import api as pyflakes_api
from pyflakes.reporter import Reporter

from pyserver.message import path_to_uri
from pyserver.services import Services


@dataclass
class DiagnosticParams:
    file_path: Path
    text: str
    version: int


KIND_ERROR = 1
KIND_WARNING = 2

PYFLAKES_REGEX = {
    # <file_name>:<line>:<column>: <message>
    KIND_ERROR: re.compile(r".+:(\d+):\d+:\ (.+)"),
    # <file_name>:<line>:<column> <message>
    KIND_WARNING: re.compile(r"^.+:(\d+):\d+\ (.+)"),
}


@dataclass
class ReportItem:
    source: str
    severity_kind: int
    lineno: int
    message: str


@dataclass
class Report:
    source: str
    error: str
    warning: str

    def _parse_report(self, kind: int):
        report = {KIND_ERROR: self.error, KIND_WARNING: self.warning}[kind]
        # pyflakes report pattern
        regex = PYFLAKES_REGEX[kind]

        for line in report.splitlines():
            if match := regex.match(line):
                lineno, message = match.groups()
                # use zero based line index
                lineno = int(lineno) - 1
                yield ReportItem(self.source, kind, int(lineno), message)

    def get_items(self) -> Iterator[ReportItem]:
        if self.error:
            yield from self._parse_report(KIND_ERROR)

        elif self.warning:
            yield from self._parse_report(KIND_WARNING)


class DiagnosticService(Services):
    def __init__(self, params: DiagnosticParams):
        self.params = params

    def execute(self) -> Report:

        # get pyflakes report
        warning_buffer = StringIO()
        error_buffer = StringIO()

        reporter = Reporter(warning_buffer, error_buffer)
        pyflakes_api.check(self.params.text, str(self.params.file_path), reporter)

        return Report(
            "pyflakes", warning=warning_buffer.getvalue(), error=error_buffer.getvalue()
        )

    def build_items(self, report: Report) -> Iterator[Dict[str, Any]]:
        lines = self.params.text.split("\n")

        def build_line_item(item: ReportItem):
            return {
                # unable determine error location correctly
                # put the line as range
                "range": {
                    "start": {"line": item.lineno, "character": 0},
                    "end": {"line": item.lineno, "character": len(lines[item.lineno])},
                },
                "severity": item.severity_kind,
                "source": item.source,
                "message": item.message,
            }

        for item in report.get_items():
            yield build_line_item(item)

    def get_result(self) -> Dict[str, Any]:
        report = self.execute()
        return {
            "uri": path_to_uri(self.params.file_path),
            "version": self.params.version,
            "diagnostics": list(self.build_items(report)),
        }
