"""protocol model"""

import json
from collections import defaultdict
from dataclasses import dataclass, fields
from pathlib import Path
from typing import List, Any, AnyStr, Union


@dataclass
class Type:
    """type"""


def construct_type(data: dict, cls: Type) -> Type:
    kwargs = {}
    default_value_map = defaultdict(
        lambda: None,
        {str: "", int: 0, bool: False},
    )
    for field in fields(cls):
        default = default_value_map[field.type]
        kwargs[field.name] = data.get(field.name, default)

    return cls(**kwargs)


@dataclass
class BaseType(Type):
    name: str


@dataclass
class ReferenceType(Type):
    name: str


@dataclass
class ArrayType(Type):
    element: Type

    def __post_init__(self):
        self.element = get_type(self.element)


@dataclass
class TupleType(Type):
    items: List[Type]

    def __post_init__(self):
        self.items = [get_type(i) for i in self.items]


@dataclass
class MapType(Type):
    key: Type
    value: Type

    def __post_init__(self):
        self.key = get_type(self.key)
        self.value = get_type(self.value)


@dataclass
class AndType(Type):
    items: List[Type]

    def __post_init__(self):
        self.items = [get_type(i) for i in self.items]


@dataclass
class OrType(Type):
    items: List[Type]

    def __post_init__(self):
        self.items = [get_type(i) for i in self.items]


@dataclass
class LiteralType(Type):
    value: Any


@dataclass
class StringLiteralType(Type):
    value: AnyStr


kind_map = {
    "base": BaseType,
    "reference": ReferenceType,
    "array": ArrayType,
    "tuple": TupleType,
    "map": MapType,
    "and": AndType,
    "or": OrType,
    "literal": LiteralType,
    "stringLiteral": StringLiteralType,
}


def get_type(data: dict) -> Type:
    kind = data["kind"]
    cls = kind_map[kind]
    return construct_type(data, cls)


@dataclass
class MetaData:
    version: str


def get_meta_data(data: dict) -> MetaData:
    return construct_type(data, MetaData)


@dataclass
class TypeAlias(Type):
    name: str
    type: Type
    documentation: str = ""
    since: str = ""

    def __post_init__(self):
        self.type = get_type(self.type)


def get_type_alias(data: dict) -> TypeAlias:
    return construct_type(data, TypeAlias)


@dataclass
class EnumerationValue(Type):
    name: str
    value: Union[str, int]
    documentation: str = ""
    since: str = ""


@dataclass
class Enumeration(Type):
    name: str
    type: Type
    values: List[EnumerationValue]
    supportsCustomValues: bool = False
    documentation: str = ""
    since: str = ""

    def __post_init__(self):
        self.type = get_type(self.type)
        self.values = [construct_type(v, EnumerationValue) for v in self.values]


def get_enumeration(data: dict) -> Enumeration:
    return construct_type(data, Enumeration)


@dataclass
class StructureProperty:
    name: str
    type: Type
    optional: bool = False
    documentation: str = ""
    since: str = ""

    def __post_init__(self):
        self.type = get_type(self.type)


@dataclass
class Structure(Type):
    name: str
    properties: List[StructureProperty]
    extends: List[Type] = None
    mixins: List[Type] = None
    documentation: str = ""
    since: str = ""

    def __post_init__(self):
        self.properties = [
            construct_type(p, StructureProperty) for p in self.properties
        ]
        self.extends = (
            [get_type(e) for e in self.extends] if self.extends is not None else []
        )
        self.mixins = (
            [get_type(m) for m in self.mixins] if self.mixins is not None else []
        )


def get_structure(data: dict) -> Structure:
    return construct_type(data, Structure)


def load_model(path: Path) -> List[Type]:
    model_path = Path(path)
    data = json.loads(model_path.read_text(encoding="utf-8"))

    types = []
    meta_data = [get_meta_data(data["metaData"])]
    types.extend(meta_data)
    enumeration = [get_enumeration(e) for e in data["enumerations"]]
    types.extend(enumeration)
    structures = [get_structure(s) for s in data["structures"]]
    types.extend(structures)
    typealiases = [get_type_alias(s) for s in data["typeAliases"]]
    types.extend(typealiases)

    return types
