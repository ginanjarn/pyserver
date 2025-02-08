from functools import partial
from dataclasses import field, fields, is_dataclass
from keyword import iskeyword
from typing import TypeVar


optional_field = partial(field, metadata={"optional": True})
"""omited field if undefined"""


def _strip_keyword(s: str) -> str:
    return s.rstrip("_")


def _escape_keyword(s: str) -> str:
    if iskeyword(s):
        return f"{s}_"
    return s


_Dataclass = TypeVar("_Dataclass")


def to_dict(obj: _Dataclass) -> dict:
    """convert class to dict"""

    if not is_dataclass(obj):
        return obj

    data = {}
    for f in fields(obj):
        value = getattr(obj, f.name)
        # omit optional field if None
        if value is None and f.metadata.get("optional"):
            continue
        data[_strip_keyword(f.name)] = to_dict(value)

    return data


def from_dict(data: dict, cls: _Dataclass) -> _Dataclass:
    """new class instance from data"""

    if not isinstance(data, dict):
        return data

    kwargs = {}

    undefined = "undefined"
    for f in fields(cls):
        value = data.get(f.name, undefined)
        if value is undefined:
            if not f.metadata.get("omitempty", False):
                raise ValueError(f"{f.name!r} field must defined")
            value = None

        kwargs[_escape_keyword(f.name)] = from_dict(value, f.type)

    return cls(**kwargs)
