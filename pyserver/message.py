"""JSON-RPC Message"""

from json import loads, dumps
from typing import Union, Any


class JSONDict(dict):
    """Dict like object"""

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def __getattr__(self, name: str) -> Any:
        return self[name]

    def __delattr__(self, name: str) -> None:
        del self[name]


def loads_rpc2(data: Union[str, bytes]) -> JSONDict:
    dct = loads(data, object_hook=JSONDict)
    if (rpc_version := dct.pop("jsonrpc", "1.0")) and rpc_version != "2.0":
        raise ValueError("expected jsonrpc version 2.0")
    return dct


def dumps_rpc2(message: dict, as_bytes: bool = False) -> Union[str, bytes]:
    temp = JSONDict(message)
    temp["jsonrpc"] = "2.0"
    if as_bytes:
        return dumps(temp).encode("utf-8")
    return dumps(temp)
