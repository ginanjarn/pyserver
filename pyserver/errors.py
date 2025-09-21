"""rpc errors"""

from typing import Union, Dict, Any, Optional


class JSONRPCException(Exception):
    """Base json-rpc exception"""

    code: int
    message: str

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ParseError(JSONRPCException):
    """An error occurred while parsing the JSON text"""

    code = -32700
    message = "parse error"


class InvalidRequest(JSONRPCException):
    """The JSON sent is not a valid Request object"""

    code = -32600
    message = "invalid request"


class MethodNotFound(JSONRPCException):
    """The method does not exist / is not available"""

    code = -32601
    message = "method not found"


class InvalidParams(JSONRPCException):
    """Invalid method parameter(s)"""

    code = -32602
    message = "invalid params"


class InternalError(JSONRPCException):
    """Internal JSON-RPC error"""

    code = -32603
    message = "internal error"


class ServerNotInitialized(JSONRPCException):
    """Server received a notification or request before the server received the `initialize` request"""

    code = -32002
    message = "server not initialized"


class UnknownErrorCode(JSONRPCException):
    code = -32001
    message = ""


class RequestFailed(JSONRPCException):
    """A request failed but it was syntactically correct"""

    code = -32803
    message = "request failed"


class ServerCancelled(JSONRPCException):
    """The server cancelled the request"""

    code = -32802
    message = "server cancelled"


class ContentModified(JSONRPCException):
    """The content of a document got modified outside normal conditions"""

    code = -32801
    message = "content modified"


class RequestCancelled(JSONRPCException):
    """The client has canceled a request and a server has detected the cancel"""

    code = -32800
    message = "request cancelled"


class ServerError(JSONRPCException):
    """Reserved for implementation-defined server-errors

    Valid error code from  -32099 to -32000.
    """

    message: str
    code: int

    def __init__(self, *args: object) -> None:
        min_range = -32099
        max_range = -32000
        if not (min_range < self.code < max_range):
            raise ValueError(f"valid code {min_range} to {max_range}")
        super().__init__(*args)


class InvalidResource(ServerError):
    """invalid resource"""

    message = "invalid resource"
    code = -32001


class FeatureDisabled(ServerError):
    """feature disabled"""

    message = "feature disabled"
    code = -32002


def transform_error(
    error: Union[JSONRPCException, Exception, None],
) -> Optional[Dict[str, Any]]:
    """transform exception to rpc error"""

    if not error:
        return None

    try:
        code = error.code
        message = error.message

    except AttributeError:
        # 'err.code' and 'err.message' may be not defined
        code = InternalError.code
        message = repr(error)

    return {"code": code, "message": message}
