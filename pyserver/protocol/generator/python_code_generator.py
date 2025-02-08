import keyword
import re
from collections import defaultdict
from functools import partial
from textwrap import indent
from typing import Any, List

try:
    from models import (
        Enumeration,
        Structure,
        TypeAlias,
        Request,
        Notification,
        Base,
        Reference,
        Array,
        Tuple,
        Map,
        Literal,
        StringLiteral,
        Or,
        And,
    )
except ImportError:
    from .models import (
        Enumeration,
        Structure,
        TypeAlias,
        Request,
        Notification,
        Base,
        Reference,
        Array,
        Tuple,
        Map,
        Literal,
        StringLiteral,
        Or,
        And,
    )

HEADER = """\
###############################################################################
#
# This module is generated from 'metaModel.json'.
#
# Follow link below to see the reference detail:
#   https://github.com/microsoft/vscode-languageserver-node/blob/main/protocol/metaModel.json
#
###############################################################################
"""

IMPORTS = """\
from dataclasses import dataclass, field
from functools import partial
from typing import List, Tuple, Dict, Union, Literal
"""

SUPPORTS = '''\
optional_field = partial(field, metadata={"optional": True})
"""optional field"""
uint = int
"""unsigned type compatibility"""
URI = str
"""Uniform Resource Identifier.
See https://tools.ietf.org/html/rfc3986"""
DocumentUri = URI
"""URI with scheme = \'file\'"""
'''


class Generator:
    def __init__(self, elements: List[Any]) -> None:
        self._elements = elements

    def generate(self) -> str:
        predefined_elements = [HEADER, IMPORTS, SUPPORTS]
        elements_code = [self._generate_element_code(e) for e in self._elements]
        return "\n\n".join(predefined_elements + elements_code)

    def _generate_element_code(self, element: Any) -> str:
        if not element:
            return ""

        func = {
            # class
            Enumeration: self._generate_enumeration,
            Structure: self._generate_structure,
            TypeAlias: self._generate_typealias,
            Request: self._generate_request,
            Notification: self._generate_notification,
            # element
            Base: self._generate_base,
            Reference: self._generate_reference,
            Array: self._generate_array,
            Tuple: self._generate_tuple,
            Map: self._generate_map,
            Literal: self._generate_literal,
            StringLiteral: self._generate_stringLiteral,
            Or: self._generate_or,
            And: self._generate_and,
        }
        try:
            return func[type(element)](element)
        except KeyError as err:
            raise KeyError(f"unable find gererator for {err}") from err

    @staticmethod
    def _wrap_docstring(documentation: str) -> str:
        if not documentation:
            return ""

        docstring = f'"""{documentation}"""'
        if "\\" in documentation:
            # documentation contain escaped character assinged as raw string
            return f"r{docstring}"
        return docstring

    def _generate_enumeration(self, element: Enumeration) -> str:
        lines = []
        enum_name = element.name
        enum_type = self._generate_element_code(element.type)
        lines.append(f"{enum_name} = {enum_type}")
        if enum_doc := element.documentation:
            lines.append(self._wrap_docstring(enum_doc))

        for enum_value in element.values:
            val_name = f"{enum_name}{enum_value.name}"
            val_value = enum_value.value
            lines.append(f"{val_name}: {enum_name} = {val_value!r}")
            if val_doc := enum_value.documentation:
                lines.append(self._wrap_docstring(val_doc))

        return "\n".join(lines)

    def _generate_structure(self, element: Structure) -> str:
        lines = []
        class_name = element.name
        class_doc = element.documentation
        extends_classes = [self._generate_element_code(i) for i in element.extends]
        mixins_classes = [self._generate_element_code(i) for i in element.mixins]

        parent_classes = ", ".join(extends_classes + mixins_classes)
        parents = f"({parent_classes})" if parent_classes else ""

        lines.extend(["@dataclass", f"class {class_name}{parents}:"])

        children_lines = []

        # class docstring
        if docstring := self._wrap_docstring(class_doc):
            children_lines.append(docstring)

        class_name_match = re.compile(rf"\b{class_name}\b")

        for property_ in element.properties:
            pname = property_.name
            pname = f"{pname}_" if keyword.iskeyword(pname) else pname
            ptype = self._generate_element_code(property_.type)
            pdoc = property_.documentation

            # quote type if same as the class name
            ptype = class_name_match.sub(f'"{class_name}"', ptype)

            line = f"{pname}: {ptype}"
            if property_.optional:
                line = f"{line} = optional_field()"

            children_lines.append(line)

            # property docstring
            if pdocstring := self._wrap_docstring(pdoc):
                children_lines.append(pdocstring)

        children = "\n".join(children_lines) or '""""""'

        indent_one = partial(indent, prefix="\t")
        lines.append(indent_one(children))

        return "\n".join(lines)

    def _generate_typealias(self, element: TypeAlias) -> str:
        lines = []
        alias_name = element.name
        defined_type = self._generate_element_code(element.type)
        tdoc = element.documentation
        lines.append(f'{alias_name} = "{defined_type}"')
        if docstring := self._wrap_docstring(tdoc):
            lines.append(docstring)

        return "\n".join(lines)

    def _generate_request(self, element: Request) -> str:
        return f"{element.typeName}Method = {element.method!r}"

    def _generate_notification(self, element: Notification) -> str:
        return f"{element.typeName}Method = {element.method!r}"

    def _generate_base(self, element: Base) -> str:
        type_map = defaultdict(
            lambda: element.name,
            {
                "null": "None",
                "string": "str",
                "boolean": "bool",
                "integer": "int",
                "uinteger": "uint",
                "decimal": "float",
            },
        )
        return type_map[element.name]

    def _generate_reference(self, element: Reference) -> str:
        return element.name

    def _generate_array(self, element: Array) -> str:
        return f"List[{self._generate_element_code(element.element)}]"

    def _generate_tuple(self, element: Tuple) -> str:
        items = [self._generate_element_code(i) for i in element.items]
        return f"Tuple[{', '.join(items)}]"

    def _generate_map(self, element: Map) -> str:
        key = self._generate_element_code(element.key)
        value = self._generate_element_code(element.value)
        return f"Dict[{key}, {value}]"

    def _generate_literal(self, element: Literal) -> str:
        return f"Literal[{element.value!r}]"

    def _generate_stringLiteral(self, element: StringLiteral) -> str:
        return f"Literal[{element.value!r}]"

    def _generate_or(self, element: Or) -> str:
        items = [self._generate_element_code(i) for i in element.items]
        return f"Union[{', '.join(items)}]"

    def _generate_and(self, element: Any) -> str:
        items = [self._generate_element_code(i) for i in element.items]
        return f"Union[{', '.join(items)}]"
