"""command handler"""

import logging
import sys
from collections import defaultdict
from contextlib import contextmanager
from functools import wraps, lru_cache
from io import StringIO

from pyserver import errors
from pyserver.workspace import Workspace, Document, uri_to_path


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
    """base handler"""

    @staticmethod
    @lru_cache(maxsize=128)
    def normalize_method(method: str) -> str:
        """normalize method to identifier name
        * replace "/" with "_"
        * replace "$" with "s"
        * convert to lower case
        """
        return method.replace("/", "_").replace("$", "s").lower()

    def handle(self, method: str, params: dict):
        try:
            func = getattr(self, self.normalize_method(method))
        except AttributeError as err:
            raise errors.MethodNotFound(f"method not found {method!r}") from err

        # exec function
        return func(params)


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
        """check if session is ready"""

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
    """VersionedDocument check version changes pre and post execution.

    Raises ContentModified if version is changed.
    """
    try:
        pre_version = document.version
        yield document

    finally:
        post_version = document.version
        # check version changes
        if pre_version != post_version:
            raise errors.ContentModified(f"{pre_version} != {post_version}")


def check_capability(capability: str):
    """check feature capability"""

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not FEATURE_CAPABILITY[capability]:
                raise errors.FeatureDisabled(f"feature {capability!r} is disabled")

            return func(*args, **kwargs)

        return wrapper

    return inner


class LSPHandler(BaseHandler):
    """LSPHandler implementation"""

    # session manager
    session = SessionManager()

    def __init__(self):
        self.workspace = None

    def initialized(self, params: dict) -> None:
        if not self.workspace:
            raise errors.InternalError("workspace not defined")

        self.session.initialize()
        return None

    @session.ready
    def shutdown(self, params: dict) -> None:
        self.session.shutdown()
        return None

    def initialize(self, params: dict) -> dict:
        if self.session.initialized:
            raise errors.ServerNotInitialized

        try:
            if root_uri := params.get("rootUri"):
                root_path = uri_to_path(root_uri)
            else:
                root_path = params["rootPath"]

        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        # setup workspace
        self.workspace = Workspace(root_path)

        return {}

    @session.ready
    def textdocument_didopen(self, params: dict) -> None:
        LOGGER.debug(f"didopen params: {params}")
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            language_id = params["textDocument"]["languageId"]
            version = params["textDocument"]["version"]
            text = params["textDocument"]["text"]

        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        self.workspace.open_document(file_path, language_id, version, text)

    @session.ready
    def textdocument_didsave(self, params: dict) -> None:
        LOGGER.debug(f"didsave params: {params}")

    @session.ready
    def textdocument_didclose(self, params: dict) -> None:
        LOGGER.debug(f"didclose params: {params}")
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        self.workspace.close_document(file_path)

    @session.ready
    def textdocument_didchange(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            version = params["textDocument"]["version"]
            content_changes = params["contentChanges"]
        except KeyError as err:
            LOGGER.debug(f"params: {params}")
            raise errors.InvalidParams(f"invalid params: {err}") from err

        self.workspace.change_document(file_path, version, content_changes)

    @session.ready
    @check_capability(FEATURE_TEXT_DOCUMENT_COMPLETION)
    def textdocument_completion(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
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
    def textdocument_hover(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
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
    def textdocument_formatting(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
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
    def textdocument_definition(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
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
    def textdocument_publishdiagnostics(self, params: dict):
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
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
    def textdocument_preparerename(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
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
    def textdocument_rename(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
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
