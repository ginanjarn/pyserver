import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Iterator

from ...base_server import BaseServer
from ...lsprotocol.lsprotocol import TextDocumentIdentifier
from ...session import DocumentNotFound
from ...uri import path_to_uri, uri_to_path

from .diagnostics import Diagnostic
from .diagnostics.pyflakes_check import PyflakesChecker


@dataclass
class Params:
    workspace_path: Path
    file_path: Path
    text: str
    version: int


class DiagnosticProvider:
    def __init__(self, params: Params):
        self.params = params

    def execute(self) -> Iterator[Diagnostic]:
        diagnostic = PyflakesChecker(self.params.file_path, self.params.text)
        return diagnostic.get_diagnostic()

    def build_item(self, item: Diagnostic) -> dict:
        start, end = item.text_range

        return {
            "range": {
                "start": {"line": start.row, "character": start.column},
                "end": {"line": end.row, "character": end.column},
            },
            "severity": item.severity,
            "code": item.code,
            "source": item.source,
            "message": item.message,
            "data": item.data,
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
