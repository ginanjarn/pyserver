"""python code generator"""

import re
from dataclasses import dataclass
from functools import partial
from keyword import iskeyword
from textwrap import indent
from typing import List, Iterator


try:
    import model as scheme_model
except ImportError:
    from . import model as scheme_model


def to_docstring(text: str) -> str:
    if not text:
        return ""

    quoted = f'"""{text}"""'
    if "\\" in text:
        return f"r{quoted}"
    return quoted


@dataclass
class PythonModel:
    """"""


@dataclass
class Property(PythonModel):
    name: str
    type: str
    documentation: str
    since: str
    optional: bool


@dataclass
class Class(PythonModel):
    name: str
    parents: List[str]
    documentation: str
    since: str
    properties: List[Property]


@dataclass
class EnumValue(PythonModel):
    name: str
    value: str
    documentation: str
    since: str


@dataclass
class EnumClass(PythonModel):
    name: str
    type: str
    documentation: str
    since: str
    values: List[EnumValue]


@dataclass
class Assignment(PythonModel):
    name: str
    type: str
    value: str
    documentation: str
    since: str


class PythonCodeGenerator:

    def __init__(self, models: List[PythonModel]) -> None:
        self.models = models

    def generate(self) -> Iterator[str]:
        required_imports = (
            '"""LSP Protocol Types"""\n'
            "\n"
            "from dataclasses import dataclass, field\n"
            "from enum import Enum\n"
            "from typing import TypeAlias, List, Tuple, Dict, Literal, Union, Any\n"
            "\n"
            "URI: TypeAlias = str\n"
            "DocumentUri: TypeAlias = str\n"
        )
        yield required_imports

        for model in self.models:
            if isinstance(model, Class):
                yield self.class_code(model)
            elif isinstance(model, EnumClass):
                yield self.enumclass_code(model)
            elif isinstance(model, Assignment):
                yield self.assignment_code(model)
            else:
                raise ValueError(f"unable handle model {type(model)}")

    def as_comment(self, text: str) -> str:
        return indent(text, prefix="# ")

    def property_code(self, p: Property, cls_name: str = "") -> str:
        code_lines = []
        p_type = p.type
        if match := re.search(rf"\b({cls_name})\b", p_type):
            match_text = match.group(1)
            p_type = p_type.replace(match_text, f'"{match_text}"')

        definition = f"{p.name}: {p_type}"
        if p.optional:
            definition += ' = field(metadata={"optional": True})'
        code_lines.append(definition)

        if doc := p.documentation:
            code_lines.append(to_docstring(doc))

        if since := p.since:
            code_lines.append(self.as_comment(f"since {since}"))

        return "\n".join(code_lines)

    def class_code(self, c: Class) -> str:
        indent_one = partial(indent, prefix="    ")

        code_lines = []
        parent = "" if not c.parents else "(" + ", ".join(c.parents) + ")"
        code_lines.append(f"@dataclass\nclass {c.name}{parent}:")

        if doc := c.documentation:
            code_lines.append(indent_one(to_docstring(doc)))
        if since := c.since:
            code_lines.append(indent_one(self.as_comment(f"since {since}")))

        for p in c.properties:
            code_lines.append(indent_one(self.property_code(p, cls_name=c.name)))

        if len(code_lines) == 1:
            code_lines.append(indent_one('""""""'))

        return "\n".join(code_lines)

    def enum_value_code(self, v: EnumValue) -> str:
        code_lines = []
        name = v.name
        if iskeyword(name):
            name = f"{name}_"
        code_lines.append(f"{name} = {v.value!r}")

        if doc := v.documentation:
            code_lines.append(to_docstring(doc))
        if since := v.since:
            code_lines.append(self.as_comment(f"since {since}"))

        return "\n".join(code_lines)

    def enumclass_code(self, c: EnumClass) -> str:
        indent_one = partial(indent, prefix="    ")

        code_lines = []
        code_lines.append(f"class {c.name}(Enum):")

        classmember_lines = []
        if doc := c.documentation:
            classmember_lines.append(to_docstring(doc))
        if since := c.since:
            classmember_lines.append(self.as_comment(f"since {since}"))
        for v in c.values:
            classmember_lines.append(self.enum_value_code(v))

        if not classmember_lines:
            classmember_lines.append('""""""')

        code_lines.append(indent_one("\n".join(classmember_lines)))
        return "\n".join(code_lines)

    def assignment_code(self, a: Assignment) -> str:
        type_ = f": {a.type} " if a.type else ""
        code_lines = [f"{a.name}{type_}= {a.value}"]
        if doc := a.documentation:
            code_lines.append(to_docstring(doc))
        if since := a.since:
            code_lines.append(self.as_comment(f"since {since}"))

        return "\n".join(code_lines)


