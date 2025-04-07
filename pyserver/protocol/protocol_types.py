"""LSP Protocol Types"""

from dataclasses import dataclass, field
from typing import TypeAlias, List, Tuple, Dict, Literal, Union, Any

URI: TypeAlias = str
DocumentUri: TypeAlias = str


__lsp_version__= '3.17.0'

SemanticTokenTypes: TypeAlias = str
"""A set of predefined token types. This set is not fixed
an clients can specify additional token types via the
corresponding client capabilities.

@since 3.16.0"""
# since 3.16.0

SemanticTokenTypesnamespace: SemanticTokenTypes = 'namespace'

SemanticTokenTypestype: SemanticTokenTypes = 'type'
"""Represents a generic type. Acts as a fallback for types which can't be mapped to
a specific type like class or enum."""

SemanticTokenTypesclass: SemanticTokenTypes = 'class'

SemanticTokenTypesenum: SemanticTokenTypes = 'enum'

SemanticTokenTypesinterface: SemanticTokenTypes = 'interface'

SemanticTokenTypesstruct: SemanticTokenTypes = 'struct'

SemanticTokenTypestypeParameter: SemanticTokenTypes = 'typeParameter'

SemanticTokenTypesparameter: SemanticTokenTypes = 'parameter'

SemanticTokenTypesvariable: SemanticTokenTypes = 'variable'

SemanticTokenTypesproperty: SemanticTokenTypes = 'property'

SemanticTokenTypesenumMember: SemanticTokenTypes = 'enumMember'

SemanticTokenTypesevent: SemanticTokenTypes = 'event'

SemanticTokenTypesfunction: SemanticTokenTypes = 'function'

SemanticTokenTypesmethod: SemanticTokenTypes = 'method'

SemanticTokenTypesmacro: SemanticTokenTypes = 'macro'

SemanticTokenTypeskeyword: SemanticTokenTypes = 'keyword'

SemanticTokenTypesmodifier: SemanticTokenTypes = 'modifier'

SemanticTokenTypescomment: SemanticTokenTypes = 'comment'

SemanticTokenTypesstring: SemanticTokenTypes = 'string'

SemanticTokenTypesnumber: SemanticTokenTypes = 'number'

SemanticTokenTypesregexp: SemanticTokenTypes = 'regexp'

SemanticTokenTypesoperator: SemanticTokenTypes = 'operator'

SemanticTokenTypesdecorator: SemanticTokenTypes = 'decorator'
"""@since 3.17.0"""
# since 3.17.0

SemanticTokenTypeslabel: SemanticTokenTypes = 'label'
"""@since 3.18.0"""
# since 3.18.0

SemanticTokenModifiers: TypeAlias = str
"""A set of predefined token modifiers. This set is not fixed
an clients can specify additional token types via the
corresponding client capabilities.

@since 3.16.0"""
# since 3.16.0

SemanticTokenModifiersdeclaration: SemanticTokenModifiers = 'declaration'

SemanticTokenModifiersdefinition: SemanticTokenModifiers = 'definition'

SemanticTokenModifiersreadonly: SemanticTokenModifiers = 'readonly'

SemanticTokenModifiersstatic: SemanticTokenModifiers = 'static'

SemanticTokenModifiersdeprecated: SemanticTokenModifiers = 'deprecated'

SemanticTokenModifiersabstract: SemanticTokenModifiers = 'abstract'

SemanticTokenModifiersasync: SemanticTokenModifiers = 'async'

SemanticTokenModifiersmodification: SemanticTokenModifiers = 'modification'

SemanticTokenModifiersdocumentation: SemanticTokenModifiers = 'documentation'

SemanticTokenModifiersdefaultLibrary: SemanticTokenModifiers = 'defaultLibrary'

DocumentDiagnosticReportKind: TypeAlias = str
"""The document diagnostic report kinds.

@since 3.17.0"""
# since 3.17.0

DocumentDiagnosticReportKindFull: DocumentDiagnosticReportKind = 'full'
"""A diagnostic report with a full
set of problems."""

DocumentDiagnosticReportKindUnchanged: DocumentDiagnosticReportKind = 'unchanged'
"""A report indicating that the last
returned report is still accurate."""

ErrorCodes: TypeAlias = int
"""Predefined error codes."""

ErrorCodesParseError: ErrorCodes = -32700

ErrorCodesInvalidRequest: ErrorCodes = -32600

ErrorCodesMethodNotFound: ErrorCodes = -32601

ErrorCodesInvalidParams: ErrorCodes = -32602

ErrorCodesInternalError: ErrorCodes = -32603

ErrorCodesServerNotInitialized: ErrorCodes = -32002
"""Error code indicating that a server received a notification or
request before the server has received the `initialize` request."""

ErrorCodesUnknownErrorCode: ErrorCodes = -32001

LSPErrorCodes: TypeAlias = int

LSPErrorCodesRequestFailed: LSPErrorCodes = -32803
"""A request failed but it was syntactically correct, e.g the
method name was known and the parameters were valid. The error
message should contain human readable information about why
the request failed.

@since 3.17.0"""
# since 3.17.0

LSPErrorCodesServerCancelled: LSPErrorCodes = -32802
"""The server cancelled the request. This error code should
only be used for requests that explicitly support being
server cancellable.

@since 3.17.0"""
# since 3.17.0

LSPErrorCodesContentModified: LSPErrorCodes = -32801
"""The server detected that the content of a document got
modified outside normal conditions. A server should
NOT send this error code if it detects a content change
in it unprocessed messages. The result even computed
on an older state might still be useful for the client.

If a client decides that a result is not of any use anymore
the client should cancel the request."""

LSPErrorCodesRequestCancelled: LSPErrorCodes = -32800
"""The client has canceled a request and a server has detected
the cancel."""

FoldingRangeKind: TypeAlias = str
"""A set of predefined range kinds."""

FoldingRangeKindComment: FoldingRangeKind = 'comment'
"""Folding range for a comment"""

FoldingRangeKindImports: FoldingRangeKind = 'imports'
"""Folding range for an import or include"""

FoldingRangeKindRegion: FoldingRangeKind = 'region'
"""Folding range for a region (e.g. `#region`)"""

SymbolKind: TypeAlias = int
"""A symbol kind."""

SymbolKindFile: SymbolKind = 1

SymbolKindModule: SymbolKind = 2

SymbolKindNamespace: SymbolKind = 3

SymbolKindPackage: SymbolKind = 4

SymbolKindClass: SymbolKind = 5

SymbolKindMethod: SymbolKind = 6

SymbolKindProperty: SymbolKind = 7

SymbolKindField: SymbolKind = 8

SymbolKindConstructor: SymbolKind = 9

SymbolKindEnum: SymbolKind = 10

SymbolKindInterface: SymbolKind = 11

SymbolKindFunction: SymbolKind = 12

SymbolKindVariable: SymbolKind = 13

SymbolKindConstant: SymbolKind = 14

SymbolKindString: SymbolKind = 15

SymbolKindNumber: SymbolKind = 16

SymbolKindBoolean: SymbolKind = 17

SymbolKindArray: SymbolKind = 18

SymbolKindObject: SymbolKind = 19

SymbolKindKey: SymbolKind = 20

SymbolKindNull: SymbolKind = 21

SymbolKindEnumMember: SymbolKind = 22

SymbolKindStruct: SymbolKind = 23

SymbolKindEvent: SymbolKind = 24

SymbolKindOperator: SymbolKind = 25

SymbolKindTypeParameter: SymbolKind = 26

SymbolTag: TypeAlias = int
"""Symbol tags are extra annotations that tweak the rendering of a symbol.

@since 3.16"""
# since 3.16

SymbolTagDeprecated: SymbolTag = 1
"""Render a symbol as obsolete, usually using a strike-out."""

UniquenessLevel: TypeAlias = str
"""Moniker uniqueness level to define scope of the moniker.

@since 3.16.0"""
# since 3.16.0

UniquenessLeveldocument: UniquenessLevel = 'document'
"""The moniker is only unique inside a document"""

UniquenessLevelproject: UniquenessLevel = 'project'
"""The moniker is unique inside a project for which a dump got created"""

UniquenessLevelgroup: UniquenessLevel = 'group'
"""The moniker is unique inside the group to which a project belongs"""

UniquenessLevelscheme: UniquenessLevel = 'scheme'
"""The moniker is unique inside the moniker scheme."""

UniquenessLevelglobal: UniquenessLevel = 'global'
"""The moniker is globally unique"""

MonikerKind: TypeAlias = str
"""The moniker kind.

@since 3.16.0"""
# since 3.16.0

MonikerKindimport: MonikerKind = 'import'
"""The moniker represent a symbol that is imported into a project"""

MonikerKindexport: MonikerKind = 'export'
"""The moniker represents a symbol that is exported from a project"""

MonikerKindlocal: MonikerKind = 'local'
"""The moniker represents a symbol that is local to a project (e.g. a local
variable of a function, a class not visible outside the project, ...)"""

InlayHintKind: TypeAlias = int
"""Inlay hint kinds.

@since 3.17.0"""
# since 3.17.0

InlayHintKindType: InlayHintKind = 1
"""An inlay hint that for a type annotation."""

InlayHintKindParameter: InlayHintKind = 2
"""An inlay hint that is for a parameter."""

MessageType: TypeAlias = int
"""The message type"""

MessageTypeError: MessageType = 1
"""An error message."""

MessageTypeWarning: MessageType = 2
"""A warning message."""

MessageTypeInfo: MessageType = 3
"""An information message."""

MessageTypeLog: MessageType = 4
"""A log message."""

MessageTypeDebug: MessageType = 5
"""A debug message.

@since 3.18.0
@proposed"""
# since 3.18.0

TextDocumentSyncKind: TypeAlias = int
"""Defines how the host (editor) should sync
document changes to the language server."""

TextDocumentSyncKindNone: TextDocumentSyncKind = 0
"""Documents should not be synced at all."""

TextDocumentSyncKindFull: TextDocumentSyncKind = 1
"""Documents are synced by always sending the full content
of the document."""

TextDocumentSyncKindIncremental: TextDocumentSyncKind = 2
"""Documents are synced by sending the full content on open.
After that only incremental updates to the document are
send."""

TextDocumentSaveReason: TypeAlias = int
"""Represents reasons why a text document is saved."""

TextDocumentSaveReasonManual: TextDocumentSaveReason = 1
"""Manually triggered, e.g. by the user pressing save, by starting debugging,
or by an API call."""

TextDocumentSaveReasonAfterDelay: TextDocumentSaveReason = 2
"""Automatic after a delay."""

TextDocumentSaveReasonFocusOut: TextDocumentSaveReason = 3
"""When the editor lost focus."""

CompletionItemKind: TypeAlias = int
"""The kind of a completion entry."""

CompletionItemKindText: CompletionItemKind = 1

CompletionItemKindMethod: CompletionItemKind = 2

CompletionItemKindFunction: CompletionItemKind = 3

CompletionItemKindConstructor: CompletionItemKind = 4

CompletionItemKindField: CompletionItemKind = 5

CompletionItemKindVariable: CompletionItemKind = 6

CompletionItemKindClass: CompletionItemKind = 7

CompletionItemKindInterface: CompletionItemKind = 8

CompletionItemKindModule: CompletionItemKind = 9

CompletionItemKindProperty: CompletionItemKind = 10

CompletionItemKindUnit: CompletionItemKind = 11

CompletionItemKindValue: CompletionItemKind = 12

CompletionItemKindEnum: CompletionItemKind = 13

CompletionItemKindKeyword: CompletionItemKind = 14

CompletionItemKindSnippet: CompletionItemKind = 15

CompletionItemKindColor: CompletionItemKind = 16

CompletionItemKindFile: CompletionItemKind = 17

CompletionItemKindReference: CompletionItemKind = 18

CompletionItemKindFolder: CompletionItemKind = 19

CompletionItemKindEnumMember: CompletionItemKind = 20

CompletionItemKindConstant: CompletionItemKind = 21

CompletionItemKindStruct: CompletionItemKind = 22

CompletionItemKindEvent: CompletionItemKind = 23

CompletionItemKindOperator: CompletionItemKind = 24

CompletionItemKindTypeParameter: CompletionItemKind = 25

CompletionItemTag: TypeAlias = int
"""Completion item tags are extra annotations that tweak the rendering of a completion
item.

@since 3.15.0"""
# since 3.15.0

CompletionItemTagDeprecated: CompletionItemTag = 1
"""Render a completion as obsolete, usually using a strike-out."""

InsertTextFormat: TypeAlias = int
"""Defines whether the insert text in a completion item should be interpreted as
plain text or a snippet."""

InsertTextFormatPlainText: InsertTextFormat = 1
"""The primary text to be inserted is treated as a plain string."""

InsertTextFormatSnippet: InsertTextFormat = 2
"""The primary text to be inserted is treated as a snippet.

A snippet can define tab stops and placeholders with `$1`, `$2`
and `${3:foo}`. `$0` defines the final tab stop, it defaults to
the end of the snippet. Placeholders with equal identifiers are linked,
that is typing in one will update others too.

See also: https://microsoft.github.io/language-server-protocol/specifications/specification-current/#snippet_syntax"""

InsertTextMode: TypeAlias = int
"""How whitespace and indentation is handled during completion
item insertion.

@since 3.16.0"""
# since 3.16.0

InsertTextModeasIs: InsertTextMode = 1
"""The insertion or replace strings is taken as it is. If the
value is multi line the lines below the cursor will be
inserted using the indentation defined in the string value.
The client will not apply any kind of adjustments to the
string."""

InsertTextModeadjustIndentation: InsertTextMode = 2
"""The editor adjusts leading whitespace of new lines so that
they match the indentation up to the cursor of the line for
which the item is accepted.

Consider a line like this: <2tabs><cursor><3tabs>foo. Accepting a
multi line completion item is indented using 2 tabs and all
following lines inserted will be indented using 2 tabs as well."""

DocumentHighlightKind: TypeAlias = int
"""A document highlight kind."""

DocumentHighlightKindText: DocumentHighlightKind = 1
"""A textual occurrence."""

DocumentHighlightKindRead: DocumentHighlightKind = 2
"""Read-access of a symbol, like reading a variable."""

DocumentHighlightKindWrite: DocumentHighlightKind = 3
"""Write-access of a symbol, like writing to a variable."""

CodeActionKind: TypeAlias = str
"""A set of predefined code action kinds"""

CodeActionKindEmpty: CodeActionKind = ''
"""Empty kind."""

CodeActionKindQuickFix: CodeActionKind = 'quickfix'
"""Base kind for quickfix actions: 'quickfix'"""

CodeActionKindRefactor: CodeActionKind = 'refactor'
"""Base kind for refactoring actions: 'refactor'"""

CodeActionKindRefactorExtract: CodeActionKind = 'refactor.extract'
"""Base kind for refactoring extraction actions: 'refactor.extract'

Example extract actions:

- Extract method
- Extract function
- Extract variable
- Extract interface from class
- ..."""

CodeActionKindRefactorInline: CodeActionKind = 'refactor.inline'
"""Base kind for refactoring inline actions: 'refactor.inline'

Example inline actions:

- Inline function
- Inline variable
- Inline constant
- ..."""

CodeActionKindRefactorMove: CodeActionKind = 'refactor.move'
"""Base kind for refactoring move actions: `refactor.move`

Example move actions:

- Move a function to a new file
- Move a property between classes
- Move method to base class
- ...

@since 3.18.0
@proposed"""
# since 3.18.0

CodeActionKindRefactorRewrite: CodeActionKind = 'refactor.rewrite'
"""Base kind for refactoring rewrite actions: 'refactor.rewrite'

Example rewrite actions:

- Convert JavaScript function to class
- Add or remove parameter
- Encapsulate field
- Make method static
- Move method to base class
- ..."""

CodeActionKindSource: CodeActionKind = 'source'
"""Base kind for source actions: `source`

Source code actions apply to the entire file."""

CodeActionKindSourceOrganizeImports: CodeActionKind = 'source.organizeImports'
"""Base kind for an organize imports source action: `source.organizeImports`"""

CodeActionKindSourceFixAll: CodeActionKind = 'source.fixAll'
"""Base kind for auto-fix source actions: `source.fixAll`.

Fix all actions automatically fix errors that have a clear fix that do not require user input.
They should not suppress errors or perform unsafe fixes such as generating new types or classes.

@since 3.15.0"""
# since 3.15.0

CodeActionKindNotebook: CodeActionKind = 'notebook'
"""Base kind for all code actions applying to the entire notebook's scope. CodeActionKinds using
this should always begin with `notebook.`

@since 3.18.0"""
# since 3.18.0

CodeActionTag: TypeAlias = int
"""Code action tags are extra annotations that tweak the behavior of a code action.

@since 3.18.0 - proposed"""
# since 3.18.0 - proposed

CodeActionTagLLMGenerated: CodeActionTag = 1
"""Marks the code action as LLM-generated."""

TraceValue: TypeAlias = str

TraceValueOff: TraceValue = 'off'
"""Turn tracing off."""

TraceValueMessages: TraceValue = 'messages'
"""Trace messages only."""

TraceValueVerbose: TraceValue = 'verbose'
"""Verbose message tracing."""

MarkupKind: TypeAlias = str
"""Describes the content type that a client supports in various
result literals like `Hover`, `ParameterInfo` or `CompletionItem`.

Please note that `MarkupKinds` must not start with a `$`. This kinds
are reserved for internal usage."""

MarkupKindPlainText: MarkupKind = 'plaintext'
"""Plain text is supported as a content format"""

MarkupKindMarkdown: MarkupKind = 'markdown'
"""Markdown is supported as a content format"""

LanguageKind: TypeAlias = str
"""Predefined Language kinds
@since 3.18.0"""
# since 3.18.0

LanguageKindABAP: LanguageKind = 'abap'

LanguageKindWindowsBat: LanguageKind = 'bat'

LanguageKindBibTeX: LanguageKind = 'bibtex'

LanguageKindClojure: LanguageKind = 'clojure'

LanguageKindCoffeescript: LanguageKind = 'coffeescript'

LanguageKindC: LanguageKind = 'c'

LanguageKindCPP: LanguageKind = 'cpp'

LanguageKindCSharp: LanguageKind = 'csharp'

LanguageKindCSS: LanguageKind = 'css'

LanguageKindD: LanguageKind = 'd'
"""@since 3.18.0
@proposed"""
# since 3.18.0

LanguageKindDelphi: LanguageKind = 'pascal'
"""@since 3.18.0
@proposed"""
# since 3.18.0

LanguageKindDiff: LanguageKind = 'diff'

LanguageKindDart: LanguageKind = 'dart'

LanguageKindDockerfile: LanguageKind = 'dockerfile'

LanguageKindElixir: LanguageKind = 'elixir'

LanguageKindErlang: LanguageKind = 'erlang'

LanguageKindFSharp: LanguageKind = 'fsharp'

LanguageKindGitCommit: LanguageKind = 'git-commit'

LanguageKindGitRebase: LanguageKind = 'rebase'

LanguageKindGo: LanguageKind = 'go'

LanguageKindGroovy: LanguageKind = 'groovy'

LanguageKindHandlebars: LanguageKind = 'handlebars'

LanguageKindHaskell: LanguageKind = 'haskell'

LanguageKindHTML: LanguageKind = 'html'

LanguageKindIni: LanguageKind = 'ini'

LanguageKindJava: LanguageKind = 'java'

LanguageKindJavaScript: LanguageKind = 'javascript'

LanguageKindJavaScriptReact: LanguageKind = 'javascriptreact'

LanguageKindJSON: LanguageKind = 'json'

LanguageKindLaTeX: LanguageKind = 'latex'

LanguageKindLess: LanguageKind = 'less'

LanguageKindLua: LanguageKind = 'lua'

LanguageKindMakefile: LanguageKind = 'makefile'

LanguageKindMarkdown: LanguageKind = 'markdown'

LanguageKindObjectiveC: LanguageKind = 'objective-c'

LanguageKindObjectiveCPP: LanguageKind = 'objective-cpp'

LanguageKindPascal: LanguageKind = 'pascal'
"""@since 3.18.0
@proposed"""
# since 3.18.0

LanguageKindPerl: LanguageKind = 'perl'

LanguageKindPerl6: LanguageKind = 'perl6'

LanguageKindPHP: LanguageKind = 'php'

LanguageKindPowershell: LanguageKind = 'powershell'

LanguageKindPug: LanguageKind = 'jade'

LanguageKindPython: LanguageKind = 'python'

LanguageKindR: LanguageKind = 'r'

LanguageKindRazor: LanguageKind = 'razor'

LanguageKindRuby: LanguageKind = 'ruby'

LanguageKindRust: LanguageKind = 'rust'

LanguageKindSCSS: LanguageKind = 'scss'

LanguageKindSASS: LanguageKind = 'sass'

LanguageKindScala: LanguageKind = 'scala'

LanguageKindShaderLab: LanguageKind = 'shaderlab'

LanguageKindShellScript: LanguageKind = 'shellscript'

LanguageKindSQL: LanguageKind = 'sql'

LanguageKindSwift: LanguageKind = 'swift'

LanguageKindTypeScript: LanguageKind = 'typescript'

LanguageKindTypeScriptReact: LanguageKind = 'typescriptreact'

LanguageKindTeX: LanguageKind = 'tex'

LanguageKindVisualBasic: LanguageKind = 'vb'

LanguageKindXML: LanguageKind = 'xml'

LanguageKindXSL: LanguageKind = 'xsl'

LanguageKindYAML: LanguageKind = 'yaml'

InlineCompletionTriggerKind: TypeAlias = int
"""Describes how an {@link InlineCompletionItemProvider inline completion provider} was triggered.

@since 3.18.0
@proposed"""
# since 3.18.0

InlineCompletionTriggerKindInvoked: InlineCompletionTriggerKind = 1
"""Completion was triggered explicitly by a user gesture."""

InlineCompletionTriggerKindAutomatic: InlineCompletionTriggerKind = 2
"""Completion was triggered automatically while editing."""

PositionEncodingKind: TypeAlias = str
"""A set of predefined position encoding kinds.

@since 3.17.0"""
# since 3.17.0

PositionEncodingKindUTF8: PositionEncodingKind = 'utf-8'
"""Character offsets count UTF-8 code units (e.g. bytes)."""

PositionEncodingKindUTF16: PositionEncodingKind = 'utf-16'
"""Character offsets count UTF-16 code units.

This is the default and must always be supported
by servers"""

PositionEncodingKindUTF32: PositionEncodingKind = 'utf-32'
"""Character offsets count UTF-32 code units.

Implementation note: these are the same as Unicode codepoints,
so this `PositionEncodingKind` may also be used for an
encoding-agnostic representation of character offsets."""

FileChangeType: TypeAlias = int
"""The file event type"""

FileChangeTypeCreated: FileChangeType = 1
"""The file got created."""

FileChangeTypeChanged: FileChangeType = 2
"""The file got changed."""

FileChangeTypeDeleted: FileChangeType = 3
"""The file got deleted."""

WatchKind: TypeAlias = int

WatchKindCreate: WatchKind = 1
"""Interested in create events."""

WatchKindChange: WatchKind = 2
"""Interested in change events"""

WatchKindDelete: WatchKind = 4
"""Interested in delete events"""

DiagnosticSeverity: TypeAlias = int
"""The diagnostic's severity."""

DiagnosticSeverityError: DiagnosticSeverity = 1
"""Reports an error."""

DiagnosticSeverityWarning: DiagnosticSeverity = 2
"""Reports a warning."""

DiagnosticSeverityInformation: DiagnosticSeverity = 3
"""Reports an information."""

DiagnosticSeverityHint: DiagnosticSeverity = 4
"""Reports a hint."""

DiagnosticTag: TypeAlias = int
"""The diagnostic tags.

@since 3.15.0"""
# since 3.15.0

DiagnosticTagUnnecessary: DiagnosticTag = 1
"""Unused or unnecessary code.

Clients are allowed to render diagnostics with this tag faded out instead of having
an error squiggle."""

DiagnosticTagDeprecated: DiagnosticTag = 2
"""Deprecated or obsolete code.

Clients are allowed to rendered diagnostics with this tag strike through."""

CompletionTriggerKind: TypeAlias = int
"""How a completion was triggered"""

CompletionTriggerKindInvoked: CompletionTriggerKind = 1
"""Completion was triggered by typing an identifier (24x7 code
complete), manual invocation (e.g Ctrl+Space) or via API."""

CompletionTriggerKindTriggerCharacter: CompletionTriggerKind = 2
"""Completion was triggered by a trigger character specified by
the `triggerCharacters` properties of the `CompletionRegistrationOptions`."""

CompletionTriggerKindTriggerForIncompleteCompletions: CompletionTriggerKind = 3
"""Completion was re-triggered as current completion list is incomplete"""

ApplyKind: TypeAlias = int
"""Defines how values from a set of defaults and an individual item will be
merged.

@since 3.18.0"""
# since 3.18.0

