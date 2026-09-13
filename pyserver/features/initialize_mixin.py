from ..base_server import BaseServer
from ..lsprotocol.client import InitializeParams, InitializeResult, InitializedParams
from ..session import WorkspaceFolder
from ..uri import uri_to_path
from ..version import __version__


class InitializeMixin(BaseServer):
    def handle_initialize_request(
        self, context: dict, params: InitializeParams
    ) -> InitializeResult:
        try:
            self.session.root_path = uri_to_path(params.rootUri)
        except KeyError:
            self.session.root_path = params.rootPath

        self.session.workspace_folders = [
            WorkspaceFolder(uri_to_path(f.uri), f.name) for f in params.workspaceFolders
        ]

        return {
            "capabilities": {
                "positionEncoding": "utf-8",
                "textDocumentSync": {
                    "openClose": True,
                    "change": 2,
                    "willSave": False,
                    "willSaveWaitUntil": False,
                    "save": True,
                },
                "notebookDocumentSync": {"notebookSelector": [], "save": False},
                "completionProvider": {
                    "triggerCharacters": ["[", "{", "(", ",", "."],
                    "allCommitCharacters": [],
                    "resolveProvider": False,
                    "completionItem": {"labelDetailsSupport": False},
                    "workDoneProgress": False,
                },
                "hoverProvider": True,
                "signatureHelpProvider": {
                    "triggerCharacters": ["(", ","],
                    "retriggerCharacters": [],
                    "workDoneProgress": False,
                },
                "declarationProvider": False,
                "definitionProvider": True,
                "typeDefinitionProvider": False,
                "implementationProvider": False,
                "referencesProvider": False,
                "documentHighlightProvider": False,
                "documentSymbolProvider": True,
                "codeActionProvider": False,
                "codeLensProvider": {
                    "resolveProvider": False,
                    "workDoneProgress": False,
                },
                "documentLinkProvider": {
                    "resolveProvider": False,
                    "workDoneProgress": False,
                },
                "colorProvider": False,
                "workspaceSymbolProvider": False,
                "documentFormattingProvider": True,
                "documentRangeFormattingProvider": False,
                "documentOnTypeFormattingProvider": {
                    "firstTriggerCharacter": "",
                    "moreTriggerCharacter": [],
                },
                "renameProvider": True,
                "foldingRangeProvider": False,
                "selectionRangeProvider": False,
                "executeCommandProvider": {"commands": [], "workDoneProgress": False},
                "callHierarchyProvider": False,
                "linkedEditingRangeProvider": False,
                "semanticTokensProvider": {
                    "legend": {"tokenTypes": [], "tokenModifiers": []},
                    "range": False,
                    "full": False,
                    "workDoneProgress": False,
                },
                "monikerProvider": False,
                "typeHierarchyProvider": False,
                "inlineValueProvider": False,
                "inlayHintProvider": False,
                "diagnosticProvider": {
                    "identifier": "",
                    "interFileDependencies": False,
                    "workspaceDiagnostics": False,
                    "workDoneProgress": False,
                },
                "inlineCompletionProvider": False,
                "workspace": {
                    "workspaceFolders": {"supported": False, "changeNotifications": ""},
                    "fileOperations": {
                        "didCreate": {"filters": []},
                        "willCreate": {"filters": []},
                        "didRename": {"filters": []},
                        "willRename": {"filters": []},
                        "didDelete": {"filters": []},
                        "willDelete": {"filters": []},
                    },
                    "textDocumentContent": {"schemes": []},
                },
                "experimental": {},
            },
            "serverInfo": {"name": "pyserver", "version": __version__},
        }

    def handle_initialized_notification(
        self, context: dict, params: InitializedParams
    ) -> None:
        self.session.is_initialized = True
