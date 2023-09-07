"""message handler"""

__all__ = ["RPCMessage"]

import json
from pyserver.errors import ParseError


class RPCMessage:
    """rpc message"""

    JSONRPC_VERSION = "2.0"
    CONTENT_ENCODING = "utf-8"

    def __init__(self, message: dict):
        if not isinstance(message, dict):
            raise TypeError("message type must <class 'dict'>")

        self.message = message
        # set jsonrpc version
        self.message["jsonrpc"] = self.JSONRPC_VERSION

    def __repr__(self):
        return f"RPCMessage({self.message})"

    def get(self, key: str):
        return self.message.get(key)

    def set(self, key, value):
        self.message.set(key, value)

    def to_bytes(self) -> bytes:
        message_str = json.dumps(self.message)
        message_encoded = message_str.encode(self.CONTENT_ENCODING)
        return message_encoded

    @classmethod
    def from_bytes(cls, b: bytes, /):
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
    def notification(cls, method, params):
        return cls({"method": method, "params": params})

    @classmethod
    def request(cls, id_, method, params):
        return cls({"id": id_, "method": method, "params": params})

    @classmethod
    def response(cls, id_, result=None, error=None):
        if error:
            return cls({"id": id_, "error": error})
        return cls({"id": id_, "result": result})
