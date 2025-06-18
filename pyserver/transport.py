"""transport handler"""

import re
import sys
from abc import ABC, abstractmethod
from functools import lru_cache
from io import BytesIO

SEPARATOR = b"\r\n"


class HeaderError(ValueError):
    """header error"""


def wrap_content(content: bytes) -> bytes:
    """wrap content"""
    header = b"Content-Length: %d\r\n" % len(content)
    return b"%s%s%s" % (header, SEPARATOR, content)


@lru_cache(maxsize=512)
def get_content_length(header: bytes) -> int:
    for line in header.splitlines():
        if match := re.match(rb"Content-Length: (\d+)", line):
            return int(match.group(1))

    raise HeaderError("unable get 'Content-Length'")


class Transport(ABC):
    """transport abstraction"""

    @abstractmethod
    def listen_connection(self) -> None:
        """wait client connection"""

    @abstractmethod
    def terminate(self) -> None:
        """terminate from client"""

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

    def listen_connection(self):
        # just wait until terminated
        pass

    def terminate(self) -> None:
        """terminate"""
        pass

    def write(self, data: bytes):
        buffer = sys.stdout.buffer
        buffer.write(wrap_content(data))
        buffer.flush()

    def read(self):
        buffer = sys.stdin.buffer

        headers_buffer = BytesIO()
        while line := buffer.readline():
            if line == SEPARATOR:
                break
            headers_buffer.write(line)

        # no header received
        if not headers_buffer.getvalue():
            raise EOFError("stdin closed")

        content_length = get_content_length(headers_buffer.getvalue())
        # read() is blocking until content_length satisfied
        return buffer.read(content_length)
