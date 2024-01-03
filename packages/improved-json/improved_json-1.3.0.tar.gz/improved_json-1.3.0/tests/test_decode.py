from copy import deepcopy
from pathlib import Path
import unittest
import json

from improved_json.improved_json import PATH_PREFIX
import improved_json

standard = {
    "list": [0, 1, 2],
    "dict": {"a": 1, "b": 2, "c": 3},
    "null": None,
    "bool": True,
    "int": 9,
    "float": 3.5,
    "str": "str",
    "tuple": (4, 5, 6),  # To be nice
    "other": "value",
}
standard_s = json.dumps(standard)
path = Path("/a/b/c")
path_s = f"{PATH_PREFIX}{path}"


class TestDecode(unittest.TestCase):
    """
    Test improved_json's json decoding abilities
    """

    def test_standard(self):
        self.assertEqual(improved_json.dumps(standard), standard_s)

    def test_value(self):
        new = deepcopy(standard)
        new["other"] = path
        new_s = standard_s.replace(standard["other"], path_s)
        self.assertEqual(improved_json.dumps(new), new_s)

    def test_list(self):
        new = deepcopy(standard)
        new["list"] = [path]
        new_s = standard_s.replace(json.dumps(standard["list"]), json.dumps([path_s]))
        self.assertEqual(improved_json.dumps(new), new_s)

    def test_tuple(self):
        new = deepcopy(standard)
        new["tuple"] = (path,)
        new_s = standard_s.replace(json.dumps(standard["tuple"]), json.dumps((path_s,)))
        self.assertEqual(improved_json.dumps(new), new_s)

    def test_dict(self):
        new = deepcopy(standard)
        new["dict"] = {"8": path}
        new_s = standard_s.replace(json.dumps(standard["dict"]), json.dumps({8: path_s}))
        self.assertEqual(improved_json.dumps(new), new_s)

    def test_dict_key(self):
        new = deepcopy(standard)
        new[path] = new["other"]  # Other because it is last and order matters
        del new["other"]
        new_s = standard_s.replace("other", path_s)
        self.assertEqual(improved_json.dumps(new), new_s)


if __name__ == "__main__":
    unittest.main()
