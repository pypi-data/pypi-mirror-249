from pathlib import Path
import typing
import json

from .type_check import improved_json_type, json_type


# Uncommon strings to ensure we don't over-aggressively
# dicts that happen to match our encoding but aren't ours
PATH_ID = "pathlib.Path s#*E3"


class Decoder(json.JSONDecoder):
    """
    A custom json decoder that supports pathlib.Path objects
    """

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self._object_hook, *args, **kwargs)

    def _object_hook(self, obj: json_type) -> improved_json_type:
        """
        On decode, if a pathlib.Path is detected, decode it
        """
        if isinstance(obj, dict) and len(obj) == 2 and obj.get("tid", None) == PATH_ID and "path" in obj:
            p = obj["path"]
            if isinstance(p, str):
                return Path(p)
        return typing.cast(improved_json_type, obj)  # cast for mypy


class Encoder(json.JSONEncoder):
    """
    A custom json encoder that supports pathlib.Path objects
    """

    def default(self, o: improved_json_type) -> improved_json_type:
        """
        On encode, if a pathlib.Path is detected, encode it
        """
        if isinstance(o, Path):
            return {"tid": PATH_ID, "path": str(o)}
        return super().default(o)
