from dataclasses import dataclass
from collections import namedtuple
from typing import Optional, Any

TextRange = namedtuple("TextRange", ["start", "end"])


KIND_ERROR = 1
KIND_WARNING = 2


@dataclass
class Diagnostic:
    """Diagnostic item"""

    text_range: TextRange
    severity: int
    code: str
    message: str
    source: str
    data: Optional[Any] = None
