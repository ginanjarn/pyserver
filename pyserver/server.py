from .base_server import BaseServer

from .features.initialize_mixin import InitializeMixin
from .features.text_document.completion_mixin import DocumentCompletionMixin
from .features.text_document.definition_mixin import DocumentDefinitionMixin
from .features.text_document.diagnostic_mixin import DocumentDiagnosticMixin
from .features.text_document.formatting_mixin import DocumentFormattingMixin
from .features.text_document.hover_mixin import DocumentHoverMixin
from .features.text_document.prepare_rename_mixin import DocumentPepareRenameMixin
from .features.text_document.rename_mixin import DocumentRenameMixin
from .features.text_document.signature_help_mixin import DocumentSignatureHelpMixin
from .features.text_document.symbol_mixin import DocumentSymbolMixin
from .features.text_document.synchronization_mixin import DocumentSynchronizationMixin


class Server(
    InitializeMixin,
    DocumentCompletionMixin,
    DocumentDefinitionMixin,
    DocumentDiagnosticMixin,
    DocumentFormattingMixin,
    DocumentHoverMixin,
    DocumentPepareRenameMixin,
    DocumentRenameMixin,
    DocumentSignatureHelpMixin,
    DocumentSymbolMixin,
    DocumentSynchronizationMixin,
    BaseServer,
):
    """Server implementation"""