class PythonDependencyManager:
    def __init__(self, models: List[PythonModel]) -> None:
        self.models = list(models)
        self._dependencies = {}
        self.generate_dependencies()

    def generate_dependencies(self):
        for model in self.models:
            self._dependencies[model.name] = list(self.get_dependencies(model))

    def get_dependencies(self, model: PythonModel) -> Iterator[str]:
        func_map = {
            Assignment: self.get_assignment_dependencies,
            Property: self.get_property_dependencies,
            Class: self.get_class_dependencies,
            EnumClass: self.get_enumclass_dependencies,
        }

        yield from func_map[type(model)](model)

    def get_assignment_dependencies(self, model: Assignment) -> Iterator[str]:
        yield from self.get_type(model.type)

        if model.type == "TypeAlias":
            yield from self.get_type(model.value)

    def get_class_dependencies(self, model: Class) -> Iterator[str]:
        for p in model.parents:
            yield from self.get_type(p)

        for p in model.properties:
            yield from self.get_property_dependencies(p)

    def get_property_dependencies(self, model: Property) -> Iterator[str]:
        yield from self.get_type(model.type)

    def get_enumclass_dependencies(self, model: EnumClass) -> Iterator[str]:
        yield from self.get_type(model.type)

    def get_type(self, type_: str) -> Iterator[str]:
        names = re.findall(r"([A-Za-z_]\w+)", type_)
        for name in names:
            yield name

            if name == "Literal":
                return

    def get_sorted_name(self) -> List[str]:
        def get_dependencies(name: str) -> List[str]:
            names = []
            deps = self._dependencies.get(name, [])
            for dep in deps:
                if dep == name:
                    continue
                names.extend(get_dependencies(dep))
            return names + [name]

        names = []
        for name in self._dependencies.keys():
            for dep in get_dependencies(name):
                if dep not in names:
                    names.append(dep)

        return names

    def get_model_with_name(self, name: str) -> PythonModel:
        for model in self.models:
            if model.name == name:
                return model

        print(f"model undefined: {name!r}")
        return None

    def get_sorted(self) -> Iterator[PythonModel]:
        for name in self.get_sorted_name():
            if model := self.get_model_with_name(name):
                yield model


class PythonTypeNameGetter:
    def get_name(self, model: scheme_model.Type) -> str:
        type_map = {
            scheme_model.BaseType: self.from_base_type,
            scheme_model.ReferenceType: self.from_reference_type,
            scheme_model.ArrayType: self.from_array_type,
            scheme_model.TupleType: self.from_tuple_type,
            scheme_model.MapType: self.from_map_type,
            scheme_model.AndType: self.from_and_type,
            scheme_model.OrType: self.from_or_type,
            scheme_model.LiteralType: self.from_literal_type,
            scheme_model.StringLiteralType: self.from_stringliteral_type,
        }
        try:
            return type_map[type(model)](model)
        except KeyError as e:
            print("error get name for:", model)
            raise e

    def from_base_type(self, model: scheme_model.BaseType) -> str:
        python_builtin_types = {
            "integer": "int",
            "uinteger": "int",
            "decimal": "float",
            "string": "str",
            "null": "None",
            "boolean": "bool",
        }
        return python_builtin_types.get(model.name, model.name)

    def from_reference_type(self, model: scheme_model.ReferenceType) -> str:
        # prevent RecursionError
        if model.name == "LSPAny":
            return "Any"
        return model.name

    def from_array_type(self, model: scheme_model.ArrayType) -> str:
        return f"List[{self.get_name(model.element)}]"

    def from_tuple_type(self, model: scheme_model.TupleType) -> str:
        types_ = ", ".join([self.get_name(i) for i in model.items])
        return f"Tuple[{types_}]"

    def from_map_type(self, model: scheme_model.MapType) -> str:
        key, value = self.get_name(model.key), self.get_name(model.value)
        return f"Dict[{key}, {value}]"

    def from_and_type(self, model: scheme_model.AndType) -> str:
        types_ = ", ".join([self.get_name(i) for i in model.items])
        return f"List[{types_}]"

    def from_or_type(self, model: scheme_model.OrType) -> str:
        types_ = ", ".join([self.get_name(i) for i in model.items])
        return f"Union[{types_}]"

    def from_literal_type(self, model: scheme_model.LiteralType) -> str:
        return f"Literal[{model.value}]"

    def from_stringliteral_type(self, model: scheme_model.StringLiteralType) -> str:
        return f"Literal[{model.value!r}]"


