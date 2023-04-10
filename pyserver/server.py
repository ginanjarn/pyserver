"""LSP implementation"""

import logging
import queue
import re
import threading
import sys
from collections import namedtuple
from functools import lru_cache
from typing import Optional, Any, Callable, Iterator

from pyserver import errors
from pyserver.errors import ContentIncomplete
from pyserver.handler import BaseHandler
from pyserver.message import RPCMessage
from pyserver.transport import Transport

LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)  # module logging level
STREAM_HANDLER = logging.StreamHandler()
LOG_TEMPLATE = "%(levelname)s %(asctime)s %(filename)s:%(lineno)s  %(message)s"
STREAM_HANDLER.setFormatter(logging.Formatter(LOG_TEMPLATE))
LOGGER.addHandler(STREAM_HANDLER)


class MissingHeader(Exception):
    """missing header"""


class Stream:
    r"""stream object

    This class handle JSONRPC stream format
        '<header>\r\n<content>'

    Header items must seperated by '\r\n'
    """

    HEADER_ENCODING = "ascii"
    SEPARATOR = b"\r\n\r\n"

    def __init__(self, content: bytes = b""):
        self.buffer = [content] if content else []
        self._lock = threading.RLock()

    def put(self, data: bytes) -> None:
        """put stream data"""
        with self._lock:
            self.buffer.append(data)

    @staticmethod
    @lru_cache(128)
    def _get_content_length(headers: bytes) -> int:
        pattern = re.compile(rb"^Content-Length: (\d+)", flags=re.MULTILINE)
        if found := pattern.search(headers):
            return int(found.group(1))
        raise ValueError("unable get 'Content-Length'")

    def get_contents(self) -> Iterator[bytes]:
        """get contents"""

        def get_content():
            text_buffer = b"".join(self.buffer)

            if not text_buffer:
                raise EOFError("buffer empty")

            # read header
            try:
                header_end = text_buffer.index(self.SEPARATOR)
            except ValueError as err:
                raise MissingHeader("unable get message header") from err

            content_length = self._get_content_length(text_buffer[:header_end])

            # read content
            start = header_end + len(self.SEPARATOR)
            end = start + content_length
            content = text_buffer[start:end]

            recv_len = len(content)
            if recv_len < content_length:
                raise ContentIncomplete(f"want: {content_length}, expected: {recv_len}")

            # restore unread buffer
            self.buffer = [text_buffer[end:]]
            return content

        while True:
            with self._lock:
                try:
                    content = get_content()
                except (EOFError, ContentIncomplete):
                    break

                # fetch next line if missing header
                # this used to parse from standard io which enforce readline()
                except MissingHeader as err:
                    LOGGER.debug(err)
                    break

                except Exception as err:
                    LOGGER.critical(err, exc_info=True)
                    sys.exit(1)

                else:
                    yield content

    @staticmethod
    def wrap_content(content: bytes):
        header = f"Content-Length: {len(content)}".encode(Stream.HEADER_ENCODING)
        return b"".join([header, Stream.SEPARATOR, content])


RequestData = namedtuple("RequestData", ["id_", "method", "params"])


class RequestHandler:
    """RequestHandler executed outside main loop to make request cancelable"""

    def __init__(
        self,
        exec_callback: Callable[[int, str, dict], Any],
        respond_callback: Callable[[int, Any, Any], None],
    ):
        self.request_queue = queue.Queue()
        self.canceled_requests = set()

        self.exec_callback = exec_callback
        self.respond_callback = respond_callback

    def add(self, request_id, method, params):
        self.request_queue.put(RequestData(request_id, method, params))

    def cancel(self, request_id: int):
        self.canceled_requests.add(request_id)

    def check_canceled(self, request_id: int):
        if request_id in self.canceled_requests:
            self.canceled_requests.remove(request_id)
            raise errors.RequestCanceled(f'request canceled "{request_id}"')

    def execute(self, request: RequestData):
        LOGGER.info(f"Exec Request: {request.method!r} {request.params}")
        result, error = None, None

        try:
            self.check_canceled(request.id_)
            result = self.exec_callback(request.method, request.params)

            # may be request canceled during execute
            self.check_canceled(request.id_)

        except errors.RequestCanceled as err:
            error = err
        except errors.FeatureDisabled as err:
            error = err
        except Exception as err:
            LOGGER.debug(err, exc_info=True)
            error = errors.InternalError(err)

        self.respond_callback(request.id_, result, errors.transform_error(error))

    def _run(self):
        while True:
            message = self.request_queue.get()
            self.execute(message)

    def run(self):
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()


