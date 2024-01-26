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

    @property
    def stdin(self):
        return sys.stdin.buffer

    @property
    def stdout(self):
        return sys.stdout.buffer

    def terminate(self):
        """terminate"""
        sys.exit(0)

    def write(self, data: bytes):
        prepared_data = wrap_rpc(data)
        self.stdout.write(prepared_data)
        self.stdout.flush()

    def read(self):
        # get header
        temp_header = BytesIO()
        n_header = 0
        while line := self.stdin.readline():
            # header and content separated by newline with \r\n
            if line == b"\r\n":
                break

            n = temp_header.write(line)
            n_header += n

        # no header received
        if not n_header:
            raise EOFError("stdin closed")

        try:
            content_length = get_content_length(temp_header.getvalue())

        except HeaderError as err:
            raise err

        # in some case where received content less than content_length
        temp_content = BytesIO()
        n_content = 0
        while True:
            if n_content < content_length:
                unread_length = content_length - n_content
                if chunk := self.stdin.read(unread_length):
                    n = temp_content.write(chunk)
                    n_content += n
                else:
                    raise EOFError("stdin closed")
            else:
                break

        content = temp_content.getvalue()
        return content
