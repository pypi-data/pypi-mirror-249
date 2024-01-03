from typing import Any, List, Dict, Optional, Union, Container, Iterable, get_origin, get_args, cast
from types import NoneType, UnionType
from collections import abc
from pathlib import Path


json_type = None | str | int | float | bool | dict[str, "json_type"] | list["json_type"]
improved_json_type = (
    None | str | int | float | bool | dict[str, "improved_json_type"] | list["improved_json_type"] | Path
)

lists = (list, List, Container, abc.Container, Iterable, abc.Iterable)
dicts = (dict, Dict, Container, abc.Container, Iterable, abc.Iterable)
unions = (UnionType, Union, Optional)
custom = (Path,)


def _test(cond: bool, obj: improved_json_type, type_: type) -> None:
    """
    :param cond: If False, raise a TypeError
    :param obj: The object being type checked
    :param type_: The type obj_ should be
    """
    if not cond:
        raise TypeError(f"{obj} is not of type: {type_}")


def type_check(obj: improved_json_type, type_: type) -> None:
    """
    Supports type_ containing some parameterized generic types from the typing module
    Also supports some parameterized generic without parameters (i.e. as generics)
    Raises TypeError if obj is not of type type_
    Raises ValueError if type_ is invalid
    :obj: A valid json object to type check
    :type_: The type to check if obj is
    """
    if type_ == Any:
        return
    for i in (bool, int, float, str, NoneType):
        if type_ == i:
            _test(isinstance(obj, i), obj, type_)
            return
    if type_ == Path:
        _test(isinstance(obj, Path), obj, type_)
        return
    # Composite type
    origin = get_origin(type_)
    if origin is None:
        if type_ in unions:
            raise ValueError(f"Union types must have a parameter: {type_}")
        origin = type_
    if origin in lists:
        _test(isinstance(obj, list), obj, type_)
        _check_list(cast(list[improved_json_type], obj), type_)
        return
    if origin in dicts:
        _test(isinstance(obj, dict), obj, type_)
        _check_dict(cast(dict[str, improved_json_type], obj), type_)
        return
    if origin in unions:
        for i in get_args(type_):
            try:
                type_check(obj, i)
                return
            except TypeError:
                pass
        _test(False, obj, type_)
    raise ValueError("Bad input type found in obj; this is not a json!")


def _check_dict(obj: dict[str, improved_json_type], type_: type) -> None:
    """
    Raises TypeError if obj is not of type type_
    Raises ValueError if type_ is invalid
    :param obj: A dict to check the type of
    :return: True if obj is of type type_
    """
    args = get_args(type_)
    if not args:
        return
    if len(args) != 2:
        raise ValueError(f"dict object may only have 0 or 2 parameters: {type_}")
    if args[0] != str:
        raise ValueError("dict first parameter must be str")
    if len(args) == 2:
        for i in obj.values():
            type_check(i, args[1])


def _check_list(obj: list[improved_json_type], type_: type) -> None:
    """
    Raises TypeError if obj is not of type type_
    Raises ValueError if type_ is invalid
    :param obj: A list to check the type of
    :return: True if obj is of type type_
    """
    args = get_args(type_)
    if not args:
        return
    if len(args) > 1:
        raise ValueError(f"list object cannot have more than one parameter: {type_}")
    for i in obj:
        type_check(i, args[0])
