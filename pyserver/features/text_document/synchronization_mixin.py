import logging
from collections import namedtuple
from typing import List

from ...base_server import BaseServer
from ...lsprotocol.lsprotocol import TextDocumentContentChangeEvent
from ...lsprotocol.server import (
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
    DidCloseTextDocumentParams,
    DidChangeTextDocumentParams,
)
from ...session import Document
from ...uri import uri_to_path

LOGGER = logging.getLogger(__name__)
LineCharacter = namedtuple("LineCharacter", ["line", "character"])


class DocumentSynchronizationMixin(BaseServer):

    def handle_did_open_text_document_notification(
        self, context: dict, params: DidOpenTextDocumentParams
    ) -> None:
        language_id = "python"

        if params.textDocument.languageId != language_id:
            LOGGER.warning("Invalid language id, expected: %s", language_id)
            return

        document = Document(
            uri_to_path(params.textDocument.uri),
            params.textDocument.text,
            params.textDocument.version,
        )
        self.session.add_document(document)

        # publish diagnostics
        self._publish_diagnostics(params.textDocument)

    def handle_did_save_text_document_notification(
        self, context: dict, params: DidSaveTextDocumentParams
    ) -> None:
        # publish diagnostics
        self._publish_diagnostics(params.textDocument)

    def handle_did_close_text_document_notification(
        self, context: dict, params: DidCloseTextDocumentParams
    ) -> None:
        self.session.delete_document(uri_to_path(params.textDocument.uri))

    def handle_did_change_text_document_notification(
        self, context: dict, params: DidChangeTextDocumentParams
    ) -> None:
        document = self.session.get_document(uri_to_path(params.textDocument.uri))
        document.text = self.apply_change(document.text, params.contentChanges)
        document.version = params.textDocument.version

        # publish diagnostics
        self._publish_diagnostics(params.textDocument)

    def apply_change(
        self, origin: str, content_change: List[TextDocumentContentChangeEvent]
    ) -> str:

        line_end = "\n"
        lines = origin.split(line_end)

        for change in content_change:
            # If only a text is provided it is considered to be the full content of the document.
            if not change.range:
                return change.text

            srow, scol = LineCharacter(**change.range.start)
            erow, ecol = LineCharacter(**change.range.end)
            new_text = change.text

            insert = "".join([lines[srow][:scol], new_text, lines[erow][ecol:]])
            lines = lines[:srow] + insert.split(line_end) + lines[erow + 1 :]

        return line_end.join(lines)