class PythonModelAdapter:
    def __init__(self, models: List[scheme_model.Type]) -> None:
        self.models = models

    def adapt(self) -> Iterator[PythonModel]:

        type_map = {
            scheme_model.MetaData: self.adapt_metadata,
            scheme_model.Enumeration: self.adapt_enumeration,
            scheme_model.Structure: self.adapt_structure,
            scheme_model.TypeAlias: self.adapt_typealias,
        }
        for model in self.models:
            yield from type_map[type(model)](model)

    def get_type_name(self, model: scheme_model.Type) -> str:
        return PythonTypeNameGetter().get_name(model)

    def adapt_metadata(self, model: scheme_model.MetaData) -> Iterator[Assignment]:
        yield Assignment("__lsp_version__", "", repr(model.version), "", "")

    def adapt_enumeration_value(
        self, model: scheme_model.EnumerationValue
    ) -> Iterator[EnumClass]:
        return EnumValue(model.name, model.value, model.documentation, model.since)

    def adapt_enumeration(self, model: scheme_model.Enumeration) -> Iterator[EnumClass]:
        enum_name = model.name
        enum_type = self.get_type_name(model.type)
        enum_values = [self.adapt_enumeration_value(v) for v in model.values]
        yield EnumClass(
            enum_name, enum_type, model.documentation, model.since, enum_values
        )

    def get_mixin_properties(self, model: scheme_model.Type) -> List[Property]:
        target_properties = []
        for m in self.models:
            if not isinstance(m, scheme_model.Structure):
                continue

            m: scheme_model.Structure
            if m.name == model.name:
                target_properties = m.properties
                break

        return target_properties

    def adapt_structure_property(
        self, model: scheme_model.StructureProperty
    ) -> Property:
        name = model.name
        name = f"{name}_" if iskeyword(name) else name
        return Property(
            name,
            self.get_type_name(model.type),
            model.documentation,
            model.since,
            model.optional,
        )

    def adapt_structure(self, model: scheme_model.Structure) -> Iterator[Class]:
        class_name = model.name
        class_parents = [self.get_type_name(p) for p in model.extends]
        class_documentation = model.documentation
        class_since = model.since
        class_properties = model.properties

        for mixin in model.mixins:
            class_properties.extend(self.get_mixin_properties(mixin))

        yield Class(
            class_name,
            class_parents,
            class_documentation,
            class_since,
            [self.adapt_structure_property(p) for p in class_properties],
        )

    def adapt_typealias(self, model: scheme_model.TypeAlias) -> Iterator[Assignment]:
        yield Assignment(
            model.name,
            "TypeAlias",
            self.get_type_name(model.type),
            model.documentation,
            model.since,
        )


def generate_code(models: List[scheme_model.Type]) -> Iterator[str]:
    """generate code from models"""
    adaptor = PythonModelAdapter(models)
    manager = PythonDependencyManager(adaptor.adapt())
    generator = PythonCodeGenerator(manager.get_sorted())
    yield from generator.generate()
