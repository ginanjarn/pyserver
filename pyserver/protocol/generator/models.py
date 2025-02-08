import enum
from dataclasses import dataclass, field
from typing import List, Any


class TypeKind(enum.Enum):
    Base = "base"
    Reference = "reference"
    Array = "array"
    Tuple = "tuple"
    Map = "map"
    Literal = "literal"
    StringLiteral = "stringLiteral"
    Or = "or"
    And = "and"


@dataclass
class Type:
    """"""

    kind: str


@dataclass
class Base(Type):
    name: str


@dataclass
class Reference(Type):
    name: str


@dataclass
class Array(Type):
    element: Type

    def __post_init__(self):
        self.element = create_type(self.element)


@dataclass
class Tuple(Type):
    items: List[Type]

    def __post_init__(self):
        self.items = [create_type(t) for t in self.items]


@dataclass
class Map(Type):
    key: Type
    value: Type

    def __post_init__(self):
        self.key = create_type(self.key)
        self.value = create_type(self.value)


@dataclass
class Literal(Type):
    value: Any


@dataclass
class StringLiteral(Type):
    value: str


@dataclass
class Or(Type):
    items: List[Type]

    def __post_init__(self):
        self.items = [create_type(t) for t in self.items]


@dataclass
class And(Type):
    items: List[Type]

    def __post_init__(self):
        self.items = [create_type(t) for t in self.items]


_type_map = {
    TypeKind.Base: Base,
    TypeKind.Reference: Reference,
    TypeKind.Array: Array,
    TypeKind.Tuple: Tuple,
    TypeKind.Map: Map,
    TypeKind.Literal: Literal,
    TypeKind.StringLiteral: StringLiteral,
    TypeKind.Or: Or,
    TypeKind.And: And,
}


def create_type(scheme: dict) -> Type:
    if scheme is None:
        return None

    kind = TypeKind(scheme["kind"])
    return _type_map[kind](**scheme)


@dataclass
class EnumValue:
    name: str
    value: str
    documentation: str = field(default="", repr=False)
    since: str = "0.1.0"
    proposed: bool = False


@dataclass
class Enumeration:
    name: str
    type: Type
    values: List[EnumValue] = field(default_factory=list)
    documentation: str = field(default="", repr=False)
    supportsCustomValues: bool = False
    since: str = "0.1.0"
    proposed: bool = False

    def __post_init__(self):
        self.type = create_type(self.type)
        self.values = [EnumValue(**v) for v in self.values]


@dataclass
class Property:
    name: str
    type: Type
    documentation: str = field(default="", repr=False)
    optional: bool = False
    since: str = "0.1.0"
    sinceTags: List[str] = field(default_factory=list)
    proposed: bool = False
    deprecated: bool = False

    def __post_init__(self):
        self.type = create_type(self.type)


@dataclass
class Structure:
    name: str
    properties: List[Property] = field(default_factory=list)
    extends: List[Type] = field(default_factory=list)
    mixins: List[Type] = field(default_factory=list)
    documentation: str = field(default="", repr=False)
    since: str = "0.1.0"
    sinceTags: List = field(default_factory=list)
    proposed: bool = False
    deprecated: bool = False

    def __post_init__(self):
        self.properties = [Property(**p) for p in self.properties]
        self.extends = [create_type(t) for t in self.extends]
        self.mixins = [create_type(t) for t in self.mixins]


@dataclass
class TypeAlias:
    name: str
    type: Type
    documentation: str = field(default="", repr=False)
    since: str = "0.1.0"
    sinceTags: List = field(default_factory=list)
    proposed: bool = False
    deprecated: bool = False

    def __post_init__(self):
        self.type = create_type(self.type)


class MessageDirection(enum.Enum):
    ClientToServer = "clientToServer"
    ServerToClient = "serverToClient"
    Both = "both"


@dataclass
class Request:
    method: str
    typeName: str
    messageDirection: MessageDirection
    registrationMethod: str = ""
    result: Type = None
    errorData: Type = None
    params: Type = None
    partialResult: Type = None
    registrationOptions: Type = None
    documentation: str = field(default="", repr=False)
    since: str = "0.1.0"
    sinceTags: List = field(default_factory=list)
    proposed: bool = False
    deprecated: bool = False

    def __post_init__(self):
        self.result = create_type(self.result)
        self.params = create_type(self.params)
        self.errorData = create_type(self.errorData)
        self.messageDirection = MessageDirection(self.messageDirection)
        self.partialResult = create_type(self.partialResult)
        self.registrationOptions = create_type(self.registrationOptions)


@dataclass
class Notification:
    method: str
    typeName: str
    messageDirection: MessageDirection
    registrationMethod: str = ""
    params: Type = None
    registrationOptions: Type = None
    documentation: str = field(default="", repr=False)
    since: str = "0.1.0"
    sinceTags: List = field(default_factory=list)
    proposed: bool = False
    deprecated: bool = False

    def __post_init__(self):
        self.params = create_type(self.params)
        self.messageDirection = MessageDirection(self.messageDirection)
        self.registrationOptions = create_type(self.registrationOptions)
