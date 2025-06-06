"""command handler"""

from pathlib import Path
from typing import Callable, Dict, Any, Optional

from pyserver import errors
from pyserver.document import apply_document_changes
from pyserver.uri import uri_to_path
from pyserver.session import Session, SessionStatus


MethodName = str
Params = dict | list | None
SessionHandleFunction = Callable[[Session, Params], Any]


class LSPHandler:
    """LSPHandler implementation"""

    def __init__(self):
        self.session = Session()
        self.handler_map = {}

        InitializeManager(self.handler_map)
        DocumentSynchronizer(self.handler_map)

    def register_handlers(
        self, mapping: Dict[MethodName, SessionHandleFunction], /
    ) -> None:
        self.handler_map.update(mapping)

    noninitialized_methods = frozenset({"initialize", "initialized", "shutdown"})

    def handle(self, method: MethodName, params: Params) -> Optional[Any]:
        if self.session.status is SessionStatus.ShuttingDown:
            raise errors.InvalidRequest("'exit' command is required")

        if (
            self.session.status is SessionStatus.NotInitialized
        ) and method not in self.noninitialized_methods:
            raise errors.ServerNotInitialized("server not initialized")

        try:
            func = self.handler_map[method]
        except KeyError as err:
            raise errors.MethodNotFound(f"method not found {method!r}") from err

        # external handler
        return func(self.session, params)


class InitializeManager:

    def __init__(self, handler_map: dict):
        handler_map.update(
            {
                "initialize": self.initialize,
                "initialized": self.initialized,
                "shutdown": self.shutdown,
            }
        )

    def initialize(self, session: Session, params: dict) -> dict:
        if session.status is SessionStatus.Initialized:
            raise errors.InternalError("server has initialized")

        try:
            if root_uri := params.get("rootUri"):
                root_path = Path(uri_to_path(root_uri))
            else:
                root_path = Path(params["rootPath"])

        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        if not root_path.is_dir():
            raise errors.InternalError("root path/uri must a directory")

        session.root_path = root_path
        session.status = SessionStatus.Initializing

        return {}

    def initialized(self, session: Session, params: dict) -> None:
        if session.status is not SessionStatus.Initializing:
            raise errors.InternalError("server not initialized")

        session.status == SessionStatus.Initialized
        return None

    def shutdown(self, session: Session, params: dict) -> None:
        session.status == SessionStatus.ShuttingDown
        return None


class DocumentSynchronizer:

    def __init__(self, handler_map: dict):
        handler_map.update(
            {
                "textDocument/didOpen": self.didopen,
                "textDocument/didChange": self.didchange,
                "textDocument/didSave": self.didsave,
                "textDocument/didClose": self.didclose,
            }
        )

    def didopen(self, session: Session, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            language_id = params["textDocument"]["languageId"]
            version = params["textDocument"]["version"]
            text = params["textDocument"]["text"]

        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        session.add_document(file_path, language_id, version, text)

    def didsave(self, session: Session, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        if document := session.get_document(file_path):
            document.is_saved = True

    def didclose(self, session: Session, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        session.remove_document(file_path)

    def didchange(self, session: Session, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            version = params["textDocument"]["version"]
            content_changes = params["contentChanges"]
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        document = session.get_document(file_path)
        # only update if version incremented
        if version <= document.version:
            return

        apply_document_changes(document, content_changes)
