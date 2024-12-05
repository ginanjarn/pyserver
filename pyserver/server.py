"""LSP implementation"""

import logging
import queue
import threading
from dataclasses import dataclass
from typing import Optional, Any, Callable

from pyserver import errors
from pyserver.handler import Handler
from pyserver.message import RPCMessage
from pyserver.transport import Transport

LOGGER = logging.getLogger("pyserver")


@dataclass
class RequestCommand:
    id: int
    method: str
    params: dict


class RequestManager:
    """RequestHandler executed outside main loop to make request cancelable"""

    def __init__(
        self,
        handle_function: Callable[[int, str, dict], Any],
        response_callback: Callable[[int, Any, Any], None],
    ):
        self.request_queue = queue.Queue()
        self.canceled_requests = set()

        self.cancel_lock = threading.RLock()
        self.in_process_id = -1

        self.handle_function = handle_function
        self.response_callback = response_callback

    def add(self, request_id: int, method: str, params: dict):
        self.request_queue.put(RequestCommand(request_id, method, params))

    def cancel(self, request_id: int):
        with self.cancel_lock:
            self.canceled_requests.add(request_id)

    def cancel_all(self):
        with self.cancel_lock:
            self.cancel(self.in_process_id)

            # detach 'request_queue'
            while not self.request_queue.empty():
                self.request_queue.get_nowait()

    def check_canceled(self, request_id: int):
        # 'canceled_requests' data may be changed during iteration
        with self.cancel_lock:
            if request_id in self.canceled_requests:
                raise errors.RequestCancelled(f'request canceled "{request_id}"')

    def handle(self, request: RequestCommand):
        result, error = None, None

        try:
            # Check request cancelation before and after exec command
            self.check_canceled(request.id)
            self.in_process_id = request.id
            result = self.handle_function(request.method, request.params)
            self.check_canceled(request.id)

        except errors.RequestCancelled as err:
            self.canceled_requests.remove(request.id)
            error = err

        except (
            errors.InvalidParams,
            errors.ContentModified,
            errors.InvalidResource,
            errors.MethodNotFound,
        ) as err:
            error = err

        except Exception as err:
            LOGGER.error("Error handle request: '%s'", err, exc_info=True)
            error = errors.InternalError(err)

        self.response_callback(request.id, result, errors.transform_error(error))

    def _run_task(self):
        while request := self.request_queue.get():
            self.handle(request)

    def run(self):
        thread = threading.Thread(target=self._run_task, daemon=True)
        thread.start()


class ServerRequestManager:
    """Manage server request"""

    def __init__(self):
        self.request_id = -1
        self.method = ""
        self._is_waiting_response = False

    def is_waiting_response(self) -> bool:
        """"""
        return self._is_waiting_response

    def add(self, method: str) -> int:
        """return request id for added method"""

        self.method = method
        self.request_id += 1
        self._is_waiting_response = True
        return self.request_id

    def get(self, message_id: int) -> str:
        """get method for response id"""

        if message_id != self.request_id:
            raise ValueError(f"invalid response for request ({self.request_id})")

        self._is_waiting_response = False
        return self.method


class LSPServer:
    """LSP server"""

    def __init__(self, transport: Transport, handler: Handler, /):
        self.transport = transport
        self.handler = handler

        # client request handler
        self.request_manager = RequestManager(self.handler.handle, self.send_response)
        self.server_request_manager = ServerRequestManager()

    def send_message(self, message: RPCMessage):
        LOGGER.debug("Send >> %s", message)
        content = message.dumps(as_bytes=True)
        self.transport.write(content)

    def send_request(self, method: str, params: Any):
        request_id = self.server_request_manager.add(method)
        self.send_message(RPCMessage.request(request_id, method, params))

    def send_response(
        self, request_id: int, result: Optional[Any] = None, error: Optional[Any] = None
    ):
        self.send_message(RPCMessage.response(request_id, result, error))

    def send_notification(self, method: str, params: Any):
        self.send_message(RPCMessage.notification(method, params))

    def listen(self):
        """listen client message"""

        self.transport.listen_connection()
        self.request_manager.run()

        try:
            self._listen_message()

        except Exception as err:
            self.send_notification(
                "window/logMessage", {"type": 1, "message": repr(err)}
            )
        self.shutdown()

    def shutdown(self):
        """shutdown server"""
        self.transport.terminate()

    def _listen_message(self):
        """listen message"""

        while True:
            try:
                content = self.transport.read()
            except EOFError:
                return

            message = RPCMessage.loads(content)
            LOGGER.debug("Received << %s", message)

            self.exec_message(message)

    def _publish_diagnostics(self, params: dict):
        try:
            diagnostics_params = self.handler.handle(
                "textDocument/publishDiagnostics", params
            )

        except (
            errors.InvalidParams,
            errors.ContentModified,
            errors.InvalidResource,
            errors.MethodNotFound,
        ):
            # ignore above exception
            pass

        except Exception as err:
            LOGGER.error("Error get diagnostics: '%s'", err, exc_info=True)

        else:
            self.send_notification(
                "textDocument/publishDiagnostics", diagnostics_params
            )

    def exec_notification(self, method, params):
        if method == "exit":
            self.shutdown()
            return

        if method == "$/cancelRequest":
            self.request_manager.cancel(params["id"])
            return

        self.handler.handle(method, params)

        if method in {
            "textDocument/didOpen",
            "textDocument/didChange",
        }:
            # cancel all current request
            self.request_manager.cancel_all()
            # publish diagnostics
            self._publish_diagnostics(params)

    def exec_response(self, response: dict):
        method = self.server_request_manager.get(response["id"])
        self.handler.handle(method, response)

    def exec_message(self, message: RPCMessage):
        """exec received message"""

        # message characteristic
        # - notification  : method, params
        # - request       : id, method, params
        # - response*     : id, result | error
        #
        # * response only have single value of result or error

        message_id = message.get("id")

        if self.server_request_manager.is_waiting_response() and message_id is not None:
            LOGGER.info("Handle response (%d)", message_id)
            self.exec_response(message.data)
            return

        method = message.get("method")
        params = message.get("params")

        if not method:
            # request or notification message must contain method
            raise errors.InternalError("Invalid message")

        if message_id is None:
            LOGGER.info("Handle notification (%s)", method)
            self.exec_notification(method, params)
            return

        # else:
        LOGGER.info("Handle request (%d)", message_id)
        self.request_manager.add(message_id, method, params)
