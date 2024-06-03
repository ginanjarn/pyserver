"""transport handler"""

import re
import sys
from abc import ABC, abstractmethod
from functools import lru_cache
from io import BytesIO


class HeaderError(ValueError):
    """header error"""


def wrap_rpc(content: bytes) -> bytes:
    """wrap content as rpc body"""
    header = b"Content-Length: %d\r\n" % len(content)
    return b"%s\r\n%s" % (header, content)


@lru_cache(maxsize=512)
def get_content_length(header: bytes) -> int:
    for line in header.splitlines():
        if match := re.match(rb"Content-Length: (\d+)", line):
            return int(match.group(1))

    raise HeaderError("unable get 'Content-Length'")


class Transport(ABC):
    """transport abstraction"""

    @abstractmethod
    def listen(self) -> None:
        """listen client message"""

    @abstractmethod
    def terminate(self) -> None:
        """terminate"""

    @abstractmethod
    def write(self, data: bytes) -> None:
        """write data to client"""

    @abstractmethod
    def read(self) -> bytes:
        """read data from client"""


class StandardIO(Transport):
    """StandardIO Transport implementation"""

    def __init__(self):
        pass

    def listen(self):
        # just wait until terminated
        pass

    def terminate(self):
        """terminate"""
        sys.exit(0)

    def write(self, data: bytes):
        prepared_data = wrap_rpc(data)
        sys.stdout.buffer.write(prepared_data)
        sys.stdout.buffer.flush()

    def read(self):
        # get header
        headers_buffer = BytesIO()
        while line := sys.stdin.buffer.readline():
            # header and content separated by newline with \r\n
            if line == b"\r\n":
                break

            headers_buffer.write(line)

        # no header received
        if not headers_buffer.getvalue():
            raise EOFError("stdin closed")

        content_length = get_content_length(headers_buffer.getvalue())

        # the read() function will block until specified content_length satisfied
        return sys.stdin.buffer.read(content_length)