ApplyKindReplace: ApplyKind = 1
"""The value from the individual item (if provided and not `null`) will be
used instead of the default."""

ApplyKindMerge: ApplyKind = 2
"""The value from the item will be merged with the default.

The specific rules for mergeing values are defined against each field
that supports merging."""

SignatureHelpTriggerKind: TypeAlias = int
"""How a signature help was triggered.

@since 3.15.0"""
# since 3.15.0

SignatureHelpTriggerKindInvoked: SignatureHelpTriggerKind = 1
"""Signature help was invoked manually by the user or by a command."""

SignatureHelpTriggerKindTriggerCharacter: SignatureHelpTriggerKind = 2
"""Signature help was triggered by a trigger character."""

SignatureHelpTriggerKindContentChange: SignatureHelpTriggerKind = 3
"""Signature help was triggered by the cursor moving or by the document content changing."""

CodeActionTriggerKind: TypeAlias = int
"""The reason why code actions were requested.

@since 3.17.0"""
# since 3.17.0

CodeActionTriggerKindInvoked: CodeActionTriggerKind = 1
"""Code actions were explicitly requested by the user or by an extension."""

CodeActionTriggerKindAutomatic: CodeActionTriggerKind = 2
"""Code actions were requested automatically.

This typically happens when current selection in a file changes, but can
also be triggered when file content changes."""

FileOperationPatternKind: TypeAlias = str
"""A pattern kind describing if a glob pattern matches a file a folder or
both.

@since 3.16.0"""
# since 3.16.0

FileOperationPatternKindfile: FileOperationPatternKind = 'file'
"""The pattern matches a file only."""

FileOperationPatternKindfolder: FileOperationPatternKind = 'folder'
"""The pattern matches a folder only."""

NotebookCellKind: TypeAlias = int
"""A notebook cell kind.

@since 3.17.0"""
# since 3.17.0

NotebookCellKindMarkup: NotebookCellKind = 1
"""A markup-cell is formatted source that is used for display."""

NotebookCellKindCode: NotebookCellKind = 2
"""A code-cell is source code."""

ResourceOperationKind: TypeAlias = str

ResourceOperationKindCreate: ResourceOperationKind = 'create'
"""Supports creating new files and folders."""

ResourceOperationKindRename: ResourceOperationKind = 'rename'
"""Supports renaming existing files and folders."""

ResourceOperationKindDelete: ResourceOperationKind = 'delete'
"""Supports deleting existing files and folders."""

FailureHandlingKind: TypeAlias = str

FailureHandlingKindAbort: FailureHandlingKind = 'abort'
"""Applying the workspace change is simply aborted if one of the changes provided
fails. All operations executed before the failing operation stay executed."""

FailureHandlingKindTransactional: FailureHandlingKind = 'transactional'
"""All operations are executed transactional. That means they either all
succeed or no changes at all are applied to the workspace."""

FailureHandlingKindTextOnlyTransactional: FailureHandlingKind = 'textOnlyTransactional'
"""If the workspace edit contains only textual file changes they are executed transactional.
If resource changes (create, rename or delete file) are part of the change the failure
handling strategy is abort."""

FailureHandlingKindUndo: FailureHandlingKind = 'undo'
"""The client tries to undo the operations already executed. But there is no
guarantee that this is succeeding."""

PrepareSupportDefaultBehavior: TypeAlias = int

PrepareSupportDefaultBehaviorIdentifier: PrepareSupportDefaultBehavior = 1
"""The client's default behavior is to select the identifier
according the to language's syntax rule."""

TokenFormat: TypeAlias = str

TokenFormatRelative: TokenFormat = 'relative'

@dataclass
class TextDocumentIdentifier:
    """A literal to identify a text document in the client."""
    uri: DocumentUri
    """The text document's uri."""

@dataclass
class Position:
    r"""Position in a text document expressed as zero-based line and character
    offset. Prior to 3.17 the offsets were always based on a UTF-16 string
    representation. So a string of the form `a𐐀b` the character offset of the
    character `a` is 0, the character offset of `𐐀` is 1 and the character
    offset of b is 3 since `𐐀` is represented using two code units in UTF-16.
    Since 3.17 clients and servers can agree on a different string encoding
    representation (e.g. UTF-8). The client announces it's supported encoding
    via the client capability [`general.positionEncodings`](https://microsoft.github.io/language-server-protocol/specifications/specification-current/#clientCapabilities).
    The value is an array of position encodings the client supports, with
    decreasing preference (e.g. the encoding at index `0` is the most preferred
    one). To stay backwards compatible the only mandatory encoding is UTF-16
    represented via the string `utf-16`. The server can pick one of the
    encodings offered by the client and signals that encoding back to the
    client via the initialize result's property
    [`capabilities.positionEncoding`](https://microsoft.github.io/language-server-protocol/specifications/specification-current/#serverCapabilities). If the string value
    `utf-16` is missing from the client's capability `general.positionEncodings`
    servers can safely assume that the client supports UTF-16. If the server
    omits the position encoding in its initialize result the encoding defaults
    to the string value `utf-16`. Implementation considerations: since the
    conversion from one encoding into another requires the content of the
    file / line the conversion is best done where the file is read which is
    usually on the server side.

    Positions are line end character agnostic. So you can not specify a position
    that denotes `\r|\n` or `\n|` where `|` represents the character offset.

    @since 3.17.0 - support for negotiated position encoding."""
    # since 3.17.0 - support for negotiated position encoding.
    line: int
    """Line position in a document (zero-based)."""
    character: int
    """Character offset on a line in a document (zero-based).

    The meaning of this offset is determined by the negotiated
    `PositionEncodingKind`."""

@dataclass
class TextDocumentPositionParams:
    """A parameter literal used in requests to pass a text document and a position inside that
    document."""
    textDocument: TextDocumentIdentifier
    """The text document."""
    position: Position
    """The position inside the text document."""

ProgressToken: TypeAlias = Union[int, str]

@dataclass
class ImplementationParams(TextDocumentPositionParams):
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class Range:
    """A range in a text document expressed as (zero-based) start and end positions.

    If you want to specify a range that contains a line including the line ending
    character(s) then use an end position denoting the start of the next line.
    For example:
    ```ts
    {
        start: { line: 5, character: 23 }
        end : { line 6, character : 0 }
    }
    ```"""
    start: Position
    """The range's start position."""
    end: Position
    """The range's end position."""

@dataclass
class Location:
    """Represents a location inside a resource, such as a line
    inside a text file."""
    uri: DocumentUri
    range: Range

Pattern: TypeAlias = str
"""The glob pattern to watch relative to the base path. Glob patterns can have the following syntax:
- `*` to match one or more characters in a path segment
- `?` to match on one character in a path segment
- `**` to match any number of path segments, including none
- `{}` to group conditions (e.g. `**​/*.{ts,js}` matches all TypeScript and JavaScript files)
- `[]` to declare a range of characters to match in a path segment (e.g., `example.[0-9]` to match on `example.0`, `example.1`, …)
- `[!...]` to negate a range of characters to match in a path segment (e.g., `example.[!0-9]` to match on `example.a`, `example.b`, but not `example.0`)

@since 3.17.0"""
# since 3.17.0

@dataclass
class WorkspaceFolder:
    """A workspace folder inside a client."""
    uri: URI
    """The associated URI for this workspace folder."""
    name: str
    """The name of the workspace folder. Used to refer to this
    workspace folder in the user interface."""

@dataclass
class RelativePattern:
    """A relative pattern is a helper to construct glob patterns that are matched
    relatively to a base URI. The common value for a `baseUri` is a workspace
    folder root, but it can be another absolute URI as well.

    @since 3.17.0"""
    # since 3.17.0
    baseUri: Union[WorkspaceFolder, URI]
    """A workspace folder or a base URI to which this pattern will be matched
    against relatively."""
    pattern: Pattern
    """The actual glob pattern;"""

GlobPattern: TypeAlias = Union[Pattern, RelativePattern]
"""The glob pattern. Either a string pattern or a relative pattern.

@since 3.17.0"""
# since 3.17.0

@dataclass
class TextDocumentFilterLanguage:
    """A document filter where `language` is required field.

    @since 3.18.0"""
    # since 3.18.0
    language: str
    """A language id, like `typescript`."""
    scheme: str = field(metadata={"optional": True})
    """A Uri {@link Uri.scheme scheme}, like `file` or `untitled`."""
    pattern: GlobPattern = field(metadata={"optional": True})
    """A glob pattern, like **​/*.{ts,js}. See TextDocumentFilter for examples.

    @since 3.18.0 - support for relative patterns. Whether clients support
    relative patterns depends on the client capability
    `textDocuments.filters.relativePatternSupport`."""
    # since 3.18.0 - support for relative patterns. Whether clients support
    # relative patterns depends on the client capability
    # `textDocuments.filters.relativePatternSupport`.

@dataclass
class TextDocumentFilterScheme:
    """A document filter where `scheme` is required field.

    @since 3.18.0"""
    # since 3.18.0
    language: str = field(metadata={"optional": True})
    """A language id, like `typescript`."""
    scheme: str
    """A Uri {@link Uri.scheme scheme}, like `file` or `untitled`."""
    pattern: GlobPattern = field(metadata={"optional": True})
    """A glob pattern, like **​/*.{ts,js}. See TextDocumentFilter for examples.

    @since 3.18.0 - support for relative patterns. Whether clients support
    relative patterns depends on the client capability
    `textDocuments.filters.relativePatternSupport`."""
    # since 3.18.0 - support for relative patterns. Whether clients support
    # relative patterns depends on the client capability
    # `textDocuments.filters.relativePatternSupport`.

@dataclass
class TextDocumentFilterPattern:
    """A document filter where `pattern` is required field.

    @since 3.18.0"""
    # since 3.18.0
    language: str = field(metadata={"optional": True})
    """A language id, like `typescript`."""
    scheme: str = field(metadata={"optional": True})
    """A Uri {@link Uri.scheme scheme}, like `file` or `untitled`."""
    pattern: GlobPattern
    """A glob pattern, like **​/*.{ts,js}. See TextDocumentFilter for examples.

    @since 3.18.0 - support for relative patterns. Whether clients support
    relative patterns depends on the client capability
    `textDocuments.filters.relativePatternSupport`."""
    # since 3.18.0 - support for relative patterns. Whether clients support
    # relative patterns depends on the client capability
    # `textDocuments.filters.relativePatternSupport`.

TextDocumentFilter: TypeAlias = Union[TextDocumentFilterLanguage, TextDocumentFilterScheme, TextDocumentFilterPattern]
"""A document filter denotes a document by different properties like
the {@link TextDocument.languageId language}, the {@link Uri.scheme scheme} of
its resource, or a glob-pattern that is applied to the {@link TextDocument.fileName path}.

Glob patterns can have the following syntax:
- `*` to match one or more characters in a path segment
- `?` to match on one character in a path segment
- `**` to match any number of path segments, including none
- `{}` to group sub patterns into an OR expression. (e.g. `**​/*.{ts,js}` matches all TypeScript and JavaScript files)
- `[]` to declare a range of characters to match in a path segment (e.g., `example.[0-9]` to match on `example.0`, `example.1`, …)
- `[!...]` to negate a range of characters to match in a path segment (e.g., `example.[!0-9]` to match on `example.a`, `example.b`, but not `example.0`)

@sample A language filter that applies to typescript files on disk: `{ language: 'typescript', scheme: 'file' }`
@sample A language filter that applies to all package.json paths: `{ language: 'json', pattern: '**package.json' }`

@since 3.17.0"""
# since 3.17.0

@dataclass
class NotebookDocumentFilterNotebookType:
    """A notebook document filter where `notebookType` is required field.

    @since 3.18.0"""
    # since 3.18.0
    notebookType: str
    """The type of the enclosing notebook."""
    scheme: str = field(metadata={"optional": True})
    """A Uri {@link Uri.scheme scheme}, like `file` or `untitled`."""
    pattern: GlobPattern = field(metadata={"optional": True})
    """A glob pattern."""

@dataclass
class NotebookDocumentFilterScheme:
    """A notebook document filter where `scheme` is required field.

    @since 3.18.0"""
    # since 3.18.0
    notebookType: str = field(metadata={"optional": True})
    """The type of the enclosing notebook."""
    scheme: str
    """A Uri {@link Uri.scheme scheme}, like `file` or `untitled`."""
    pattern: GlobPattern = field(metadata={"optional": True})
    """A glob pattern."""

@dataclass
class NotebookDocumentFilterPattern:
    """A notebook document filter where `pattern` is required field.

    @since 3.18.0"""
    # since 3.18.0
    notebookType: str = field(metadata={"optional": True})
    """The type of the enclosing notebook."""
    scheme: str = field(metadata={"optional": True})
    """A Uri {@link Uri.scheme scheme}, like `file` or `untitled`."""
    pattern: GlobPattern
    """A glob pattern."""

NotebookDocumentFilter: TypeAlias = Union[NotebookDocumentFilterNotebookType, NotebookDocumentFilterScheme, NotebookDocumentFilterPattern]
"""A notebook document filter denotes a notebook document by
different properties. The properties will be match
against the notebook's URI (same as with documents)

@since 3.17.0"""
# since 3.17.0

@dataclass
class NotebookCellTextDocumentFilter:
    """A notebook cell text document filter denotes a cell text
    document by different properties.

    @since 3.17.0"""
    # since 3.17.0
    notebook: Union[str, NotebookDocumentFilter]
    """A filter that matches against the notebook
    containing the notebook cell. If a string
    value is provided it matches against the
    notebook type. '*' matches every notebook."""
    language: str = field(metadata={"optional": True})
    """A language id like `python`.

    Will be matched against the language id of the
    notebook cell document. '*' matches every language."""

DocumentFilter: TypeAlias = Union[TextDocumentFilter, NotebookCellTextDocumentFilter]
"""A document filter describes a top level text document or
a notebook cell document.

@since 3.17.0 - support for NotebookCellTextDocumentFilter."""
# since 3.17.0 - support for NotebookCellTextDocumentFilter.

DocumentSelector: TypeAlias = List[DocumentFilter]
"""A document selector is the combination of one or many document filters.

@sample `let sel:DocumentSelector = [{ language: 'typescript' }, { language: 'json', pattern: '**∕tsconfig.json' }]`;

The use of a string as a document filter is deprecated @since 3.16.0."""
# since 3.16.0.

@dataclass
class TextDocumentRegistrationOptions:
    """General text document registration options."""
    documentSelector: Union[DocumentSelector, None]
    """A document selector to identify the scope of the registration. If set to null
    the document selector provided on the client side will be used."""

@dataclass
class ImplementationOptions:
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class ImplementationRegistrationOptions(TextDocumentRegistrationOptions, ImplementationOptions):
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class TypeDefinitionParams(TextDocumentPositionParams):
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class TypeDefinitionOptions:
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class TypeDefinitionRegistrationOptions(TextDocumentRegistrationOptions, TypeDefinitionOptions):
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class WorkspaceFoldersChangeEvent:
    """The workspace folder change event."""
    added: List[WorkspaceFolder]
    """The array of added workspace folders"""
    removed: List[WorkspaceFolder]
    """The array of the removed workspace folders"""

@dataclass
class DidChangeWorkspaceFoldersParams:
    """The parameters of a `workspace/didChangeWorkspaceFolders` notification."""
    event: WorkspaceFoldersChangeEvent
    """The actual workspace folder change event."""

@dataclass
class ConfigurationItem:
    scopeUri: URI = field(metadata={"optional": True})
    """The scope to get the configuration section for."""
    section: str = field(metadata={"optional": True})
    """The configuration section asked for."""

@dataclass
class ConfigurationParams:
    """The parameters of a configuration request."""
    items: List[ConfigurationItem]

@dataclass
class DocumentColorParams:
    """Parameters for a {@link DocumentColorRequest}."""
    textDocument: TextDocumentIdentifier
    """The text document."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class Color:
    """Represents a color in RGBA space."""
    red: float
    """The red component of this color in the range [0-1]."""
    green: float
    """The green component of this color in the range [0-1]."""
    blue: float
    """The blue component of this color in the range [0-1]."""
    alpha: float
    """The alpha component of this color in the range [0-1]."""

@dataclass
class ColorInformation:
    """Represents a color range from a document."""
    range: Range
    """The range in the document where this color appears."""
    color: Color
    """The actual color value for this color range."""

@dataclass
class DocumentColorOptions:
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class DocumentColorRegistrationOptions(TextDocumentRegistrationOptions, DocumentColorOptions):
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class ColorPresentationParams:
    """Parameters for a {@link ColorPresentationRequest}."""
    textDocument: TextDocumentIdentifier
    """The text document."""
    color: Color
    """The color to request presentations for."""
    range: Range
    """The range where the color would be inserted. Serves as a context."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class TextEdit:
    """A text edit applicable to a text document."""
    range: Range
    """The range of the text document to be manipulated. To insert
    text into a document create a range where start === end."""
    newText: str
    """The string to be inserted. For delete operations use an
    empty string."""

@dataclass
class ColorPresentation:
    label: str
    """The label of this color presentation. It will be shown on the color
    picker header. By default this is also the text that is inserted when selecting
    this color presentation."""
    textEdit: TextEdit = field(metadata={"optional": True})
    """An {@link TextEdit edit} which is applied to a document when selecting
    this presentation for the color.  When `falsy` the {@link ColorPresentation.label label}
    is used."""
    additionalTextEdits: List[TextEdit] = field(metadata={"optional": True})
    """An optional array of additional {@link TextEdit text edits} that are applied when
    selecting this color presentation. Edits must not overlap with the main {@link ColorPresentation.textEdit edit} nor with themselves."""

@dataclass
class WorkDoneProgressOptions:
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class FoldingRangeParams:
    """Parameters for a {@link FoldingRangeRequest}."""
    textDocument: TextDocumentIdentifier
    """The text document."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class FoldingRange:
    """Represents a folding range. To be valid, start and end line must be bigger than zero and smaller
    than the number of lines in the document. Clients are free to ignore invalid ranges."""
    startLine: int
    """The zero-based start line of the range to fold. The folded area starts after the line's last character.
    To be valid, the end must be zero or larger and smaller than the number of lines in the document."""
    startCharacter: int = field(metadata={"optional": True})
    """The zero-based character offset from where the folded range starts. If not defined, defaults to the length of the start line."""
    endLine: int
    """The zero-based end line of the range to fold. The folded area ends with the line's last character.
    To be valid, the end must be zero or larger and smaller than the number of lines in the document."""
    endCharacter: int = field(metadata={"optional": True})
    """The zero-based character offset before the folded range ends. If not defined, defaults to the length of the end line."""
    kind: FoldingRangeKind = field(metadata={"optional": True})
    """Describes the kind of the folding range such as 'comment' or 'region'. The kind
    is used to categorize folding ranges and used by commands like 'Fold all comments'.
    See {@link FoldingRangeKind} for an enumeration of standardized kinds."""
    collapsedText: str = field(metadata={"optional": True})
    """The text that the client should show when the specified range is
    collapsed. If not defined or not supported by the client, a default
    will be chosen by the client.

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class FoldingRangeOptions:
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class FoldingRangeRegistrationOptions(TextDocumentRegistrationOptions, FoldingRangeOptions):
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class DeclarationParams(TextDocumentPositionParams):
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class DeclarationOptions:
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class DeclarationRegistrationOptions(DeclarationOptions, TextDocumentRegistrationOptions):
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class SelectionRangeParams:
    """A parameter literal used in selection range requests."""
    textDocument: TextDocumentIdentifier
    """The text document."""
    positions: List[Position]
    """The positions inside the text document."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class SelectionRange:
    """A selection range represents a part of a selection hierarchy. A selection range
    may have a parent selection range that contains it."""
    range: Range
    """The {@link Range range} of this selection range."""
    parent: "SelectionRange" = field(metadata={"optional": True})
    """The parent selection range containing this range. Therefore `parent.range` must contain `this.range`."""

@dataclass
class SelectionRangeOptions:
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class SelectionRangeRegistrationOptions(SelectionRangeOptions, TextDocumentRegistrationOptions):
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class WorkDoneProgressCreateParams:
    token: ProgressToken
    """The token to be used to report progress."""

@dataclass
class WorkDoneProgressCancelParams:
    token: ProgressToken
    """The token to be used to report progress."""

@dataclass
class CallHierarchyPrepareParams(TextDocumentPositionParams):
    """The parameter of a `textDocument/prepareCallHierarchy` request.

    @since 3.16.0"""
    # since 3.16.0
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class CallHierarchyItem:
    """Represents programming constructs like functions or constructors in the context
    of call hierarchy.

    @since 3.16.0"""
    # since 3.16.0
    name: str
    """The name of this item."""
    kind: SymbolKind
    """The kind of this item."""
    tags: List[SymbolTag] = field(metadata={"optional": True})
    """Tags for this item."""
    detail: str = field(metadata={"optional": True})
    """More detail for this item, e.g. the signature of a function."""
    uri: DocumentUri
    """The resource identifier of this item."""
    range: Range
    """The range enclosing this symbol not including leading/trailing whitespace but everything else, e.g. comments and code."""
    selectionRange: Range
    """The range that should be selected and revealed when this symbol is being picked, e.g. the name of a function.
    Must be contained by the {@link CallHierarchyItem.range `range`}."""
    data: Any = field(metadata={"optional": True})
    """A data entry field that is preserved between a call hierarchy prepare and
    incoming calls or outgoing calls requests."""

@dataclass
class CallHierarchyOptions:
    """Call hierarchy options used during static registration.

    @since 3.16.0"""
    # since 3.16.0
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class CallHierarchyRegistrationOptions(TextDocumentRegistrationOptions, CallHierarchyOptions):
    """Call hierarchy options used during static or dynamic registration.

    @since 3.16.0"""
    # since 3.16.0
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class CallHierarchyIncomingCallsParams:
    """The parameter of a `callHierarchy/incomingCalls` request.

    @since 3.16.0"""
    # since 3.16.0
    item: CallHierarchyItem
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class CallHierarchyIncomingCall:
    """Represents an incoming call, e.g. a caller of a method or constructor.

    @since 3.16.0"""
    # since 3.16.0
    from_: CallHierarchyItem
    """The item that makes the call."""
    fromRanges: List[Range]
    """The ranges at which the calls appear. This is relative to the caller
    denoted by {@link CallHierarchyIncomingCall.from `this.from`}."""

@dataclass
class CallHierarchyOutgoingCallsParams:
    """The parameter of a `callHierarchy/outgoingCalls` request.

    @since 3.16.0"""
    # since 3.16.0
    item: CallHierarchyItem
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class CallHierarchyOutgoingCall:
    """Represents an outgoing call, e.g. calling a getter from a method or a method from a constructor etc.

    @since 3.16.0"""
    # since 3.16.0
    to: CallHierarchyItem
    """The item that is called."""
    fromRanges: List[Range]
    """The range at which this item is called. This is the range relative to the caller, e.g the item
    passed to {@link CallHierarchyItemProvider.provideCallHierarchyOutgoingCalls `provideCallHierarchyOutgoingCalls`}
    and not {@link CallHierarchyOutgoingCall.to `this.to`}."""

@dataclass
class SemanticTokensParams:
    """@since 3.16.0"""
    # since 3.16.0
    textDocument: TextDocumentIdentifier
    """The text document."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class SemanticTokens:
    """@since 3.16.0"""
    # since 3.16.0
    resultId: str = field(metadata={"optional": True})
    """An optional result id. If provided and clients support delta updating
    the client will include the result id in the next semantic token request.
    A server can then instead of computing all semantic tokens again simply
    send a delta."""
    data: List[int]
    """The actual tokens."""

@dataclass
class SemanticTokensPartialResult:
    """@since 3.16.0"""
    # since 3.16.0
    data: List[int]

@dataclass
class SemanticTokensLegend:
    """@since 3.16.0"""
    # since 3.16.0
    tokenTypes: List[str]
    """The token types a server uses."""
    tokenModifiers: List[str]
    """The token modifiers a server uses."""

@dataclass
class SemanticTokensFullDelta:
    """Semantic tokens options to support deltas for full documents

    @since 3.18.0"""
    # since 3.18.0
    delta: bool = field(metadata={"optional": True})
    """The server supports deltas for full documents."""

