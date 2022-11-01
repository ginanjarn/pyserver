"""command handler"""

import logging
from contextlib import contextmanager
from functools import wraps

from pyserver import errors
from pyserver import message
from pyserver.workspace import Workspace, Document

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
        self.initialized = False
        self._request_shutdown = False

    def initialize(self):
        self.initialized = True

    def shutdown(self):
        self._request_shutdown = True

    def ready(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self.initialized:
                raise errors.ServerNotInitialized

            if self._request_shutdown:
                raise errors.InvalidRequest("waiting 'exit' command")

            return func(*args, **kwargs)

        return wrapper


@contextmanager
def VersionedDocument(document: Document):
    """VersionedDocument check any version modification"""

    pre_version = document.version
    yield document
    if document.version != pre_version:
        raise errors.ContentModified


class LSPHandler(BaseHandler):
    """LSPHandler implementation"""

    # session manager
    session = SessionManager()

    def __init__(self):
        self.workspace = None

    def handle_initialized(self, params: dict) -> None:
        if not self.workspace:
            raise errors.InternalError("workspace not defined")

        self.session.initialize()
        return None

    @session.ready
    def handle_shutdown(self, params: dict) -> None:
        self.session.shutdown()
        return None

    def handle_initialize(self, params: dict) -> dict:
        if self.session.initialized:
            raise errors.ServerNotInitialized

        try:
            if root_uri := params.get("rootUri"):
                root_path = message.uri_to_path(root_uri)
            else:
                root_path = params["rootPath"]

        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        # setup workspace
        self.workspace = Workspace(root_path)

        return {}

    @session.ready
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

    @session.ready
    def handle_textdocument_didsave(self, params: dict) -> None:
        LOGGER.debug(f"didsave params: {params}")

    @session.ready
    def handle_textdocument_didclose(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        self.workspace.close_document(file_name)

    @session.ready
    def handle_textdocument_didchange(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
            content_changes = params["contentChanges"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        self.workspace.get_document(file_name).did_change(content_changes)

    @session.ready
    def handle_textdocument_completion(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        root_path = self.workspace.root_path
        document = self.workspace.get_document(file_name)
        text = document.text

        with VersionedDocument(document) as document:
            params = completion.CompletionParams(
                root_path, file_name, text, line, character
            )
            service = completion.CompletionService(params)
            return service.get_result()

    @session.ready
    def handle_textdocument_hover(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        root_path = self.workspace.root_path
        document = self.workspace.get_document(file_name)
        text = document.text

        with VersionedDocument(document) as document:
            params = hover.HoverParams(root_path, file_name, text, line, character)
            service = hover.HoverService(params)
            return service.get_result()

    @session.ready
    def handle_textdocument_formatting(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        document = self.workspace.get_document(file_name)
        text = document.text

        with VersionedDocument(document) as document:
            params = formatting.FormattingParams(file_name, text)
            service = formatting.FormattingService(params)
            return service.get_result()

    @session.ready
    def handle_textdocument_definition(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        root_path = self.workspace.root_path
        document = self.workspace.get_document(file_name)
        text = document.text

        with VersionedDocument(document) as document:
            params = definition.DefinitionParams(
                root_path, file_name, text, line, character
            )
            service = definition.DefinitionService(params)
            return service.get_result()

    @session.ready
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

    @session.ready
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

        with VersionedDocument(document) as document:
            params = prepare_rename.PrepareRenameParams(
                self.workspace.root_path, file_name, text, line, character
            )
            service = prepare_rename.PrepareRenameService(params)
            return service.get_result()

    @session.ready
    def handle_textdocument_rename(self, params: dict) -> None:
        try:
            file_name = message.uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
            new_name = params["newName"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        document = self.workspace.get_document(file_name)

        with VersionedDocument(document) as document:
            params = rename.RenameParams(
                self.workspace, file_name, line, character, new_name
            )
            service = rename.RenameService(params)
            return service.get_result()
