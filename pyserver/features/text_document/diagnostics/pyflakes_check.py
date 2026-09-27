from ast import parse, AST, iter_child_nodes
from collections import defaultdict, namedtuple
from typing import Iterator, List, Dict

from pyflakes.checker import Checker
from pyflakes.messages import Message

from . import Diagnostic, TextRange, KIND_ERROR, KIND_WARNING

RowCol = namedtuple("RowCol", ["row", "column"])

FLAKE8_PYFLAKES_CODES = defaultdict(
    lambda: "F999",
    {
        "UnusedImport": "F401",
        "ImportShadowedByLoopVar": "F402",
        "ImportStarUsed": "F403",
        "LateFutureImport": "F404",
        "ImportStarUsage": "F405",
        "ImportStarNotPermitted": "F406",
        "FutureFeatureNotDefined": "F407",
        "PercentFormatInvalidFormat": "F501",
        "PercentFormatExpectedMapping": "F502",
        "PercentFormatExpectedSequence": "F503",
        "PercentFormatExtraNamedArguments": "F504",
        "PercentFormatMissingArgument": "F505",
        "PercentFormatMixedPositionalAndNamed": "F506",
        "PercentFormatPositionalCountMismatch": "F507",
        "PercentFormatStarRequiresSequence": "F508",
        "PercentFormatUnsupportedFormatCharacter": "F509",
        "StringDotFormatInvalidFormat": "F521",
        "StringDotFormatExtraNamedArguments": "F522",
        "StringDotFormatExtraPositionalArguments": "F523",
        "StringDotFormatMissingArgument": "F524",
        "StringDotFormatMixingAutomatic": "F525",
        "FStringMissingPlaceholders": "F541",
        "TStringMissingPlaceholders": "F542",
        "MultiValueRepeatedKeyLiteral": "F601",
        "MultiValueRepeatedKeyVariable": "F602",
        "TooManyExpressionsInStarredAssignment": "F621",
        "TwoStarredExpressions": "F622",
        "AssertTuple": "F631",
        "IsLiteral": "F632",
        "InvalidPrintSyntax": "F633",
        "IfTuple": "F634",
        "BreakOutsideLoop": "F701",
        "ContinueOutsideLoop": "F702",
        "YieldOutsideFunction": "F704",
        "ReturnOutsideFunction": "F706",
        "DefaultExceptNotLast": "F707",
        "DoctestSyntaxError": "F721",
        "ForwardAnnotationSyntaxError": "F722",
        "RedefinedWhileUnused": "F811",
        "UndefinedName": "F821",
        "UndefinedExport": "F822",
        "UndefinedLocal": "F823",
        "UnusedIndirectAssignment": "F824",
        "DuplicateArgument": "F831",
        "UnusedVariable": "F841",
        "UnusedAnnotation": "F842",
        "RaiseNotImplemented": "F901",
    },
)
FLAKE8_PYFLAKES_FIELDS = defaultdict(
    lambda: (),
    {
        "UnusedImport": ("name",),
        "ImportShadowedByLoopVar": ("name", "orig_lineno"),
        "ImportStarUsed": ("modname",),
        "LateFutureImport": (),
        "ImportStarUsage": ("name", "from_list"),
        "ImportStarNotPermitted": ("modname",),
        "FutureFeatureNotDefined": ("name",),
        "PercentFormatInvalidFormat": ("error",),
        "PercentFormatExpectedMapping": (),
        "PercentFormatExpectedSequence": (),
        "PercentFormatExtraNamedArguments": (),
        "PercentFormatMissingArgument": ("missing_arguments",),
        "PercentFormatMixedPositionalAndNamed": (),
        "PercentFormatPositionalCountMismatch": (),
        "PercentFormatStarRequiresSequence": (),
        "PercentFormatUnsupportedFormatCharacter": (),
        "StringDotFormatInvalidFormat": (),
        "StringDotFormatExtraNamedArguments": (),
        "StringDotFormatExtraPositionalArguments": (),
        "StringDotFormatMissingArgument": ("missing_arguments",),
        "StringDotFormatMixingAutomatic": (),
        "FStringMissingPlaceholders": (),
        "TStringMissingPlaceholders": (),
        "MultiValueRepeatedKeyLiteral": ("key",),
        "MultiValueRepeatedKeyVariable": ("key",),
        "TooManyExpressionsInStarredAssignment": (),
        "TwoStarredExpressions": (),
        "AssertTuple": (),
        "IsLiteral": (),
        "InvalidPrintSyntax": (),
        "IfTuple": (),
        "BreakOutsideLoop": (),
        "ContinueOutsideLoop": (),
        "YieldOutsideFunction": (),
        "ReturnOutsideFunction": (),
        "DefaultExceptNotLast": (),
        "DoctestSyntaxError": (),
        "ForwardAnnotationSyntaxError": ("annotation",),
        "RedefinedWhileUnused": ("name", "orig_lineno"),
        "UndefinedName": ("name",),
        "UndefinedExport": ("name",),
        "UndefinedLocal": ("name", "orig_lineno"),
        "UnusedIndirectAssignment": ("type", "name"),
        "DuplicateArgument": ("name",),
        "UnusedVariable": ("names",),
        "UnusedAnnotation": ("names",),
        "RaiseNotImplemented": (),
    },
)


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
        text_range = TextRange(min(a, b), max(a, b))
        yield Diagnostic(text_range, KIND_ERROR, "F999", msg, "ast")

    def _get_warnings(self, node: AST, filename: str) -> Iterator[Diagnostic]:

        check = Checker(node, filename=filename)
        check.messages.sort(key=lambda m: (m.lineno, m.col))

        node_map = find_nodes(node, [(m.lineno, m.col) for m in check.messages])
        yield from (self._build_warning(m, node_map) for m in check.messages)

    def _build_warning(
        self, message: Message, node_map: Dict[RowCol, AST]
    ) -> Diagnostic:

        node = node_map[(message.lineno, message.col)]
        a = RowCol(node.lineno - 1, node.col_offset)
        b = RowCol(node.end_lineno - 1, node.end_col_offset)
        start = min(a, b)
        end = max(a, b)

        text_range = TextRange(start, end)
        text_msg = message.message % message.message_args

        pyflakes_msg_name = type(message).__name__
        code = FLAKE8_PYFLAKES_CODES[pyflakes_msg_name]
        data = dict(zip(FLAKE8_PYFLAKES_FIELDS[pyflakes_msg_name], message.message_args))

        return Diagnostic(text_range, KIND_WARNING, code, text_msg, "pyflakes", data)


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