@dataclass
class SemanticTokensOptions:
    """@since 3.16.0"""
    # since 3.16.0
    legend: SemanticTokensLegend
    """The legend used by the server"""
    range: Union[bool, Literal[{'properties': []}]] = field(metadata={"optional": True})
    """Server supports providing semantic tokens for a specific range
    of a document."""
    full: Union[bool, SemanticTokensFullDelta] = field(metadata={"optional": True})
    """Server supports providing semantic tokens for a full document."""
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class SemanticTokensRegistrationOptions(TextDocumentRegistrationOptions, SemanticTokensOptions):
    """@since 3.16.0"""
    # since 3.16.0
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class SemanticTokensDeltaParams:
    """@since 3.16.0"""
    # since 3.16.0
    textDocument: TextDocumentIdentifier
    """The text document."""
    previousResultId: str
    """The result id of a previous response. The result Id can either point to a full response
    or a delta response depending on what was received last."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class SemanticTokensEdit:
    """@since 3.16.0"""
    # since 3.16.0
    start: int
    """The start offset of the edit."""
    deleteCount: int
    """The count of elements to remove."""
    data: List[int] = field(metadata={"optional": True})
    """The elements to insert."""

@dataclass
class SemanticTokensDelta:
    """@since 3.16.0"""
    # since 3.16.0
    resultId: str = field(metadata={"optional": True})
    edits: List[SemanticTokensEdit]
    """The semantic token edits to transform a previous result into a new result."""

@dataclass
class SemanticTokensDeltaPartialResult:
    """@since 3.16.0"""
    # since 3.16.0
    edits: List[SemanticTokensEdit]

@dataclass
class SemanticTokensRangeParams:
    """@since 3.16.0"""
    # since 3.16.0
    textDocument: TextDocumentIdentifier
    """The text document."""
    range: Range
    """The range the semantic tokens are requested for."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class ShowDocumentParams:
    """Params to show a resource in the UI.

    @since 3.16.0"""
    # since 3.16.0
    uri: URI
    """The uri to show."""
    external: bool = field(metadata={"optional": True})
    """Indicates to show the resource in an external program.
    To show, for example, `https://code.visualstudio.com/`
    in the default WEB browser set `external` to `true`."""
    takeFocus: bool = field(metadata={"optional": True})
    """An optional property to indicate whether the editor
    showing the document should take focus or not.
    Clients might ignore this property if an external
    program is started."""
    selection: Range = field(metadata={"optional": True})
    """An optional selection range if the document is a text
    document. Clients might ignore the property if an
    external program is started or the file is not a text
    file."""

@dataclass
class ShowDocumentResult:
    """The result of a showDocument request.

    @since 3.16.0"""
    # since 3.16.0
    success: bool
    """A boolean indicating if the show was successful."""

@dataclass
class LinkedEditingRangeParams(TextDocumentPositionParams):
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class LinkedEditingRanges:
    """The result of a linked editing range request.

    @since 3.16.0"""
    # since 3.16.0
    ranges: List[Range]
    """A list of ranges that can be edited together. The ranges must have
    identical length and contain identical text content. The ranges cannot overlap."""
    wordPattern: str = field(metadata={"optional": True})
    """An optional word pattern (regular expression) that describes valid contents for
    the given ranges. If no pattern is provided, the client configuration's word
    pattern will be used."""

@dataclass
class LinkedEditingRangeOptions:
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class LinkedEditingRangeRegistrationOptions(TextDocumentRegistrationOptions, LinkedEditingRangeOptions):
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class FileCreate:
    """Represents information on a file/folder create.

    @since 3.16.0"""
    # since 3.16.0
    uri: str
    """A file:// URI for the location of the file/folder being created."""

@dataclass
class CreateFilesParams:
    """The parameters sent in notifications/requests for user-initiated creation of
    files.

    @since 3.16.0"""
    # since 3.16.0
    files: List[FileCreate]
    """An array of all files/folders created in this operation."""

@dataclass
class OptionalVersionedTextDocumentIdentifier(TextDocumentIdentifier):
    """A text document identifier to optionally denote a specific version of a text document."""
    version: Union[int, None]
    """The version number of this document. If a versioned text document identifier
    is sent from the server to the client and the file is not open in the editor
    (the server has not received an open notification before) the server can send
    `null` to indicate that the version is unknown and the content on disk is the
    truth (as specified with document content ownership)."""

ChangeAnnotationIdentifier: TypeAlias = str
"""An identifier to refer to a change annotation stored with a workspace edit."""

@dataclass
class AnnotatedTextEdit(TextEdit):
    """A special text edit with an additional change annotation.

    @since 3.16.0."""
    # since 3.16.0.
    annotationId: ChangeAnnotationIdentifier
    """The actual identifier of the change annotation"""

@dataclass
class StringValue:
    """A string value used as a snippet is a template which allows to insert text
    and to control the editor cursor when insertion happens.

    A snippet can define tab stops and placeholders with `$1`, `$2`
    and `${3:foo}`. `$0` defines the final tab stop, it defaults to
    the end of the snippet. Variables are defined with `$name` and
    `${name:default value}`.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    kind: Literal['snippet']
    """The kind of string value."""
    value: str
    """The snippet string."""

@dataclass
class SnippetTextEdit:
    """An interactive text edit.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    range: Range
    """The range of the text document to be manipulated."""
    snippet: StringValue
    """The snippet to be inserted."""
    annotationId: ChangeAnnotationIdentifier = field(metadata={"optional": True})
    """The actual identifier of the snippet edit."""

@dataclass
class TextDocumentEdit:
    """Describes textual changes on a text document. A TextDocumentEdit describes all changes
    on a document version Si and after they are applied move the document to version Si+1.
    So the creator of a TextDocumentEdit doesn't need to sort the array of edits or do any
    kind of ordering. However the edits must be non overlapping."""
    textDocument: OptionalVersionedTextDocumentIdentifier
    """The text document to change."""
    edits: List[Union[TextEdit, AnnotatedTextEdit, SnippetTextEdit]]
    """The edits to be applied.

    @since 3.16.0 - support for AnnotatedTextEdit. This is guarded using a
    client capability.

    @since 3.18.0 - support for SnippetTextEdit. This is guarded using a
    client capability."""
    # since 3.18.0 - support for SnippetTextEdit. This is guarded using a
    # client capability.

@dataclass
class ResourceOperation:
    """A generic resource operation."""
    kind: str
    """The resource operation kind."""
    annotationId: ChangeAnnotationIdentifier = field(metadata={"optional": True})
    """An optional annotation identifier describing the operation.

    @since 3.16.0"""
    # since 3.16.0

@dataclass
class CreateFileOptions:
    """Options to create a file."""
    overwrite: bool = field(metadata={"optional": True})
    """Overwrite existing file. Overwrite wins over `ignoreIfExists`"""
    ignoreIfExists: bool = field(metadata={"optional": True})
    """Ignore if exists."""

@dataclass
class CreateFile(ResourceOperation):
    """Create file operation."""
    kind: Literal['create']
    """A create"""
    uri: DocumentUri
    """The resource to create."""
    options: CreateFileOptions = field(metadata={"optional": True})
    """Additional options"""

@dataclass
class RenameFileOptions:
    """Rename file options"""
    overwrite: bool = field(metadata={"optional": True})
    """Overwrite target if existing. Overwrite wins over `ignoreIfExists`"""
    ignoreIfExists: bool = field(metadata={"optional": True})
    """Ignores if target exists."""

@dataclass
class RenameFile(ResourceOperation):
    """Rename file operation"""
    kind: Literal['rename']
    """A rename"""
    oldUri: DocumentUri
    """The old (existing) location."""
    newUri: DocumentUri
    """The new location."""
    options: RenameFileOptions = field(metadata={"optional": True})
    """Rename options."""

@dataclass
class DeleteFileOptions:
    """Delete file options"""
    recursive: bool = field(metadata={"optional": True})
    """Delete the content recursively if a folder is denoted."""
    ignoreIfNotExists: bool = field(metadata={"optional": True})
    """Ignore the operation if the file doesn't exist."""

@dataclass
class DeleteFile(ResourceOperation):
    """Delete file operation"""
    kind: Literal['delete']
    """A delete"""
    uri: DocumentUri
    """The file to delete."""
    options: DeleteFileOptions = field(metadata={"optional": True})
    """Delete options."""

@dataclass
class ChangeAnnotation:
    """Additional information that describes document changes.

    @since 3.16.0"""
    # since 3.16.0
    label: str
    """A human-readable string describing the actual change. The string
    is rendered prominent in the user interface."""
    needsConfirmation: bool = field(metadata={"optional": True})
    """A flag which indicates that user confirmation is needed
    before applying the change."""
    description: str = field(metadata={"optional": True})
    """A human-readable string which is rendered less prominent in
    the user interface."""

@dataclass
class WorkspaceEdit:
    """A workspace edit represents changes to many resources managed in the workspace. The edit
    should either provide `changes` or `documentChanges`. If documentChanges are present
    they are preferred over `changes` if the client can handle versioned document edits.

    Since version 3.13.0 a workspace edit can contain resource operations as well. If resource
    operations are present clients need to execute the operations in the order in which they
    are provided. So a workspace edit for example can consist of the following two changes:
    (1) a create file a.txt and (2) a text document edit which insert text into file a.txt.

    An invalid sequence (e.g. (1) delete file a.txt and (2) insert text into file a.txt) will
    cause failure of the operation. How the client recovers from the failure is described by
    the client capability: `workspace.workspaceEdit.failureHandling`"""
    changes: Dict[DocumentUri, List[TextEdit]] = field(metadata={"optional": True})
    """Holds changes to existing resources."""
    documentChanges: List[Union[TextDocumentEdit, CreateFile, RenameFile, DeleteFile]] = field(metadata={"optional": True})
    """Depending on the client capability `workspace.workspaceEdit.resourceOperations` document changes
    are either an array of `TextDocumentEdit`s to express changes to n different text documents
    where each text document edit addresses a specific version of a text document. Or it can contain
    above `TextDocumentEdit`s mixed with create, rename and delete file / folder operations.

    Whether a client supports versioned document edits is expressed via
    `workspace.workspaceEdit.documentChanges` client capability.

    If a client neither supports `documentChanges` nor `workspace.workspaceEdit.resourceOperations` then
    only plain `TextEdit`s using the `changes` property are supported."""
    changeAnnotations: Dict[ChangeAnnotationIdentifier, ChangeAnnotation] = field(metadata={"optional": True})
    """A map of change annotations that can be referenced in `AnnotatedTextEdit`s or create, rename and
    delete file / folder operations.

    Whether clients honor this property depends on the client capability `workspace.changeAnnotationSupport`.

    @since 3.16.0"""
    # since 3.16.0

@dataclass
class FileOperationPatternOptions:
    """Matching options for the file operation pattern.

    @since 3.16.0"""
    # since 3.16.0
    ignoreCase: bool = field(metadata={"optional": True})
    """The pattern should be matched ignoring casing."""

@dataclass
class FileOperationPattern:
    """A pattern to describe in which file operation requests or notifications
    the server is interested in receiving.

    @since 3.16.0"""
    # since 3.16.0
    glob: str
    """The glob pattern to match. Glob patterns can have the following syntax:
    - `*` to match one or more characters in a path segment
    - `?` to match on one character in a path segment
    - `**` to match any number of path segments, including none
    - `{}` to group sub patterns into an OR expression. (e.g. `**​/*.{ts,js}` matches all TypeScript and JavaScript files)
    - `[]` to declare a range of characters to match in a path segment (e.g., `example.[0-9]` to match on `example.0`, `example.1`, …)
    - `[!...]` to negate a range of characters to match in a path segment (e.g., `example.[!0-9]` to match on `example.a`, `example.b`, but not `example.0`)"""
    matches: FileOperationPatternKind = field(metadata={"optional": True})
    """Whether to match files or folders with this pattern.

    Matches both if undefined."""
    options: FileOperationPatternOptions = field(metadata={"optional": True})
    """Additional options used during matching."""

@dataclass
class FileOperationFilter:
    """A filter to describe in which file operation requests or notifications
    the server is interested in receiving.

    @since 3.16.0"""
    # since 3.16.0
    scheme: str = field(metadata={"optional": True})
    """A Uri scheme like `file` or `untitled`."""
    pattern: FileOperationPattern
    """The actual file operation pattern."""

@dataclass
class FileOperationRegistrationOptions:
    """The options to register for file operations.

    @since 3.16.0"""
    # since 3.16.0
    filters: List[FileOperationFilter]
    """The actual filters."""

@dataclass
class FileRename:
    """Represents information on a file/folder rename.

    @since 3.16.0"""
    # since 3.16.0
    oldUri: str
    """A file:// URI for the original location of the file/folder being renamed."""
    newUri: str
    """A file:// URI for the new location of the file/folder being renamed."""

@dataclass
class RenameFilesParams:
    """The parameters sent in notifications/requests for user-initiated renames of
    files.

    @since 3.16.0"""
    # since 3.16.0
    files: List[FileRename]
    """An array of all files/folders renamed in this operation. When a folder is renamed, only
    the folder will be included, and not its children."""

@dataclass
class FileDelete:
    """Represents information on a file/folder delete.

    @since 3.16.0"""
    # since 3.16.0
    uri: str
    """A file:// URI for the location of the file/folder being deleted."""

@dataclass
class DeleteFilesParams:
    """The parameters sent in notifications/requests for user-initiated deletes of
    files.

    @since 3.16.0"""
    # since 3.16.0
    files: List[FileDelete]
    """An array of all files/folders deleted in this operation."""

@dataclass
class MonikerParams(TextDocumentPositionParams):
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class Moniker:
    """Moniker definition to match LSIF 0.5 moniker definition.

    @since 3.16.0"""
    # since 3.16.0
    scheme: str
    """The scheme of the moniker. For example tsc or .Net"""
    identifier: str
    """The identifier of the moniker. The value is opaque in LSIF however
    schema owners are allowed to define the structure if they want."""
    unique: UniquenessLevel
    """The scope in which the moniker is unique"""
    kind: MonikerKind = field(metadata={"optional": True})
    """The moniker kind if known."""

@dataclass
class MonikerOptions:
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class MonikerRegistrationOptions(TextDocumentRegistrationOptions, MonikerOptions):
    """"""

@dataclass
class TypeHierarchyPrepareParams(TextDocumentPositionParams):
    """The parameter of a `textDocument/prepareTypeHierarchy` request.

    @since 3.17.0"""
    # since 3.17.0
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class TypeHierarchyItem:
    """@since 3.17.0"""
    # since 3.17.0
    name: str
    """The name of this item."""
    kind: SymbolKind
    """The kind of this item."""
    tags: List[SymbolTag] = field(metadata={"optional": True})
    """Tags for this item."""
    detail: str = field(metadata={"optional": True})
    """More detail for this item, e.g. the signature of a function."""
    uri: DocumentUri
    """The resource identifier of this item."""
    range: Range
    """The range enclosing this symbol not including leading/trailing whitespace
    but everything else, e.g. comments and code."""
    selectionRange: Range
    """The range that should be selected and revealed when this symbol is being
    picked, e.g. the name of a function. Must be contained by the
    {@link TypeHierarchyItem.range `range`}."""
    data: Any = field(metadata={"optional": True})
    """A data entry field that is preserved between a type hierarchy prepare and
    supertypes or subtypes requests. It could also be used to identify the
    type hierarchy in the server, helping improve the performance on
    resolving supertypes and subtypes."""

@dataclass
class TypeHierarchyOptions:
    """Type hierarchy options used during static registration.

    @since 3.17.0"""
    # since 3.17.0
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class TypeHierarchyRegistrationOptions(TextDocumentRegistrationOptions, TypeHierarchyOptions):
    """Type hierarchy options used during static or dynamic registration.

    @since 3.17.0"""
    # since 3.17.0
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class TypeHierarchySupertypesParams:
    """The parameter of a `typeHierarchy/supertypes` request.

    @since 3.17.0"""
    # since 3.17.0
    item: TypeHierarchyItem
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class TypeHierarchySubtypesParams:
    """The parameter of a `typeHierarchy/subtypes` request.

    @since 3.17.0"""
    # since 3.17.0
    item: TypeHierarchyItem
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class InlineValueContext:
    """@since 3.17.0"""
    # since 3.17.0
    frameId: int
    """The stack frame (as a DAP Id) where the execution has stopped."""
    stoppedLocation: Range
    """The document range where execution has stopped.
    Typically the end position of the range denotes the line where the inline values are shown."""

@dataclass
class InlineValueParams:
    """A parameter literal used in inline value requests.

    @since 3.17.0"""
    # since 3.17.0
    textDocument: TextDocumentIdentifier
    """The text document."""
    range: Range
    """The document range for which inline values should be computed."""
    context: InlineValueContext
    """Additional information about the context in which inline values were
    requested."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class InlineValueOptions:
    """Inline value options used during static registration.

    @since 3.17.0"""
    # since 3.17.0
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class InlineValueRegistrationOptions(InlineValueOptions, TextDocumentRegistrationOptions):
    """Inline value options used during static or dynamic registration.

    @since 3.17.0"""
    # since 3.17.0
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class InlayHintParams:
    """A parameter literal used in inlay hint requests.

    @since 3.17.0"""
    # since 3.17.0
    textDocument: TextDocumentIdentifier
    """The text document."""
    range: Range
    """The document range for which inlay hints should be computed."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class MarkupContent:
    r"""A `MarkupContent` literal represents a string value which content is interpreted base on its
    kind flag. Currently the protocol supports `plaintext` and `markdown` as markup kinds.

    If the kind is `markdown` then the value can contain fenced code blocks like in GitHub issues.
    See https://help.github.com/articles/creating-and-highlighting-code-blocks/#syntax-highlighting

    Here is an example how such a string can be constructed using JavaScript / TypeScript:
    ```ts
    let markdown: MarkdownContent = {
     kind: MarkupKind.Markdown,
     value: [
       '# Header',
       'Some text',
       '```typescript',
       'someCode();',
       '```'
     ].join('\n')
    };
    ```

    *Please Note* that clients might sanitize the return markdown. A client could decide to
    remove HTML from the markdown to avoid script execution."""
    kind: MarkupKind
    """The type of the Markup"""
    value: str
    """The content itself"""

@dataclass
class Command:
    """Represents a reference to a command. Provides a title which
    will be used to represent a command in the UI and, optionally,
    an array of arguments which will be passed to the command handler
    function when invoked."""
    title: str
    """Title of the command, like `save`."""
    tooltip: str = field(metadata={"optional": True})
    """An optional tooltip.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    command: str
    """The identifier of the actual command handler."""
    arguments: List[Any] = field(metadata={"optional": True})
    """Arguments that the command handler should be
    invoked with."""

@dataclass
class InlayHintLabelPart:
    """An inlay hint label part allows for interactive and composite labels
    of inlay hints.

    @since 3.17.0"""
    # since 3.17.0
    value: str
    """The value of this label part."""
    tooltip: Union[str, MarkupContent] = field(metadata={"optional": True})
    """The tooltip text when you hover over this label part. Depending on
    the client capability `inlayHint.resolveSupport` clients might resolve
    this property late using the resolve request."""
    location: Location = field(metadata={"optional": True})
    """An optional source code location that represents this
    label part.

    The editor will use this location for the hover and for code navigation
    features: This part will become a clickable link that resolves to the
    definition of the symbol at the given location (not necessarily the
    location itself), it shows the hover that shows at the given location,
    and it shows a context menu with further code navigation commands.

    Depending on the client capability `inlayHint.resolveSupport` clients
    might resolve this property late using the resolve request."""
    command: Command = field(metadata={"optional": True})
    """An optional command for this label part.

    Depending on the client capability `inlayHint.resolveSupport` clients
    might resolve this property late using the resolve request."""

@dataclass
class InlayHint:
    """Inlay hint information.

    @since 3.17.0"""
    # since 3.17.0
    position: Position
    """The position of this hint.

    If multiple hints have the same position, they will be shown in the order
    they appear in the response."""
    label: Union[str, List[InlayHintLabelPart]]
    """The label of this hint. A human readable string or an array of
    InlayHintLabelPart label parts.

    *Note* that neither the string nor the label part can be empty."""
    kind: InlayHintKind = field(metadata={"optional": True})
    """The kind of this hint. Can be omitted in which case the client
    should fall back to a reasonable default."""
    textEdits: List[TextEdit] = field(metadata={"optional": True})
    """Optional text edits that are performed when accepting this inlay hint.

    *Note* that edits are expected to change the document so that the inlay
    hint (or its nearest variant) is now part of the document and the inlay
    hint itself is now obsolete."""
    tooltip: Union[str, MarkupContent] = field(metadata={"optional": True})
    """The tooltip text when you hover over this item."""
    paddingLeft: bool = field(metadata={"optional": True})
    """Render padding before the hint.

    Note: Padding should use the editor's background color, not the
    background color of the hint itself. That means padding can be used
    to visually align/separate an inlay hint."""
    paddingRight: bool = field(metadata={"optional": True})
    """Render padding after the hint.

    Note: Padding should use the editor's background color, not the
    background color of the hint itself. That means padding can be used
    to visually align/separate an inlay hint."""
    data: Any = field(metadata={"optional": True})
    """A data entry field that is preserved on an inlay hint between
    a `textDocument/inlayHint` and a `inlayHint/resolve` request."""

@dataclass
class InlayHintOptions:
    """Inlay hint options used during static registration.

    @since 3.17.0"""
    # since 3.17.0
    resolveProvider: bool = field(metadata={"optional": True})
    """The server provides support to resolve additional
    information for an inlay hint item."""
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class InlayHintRegistrationOptions(InlayHintOptions, TextDocumentRegistrationOptions):
    """Inlay hint options used during static or dynamic registration.

    @since 3.17.0"""
    # since 3.17.0
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class DocumentDiagnosticParams:
    """Parameters of the document diagnostic request.

    @since 3.17.0"""
    # since 3.17.0
    textDocument: TextDocumentIdentifier
    """The text document."""
    identifier: str = field(metadata={"optional": True})
    """The additional identifier  provided during registration."""
    previousResultId: str = field(metadata={"optional": True})
    """The result id of a previous response if provided."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class CodeDescription:
    """Structure to capture a description for an error code.

    @since 3.16.0"""
    # since 3.16.0
    href: URI
    """An URI to open with more information about the diagnostic error."""

@dataclass
class DiagnosticRelatedInformation:
    """Represents a related message and source code location for a diagnostic. This should be
    used to point to code locations that cause or related to a diagnostics, e.g when duplicating
    a symbol in a scope."""
    location: Location
    """The location of this related diagnostic information."""
    message: str
    """The message of this related diagnostic information."""

@dataclass
class Diagnostic:
    """Represents a diagnostic, such as a compiler error or warning. Diagnostic objects
    are only valid in the scope of a resource."""
    range: Range
    """The range at which the message applies"""
    severity: DiagnosticSeverity = field(metadata={"optional": True})
    """The diagnostic's severity. To avoid interpretation mismatches when a
    server is used with different clients it is highly recommended that servers
    always provide a severity value."""
    code: Union[int, str] = field(metadata={"optional": True})
    """The diagnostic's code, which usually appear in the user interface."""
    codeDescription: CodeDescription = field(metadata={"optional": True})
    """An optional property to describe the error code.
    Requires the code field (above) to be present/not null.

    @since 3.16.0"""
    # since 3.16.0
    source: str = field(metadata={"optional": True})
    """A human-readable string describing the source of this
    diagnostic, e.g. 'typescript' or 'super lint'. It usually
    appears in the user interface."""
    message: str
    """The diagnostic's message. It usually appears in the user interface"""
    tags: List[DiagnosticTag] = field(metadata={"optional": True})
    """Additional metadata about the diagnostic.

    @since 3.15.0"""
    # since 3.15.0
    relatedInformation: List[DiagnosticRelatedInformation] = field(metadata={"optional": True})
    """An array of related diagnostic information, e.g. when symbol-names within
    a scope collide all definitions can be marked via this property."""
    data: Any = field(metadata={"optional": True})
    """A data entry field that is preserved between a `textDocument/publishDiagnostics`
    notification and `textDocument/codeAction` request.

    @since 3.16.0"""
    # since 3.16.0

@dataclass
class FullDocumentDiagnosticReport:
    """A diagnostic report with a full set of problems.

    @since 3.17.0"""
    # since 3.17.0
    kind: Literal['full']
    """A full document diagnostic report."""
    resultId: str = field(metadata={"optional": True})
    """An optional result id. If provided it will
    be sent on the next diagnostic request for the
    same document."""
    items: List[Diagnostic]
    """The actual items."""

@dataclass
class UnchangedDocumentDiagnosticReport:
    """A diagnostic report indicating that the last returned
    report is still accurate.

    @since 3.17.0"""
    # since 3.17.0
    kind: Literal['unchanged']
    """A document diagnostic report indicating
    no changes to the last result. A server can
    only return `unchanged` if result ids are
    provided."""
    resultId: str
    """A result id which will be sent on the next
    diagnostic request for the same document."""

@dataclass
class DocumentDiagnosticReportPartialResult:
    """A partial result for a document diagnostic report.

    @since 3.17.0"""
    # since 3.17.0
    relatedDocuments: Dict[DocumentUri, Union[FullDocumentDiagnosticReport, UnchangedDocumentDiagnosticReport]]

@dataclass
class DiagnosticServerCancellationData:
    """Cancellation data returned from a diagnostic request.

    @since 3.17.0"""
    # since 3.17.0
    retriggerRequest: bool

