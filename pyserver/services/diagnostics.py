"""completion service"""

import re
from collections import namedtuple
from dataclasses import dataclass
from io import StringIO
from typing import Dict, Any

from pyflakes import api as pyflakes_api
from pyflakes.reporter import Reporter

from pyserver.message import path_to_uri
from pyserver.services import Services


@dataclass
class DiagnosticParams:
    file_name: str
    text: str
    version: int


Report = namedtuple("Reporte", ["warning", "error"])

# <file_name>:<line>:<column> <message>
warning_regex = re.compile(r"^.+:(\d+):\d+\ (.+)")
# <file_name>:<line>:<column>: <message>
error_regex = re.compile(r".+:(\d+):\d+:\ (.+)")


class DiagnosticService(Services):
    def __init__(self, params: DiagnosticParams):
        self.params = params

    def execute(self) -> Report:
        warning_stream = StringIO()
        error_stream = StringIO()
        reporter = Reporter(warning_stream, error_stream)

        pyflakes_api.check(self.params.text, self.params.file_name, reporter)

        return Report(warning_stream.getvalue(), error_stream.getvalue())

    def build_items(self, report: Report):
        lines = self.params.text.split("\n")

        def build_line_item(pattern, line, severity):
            match = pattern.match(line)
            if not match:
                return None

            line_index = int(match.group(1)) - 1  # pyflakes use 1-based line index
            message = match.group(2)

            return {
                # unable determine error location correctly
                # put the line as range
                "range": {
                    "start": {"line": line_index, "character": 0},
                    "end": {"line": line_index, "character": len(lines[line_index])},
                },
                "severity": severity,
                "source": "pyflakes",
                "message": message,
            }

        if report.error:
            error_lines = report.error.splitlines()
            # pyflakes only report first error occured while checking
            if item := build_line_item(error_regex, error_lines[0], 1):
                yield item

        elif report.warning:
            warning_lines = report.warning.splitlines()
            for w_line in warning_lines:
                if item := build_line_item(warning_regex, w_line, 2):
                    yield item

    def get_result(self) -> Dict[str, Any]:
        report = self.execute()
        return {
            "uri": path_to_uri(self.params.file_name),
            "version": self.params.version,
            "diagnostics": list(self.build_items(report)),
        }
