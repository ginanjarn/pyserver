"""completion service"""

import ast
from dataclasses import dataclass
from collections import namedtuple
from pathlib import Path
from typing import Dict, Any, Iterator, Iterable

from pyflakes import checker

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

RowCol = namedtuple("RowCol", ["row", "column"])
TextRange = namedtuple("TextRange", ["start", "end"])


@dataclass
class Diagnostic:
    severity: int
    file_name: str
    text_range: TextRange
    message: str
    source: str


class PyflakesDiagnostic:
    def __init__(self, file_name: str, text: str, /):
        self.file_name = file_name
        self.text = text

    def get_diagnostic(self) -> Iterator[Diagnostic]:
        yield from self._check(self.file_name, self.text)

    def _check(self, filename: str, source: str, /) -> Iterator[Diagnostic]:
        try:
            tree = ast.parse(source, filename=filename)

        except SyntaxError as err:
            yield from self._get_error(err, filename)
        else:
            yield from self._get_warnings(tree, filename)

    def _get_error(self, err: SyntaxError, filename: str) -> Iterator[Diagnostic]:

        # lineno might be None if the error was during tokenization
        # lineno might be 0 if the error came from stdin
        lineno = err.lineno or 1
        offset = err.offset or 1

        # some versions of python emit an offset of -1 for certain encoding errors
        offset = max(offset, 1)

        # python ast use 1-based line index
        lineno -= 1
        offset -= 1

        msg = err.args[0]

        # entire error line as range
        lines = self.text.splitlines()
        start = RowCol(lineno, 0)
        end = RowCol(lineno, len(lines[lineno]))
        text_range = TextRange(start, end)
        yield Diagnostic(KIND_ERROR, filename, text_range, msg, "pyflakes")

    def _get_warnings(self, node: ast.AST, filename: str) -> Iterator[Diagnostic]:

        w = checker.Checker(node, filename=filename)
        w.messages.sort(key=lambda m: m.lineno)

        for message in w.messages:
            # look at the '__str__' of 'pyflakes.Message'
            filename = message.filename
            lineno = message.lineno
            offset = message.col
            msg = message.message % message.message_args

            text_range = self._get_leaf_range(node, RowCol(lineno, offset))
            yield Diagnostic(KIND_WARNING, filename, text_range, msg, "pyflakes")

    def _get_leaf_range(self, node: ast.AST, location: RowCol) -> TextRange:
        visitor = FindLeafVisitor(*location)
        visitor.visit(node)
        target_node = visitor.target_node

        # python ast use 1-based line index
        start = RowCol(target_node.lineno - 1, target_node.col_offset)
        end = RowCol(target_node.end_lineno - 1, target_node.end_col_offset)
        return TextRange(start, end)


class FindLeafVisitor(ast.NodeVisitor):
    def __init__(self, line: int, col: int, /) -> None:
        self.line = line
        self.col = col
        self.target_node = None

    def visit(self, node: ast.AST) -> Any:
        try:
            if (node.lineno <= self.line) and (self.line <= node.end_lineno):
                if (node.col_offset <= self.col) and (self.col <= node.end_col_offset):
                    self.target_node = node
        except AttributeError:
            pass

        self.generic_visit(node)


class DiagnosticService:
    def __init__(self, params: DiagnosticParams):
        self.params = params

    def execute(self) -> Diagnostic:
        diagnostic = PyflakesDiagnostic(self.params.file_path, self.params.text)
        return diagnostic.get_diagnostic()

    def build_items(
        self, diagnostics: Iterable[Diagnostic]
    ) -> Iterator[Dict[str, Any]]:

        def build_line_item(item: Diagnostic):
            start, end = item.text_range

            return {
                "range": {
                    "start": {"line": start.row, "character": start.column},
                    "end": {"line": end.row, "character": end.column},
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
