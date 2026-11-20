"""Small JSON helpers shared by the public command line tools."""
import json
import math
from pathlib import Path


def write_json(path, value):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                 allow_nan=False) + "\n", encoding="utf-8")


def positive_int(value):
    value = int(value)
    if value < 1:
        raise ValueError("Expected an integer >= 1")
    return value


def positive_float(value):
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError("Expected a positive finite number")
    return value
