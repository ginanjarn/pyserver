import threading
import time
from ast import parse, AST, iter_child_nodes
from dataclasses import dataclass
from collections import namedtuple
from pathlib import Path
from typing import Dict, Any, Iterator, List

from pyflakes.checker import Checker
from pyflakes.messages import Message

from ...base_server import BaseServer
from ...lsprotocol.lsprotocol import TextDocumentIdentifier
from ...session import DocumentNotFound
from ...uri import path_to_uri, uri_to_path


@dataclass
class Params:
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

        end_lineno = getattr(err, "end_lineno", lineno)
        end_offset = getattr(err, "end_offset", offset)

        # python ast use 1-based line index
        lineno -= 1
        offset -= 1
        end_lineno -= 1
        end_offset -= 1

        a = RowCol(lineno, offset)
        b = RowCol(end_lineno, end_offset)

        msg = err.msg or err.args[0]
        filename = err.filename or filename
        text_range = TextRange(min(a, b), max(a, b))
        yield Diagnostic(KIND_ERROR, filename, text_range, msg, "ast")

    def _get_warnings(self, node: AST, filename: str) -> Iterator[Diagnostic]:

        w = Checker(node, filename=filename)
        w.messages.sort(key=lambda m: (m.lineno, m.col))

        node_map = find_nodes(node, [(m.lineno, m.col) for m in w.messages])
        yield from (self._build_warning(m, node_map) for m in w.messages)

    def _build_warning(
        self, message: Message, node_map: Dict[RowCol, AST]
    ) -> Diagnostic:

        filename = message.filename
        text_msg = message.message % message.message_args

        node = node_map[(message.lineno, message.col)]
        start = RowCol(node.lineno - 1, node.col_offset)
        end = RowCol(node.end_lineno - 1, node.end_col_offset)

        text_range = TextRange(start, end)
        return Diagnostic(KIND_WARNING, filename, text_range, text_msg, "pyflakes")


def find_nodes(tree: AST, targets: List[RowCol]) -> Dict[RowCol, AST]:
    stack = [tree]
    target_set = set(targets)
    results = {}

    while stack:
        node = stack.pop()
        if hasattr(node, "lineno"):
            pos = (node.lineno, node.col_offset)
            if pos in target_set:
                results[pos] = node
        stack.extend(iter_child_nodes(node))

    return results


class DiagnosticProvider:
    def __init__(self, params: Params):
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


class DocumentDiagnosticMixin(BaseServer):
    publish_event = threading.Event()
    publish_diagnostic_target = None
    publish_thread = None
    publish_interval = 0.5  # second

    def publish_listener(self):
        while True:
            self.publish_event.wait()

            # Consume trigger
            self.publish_event.clear()
            self._publish_diagnostics_task(self.publish_diagnostic_target)
            time.sleep(self.publish_interval)

    def _publish_diagnostics(self, text_document: TextDocumentIdentifier):
        if self.publish_thread is None:
            self.publish_thread = threading.Thread(
                target=self.publish_listener, daemon=True
            )
            self.publish_thread.start()

        # Feed trigger
        self.publish_diagnostic_target = text_document
        self.publish_event.set()

    def _publish_diagnostics_task(self, text_document: TextDocumentIdentifier):
        file_name = uri_to_path(text_document.uri)
        try:
            document = self.session.get_document(file_name)
        except DocumentNotFound:
            return

        params = Params(
            self.session.root_path,
            document.file_name,
            document.text,
            document.version,
        )
        service = DiagnosticProvider(params)
        diagnostics = service.get_diagnostics()

        # send to client
        self.publish_diagnostics_notification(diagnostics)
