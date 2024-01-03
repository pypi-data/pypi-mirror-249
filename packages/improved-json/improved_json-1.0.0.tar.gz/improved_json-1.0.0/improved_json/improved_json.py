from pathlib import Path
from typing import Any
import json

from .coders import Decoder, Encoder
from .type_check import type_check, improved_json_type


__all__ = (
    "loadf",
    "dumpf",
    "loads",
    "dumps",
    "allow_override_cls",
)


# Change to allow setting cls in load functions
# Doing so negates the custom decoding abilities of these functions though
allow_override_cls: bool = False


def loadf(path: str | Path, *args, **kwargs) -> improved_json_type:
    """
    A wrapper around loads that loads the data field from the given file path
    Other arguments are otherwise passed through to loads
    :param path: The file path to load
    """
    if isinstance(path, str):
        path = Path(path)
    with path.open("r") as f:
        data = f.read()
    return loads(data, *args, **kwargs)


def dumpf(path: str | Path, *args, **kwargs) -> int:
    """
    A wrapper around dumps that outputs the data to the given path
    Other arguments are otherwise passed through to dumps
    :param path: The file path to write to
    :return: The number of bytes written
    """
    out: str = dumps(*args, **kwargs)
    if isinstance(path, str):
        path = Path(path)
    with path.open("w") as f:
        return f.write(out)


def loads(data: str | bytes, type_: type | Any = Any, **kwargs) -> improved_json_type:
    """
    Load a json object from the string data
    Other arguments are otherwise passed through to json.loads
    Supports type_ containing some parameterized generic types from the typing module
    Also supports some parameterized generic without parameters (i.e. as generics)
    Raises ValueError if type_ is invalid
    :param data: The string to load
    :param type_: The required return type
    :return: The json object constructed from data
    """
    if "cls" in kwargs and not allow_override_cls:
        raise RuntimeError("Cannot overload cls in a load function; set allow_override_cls to change this")
    if "cls" not in kwargs:
        kwargs["cls"] = Decoder
    ret = json.loads(data, **kwargs)
    type_check(ret, type_)
    return ret


def dumps(obj: improved_json_type, **kwargs) -> str:
    """
    Dump the improved json object to a string
    Other arguments are otherwise passed through to json.dumps
    :param obj: The json object to convert to a string
    :return: obj represented as a string
    """
    if "cls" in kwargs and not allow_override_cls:
        raise RuntimeError("Cannot overload cls in a load function; set allow_override_cls to change this")
    if "cls" not in kwargs:
        kwargs["cls"] = Encoder
    return json.dumps(obj, **kwargs)
