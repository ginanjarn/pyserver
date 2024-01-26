"""Python language sever implementation"""

import sys
import argparse
import logging
from pathlib import Path

ver = sys.version_info
if ver < (3, 8):
    print("Python >= 3.8 is required !!!", file=sys.stderr)
    sys.exit(1)

from pyserver import handler
from pyserver import server
from pyserver import transport


# logging format
LOGGING_FORMAT = (
    "[%(name)s]%(levelname)s %(asctime)s %(filename)s:%(lineno)s  %(message)s"
)

# stderr stream logging handler
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(logging.Formatter(LOGGING_FORMAT))

# file logging handler
LOG_DIR = Path().home().joinpath(".pyserver")
LOG_DIR.mkdir(parents=True, exist_ok=True)  # maybe not created yet
FILE_HANDLER = logging.FileHandler(LOG_DIR.joinpath("pyserver.log"))
FILE_HANDLER.setLevel(logging.ERROR)
FILE_HANDLER.setFormatter(logging.Formatter(LOGGING_FORMAT))

# logging channel
LOGGER = logging.getLogger("pyserver")

# set handler
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(FILE_HANDLER)


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

    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-vv", "--veryverbose", action="store_true")

    arguments = parser.parse_args()

    if arguments.stdin:
        transport_ = transport.StandardIO()
    else:
        parser.print_help()
        sys.exit(1)

    if arguments.verbose:
        LOGGER.setLevel(logging.INFO)

    if arguments.veryverbose:
        LOGGER.setLevel(logging.DEBUG)

    handler_ = handler.LSPHandler()
    srv = server.LSPServer(transport_, handler_)
    srv.listen()


if __name__ == "__main__":
    main()
