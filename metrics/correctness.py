"""Functional correctness using the retained LeetCodeDataset execution helper."""
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path

from third_party.lcd_execution import check_correctness
from .common import positive_float, positive_int, write_json


def estimate_pass_at_k(n, c, k):
    if not (0 <= c <= n and 1 <= k <= n):
        raise ValueError("Require 0 <= correct <= samples and 1 <= k <= samples")
    if n - c < k:
        return 1.0
    return 1.0 - math.prod(1.0 - k / i for i in range(n - c + 1, n + 1))


def summarize(results, ks):
    counts = defaultdict(lambda: [0, 0])
    for row in results:
        counts[row["task_id"]][0] += 1
        counts[row["task_id"]][1] += int(row["passed"])
    if not counts:
        raise ValueError("No evaluation results")
    scores, unavailable = {}, []
    for k in ks:
        if all(n >= k for n, _ in counts.values()):
            scores[f"pass@{k}"] = sum(estimate_pass_at_k(n, c, k)
                                      for n, c in counts.values()) / len(counts)
        else:
            unavailable.append(k)
    return {"n_tasks": len(counts), "n_samples": len(results),
            "sample_pass_rate": sum(r["passed"] for r in results) / len(results),
            "pass_at_k": scores, "unavailable_k": unavailable,
            "per_task": {t: {"n": n, "correct": c} for t, (n, c) in counts.items()}}


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--problems", type=Path, required=True)
    parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument("--k", type=positive_int, nargs="+", default=[1])
    parser.add_argument("--timeout", type=positive_float, default=10)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = read_jsonl(args.problems)
    problems = {r["task_id"]: r for r in rows}
    samples = read_jsonl(args.samples)
    if len(problems) != len(rows):
        parser.error("Duplicate problem task_id")
    if not samples or set(problems) != {r["task_id"] for r in samples}:
        parser.error("Problem and attempted task_id sets must match exactly")
    results = []
    for index, sample in enumerate(samples):
        row = check_correctness(problems[sample["task_id"]], sample["completion"], args.timeout, index)
        # Do not export candidate code, problem prompts or test suites.
        results.append(row)
    report = summarize(results, args.k)
    report.update(timeout_seconds=args.timeout, results=results)
    write_json(args.output, report)


if __name__ == "__main__":
    main()
