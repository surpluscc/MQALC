"""Maintainability index using Radon mi_visit(multi=True)."""
import argparse
import hashlib
from importlib.metadata import version
from pathlib import Path

from .common import write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    from radon.metrics import mi_rank, mi_visit

    root = args.source
    if not root.exists():
        parser.error("Source does not exist")
    paths = [root] if root.is_file() else sorted(root.rglob("*.py"))
    if not paths:
        parser.error("No Python source files found")
    rows = []
    for path in paths:
        row = {"file": path.name if root.is_file() else path.relative_to(root).as_posix()}
        try:
            raw = path.read_bytes()
            row["sha256"] = hashlib.sha256(raw).hexdigest()
            score = mi_visit(raw.decode("utf-8-sig"), multi=True)
            row.update(status="ok", MI=score, rank=mi_rank(score))
        except Exception as exc:
            row.update(status="error", error=type(exc).__name__)
        rows.append(row)
    valid = [r["MI"] for r in rows if r["status"] == "ok"]
    write_json(args.output, {"radon_version": version("radon"), "multi": True,
                            "n_total": len(rows), "n_valid": len(valid),
                            "mean_MI": sum(valid) / len(valid) if valid else None,
                            "files": rows})
    if len(valid) != len(rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
