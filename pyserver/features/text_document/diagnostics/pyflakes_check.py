from ast import parse, AST, iter_child_nodes
from collections import namedtuple
from typing import Iterator, List, Dict

from pyflakes.checker import Checker
from pyflakes.messages import Message

from . import Diagnostic, TextRange, KIND_ERROR, KIND_WARNING

RowCol = namedtuple("RowCol", ["row", "column"])


class PyflakesChecker:

    def __init__(self, file_name: str, text: str, /):
        self.file_name = file_name
        self.text = text

    def get_diagnostic(self) -> Iterator[Diagnostic]:
        yield from self._check(self.file_name, self.text)

    def _check(self, filename: str, source: str, /) -> Iterator[Diagnostic]:
        try:
            tree = parse(source, filename=filename)
        except SyntaxError as err:
            yield from self._get_error(err, filename)
        else:
            yield from self._get_warnings(tree, filename)

    def _get_error(self, err: SyntaxError, filename: str) -> Iterator[Diagnostic]:

        # lineno might be None if the error was during tokenization
        # lineno might be 0 if the error came from stdin
        lineno = err.lineno or 1
        offset = err.offset or 1

        # some versions of python emit an offset of -1 for certain encoding errors
        offset = max(offset, 1)

        end_lineno = getattr(err, "end_lineno", lineno)
        end_offset = getattr(err, "end_offset", offset)

        # python ast use 1-based line index
        lineno -= 1
        offset -= 1
        end_lineno -= 1
        end_offset -= 1

        a = RowCol(lineno, offset)
        b = RowCol(end_lineno, end_offset)

        msg = err.msg or err.args[0]
        filename = err.filename or filename
        text_range = TextRange(min(a, b), max(a, b))
        yield Diagnostic(KIND_ERROR, filename, text_range, msg, "ast")

    def _get_warnings(self, node: AST, filename: str) -> Iterator[Diagnostic]:

        check = Checker(node, filename=filename)
        check.messages.sort(key=lambda m: (m.lineno, m.col))

        node_map = find_nodes(node, [(m.lineno, m.col) for m in check.messages])
        yield from (self._build_warning(m, node_map) for m in check.messages)

    def _build_warning(
        self, message: Message, node_map: Dict[RowCol, AST]
    ) -> Diagnostic:

        filename = message.filename
        text_msg = message.message % message.message_args

        node = node_map[(message.lineno, message.col)]
        start = RowCol(node.lineno - 1, node.col_offset)
        end = RowCol(node.end_lineno - 1, node.end_col_offset)

        text_range = TextRange(start, end)
        return Diagnostic(KIND_WARNING, filename, text_range, text_msg, "pyflakes")


def find_nodes(tree: AST, targets: List[RowCol]) -> Dict[RowCol, AST]:
    stack = [tree]
    target_set = set(targets)
    results = {}

    while stack:
        node = stack.pop()
        if hasattr(node, "lineno"):
            pos = (node.lineno, node.col_offset)
            if pos in target_set:
                results[pos] = node
        stack.extend(iter_child_nodes(node))

    return results
