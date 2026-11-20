"""Spearman and Kendall correlation for paired rank vectors."""
import argparse
import json
import math
from pathlib import Path

from .common import write_json


def correlation(a, b):
    from scipy.stats import kendalltau, spearmanr

    if len(a) != len(b) or len(a) < 2:
        raise ValueError("Provide equal-length paired vectors with at least two items")
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x)
           for x in a + b):
        raise ValueError("Rank vectors must contain only finite numbers")
    if len(set(a)) < 2 or len(set(b)) < 2:
        return {"n": len(a), "status": "undefined_constant_vector",
                "spearman_rho": None, "kendall_tau_b": None}
    return {"n": len(a), "status": "ok",
            "spearman_rho": float(spearmanr(a, b).statistic),
            "kendall_tau_b": float(kendalltau(a, b, variant="b").statistic)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    write_json(args.output, correlation(data["ranks_a"], data["ranks_b"]))


if __name__ == "__main__":
    main()
