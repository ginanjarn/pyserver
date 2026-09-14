from dataclasses import dataclass
from collections import namedtuple

TextRange = namedtuple("TextRange", ["start", "end"])


KIND_ERROR = 1
KIND_WARNING = 2


@dataclass
class Diagnostic:
    """Diagnostic item"""

    severity: int
    file_name: str
    text_range: TextRange
    message: str
    source: str
