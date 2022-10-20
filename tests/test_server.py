"""server test"""

import json
import logging
import os
import queue
import re
import subprocess
import sys
import threading
from abc import ABC, abstractmethod
from typing import List, Optional, Any
from urllib.parse import urlparse, urlunparse, quote, unquote
from urllib.request import pathname2url, url2pathname

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)  # module logging level
STREAM_HANDLER = logging.StreamHandler()
LOG_TEMPLATE = "%(levelname)s %(asctime)s %(filename)s:%(lineno)s  %(message)s"
STREAM_HANDLER.setFormatter(logging.Formatter(LOG_TEMPLATE))
LOGGER.addHandler(STREAM_HANDLER)


class InvalidMessage(ValueError):
    """message not comply to jsonrpc 2.0 specification"""


class ContentIncomplete(ValueError):
    """expected size less than defined"""


class ServerOffline(Exception):
    """server offline"""


class DocumentURI(str):
    """document uri"""

    @classmethod
    def from_path(cls, file_name):
        """from file name"""
        return cls(urlunparse(("file", "", quote(pathname2url(file_name)), "", "", "")))

    def to_path(self) -> str:
        """convert to path"""
        return url2pathname(unquote(urlparse(self).path))


def path_to_uri(path: str):
    return DocumentURI.from_path(path)


def uri_to_path(uri: str):
    return DocumentURI(uri).to_path()


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
            raise InvalidMessage(err) from err
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

    def get_content(self) -> bytes:
        """read stream data

        Returns
        ------
        content: bytes

        Raises:
        -------
        InvalidMessage
        EOFError
        ContentIncomplete
        """

        with self._lock:

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

                LOGGER.error(err)
                LOGGER.debug("buffer: %s", buffers)
                raise InvalidMessage(f"header error: {repr(err)}") from err

            start_index = header_end + len(separator)
            end_index = start_index + content_length
            content = buffers[start_index:end_index]
            recv_len = len(content)

            if recv_len < content_length:
                raise ContentIncomplete(f"want: {content_length}, expected: {recv_len}")

            # replace buffer
            self.buffer = [buffers[end_index:]]
            return content

    @staticmethod
    def wrap_content(content: bytes):
        header = f"Content-Length: {len(content)}"
        return b"\r\n\r\n".join([header.encode(Stream.HEADER_ENCODING), content])


class AbstractTransport(ABC):
    """abstract transport"""

    @abstractmethod
    def run_server(self):
        """run server"""

    @abstractmethod
    def is_running(self):
        """check if server is running"""

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


class StandardIO(AbstractTransport):
    """standard io Transport implementation"""

    BUFFER_LENGTH = 4096

    def __init__(
        self, executable: str, arguments: List[str], *, env: Optional[dict] = None
    ):

        self.server_command = [executable]
        if arguments:
            self.server_command.extend(arguments)
        self.env = env

        self.server_process: subprocess.Popen = None

        # set default queue
        self._channel = queue.Queue()

    def get_channel(self) -> queue.Queue:
        return self._channel

    def run_server(self):
        LOGGER.info("run_server")

        command = self.server_command
        startupinfo = None

        if os.name == "nt":
            # if on Windows, hide process window
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.SW_HIDE | subprocess.STARTF_USESHOWWINDOW

        LOGGER.debug("command: %s", command)
        try:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=self.env,
                bufsize=0,  # no buffering
                startupinfo=startupinfo,
            )
        except FileNotFoundError as err:
            raise FileNotFoundError(f"'{command[0]}' not found in PATH") from err
        except Exception as err:
            raise Exception(f"run server error: {err}") from err

        # listen server message
        self.server_process = process
        self.listen()

    def is_running(self):
        """check if server is running"""

        if not self.server_process:
            return False
        if self.server_process.poll() is None:
            return True

        return True

    def send_message(self, message: RPCMessage):
        LOGGER.debug(f"Send >> {message}")

        if self.server_process is None:
            raise ServerOffline("server not started")

        bmessage = Stream.wrap_content(message.to_bytes())
        try:
            self.server_process.stdin.write(bmessage)
            self.server_process.stdin.flush()

        except OSError as err:
            raise ServerOffline("server has terminated") from err

    def _listen_stdout(self):
        """listen stdout task"""

        while True:
            buf = self.server_process.stdout.read(self.BUFFER_LENGTH)
            self._channel.put(buf)

            if not buf:
                LOGGER.debug("stdout closed")
                return

    def _listen_stderr(self):
        """listen stderr task"""

        while True:
            if buf := self.server_process.stderr.readline(self.BUFFER_LENGTH):
                print(buf.decode())
            else:
                LOGGER.debug("stderr closed")
                return

    def listen(self):
        """listen PIPE"""
        LOGGER.info("listen")

        stdout_thread = threading.Thread(target=self._listen_stdout, daemon=True)
        stderr_thread = threading.Thread(target=self._listen_stderr, daemon=True)
        stdout_thread.start()
        stderr_thread.start()

    def terminate(self):
        """terminate process"""
        LOGGER.info("terminate")

        if self.is_running():
            self.server_process.terminate()


import socket


class TCPIO(AbstractTransport):
    """TCP io Transport implementation"""

    BUFFER_LENGTH = 4096
    DEFAULT_ADDRESS = ("localhost", 9825)

    def __init__(self):

        # set default queue
        self._channel = queue.Queue()

        self.conn: socket.socket = None
        self._is_connected = False

    def get_channel(self) -> queue.Queue:
        return self._channel

    def is_running(self):
        """check if server is running"""
        return self._is_connected

    def run_server(self):
        """run server"""
        threading.Thread(target=self.listen, daemon=True).start()
        # self.listen()

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
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect(self.DEFAULT_ADDRESS)
            self._is_connected = True
            self._listen_socket()

        except ConnectionError as err:
            LOGGER.debug(err)
            self._is_connected = False

    def terminate(self):
        """terminate process"""
        LOGGER.info("terminate")
        if self.conn:
            self.conn.close()


class Client:
    def __init__(self):
        self.client = self.get_running_client()

    def get_client(self):
        # return StandardIO("python", ["-m", "pyserver"])
        return TCPIO()

    def get_running_client(self):
        client = self.get_client()
        client.run_server()
        return client

    def notify(self, method: Any, params: Any):
        self.client.send_message(RPCMessage.notification(method, params))

    def request(self, id_: int, method: Any, params: Any):
        self.client.send_message(RPCMessage.request(id_, method, params))

    def cancel_request(self, id_: int):
        self.notify("$/cancelRequest", {"id": id_})