@dataclass
class DiagnosticOptions:
    """Diagnostic options.

    @since 3.17.0"""
    # since 3.17.0
    identifier: str = field(metadata={"optional": True})
    """An optional identifier under which the diagnostics are
    managed by the client."""
    interFileDependencies: bool
    """Whether the language has inter file dependencies meaning that
    editing code in one file can result in a different diagnostic
    set in another file. Inter file dependencies are common for
    most programming languages and typically uncommon for linters."""
    workspaceDiagnostics: bool
    """The server provides support for workspace diagnostics as well."""
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class DiagnosticRegistrationOptions(TextDocumentRegistrationOptions, DiagnosticOptions):
    """Diagnostic registration options.

    @since 3.17.0"""
    # since 3.17.0
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class PreviousResultId:
    """A previous result id in a workspace pull request.

    @since 3.17.0"""
    # since 3.17.0
    uri: DocumentUri
    """The URI for which the client knowns a
    result id."""
    value: str
    """The value of the previous result id."""

@dataclass
class WorkspaceDiagnosticParams:
    """Parameters of the workspace diagnostic request.

    @since 3.17.0"""
    # since 3.17.0
    identifier: str = field(metadata={"optional": True})
    """The additional identifier provided during registration."""
    previousResultIds: List[PreviousResultId]
    """The currently known diagnostic reports with their
    previous result ids."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class WorkspaceFullDocumentDiagnosticReport(FullDocumentDiagnosticReport):
    """A full document diagnostic report for a workspace diagnostic result.

    @since 3.17.0"""
    # since 3.17.0
    uri: DocumentUri
    """The URI for which diagnostic information is reported."""
    version: Union[int, None]
    """The version number for which the diagnostics are reported.
    If the document is not marked as open `null` can be provided."""

@dataclass
class WorkspaceUnchangedDocumentDiagnosticReport(UnchangedDocumentDiagnosticReport):
    """An unchanged document diagnostic report for a workspace diagnostic result.

    @since 3.17.0"""
    # since 3.17.0
    uri: DocumentUri
    """The URI for which diagnostic information is reported."""
    version: Union[int, None]
    """The version number for which the diagnostics are reported.
    If the document is not marked as open `null` can be provided."""

WorkspaceDocumentDiagnosticReport: TypeAlias = Union[WorkspaceFullDocumentDiagnosticReport, WorkspaceUnchangedDocumentDiagnosticReport]
"""A workspace diagnostic document report.

@since 3.17.0"""
# since 3.17.0

@dataclass
class WorkspaceDiagnosticReport:
    """A workspace diagnostic report.

    @since 3.17.0"""
    # since 3.17.0
    items: List[WorkspaceDocumentDiagnosticReport]

@dataclass
class WorkspaceDiagnosticReportPartialResult:
    """A partial result for a workspace diagnostic report.

    @since 3.17.0"""
    # since 3.17.0
    items: List[WorkspaceDocumentDiagnosticReport]

LSPObject: TypeAlias = Dict[str, Any]
"""LSP object definition.
@since 3.17.0"""
# since 3.17.0

@dataclass
class ExecutionSummary:
    executionOrder: int
    """A strict monotonically increasing value
    indicating the execution order of a cell
    inside a notebook."""
    success: bool = field(metadata={"optional": True})
    """Whether the execution was successful or
    not if known by the client."""

@dataclass
class NotebookCell:
    """A notebook cell.

    A cell's document URI must be unique across ALL notebook
    cells and can therefore be used to uniquely identify a
    notebook cell or the cell's text document.

    @since 3.17.0"""
    # since 3.17.0
    kind: NotebookCellKind
    """The cell's kind"""
    document: DocumentUri
    """The URI of the cell's text document
    content."""
    metadata: LSPObject = field(metadata={"optional": True})
    """Additional metadata stored with the cell.

    Note: should always be an object literal (e.g. LSPObject)"""
    executionSummary: ExecutionSummary = field(metadata={"optional": True})
    """Additional execution summary information
    if supported by the client."""

@dataclass
class NotebookDocument:
    """A notebook document.

    @since 3.17.0"""
    # since 3.17.0
    uri: URI
    """The notebook document's uri."""
    notebookType: str
    """The type of the notebook."""
    version: int
    """The version number of this document (it will increase after each
    change, including undo/redo)."""
    metadata: LSPObject = field(metadata={"optional": True})
    """Additional metadata stored with the notebook
    document.

    Note: should always be an object literal (e.g. LSPObject)"""
    cells: List[NotebookCell]
    """The cells of a notebook."""

@dataclass
class TextDocumentItem:
    """An item to transfer a text document from the client to the
    server."""
    uri: DocumentUri
    """The text document's uri."""
    languageId: LanguageKind
    """The text document's language identifier."""
    version: int
    """The version number of this document (it will increase after each
    change, including undo/redo)."""
    text: str
    """The content of the opened text document."""

@dataclass
class DidOpenNotebookDocumentParams:
    """The params sent in an open notebook document notification.

    @since 3.17.0"""
    # since 3.17.0
    notebookDocument: NotebookDocument
    """The notebook document that got opened."""
    cellTextDocuments: List[TextDocumentItem]
    """The text documents that represent the content
    of a notebook cell."""

@dataclass
class NotebookCellLanguage:
    """@since 3.18.0"""
    # since 3.18.0
    language: str

@dataclass
class NotebookDocumentFilterWithNotebook:
    """@since 3.18.0"""
    # since 3.18.0
    notebook: Union[str, NotebookDocumentFilter]
    """The notebook to be synced If a string
    value is provided it matches against the
    notebook type. '*' matches every notebook."""
    cells: List[NotebookCellLanguage] = field(metadata={"optional": True})
    """The cells of the matching notebook to be synced."""

@dataclass
class NotebookDocumentFilterWithCells:
    """@since 3.18.0"""
    # since 3.18.0
    notebook: Union[str, NotebookDocumentFilter] = field(metadata={"optional": True})
    """The notebook to be synced If a string
    value is provided it matches against the
    notebook type. '*' matches every notebook."""
    cells: List[NotebookCellLanguage]
    """The cells of the matching notebook to be synced."""

@dataclass
class NotebookDocumentSyncOptions:
    """Options specific to a notebook plus its cells
    to be synced to the server.

    If a selector provides a notebook document
    filter but no cell selector all cells of a
    matching notebook document will be synced.

    If a selector provides no notebook document
    filter but only a cell selector all notebook
    document that contain at least one matching
    cell will be synced.

    @since 3.17.0"""
    # since 3.17.0
    notebookSelector: List[Union[NotebookDocumentFilterWithNotebook, NotebookDocumentFilterWithCells]]
    """The notebooks to be synced"""
    save: bool = field(metadata={"optional": True})
    """Whether save notification should be forwarded to
    the server. Will only be honored if mode === `notebook`."""

@dataclass
class NotebookDocumentSyncRegistrationOptions(NotebookDocumentSyncOptions):
    """Registration options specific to a notebook.

    @since 3.17.0"""
    # since 3.17.0
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class VersionedNotebookDocumentIdentifier:
    """A versioned notebook document identifier.

    @since 3.17.0"""
    # since 3.17.0
    version: int
    """The version number of this notebook document."""
    uri: URI
    """The notebook document's uri."""

@dataclass
class NotebookCellArrayChange:
    """A change describing how to move a `NotebookCell`
    array from state S to S'.

    @since 3.17.0"""
    # since 3.17.0
    start: int
    """The start oftest of the cell that changed."""
    deleteCount: int
    """The deleted cells"""
    cells: List[NotebookCell] = field(metadata={"optional": True})
    """The new cells, if any"""

@dataclass
class NotebookDocumentCellChangeStructure:
    """Structural changes to cells in a notebook document.

    @since 3.18.0"""
    # since 3.18.0
    array: NotebookCellArrayChange
    """The change to the cell array."""
    didOpen: List[TextDocumentItem] = field(metadata={"optional": True})
    """Additional opened cell text documents."""
    didClose: List[TextDocumentIdentifier] = field(metadata={"optional": True})
    """Additional closed cell text documents."""

@dataclass
class VersionedTextDocumentIdentifier(TextDocumentIdentifier):
    """A text document identifier to denote a specific version of a text document."""
    version: int
    """The version number of this document."""

@dataclass
class TextDocumentContentChangePartial:
    """@since 3.18.0"""
    # since 3.18.0
    range: Range
    """The range of the document that changed."""
    rangeLength: int = field(metadata={"optional": True})
    """The optional length of the range that got replaced.

    @deprecated use range instead."""
    text: str
    """The new text for the provided range."""

@dataclass
class TextDocumentContentChangeWholeDocument:
    """@since 3.18.0"""
    # since 3.18.0
    text: str
    """The new text of the whole document."""

TextDocumentContentChangeEvent: TypeAlias = Union[TextDocumentContentChangePartial, TextDocumentContentChangeWholeDocument]
"""An event describing a change to a text document. If only a text is provided
it is considered to be the full content of the document."""

@dataclass
class NotebookDocumentCellContentChanges:
    """Content changes to a cell in a notebook document.

    @since 3.18.0"""
    # since 3.18.0
    document: VersionedTextDocumentIdentifier
    changes: List[TextDocumentContentChangeEvent]

@dataclass
class NotebookDocumentCellChanges:
    """Cell changes to a notebook document.

    @since 3.18.0"""
    # since 3.18.0
    structure: NotebookDocumentCellChangeStructure = field(metadata={"optional": True})
    """Changes to the cell structure to add or
    remove cells."""
    data: List[NotebookCell] = field(metadata={"optional": True})
    """Changes to notebook cells properties like its
    kind, execution summary or metadata."""
    textContent: List[NotebookDocumentCellContentChanges] = field(metadata={"optional": True})
    """Changes to the text content of notebook cells."""

@dataclass
class NotebookDocumentChangeEvent:
    """A change event for a notebook document.

    @since 3.17.0"""
    # since 3.17.0
    metadata: LSPObject = field(metadata={"optional": True})
    """The changed meta data if any.

    Note: should always be an object literal (e.g. LSPObject)"""
    cells: NotebookDocumentCellChanges = field(metadata={"optional": True})
    """Changes to cells"""

@dataclass
class DidChangeNotebookDocumentParams:
    """The params sent in a change notebook document notification.

    @since 3.17.0"""
    # since 3.17.0
    notebookDocument: VersionedNotebookDocumentIdentifier
    """The notebook document that did change. The version number points
    to the version after all provided changes have been applied. If
    only the text document content of a cell changes the notebook version
    doesn't necessarily have to change."""
    change: NotebookDocumentChangeEvent
    """The actual changes to the notebook document.

    The changes describe single state changes to the notebook document.
    So if there are two changes c1 (at array index 0) and c2 (at array
    index 1) for a notebook in state S then c1 moves the notebook from
    S to S' and c2 from S' to S''. So c1 is computed on the state S and
    c2 is computed on the state S'.

    To mirror the content of a notebook using change events use the following approach:
    - start with the same initial content
    - apply the 'notebookDocument/didChange' notifications in the order you receive them.
    - apply the `NotebookChangeEvent`s in a single notification in the order
      you receive them."""

@dataclass
class NotebookDocumentIdentifier:
    """A literal to identify a notebook document in the client.

    @since 3.17.0"""
    # since 3.17.0
    uri: URI
    """The notebook document's uri."""

@dataclass
class DidSaveNotebookDocumentParams:
    """The params sent in a save notebook document notification.

    @since 3.17.0"""
    # since 3.17.0
    notebookDocument: NotebookDocumentIdentifier
    """The notebook document that got saved."""

@dataclass
class DidCloseNotebookDocumentParams:
    """The params sent in a close notebook document notification.

    @since 3.17.0"""
    # since 3.17.0
    notebookDocument: NotebookDocumentIdentifier
    """The notebook document that got closed."""
    cellTextDocuments: List[TextDocumentIdentifier]
    """The text documents that represent the content
    of a notebook cell that got closed."""

@dataclass
class SelectedCompletionInfo:
    """Describes the currently selected completion item.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    range: Range
    """The range that will be replaced if this completion item is accepted."""
    text: str
    """The text the range will be replaced with if this completion is accepted."""

@dataclass
class InlineCompletionContext:
    """Provides information about the context in which an inline completion was requested.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    triggerKind: InlineCompletionTriggerKind
    """Describes how the inline completion was triggered."""
    selectedCompletionInfo: SelectedCompletionInfo = field(metadata={"optional": True})
    """Provides information about the currently selected item in the autocomplete widget if it is visible."""

@dataclass
class InlineCompletionParams(TextDocumentPositionParams):
    """A parameter literal used in inline completion requests.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    context: InlineCompletionContext
    """Additional information about the context in which inline completions were
    requested."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class InlineCompletionItem:
    """An inline completion item represents a text snippet that is proposed inline to complete text that is being typed.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    insertText: Union[str, StringValue]
    """The text to replace the range with. Must be set."""
    filterText: str = field(metadata={"optional": True})
    """A text that is used to decide if this inline completion should be shown. When `falsy` the {@link InlineCompletionItem.insertText} is used."""
    range: Range = field(metadata={"optional": True})
    """The range to replace. Must begin and end on the same line."""
    command: Command = field(metadata={"optional": True})
    """An optional {@link Command} that is executed *after* inserting this completion."""

@dataclass
class InlineCompletionList:
    """Represents a collection of {@link InlineCompletionItem inline completion items} to be presented in the editor.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    items: List[InlineCompletionItem]
    """The inline completion items"""

@dataclass
class InlineCompletionOptions:
    """Inline completion options used during static registration.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class InlineCompletionRegistrationOptions(InlineCompletionOptions, TextDocumentRegistrationOptions):
    """Inline completion options used during static or dynamic registration.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class TextDocumentContentParams:
    """Parameters for the `workspace/textDocumentContent` request.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    uri: DocumentUri
    """The uri of the text document."""

@dataclass
class TextDocumentContentResult:
    """Result of the `workspace/textDocumentContent` request.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    text: str
    """The text content of the text document. Please note, that the content of
    any subsequent open notifications for the text document might differ
    from the returned content due to whitespace and line ending
    normalizations done on the client"""

@dataclass
class TextDocumentContentOptions:
    """Text document content provider options.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    schemes: List[str]
    """The schemes for which the server provides content."""

@dataclass
class TextDocumentContentRegistrationOptions(TextDocumentContentOptions):
    """Text document content provider registration options.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class TextDocumentContentRefreshParams:
    """Parameters for the `workspace/textDocumentContent/refresh` request.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    uri: DocumentUri
    """The uri of the text document to refresh."""

@dataclass
class Registration:
    """General parameters to register for a notification or to register a provider."""
    id: str
    """The id used to register the request. The id can be used to deregister
    the request again."""
    method: str
    """The method / capability to register for."""
    registerOptions: Any = field(metadata={"optional": True})
    """Options necessary for the registration."""

@dataclass
class RegistrationParams:
    registrations: List[Registration]

@dataclass
class Unregistration:
    """General parameters to unregister a request or notification."""
    id: str
    """The id used to unregister the request or notification. Usually an id
    provided during the register request."""
    method: str
    """The method to unregister for."""

@dataclass
class UnregistrationParams:
    unregisterations: List[Unregistration]

@dataclass
class ClientInfo:
    """Information about the client

    @since 3.15.0
    @since 3.18.0 ClientInfo type name added."""
    # since 3.18.0 ClientInfo type name added.
    name: str
    """The name of the client as defined by the client."""
    version: str = field(metadata={"optional": True})
    """The client's version as defined by the client."""

@dataclass
class ChangeAnnotationsSupportOptions:
    """@since 3.18.0"""
    # since 3.18.0
    groupsOnLabel: bool = field(metadata={"optional": True})
    """Whether the client groups edits with equal labels into tree nodes,
    for instance all edits labelled with "Changes in Strings" would
    be a tree node."""

@dataclass
class WorkspaceEditClientCapabilities:
    documentChanges: bool = field(metadata={"optional": True})
    """The client supports versioned document changes in `WorkspaceEdit`s"""
    resourceOperations: List[ResourceOperationKind] = field(metadata={"optional": True})
    """The resource operations the client supports. Clients should at least
    support 'create', 'rename' and 'delete' files and folders.

    @since 3.13.0"""
    # since 3.13.0
    failureHandling: FailureHandlingKind = field(metadata={"optional": True})
    """The failure handling strategy of a client if applying the workspace edit
    fails.

    @since 3.13.0"""
    # since 3.13.0
    normalizesLineEndings: bool = field(metadata={"optional": True})
    """Whether the client normalizes line endings to the client specific
    setting.
    If set to `true` the client will normalize line ending characters
    in a workspace edit to the client-specified new line
    character.

    @since 3.16.0"""
    # since 3.16.0
    changeAnnotationSupport: ChangeAnnotationsSupportOptions = field(metadata={"optional": True})
    """Whether the client in general supports change annotations on text edits,
    create file, rename file and delete file changes.

    @since 3.16.0"""
    # since 3.16.0
    metadataSupport: bool = field(metadata={"optional": True})
    """Whether the client supports `WorkspaceEditMetadata` in `WorkspaceEdit`s.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    snippetEditSupport: bool = field(metadata={"optional": True})
    """Whether the client supports snippets as text edits.

    @since 3.18.0
    @proposed"""
    # since 3.18.0

@dataclass
class DidChangeConfigurationClientCapabilities:
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Did change configuration notification supports dynamic registration."""

@dataclass
class DidChangeWatchedFilesClientCapabilities:
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Did change watched files notification supports dynamic registration. Please note
    that the current protocol doesn't support static configuration for file changes
    from the server side."""
    relativePatternSupport: bool = field(metadata={"optional": True})
    """Whether the client has support for {@link  RelativePattern relative pattern}
    or not.

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class ClientSymbolKindOptions:
    """@since 3.18.0"""
    # since 3.18.0
    valueSet: List[SymbolKind] = field(metadata={"optional": True})
    """The symbol kind values the client supports. When this
    property exists the client also guarantees that it will
    handle values outside its set gracefully and falls back
    to a default value when unknown.

    If this property is not present the client only supports
    the symbol kinds from `File` to `Array` as defined in
    the initial version of the protocol."""

@dataclass
class ClientSymbolTagOptions:
    """@since 3.18.0"""
    # since 3.18.0
    valueSet: List[SymbolTag]
    """The tags supported by the client."""

@dataclass
class ClientSymbolResolveOptions:
    """@since 3.18.0"""
    # since 3.18.0
    properties: List[str]
    """The properties that a client can resolve lazily. Usually
    `location.range`"""

@dataclass
class WorkspaceSymbolClientCapabilities:
    """Client capabilities for a {@link WorkspaceSymbolRequest}."""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Symbol request supports dynamic registration."""
    symbolKind: ClientSymbolKindOptions = field(metadata={"optional": True})
    """Specific capabilities for the `SymbolKind` in the `workspace/symbol` request."""
    tagSupport: ClientSymbolTagOptions = field(metadata={"optional": True})
    """The client supports tags on `SymbolInformation`.
    Clients supporting tags have to handle unknown tags gracefully.

    @since 3.16.0"""
    # since 3.16.0
    resolveSupport: ClientSymbolResolveOptions = field(metadata={"optional": True})
    """The client support partial workspace symbols. The client will send the
    request `workspaceSymbol/resolve` to the server to resolve additional
    properties.

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class ExecuteCommandClientCapabilities:
    """The client capabilities of a {@link ExecuteCommandRequest}."""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Execute command supports dynamic registration."""

@dataclass
class SemanticTokensWorkspaceClientCapabilities:
    """@since 3.16.0"""
    # since 3.16.0
    refreshSupport: bool = field(metadata={"optional": True})
    """Whether the client implementation supports a refresh request sent from
    the server to the client.

    Note that this event is global and will force the client to refresh all
    semantic tokens currently shown. It should be used with absolute care
    and is useful for situation where a server for example detects a project
    wide change that requires such a calculation."""

@dataclass
class CodeLensWorkspaceClientCapabilities:
    """@since 3.16.0"""
    # since 3.16.0
    refreshSupport: bool = field(metadata={"optional": True})
    """Whether the client implementation supports a refresh request sent from the
    server to the client.

    Note that this event is global and will force the client to refresh all
    code lenses currently shown. It should be used with absolute care and is
    useful for situation where a server for example detect a project wide
    change that requires such a calculation."""

@dataclass
class FileOperationClientCapabilities:
    """Capabilities relating to events from file operations by the user in the client.

    These events do not come from the file system, they come from user operations
    like renaming a file in the UI.

    @since 3.16.0"""
    # since 3.16.0
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether the client supports dynamic registration for file requests/notifications."""
    didCreate: bool = field(metadata={"optional": True})
    """The client has support for sending didCreateFiles notifications."""
    willCreate: bool = field(metadata={"optional": True})
    """The client has support for sending willCreateFiles requests."""
    didRename: bool = field(metadata={"optional": True})
    """The client has support for sending didRenameFiles notifications."""
    willRename: bool = field(metadata={"optional": True})
    """The client has support for sending willRenameFiles requests."""
    didDelete: bool = field(metadata={"optional": True})
    """The client has support for sending didDeleteFiles notifications."""
    willDelete: bool = field(metadata={"optional": True})
    """The client has support for sending willDeleteFiles requests."""

@dataclass
class InlineValueWorkspaceClientCapabilities:
    """Client workspace capabilities specific to inline values.

    @since 3.17.0"""
    # since 3.17.0
    refreshSupport: bool = field(metadata={"optional": True})
    """Whether the client implementation supports a refresh request sent from the
    server to the client.

    Note that this event is global and will force the client to refresh all
    inline values currently shown. It should be used with absolute care and is
    useful for situation where a server for example detects a project wide
    change that requires such a calculation."""

@dataclass
class InlayHintWorkspaceClientCapabilities:
    """Client workspace capabilities specific to inlay hints.

    @since 3.17.0"""
    # since 3.17.0
    refreshSupport: bool = field(metadata={"optional": True})
    """Whether the client implementation supports a refresh request sent from
    the server to the client.

    Note that this event is global and will force the client to refresh all
    inlay hints currently shown. It should be used with absolute care and
    is useful for situation where a server for example detects a project wide
    change that requires such a calculation."""

@dataclass
class DiagnosticWorkspaceClientCapabilities:
    """Workspace client capabilities specific to diagnostic pull requests.

    @since 3.17.0"""
    # since 3.17.0
    refreshSupport: bool = field(metadata={"optional": True})
    """Whether the client implementation supports a refresh request sent from
    the server to the client.

    Note that this event is global and will force the client to refresh all
    pulled diagnostics currently shown. It should be used with absolute care and
    is useful for situation where a server for example detects a project wide
    change that requires such a calculation."""

@dataclass
class FoldingRangeWorkspaceClientCapabilities:
    """Client workspace capabilities specific to folding ranges

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    refreshSupport: bool = field(metadata={"optional": True})
    """Whether the client implementation supports a refresh request sent from the
    server to the client.

    Note that this event is global and will force the client to refresh all
    folding ranges currently shown. It should be used with absolute care and is
    useful for situation where a server for example detects a project wide
    change that requires such a calculation.

    @since 3.18.0
    @proposed"""
    # since 3.18.0

@dataclass
class TextDocumentContentClientCapabilities:
    """Client capabilities for a text document content provider.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Text document content provider supports dynamic registration."""

@dataclass
class WorkspaceClientCapabilities:
    """Workspace specific client capabilities."""
    applyEdit: bool = field(metadata={"optional": True})
    """The client supports applying batch edits
    to the workspace by supporting the request
    'workspace/applyEdit'"""
    workspaceEdit: WorkspaceEditClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to `WorkspaceEdit`s."""
    didChangeConfiguration: DidChangeConfigurationClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `workspace/didChangeConfiguration` notification."""
    didChangeWatchedFiles: DidChangeWatchedFilesClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `workspace/didChangeWatchedFiles` notification."""
    symbol: WorkspaceSymbolClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `workspace/symbol` request."""
    executeCommand: ExecuteCommandClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `workspace/executeCommand` request."""
    workspaceFolders: bool = field(metadata={"optional": True})
    """The client has support for workspace folders.

    @since 3.6.0"""
    # since 3.6.0
    configuration: bool = field(metadata={"optional": True})
    """The client supports `workspace/configuration` requests.

    @since 3.6.0"""
    # since 3.6.0
    semanticTokens: SemanticTokensWorkspaceClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the semantic token requests scoped to the
    workspace.

    @since 3.16.0."""
    # since 3.16.0.
    codeLens: CodeLensWorkspaceClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the code lens requests scoped to the
    workspace.

    @since 3.16.0."""
    # since 3.16.0.
    fileOperations: FileOperationClientCapabilities = field(metadata={"optional": True})
    """The client has support for file notifications/requests for user operations on files.

    Since 3.16.0"""
    inlineValue: InlineValueWorkspaceClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the inline values requests scoped to the
    workspace.

    @since 3.17.0."""
    # since 3.17.0.
    inlayHint: InlayHintWorkspaceClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the inlay hint requests scoped to the
    workspace.

    @since 3.17.0."""
    # since 3.17.0.
    diagnostics: DiagnosticWorkspaceClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the diagnostic requests scoped to the
    workspace.

    @since 3.17.0."""
    # since 3.17.0.
    foldingRange: FoldingRangeWorkspaceClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the folding range requests scoped to the workspace.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    textDocumentContent: TextDocumentContentClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `workspace/textDocumentContent` request.

    @since 3.18.0
    @proposed"""
    # since 3.18.0

