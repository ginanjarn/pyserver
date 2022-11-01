"""LSP implementation"""

import logging
import threading
import queue
from collections import namedtuple
from functools import lru_cache
from typing import Optional, Any, Callable

from pyserver import errors
from pyserver.handler import BaseHandler
from pyserver.message import RPCMessage
from pyserver.transport import AbstractTransport, Stream

LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)  # module logging level
STREAM_HANDLER = logging.StreamHandler()
LOG_TEMPLATE = "%(levelname)s %(asctime)s %(filename)s:%(lineno)s  %(message)s"
STREAM_HANDLER.setFormatter(logging.Formatter(LOG_TEMPLATE))
LOGGER.addHandler(STREAM_HANDLER)


RequestData = namedtuple("RequestData", ["id_", "method", "params"])


class RequestHandler:
    """RequestHandler executed outside main loop to make request cancelable"""

    def __init__(
        self,
        exec_callback: Callable[[int, str, dict], Any],
        respond_callback: Callable[[int, Any, Any], None],
    ):
        self.requests = queue.Queue()
        self.canceled_requests = set()

        self.exec_callback = exec_callback
        self.respond_callback = respond_callback

    def add(self, request_id, method, params):
        self.requests.put(RequestData(request_id, method, params))

    def cancel(self, request_id: int):
        self.canceled_requests.add(request_id)

    def check_canceled(self, request_id: int):
        if request_id in self.canceled_requests:
            self.canceled_requests.remove(request_id)
            raise errors.RequestCanceled(f'request canceled "{request_id}"')

    def execute(self, req: RequestData):
        LOGGER.info(f"Exec Request: {req.method!r} {req.params}")
        result, error = None, None

        try:
            self.check_canceled(req.id_)
            result = self.exec_callback(req.method, req.params)
            self.check_canceled(req.id_)

        except errors.RequestCanceled as err:
            error = err
        except Exception as err:
            LOGGER.error(err, exc_info=True)
            error = err

        self.respond_callback(req.id_, result, errors.transform_error(error))

    def _run(self):
        while True:
            message = self.requests.get()
            self.execute(message)

    def run(self):
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()


class Commands:
    """commands interface"""

    def __init__(self, transport: AbstractTransport):
        self.transport = transport
        self.request_id = 0
        self.request_map = {}

    def get_new_request_id(self):
        self.request_id += 1
        return self.request_id

    def send_message(self, message: RPCMessage):
        LOGGER.debug(f"Send >> {message}")
        self.transport.send_message(message)

    def send_request(self, method: str, params: Any):
        request_id = self.get_new_request_id()
        message = RPCMessage.request(request_id, method, params)

        if self.request_map:
            # cancel all previous request
            request_map_c = self.request_map.copy()
            for req_id, req_method in request_map_c.items():
                if req_method == method:
                    self.cancel_request(req_id)

        self.request_map[request_id] = method
        self.send_message(message)

    def cancel_request(self, request_id: int):
        del self.request_map[request_id]
        self.send_notification("$/cancelRequest", {"id": request_id})

    def send_response(
        self, request_id: int, result: Optional[Any] = None, error: Optional[Any] = None
    ):
        self.send_message(RPCMessage.response(request_id, result, error))

    def send_notification(self, method: str, params: Any):
        self.send_message(RPCMessage.notification(method, params))


class LSPServer(Commands):
    """LSP server"""

    def __init__(self, transport: AbstractTransport, handler: BaseHandler, /):
        super().__init__(transport)

        self.transport_channel = self.transport.get_channel()
        self.handler = handler

        self.request_handler = RequestHandler(self.exec_command, self.send_response)

        self._publish_diagnostic_lock = threading.Lock()
        self._listen_lock = threading.Lock()

    def listen(self):
        """listen remote"""

        # listen message
        thread = threading.Thread(target=self._listen_message, daemon=True)
        thread.start()

        self.request_handler.run()
        self.transport.listen()

    def shutdown_server(self):
        """shutdown server"""
        self.transport.terminate()

    def _listen_message(self):
        stream = Stream()

        def exec_buffered_message():
            for content in stream.get_contents():
                message = RPCMessage.from_bytes(content)
                LOGGER.debug(f"Received << {message}")
                try:
                    self.exec_message(message)
                except Exception as err:
                    LOGGER.error(err, exc_info=True)

        while True:
            # this scope must thread-locked to prevent shuffled chunk
            with self._listen_lock:
                chunk = self.transport_channel.get()
                stream.put(chunk)
                if not chunk:
                    return

                exec_buffered_message()

    @staticmethod
    @lru_cache(maxsize=128)
    def flatten_method(method: str):
        """flatten method to lower case and replace character to valid identifier name"""
        flat_method = method.lower().replace("/", "_").replace("$", "s")
        return f"handle_{flat_method}"

    def exec_command(self, method: str, params: RPCMessage):
        try:
            func = getattr(self.handler, self.flatten_method(method))
        except AttributeError:
            raise errors.MethodNotFound(f"method not found {method!r}")

        # exec function
        return func(params)

    def exec_notification(self, method, params):
        LOGGER.info(f"Exec Notification: {method!r} {params}")

        if method == "exit":
            self.shutdown_server()
            return

        if method == "$/cancelRequest":
            self.request_handler.cancel(params["id"])
            return

        try:
            self.exec_command(method, params)
        except Exception as err:
            LOGGER.error(err, exc_info=True)

        if self._publish_diagnostic_lock.locked():
            return

        if method not in {
            "textDocument/didOpen",
            "textDocument/didChange",
        }:
            return

        with self._publish_diagnostic_lock:
            try:
                diagnostic_params = self.exec_command(
                    "textDocument/publishDiagnostics", params
                )
                self.send_notification(
                    "textDocument/publishDiagnostics", diagnostic_params
                )

            except errors.InvalidResource:
                # ignore document which not in project
                pass
            except Exception as err:
                LOGGER.error(err, exc_info=True)

    def exec_response(self, message: RPCMessage):
        LOGGER.info(f"Exec Response: {message}")
        try:
            if error := message.get("error"):
                LOGGER.info(error["message"])
                return

            method = self.request_map.pop(message["id"])

        except KeyError:
            LOGGER.info(f"invalid response {message['id']}")
        else:
            self.exec_command(method, message)

    def exec_message(self, message: RPCMessage):
        """exec received message"""

        msg_id = message.get("id")
        method = message.get("method")

        if method:
            params = message.get("params")

            if msg_id is None:
                self.exec_notification(method, params)
            else:
                self.request_handler.add(msg_id, method, params)

        elif msg_id is not None:
            self.exec_response(message)
        else:
            LOGGER.error(f"invalid message: {message}")
