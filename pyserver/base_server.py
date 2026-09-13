""""""

import logging
from queue import Queue
from threading import Thread
from typing import Optional, Any, Callable

from .errors import transform_error, ServerNotInitialized
from .lsprotocol.server import Server, CancelParams
from .message import loads_rpc2, dumps_rpc2
from .session import Session
from .transport import Transport

LOGGER = logging.getLogger(__name__)


class Context(dict):
    """Context data"""


Method = str
Params = dict
Result = dict


class MessageExchangeBase:
    """Base class for message exchange over a transport."""

    def __init__(self, transport: Transport):
        self.transport: Transport = transport

    def send(self, message: dict) -> None:
        """Send a message over the transport."""
        try:
            content = dumps_rpc2(message, as_bytes=True)
            self.transport.write(content)
        except Exception as err:
            LOGGER.error("Failed to send message: %s", err)
            raise

    def recv(self) -> dict:
        """Receive a message from the transport."""
        try:
            content = self.transport.read()
            return loads_rpc2(content)
        except Exception as err:
            LOGGER.error("Failed to receive/parse message: %s", err)
            raise

    def _handle(
        self, context: Context, method: Method, param_or_result: Optional[Any] = None
    ) -> Optional[Result]:
        """handle command"""
        raise NotImplementedError("_handle")

    def listen(self) -> None:
        """listen message"""
        raise NotImplementedError("listen")


class ServerRequestManager:
    def __init__(self, handle) -> None:
        self._handle = handle
        self._request_count = 0

        self.pending_id = 0
        self.pending_method = ""

    def add(self, method: Method) -> int:
        self._request_count += 1

        self.pending_method = method
        self.pending_id = self._request_count
        return self._request_count

    def handle_result(self, context: Context, result: Result):
        if (resp_id := context["id"]) and resp_id != self.pending_id:
            raise Exception("expected response for message (%d)" % self.pending_id)

        self._handle(context, self.pending_method, result)


class ServerCommand(MessageExchangeBase):
    def __init__(self):
        self.server_request_manager = ServerRequestManager(self._handle)

    def request(self, method: Method, params: Params):
        req_id = self.server_request_manager.add(method)
        self.send({"id": req_id, "method": method, "params": params})

    def handle_response(self, context: Context, response: dict):
        if response.get("error"):
            raise ValueError("expected success response")

        result = response.get("result")
        self.server_request_manager.handle_result(context, result)

    def notify(self, method: Method, params: Params):
        self.send({"method": method, "params": params})


class CancelableClientRequestManager:
    def __init__(
        self,
        handler: Callable[[Context, Method, Params], Any],
        respond_callback: Callable[[dict], None],
    ) -> None:
        self.handler = handler
        self.respond = respond_callback
        self.task_queue = Queue()
        self.canceled_tasks = set()

    def add(self, context: Context, method: Method, params: Params):
        self.task_queue.put((context, method, params))

    def cancel(self, message_id: int):
        self.canceled_tasks.add(message_id)

    def loop_until_done(self):
        def exec_task():
            while True:
                context, method, params = self.task_queue.get()
                # Ignore canceled request
                if context["id"] in self.canceled_tasks:
                    self.canceled_tasks.remove(context["id"])
                    continue

                try:
                    result = self.handler(context, method, params)
                    self.respond(context, result=result)
                except Exception as err:
                    error = {"code": 1, "message": transform_error(err)}
                    self.respond(context, error=error)

        Thread(target=exec_task, daemon=True).start()


class ClientHandler(MessageExchangeBase):

    def __init__(self):
        self.client_request_manager = CancelableClientRequestManager(
            self._handle, self.respond
        )
        self.client_request_manager.loop_until_done()

    def handle_request(self, context: Context, method: Method, params: Params):
        if method not in {"initialize", "shutdown"}:
            if not self.session.is_initialized:
                raise ServerNotInitialized("Server not initialized")

        self.client_request_manager.add(context, method, params)

    def respond(
        self,
        context: Context,
        result: Optional[dict] = None,
        error: Optional[dict] = None,
    ):
        temp = {"id": context["id"]}
        if error:
            temp["error"] = error
        else:
            temp["result"] = result

        self.send(temp)

    def handle_notification(self, context: Context, method: Method, params: Params):
        if method not in {"exit", "initialized"}:
            if not self.session.is_initialized:
                raise ServerNotInitialized("Server not initialized")

        self._handle(context, method, params)

    def handle_cancel_notification(self, context: dict, params: CancelParams) -> None:
        self.client_request_manager.cancel(params["id"])

    def _publish_diagnostics(self, text_document: dict) -> None:
        raise NotImplementedError("_publish_diagnostics")


class RPC(ServerCommand, ClientHandler, Server):
    def __init__(self, transport: Transport):
        MessageExchangeBase.__init__(self, transport)
        ServerCommand.__init__(self)
        ClientHandler.__init__(self)

        self.session: Session = Session()

    def listen(self) -> None:
        """"""
        while True:
            try:
                message = self.recv()
                message_id = message.get("id")
                context = {"id": message_id} if message_id else {}

                if method := message.get("method"):
                    params = message.get("params")
                    if message_id is not None:
                        self.handle_request(context, method, params)
                        continue
                    self.handle_notification(context, method, params)
                    continue
                self.handle_response(context, message)

            except Exception as err:
                LOGGER.exception("Error handle message: %s", err, exc_info=True)
                raise

    def _handle(
        self, context: Context, method: Method, param_or_result: Optional[Any] = None
    ) -> Optional[Result]:
        return self.handle(context, method, param_or_result)


class BaseServer(RPC):
    """Base Server"""
