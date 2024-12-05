"""message handler"""

__all__ = ["RPCMessage"]

import json
from typing import Optional, Union
from pyserver.errors import ParseError

MethodName = str


class RPCMessage(dict):
    """rpc message"""

    @classmethod
    def request(cls, id: int, method: MethodName, params: dict):
        return cls({"id": id, "method": method, "params": params})

    @classmethod
    def notification(cls, method: MethodName, params: dict):
        return cls({"method": method, "params": params})

    @classmethod
    def response(
        cls, id: int, result: Optional[dict] = None, error: Optional[dict] = None
    ):
        if error:
            return cls({"id": id, "error": error})
        return cls({"id": id, "result": result})

    def dumps(self, *, as_bytes: bool = False) -> Union[str, bytes]:
        """dump rpc message to json text"""

        self["jsonrpc"] = "2.0"
        dumped = json.dumps(self)
        if as_bytes:
            return dumped.encode()
        return dumped

    @classmethod
    def loads(cls, data: Union[str, bytes]) -> "RPCMessage":
        """load rpc message from json text"""

        try:
            loaded = json.loads(data)
        except json.JSONDecoder as err:
            raise ParseError(err) from err

        if loaded.get("jsonrpc") != "2.0":
            raise ValueError("JSON-RPC v2.0 is required")
        return cls(loaded)
