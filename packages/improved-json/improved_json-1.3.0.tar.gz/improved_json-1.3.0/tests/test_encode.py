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
    "other": "value",
}
standard_s = json.dumps(standard)
path = Path("/a/b/c")
path_s = f"{PATH_PREFIX}{path}"


class TestEncode(unittest.TestCase):
    """
    Test improved_json's json encoding abilities
    """

    def test_standard(self):
        self.assertEqual(improved_json.loads(standard_s), standard)

    def test_value(self):
        new = deepcopy(standard)
        new["other"] = path
        new_s = standard_s.replace(standard["other"], path_s)
        self.assertEqual(improved_json.loads(new_s), new)

    def test_list(self):
        new = deepcopy(standard)
        new["list"] = [path]
        new_s = standard_s.replace(json.dumps(standard["list"]), json.dumps([path_s]))
        self.assertEqual(improved_json.loads(new_s), new)

    def test_dict(self):
        new = deepcopy(standard)
        new["dict"] = {"8": path}
        new_s = standard_s.replace(json.dumps(standard["dict"]), json.dumps({8: path_s}))
        self.assertEqual(improved_json.loads(new_s), new)

    def test_dict_key(self):
        new = deepcopy(standard)
        new[path] = new["dict"]
        del new["dict"]
        new_s = standard_s.replace("dict", path_s)
        self.assertEqual(improved_json.loads(new_s), new)


if __name__ == "__main__":
    unittest.main()
