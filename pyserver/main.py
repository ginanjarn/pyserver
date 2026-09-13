"""Python language sever implementation"""

import argparse
import logging
import sys
from functools import partial
from pathlib import Path

from .server import Server
from .transport import StandardIO
from .version import __version__

printerr = partial(print, file=sys.stderr)
"""print to stderr"""

ver = sys.version_info
if ver < (3, 8):
    printerr("Python >= 3.8 is required !!!")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        usage="python -m pyserver [options]",
        description="Python Language Server implementation",
    )
    parser.add_argument(
        "-i",
        "--stdin",
        action="store_true",
        help="communicate through standard input",
    )

    parser.add_argument("-v", "--version", action="store_true", help="print version")
    parser.add_argument("--verbose", action="store_true", help="verbose logging")

    arguments = parser.parse_args()

    if arguments.version:
        printerr("version", __version__)
        sys.exit(0)

    if arguments.stdin:
        transport_ = StandardIO()
    else:
        printerr("Currently only standard input implementation available.")
        parser.print_help()
        sys.exit(1)

    log_level = logging.ERROR
    if arguments.verbose:
        log_level = logging.DEBUG
    setup_logger(log_level)

    try:
        server = Server(transport_)
        server.listen()
    except Exception:
        sys.exit(1)
    else:
        sys.exit(0)


def setup_logger(level: int):
    """setup logger"""

    stream_handler = logging.StreamHandler()

    log_directory = Path().home() / ".pyserver"
    # create directory if not exist
    log_directory.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_directory.joinpath("pyserver.log"))
    file_handler.setLevel(logging.ERROR)

    # Global config
    log_format = "%(levelname)s\t%(asctime)s %(filename)s:%(lineno)s  %(message)s"
    logging.basicConfig(format=log_format, handlers=[stream_handler, file_handler])

    # Channel specific config
    logger = logging.getLogger(__name__.split(".")[0])
    logger.setLevel(level)
