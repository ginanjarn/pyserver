"""transport handler"""

import re
import sys
from abc import ABC, abstractmethod
from functools import lru_cache
from io import BytesIO


class HeaderError(ValueError):
    """header error"""


@lru_cache(maxsize=512)
def get_content_length(header: bytes) -> int:
    for line in header.splitlines():
        if match := re.match(rb"Content-Length: (\d+)", line):
            return int(match.group(1))

    raise HeaderError("unable get 'Content-Length'")


class Protocol:
    """Tranfer protocol"""

    separator = b"\r\n"

    @staticmethod
    def dumps(content: bytes) -> bytes:
        header = b"Content-Length: %d\r\n" % len(content)
        return b"%s%s%s" % (header, Protocol.separator, content)

    @staticmethod
    def loads(stream: BytesIO) -> bytes:
        # get header
        headers_buffer = BytesIO()
        while line := stream.readline():
            # header and content separated by newline with \r\n
            if line == Protocol.separator:
                break

            headers_buffer.write(line)

        # no header received
        if not headers_buffer.getvalue():
            raise EOFError("stream closed")

        content_length = get_content_length(headers_buffer.getvalue())

        # the read() function will block until specified content_length satisfied
        return stream.read(content_length)


class Transport(ABC):
    """transport abstraction"""

    @abstractmethod
    def listen_connection(self) -> None:
        """wait client connection"""

    @abstractmethod
    def terminate(self, exit_code: int = 0) -> None:
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

    def terminate(self, exit_code: int = 0) -> None:
        """terminate"""
        sys.exit(exit_code)

    def write(self, data: bytes):
        prepared_data = Protocol.dumps(data)
        sys.stdout.buffer.write(prepared_data)
        sys.stdout.buffer.flush()

    def read(self):
        return Protocol.loads(sys.stdin.buffer)
