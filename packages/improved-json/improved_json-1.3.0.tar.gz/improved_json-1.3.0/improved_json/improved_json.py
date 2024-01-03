from typing import Any, cast
from pathlib import Path
import json

from .type_check import type_check, improved_json_type


# TODO: tuple support
__all__ = (
    "loadf",
    "dumpf",
    "loads",
    "dumps",
)


PATH_PREFIX = "Path s#*E3|: "


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
    ret = _replace(json.loads(data, **kwargs), False)
    type_check(ret, type_)
    return ret


def dumps(obj: improved_json_type, **kwargs) -> str:
    """
    Dump the improved json object to a string
    Other arguments are otherwise passed through to json.dumps
    :param obj: The json object to convert to a string
    :return: obj represented as a string
    """
    return json.dumps(_replace(obj, True), **kwargs)


def _replace(o: improved_json_type, to_string: bool) -> improved_json_type:
    if isinstance(o, dict):
        return {cast(str | Path, _replace(i, to_string)): _replace(k, to_string) for i, k in o.items()}
    if isinstance(o, (tuple, list)):  # Support tuples to be nice
        return type(o)(_replace(i, to_string) for i in o)
    if to_string:
        if isinstance(o, Path):
            return f"{PATH_PREFIX}{o}"
    elif isinstance(o, str) and o.startswith(PATH_PREFIX):
        return Path(o[len(PATH_PREFIX) :])
    return o
