"""LSP implementation"""

import logging
import threading
import queue
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


class Commands:
    """commands interface"""

    def __init__(self, transport: AbstractTransport):
        self.transport = transport
        self.current_req_id = 0
        self.request_map = {}

    def next_request_id(self):
        self.current_req_id += 1
        return self.current_req_id

    def send_request(self, method: str, params: Any):
        request_id = self.next_request_id()
        message = RPCMessage.request(request_id, method, params)

        if self.request_map:
            # cancel all previous request
            request_map_c = self.request_map.copy()
            for req_id, req_method in request_map_c.items():
                if req_method == method:
                    self.cancel_request(req_id)

        self.request_map[request_id] = method
        self.transport.send_message(message)

    def cancel_request(self, request_id: int):
        del self.request_map[request_id]
        self.send_notification("$/cancelRequest", {"id": request_id})

    def send_response(
        self, request_id: int, result: Optional[Any] = None, error: Optional[Any] = None
    ):
        self.transport.send_message(RPCMessage.response(request_id, result, error))

    def send_notification(self, method: str, params: Any):
        self.transport.send_message(RPCMessage.notification(method, params))


class RequestHandler:
    def __init__(
        self,
        exec_callback: Callable[[RPCMessage], Any],
        write_callback: Callable[[RPCMessage], None],
    ):
        self.requests = queue.Queue()
        self.canceled_requests = set()

        self.exec_callback = exec_callback
        self.write_callback = write_callback

        self.lock = threading.Lock()

    def add(self, message: RPCMessage):
        self.requests.put(message)

    def cancel(self, id_: int):
        self.canceled_requests.add(id_)

    def is_canceled(self, id_: int):

        try:
            self.canceled_requests.remove(id_)
            return True
        except KeyError:
            return False

    def execute(self, message: RPCMessage):
        LOGGER.debug(f"execute message: {message}")
        result, error = None, None
        id_ = message["id"]

        # check request cancelation before and after exec request

        if self.is_canceled(id_):
            error = errors.InvalidRequest(f"request canceled {id_!r}")

        else:
            # execute
            try:
                result = self.exec_callback(message)
            except Exception as err:
                LOGGER.error(err, exc_info=True)
                error = err

        if self.is_canceled(id_):
            error = errors.InvalidRequest(f"request canceled {id_!r}")

        result_message = RPCMessage.response(id_, result, errors.transform_error(error))
        LOGGER.debug(result_message)
        self.write_callback(result_message)

    def _run(self):
        while True:
            with self.lock:
                message = self.requests.get()
                self.execute(message)

    def run(self):
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()


class LSPServer(Commands):
    """LSP server"""

    def __init__(self, transport: AbstractTransport, handler: BaseHandler, /):
        super().__init__(transport)

        self.transport_channel = self.transport.get_channel()
        self.handler: BaseHandler = handler

        self.request_handler = RequestHandler(
            self.exec_request, self.transport.send_message
        )

        self._publish_diagnostic_lock = threading.Lock()

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
        while True:
            message = self.transport_channel.get()
            stream.put(message)
            if not message:
                return

            for content in stream.get_contents():
                message = RPCMessage.from_bytes(content)
                LOGGER.debug(f"Received << {message}")
                try:
                    self.exec_message(message)
                except Exception as err:
                    LOGGER.error(err, exc_info=True)

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
                params = self.exec_command("textDocument/publishDiagnostics", params)
                self.send_notification("textDocument/publishDiagnostics", params)
            except Exception as err:
                LOGGER.error(err, exc_info=True)

    def exec_response(self, message: RPCMessage):
        LOGGER.info(f"Exec Response: {message}")
        try:
            method = self.request_map.pop(message["id"])
        except KeyError as err:
            if error := message.get("error"):
                LOGGER.info(error["message"])
                return
            raise Exception(f"invalid response 'id': {err}")

        try:
            self.exec_command(method, message)
        except Exception as err:
            LOGGER.error(err, exc_info=True)

    @staticmethod
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

    def exec_request(self, message: RPCMessage):
        method = message["method"]
        params = message["params"]
        LOGGER.info(f"Exec Request {method!r} {params}")
        return self.exec_command(method, params)

    def exec_message(self, message: RPCMessage):
        """exec received message"""

        message_id = message.get("id")
        message_method = message.get("method")
        if message_method:
            params = message.get("params")
            if message_id is not None:
                self.request_handler.add(message)

            else:
                self.exec_notification(message_method, params)

        elif message_id is not None:
            self.exec_response(message)
        else:
            LOGGER.error(f"invalid message: {message}")
