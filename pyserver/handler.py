"""command handler"""

import sys
from abc import ABC, abstractmethod
from contextlib import contextmanager
from functools import wraps, lru_cache

from pyserver import errors
from pyserver.workspace import Workspace, Document, uri_to_path


try:
    from pyserver.services import completion
    from pyserver.services import hover
    from pyserver.services import formatting
    from pyserver.services import definition
    from pyserver.services import diagnostics
    from pyserver.services import prepare_rename
    from pyserver.services import rename
    from pyserver.services import signature_help

except ImportError as err:
    message = """\
Error import required packages!

Following required packages must be installed:
- jedi
- black
- pyflakes

"""
    print(message, file=sys.stderr)
    print(f"error: {err!r}", file=sys.stderr)
    sys.exit(1)


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
            raise errors.ContentModified(
                f"version changed. want:{pre_version}, expected:{post_version}"
            )


class LSPHandler(Handler):
    """LSPHandler implementation"""

    # session manager
    session = SessionManager()

    def __init__(self):
        self.workspace = None

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
            raise errors.InvalidParams(f"invalid params: {err}") from err

        # setup workspace
        self.workspace = Workspace(root_path)

        return {}

    @session.ready
    def textdocument_didopen(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            language_id = params["textDocument"]["languageId"]
            version = params["textDocument"]["version"]
            text = params["textDocument"]["text"]

        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        self.workspace.add_document(file_path, language_id, version, text)

    @session.ready
    def textdocument_didsave(self, params: dict) -> None:
        pass

    @session.ready
    def textdocument_didclose(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        self.workspace.remove_document(file_path)

    @session.ready
    def textdocument_didchange(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            version = params["textDocument"]["version"]
            content_changes = params["contentChanges"]
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        document = self.workspace.get_document(file_path)
        document.did_change(version, content_changes)

    @session.ready
    def textdocument_completion(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            params = completion.CompletionParams(document, line, character)
            service = completion.CompletionService(params)
            return service.get_result()

    @session.ready
    def textdocument_hover(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            params = hover.HoverParams(document, line, character)
            service = hover.HoverService(params)
            return service.get_result()

    @session.ready
    def textdocument_formatting(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            params = formatting.FormattingParams(document)
            service = formatting.FormattingService(params)
            return service.get_result()

    @session.ready
    def textdocument_definition(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            params = definition.DefinitionParams(document, line, character)
            service = definition.DefinitionService(params)
            return service.get_result()

    @session.ready
    def textdocument_publishdiagnostics(self, params: dict):
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            params = diagnostics.DiagnosticParams(document)
            service = diagnostics.DiagnosticService(params)
            return service.get_result()

    @session.ready
    def textdocument_preparerename(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            params = prepare_rename.PrepareRenameParams(document, line, character)
            service = prepare_rename.PrepareRenameService(params)
            return service.get_result()

    @session.ready
    def textdocument_rename(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
            new_name = params["newName"]
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            params = rename.RenameParams(document, line, character, new_name)
            service = rename.RenameService(params)
            return service.get_result()

    @session.ready
    def textdocument_signaturehelp(self, params: dict) -> None:
        try:
            file_path = uri_to_path(params["textDocument"]["uri"])
            line = params["position"]["line"]
            character = params["position"]["character"]
        except KeyError as err:
            raise errors.InvalidParams(f"invalid params: {err}") from err

        with VersionedDocument(self.workspace.get_document(file_path)) as document:
            params = signature_help.SignatureHelpParams(document, line, character)
            service = signature_help.SignatureHelpService(params)
            return service.get_result()
