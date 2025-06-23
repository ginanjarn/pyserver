"""document diagnostics"""

from ast import parse, AST, Module, walk
from dataclasses import dataclass
from collections import namedtuple
from pathlib import Path
from typing import Dict, Any, Iterator, Optional

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
        if not isinstance(node, Module):
            raise ValueError("node must %s" % Module)

        # nodes location must sorted
        self.nodes = list(
            sorted(
                [n for n in walk(node) if hasattr(n, "lineno")],
                key=lambda n: (n.lineno, n.col_offset),
            )
        )

        self._prev_location = RowCol(0, 0)
        self._anchor = 0

    def get_leaf_at(self, location: RowCol) -> Optional[AST]:
        """get leaf at location"""
        return self._get_leaf_at(location)

    def _get_leaf_at(self, location: RowCol) -> Optional[AST]:
        # Search location must incremented to avoid search from parent
        if location < self._prev_location:
            raise ValueError(f"location must greater than {self._prev_location}")
        self._prev_location = location

        target: AST = None

        # Find leaf from children
        # Search from anchored location not from beginning for eficiency
        for index in range(self._anchor, len(self.nodes)):
            leaf = self.nodes[index]
            start, end = (
                (leaf.lineno, leaf.col_offset),
                (leaf.end_lineno, leaf.end_col_offset),
            )
            if start > location:
                break
            if start <= location <= end:
                target = leaf
                # update anchor to current node
                self._anchor = index

        if target:
            return target

        # Not found in children
        # Find leaf from parent, find nearest leaf from end
        for rindex in range(self._anchor, 0, -1):
            leaf = self.nodes[rindex]
            start, end = (
                (leaf.lineno, leaf.col_offset),
                (leaf.end_lineno, leaf.end_col_offset),
            )
            if end < location:
                break
            if start <= location <= end:
                target = leaf
                # In here we use reverse index, don't update anchor

        return target


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


class DiagnosticProvider:
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

    def get_diagnostics(self) -> Dict[str, Any]:
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
    service = DiagnosticProvider(params)
    return service.get_diagnostics()
