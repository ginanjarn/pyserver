"""command handler"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Dict, Any, Optional

from pyserver import errors
from pyserver.uri import uri_to_path
from pyserver.session import Session, SessionStatus


class Handler(ABC):
    """base handler"""

    @abstractmethod
    def handle(self, method: str, params: dict):
        """handle message"""


MethodName = str
RPCParams = Dict[str, Any]
HandlerCallback = Callable[[Session, RPCParams], None]


class LSPHandler(Handler):
    """LSPHandler implementation"""

    def __init__(self):
        self.session = Session()

        self.handler_map = {
            "initialize": self.initialize,
            "initialized": self.initialized,
            "shutdown": self.shutdown,
            "textDocument/didOpen": self.textdocument_didopen,
            "textDocument/didChange": self.textdocument_didchange,
            "textDocument/didSave": self.textdocument_didsave,
            "textDocument/didClose": self.textdocument_didclose,
        }

    def register_handlers(self, mapping: Dict[MethodName, HandlerCallback], /) -> None:
        self.handler_map.update(mapping)

    def handle(self, method: str, params: dict) -> Optional[Any]:
        if self.session.status == SessionStatus.ShuttingDown:
            raise errors.InvalidRequest("'exit' command is required")

        elif self.session.status == SessionStatus.NotInitialized and method not in {
            "initialize",
            "initialized",
            "shutdown",
        }:
            raise errors.ServerNotInitialized("server not initialized")

        try:
            func = self.handler_map[method]
        except KeyError as err:
            raise errors.MethodNotFound(f"method not found {method!r}") from err

        # external handler
        return func(self.session, params)

    def initialized(self, session: Session, params: dict) -> None:
        if not session.status == SessionStatus.Initializing:
            raise errors.InternalError("server not initialized")

        session.status == SessionStatus.Initialized
        return None

    def shutdown(self, session: Session, params: dict) -> None:
        session.status == SessionStatus.ShuttingDown
        return None

    def initialize(self, session: Session, params: dict) -> dict:
        if session.status == SessionStatus.Initialized:
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

    def textdocument_didopen(self, session: Session, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            language_id = params["textDocument"]["languageId"]
            version = params["textDocument"]["version"]
            text = params["textDocument"]["text"]

        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        session.add_document(file_path, language_id, version, text)

    def textdocument_didsave(self, session: Session, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        if document := session.get_document(file_path):
            document.save()

    def textdocument_didclose(self, session: Session, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        session.remove_document(file_path)

    def textdocument_didchange(self, session: Session, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            version = params["textDocument"]["version"]
            content_changes = params["contentChanges"]
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        document = session.get_document(file_path)
        document.did_change(version, content_changes)
