"""command handler"""

from abc import ABC, abstractmethod
from functools import wraps
from typing import Callable, Dict, Any, Optional

from pyserver import errors
from pyserver.workspace import Workspace, uri_to_path


class Handler(ABC):
    """base handler"""

    @abstractmethod
    def handle(self, method: str, params: dict):
        """handle message"""


class SessionManager:
    """Session manager

    session define following rules:
    * all command must initialized, except 'exit'
    * all request must return 'InvalidRequest' after shutdown request
    """

    def __init__(self):
        self.workspace: Workspace = None
        self.is_initialized = False
        self.is_shuttingdown = False

    def initialize(self, workspace: Workspace):
        self.workspace = workspace

    def set_initialized(self, status: bool = True):
        self.is_initialized = status

    def shutdown(self):
        self.workspace = None
        self.is_shuttingdown = True

    def must_initialized(self, func):
        """check if session is initialized"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self.is_initialized:
                raise errors.ServerNotInitialized

            return func(*args, **kwargs)

        return wrapper


MethodName = str
RPCParams = Dict[str, Any]
HandlerCallback = Callable[[Workspace, RPCParams], None]


class LSPHandler(Handler):
    """LSPHandler implementation"""

    # session manager
    session = SessionManager()

    def __init__(self):
        self._internal_handler_map = {
            "initialize": self.initialize,
            "initialized": self.initialized,
            "shutdown": self.shutdown,
            "textDocument/didOpen": self.textdocument_didopen,
            "textDocument/didChange": self.textdocument_didchange,
            "textDocument/didSave": self.textdocument_didsave,
            "textDocument/didClose": self.textdocument_didclose,
        }
        self._extension_handler_map = {}

    def register_handlers(self, mapping: Dict[MethodName, HandlerCallback] = None):
        self._extension_handler_map.update(mapping)

    def handle(self, method: str, params: dict) -> Optional[Any]:
        if self.session.is_shuttingdown:
            raise errors.InvalidRequest("'exit' command is required")

        workspace = self.session.workspace

        # builtin handler
        if func := self._internal_handler_map.get(method):
            return func(workspace, params)

        # external handler must initialized
        if not self.session.is_initialized:
            raise errors.ServerNotInitialized("not initialized")

        try:
            func = self._extension_handler_map[method]
        except KeyError as err:
            raise errors.MethodNotFound(f"method not found {method!r}") from err

        # external handler
        return func(workspace, params)

    def initialized(self, workspace: Workspace, params: dict) -> None:
        if not self.session.workspace:
            raise errors.InternalError("workspace not defined")

        self.session.set_initialized()
        return None

    @session.must_initialized
    def shutdown(self, workspace: Workspace, params: dict) -> None:
        self.session.shutdown()
        return None

    def initialize(self, workspace: Workspace, params: dict) -> dict:
        if self.session.is_initialized:
            raise errors.ServerNotInitialized

        try:
            if root_uri := params.get("rootUri"):
                root_path = uri_to_path(root_uri)
            else:
                root_path = params["rootPath"]

        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        # setup workspace
        self.session.initialize(Workspace(root_path))

        return {}

    @session.must_initialized
    def textdocument_didopen(self, workspace: Workspace, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            language_id = params["textDocument"]["languageId"]
            version = params["textDocument"]["version"]
            text = params["textDocument"]["text"]

        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        workspace.add_document(file_path, language_id, version, text)

    @session.must_initialized
    def textdocument_didsave(self, workspace: Workspace, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        if document := workspace.get_document(file_path):
            document.save()

    @session.must_initialized
    def textdocument_didclose(self, workspace: Workspace, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        workspace.remove_document(file_path)

    @session.must_initialized
    def textdocument_didchange(self, workspace: Workspace, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            version = params["textDocument"]["version"]
            content_changes = params["contentChanges"]
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        document = workspace.get_document(file_path)
        document.did_change(version, content_changes)
