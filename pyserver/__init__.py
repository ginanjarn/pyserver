"""Python language sever implementation"""

import sys

ver = sys.version_info
if ver < (3, 8):
    print("Python >= 3.8 is required !!!", file=sys.stderr)
    sys.exit(1)

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