@dataclass
class TextDocumentSyncClientCapabilities:
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether text document synchronization supports dynamic registration."""
    willSave: bool = field(metadata={"optional": True})
    """The client supports sending will save notifications."""
    willSaveWaitUntil: bool = field(metadata={"optional": True})
    """The client supports sending a will save request and
    waits for a response providing text edits which will
    be applied to the document before it is saved."""
    didSave: bool = field(metadata={"optional": True})
    """The client supports did save notifications."""

@dataclass
class TextDocumentFilterClientCapabilities:
    relativePatternSupport: bool = field(metadata={"optional": True})
    """The client supports Relative Patterns.

    @since 3.18.0"""
    # since 3.18.0

@dataclass
class CompletionItemTagOptions:
    """@since 3.18.0"""
    # since 3.18.0
    valueSet: List[CompletionItemTag]
    """The tags supported by the client."""

@dataclass
class ClientCompletionItemResolveOptions:
    """@since 3.18.0"""
    # since 3.18.0
    properties: List[str]
    """The properties that a client can resolve lazily."""

@dataclass
class ClientCompletionItemInsertTextModeOptions:
    """@since 3.18.0"""
    # since 3.18.0
    valueSet: List[InsertTextMode]

@dataclass
class ClientCompletionItemOptions:
    """@since 3.18.0"""
    # since 3.18.0
    snippetSupport: bool = field(metadata={"optional": True})
    """Client supports snippets as insert text.

    A snippet can define tab stops and placeholders with `$1`, `$2`
    and `${3:foo}`. `$0` defines the final tab stop, it defaults to
    the end of the snippet. Placeholders with equal identifiers are linked,
    that is typing in one will update others too."""
    commitCharactersSupport: bool = field(metadata={"optional": True})
    """Client supports commit characters on a completion item."""
    documentationFormat: List[MarkupKind] = field(metadata={"optional": True})
    """Client supports the following content formats for the documentation
    property. The order describes the preferred format of the client."""
    deprecatedSupport: bool = field(metadata={"optional": True})
    """Client supports the deprecated property on a completion item."""
    preselectSupport: bool = field(metadata={"optional": True})
    """Client supports the preselect property on a completion item."""
    tagSupport: CompletionItemTagOptions = field(metadata={"optional": True})
    """Client supports the tag property on a completion item. Clients supporting
    tags have to handle unknown tags gracefully. Clients especially need to
    preserve unknown tags when sending a completion item back to the server in
    a resolve call.

    @since 3.15.0"""
    # since 3.15.0
    insertReplaceSupport: bool = field(metadata={"optional": True})
    """Client support insert replace edit to control different behavior if a
    completion item is inserted in the text or should replace text.

    @since 3.16.0"""
    # since 3.16.0
    resolveSupport: ClientCompletionItemResolveOptions = field(metadata={"optional": True})
    """Indicates which properties a client can resolve lazily on a completion
    item. Before version 3.16.0 only the predefined properties `documentation`
    and `details` could be resolved lazily.

    @since 3.16.0"""
    # since 3.16.0
    insertTextModeSupport: ClientCompletionItemInsertTextModeOptions = field(metadata={"optional": True})
    """The client supports the `insertTextMode` property on
    a completion item to override the whitespace handling mode
    as defined by the client (see `insertTextMode`).

    @since 3.16.0"""
    # since 3.16.0
    labelDetailsSupport: bool = field(metadata={"optional": True})
    """The client has support for completion item label
    details (see also `CompletionItemLabelDetails`).

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class ClientCompletionItemOptionsKind:
    """@since 3.18.0"""
    # since 3.18.0
    valueSet: List[CompletionItemKind] = field(metadata={"optional": True})
    """The completion item kind values the client supports. When this
    property exists the client also guarantees that it will
    handle values outside its set gracefully and falls back
    to a default value when unknown.

    If this property is not present the client only supports
    the completion items kinds from `Text` to `Reference` as defined in
    the initial version of the protocol."""

@dataclass
class CompletionListCapabilities:
    """The client supports the following `CompletionList` specific
    capabilities.

    @since 3.17.0"""
    # since 3.17.0
    itemDefaults: List[str] = field(metadata={"optional": True})
    """The client supports the following itemDefaults on
    a completion list.

    The value lists the supported property names of the
    `CompletionList.itemDefaults` object. If omitted
    no properties are supported.

    @since 3.17.0"""
    # since 3.17.0
    applyKindSupport: bool = field(metadata={"optional": True})
    """Specifies whether the client supports `CompletionList.applyKind` to
    indicate how supported values from `completionList.itemDefaults`
    and `completion` will be combined.

    If a client supports `applyKind` it must support it for all fields
    that it supports that are listed in `CompletionList.applyKind`. This
    means when clients add support for new/future fields in completion
    items the MUST also support merge for them if those fields are
    defined in `CompletionList.applyKind`.

    @since 3.18.0"""
    # since 3.18.0

@dataclass
class CompletionClientCapabilities:
    """Completion client capabilities"""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether completion supports dynamic registration."""
    completionItem: ClientCompletionItemOptions = field(metadata={"optional": True})
    """The client supports the following `CompletionItem` specific
    capabilities."""
    completionItemKind: ClientCompletionItemOptionsKind = field(metadata={"optional": True})
    insertTextMode: InsertTextMode = field(metadata={"optional": True})
    """Defines how the client handles whitespace and indentation
    when accepting a completion item that uses multi line
    text in either `insertText` or `textEdit`.

    @since 3.17.0"""
    # since 3.17.0
    contextSupport: bool = field(metadata={"optional": True})
    """The client supports to send additional context information for a
    `textDocument/completion` request."""
    completionList: CompletionListCapabilities = field(metadata={"optional": True})
    """The client supports the following `CompletionList` specific
    capabilities.

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class HoverClientCapabilities:
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether hover supports dynamic registration."""
    contentFormat: List[MarkupKind] = field(metadata={"optional": True})
    """Client supports the following content formats for the content
    property. The order describes the preferred format of the client."""

@dataclass
class ClientSignatureParameterInformationOptions:
    """@since 3.18.0"""
    # since 3.18.0
    labelOffsetSupport: bool = field(metadata={"optional": True})
    """The client supports processing label offsets instead of a
    simple label string.

    @since 3.14.0"""
    # since 3.14.0

@dataclass
class ClientSignatureInformationOptions:
    """@since 3.18.0"""
    # since 3.18.0
    documentationFormat: List[MarkupKind] = field(metadata={"optional": True})
    """Client supports the following content formats for the documentation
    property. The order describes the preferred format of the client."""
    parameterInformation: ClientSignatureParameterInformationOptions = field(metadata={"optional": True})
    """Client capabilities specific to parameter information."""
    activeParameterSupport: bool = field(metadata={"optional": True})
    """The client supports the `activeParameter` property on `SignatureInformation`
    literal.

    @since 3.16.0"""
    # since 3.16.0
    noActiveParameterSupport: bool = field(metadata={"optional": True})
    """The client supports the `activeParameter` property on
    `SignatureHelp`/`SignatureInformation` being set to `null` to
    indicate that no parameter should be active.

    @since 3.18.0
    @proposed"""
    # since 3.18.0

@dataclass
class SignatureHelpClientCapabilities:
    """Client Capabilities for a {@link SignatureHelpRequest}."""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether signature help supports dynamic registration."""
    signatureInformation: ClientSignatureInformationOptions = field(metadata={"optional": True})
    """The client supports the following `SignatureInformation`
    specific properties."""
    contextSupport: bool = field(metadata={"optional": True})
    """The client supports to send additional context information for a
    `textDocument/signatureHelp` request. A client that opts into
    contextSupport will also support the `retriggerCharacters` on
    `SignatureHelpOptions`.

    @since 3.15.0"""
    # since 3.15.0

@dataclass
class DeclarationClientCapabilities:
    """@since 3.14.0"""
    # since 3.14.0
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether declaration supports dynamic registration. If this is set to `true`
    the client supports the new `DeclarationRegistrationOptions` return value
    for the corresponding server capability as well."""
    linkSupport: bool = field(metadata={"optional": True})
    """The client supports additional metadata in the form of declaration links."""

@dataclass
class DefinitionClientCapabilities:
    """Client Capabilities for a {@link DefinitionRequest}."""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether definition supports dynamic registration."""
    linkSupport: bool = field(metadata={"optional": True})
    """The client supports additional metadata in the form of definition links.

    @since 3.14.0"""
    # since 3.14.0

@dataclass
class TypeDefinitionClientCapabilities:
    """Since 3.6.0"""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether implementation supports dynamic registration. If this is set to `true`
    the client supports the new `TypeDefinitionRegistrationOptions` return value
    for the corresponding server capability as well."""
    linkSupport: bool = field(metadata={"optional": True})
    """The client supports additional metadata in the form of definition links.

    Since 3.14.0"""

@dataclass
class ImplementationClientCapabilities:
    """@since 3.6.0"""
    # since 3.6.0
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether implementation supports dynamic registration. If this is set to `true`
    the client supports the new `ImplementationRegistrationOptions` return value
    for the corresponding server capability as well."""
    linkSupport: bool = field(metadata={"optional": True})
    """The client supports additional metadata in the form of definition links.

    @since 3.14.0"""
    # since 3.14.0

@dataclass
class ReferenceClientCapabilities:
    """Client Capabilities for a {@link ReferencesRequest}."""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether references supports dynamic registration."""

@dataclass
class DocumentHighlightClientCapabilities:
    """Client Capabilities for a {@link DocumentHighlightRequest}."""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether document highlight supports dynamic registration."""

@dataclass
class DocumentSymbolClientCapabilities:
    """Client Capabilities for a {@link DocumentSymbolRequest}."""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether document symbol supports dynamic registration."""
    symbolKind: ClientSymbolKindOptions = field(metadata={"optional": True})
    """Specific capabilities for the `SymbolKind` in the
    `textDocument/documentSymbol` request."""
    hierarchicalDocumentSymbolSupport: bool = field(metadata={"optional": True})
    """The client supports hierarchical document symbols."""
    tagSupport: ClientSymbolTagOptions = field(metadata={"optional": True})
    """The client supports tags on `SymbolInformation`. Tags are supported on
    `DocumentSymbol` if `hierarchicalDocumentSymbolSupport` is set to true.
    Clients supporting tags have to handle unknown tags gracefully.

    @since 3.16.0"""
    # since 3.16.0
    labelSupport: bool = field(metadata={"optional": True})
    """The client supports an additional label presented in the UI when
    registering a document symbol provider.

    @since 3.16.0"""
    # since 3.16.0

@dataclass
class ClientCodeActionKindOptions:
    """@since 3.18.0"""
    # since 3.18.0
    valueSet: List[CodeActionKind]
    """The code action kind values the client supports. When this
    property exists the client also guarantees that it will
    handle values outside its set gracefully and falls back
    to a default value when unknown."""

@dataclass
class ClientCodeActionLiteralOptions:
    """@since 3.18.0"""
    # since 3.18.0
    codeActionKind: ClientCodeActionKindOptions
    """The code action kind is support with the following value
    set."""

@dataclass
class ClientCodeActionResolveOptions:
    """@since 3.18.0"""
    # since 3.18.0
    properties: List[str]
    """The properties that a client can resolve lazily."""

@dataclass
class CodeActionTagOptions:
    """@since 3.18.0 - proposed"""
    # since 3.18.0 - proposed
    valueSet: List[CodeActionTag]
    """The tags supported by the client."""

@dataclass
class CodeActionClientCapabilities:
    """The Client Capabilities of a {@link CodeActionRequest}."""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether code action supports dynamic registration."""
    codeActionLiteralSupport: ClientCodeActionLiteralOptions = field(metadata={"optional": True})
    """The client support code action literals of type `CodeAction` as a valid
    response of the `textDocument/codeAction` request. If the property is not
    set the request can only return `Command` literals.

    @since 3.8.0"""
    # since 3.8.0
    isPreferredSupport: bool = field(metadata={"optional": True})
    """Whether code action supports the `isPreferred` property.

    @since 3.15.0"""
    # since 3.15.0
    disabledSupport: bool = field(metadata={"optional": True})
    """Whether code action supports the `disabled` property.

    @since 3.16.0"""
    # since 3.16.0
    dataSupport: bool = field(metadata={"optional": True})
    """Whether code action supports the `data` property which is
    preserved between a `textDocument/codeAction` and a
    `codeAction/resolve` request.

    @since 3.16.0"""
    # since 3.16.0
    resolveSupport: ClientCodeActionResolveOptions = field(metadata={"optional": True})
    """Whether the client supports resolving additional code action
    properties via a separate `codeAction/resolve` request.

    @since 3.16.0"""
    # since 3.16.0
    honorsChangeAnnotations: bool = field(metadata={"optional": True})
    """Whether the client honors the change annotations in
    text edits and resource operations returned via the
    `CodeAction#edit` property by for example presenting
    the workspace edit in the user interface and asking
    for confirmation.

    @since 3.16.0"""
    # since 3.16.0
    documentationSupport: bool = field(metadata={"optional": True})
    """Whether the client supports documentation for a class of
    code actions.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    tagSupport: CodeActionTagOptions = field(metadata={"optional": True})
    """Client supports the tag property on a code action. Clients
    supporting tags have to handle unknown tags gracefully.

    @since 3.18.0 - proposed"""
    # since 3.18.0 - proposed

@dataclass
class ClientCodeLensResolveOptions:
    """@since 3.18.0"""
    # since 3.18.0
    properties: List[str]
    """The properties that a client can resolve lazily."""

@dataclass
class CodeLensClientCapabilities:
    """The client capabilities  of a {@link CodeLensRequest}."""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether code lens supports dynamic registration."""
    resolveSupport: ClientCodeLensResolveOptions = field(metadata={"optional": True})
    """Whether the client supports resolving additional code lens
    properties via a separate `codeLens/resolve` request.

    @since 3.18.0"""
    # since 3.18.0

@dataclass
class DocumentLinkClientCapabilities:
    """The client capabilities of a {@link DocumentLinkRequest}."""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether document link supports dynamic registration."""
    tooltipSupport: bool = field(metadata={"optional": True})
    """Whether the client supports the `tooltip` property on `DocumentLink`.

    @since 3.15.0"""
    # since 3.15.0

@dataclass
class DocumentColorClientCapabilities:
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether implementation supports dynamic registration. If this is set to `true`
    the client supports the new `DocumentColorRegistrationOptions` return value
    for the corresponding server capability as well."""

@dataclass
class DocumentFormattingClientCapabilities:
    """Client capabilities of a {@link DocumentFormattingRequest}."""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether formatting supports dynamic registration."""

@dataclass
class DocumentRangeFormattingClientCapabilities:
    """Client capabilities of a {@link DocumentRangeFormattingRequest}."""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether range formatting supports dynamic registration."""
    rangesSupport: bool = field(metadata={"optional": True})
    """Whether the client supports formatting multiple ranges at once.

    @since 3.18.0
    @proposed"""
    # since 3.18.0

@dataclass
class DocumentOnTypeFormattingClientCapabilities:
    """Client capabilities of a {@link DocumentOnTypeFormattingRequest}."""
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether on type formatting supports dynamic registration."""

@dataclass
class RenameClientCapabilities:
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether rename supports dynamic registration."""
    prepareSupport: bool = field(metadata={"optional": True})
    """Client supports testing for validity of rename operations
    before execution.

    @since 3.12.0"""
    # since 3.12.0
    prepareSupportDefaultBehavior: PrepareSupportDefaultBehavior = field(metadata={"optional": True})
    """Client supports the default behavior result.

    The value indicates the default behavior used by the
    client.

    @since 3.16.0"""
    # since 3.16.0
    honorsChangeAnnotations: bool = field(metadata={"optional": True})
    """Whether the client honors the change annotations in
    text edits and resource operations returned via the
    rename request's workspace edit by for example presenting
    the workspace edit in the user interface and asking
    for confirmation.

    @since 3.16.0"""
    # since 3.16.0

@dataclass
class ClientFoldingRangeKindOptions:
    """@since 3.18.0"""
    # since 3.18.0
    valueSet: List[FoldingRangeKind] = field(metadata={"optional": True})
    """The folding range kind values the client supports. When this
    property exists the client also guarantees that it will
    handle values outside its set gracefully and falls back
    to a default value when unknown."""

@dataclass
class ClientFoldingRangeOptions:
    """@since 3.18.0"""
    # since 3.18.0
    collapsedText: bool = field(metadata={"optional": True})
    """If set, the client signals that it supports setting collapsedText on
    folding ranges to display custom labels instead of the default text.

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class FoldingRangeClientCapabilities:
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether implementation supports dynamic registration for folding range
    providers. If this is set to `true` the client supports the new
    `FoldingRangeRegistrationOptions` return value for the corresponding
    server capability as well."""
    rangeLimit: int = field(metadata={"optional": True})
    """The maximum number of folding ranges that the client prefers to receive
    per document. The value serves as a hint, servers are free to follow the
    limit."""
    lineFoldingOnly: bool = field(metadata={"optional": True})
    """If set, the client signals that it only supports folding complete lines.
    If set, client will ignore specified `startCharacter` and `endCharacter`
    properties in a FoldingRange."""
    foldingRangeKind: ClientFoldingRangeKindOptions = field(metadata={"optional": True})
    """Specific options for the folding range kind.

    @since 3.17.0"""
    # since 3.17.0
    foldingRange: ClientFoldingRangeOptions = field(metadata={"optional": True})
    """Specific options for the folding range.

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class SelectionRangeClientCapabilities:
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether implementation supports dynamic registration for selection range providers. If this is set to `true`
    the client supports the new `SelectionRangeRegistrationOptions` return value for the corresponding server
    capability as well."""

@dataclass
class ClientDiagnosticsTagOptions:
    """@since 3.18.0"""
    # since 3.18.0
    valueSet: List[DiagnosticTag]
    """The tags supported by the client."""

@dataclass
class DiagnosticsCapabilities:
    """General diagnostics capabilities for pull and push model."""
    relatedInformation: bool = field(metadata={"optional": True})
    """Whether the clients accepts diagnostics with related information."""
    tagSupport: ClientDiagnosticsTagOptions = field(metadata={"optional": True})
    """Client supports the tag property to provide meta data about a diagnostic.
    Clients supporting tags have to handle unknown tags gracefully.

    @since 3.15.0"""
    # since 3.15.0
    codeDescriptionSupport: bool = field(metadata={"optional": True})
    """Client supports a codeDescription property

    @since 3.16.0"""
    # since 3.16.0
    dataSupport: bool = field(metadata={"optional": True})
    """Whether code action supports the `data` property which is
    preserved between a `textDocument/publishDiagnostics` and
    `textDocument/codeAction` request.

    @since 3.16.0"""
    # since 3.16.0

@dataclass
class PublishDiagnosticsClientCapabilities(DiagnosticsCapabilities):
    """The publish diagnostic client capabilities."""
    versionSupport: bool = field(metadata={"optional": True})
    """Whether the client interprets the version property of the
    `textDocument/publishDiagnostics` notification's parameter.

    @since 3.15.0"""
    # since 3.15.0

@dataclass
class CallHierarchyClientCapabilities:
    """@since 3.16.0"""
    # since 3.16.0
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether implementation supports dynamic registration. If this is set to `true`
    the client supports the new `(TextDocumentRegistrationOptions & StaticRegistrationOptions)`
    return value for the corresponding server capability as well."""

@dataclass
class ClientSemanticTokensRequestFullDelta:
    """@since 3.18.0"""
    # since 3.18.0
    delta: bool = field(metadata={"optional": True})
    """The client will send the `textDocument/semanticTokens/full/delta` request if
    the server provides a corresponding handler."""

@dataclass
class ClientSemanticTokensRequestOptions:
    """@since 3.18.0"""
    # since 3.18.0
    range: Union[bool, Literal[{'properties': []}]] = field(metadata={"optional": True})
    """The client will send the `textDocument/semanticTokens/range` request if
    the server provides a corresponding handler."""
    full: Union[bool, ClientSemanticTokensRequestFullDelta] = field(metadata={"optional": True})
    """The client will send the `textDocument/semanticTokens/full` request if
    the server provides a corresponding handler."""

@dataclass
class SemanticTokensClientCapabilities:
    """@since 3.16.0"""
    # since 3.16.0
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether implementation supports dynamic registration. If this is set to `true`
    the client supports the new `(TextDocumentRegistrationOptions & StaticRegistrationOptions)`
    return value for the corresponding server capability as well."""
    requests: ClientSemanticTokensRequestOptions
    """Which requests the client supports and might send to the server
    depending on the server's capability. Please note that clients might not
    show semantic tokens or degrade some of the user experience if a range
    or full request is advertised by the client but not provided by the
    server. If for example the client capability `requests.full` and
    `request.range` are both set to true but the server only provides a
    range provider the client might not render a minimap correctly or might
    even decide to not show any semantic tokens at all."""
    tokenTypes: List[str]
    """The token types that the client supports."""
    tokenModifiers: List[str]
    """The token modifiers that the client supports."""
    formats: List[TokenFormat]
    """The token formats the clients supports."""
    overlappingTokenSupport: bool = field(metadata={"optional": True})
    """Whether the client supports tokens that can overlap each other."""
    multilineTokenSupport: bool = field(metadata={"optional": True})
    """Whether the client supports tokens that can span multiple lines."""
    serverCancelSupport: bool = field(metadata={"optional": True})
    """Whether the client allows the server to actively cancel a
    semantic token request, e.g. supports returning
    LSPErrorCodes.ServerCancelled. If a server does the client
    needs to retrigger the request.

    @since 3.17.0"""
    # since 3.17.0
    augmentsSyntaxTokens: bool = field(metadata={"optional": True})
    """Whether the client uses semantic tokens to augment existing
    syntax tokens. If set to `true` client side created syntax
    tokens and semantic tokens are both used for colorization. If
    set to `false` the client only uses the returned semantic tokens
    for colorization.

    If the value is `undefined` then the client behavior is not
    specified.

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class LinkedEditingRangeClientCapabilities:
    """Client capabilities for the linked editing range request.

    @since 3.16.0"""
    # since 3.16.0
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether implementation supports dynamic registration. If this is set to `true`
    the client supports the new `(TextDocumentRegistrationOptions & StaticRegistrationOptions)`
    return value for the corresponding server capability as well."""

@dataclass
class MonikerClientCapabilities:
    """Client capabilities specific to the moniker request.

    @since 3.16.0"""
    # since 3.16.0
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether moniker supports dynamic registration. If this is set to `true`
    the client supports the new `MonikerRegistrationOptions` return value
    for the corresponding server capability as well."""

@dataclass
class TypeHierarchyClientCapabilities:
    """@since 3.17.0"""
    # since 3.17.0
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether implementation supports dynamic registration. If this is set to `true`
    the client supports the new `(TextDocumentRegistrationOptions & StaticRegistrationOptions)`
    return value for the corresponding server capability as well."""

@dataclass
class InlineValueClientCapabilities:
    """Client capabilities specific to inline values.

    @since 3.17.0"""
    # since 3.17.0
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether implementation supports dynamic registration for inline value providers."""

@dataclass
class ClientInlayHintResolveOptions:
    """@since 3.18.0"""
    # since 3.18.0
    properties: List[str]
    """The properties that a client can resolve lazily."""

@dataclass
class InlayHintClientCapabilities:
    """Inlay hint client capabilities.

    @since 3.17.0"""
    # since 3.17.0
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether inlay hints support dynamic registration."""
    resolveSupport: ClientInlayHintResolveOptions = field(metadata={"optional": True})
    """Indicates which properties a client can resolve lazily on an inlay
    hint."""

