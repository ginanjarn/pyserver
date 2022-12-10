"""transport handler"""

import logging
import socket
import sys
import threading
from abc import ABC, abstractmethod

LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)  # module logging level
STREAM_HANDLER = logging.StreamHandler()
LOG_TEMPLATE = "%(levelname)s %(asctime)s %(filename)s:%(lineno)s  %(message)s"
STREAM_HANDLER.setFormatter(logging.Formatter(LOG_TEMPLATE))
LOGGER.addHandler(STREAM_HANDLER)


class Transport(ABC):
    """Transport Abstraction

    Transport provide connection to remote.
    Fetch and send data handled by user class.

    methods:
    * send() -> send message to remote
    * poll() -> poll message from remote
    * listen() -> listen connection
    * terminate() -> terminate connection

    """

    @abstractmethod
    def poll(self) -> bytes:
        """poll message

        poll() must run in separated thread to listen() or will deadlock
        """

    @abstractmethod
    def send(self, data: bytes):
        """send message"""

    @abstractmethod
    def listen(self):
        """listen connection"""

    @abstractmethod
    def terminate(self):
        """terminate connection"""


class AddressInUse(OSError):
    """socket address has used by other process"""


class TCPIO(Transport):
    """TCPIO Transport implementation"""

    BUFFER_LENGTH = 4096
    DEFAULT_ADDRESS = ("localhost", 9825)
    DEFAULT_TIMEOUT = 60

    def __init__(self, timeout=None):

        self.address = self.DEFAULT_ADDRESS
        self.conn: socket.socket = None

        self.listen_event = threading.Event()
        self.connect_event = threading.Event()

        self.timeout = timeout
        if timeout is None or timeout < 0:
            self.timeout = self.DEFAULT_TIMEOUT

    def send(self, data: bytes):
        self.conn.sendall(data)

    def poll(self):
        LOGGER.info("poll")
        self.connect_event.wait()

        if self.conn is None:
            self.terminate()
            return b""

        try:
            if chunk := self.conn.recv(self.BUFFER_LENGTH):
                return chunk

        except ConnectionError as err:
            LOGGER.debug(err)

        self.terminate()
        return b""

    def listen(self):
        LOGGER.info("listen")

        self.listen_event.clear()
        self.connect_event.clear()

        def printerr(value):
            """print to stderr"""
            print(value, file=sys.stderr)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)

                try:
                    sock.bind(self.address)
                except OSError as err:
                    # OSError raised if address has used by other process
                    raise AddressInUse(err) from err

                sock.listen()
                printerr(f"listening connection at {self.address}")

                self.conn, addr = sock.accept()
                self.connect_event.set()
                printerr(f"accept connection from {addr}")

                # listen until socket closed
                self.listen_event.wait()

        except ConnectionError as err:
            LOGGER.debug(err)

        except socket.timeout:
            printerr(f"no connection at {self.timeout} second(s).\nexit...")

        except AddressInUse as err:
            printerr(err)

        finally:
            self.terminate()

    def terminate(self):
        """terminate process"""
        LOGGER.info("terminate")

        self.connect_event.set()
        self.listen_event.set()
