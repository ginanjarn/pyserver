"""message handler"""

import json
from functools import lru_cache
from urllib.parse import urlparse, urlunparse, quote, unquote
from urllib.request import pathname2url, url2pathname

from pyserver.errors import ParseError


class RPCMessage(dict):
    """rpc message"""

    JSONRPC_VERSION = "2.0"
    CONTENT_ENCODING = "utf-8"

    def __init__(self, mapping=None, **kwargs):
        super().__init__(kwargs)
        if mapping:
            self.update(mapping)
        # set jsonrpc version
        self["jsonrpc"] = self.JSONRPC_VERSION

    @classmethod
    def from_str(cls, s: str, /):
        return cls(json.loads(s))

    def to_bytes(self) -> bytes:
        message_str = json.dumps(self)
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


class DocumentURI(str):
    """document uri"""

    @classmethod
    def from_path(cls, file_name):
        """from file name"""
        return cls(
            urlunparse(("file", "", quote(pathname2url(str(file_name))), "", "", ""))
        )

    def to_path(self) -> str:
        """convert to path"""
        return url2pathname(unquote(urlparse(self).path))


@lru_cache(128)
def path_to_uri(path: str):
    return DocumentURI.from_path(path)


@lru_cache(128)
def uri_to_path(uri: str):
    return DocumentURI(uri).to_path()