@dataclass
class DiagnosticClientCapabilities(DiagnosticsCapabilities):
    """Client capabilities specific to diagnostic pull requests.

    @since 3.17.0"""
    # since 3.17.0
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether implementation supports dynamic registration. If this is set to `true`
    the client supports the new `(TextDocumentRegistrationOptions & StaticRegistrationOptions)`
    return value for the corresponding server capability as well."""
    relatedDocumentSupport: bool = field(metadata={"optional": True})
    """Whether the clients supports related documents for document diagnostic pulls."""

@dataclass
class InlineCompletionClientCapabilities:
    """Client capabilities specific to inline completions.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether implementation supports dynamic registration for inline completion providers."""

@dataclass
class TextDocumentClientCapabilities:
    """Text document specific client capabilities."""
    synchronization: TextDocumentSyncClientCapabilities = field(metadata={"optional": True})
    """Defines which synchronization capabilities the client supports."""
    filters: TextDocumentFilterClientCapabilities = field(metadata={"optional": True})
    """Defines which filters the client supports.

    @since 3.18.0"""
    # since 3.18.0
    completion: CompletionClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/completion` request."""
    hover: HoverClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/hover` request."""
    signatureHelp: SignatureHelpClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/signatureHelp` request."""
    declaration: DeclarationClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/declaration` request.

    @since 3.14.0"""
    # since 3.14.0
    definition: DefinitionClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/definition` request."""
    typeDefinition: TypeDefinitionClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/typeDefinition` request.

    @since 3.6.0"""
    # since 3.6.0
    implementation: ImplementationClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/implementation` request.

    @since 3.6.0"""
    # since 3.6.0
    references: ReferenceClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/references` request."""
    documentHighlight: DocumentHighlightClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/documentHighlight` request."""
    documentSymbol: DocumentSymbolClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/documentSymbol` request."""
    codeAction: CodeActionClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/codeAction` request."""
    codeLens: CodeLensClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/codeLens` request."""
    documentLink: DocumentLinkClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/documentLink` request."""
    colorProvider: DocumentColorClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/documentColor` and the
    `textDocument/colorPresentation` request.

    @since 3.6.0"""
    # since 3.6.0
    formatting: DocumentFormattingClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/formatting` request."""
    rangeFormatting: DocumentRangeFormattingClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/rangeFormatting` request."""
    onTypeFormatting: DocumentOnTypeFormattingClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/onTypeFormatting` request."""
    rename: RenameClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/rename` request."""
    foldingRange: FoldingRangeClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/foldingRange` request.

    @since 3.10.0"""
    # since 3.10.0
    selectionRange: SelectionRangeClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/selectionRange` request.

    @since 3.15.0"""
    # since 3.15.0
    publishDiagnostics: PublishDiagnosticsClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/publishDiagnostics` notification."""
    callHierarchy: CallHierarchyClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the various call hierarchy requests.

    @since 3.16.0"""
    # since 3.16.0
    semanticTokens: SemanticTokensClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the various semantic token request.

    @since 3.16.0"""
    # since 3.16.0
    linkedEditingRange: LinkedEditingRangeClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/linkedEditingRange` request.

    @since 3.16.0"""
    # since 3.16.0
    moniker: MonikerClientCapabilities = field(metadata={"optional": True})
    """Client capabilities specific to the `textDocument/moniker` request.

    @since 3.16.0"""
    # since 3.16.0
    typeHierarchy: TypeHierarchyClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the various type hierarchy requests.

    @since 3.17.0"""
    # since 3.17.0
    inlineValue: InlineValueClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/inlineValue` request.

    @since 3.17.0"""
    # since 3.17.0
    inlayHint: InlayHintClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the `textDocument/inlayHint` request.

    @since 3.17.0"""
    # since 3.17.0
    diagnostic: DiagnosticClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the diagnostic pull model.

    @since 3.17.0"""
    # since 3.17.0
    inlineCompletion: InlineCompletionClientCapabilities = field(metadata={"optional": True})
    """Client capabilities specific to inline completions.

    @since 3.18.0
    @proposed"""
    # since 3.18.0

@dataclass
class NotebookDocumentSyncClientCapabilities:
    """Notebook specific client capabilities.

    @since 3.17.0"""
    # since 3.17.0
    dynamicRegistration: bool = field(metadata={"optional": True})
    """Whether implementation supports dynamic registration. If this is
    set to `true` the client supports the new
    `(TextDocumentRegistrationOptions & StaticRegistrationOptions)`
    return value for the corresponding server capability as well."""
    executionSummarySupport: bool = field(metadata={"optional": True})
    """The client supports sending execution summary data per cell."""

@dataclass
class NotebookDocumentClientCapabilities:
    """Capabilities specific to the notebook document support.

    @since 3.17.0"""
    # since 3.17.0
    synchronization: NotebookDocumentSyncClientCapabilities
    """Capabilities specific to notebook document synchronization

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class ClientShowMessageActionItemOptions:
    """@since 3.18.0"""
    # since 3.18.0
    additionalPropertiesSupport: bool = field(metadata={"optional": True})
    """Whether the client supports additional attributes which
    are preserved and send back to the server in the
    request's response."""

@dataclass
class ShowMessageRequestClientCapabilities:
    """Show message request client capabilities"""
    messageActionItem: ClientShowMessageActionItemOptions = field(metadata={"optional": True})
    """Capabilities specific to the `MessageActionItem` type."""

@dataclass
class ShowDocumentClientCapabilities:
    """Client capabilities for the showDocument request.

    @since 3.16.0"""
    # since 3.16.0
    support: bool
    """The client has support for the showDocument
    request."""

@dataclass
class WindowClientCapabilities:
    workDoneProgress: bool = field(metadata={"optional": True})
    """It indicates whether the client supports server initiated
    progress using the `window/workDoneProgress/create` request.

    The capability also controls Whether client supports handling
    of progress notifications. If set servers are allowed to report a
    `workDoneProgress` property in the request specific server
    capabilities.

    @since 3.15.0"""
    # since 3.15.0
    showMessage: ShowMessageRequestClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the showMessage request.

    @since 3.16.0"""
    # since 3.16.0
    showDocument: ShowDocumentClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the showDocument request.

    @since 3.16.0"""
    # since 3.16.0

@dataclass
class StaleRequestSupportOptions:
    """@since 3.18.0"""
    # since 3.18.0
    cancel: bool
    """The client will actively cancel the request."""
    retryOnContentModified: List[str]
    """The list of requests for which the client
    will retry the request if it receives a
    response with error code `ContentModified`"""

RegularExpressionEngineKind: TypeAlias = str

@dataclass
class RegularExpressionsClientCapabilities:
    """Client capabilities specific to regular expressions.

    @since 3.16.0"""
    # since 3.16.0
    engine: RegularExpressionEngineKind
    """The engine's name."""
    version: str = field(metadata={"optional": True})
    """The engine's version."""

@dataclass
class MarkdownClientCapabilities:
    """Client capabilities specific to the used markdown parser.

    @since 3.16.0"""
    # since 3.16.0
    parser: str
    """The name of the parser."""
    version: str = field(metadata={"optional": True})
    """The version of the parser."""
    allowedTags: List[str] = field(metadata={"optional": True})
    """A list of HTML tags that the client allows / supports in
    Markdown.

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class GeneralClientCapabilities:
    """General client capabilities.

    @since 3.16.0"""
    # since 3.16.0
    staleRequestSupport: StaleRequestSupportOptions = field(metadata={"optional": True})
    """Client capability that signals how the client
    handles stale requests (e.g. a request
    for which the client will not process the response
    anymore since the information is outdated).

    @since 3.17.0"""
    # since 3.17.0
    regularExpressions: RegularExpressionsClientCapabilities = field(metadata={"optional": True})
    """Client capabilities specific to regular expressions.

    @since 3.16.0"""
    # since 3.16.0
    markdown: MarkdownClientCapabilities = field(metadata={"optional": True})
    """Client capabilities specific to the client's markdown parser.

    @since 3.16.0"""
    # since 3.16.0
    positionEncodings: List[PositionEncodingKind] = field(metadata={"optional": True})
    """The position encodings supported by the client. Client and server
    have to agree on the same position encoding to ensure that offsets
    (e.g. character position in a line) are interpreted the same on both
    sides.

    To keep the protocol backwards compatible the following applies: if
    the value 'utf-16' is missing from the array of position encodings
    servers can assume that the client supports UTF-16. UTF-16 is
    therefore a mandatory encoding.

    If omitted it defaults to ['utf-16'].

    Implementation considerations: since the conversion from one encoding
    into another requires the content of the file / line the conversion
    is best done where the file is read which is usually on the server
    side.

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class ClientCapabilities:
    """Defines the capabilities provided by the client."""
    workspace: WorkspaceClientCapabilities = field(metadata={"optional": True})
    """Workspace specific client capabilities."""
    textDocument: TextDocumentClientCapabilities = field(metadata={"optional": True})
    """Text document specific client capabilities."""
    notebookDocument: NotebookDocumentClientCapabilities = field(metadata={"optional": True})
    """Capabilities specific to the notebook document support.

    @since 3.17.0"""
    # since 3.17.0
    window: WindowClientCapabilities = field(metadata={"optional": True})
    """Window specific client capabilities."""
    general: GeneralClientCapabilities = field(metadata={"optional": True})
    """General client capabilities.

    @since 3.16.0"""
    # since 3.16.0
    experimental: Any = field(metadata={"optional": True})
    """Experimental client capabilities."""

@dataclass
class _InitializeParams:
    """The initialize parameters"""
    processId: Union[int, None]
    """The process Id of the parent process that started
    the server.

    Is `null` if the process has not been started by another process.
    If the parent process is not alive then the server should exit."""
    clientInfo: ClientInfo = field(metadata={"optional": True})
    """Information about the client

    @since 3.15.0"""
    # since 3.15.0
    locale: str = field(metadata={"optional": True})
    """The locale the client is currently showing the user interface
    in. This must not necessarily be the locale of the operating
    system.

    Uses IETF language tags as the value's syntax
    (See https://en.wikipedia.org/wiki/IETF_language_tag)

    @since 3.16.0"""
    # since 3.16.0
    rootPath: Union[str, None] = field(metadata={"optional": True})
    """The rootPath of the workspace. Is null
    if no folder is open.

    @deprecated in favour of rootUri."""
    rootUri: Union[DocumentUri, None]
    """The rootUri of the workspace. Is null if no
    folder is open. If both `rootPath` and `rootUri` are set
    `rootUri` wins.

    @deprecated in favour of workspaceFolders."""
    capabilities: ClientCapabilities
    """The capabilities provided by the client (editor or tool)"""
    initializationOptions: Any = field(metadata={"optional": True})
    """User provided initialization options."""
    trace: TraceValue = field(metadata={"optional": True})
    """The initial trace setting. If omitted trace is disabled ('off')."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class WorkspaceFoldersInitializeParams:
    workspaceFolders: Union[List[WorkspaceFolder], None] = field(metadata={"optional": True})
    """The workspace folders configured in the client when the server starts.

    This property is only available if the client supports workspace folders.
    It can be `null` if the client supports workspace folders but none are
    configured.

    @since 3.6.0"""
    # since 3.6.0

@dataclass
class InitializeParams(_InitializeParams, WorkspaceFoldersInitializeParams):
    """"""

@dataclass
class SaveOptions:
    """Save options."""
    includeText: bool = field(metadata={"optional": True})
    """The client is supposed to include the content on save."""

@dataclass
class TextDocumentSyncOptions:
    openClose: bool = field(metadata={"optional": True})
    """Open and close notifications are sent to the server. If omitted open close notification should not
    be sent."""
    change: TextDocumentSyncKind = field(metadata={"optional": True})
    """Change notifications are sent to the server. See TextDocumentSyncKind.None, TextDocumentSyncKind.Full
    and TextDocumentSyncKind.Incremental. If omitted it defaults to TextDocumentSyncKind.None."""
    willSave: bool = field(metadata={"optional": True})
    """If present will save notifications are sent to the server. If omitted the notification should not be
    sent."""
    willSaveWaitUntil: bool = field(metadata={"optional": True})
    """If present will save wait until requests are sent to the server. If omitted the request should not be
    sent."""
    save: Union[bool, SaveOptions] = field(metadata={"optional": True})
    """If present save notifications are sent to the server. If omitted the notification should not be
    sent."""

@dataclass
class ServerCompletionItemOptions:
    """@since 3.18.0"""
    # since 3.18.0
    labelDetailsSupport: bool = field(metadata={"optional": True})
    """The server has support for completion item label
    details (see also `CompletionItemLabelDetails`) when
    receiving a completion item in a resolve call.

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class CompletionOptions:
    """Completion options."""
    triggerCharacters: List[str] = field(metadata={"optional": True})
    """Most tools trigger completion request automatically without explicitly requesting
    it using a keyboard shortcut (e.g. Ctrl+Space). Typically they do so when the user
    starts to type an identifier. For example if the user types `c` in a JavaScript file
    code complete will automatically pop up present `console` besides others as a
    completion item. Characters that make up identifiers don't need to be listed here.

    If code complete should automatically be trigger on characters not being valid inside
    an identifier (for example `.` in JavaScript) list them in `triggerCharacters`."""
    allCommitCharacters: List[str] = field(metadata={"optional": True})
    """The list of all possible characters that commit a completion. This field can be used
    if clients don't support individual commit characters per completion item. See
    `ClientCapabilities.textDocument.completion.completionItem.commitCharactersSupport`

    If a server provides both `allCommitCharacters` and commit characters on an individual
    completion item the ones on the completion item win.

    @since 3.2.0"""
    # since 3.2.0
    resolveProvider: bool = field(metadata={"optional": True})
    """The server provides support to resolve additional
    information for a completion item."""
    completionItem: ServerCompletionItemOptions = field(metadata={"optional": True})
    """The server supports the following `CompletionItem` specific
    capabilities.

    @since 3.17.0"""
    # since 3.17.0
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class HoverOptions:
    """Hover options."""
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class SignatureHelpOptions:
    """Server Capabilities for a {@link SignatureHelpRequest}."""
    triggerCharacters: List[str] = field(metadata={"optional": True})
    """List of characters that trigger signature help automatically."""
    retriggerCharacters: List[str] = field(metadata={"optional": True})
    """List of characters that re-trigger signature help.

    These trigger characters are only active when signature help is already showing. All trigger characters
    are also counted as re-trigger characters.

    @since 3.15.0"""
    # since 3.15.0
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class DefinitionOptions:
    """Server Capabilities for a {@link DefinitionRequest}."""
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class ReferenceOptions:
    """Reference options."""
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class DocumentHighlightOptions:
    """Provider options for a {@link DocumentHighlightRequest}."""
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class DocumentSymbolOptions:
    """Provider options for a {@link DocumentSymbolRequest}."""
    label: str = field(metadata={"optional": True})
    """A human-readable string that is shown when multiple outlines trees
    are shown for the same document.

    @since 3.16.0"""
    # since 3.16.0
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class CodeActionKindDocumentation:
    """Documentation for a class of code actions.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    kind: CodeActionKind
    """The kind of the code action being documented.

    If the kind is generic, such as `CodeActionKind.Refactor`, the documentation will be shown whenever any
    refactorings are returned. If the kind if more specific, such as `CodeActionKind.RefactorExtract`, the
    documentation will only be shown when extract refactoring code actions are returned."""
    command: Command
    """Command that is ued to display the documentation to the user.

    The title of this documentation code action is taken from {@linkcode Command.title}"""

@dataclass
class CodeActionOptions:
    """Provider options for a {@link CodeActionRequest}."""
    codeActionKinds: List[CodeActionKind] = field(metadata={"optional": True})
    """CodeActionKinds that this server may return.

    The list of kinds may be generic, such as `CodeActionKind.Refactor`, or the server
    may list out every specific kind they provide."""
    documentation: List[CodeActionKindDocumentation] = field(metadata={"optional": True})
    """Static documentation for a class of code actions.

    Documentation from the provider should be shown in the code actions menu if either:

    - Code actions of `kind` are requested by the editor. In this case, the editor will show the documentation that
      most closely matches the requested code action kind. For example, if a provider has documentation for
      both `Refactor` and `RefactorExtract`, when the user requests code actions for `RefactorExtract`,
      the editor will use the documentation for `RefactorExtract` instead of the documentation for `Refactor`.

    - Any code actions of `kind` are returned by the provider.

    At most one documentation entry should be shown per provider.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    resolveProvider: bool = field(metadata={"optional": True})
    """The server provides support to resolve additional
    information for a code action.

    @since 3.16.0"""
    # since 3.16.0
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class CodeLensOptions:
    """Code Lens provider options of a {@link CodeLensRequest}."""
    resolveProvider: bool = field(metadata={"optional": True})
    """Code lens has a resolve provider as well."""
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class DocumentLinkOptions:
    """Provider options for a {@link DocumentLinkRequest}."""
    resolveProvider: bool = field(metadata={"optional": True})
    """Document links have a resolve provider as well."""
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class WorkspaceSymbolOptions:
    """Server capabilities for a {@link WorkspaceSymbolRequest}."""
    resolveProvider: bool = field(metadata={"optional": True})
    """The server provides support to resolve additional
    information for a workspace symbol.

    @since 3.17.0"""
    # since 3.17.0
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class DocumentFormattingOptions:
    """Provider options for a {@link DocumentFormattingRequest}."""
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class DocumentRangeFormattingOptions:
    """Provider options for a {@link DocumentRangeFormattingRequest}."""
    rangesSupport: bool = field(metadata={"optional": True})
    """Whether the server supports formatting multiple ranges at once.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class DocumentOnTypeFormattingOptions:
    """Provider options for a {@link DocumentOnTypeFormattingRequest}."""
    firstTriggerCharacter: str
    """A character on which formatting should be triggered, like `{`."""
    moreTriggerCharacter: List[str] = field(metadata={"optional": True})
    """More trigger characters."""

@dataclass
class RenameOptions:
    """Provider options for a {@link RenameRequest}."""
    prepareProvider: bool = field(metadata={"optional": True})
    """Renames should be checked and tested before being executed.

    @since version 3.12.0"""
    # since version 3.12.0
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class ExecuteCommandOptions:
    """The server capabilities of a {@link ExecuteCommandRequest}."""
    commands: List[str]
    """The commands to be executed on the server"""
    workDoneProgress: bool = field(metadata={"optional": True})

@dataclass
class WorkspaceFoldersServerCapabilities:
    supported: bool = field(metadata={"optional": True})
    """The server has support for workspace folders"""
    changeNotifications: Union[str, bool] = field(metadata={"optional": True})
    """Whether the server wants to receive workspace folder
    change notifications.

    If a string is provided the string is treated as an ID
    under which the notification is registered on the client
    side. The ID can be used to unregister for these events
    using the `client/unregisterCapability` request."""

@dataclass
class FileOperationOptions:
    """Options for notifications/requests for user operations on files.

    @since 3.16.0"""
    # since 3.16.0
    didCreate: FileOperationRegistrationOptions = field(metadata={"optional": True})
    """The server is interested in receiving didCreateFiles notifications."""
    willCreate: FileOperationRegistrationOptions = field(metadata={"optional": True})
    """The server is interested in receiving willCreateFiles requests."""
    didRename: FileOperationRegistrationOptions = field(metadata={"optional": True})
    """The server is interested in receiving didRenameFiles notifications."""
    willRename: FileOperationRegistrationOptions = field(metadata={"optional": True})
    """The server is interested in receiving willRenameFiles requests."""
    didDelete: FileOperationRegistrationOptions = field(metadata={"optional": True})
    """The server is interested in receiving didDeleteFiles file notifications."""
    willDelete: FileOperationRegistrationOptions = field(metadata={"optional": True})
    """The server is interested in receiving willDeleteFiles file requests."""

@dataclass
class WorkspaceOptions:
    """Defines workspace specific capabilities of the server.

    @since 3.18.0"""
    # since 3.18.0
    workspaceFolders: WorkspaceFoldersServerCapabilities = field(metadata={"optional": True})
    """The server supports workspace folder.

    @since 3.6.0"""
    # since 3.6.0
    fileOperations: FileOperationOptions = field(metadata={"optional": True})
    """The server is interested in notifications/requests for operations on files.

    @since 3.16.0"""
    # since 3.16.0
    textDocumentContent: Union[TextDocumentContentOptions, TextDocumentContentRegistrationOptions] = field(metadata={"optional": True})
    """The server supports the `workspace/textDocumentContent` request.

    @since 3.18.0
    @proposed"""
    # since 3.18.0

@dataclass
class ServerCapabilities:
    """Defines the capabilities provided by a language
    server."""
    positionEncoding: PositionEncodingKind = field(metadata={"optional": True})
    """The position encoding the server picked from the encodings offered
    by the client via the client capability `general.positionEncodings`.

    If the client didn't provide any position encodings the only valid
    value that a server can return is 'utf-16'.

    If omitted it defaults to 'utf-16'.

    @since 3.17.0"""
    # since 3.17.0
    textDocumentSync: Union[TextDocumentSyncOptions, TextDocumentSyncKind] = field(metadata={"optional": True})
    """Defines how text documents are synced. Is either a detailed structure
    defining each notification or for backwards compatibility the
    TextDocumentSyncKind number."""
    notebookDocumentSync: Union[NotebookDocumentSyncOptions, NotebookDocumentSyncRegistrationOptions] = field(metadata={"optional": True})
    """Defines how notebook documents are synced.

    @since 3.17.0"""
    # since 3.17.0
    completionProvider: CompletionOptions = field(metadata={"optional": True})
    """The server provides completion support."""
    hoverProvider: Union[bool, HoverOptions] = field(metadata={"optional": True})
    """The server provides hover support."""
    signatureHelpProvider: SignatureHelpOptions = field(metadata={"optional": True})
    """The server provides signature help support."""
    declarationProvider: Union[bool, DeclarationOptions, DeclarationRegistrationOptions] = field(metadata={"optional": True})
    """The server provides Goto Declaration support."""
    definitionProvider: Union[bool, DefinitionOptions] = field(metadata={"optional": True})
    """The server provides goto definition support."""
    typeDefinitionProvider: Union[bool, TypeDefinitionOptions, TypeDefinitionRegistrationOptions] = field(metadata={"optional": True})
    """The server provides Goto Type Definition support."""
    implementationProvider: Union[bool, ImplementationOptions, ImplementationRegistrationOptions] = field(metadata={"optional": True})
    """The server provides Goto Implementation support."""
    referencesProvider: Union[bool, ReferenceOptions] = field(metadata={"optional": True})
    """The server provides find references support."""
    documentHighlightProvider: Union[bool, DocumentHighlightOptions] = field(metadata={"optional": True})
    """The server provides document highlight support."""
    documentSymbolProvider: Union[bool, DocumentSymbolOptions] = field(metadata={"optional": True})
    """The server provides document symbol support."""
    codeActionProvider: Union[bool, CodeActionOptions] = field(metadata={"optional": True})
    """The server provides code actions. CodeActionOptions may only be
    specified if the client states that it supports
    `codeActionLiteralSupport` in its initial `initialize` request."""
    codeLensProvider: CodeLensOptions = field(metadata={"optional": True})
    """The server provides code lens."""
    documentLinkProvider: DocumentLinkOptions = field(metadata={"optional": True})
    """The server provides document link support."""
    colorProvider: Union[bool, DocumentColorOptions, DocumentColorRegistrationOptions] = field(metadata={"optional": True})
    """The server provides color provider support."""
    workspaceSymbolProvider: Union[bool, WorkspaceSymbolOptions] = field(metadata={"optional": True})
    """The server provides workspace symbol support."""
    documentFormattingProvider: Union[bool, DocumentFormattingOptions] = field(metadata={"optional": True})
    """The server provides document formatting."""
    documentRangeFormattingProvider: Union[bool, DocumentRangeFormattingOptions] = field(metadata={"optional": True})
    """The server provides document range formatting."""
    documentOnTypeFormattingProvider: DocumentOnTypeFormattingOptions = field(metadata={"optional": True})
    """The server provides document formatting on typing."""
    renameProvider: Union[bool, RenameOptions] = field(metadata={"optional": True})
    """The server provides rename support. RenameOptions may only be
    specified if the client states that it supports
    `prepareSupport` in its initial `initialize` request."""
    foldingRangeProvider: Union[bool, FoldingRangeOptions, FoldingRangeRegistrationOptions] = field(metadata={"optional": True})
    """The server provides folding provider support."""
    selectionRangeProvider: Union[bool, SelectionRangeOptions, SelectionRangeRegistrationOptions] = field(metadata={"optional": True})
    """The server provides selection range support."""
    executeCommandProvider: ExecuteCommandOptions = field(metadata={"optional": True})
    """The server provides execute command support."""
    callHierarchyProvider: Union[bool, CallHierarchyOptions, CallHierarchyRegistrationOptions] = field(metadata={"optional": True})
    """The server provides call hierarchy support.

    @since 3.16.0"""
    # since 3.16.0
    linkedEditingRangeProvider: Union[bool, LinkedEditingRangeOptions, LinkedEditingRangeRegistrationOptions] = field(metadata={"optional": True})
    """The server provides linked editing range support.

    @since 3.16.0"""
    # since 3.16.0
    semanticTokensProvider: Union[SemanticTokensOptions, SemanticTokensRegistrationOptions] = field(metadata={"optional": True})
    """The server provides semantic tokens support.

    @since 3.16.0"""
    # since 3.16.0
    monikerProvider: Union[bool, MonikerOptions, MonikerRegistrationOptions] = field(metadata={"optional": True})
    """The server provides moniker support.

    @since 3.16.0"""
    # since 3.16.0
    typeHierarchyProvider: Union[bool, TypeHierarchyOptions, TypeHierarchyRegistrationOptions] = field(metadata={"optional": True})
    """The server provides type hierarchy support.

    @since 3.17.0"""
    # since 3.17.0
    inlineValueProvider: Union[bool, InlineValueOptions, InlineValueRegistrationOptions] = field(metadata={"optional": True})
    """The server provides inline values.

    @since 3.17.0"""
    # since 3.17.0
    inlayHintProvider: Union[bool, InlayHintOptions, InlayHintRegistrationOptions] = field(metadata={"optional": True})
    """The server provides inlay hints.

    @since 3.17.0"""
    # since 3.17.0
    diagnosticProvider: Union[DiagnosticOptions, DiagnosticRegistrationOptions] = field(metadata={"optional": True})
    """The server has support for pull model diagnostics.

    @since 3.17.0"""
    # since 3.17.0
    inlineCompletionProvider: Union[bool, InlineCompletionOptions] = field(metadata={"optional": True})
    """Inline completion options used during static registration.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    workspace: WorkspaceOptions = field(metadata={"optional": True})
    """Workspace specific server capabilities."""
    experimental: Any = field(metadata={"optional": True})
    """Experimental server capabilities."""

