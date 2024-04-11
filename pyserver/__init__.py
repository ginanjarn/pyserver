"""Python language sever implementation"""

import sys
import argparse
import logging
from pathlib import Path

ver = sys.version_info
if ver < (3, 8):
    print("Python >= 3.8 is required !!!", file=sys.stderr)
    sys.exit(1)

from pyserver.handler import LSPHandler
from pyserver.server import LSPServer
from pyserver.transport import StandardIO


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
    err_message = """\
Error import required packages!

Following required packages must be installed:
- jedi
- black
- pyflakes

"""
    print(err_message, file=sys.stderr)
    print("error:", repr(err), file=sys.stderr)


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
        transport_ = StandardIO()
    else:
        parser.print_help()
        sys.exit(1)

    if arguments.verbose:
        LOGGER.setLevel(logging.INFO)

    if arguments.veryverbose:
        LOGGER.setLevel(logging.DEBUG)

    handler_ = LSPHandler()
    handler_.register_handlers(
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
    srv = LSPServer(transport_, handler_)
    srv.listen()


if __name__ == "__main__":
    main()
