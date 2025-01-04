"""LSP implementation"""

import logging
import queue
import threading
from typing import Optional, Any, Callable

from pyserver import errors
from pyserver.handler import Handler
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

    def add(self, message: Request):
        self.request_queue.put(message)

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

    def handle(self, request: Request):
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


class DiagnosticsPublisher:
    """"""

    def __init__(
        self,
        handle_function: Callable[[str, dict], Any],
        notification_callback: Callable[[Any, Any], None],
    ) -> None:
        self.handle_function = handle_function
        self.send_notification = notification_callback

        self.event = threading.Event()
        self.target_params = None

    def publish(self, params: dict) -> None:
        """"""
        self.target_params = params
        self.event.set()

    def run(self) -> None:
        """"""
        thread = threading.Thread(target=self._run_task, daemon=True)
        thread.start()

    def _run_task(self):
        while True:
            self.event.wait()
            self.event.clear()
            self._publish_diagnostics(self.target_params)

    def _publish_diagnostics(self, params: dict):
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


# Exit code
EXIT_SUCCESS = 0
EXIT_ERROR = 1


class LSPServer:
    """LSP server"""

    def __init__(self, transport: Transport, handler: Handler, /):
        self.transport = transport
        self.handler = handler

        # client request handler
        self.request_manager = RequestManager(self.handler.handle, self.send_response)
        self.server_request_manager = ServerRequestManager()

        # diagnostic publisher
        self.diagnostics_publisher = DiagnosticsPublisher(
            self.handler.handle, self.send_notification
        )

    def send_message(self, message: Message):
        LOGGER.debug("Send >> %s", message)
        content = dumps(message, as_bytes=True)
        self.transport.write(content)

    def send_request(self, method: str, params: Any):
        request_id = self.server_request_manager.add(method)
        self.send_message(Request(request_id, method, params))

    def send_response(
        self, request_id: int, result: Optional[Any] = None, error: Optional[Any] = None
    ):
        self.send_message(Response(request_id, result, error))

    def send_notification(self, method: str, params: Any):
        self.send_message(Notification(method, params))

    def listen(self):
        """listen client message"""

        self.transport.listen_connection()
        self.request_manager.run()
        self.diagnostics_publisher.run()

        try:
            self._listen_message()

        except Exception as err:
            self.send_notification(
                "window/logMessage", {"type": 1, "message": repr(err)}
            )
        self.exit(EXIT_ERROR)

    def exit(self, exit_code: int = 0):
        """exit server"""
        self.transport.terminate(exit_code)

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
            self.exit(EXIT_SUCCESS)
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
            self.diagnostics_publisher.publish(params)

    def exec_request(self, message: Request):
        self.request_manager.add(message)

    def exec_response(self, message: Response):
        method = self.server_request_manager.get(message.id)
        if message.error:
            LOGGER.error("Expected success result for request (%d).", message.id)
            self.exit(EXIT_ERROR)
            return

        self.handler.handle(method, message)

    def exec_message(self, message: Message) -> Optional[Any]:
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
            self.exit(EXIT_ERROR)

        return exec_map[type(message)](message)