@dataclass
class ServerInfo:
    """Information about the server

    @since 3.15.0
    @since 3.18.0 ServerInfo type name added."""
    # since 3.18.0 ServerInfo type name added.
    name: str
    """The name of the server as defined by the server."""
    version: str = field(metadata={"optional": True})
    """The server's version as defined by the server."""

@dataclass
class InitializeResult:
    """The result returned from an initialize request."""
    capabilities: ServerCapabilities
    """The capabilities the language server provides."""
    serverInfo: ServerInfo = field(metadata={"optional": True})
    """Information about the server.

    @since 3.15.0"""
    # since 3.15.0

@dataclass
class InitializeError:
    """The data type of the ResponseError if the
    initialize request fails."""
    retry: bool
    """Indicates whether the client execute the following retry logic:
    (1) show the message provided by the ResponseError to the user
    (2) user selects retry or cancel
    (3) if user selected retry the initialize method is sent again."""

@dataclass
class InitializedParams:
    """"""

@dataclass
class DidChangeConfigurationParams:
    """The parameters of a change configuration notification."""
    settings: Any
    """The actual changed settings"""

@dataclass
class DidChangeConfigurationRegistrationOptions:
    section: Union[str, List[str]] = field(metadata={"optional": True})

@dataclass
class ShowMessageParams:
    """The parameters of a notification message."""
    type: MessageType
    """The message type. See {@link MessageType}"""
    message: str
    """The actual message."""

@dataclass
class MessageActionItem:
    title: str
    """A short title like 'Retry', 'Open Log' etc."""

@dataclass
class ShowMessageRequestParams:
    type: MessageType
    """The message type. See {@link MessageType}"""
    message: str
    """The actual message."""
    actions: List[MessageActionItem] = field(metadata={"optional": True})
    """The message action items to present."""

@dataclass
class LogMessageParams:
    """The log message parameters."""
    type: MessageType
    """The message type. See {@link MessageType}"""
    message: str
    """The actual message."""

@dataclass
class DidOpenTextDocumentParams:
    """The parameters sent in an open text document notification"""
    textDocument: TextDocumentItem
    """The document that was opened."""

@dataclass
class DidChangeTextDocumentParams:
    """The change text document notification's parameters."""
    textDocument: VersionedTextDocumentIdentifier
    """The document that did change. The version number points
    to the version after all provided content changes have
    been applied."""
    contentChanges: List[TextDocumentContentChangeEvent]
    """The actual content changes. The content changes describe single state changes
    to the document. So if there are two content changes c1 (at array index 0) and
    c2 (at array index 1) for a document in state S then c1 moves the document from
    S to S' and c2 from S' to S''. So c1 is computed on the state S and c2 is computed
    on the state S'.

    To mirror the content of a document using change events use the following approach:
    - start with the same initial content
    - apply the 'textDocument/didChange' notifications in the order you receive them.
    - apply the `TextDocumentContentChangeEvent`s in a single notification in the order
      you receive them."""

@dataclass
class TextDocumentChangeRegistrationOptions(TextDocumentRegistrationOptions):
    """Describe options to be used when registered for text document change events."""
    syncKind: TextDocumentSyncKind
    """How documents are synced to the server."""

@dataclass
class DidCloseTextDocumentParams:
    """The parameters sent in a close text document notification"""
    textDocument: TextDocumentIdentifier
    """The document that was closed."""

@dataclass
class DidSaveTextDocumentParams:
    """The parameters sent in a save text document notification"""
    textDocument: TextDocumentIdentifier
    """The document that was saved."""
    text: str = field(metadata={"optional": True})
    """Optional the content when saved. Depends on the includeText value
    when the save notification was requested."""

@dataclass
class TextDocumentSaveRegistrationOptions(TextDocumentRegistrationOptions, SaveOptions):
    """Save registration options."""

@dataclass
class WillSaveTextDocumentParams:
    """The parameters sent in a will save text document notification."""
    textDocument: TextDocumentIdentifier
    """The document that will be saved."""
    reason: TextDocumentSaveReason
    """The 'TextDocumentSaveReason'."""

@dataclass
class FileEvent:
    """An event describing a file change."""
    uri: DocumentUri
    """The file's uri."""
    type: FileChangeType
    """The change type."""

@dataclass
class DidChangeWatchedFilesParams:
    """The watched files change notification's parameters."""
    changes: List[FileEvent]
    """The actual file events."""

@dataclass
class FileSystemWatcher:
    globPattern: GlobPattern
    """The glob pattern to watch. See {@link GlobPattern glob pattern} for more detail.

    @since 3.17.0 support for relative patterns."""
    # since 3.17.0 support for relative patterns.
    kind: WatchKind = field(metadata={"optional": True})
    """The kind of events of interest. If omitted it defaults
    to WatchKind.Create | WatchKind.Change | WatchKind.Delete
    which is 7."""

@dataclass
class DidChangeWatchedFilesRegistrationOptions:
    """Describe options to be used when registered for text document change events."""
    watchers: List[FileSystemWatcher]
    """The watchers to register."""

@dataclass
class PublishDiagnosticsParams:
    """The publish diagnostic notification's parameters."""
    uri: DocumentUri
    """The URI for which diagnostic information is reported."""
    version: int = field(metadata={"optional": True})
    """Optional the version number of the document the diagnostics are published for.

    @since 3.15.0"""
    # since 3.15.0
    diagnostics: List[Diagnostic]
    """An array of diagnostic information items."""

@dataclass
class CompletionContext:
    """Contains additional information about the context in which a completion request is triggered."""
    triggerKind: CompletionTriggerKind
    """How the completion was triggered."""
    triggerCharacter: str = field(metadata={"optional": True})
    """The trigger character (a single character) that has trigger code complete.
    Is undefined if `triggerKind !== CompletionTriggerKind.TriggerCharacter`"""

@dataclass
class CompletionParams(TextDocumentPositionParams):
    """Completion parameters"""
    context: CompletionContext = field(metadata={"optional": True})
    """The completion context. This is only available it the client specifies
    to send this using the client capability `textDocument.completion.contextSupport === true`"""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class CompletionItemLabelDetails:
    """Additional details for a completion item label.

    @since 3.17.0"""
    # since 3.17.0
    detail: str = field(metadata={"optional": True})
    """An optional string which is rendered less prominently directly after {@link CompletionItem.label label},
    without any spacing. Should be used for function signatures and type annotations."""
    description: str = field(metadata={"optional": True})
    """An optional string which is rendered less prominently after {@link CompletionItem.detail}. Should be used
    for fully qualified names and file paths."""

@dataclass
class InsertReplaceEdit:
    """A special text edit to provide an insert and a replace operation.

    @since 3.16.0"""
    # since 3.16.0
    newText: str
    """The string to be inserted."""
    insert: Range
    """The range if the insert is requested"""
    replace: Range
    """The range if the replace is requested."""

@dataclass
class CompletionItem:
    """A completion item represents a text snippet that is
    proposed to complete text that is being typed."""
    label: str
    """The label of this completion item.

    The label property is also by default the text that
    is inserted when selecting this completion.

    If label details are provided the label itself should
    be an unqualified name of the completion item."""
    labelDetails: CompletionItemLabelDetails = field(metadata={"optional": True})
    """Additional details for the label

    @since 3.17.0"""
    # since 3.17.0
    kind: CompletionItemKind = field(metadata={"optional": True})
    """The kind of this completion item. Based of the kind
    an icon is chosen by the editor."""
    tags: List[CompletionItemTag] = field(metadata={"optional": True})
    """Tags for this completion item.

    @since 3.15.0"""
    # since 3.15.0
    detail: str = field(metadata={"optional": True})
    """A human-readable string with additional information
    about this item, like type or symbol information."""
    documentation: Union[str, MarkupContent] = field(metadata={"optional": True})
    """A human-readable string that represents a doc-comment."""
    deprecated: bool = field(metadata={"optional": True})
    """Indicates if this item is deprecated.
    @deprecated Use `tags` instead."""
    preselect: bool = field(metadata={"optional": True})
    """Select this item when showing.

    *Note* that only one completion item can be selected and that the
    tool / client decides which item that is. The rule is that the *first*
    item of those that match best is selected."""
    sortText: str = field(metadata={"optional": True})
    """A string that should be used when comparing this item
    with other items. When `falsy` the {@link CompletionItem.label label}
    is used."""
    filterText: str = field(metadata={"optional": True})
    """A string that should be used when filtering a set of
    completion items. When `falsy` the {@link CompletionItem.label label}
    is used."""
    insertText: str = field(metadata={"optional": True})
    """A string that should be inserted into a document when selecting
    this completion. When `falsy` the {@link CompletionItem.label label}
    is used.

    The `insertText` is subject to interpretation by the client side.
    Some tools might not take the string literally. For example
    VS Code when code complete is requested in this example
    `con<cursor position>` and a completion item with an `insertText` of
    `console` is provided it will only insert `sole`. Therefore it is
    recommended to use `textEdit` instead since it avoids additional client
    side interpretation."""
    insertTextFormat: InsertTextFormat = field(metadata={"optional": True})
    """The format of the insert text. The format applies to both the
    `insertText` property and the `newText` property of a provided
    `textEdit`. If omitted defaults to `InsertTextFormat.PlainText`.

    Please note that the insertTextFormat doesn't apply to
    `additionalTextEdits`."""
    insertTextMode: InsertTextMode = field(metadata={"optional": True})
    """How whitespace and indentation is handled during completion
    item insertion. If not provided the clients default value depends on
    the `textDocument.completion.insertTextMode` client capability.

    @since 3.16.0"""
    # since 3.16.0
    textEdit: Union[TextEdit, InsertReplaceEdit] = field(metadata={"optional": True})
    """An {@link TextEdit edit} which is applied to a document when selecting
    this completion. When an edit is provided the value of
    {@link CompletionItem.insertText insertText} is ignored.

    Most editors support two different operations when accepting a completion
    item. One is to insert a completion text and the other is to replace an
    existing text with a completion text. Since this can usually not be
    predetermined by a server it can report both ranges. Clients need to
    signal support for `InsertReplaceEdits` via the
    `textDocument.completion.insertReplaceSupport` client capability
    property.

    *Note 1:* The text edit's range as well as both ranges from an insert
    replace edit must be a [single line] and they must contain the position
    at which completion has been requested.
    *Note 2:* If an `InsertReplaceEdit` is returned the edit's insert range
    must be a prefix of the edit's replace range, that means it must be
    contained and starting at the same position.

    @since 3.16.0 additional type `InsertReplaceEdit`"""
    # since 3.16.0 additional type `InsertReplaceEdit`
    textEditText: str = field(metadata={"optional": True})
    """The edit text used if the completion item is part of a CompletionList and
    CompletionList defines an item default for the text edit range.

    Clients will only honor this property if they opt into completion list
    item defaults using the capability `completionList.itemDefaults`.

    If not provided and a list's default range is provided the label
    property is used as a text.

    @since 3.17.0"""
    # since 3.17.0
    additionalTextEdits: List[TextEdit] = field(metadata={"optional": True})
    """An optional array of additional {@link TextEdit text edits} that are applied when
    selecting this completion. Edits must not overlap (including the same insert position)
    with the main {@link CompletionItem.textEdit edit} nor with themselves.

    Additional text edits should be used to change text unrelated to the current cursor position
    (for example adding an import statement at the top of the file if the completion item will
    insert an unqualified type)."""
    commitCharacters: List[str] = field(metadata={"optional": True})
    """An optional set of characters that when pressed while this completion is active will accept it first and
    then type that character. *Note* that all commit characters should have `length=1` and that superfluous
    characters will be ignored."""
    command: Command = field(metadata={"optional": True})
    """An optional {@link Command command} that is executed *after* inserting this completion. *Note* that
    additional modifications to the current document should be described with the
    {@link CompletionItem.additionalTextEdits additionalTextEdits}-property."""
    data: Any = field(metadata={"optional": True})
    """A data entry field that is preserved on a completion item between a
    {@link CompletionRequest} and a {@link CompletionResolveRequest}."""

@dataclass
class EditRangeWithInsertReplace:
    """Edit range variant that includes ranges for insert and replace operations.

    @since 3.18.0"""
    # since 3.18.0
    insert: Range
    replace: Range

@dataclass
class CompletionItemDefaults:
    """In many cases the items of an actual completion result share the same
    value for properties like `commitCharacters` or the range of a text
    edit. A completion list can therefore define item defaults which will
    be used if a completion item itself doesn't specify the value.

    If a completion list specifies a default value and a completion item
    also specifies a corresponding value, the rules for combining these are
    defined by `applyKinds` (if the client supports it), defaulting to
    ApplyKind.Replace.

    Servers are only allowed to return default values if the client
    signals support for this via the `completionList.itemDefaults`
    capability.

    @since 3.17.0"""
    # since 3.17.0
    commitCharacters: List[str] = field(metadata={"optional": True})
    """A default commit character set.

    @since 3.17.0"""
    # since 3.17.0
    editRange: Union[Range, EditRangeWithInsertReplace] = field(metadata={"optional": True})
    """A default edit range.

    @since 3.17.0"""
    # since 3.17.0
    insertTextFormat: InsertTextFormat = field(metadata={"optional": True})
    """A default insert text format.

    @since 3.17.0"""
    # since 3.17.0
    insertTextMode: InsertTextMode = field(metadata={"optional": True})
    """A default insert text mode.

    @since 3.17.0"""
    # since 3.17.0
    data: Any = field(metadata={"optional": True})
    """A default data value.

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class CompletionItemApplyKinds:
    """Specifies how fields from a completion item should be combined with those
    from `completionList.itemDefaults`.

    If unspecified, all fields will be treated as ApplyKind.Replace.

    If a field's value is ApplyKind.Replace, the value from a completion item (if
    provided and not `null`) will always be used instead of the value from
    `completionItem.itemDefaults`.

    If a field's value is ApplyKind.Merge, the values will be merged using the rules
    defined against each field below.

    Servers are only allowed to return `applyKind` if the client
    signals support for this via the `completionList.applyKindSupport`
    capability.

    @since 3.18.0"""
    # since 3.18.0
    commitCharacters: ApplyKind = field(metadata={"optional": True})
    """Specifies whether commitCharacters on a completion will replace or be
    merged with those in `completionList.itemDefaults.commitCharacters`.

    If ApplyKind.Replace, the commit characters from the completion item will
    always be used unless not provided, in which case those from
    `completionList.itemDefaults.commitCharacters` will be used. An
    empty list can be used if a completion item does not have any commit
    characters and also should not use those from
    `completionList.itemDefaults.commitCharacters`.

    If ApplyKind.Merge the commitCharacters for the completion will be the
    union of all values in both `completionList.itemDefaults.commitCharacters`
    and the completion's own `commitCharacters`.

    @since 3.18.0"""
    # since 3.18.0
    data: ApplyKind = field(metadata={"optional": True})
    """Specifies whether the `data` field on a completion will replace or
    be merged with data from `completionList.itemDefaults.data`.

    If ApplyKind.Replace, the data from the completion item will be used if
    provided (and not `null`), otherwise
    `completionList.itemDefaults.data` will be used. An empty object can
    be used if a completion item does not have any data but also should
    not use the value from `completionList.itemDefaults.data`.

    If ApplyKind.Merge, a shallow merge will be performed between
    `completionList.itemDefaults.data` and the completion's own data
    using the following rules:

    - If a completion's `data` field is not provided (or `null`), the
      entire `data` field from `completionList.itemDefaults.data` will be
      used as-is.
    - If a completion's `data` field is provided, each field will
      overwrite the field of the same name in
      `completionList.itemDefaults.data` but no merging of nested fields
      within that value will occur.

    @since 3.18.0"""
    # since 3.18.0

@dataclass
class CompletionList:
    """Represents a collection of {@link CompletionItem completion items} to be presented
    in the editor."""
    isIncomplete: bool
    """This list it not complete. Further typing results in recomputing this list.

    Recomputed lists have all their items replaced (not appended) in the
    incomplete completion sessions."""
    itemDefaults: CompletionItemDefaults = field(metadata={"optional": True})
    """In many cases the items of an actual completion result share the same
    value for properties like `commitCharacters` or the range of a text
    edit. A completion list can therefore define item defaults which will
    be used if a completion item itself doesn't specify the value.

    If a completion list specifies a default value and a completion item
    also specifies a corresponding value, the rules for combining these are
    defined by `applyKinds` (if the client supports it), defaulting to
    ApplyKind.Replace.

    Servers are only allowed to return default values if the client
    signals support for this via the `completionList.itemDefaults`
    capability.

    @since 3.17.0"""
    # since 3.17.0
    applyKind: CompletionItemApplyKinds = field(metadata={"optional": True})
    """Specifies how fields from a completion item should be combined with those
    from `completionList.itemDefaults`.

    If unspecified, all fields will be treated as ApplyKind.Replace.

    If a field's value is ApplyKind.Replace, the value from a completion item
    (if provided and not `null`) will always be used instead of the value
    from `completionItem.itemDefaults`.

    If a field's value is ApplyKind.Merge, the values will be merged using
    the rules defined against each field below.

    Servers are only allowed to return `applyKind` if the client
    signals support for this via the `completionList.applyKindSupport`
    capability.

    @since 3.18.0"""
    # since 3.18.0
    items: List[CompletionItem]
    """The completion items."""

@dataclass
class CompletionRegistrationOptions(TextDocumentRegistrationOptions, CompletionOptions):
    """Registration options for a {@link CompletionRequest}."""

@dataclass
class HoverParams(TextDocumentPositionParams):
    """Parameters for a {@link HoverRequest}."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class MarkedStringWithLanguage:
    """@since 3.18.0
    @deprecated use MarkupContent instead."""
    # since 3.18.0
    language: str
    value: str

MarkedString: TypeAlias = Union[str, MarkedStringWithLanguage]
"""MarkedString can be used to render human readable text. It is either a markdown string
or a code-block that provides a language and a code snippet. The language identifier
is semantically equal to the optional language identifier in fenced code blocks in GitHub
issues. See https://help.github.com/articles/creating-and-highlighting-code-blocks/#syntax-highlighting

The pair of a language and a value is an equivalent to markdown:
```${language}
${value}
```

Note that markdown strings will be sanitized - that means html will be escaped.
@deprecated use MarkupContent instead."""

@dataclass
class Hover:
    """The result of a hover request."""
    contents: Union[MarkupContent, MarkedString, List[MarkedString]]
    """The hover's content"""
    range: Range = field(metadata={"optional": True})
    """An optional range inside the text document that is used to
    visualize the hover, e.g. by changing the background color."""

@dataclass
class HoverRegistrationOptions(TextDocumentRegistrationOptions, HoverOptions):
    """Registration options for a {@link HoverRequest}."""

@dataclass
class ParameterInformation:
    """Represents a parameter of a callable-signature. A parameter can
    have a label and a doc-comment."""
    label: Union[str, Tuple[int, int]]
    """The label of this parameter information.

    Either a string or an inclusive start and exclusive end offsets within its containing
    signature label. (see SignatureInformation.label). The offsets are based on a UTF-16
    string representation as `Position` and `Range` does.

    To avoid ambiguities a server should use the [start, end] offset value instead of using
    a substring. Whether a client support this is controlled via `labelOffsetSupport` client
    capability.

    *Note*: a label of type string should be a substring of its containing signature label.
    Its intended use case is to highlight the parameter label part in the `SignatureInformation.label`."""
    documentation: Union[str, MarkupContent] = field(metadata={"optional": True})
    """The human-readable doc-comment of this parameter. Will be shown
    in the UI but can be omitted."""

@dataclass
class SignatureInformation:
    """Represents the signature of something callable. A signature
    can have a label, like a function-name, a doc-comment, and
    a set of parameters."""
    label: str
    """The label of this signature. Will be shown in
    the UI."""
    documentation: Union[str, MarkupContent] = field(metadata={"optional": True})
    """The human-readable doc-comment of this signature. Will be shown
    in the UI but can be omitted."""
    parameters: List[ParameterInformation] = field(metadata={"optional": True})
    """The parameters of this signature."""
    activeParameter: Union[int, None] = field(metadata={"optional": True})
    """The index of the active parameter.

    If `null`, no parameter of the signature is active (for example a named
    argument that does not match any declared parameters). This is only valid
    if the client specifies the client capability
    `textDocument.signatureHelp.noActiveParameterSupport === true`

    If provided (or `null`), this is used in place of
    `SignatureHelp.activeParameter`.

    @since 3.16.0"""
    # since 3.16.0

@dataclass
class SignatureHelp:
    """Signature help represents the signature of something
    callable. There can be multiple signature but only one
    active and only one active parameter."""
    signatures: List[SignatureInformation]
    """One or more signatures."""
    activeSignature: int = field(metadata={"optional": True})
    """The active signature. If omitted or the value lies outside the
    range of `signatures` the value defaults to zero or is ignored if
    the `SignatureHelp` has no signatures.

    Whenever possible implementors should make an active decision about
    the active signature and shouldn't rely on a default value.

    In future version of the protocol this property might become
    mandatory to better express this."""
    activeParameter: Union[int, None] = field(metadata={"optional": True})
    """The active parameter of the active signature.

    If `null`, no parameter of the signature is active (for example a named
    argument that does not match any declared parameters). This is only valid
    if the client specifies the client capability
    `textDocument.signatureHelp.noActiveParameterSupport === true`

    If omitted or the value lies outside the range of
    `signatures[activeSignature].parameters` defaults to 0 if the active
    signature has parameters.

    If the active signature has no parameters it is ignored.

    In future version of the protocol this property might become
    mandatory (but still nullable) to better express the active parameter if
    the active signature does have any."""

@dataclass
class SignatureHelpContext:
    """Additional information about the context in which a signature help request was triggered.

    @since 3.15.0"""
    # since 3.15.0
    triggerKind: SignatureHelpTriggerKind
    """Action that caused signature help to be triggered."""
    triggerCharacter: str = field(metadata={"optional": True})
    """Character that caused signature help to be triggered.

    This is undefined when `triggerKind !== SignatureHelpTriggerKind.TriggerCharacter`"""
    isRetrigger: bool
    """`true` if signature help was already showing when it was triggered.

    Retriggers occurs when the signature help is already active and can be caused by actions such as
    typing a trigger character, a cursor move, or document content changes."""
    activeSignatureHelp: SignatureHelp = field(metadata={"optional": True})
    """The currently active `SignatureHelp`.

    The `activeSignatureHelp` has its `SignatureHelp.activeSignature` field updated based on
    the user navigating through available signatures."""

@dataclass
class SignatureHelpParams(TextDocumentPositionParams):
    """Parameters for a {@link SignatureHelpRequest}."""
    context: SignatureHelpContext = field(metadata={"optional": True})
    """The signature help context. This is only available if the client specifies
    to send this using the client capability `textDocument.signatureHelp.contextSupport === true`

    @since 3.15.0"""
    # since 3.15.0
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class SignatureHelpRegistrationOptions(TextDocumentRegistrationOptions, SignatureHelpOptions):
    """Registration options for a {@link SignatureHelpRequest}."""

