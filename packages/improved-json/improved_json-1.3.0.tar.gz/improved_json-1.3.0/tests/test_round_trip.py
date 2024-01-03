from copy import deepcopy
from pathlib import Path
import unittest

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
path = Path("/a/b/c")


def _rt(x):
    return improved_json.loads(improved_json.dumps(x))


class TestRoundTrip(unittest.TestCase):
    """
    Test improved_json's json encoding and decoding to ensure roundtrips work
    """

    def test_standard(self):
        self.assertEqual(standard, _rt(standard))

    def test_value(self):
        new = deepcopy(standard)
        new["other"] = path
        self.assertEqual(new, _rt(new))

    def test_list(self):
        new = deepcopy(standard)
        new["list"] = [path]
        self.assertEqual(new, _rt(new))

    def test_dict(self):
        new = deepcopy(standard)
        new["dict"] = {"8": path}
        self.assertEqual(new, _rt(new))

    def test_dict_key(self):
        new = deepcopy(standard)
        new[path] = new["dict"]
        del new["dict"]
        self.assertEqual(new, _rt(new))


if __name__ == "__main__":
    unittest.main()
