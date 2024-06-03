"""message handler"""

__all__ = ["RPCMessage"]

import json
from typing import Any, Optional
from pyserver.errors import ParseError


class RPCMessage:
    """rpc message"""

    JSONRPC_VERSION = "2.0"
    CONTENT_ENCODING = "utf-8"

    __slots__ = ["data"]

    def __init__(self, data: dict):
        if not isinstance(data, dict):
            raise TypeError("message type must <class 'dict'>")

        self.data = data
        # set jsonrpc version
        self.data["jsonrpc"] = self.JSONRPC_VERSION

    def __repr__(self):
        return f"RPCMessage({self.data})"

    def get(self, key: str) -> None:
        """get data

        Returns:
            Any data or None if key not found
        """
        return self.data.get(key)

    def set(self, key: str, value: Any):
        self.data.set(key, value)

    def to_bytes(self) -> bytes:
        """serialize data to bytes"""

        message_str = json.dumps(self.data)
        message_encoded = message_str.encode(self.CONTENT_ENCODING)
        return message_encoded

    @classmethod
    def from_bytes(cls, b: bytes, /):
        """create from bytes"""

        try:
            message_str = b.decode(cls.CONTENT_ENCODING)
            message = json.loads(message_str)

            if message["jsonrpc"] != cls.JSONRPC_VERSION:
                raise ValueError("invalid jsonrpc version")

        except Exception as err:
            raise ParseError(err) from err
        else:
            return cls(message)

    @classmethod
    def notification(cls, method: str, params: Any):
        """create notification message"""
        return cls({"method": method, "params": params})

    @classmethod
    def request(cls, id_: int, method: str, params: Any):
        """create request message"""
        return cls({"id": id_, "method": method, "params": params})

    @classmethod
    def response(
        cls, id_: int, result: Optional[dict] = None, error: Optional[dict] = None
    ):
        """create response message"""
        if error:
            return cls({"id": id_, "error": error})
        return cls({"id": id_, "result": result})