@dataclass
class DefinitionParams(TextDocumentPositionParams):
    """Parameters for a {@link DefinitionRequest}."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class DefinitionRegistrationOptions(TextDocumentRegistrationOptions, DefinitionOptions):
    """Registration options for a {@link DefinitionRequest}."""

@dataclass
class ReferenceContext:
    """Value-object that contains additional information when
    requesting references."""
    includeDeclaration: bool
    """Include the declaration of the current symbol."""

@dataclass
class ReferenceParams(TextDocumentPositionParams):
    """Parameters for a {@link ReferencesRequest}."""
    context: ReferenceContext
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class ReferenceRegistrationOptions(TextDocumentRegistrationOptions, ReferenceOptions):
    """Registration options for a {@link ReferencesRequest}."""

@dataclass
class DocumentHighlightParams(TextDocumentPositionParams):
    """Parameters for a {@link DocumentHighlightRequest}."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class DocumentHighlight:
    """A document highlight is a range inside a text document which deserves
    special attention. Usually a document highlight is visualized by changing
    the background color of its range."""
    range: Range
    """The range this highlight applies to."""
    kind: DocumentHighlightKind = field(metadata={"optional": True})
    """The highlight kind, default is {@link DocumentHighlightKind.Text text}."""

@dataclass
class DocumentHighlightRegistrationOptions(TextDocumentRegistrationOptions, DocumentHighlightOptions):
    """Registration options for a {@link DocumentHighlightRequest}."""

@dataclass
class DocumentSymbolParams:
    """Parameters for a {@link DocumentSymbolRequest}."""
    textDocument: TextDocumentIdentifier
    """The text document."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class BaseSymbolInformation:
    """A base for all symbol information."""
    name: str
    """The name of this symbol."""
    kind: SymbolKind
    """The kind of this symbol."""
    tags: List[SymbolTag] = field(metadata={"optional": True})
    """Tags for this symbol.

    @since 3.16.0"""
    # since 3.16.0
    containerName: str = field(metadata={"optional": True})
    """The name of the symbol containing this symbol. This information is for
    user interface purposes (e.g. to render a qualifier in the user interface
    if necessary). It can't be used to re-infer a hierarchy for the document
    symbols."""

@dataclass
class SymbolInformation(BaseSymbolInformation):
    """Represents information about programming constructs like variables, classes,
    interfaces etc."""
    deprecated: bool = field(metadata={"optional": True})
    """Indicates if this symbol is deprecated.

    @deprecated Use tags instead"""
    location: Location
    """The location of this symbol. The location's range is used by a tool
    to reveal the location in the editor. If the symbol is selected in the
    tool the range's start information is used to position the cursor. So
    the range usually spans more than the actual symbol's name and does
    normally include things like visibility modifiers.

    The range doesn't have to denote a node range in the sense of an abstract
    syntax tree. It can therefore not be used to re-construct a hierarchy of
    the symbols."""

@dataclass
class DocumentSymbol:
    """Represents programming constructs like variables, classes, interfaces etc.
    that appear in a document. Document symbols can be hierarchical and they
    have two ranges: one that encloses its definition and one that points to
    its most interesting range, e.g. the range of an identifier."""
    name: str
    """The name of this symbol. Will be displayed in the user interface and therefore must not be
    an empty string or a string only consisting of white spaces."""
    detail: str = field(metadata={"optional": True})
    """More detail for this symbol, e.g the signature of a function."""
    kind: SymbolKind
    """The kind of this symbol."""
    tags: List[SymbolTag] = field(metadata={"optional": True})
    """Tags for this document symbol.

    @since 3.16.0"""
    # since 3.16.0
    deprecated: bool = field(metadata={"optional": True})
    """Indicates if this symbol is deprecated.

    @deprecated Use tags instead"""
    range: Range
    """The range enclosing this symbol not including leading/trailing whitespace but everything else
    like comments. This information is typically used to determine if the clients cursor is
    inside the symbol to reveal in the symbol in the UI."""
    selectionRange: Range
    """The range that should be selected and revealed when this symbol is being picked, e.g the name of a function.
    Must be contained by the `range`."""
    children: List["DocumentSymbol"] = field(metadata={"optional": True})
    """Children of this symbol, e.g. properties of a class."""

@dataclass
class DocumentSymbolRegistrationOptions(TextDocumentRegistrationOptions, DocumentSymbolOptions):
    """Registration options for a {@link DocumentSymbolRequest}."""

@dataclass
class CodeActionContext:
    """Contains additional diagnostic information about the context in which
    a {@link CodeActionProvider.provideCodeActions code action} is run."""
    diagnostics: List[Diagnostic]
    """An array of diagnostics known on the client side overlapping the range provided to the
    `textDocument/codeAction` request. They are provided so that the server knows which
    errors are currently presented to the user for the given range. There is no guarantee
    that these accurately reflect the error state of the resource. The primary parameter
    to compute code actions is the provided range."""
    only: List[CodeActionKind] = field(metadata={"optional": True})
    """Requested kind of actions to return.

    Actions not of this kind are filtered out by the client before being shown. So servers
    can omit computing them."""
    triggerKind: CodeActionTriggerKind = field(metadata={"optional": True})
    """The reason why code actions were requested.

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class CodeActionParams:
    """The parameters of a {@link CodeActionRequest}."""
    textDocument: TextDocumentIdentifier
    """The document in which the command was invoked."""
    range: Range
    """The range for which the command was invoked."""
    context: CodeActionContext
    """Context carrying additional information."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class CodeActionDisabled:
    """Captures why the code action is currently disabled.

    @since 3.18.0"""
    # since 3.18.0
    reason: str
    """Human readable description of why the code action is currently disabled.

    This is displayed in the code actions UI."""

@dataclass
class CodeAction:
    """A code action represents a change that can be performed in code, e.g. to fix a problem or
    to refactor code.

    A CodeAction must set either `edit` and/or a `command`. If both are supplied, the `edit` is applied first, then the `command` is executed."""
    title: str
    """A short, human-readable, title for this code action."""
    kind: CodeActionKind = field(metadata={"optional": True})
    """The kind of the code action.

    Used to filter code actions."""
    diagnostics: List[Diagnostic] = field(metadata={"optional": True})
    """The diagnostics that this code action resolves."""
    isPreferred: bool = field(metadata={"optional": True})
    """Marks this as a preferred action. Preferred actions are used by the `auto fix` command and can be targeted
    by keybindings.

    A quick fix should be marked preferred if it properly addresses the underlying error.
    A refactoring should be marked preferred if it is the most reasonable choice of actions to take.

    @since 3.15.0"""
    # since 3.15.0
    disabled: CodeActionDisabled = field(metadata={"optional": True})
    """Marks that the code action cannot currently be applied.

    Clients should follow the following guidelines regarding disabled code actions:

      - Disabled code actions are not shown in automatic [lightbulbs](https://code.visualstudio.com/docs/editor/editingevolved#_code-action)
        code action menus.

      - Disabled actions are shown as faded out in the code action menu when the user requests a more specific type
        of code action, such as refactorings.

      - If the user has a [keybinding](https://code.visualstudio.com/docs/editor/refactoring#_keybindings-for-code-actions)
        that auto applies a code action and only disabled code actions are returned, the client should show the user an
        error message with `reason` in the editor.

    @since 3.16.0"""
    # since 3.16.0
    edit: WorkspaceEdit = field(metadata={"optional": True})
    """The workspace edit this code action performs."""
    command: Command = field(metadata={"optional": True})
    """A command this code action executes. If a code action
    provides an edit and a command, first the edit is
    executed and then the command."""
    data: Any = field(metadata={"optional": True})
    """A data entry field that is preserved on a code action between
    a `textDocument/codeAction` and a `codeAction/resolve` request.

    @since 3.16.0"""
    # since 3.16.0
    tags: List[CodeActionTag] = field(metadata={"optional": True})
    """Tags for this code action.

    @since 3.18.0 - proposed"""
    # since 3.18.0 - proposed

@dataclass
class CodeActionRegistrationOptions(TextDocumentRegistrationOptions, CodeActionOptions):
    """Registration options for a {@link CodeActionRequest}."""

@dataclass
class WorkspaceSymbolParams:
    """The parameters of a {@link WorkspaceSymbolRequest}."""
    query: str
    """A query string to filter symbols by. Clients may send an empty
    string here to request all symbols.

    The `query`-parameter should be interpreted in a *relaxed way* as editors
    will apply their own highlighting and scoring on the results. A good rule
    of thumb is to match case-insensitive and to simply check that the
    characters of *query* appear in their order in a candidate symbol.
    Servers shouldn't use prefix, substring, or similar strict matching."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class LocationUriOnly:
    """Location with only uri and does not include range.

    @since 3.18.0"""
    # since 3.18.0
    uri: DocumentUri

@dataclass
class WorkspaceSymbol(BaseSymbolInformation):
    """A special workspace symbol that supports locations without a range.

    See also SymbolInformation.

    @since 3.17.0"""
    # since 3.17.0
    location: Union[Location, LocationUriOnly]
    """The location of the symbol. Whether a server is allowed to
    return a location without a range depends on the client
    capability `workspace.symbol.resolveSupport`.

    See SymbolInformation#location for more details."""
    data: Any = field(metadata={"optional": True})
    """A data entry field that is preserved on a workspace symbol between a
    workspace symbol request and a workspace symbol resolve request."""

@dataclass
class WorkspaceSymbolRegistrationOptions(WorkspaceSymbolOptions):
    """Registration options for a {@link WorkspaceSymbolRequest}."""

@dataclass
class CodeLensParams:
    """The parameters of a {@link CodeLensRequest}."""
    textDocument: TextDocumentIdentifier
    """The document to request code lens for."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class CodeLens:
    """A code lens represents a {@link Command command} that should be shown along with
    source text, like the number of references, a way to run tests, etc.

    A code lens is _unresolved_ when no command is associated to it. For performance
    reasons the creation of a code lens and resolving should be done in two stages."""
    range: Range
    """The range in which this code lens is valid. Should only span a single line."""
    command: Command = field(metadata={"optional": True})
    """The command this code lens represents."""
    data: Any = field(metadata={"optional": True})
    """A data entry field that is preserved on a code lens item between
    a {@link CodeLensRequest} and a {@link CodeLensResolveRequest}"""

@dataclass
class CodeLensRegistrationOptions(TextDocumentRegistrationOptions, CodeLensOptions):
    """Registration options for a {@link CodeLensRequest}."""

@dataclass
class DocumentLinkParams:
    """The parameters of a {@link DocumentLinkRequest}."""
    textDocument: TextDocumentIdentifier
    """The document to provide document links for."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class DocumentLink:
    """A document link is a range in a text document that links to an internal or external resource, like another
    text document or a web site."""
    range: Range
    """The range this link applies to."""
    target: URI = field(metadata={"optional": True})
    """The uri this link points to. If missing a resolve request is sent later."""
    tooltip: str = field(metadata={"optional": True})
    """The tooltip text when you hover over this link.

    If a tooltip is provided, is will be displayed in a string that includes instructions on how to
    trigger the link, such as `{0} (ctrl + click)`. The specific instructions vary depending on OS,
    user settings, and localization.

    @since 3.15.0"""
    # since 3.15.0
    data: Any = field(metadata={"optional": True})
    """A data entry field that is preserved on a document link between a
    DocumentLinkRequest and a DocumentLinkResolveRequest."""

@dataclass
class DocumentLinkRegistrationOptions(TextDocumentRegistrationOptions, DocumentLinkOptions):
    """Registration options for a {@link DocumentLinkRequest}."""

@dataclass
class FormattingOptions:
    """Value-object describing what options formatting should use."""
    tabSize: int
    """Size of a tab in spaces."""
    insertSpaces: bool
    """Prefer spaces over tabs."""
    trimTrailingWhitespace: bool = field(metadata={"optional": True})
    """Trim trailing whitespace on a line.

    @since 3.15.0"""
    # since 3.15.0
    insertFinalNewline: bool = field(metadata={"optional": True})
    """Insert a newline character at the end of the file if one does not exist.

    @since 3.15.0"""
    # since 3.15.0
    trimFinalNewlines: bool = field(metadata={"optional": True})
    """Trim all newlines after the final newline at the end of the file.

    @since 3.15.0"""
    # since 3.15.0

@dataclass
class DocumentFormattingParams:
    """The parameters of a {@link DocumentFormattingRequest}."""
    textDocument: TextDocumentIdentifier
    """The document to format."""
    options: FormattingOptions
    """The format options."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class DocumentFormattingRegistrationOptions(TextDocumentRegistrationOptions, DocumentFormattingOptions):
    """Registration options for a {@link DocumentFormattingRequest}."""

@dataclass
class DocumentRangeFormattingParams:
    """The parameters of a {@link DocumentRangeFormattingRequest}."""
    textDocument: TextDocumentIdentifier
    """The document to format."""
    range: Range
    """The range to format"""
    options: FormattingOptions
    """The format options"""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class DocumentRangeFormattingRegistrationOptions(TextDocumentRegistrationOptions, DocumentRangeFormattingOptions):
    """Registration options for a {@link DocumentRangeFormattingRequest}."""

@dataclass
class DocumentRangesFormattingParams:
    """The parameters of a {@link DocumentRangesFormattingRequest}.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    textDocument: TextDocumentIdentifier
    """The document to format."""
    ranges: List[Range]
    """The ranges to format"""
    options: FormattingOptions
    """The format options"""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class DocumentOnTypeFormattingParams:
    """The parameters of a {@link DocumentOnTypeFormattingRequest}."""
    textDocument: TextDocumentIdentifier
    """The document to format."""
    position: Position
    """The position around which the on type formatting should happen.
    This is not necessarily the exact position where the character denoted
    by the property `ch` got typed."""
    ch: str
    """The character that has been typed that triggered the formatting
    on type request. That is not necessarily the last character that
    got inserted into the document since the client could auto insert
    characters as well (e.g. like automatic brace completion)."""
    options: FormattingOptions
    """The formatting options."""

@dataclass
class DocumentOnTypeFormattingRegistrationOptions(TextDocumentRegistrationOptions, DocumentOnTypeFormattingOptions):
    """Registration options for a {@link DocumentOnTypeFormattingRequest}."""

@dataclass
class RenameParams:
    """The parameters of a {@link RenameRequest}."""
    textDocument: TextDocumentIdentifier
    """The document to rename."""
    position: Position
    """The position at which this request was sent."""
    newName: str
    """The new name of the symbol. If the given name is not valid the
    request must return a {@link ResponseError} with an
    appropriate message set."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class RenameRegistrationOptions(TextDocumentRegistrationOptions, RenameOptions):
    """Registration options for a {@link RenameRequest}."""

@dataclass
class PrepareRenameParams(TextDocumentPositionParams):
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class ExecuteCommandParams:
    """The parameters of a {@link ExecuteCommandRequest}."""
    command: str
    """The identifier of the actual command handler."""
    arguments: List[Any] = field(metadata={"optional": True})
    """Arguments that the command should be invoked with."""
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class ExecuteCommandRegistrationOptions(ExecuteCommandOptions):
    """Registration options for a {@link ExecuteCommandRequest}."""

@dataclass
class WorkspaceEditMetadata:
    """Additional data about a workspace edit.

    @since 3.18.0
    @proposed"""
    # since 3.18.0
    isRefactoring: bool = field(metadata={"optional": True})
    """Signal to the editor that this edit is a refactoring."""

@dataclass
class ApplyWorkspaceEditParams:
    """The parameters passed via an apply workspace edit request."""
    label: str = field(metadata={"optional": True})
    """An optional label of the workspace edit. This label is
    presented in the user interface for example on an undo
    stack to undo the workspace edit."""
    edit: WorkspaceEdit
    """The edits to apply."""
    metadata: WorkspaceEditMetadata = field(metadata={"optional": True})
    """Additional data about the edit.

    @since 3.18.0
    @proposed"""
    # since 3.18.0

@dataclass
class ApplyWorkspaceEditResult:
    """The result returned from the apply workspace edit request.

    @since 3.17 renamed from ApplyWorkspaceEditResponse"""
    # since 3.17 renamed from ApplyWorkspaceEditResponse
    applied: bool
    """Indicates whether the edit was applied or not."""
    failureReason: str = field(metadata={"optional": True})
    """An optional textual description for why the edit was not applied.
    This may be used by the server for diagnostic logging or to provide
    a suitable error for a request that triggered the edit."""
    failedChange: int = field(metadata={"optional": True})
    """Depending on the client's failure handling strategy `failedChange` might
    contain the index of the change that failed. This property is only available
    if the client signals a `failureHandlingStrategy` in its client capabilities."""

@dataclass
class WorkDoneProgressBegin:
    kind: Literal['begin']
    title: str
    """Mandatory title of the progress operation. Used to briefly inform about
    the kind of operation being performed.

    Examples: "Indexing" or "Linking dependencies"."""
    cancellable: bool = field(metadata={"optional": True})
    """Controls if a cancel button should show to allow the user to cancel the
    long running operation. Clients that don't support cancellation are allowed
    to ignore the setting."""
    message: str = field(metadata={"optional": True})
    """Optional, more detailed associated progress message. Contains
    complementary information to the `title`.

    Examples: "3/25 files", "project/src/module2", "node_modules/some_dep".
    If unset, the previous progress message (if any) is still valid."""
    percentage: int = field(metadata={"optional": True})
    """Optional progress percentage to display (value 100 is considered 100%).
    If not provided infinite progress is assumed and clients are allowed
    to ignore the `percentage` value in subsequent in report notifications.

    The value should be steadily rising. Clients are free to ignore values
    that are not following this rule. The value range is [0, 100]."""

@dataclass
class WorkDoneProgressReport:
    kind: Literal['report']
    cancellable: bool = field(metadata={"optional": True})
    """Controls enablement state of a cancel button.

    Clients that don't support cancellation or don't support controlling the button's
    enablement state are allowed to ignore the property."""
    message: str = field(metadata={"optional": True})
    """Optional, more detailed associated progress message. Contains
    complementary information to the `title`.

    Examples: "3/25 files", "project/src/module2", "node_modules/some_dep".
    If unset, the previous progress message (if any) is still valid."""
    percentage: int = field(metadata={"optional": True})
    """Optional progress percentage to display (value 100 is considered 100%).
    If not provided infinite progress is assumed and clients are allowed
    to ignore the `percentage` value in subsequent in report notifications.

    The value should be steadily rising. Clients are free to ignore values
    that are not following this rule. The value range is [0, 100]"""

@dataclass
class WorkDoneProgressEnd:
    kind: Literal['end']
    message: str = field(metadata={"optional": True})
    """Optional, a final message indicating to for example indicate the outcome
    of the operation."""

@dataclass
class SetTraceParams:
    value: TraceValue

@dataclass
class LogTraceParams:
    message: str
    verbose: str = field(metadata={"optional": True})

@dataclass
class CancelParams:
    id: Union[int, str]
    """The request id to cancel."""

@dataclass
class ProgressParams:
    token: ProgressToken
    """The progress token provided by the client or server."""
    value: Any
    """The progress data."""

@dataclass
class WorkDoneProgressParams:
    workDoneToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report work done progress."""

@dataclass
class PartialResultParams:
    partialResultToken: ProgressToken = field(metadata={"optional": True})
    """An optional token that a server can use to report partial results (e.g. streaming) to
    the client."""

@dataclass
class LocationLink:
    """Represents the connection of two locations. Provides additional metadata over normal {@link Location locations},
    including an origin range."""
    originSelectionRange: Range = field(metadata={"optional": True})
    """Span of the origin of this link.

    Used as the underlined span for mouse interaction. Defaults to the word range at
    the definition position."""
    targetUri: DocumentUri
    """The target resource identifier of this link."""
    targetRange: Range
    """The full target range of this link. If the target for example is a symbol then target range is the
    range enclosing this symbol not including leading/trailing whitespace but everything else
    like comments. This information is typically used to highlight the range in the editor."""
    targetSelectionRange: Range
    """The range that should be selected and revealed when this link is being followed, e.g the name of a function.
    Must be contained by the `targetRange`. See also `DocumentSymbol#range`"""

@dataclass
class StaticRegistrationOptions:
    """Static registration options to be returned in the initialize
    request."""
    id: str = field(metadata={"optional": True})
    """The id used to register the request. The id can be used to deregister
    the request again. See also Registration#id."""

@dataclass
class InlineValueText:
    """Provide inline value as text.

    @since 3.17.0"""
    # since 3.17.0
    range: Range
    """The document range for which the inline value applies."""
    text: str
    """The text of the inline value."""

@dataclass
class InlineValueVariableLookup:
    """Provide inline value through a variable lookup.
    If only a range is specified, the variable name will be extracted from the underlying document.
    An optional variable name can be used to override the extracted name.

    @since 3.17.0"""
    # since 3.17.0
    range: Range
    """The document range for which the inline value applies.
    The range is used to extract the variable name from the underlying document."""
    variableName: str = field(metadata={"optional": True})
    """If specified the name of the variable to look up."""
    caseSensitiveLookup: bool
    """How to perform the lookup."""

@dataclass
class InlineValueEvaluatableExpression:
    """Provide an inline value through an expression evaluation.
    If only a range is specified, the expression will be extracted from the underlying document.
    An optional expression can be used to override the extracted expression.

    @since 3.17.0"""
    # since 3.17.0
    range: Range
    """The document range for which the inline value applies.
    The range is used to extract the evaluatable expression from the underlying document."""
    expression: str = field(metadata={"optional": True})
    """If specified the expression overrides the extracted expression."""

@dataclass
class RelatedFullDocumentDiagnosticReport(FullDocumentDiagnosticReport):
    """A full diagnostic report with a set of related documents.

    @since 3.17.0"""
    # since 3.17.0
    relatedDocuments: Dict[DocumentUri, Union[FullDocumentDiagnosticReport, UnchangedDocumentDiagnosticReport]] = field(metadata={"optional": True})
    """Diagnostics of related documents. This information is useful
    in programming languages where code in a file A can generate
    diagnostics in a file B which A depends on. An example of
    such a language is C/C++ where marco definitions in a file
    a.cpp and result in errors in a header file b.hpp.

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class RelatedUnchangedDocumentDiagnosticReport(UnchangedDocumentDiagnosticReport):
    """An unchanged diagnostic report with a set of related documents.

    @since 3.17.0"""
    # since 3.17.0
    relatedDocuments: Dict[DocumentUri, Union[FullDocumentDiagnosticReport, UnchangedDocumentDiagnosticReport]] = field(metadata={"optional": True})
    """Diagnostics of related documents. This information is useful
    in programming languages where code in a file A can generate
    diagnostics in a file B which A depends on. An example of
    such a language is C/C++ where marco definitions in a file
    a.cpp and result in errors in a header file b.hpp.

    @since 3.17.0"""
    # since 3.17.0

@dataclass
class PrepareRenamePlaceholder:
    """@since 3.18.0"""
    # since 3.18.0
    range: Range
    placeholder: str

@dataclass
class PrepareRenameDefaultBehavior:
    """@since 3.18.0"""
    # since 3.18.0
    defaultBehavior: bool

Definition: TypeAlias = Union[Location, List[Location]]
"""The definition of a symbol represented as one or many {@link Location locations}.
For most programming languages there is only one location at which a symbol is
defined.

Servers should prefer returning `DefinitionLink` over `Definition` if supported
by the client."""

DefinitionLink: TypeAlias = LocationLink
"""Information about where a symbol is defined.

Provides additional metadata over normal {@link Location location} definitions, including the range of
the defining symbol"""

LSPArray: TypeAlias = List[Any]
"""LSP arrays.
@since 3.17.0"""
# since 3.17.0

LSPAny: TypeAlias = Union[LSPObject, LSPArray, str, int, int, float, bool, None]
"""The LSP any type.
Please note that strictly speaking a property with the value `undefined`
can't be converted into JSON preserving the property name. However for
convenience it is allowed and assumed that all these properties are
optional as well.
@since 3.17.0"""
# since 3.17.0

Declaration: TypeAlias = Union[Location, List[Location]]
"""The declaration of a symbol representation as one or many {@link Location locations}."""

DeclarationLink: TypeAlias = LocationLink
"""Information about where a symbol is declared.

Provides additional metadata over normal {@link Location location} declarations, including the range of
the declaring symbol.

Servers should prefer returning `DeclarationLink` over `Declaration` if supported
by the client."""

InlineValue: TypeAlias = Union[InlineValueText, InlineValueVariableLookup, InlineValueEvaluatableExpression]
"""Inline value information can be provided by different means:
- directly as a text value (class InlineValueText).
- as a name to use for a variable lookup (class InlineValueVariableLookup)
- as an evaluatable expression (class InlineValueEvaluatableExpression)
The InlineValue types combines all inline value types into one type.

@since 3.17.0"""
# since 3.17.0

DocumentDiagnosticReport: TypeAlias = Union[RelatedFullDocumentDiagnosticReport, RelatedUnchangedDocumentDiagnosticReport]
"""The result of a document diagnostic pull request. A report can
either be a full report containing all diagnostics for the
requested document or an unchanged report indicating that nothing
has changed in terms of diagnostics in comparison to the last
pull request.

@since 3.17.0"""
# since 3.17.0

PrepareRenameResult: TypeAlias = Union[Range, PrepareRenamePlaceholder, PrepareRenameDefaultBehavior]