"""Python language sever implementation"""

from pyserver import handler
from pyserver import server
from pyserver import transport


def main():
    handler_ = handler.LSPHandler()
    transport_ = transport.TCPIO()
    srv = server.LSPServer(transport_, handler_)
    srv.listen()


if __name__ == "__main__":
    main()
