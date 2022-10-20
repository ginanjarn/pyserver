"""services module"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Params:
    """service params object"""


class Services(ABC):
    """Services abstraction

    All services must inherit this interface
    """

    @abstractmethod
    def __init__(self, params: Params):
        pass

    @abstractmethod
    def execute(self) -> Any:
        """execute service"""
        pass

    @abstractmethod
    def get_result(self) -> Dict[str, Any]:
        """get result as rpc format"""
        pass
