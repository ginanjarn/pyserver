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
class RequestData:
    id_: int
    method: str
    params: dict


class RequestHandler:
    """RequestHandler executed outside main loop to make request cancelable"""

    def __init__(
        self,
        exec_callback: Callable[[int, str, dict], Any],
        response_callback: Callable[[int, Any, Any], None],
    ):
        self.request_queue = queue.Queue()
        self.canceled_requests = set()

        self.cancel_lock = threading.Lock()

        self.current_id = -1
        self.in_process_id = -1

        self.exec_callback = exec_callback
        self.response_callback = response_callback

    def add(self, request_id, method, params):
        self.current_id = request_id
        self.request_queue.put(RequestData(request_id, method, params))

    def cancel(self, request_id: int):
        with self.cancel_lock:
            self.canceled_requests.add(request_id)

    def cancel_all(self):
        with self.cancel_lock:
            self.canceled_requests.update(
                range(self.in_process_id, self.current_id + 1)
            )

    def check_canceled(self, request_id: int):
        # 'canceled_requests' data may be changed during iteration
        with self.cancel_lock:
            if request_id in self.canceled_requests:
                raise errors.RequestCanceled(f'request canceled "{request_id}"')

    def execute(self, request: RequestData):
        result, error = None, None

        try:
            # Check request cancelation before and after exec command
            self.check_canceled(request.id_)
            self.in_process_id = request.id_
            result = self.exec_callback(request.method, request.params)
            self.check_canceled(request.id_)

        except errors.RequestCanceled as err:
            self.canceled_requests.remove(request.id_)
            error = err

        except (
            errors.InvalidParams,
            errors.ContentModified,
            errors.MethodNotFound,
        ) as err:
            error = err

        except Exception as err:
            LOGGER.exception(err, exc_info=True)
            error = errors.InternalError(err)

        self.response_callback(request.id_, result, errors.transform_error(error))

    def _run(self):
        while True:
            message = self.request_queue.get()
            self.execute(message)

    def run(self):
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()


class ServerRequestManager:
    """Manage server request"""

    def __init__(self):
        self.request_id = -1
        self.method = ""

    def is_waiting_response(self) -> bool:
        """"""
        return bool(self.method)

    def add_method(self, method: str) -> int:
        """return request id for added method"""

        self.method = method
        self.request_id += 1
        return self.request_id

    def get_method(self, message_id: int) -> str:
        """get method for response id"""

        if message_id != self.request_id:
            raise ValueError(f"invalid response for request ({self.request_id})")

        temp = self.method
        self.method = ""
        return temp


class LSPServer:
    """LSP server"""

    def __init__(self, transport: Transport, handler: Handler, /):
        self.transport = transport
        self.handler = handler

        # client request handler
        self.request_handler = RequestHandler(self.handler.handle, self.send_response)
        self.request_manager = ServerRequestManager()

    def send_message(self, message: RPCMessage):
        LOGGER.debug("Send >> %s", message)
        content = message.to_bytes()
        self.transport.write(content)

    def send_request(self, method: str, params: Any):
        request_id = self.request_manager.add_method(method)
        self.send_message(RPCMessage.request(request_id, method, params))

    def send_response(
        self, request_id: int, result: Optional[Any] = None, error: Optional[Any] = None
    ):
        self.send_message(RPCMessage.response(request_id, result, error))

    def send_notification(self, method: str, params: Any):
        self.send_message(RPCMessage.notification(method, params))

    def listen(self):
        """listen remote"""

        self.request_handler.run()
        # listen() must not blocking
        threading.Thread(target=self.transport.listen, daemon=True).start()

        self._listen_message()

    def shutdown(self):
        """shutdown server"""
        self.transport.terminate()

    def _listen_message(self):
        """listen message"""

        while True:
            try:
                content = self.transport.read()
            except EOFError:
                self.transport.terminate()

            try:
                message = RPCMessage.from_bytes(content)
                LOGGER.debug("Received << %s", message)

            except Exception as err:
                LOGGER.critical(err, exc_info=True)
                self.transport.terminate()

            try:
                self.exec_message(message)

            except Exception as err:
                LOGGER.error(err, exc_info=True)
                self.send_notification(
                    "window/logMessage", {"type": 1, "message": repr(err)}
                )

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
            LOGGER.error(err, exc_info=True)

        else:
            self.send_notification(
                "textDocument/publishDiagnostics", diagnostics_params
            )

    def exec_notification(self, method, params):
        if method == "exit":
            self.shutdown()
            return

        if method == "$/cancelRequest":
            self.request_handler.cancel(params["id"])
            return

        self.handler.handle(method, params)

        if method in {
            "textDocument/didOpen",
            "textDocument/didChange",
        }:
            # cancel all current request
            self.request_handler.cancel_all()
            # publish diagnostics
            self._publish_diagnostics(params)

    def exec_response(self, response: dict):
        method = self.request_manager.get_method(response["id"])
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
        method = message.get("method")

        if self.request_manager.is_waiting_response() and message_id is not None:
            LOGGER.info("Handle response (%d)", message_id)
            try:
                self.exec_response(message.data)
            except Exception:
                LOGGER.exception("error handle response", exc_info=True)
                self.shutdown()

        if method:
            params = message.get("params")

            if message_id is None:
                LOGGER.info("Handle notification (%s)", method)
                self.exec_notification(method, params)
            else:
                LOGGER.info("Handle request (%d)", message_id)
                self.request_handler.add(message_id, method, params)

        else:
            LOGGER.error("invalid message: '%s'", message)
