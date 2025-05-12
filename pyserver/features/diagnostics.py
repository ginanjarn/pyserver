"""completion service"""

from ast import parse, AST, walk
from dataclasses import dataclass
from collections import namedtuple
from pathlib import Path
from typing import Dict, Any, Iterator, Optional, List

from pyflakes import checker

from pyserver import errors
from pyserver.uri import uri_to_path, path_to_uri
from pyserver.session import Session


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
            tree = parse(source, filename=filename)

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

    def _get_warnings(self, node: AST, filename: str) -> Iterator[Diagnostic]:

        w = checker.Checker(node, filename=filename)
        w.messages.sort(key=lambda m: (m.lineno, m.col))

        leaf_getter = LeafGetter(node)

        for message in w.messages:
            # look at the '__str__' of 'pyflakes.Message'
            filename = message.filename
            lineno = message.lineno
            offset = message.col
            msg = message.message % message.message_args

            leaf = leaf_getter.get_leaf_at(RowCol(lineno, offset))
            text_range = get_leaf_range(leaf)
            yield Diagnostic(KIND_WARNING, filename, text_range, msg, "pyflakes")


class LeafGetter:
    """Get leaf from a node without check from beginning"""

    def __init__(self, node: AST) -> None:
        # Only select node which has location
        self.nodes = [n for n in walk(node) if hasattr(n, "lineno")]
        self.nodes.sort(key=lambda n: (n.lineno, n.col_offset))

        self._previous_location = RowCol(0, 0)
        self._iter_index = 0

    def get_leaf_at(self, location: RowCol) -> Optional[AST]:
        """get leaf at location"""
        if location < self._previous_location:
            raise ValueError(f"location must greater than {self._previous_location}")

        self._previous_location = location
        current_index = self._iter_index

        # get from child
        if leaf := self._get_leaf(self.nodes[current_index:], location):
            return leaf

        # get from nearest parent
        if leaf := self._get_leaf(
            reversed(self.nodes[:current_index]), location, increment_index=False
        ):
            return leaf

        # revert index if not found
        self._iter_index = current_index
        return None

    def _get_leaf(
        self, nodes: List[AST], location: RowCol, *, increment_index: bool = True
    ) -> Optional[AST]:
        for node in nodes:
            if increment_index:
                self._iter_index += 1

            start = (node.lineno, node.col_offset)
            end = (node.end_lineno, node.end_col_offset)

            if start <= location <= end:
                # find narrower node
                current_index = self._iter_index
                if narrower := self._get_leaf(self.nodes[current_index:], location):
                    return narrower

                # revert index if not found
                self._iter_index = current_index
                return node

            if start > location and increment_index:
                return None

        return None


def get_leaf_at(node: AST, location: RowCol) -> Optional[AST]:
    """get ast leaf at location"""
    leaf_getter = LeafGetter(node)
    return leaf_getter.get_leaf_at(location)


def get_leaf_range(leaf: AST) -> TextRange:
    """get ast leaf range at location"""

    # python ast use 1-based line index
    start = RowCol(leaf.lineno - 1, leaf.col_offset)
    end = RowCol(leaf.end_lineno - 1, leaf.end_col_offset)
    return TextRange(start, end)


class DiagnosticService:
    def __init__(self, params: DiagnosticParams):
        self.params = params

    def execute(self) -> Iterator[Diagnostic]:
        diagnostic = PyflakesDiagnostic(self.params.file_path, self.params.text)
        return diagnostic.get_diagnostic()

    def build_item(self, item: Diagnostic) -> dict:
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

    def get_result(self) -> Dict[str, Any]:
        diagnostics = self.execute()
        return {
            "uri": path_to_uri(self.params.file_path),
            "version": self.params.version,
            "diagnostics": [self.build_item(d) for d in diagnostics],
        }


def textdocument_publishdiagnostics(session: Session, params: dict):
    try:
        file_path = uri_to_path(params["textDocument"]["uri"])
    except KeyError as err:
        raise errors.InvalidParams(f"invalid params: {err}") from err

    document = session.get_document(file_path)
    params = DiagnosticParams(
        document.workspace_path,
        document.file_path,
        document.text,
        document.version,
    )
    service = DiagnosticService(params)
    return service.get_result()
