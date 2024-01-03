from typing import Optional, Any
from types import NoneType
from pathlib import Path
import unittest

from improved_json.type_check import type_check, lists, dicts

path = Path("/a/b/c")
path2 = Path("/d/e/f")


class TestTypeCheck(unittest.TestCase):
    """
    Test improved_json's json type checker
    """

    def test_basic(self):
        type_check(1, int)
        type_check(True, bool)
        type_check(2.5, float)
        type_check("s", str)
        type_check(None, NoneType)
        type_check(path, Path)
        with self.assertRaises(TypeError):
            type_check(True, int)
        with self.assertRaises(TypeError):
            type_check(1, bool)

    def test_bad_value(self):
        with self.assertRaises(ValueError):
            type_check(1, type)
        with self.assertRaises(ValueError):
            type_check([], list[int, int])
        with self.assertRaises(ValueError):
            type_check({}, dict[str])
        for dct in dicts:
            with self.assertRaises(ValueError):
                type_check({}, dct[int, int])
        with self.assertRaises(ValueError):
            type_check(1, Optional)

    def test_list(self):
        for lst in lists:
            type_check([], lst)
            type_check([1], lst)
            type_check([1, 1], lst)
            type_check([1, "b"], lst)
            type_check([], lst[int])
            type_check([1], lst[int])
            type_check([1, 2], lst[int])
            with self.assertRaises(TypeError):
                type_check([True], lst[int])
            with self.assertRaises(TypeError):
                type_check([1, True], lst[int])

    def test_dict(self):
        for dct in dicts:
            type_check({}, dct)
            type_check({"1": 2}, dct)
            type_check({"1": 2, "3": 4}, dct)
            type_check({path: 2, path2: 4}, dct)
            type_check({}, dct[str, int])
            type_check({"1": 2}, dct[str, int])
            type_check({"1": 2, "3": 4}, dct[str, int])
            type_check({path: 2, path2: 4}, dct[Path, int])
            with self.assertRaises(TypeError):
                type_check({"1": 2}, dct[str, bool])
            with self.assertRaises(TypeError):
                type_check({"1": 2, "3": "4"}, dct[str, int])
            with self.assertRaises(TypeError):
                type_check({"1": 2}, dct[Path, bool])

    def test_sublist(self):
        for lst in lists:
            type_check([[]], lst)
            type_check([[]], lst[lst])
            type_check([[]], lst[lst[int]])
            type_check([[0]], lst[lst[int]])
            with self.assertRaises(TypeError):
                type_check([[0]], lst[lst[str]])
            type_check([[0], ["a"]], lst[lst])
            with self.assertRaises(TypeError):
                type_check([[0], ["a"]], lst[lst[int]])

    def test_subdict(self):
        for dct in dicts:
            type_check({"1": {}}, dct)
            type_check({"1": {}}, dct[str, dct])
            type_check({"1": {}}, dct[str, dct[str, int]])
            type_check({"1": {"2": 3}}, dct[str, dct[str, int]])
            with self.assertRaises(TypeError):
                type_check({"1": {"2": 3}}, dct[str, dct[str, str]])
            type_check({"1": {"2": 3}, "4": {"5": "6"}}, dct[str, dct])
            with self.assertRaises(TypeError):
                type_check({"1": {"2": 3}, "4": {"5": "6"}}, dct[str, dct[str, int]])

    def test_union(self):
        type_check(None, Any)
        type_check(1, Any)
        type_check(None, Optional[int])
        type_check(1, Optional[int])
        type_check(None, int | None)
        type_check(1, int | None)


if __name__ == "__main__":
    unittest.main()
