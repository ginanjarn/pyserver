from functools import partial
from dataclasses import field, fields, is_dataclass
from keyword import iskeyword
from typing import TypeVar

# dict keys
_KEY_OPTIONAL = "optional"

_UNDEFINED = "undefined"
"""support for undefined value"""
_Dataclass = TypeVar("_Dataclass")
"""support for dataclass type"""


optional_field = partial(field, metadata={_KEY_OPTIONAL: True})
"""omited field if undefined"""


def _strip_keyword(s: str) -> str:
    return s.rstrip("_")


def _escape_keyword(s: str) -> str:
    if iskeyword(s):
        return f"{s}_"
    return s


def to_dict(obj: _Dataclass) -> dict:
    """convert class to dict"""

    if not is_dataclass(obj):
        return obj

    data = {}
    for f in fields(obj):
        value = getattr(obj, f.name)
        # omit optional field if None
        if value is None and f.metadata.get(_KEY_OPTIONAL):
            continue
        data[_strip_keyword(f.name)] = to_dict(value)

    return data


def from_dict(data: dict, cls: _Dataclass) -> _Dataclass:
    """new class instance from data"""

    if not isinstance(data, dict):
        return data

    kwargs = {}

    for f in fields(cls):
        value = data.get(f.name, _UNDEFINED)
        if value is _UNDEFINED:
            if not f.metadata.get(_KEY_OPTIONAL, False):
                raise KeyError(f"missing {f.name!r} field")
            value = None

        kwargs[_escape_keyword(f.name)] = value

    return cls(**kwargs)
