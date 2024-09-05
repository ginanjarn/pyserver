"""Python language sever implementation"""

import sys
import argparse
import logging
from pathlib import Path

from pyserver.handler import LSPHandler
from pyserver.server import LSPServer
from pyserver.transport import StandardIO

ver = sys.version_info
if ver < (3, 8):
    print("Python >= 3.8 is required !!!", file=sys.stderr)
    sys.exit(1)


__version__ = "0.1.0"


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
        print("version", __version__)
        sys.exit(0)

    if arguments.stdin:
        transport_ = StandardIO()
    else:
        print("Currently only standard input implementation available.")
        parser.print_help()
        sys.exit(1)

    log_level = logging.ERROR
    if arguments.verbose:
        log_level = logging.DEBUG
    setup_logger(log_level)

    handler_ = LSPHandler()
    load_services(handler_)

    srv = LSPServer(transport_, handler_)
    srv.listen()


def setup_logger(level: int):
    """setup logger"""

    # logging channel
    logger = logging.getLogger("pyserver")

    log_format = (
        "[%(name)s]%(levelname)s %(asctime)s %(filename)s:%(lineno)s  %(message)s"
    )

    # Log to stderr
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(stream_handler)

    # Log to file
    log_directory = Path().home().joinpath(".pyserver")
    # create directory if not exist
    log_directory.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_directory.joinpath("pyserver.log"))
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)


def load_services(handler: LSPHandler):
    """load services"""
    try:
        from pyserver.services.completion import textdocument_completion
        from pyserver.services.hover import textdocument_hover
        from pyserver.services.definition import textdocument_definition
        from pyserver.services.formatting import textdocument_formatting
        from pyserver.services.diagnostics import textdocument_publishdiagnostics
        from pyserver.services.prepare_rename import textdocument_preparerename
        from pyserver.services.rename import textdocument_rename
        from pyserver.services.signature_help import textdocument_signaturehelp

    except ImportError as err:
        err_message = (
            "Error import required packages!\n\n"
            "Following required packages must be installed:\n"
            "- jedi\n- black\n- pyflakes\n"
            f"Error: {err!r}\n"
        )
        print(err_message, file=sys.stderr)
        sys.exit(1)

    handler.register_handlers(
        {
            "textDocument/completion": textdocument_completion,
            "textDocument/hover": textdocument_hover,
            "textDocument/definition": textdocument_definition,
            "textDocument/formatting": textdocument_formatting,
            "textDocument/publishDiagnostics": textdocument_publishdiagnostics,
            "textDocument/prepareRename": textdocument_preparerename,
            "textDocument/rename": textdocument_rename,
            "textDocument/signatureHelp": textdocument_signaturehelp,
        }
    )
