"""Python language sever implementation"""

import sys
import argparse

ver = sys.version_info
if ver < (3, 8):
    print("Python >= 3.8 is required !!!", file=sys.stderr)
    sys.exit(1)

from pyserver import handler
from pyserver import server
from pyserver import transport


def main():
    parser = argparse.ArgumentParser(
        description="Python Language Server implementation"
    )
    parser.add_argument(
        "-i",
        "--stdin",
        action="store_true",
        help="communicate through standard input",
    )

    arguments = parser.parse_args()

    if arguments.stdin:
        transport_ = transport.StandardIO()
    else:
        parser.print_help()
        sys.exit(1)

    handler_ = handler.LSPHandler()
    srv = server.LSPServer(transport_, handler_)
    srv.listen()


if __name__ == "__main__":
    main()
