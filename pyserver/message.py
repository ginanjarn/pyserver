"""message handler"""

__all__ = ["Message", "Notification", "Request", "Response", "loads", "dumps"]

import json
from dataclasses import dataclass, asdict
from typing import Union, Optional

MethodName = str


@dataclass
class Message:
    """JSON-RPC Message interface"""


@dataclass
class Notification(Message):
    method: MethodName
    params: Union[dict, list]


@dataclass
class Request(Message):
    id: int
    method: MethodName
    params: Union[dict, list]


@dataclass
class Response(Message):
    id: int
    result: Optional[Union[dict, list]] = None
    error: Optional[dict] = None


def loads(json_str: Union[str, bytes]) -> Message:
    """loads json-rpc message"""

    dct = json.loads(json_str)
    try:
        if (jsonrpc_version := dct.pop("jsonrpc")) and jsonrpc_version != "2.0":
            raise ValueError("invalid jsonrpc version")
    except KeyError as err:
        raise ValueError("JSON-RPC 2.0 is required") from err

    if dct.get("method"):
        if (id := dct.get("id")) and id is not None:
            return Request(**dct)
        return Notification(**dct)
    return Response(**dct)


def dumps(message: Message, as_bytes: bool = False) -> Union[str, bytes]:
    """dumps json-rpc message"""

    dct = asdict(message)
    dct["jsonrpc"] = "2.0"

    if isinstance(message, Response):
        if message.error is None:
            del dct["error"]
        else:
            del dct["result"]

    json_str = json.dumps(dct)
    if as_bytes:
        return json_str.encode()
    return json_str
