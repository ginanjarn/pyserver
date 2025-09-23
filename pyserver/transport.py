"""transport handler"""

import sys
from abc import ABC, abstractmethod
from io import BytesIO

CONTENT_SEPARATOR = b"\r\n"


class HeaderError(ValueError):
    """header error"""


def wrap_content(content: bytes) -> bytes:
    """wrap content"""
    header = b"Content-Length: %d\r\n" % len(content)
    return b"%s%s%s" % (header, CONTENT_SEPARATOR, content)


def get_content_length(header: bytes) -> int:
    for line in header.splitlines(keepends=False):
        if line[:16] == b"Content-Length: ":
            return int(line[16:])

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
        self.stdin_buffer = sys.stdin.buffer
        self.stdout_buffer = sys.stdout.buffer

    def listen_connection(self):
        # just wait until terminated
        pass

    def terminate(self) -> None:
        """terminate"""
        pass

    def write(self, data: bytes):
        self.stdout_buffer.write(wrap_content(data))
        self.stdout_buffer.flush()

    def read(self):
        headers_buffer = BytesIO()
        while line := self.stdin_buffer.readline():
            if line == CONTENT_SEPARATOR:
                break
            headers_buffer.write(line)

        # no header received
        if not headers_buffer.getvalue():
            raise EOFError("stdin closed")

        content_length = get_content_length(headers_buffer.getvalue())
        # read() is blocking until content_length satisfied
        return self.stdin_buffer.read(content_length)
