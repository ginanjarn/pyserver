"""command handler"""

import logging
from functools import wraps
from pathlib import Path

from pyserver import errors
from pyserver import message
from pyserver.workspace import Workspace

from pyserver.services import completion
from pyserver.services import hover
from pyserver.services import formatting
from pyserver.services import definition
from pyserver.services import diagnostics
from pyserver.services import prepare_rename
from pyserver.services import rename

LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)  # module logging level
STREAM_HANDLER = logging.StreamHandler()
LOG_TEMPLATE = "%(levelname)s %(asctime)s %(filename)s:%(lineno)s  %(message)s"
STREAM_HANDLER.setFormatter(logging.Formatter(LOG_TEMPLATE))
LOGGER.addHandler(STREAM_HANDLER)


class BaseHandler:
    """base handler define rpc flattened command handler

    every command have to implement single params argument
    with 'handle_*' prefex

    >>> class DummyHandler(BaseHandler):
    ...     def handle_initialize(self, params) -> None:
    ...         pass
    ...
    """


class SessionManager:
    """Session manager

    session define following rules:
    * all command must initialized, except 'exit'
    * all request must return 'InvalidRequest' after shutdown request
    """

    def __init__(self):
        self.is_initialized = False
        self._shutdown = False

    def initialize(self):
        self.is_initialized = True

    def shutdown(self):
        self._shutdown = True

    def is_valid(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self.is_initialized:
                raise errors.ServerNotInitialized
            if self._shutdown:
                raise errors.InvalidRequest("waiting 'exit' command")

            return func(*args, **kwargs)

        return wrapper


# session manager
session = SessionManager()


class LSPHandler(BaseHandler):
    def __init__(self):
        self.workspace = None

    def handle_s_cancelrequest(self, params: dict):
        # $/cancelRequest not implemented
        pass

    def handle_initialized(self, params: dict) -> None:
        if not self.workspace:
            raise errors.InternalError("workspace not defined")

        session.initialize()
        return None

    @session.is_valid
    def handle_shutdown(self, params: dict) -> None:
        session.shutdown()
        return None

    def handle_initialize(self, params: dict) -> dict:
        if session.is_initialized:
            raise errors.ServerNotInitialized
        try:
            root_path = params["rootPath"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        if not Path(root_path).is_dir():
            raise errors.InvalidParams(f"{root_path!r} is not directory")

        # setup workspace
        self.workspace = Workspace(root_path)

        return {}

    @session.is_valid
    def handle_textdocument_didopen(self, params: dict) -> None:
        LOGGER.debug(f"didopen params: {params}")
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
            language_id = params["textDocument"]["languageId"]
            version = params["textDocument"]["version"]
            text = params["textDocument"]["text"]

        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        self.workspace.open_document(file_name, language_id, version, text)
        # LOGGER.debug(self.workspace)

    @session.is_valid
    def handle_textdocument_didsave(self, params: dict) -> None:
        LOGGER.debug(f"didsave params: {params}")

    @session.is_valid
    def handle_textdocument_didclose(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        self.workspace.close_document(file_name)
        LOGGER.debug(self.workspace)

    @session.is_valid
    def handle_textdocument_didchange(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
            content_changes = params["contentChanges"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        self.workspace.get_document(file_name).did_change(content_changes)

    @session.is_valid
    def handle_textdocument_completion(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        document = self.workspace.get_document(file_name)
        pre_version = document.version
        text = document.text
        root_path = self.workspace.root_path

        params = completion.CompletionParams(
            root_path, file_name, text, line, character
        )
        service = completion.CompletionService(params)
        result = service.get_result()

        if document.version != pre_version:
            raise errors.InvalidRequest("content modified")

        return result

    @session.is_valid
    def handle_textdocument_hover(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        document = self.workspace.get_document(file_name)
        pre_version = document.version
        text = document.text
        root_path = self.workspace.root_path

        params = hover.HoverParams(root_path, file_name, text, line, character)
        service = hover.HoverService(params)
        result = service.get_result()

        if document.version != pre_version:
            raise errors.InvalidRequest("content modified")

        return result

    @session.is_valid
    def handle_textdocument_formatting(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        document = self.workspace.get_document(file_name)
        pre_version = document.version
        text = document.text

        params = formatting.FormattingParams(file_name, text)
        service = formatting.FormattingService(params)
        result = service.get_result()

        if document.version != pre_version:
            raise errors.InvalidRequest("content modified")

        return result

    @session.is_valid
    def handle_textdocument_definition(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        text = self.workspace.get_document(file_name).text
        root_path = self.workspace.root_path

        params = definition.DefinitionParams(
            root_path, file_name, text, line, character
        )
        service = definition.DefinitionService(params)
        return service.get_result()

    @session.is_valid
    def handle_textdocument_publishdiagnostics(self, params: dict):
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        document = self.workspace.get_document(file_name)
        text = document.text
        version = document.version
        params = diagnostics.DiagnosticParams(file_name, text, version)
        service = diagnostics.DiagnosticService(params)
        result = service.get_result()
        return result

    @session.is_valid
    def handle_textdocument_preparerename(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        document = self.workspace.get_document(file_name)
        text = document.text
        params = prepare_rename.PrepareRenameParams(
            self.workspace.root_path, file_name, text, line, character
        )
        service = prepare_rename.PrepareRenameService(params)
        return service.get_result()

    @session.is_valid
    def handle_textdocument_rename(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
            new_name = params["newName"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        params = rename.RenameParams(
            self.workspace, file_name, line, character, new_name
        )
        service = rename.RenameService(params)
        return service.get_result()
