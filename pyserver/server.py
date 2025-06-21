"""LSP implementation"""

import logging
import queue
import threading
from contextlib import contextmanager
from typing import Any, Callable

from pyserver import errors
from pyserver.message import (
    Message,
    Notification,
    Request,
    Response,
    dumps,
    loads,
)
from pyserver.transport import Transport

LOGGER = logging.getLogger("pyserver")

Id = int
MethodName = str
Params = list | dict | None
Result = list | dict | None
Error = dict | None
HandleFunction = Callable[[MethodName, Params], Result]


class ServerTerminated(Exception):
    """ServerTerminated"""


class RequestManager:
    """RequestHandler executed outside main loop to make request cancelable"""

    def __init__(
        self,
        handle_function: HandleFunction,
        response_callback: Callable[[Id, Result, Error], None],
    ):
        self.handle_function = handle_function
        self.send_response = response_callback

        self.request_queue = queue.Queue()

        self.canceled_requests = set()
        self.in_process_id = -1
        self.canceled_request_lock = threading.Lock()
        self.detach_queue_lock = threading.Lock()

    def add(self, message: Request):
        with self.detach_queue_lock:
            self.request_queue.put(message)

    def cancel(self, request_id: Id):
        with self.canceled_request_lock:
            self.canceled_requests.add(request_id)

    def cancel_all(self):
        self.cancel(self.in_process_id)

        with self.detach_queue_lock:
            while not self.request_queue.empty():
                self.request_queue.get_nowait()

    def _check_canceled(self, request_id: Id):
        # 'canceled_requests' data may be changed during iteration
        with self.canceled_request_lock:
            if request_id in self.canceled_requests:
                raise errors.RequestCancelled(f'request canceled "{request_id}"')

    @contextmanager
    def check_cancelation(self, request_id: int):
        try:
            self._check_canceled(request_id)
            yield
            self._check_canceled(request_id)

        except errors.RequestCancelled as err:
            self.canceled_requests.remove(request_id)
            raise err

    def handle(self, request: Request):
        result, error = None, None

        try:
            with self.check_cancelation(request.id):
                self.in_process_id = request.id
                result = self.handle_function(request.method, request.params)

        except (
            errors.RequestCancelled,
            errors.InvalidParams,
            errors.ContentModified,
            errors.InvalidResource,
            errors.MethodNotFound,
        ) as err:
            error = err

        except Exception as err:
            LOGGER.error("Error handle request: '%s'", err, exc_info=True)
            error = errors.InternalError(err)

        if error:
            # set result to None if error occured
            result = None

        self.send_response(request.id, result, errors.transform_error(error))

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


class DiagnosticsPublisher:
    """"""

    def __init__(
        self,
        handle_function: HandleFunction,
        notification_callback: Callable[[Any, Any], None],
    ) -> None:
        self.handle_function = handle_function
        self.send_notification = notification_callback

        self._target_queue = queue.Queue()

    def publish(self, params: dict) -> None:
        """"""
        self._target_queue.put(params)

    def run(self) -> None:
        """"""
        thread = threading.Thread(target=self._run_task, daemon=True)
        thread.start()

    def _run_task(self):
        while params := self._target_queue.get():
            self._publish_diagnostics(params)

    def _publish_diagnostics(self, params: Params):
        try:
            diagnostics_params = self.handle_function(
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


class LSPServer:
    """LSP server"""

    def __init__(self, transport: Transport, handle_func: HandleFunction, /):
        self.transport = transport
        self.handle_func = handle_func

        # client request handler
        self.request_manager = RequestManager(self.handle_func, self.send_response)
        self.server_request_manager = ServerRequestManager()

        # diagnostic publisher
        self.diagnostics_publisher = DiagnosticsPublisher(
            self.handle_func, self.send_notification
        )

    def send_message(self, message: Message):
        LOGGER.debug("Send >> %s", message)
        content = dumps(message, as_bytes=True)
        self.transport.write(content)

    def send_request(self, method: MethodName, params: Params):
        request_id = self.server_request_manager.add(method)
        self.send_message(Request(request_id, method, params))

    def send_response(self, request_id: Id, result: Result = None, error: Error = None):
        self.send_message(Response(request_id, result, error))

    def send_notification(self, method: MethodName, params: Params):
        self.send_message(Notification(method, params))

    def listen(self):
        """listen client message"""

        self.transport.listen_connection()
        self.request_manager.run()
        self.diagnostics_publisher.run()

        try:
            self._listen_message()

        except ServerTerminated:
            pass
        except Exception as err:
            self.send_notification(
                "window/logMessage", {"type": 1, "message": repr(err)}
            )

    def _listen_message(self):
        """listen message"""

        while True:
            try:
                content = self.transport.read()
            except EOFError:
                return

            try:
                message = loads(content)
            except ValueError as err:
                raise errors.ParseError(err) from err

            LOGGER.debug("Received << %s", message)
            self.exec_message(message)

    def exec_notification(self, message: Notification):
        method = message.method
        params = message.params

        if method == "exit":
            self.transport.terminate()
            raise ServerTerminated()

        if method == "$/cancelRequest":
            self.request_manager.cancel(params["id"])
            return

        self.handle_func(method, params)

        if method in {
            "textDocument/didOpen",
            "textDocument/didChange",
        }:
            # cancel all current request
            self.request_manager.cancel_all()
            # publish diagnostics
            self.diagnostics_publisher.publish(params)

    def exec_request(self, message: Request):
        self.request_manager.add(message)

    def exec_response(self, message: Response):
        method = self.server_request_manager.get(message.id)
        if message.error:
            LOGGER.error("Expected success result for request (%d).", message.id)
            raise RuntimeError("expected success result")

        self.handle_func(method, message)

    def exec_message(self, message: Message) -> None:
        exec_map = {
            Notification: self.exec_notification,
            Request: self.exec_request,
            Response: self.exec_response,
        }
        if (
            self.server_request_manager.is_waiting_response()
            and type(message) != Response
        ):
            LOGGER.error(
                "Response for request (%d) is required.",
                self.server_request_manager.request_id,
            )
            raise RuntimeError("missing response")

        return exec_map[type(message)](message)
