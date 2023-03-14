"""services module"""

from dataclasses import dataclass
from typing import Any, Dict, Protocol, runtime_checkable


@dataclass
class Params:
    """service params object"""


@runtime_checkable
class Services(Protocol):
    """Services protocol

    All services must implement this protocol
    """

    def __init__(self, params: Params):
        pass

    def execute(self) -> Any:
        """execute service"""
        pass

    def get_result(self) -> Dict[str, Any]:
        """get result as rpc format"""
        pass
