"""Protocol Converter"""

from dataclasses import is_dataclass, fields, _ATOMIC_TYPES
from enum import Enum
from typing import Dict, Any, TypeVar, get_args

try:
    import protocol_types
except ImportError:
    from . import protocol_types

ProtocolClass = TypeVar("ProtocolClass")


class _MISSING:
    """Type of missing data"""


def dict_to_class(obj: Dict[str, Any], class_type: Any) -> ProtocolClass:
    """convert dict to class"""
    return _construct_object(obj, class_type)


def _construct_object(obj: Dict[str, Any], class_type: Any) -> Any:
    # see '_asdict_inner' in dataclass module.
    if type(obj) in _ATOMIC_TYPES:
        return obj

    if is_dataclass(class_type):
        return _construct_dataclass(obj, class_type)

    # class_type is class or type object
    if isinstance(class_type, type):
        return class_type(obj)

    # class_type defined as string literal
    if cls := getattr(protocol_types, class_type):
        return _construct_object(obj, cls)

    # class is substitution eg: Uniom, List, etc
    if args := get_args(class_type):
        for tp in args:
            try:
                return _construct_object(obj, tp)
            except ValueError:
                pass

    raise ValueError(f"no match constructor {class_type} for {obj}")


def _construct_dataclass(obj: Dict[str, Any], class_type: Any) -> ProtocolClass:
    kwargs = {}
    for field in fields(class_type):
        field_type = field.type
        field_name = field.name
        value = obj.get(field_name, _MISSING)

        if not field.metadata.get("optional", False) and value is _MISSING:
            raise ValueError(f"field {field_name!r} is missing")

        kwargs[field_name] = _construct_object(value, field_type)

    return class_type(**kwargs)


def class_to_dict(obj: ProtocolClass) -> Dict[str, Any]:
    """convert class to dict"""
    return _from_object(obj)


def _from_object(obj: Any) -> Any:
    # see '_asdict_inner' in dataclass module.
    if type(obj) in _ATOMIC_TYPES:
        return obj

    if is_dataclass(obj):
        return _from_dataclass(obj)

    if isinstance(obj, Enum):
        return obj.value

    raise ValueError(f"unable get dict from {obj}")


def _from_dataclass(obj: Any, cls: Any = None) -> Dict[str, Any]:
    cls_dict = {}
    for field in fields(obj):
        value = getattr(obj, field.name)
        if field.metadata.get("optional", False) and value is None:
            # omit optional unset field
            value = _MISSING

        cls_dict[field.name] = _from_object(value)

    return {k: v for k, v in cls_dict.items() if v is not _MISSING}
