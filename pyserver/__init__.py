"""Python language sever implementation"""

import sys
import argparse
import logging
from importlib import import_module
from pathlib import Path
from typing import Any, Optional

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

    stream_handler = logging.StreamHandler()

    log_directory = Path().home().joinpath(".pyserver")
    # create directory if not exist
    log_directory.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_directory.joinpath("pyserver.log"))
    file_handler.setLevel(logging.ERROR)

    # Global config
    log_format = "%(levelname)s\t%(asctime)s %(filename)s:%(lineno)s  %(message)s"
    logging.basicConfig(format=log_format, handlers=[stream_handler, file_handler])

    # Channel specific config
    logger = logging.getLogger("pyserver")
    logger.setLevel(level)


def try_import(mod_name: str, /, attr_name: str = "") -> Optional[Any]:
    """Try import module or attribute. Return 'None' if error raised."""
    try:
        mod = import_module(mod_name)
        if not attr_name:
            return mod
        return getattr(mod, attr_name)

    except Exception:
        return None


def load_services(handler: LSPHandler):
    """load services"""

    service_map = {
        "textDocument/completion": (
            "pyserver.services.completion",
            "textdocument_completion",
        ),
        "textDocument/hover": (
            "pyserver.services.hover",
            "textdocument_hover",
        ),
        "textDocument/definition": (
            "pyserver.services.definition",
            "textdocument_definition",
        ),
        "textDocument/formatting": (
            "pyserver.services.formatting",
            "textdocument_formatting",
        ),
        "textDocument/publishDiagnostics": (
            "pyserver.services.diagnostics",
            "textdocument_publishdiagnostics",
        ),
        "textDocument/prepareRename": (
            "pyserver.services.prepare_rename",
            "textdocument_preparerename",
        ),
        "textDocument/rename": (
            "pyserver.services.rename",
            "textdocument_rename",
        ),
        "textDocument/signatureHelp": (
            "pyserver.services.signature_help",
            "textdocument_signaturehelp",
        ),
    }

    for name, service_func in service_map.items():
        if func := try_import(*service_func):
            handler.register_handlers({name: func})
        else:
            err_message = f"Error load {name!r} service."
            print(err_message, file=sys.stderr)
