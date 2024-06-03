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
        self.expired_id = -1

        self.exec_callback = exec_callback
        self.response_callback = response_callback

    def add(self, request_id, method, params):
        self.current_id = request_id
        self.request_queue.put(RequestData(request_id, method, params))

    def cancel(self, request_id: int):
        with self.cancel_lock:
            self.canceled_requests.add(request_id)

    def cancel_all(self):
        self.expired_id = self.current_id

    def check_canceled(self, request_id: int):
        # 'canceled_requests' data may be changed during iteration
        with self.cancel_lock:
            if request_id in self.canceled_requests:
                self.canceled_requests.remove(request_id)
                raise errors.RequestCanceled(f'request canceled "{request_id}"')

        if request_id <= self.expired_id:
            raise errors.RequestCanceled(f'request canceled "{request_id}"')

    def execute(self, request: RequestData):
        result, error = None, None

        try:
            # Check request cancelation before and after exec command
            self.check_canceled(request.id_)
            result = self.exec_callback(request.method, request.params)
            self.check_canceled(request.id_)

        except (
            errors.InvalidParams,
            errors.ContentModified,
            errors.RequestCanceled,
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


class LSPServer:
    """LSP server"""

    def __init__(self, transport: Transport, handler: Handler, /):
        self.transport = transport
        self.request_id = 0
        self.request_map = {}
        self.canceled_requests = set()

        self.handler = handler
        self.request_handler = RequestHandler(self.handler.handle, self.send_response)

    def new_request_id(self):
        self.request_id += 1
        return self.request_id

    def send_message(self, message: RPCMessage):
        LOGGER.debug("Send >> %s", message)
        content = message.to_bytes()
        self.transport.write(content)

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
            content = self.transport.read()

            try:
                message = RPCMessage.from_bytes(content)
                LOGGER.debug("Received << %s", message)

            except Exception as err:
                LOGGER.critical(err, exc_info=True)
                self.transport.terminate(exit_code=1)

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
        message_id = response["id"]
        try:
            method = self.request_map.pop(message_id)

            if error := response.get("error"):
                if message_id in self.canceled_requests:
                    self.canceled_requests.remove(message_id)
                    return

                LOGGER.info(error["message"])
                return

        except KeyError:
            LOGGER.info(f"invalid response {message_id}")
        else:
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

        if method:
            params = message.get("params")

            if message_id is None:
                LOGGER.info("Handle notification (%s)", method)
                self.exec_notification(method, params)
            else:
                LOGGER.info("Handle request (%d)", message_id)
                self.request_handler.add(message_id, method, params)

        elif message_id is not None:
            LOGGER.info("Handle response (%d)", message_id)
            self.exec_response(message)
        else:
            LOGGER.error(f"invalid message: {message}")
