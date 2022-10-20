"""transport handler"""

import logging
import queue
import re
import socket
import sys
import threading
from abc import ABC, abstractmethod
from typing import Iterator

from pyserver.message import RPCMessage
from pyserver.errors import ParseError, ContentIncomplete

LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)  # module logging level
STREAM_HANDLER = logging.StreamHandler()
LOG_TEMPLATE = "%(levelname)s %(asctime)s %(filename)s:%(lineno)s  %(message)s"
STREAM_HANDLER.setFormatter(logging.Formatter(LOG_TEMPLATE))
LOGGER.addHandler(STREAM_HANDLER)


class AbstractTransport(ABC):
    """abstract transport"""

    @abstractmethod
    def get_channel(self) -> queue.Queue:
        """transport channel"""

    @abstractmethod
    def send_message(self, message: RPCMessage):
        """send message"""

    @abstractmethod
    def listen(self):
        """listen server message"""

    @abstractmethod
    def terminate(self):
        """terminate"""


class Stream:
    r"""stream object

    This class handle JSONRPC stream format
        '<header>\r\n<content>'
    
    Header items must seperated by '\r\n'
    """

    HEADER_ENCODING = "ascii"

    def __init__(self, content: bytes = b""):
        self.buffer = [content] if content else []
        self._lock = threading.Lock()

    def put(self, data: bytes) -> None:
        """put stream data"""
        with self._lock:
            self.buffer.append(data)

    _content_length_pattern = re.compile(r"^Content-Length: (\d+)", flags=re.MULTILINE)

    def _get_content_length(self, headers: bytes) -> int:
        """get Content-Length"""

        if found := self._content_length_pattern.search(
            headers.decode(self.HEADER_ENCODING)
        ):
            return int(found.group(1))
        raise ValueError("unable find Content-Length")

    def get_contents(self) -> Iterator[bytes]:
        """get contents

        Yield
        ------
        content: bytes

        Raises:
        -------
        ParseError
        EOFError
        ContentIncomplete
        """

        def get_content():
            buffers = b"".join(self.buffer)
            separator = b"\r\n\r\n"

            if not buffers:
                raise EOFError("buffer empty")

            try:
                header_end = buffers.index(separator)
                content_length = self._get_content_length(buffers[:header_end])

            except ValueError as err:
                # clean up buffer
                self.buffer = []

                LOGGER.debug("buffer: %s", buffers)
                raise ParseError(f"header error: {err!r}") from err

            start_index = header_end + len(separator)
            end_index = start_index + content_length
            content = buffers[start_index:end_index]
            recv_len = len(content)

            if recv_len < content_length:
                raise ContentIncomplete(f"want: {content_length}, expected: {recv_len}")

            # replace buffer
            self.buffer = [buffers[end_index:]]
            return content

        with self._lock:
            while True:
                try:
                    content = get_content()
                except (EOFError, ContentIncomplete):
                    break
                except Exception as err:
                    LOGGER.error(err)
                    # clean up buffer
                    self.buffer = []
                    break
                else:
                    yield content

    @staticmethod
    def wrap_content(content: bytes):
        header = f"Content-Length: {len(content)}"
        return b"\r\n\r\n".join([header.encode(Stream.HEADER_ENCODING), content])


class TCPIO(AbstractTransport):
    """TCPIO Transport implementation"""

    BUFFER_LENGTH = 4096
    DEFAULT_ADDRESS = ("localhost", 9825)
    DEFAULT_TIMEOUT = 60

    def __init__(self, timeout=None):

        # set default queue
        self._channel = queue.Queue()

        self.address = self.DEFAULT_ADDRESS
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None

        self.timeout = timeout
        if timeout is None or timeout < 0:
            self.timeout = self.DEFAULT_TIMEOUT
        self._sock.settimeout(self.timeout)

    def get_channel(self) -> queue.Queue:
        return self._channel

    def send_message(self, message: RPCMessage):
        LOGGER.debug(f"Send >> {message}")

        bmessage = Stream.wrap_content(message.to_bytes())
        self.conn.sendall(bmessage)

    def _listen_socket(self):
        """listen stdout task"""

        while True:
            buf = self.conn.recv(self.BUFFER_LENGTH)
            self._channel.put(buf)
            LOGGER.debug(f"buf: {buf}")

            if not buf:
                LOGGER.debug("connection closed")
                return

    def listen(self):
        """listen PIPE"""
        LOGGER.info("listen")

        try:
            self._sock.bind(self.address)
            self._sock.listen()
            print(f"listening connection at '{self.address[0]}:{self.address[1]}'")

            self.conn, addr = self._sock.accept()
            LOGGER.info(f"accept connection from {addr}")

            self._listen_socket()

        except ConnectionError as err:
            LOGGER.debug(err)

        except socket.timeout:
            print(f"no connection at {self.timeout} second(s).\nexit...")
            sys.exit(0)

    def terminate(self):
        """terminate process"""
        LOGGER.info("terminate")

        if self.conn:
            self.conn.close()

        self._sock.close()
        sys.exit(0)
