"""command handler"""

import logging
import sys
from collections import defaultdict
from contextlib import contextmanager
from functools import wraps
from io import StringIO

from pyserver import errors
from pyserver import message
from pyserver.workspace import Workspace, Document

LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)  # module logging level
STREAM_HANDLER = logging.StreamHandler()
LOG_TEMPLATE = "%(levelname)s %(asctime)s %(filename)s:%(lineno)s  %(message)s"
STREAM_HANDLER.setFormatter(logging.Formatter(LOG_TEMPLATE))
LOGGER.addHandler(STREAM_HANDLER)

# Error message buffer
IMPORT_ERROR_MESSAGE = StringIO()

# Feature names
FEATURE_TEXT_DOCUMENT_COMPLETION = "textDocument/completion"
FEATURE_TEXT_DOCUMENT_HOVER = "textDocument/hover"
FEATURE_TEXT_DOCUMENT_FORMATTING = "textDocument/formatting"
FEATURE_TEXT_DOCUMENT_DEFINITION = "textDocument/definition"
FEATURE_TEXT_DOCUMENT_DIAGNOSTICS = "textDocument/diagnostics"
FEATURE_TEXT_DOCUMENT_RENAME = "textDocument/rename"

# Feature capability
FEATURE_CAPABILITY = defaultdict(bool)

try:
    from pyserver.services import completion

    FEATURE_CAPABILITY[FEATURE_TEXT_DOCUMENT_COMPLETION] = True

except ImportError as err:
    IMPORT_ERROR_MESSAGE.write(f"{err}\n")

try:
    from pyserver.services import hover

    FEATURE_CAPABILITY[FEATURE_TEXT_DOCUMENT_HOVER] = True

except ImportError as err:
    IMPORT_ERROR_MESSAGE.write(f"{err}\n")

try:
    from pyserver.services import formatting

    FEATURE_CAPABILITY[FEATURE_TEXT_DOCUMENT_FORMATTING] = True

except ImportError as err:
    IMPORT_ERROR_MESSAGE.write(f"{err}\n")

try:
    from pyserver.services import definition

    FEATURE_CAPABILITY[FEATURE_TEXT_DOCUMENT_DEFINITION] = True

except ImportError as err:
    IMPORT_ERROR_MESSAGE.write(f"{err}\n")

try:
    from pyserver.services import diagnostics

    FEATURE_CAPABILITY[FEATURE_TEXT_DOCUMENT_DIAGNOSTICS] = True

except ImportError as err:
    IMPORT_ERROR_MESSAGE.write(f"{err}\n")

try:
    from pyserver.services import prepare_rename

    FEATURE_CAPABILITY[FEATURE_TEXT_DOCUMENT_RENAME] = True

except ImportError as err:
    IMPORT_ERROR_MESSAGE.write(f"{err}\n")

try:
    from pyserver.services import rename

    FEATURE_CAPABILITY[FEATURE_TEXT_DOCUMENT_RENAME] = True

except ImportError as err:
    IMPORT_ERROR_MESSAGE.write(f"{err}\n")

if IMPORT_ERROR_MESSAGE.getvalue():
    IMPORT_ERROR_MESSAGE.write("\nSOME FEATURES WILL BE UNAVAILABLE !!!\n\n")

    IMPORT_ERROR_MESSAGE.write("Feature capability:\n")
    for name, value in FEATURE_CAPABILITY.items():
        IMPORT_ERROR_MESSAGE.write(f" * {name} : {value}\n")

    print(IMPORT_ERROR_MESSAGE.getvalue(), file=sys.stderr)


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
    """VersionedDocument ensure document not modified after execution"""

    try:
        pre_version = document.version
        yield document

    finally:
        # check version changes
        if pre_version != document.version:
            raise errors.ContentModified


def check_capability(capability: str):
    """check feature capability wrapper"""

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not FEATURE_CAPABILITY[capability]:
                raise errors.FeatureDisabled(f"feature disabled {capability!r}")

            return func(*args, **kwargs)

        return wrapper

    return inner


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
            file_path = message.uri_to_path(params["textDocument"]["uri"])
            language_id = params["textDocument"]["languageId"]
            version = params["textDocument"]["version"]
            text = params["textDocument"]["text"]

        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        self.workspace.open_document(file_path, language_id, version, text)

    @session.ready
    def handle_textdocument_didsave(self, params: dict) -> None:
        LOGGER.debug(f"didsave params: {params}")

    @session.ready
    def handle_textdocument_didclose(self, params: dict) -> None:
        LOGGER.debug(f"didclose params: {params}")
        try:
            file_path = message.uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        self.workspace.close_document(file_path)

    @session.ready
    def handle_textdocument_didchange(self, params: dict) -> None:
        try:
            file_path = message.uri_to_path(params["textDocument"]["uri"])
            content_changes = params["contentChanges"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        self.workspace.get_document(file_path).did_change(content_changes)

    @session.ready
    @check_capability(FEATURE_TEXT_DOCUMENT_COMPLETION)
    def handle_textdocument_completion(self, params: dict) -> None:
        try:
            file_path = message.uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            root_path = self.workspace.root_path
            text = document.text

            params = completion.CompletionParams(
                root_path, file_path, text, line, character
            )
            service = completion.CompletionService(params)
            return service.get_result()

    @session.ready
    @check_capability(FEATURE_TEXT_DOCUMENT_HOVER)
    def handle_textdocument_hover(self, params: dict) -> None:
        try:
            file_path = message.uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            root_path = self.workspace.root_path
            text = document.text

            params = hover.HoverParams(root_path, file_path, text, line, character)
            service = hover.HoverService(params)
            return service.get_result()

    @session.ready
    @check_capability(FEATURE_TEXT_DOCUMENT_FORMATTING)
    def handle_textdocument_formatting(self, params: dict) -> None:
        try:
            file_path = message.uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            text = document.text

            params = formatting.FormattingParams(file_path, text)
            service = formatting.FormattingService(params)
            return service.get_result()

    @session.ready
    @check_capability(FEATURE_TEXT_DOCUMENT_DEFINITION)
    def handle_textdocument_definition(self, params: dict) -> None:
        try:
            file_path = message.uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            root_path = self.workspace.root_path
            text = document.text

            params = definition.DefinitionParams(
                root_path, file_path, text, line, character
            )
            service = definition.DefinitionService(params)
            return service.get_result()

    @session.ready
    @check_capability(FEATURE_TEXT_DOCUMENT_DIAGNOSTICS)
    def handle_textdocument_publishdiagnostics(self, params: dict):
        try:
            file_path = message.uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            text = document.text
            version = document.version

            params = diagnostics.DiagnosticParams(file_path, text, version)
            service = diagnostics.DiagnosticService(params)
            return service.get_result()

    @session.ready
    @check_capability(FEATURE_TEXT_DOCUMENT_RENAME)
    def handle_textdocument_preparerename(self, params: dict) -> None:
        try:
            file_path = message.uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            text = document.text

            params = prepare_rename.PrepareRenameParams(
                self.workspace.root_path, file_path, text, line, character
            )
            service = prepare_rename.PrepareRenameService(params)
            return service.get_result()

    @session.ready
    @check_capability(FEATURE_TEXT_DOCUMENT_RENAME)
    def handle_textdocument_rename(self, params: dict) -> None:
        try:
            file_path = message.uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
            new_name = params["newName"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            params = rename.RenameParams(
                self.workspace, document.path, line, character, new_name
            )
            service = rename.RenameService(params)
            return service.get_result()