class Commands:
    """commands interface"""

    def __init__(self, transport: Transport):
        self.transport = transport
        self.request_id = 0
        self.request_map = {}
        self.canceled_requests = set()

    def new_request_id(self):
        self.request_id += 1
        return self.request_id

    def send_message(self, message: RPCMessage):
        LOGGER.debug(f"Send >> {message}")
        content = message.to_bytes()
        self.transport.send(Stream.wrap_content(content))

    def send_request(self, method: str, params: Any):
        # cancel all previous request
        for req_id, req_method in self.request_map.items():
            if req_method == method:
                self.cancel_request(req_id)

        request_id = self.new_request_id()
        self.request_map[request_id] = method
        self.send_message(RPCMessage.request(request_id, method, params))

    def cancel_request(self, request_id: int):
        self.canceled_requests.add(request_id)
        self.send_notification("$/cancelRequest", {"id": request_id})

    def send_response(
        self, request_id: int, result: Optional[Any] = None, error: Optional[Any] = None
    ):
        self.send_message(RPCMessage.response(request_id, result, error))

    def send_notification(self, method: str, params: Any):
        self.send_message(RPCMessage.notification(method, params))


class LSPServer(Commands):
    """LSP server"""

    def __init__(self, transport: Transport, handler: BaseHandler, /):
        super().__init__(transport)

        self.handler = handler
        self.request_handler = RequestHandler(self.handler.handle, self.send_response)

        self._diagnostics_lock = threading.Lock()

    def listen(self):
        """listen remote"""

        self.request_handler.run()
        threading.Thread(target=self.transport.listen, daemon=True).start()

        self._listen_message()

    def shutdown(self):
        """shutdown server"""
        self.transport.terminate()

    def _listen_message(self):
        stream = Stream()

        def exec_buffered_message():
            for content in stream.get_contents():
                try:
                    message = RPCMessage.from_bytes(content)
                    LOGGER.debug(f"Received << {message}")

                except Exception as err:
                    LOGGER.critical(err, exc_info=True)
                    sys.exit(1)

                try:
                    self.exec_message(message)
                except Exception as err:
                    LOGGER.error(err, exc_info=True)
                    self.send_notification(
                        "window/logMessage", {"type": 1, "message": repr(err)}
                    )

        while True:
            # exec all buffered message
            exec_buffered_message()

            chunk = self.transport.poll()
            stream.put(chunk)
            if not chunk:
                return

    def _publish_diagnostics(self, params: dict):
        if self._diagnostics_lock.locked():
            return

        with self._diagnostics_lock:
            try:
                diagnostics_params = self.handler.handle(
                    "textDocument/publishDiagnostics", params
                )
                self.send_notification(
                    "textDocument/publishDiagnostics", diagnostics_params
                )

            except errors.InvalidResource:
                # ignore document which not in project
                pass
            except errors.FeatureDisabled:
                LOGGER.info("feature disabled")
            except Exception as err:
                LOGGER.error(err, exc_info=True)

    def exec_notification(self, method, params):
        LOGGER.info(f"Exec Notification: {method!r} {params}")

        if method == "exit":
            self.shutdown()
            return

        if method == "$/cancelRequest":
            self.request_handler.cancel(params["id"])
            return

        try:
            self.handler.handle(method, params)
        except Exception as err:
            LOGGER.error(err, exc_info=True)

        if method in {
            "textDocument/didOpen",
            "textDocument/didChange",
        }:
            # publish diagnostics
            threading.Thread(target=self._publish_diagnostics, args=(params,)).start()

    def exec_response(self, message: RPCMessage):
        LOGGER.info(f"Exec Response: {message}")

        message_id = message["id"]
        try:
            method = self.request_map.pop(message_id)

            if error := message.get("error"):
                if message_id in self.canceled_requests:
                    self.canceled_requests.remove(message_id)
                    return

                print(error["message"])
                return

        except KeyError:
            LOGGER.info(f"invalid response {message_id}")
        else:
            self.handler.handle(method, message)

    def exec_message(self, message: RPCMessage):
        """exec received message"""

        # message characteristic
        # - notification  : method, params
        # - request       : id, method, params
        # - response*     : id, result | error
        #
        # * response only have single value of result or error

        message_id = message.get("id")
        method = message.get("method")

        if method:
            params = message.get("params")

            if message_id is None:
                self.exec_notification(method, params)
            else:
                self.request_handler.add(message_id, method, params)

        elif message_id is not None:
            self.exec_response(message)
        else:
            LOGGER.error(f"invalid message: {message}")
