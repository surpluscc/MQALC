"""ET/MU measurement: perf_counter and tracemalloc around one target call."""
import argparse
import contextlib
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import tempfile
import time
import tracemalloc

from .common import positive_float, positive_int, write_json


def worker(config_path, result_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    try:
        # Import, object construction and input copies are outside measurement.
        with open(os.devnull, "w") as sink, contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            spec = importlib.util.spec_from_file_location("candidate", config["source"])
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            parts = config["entry_point"].split(".")
            if len(parts) == 2:
                target = getattr(getattr(module, parts[0])(), parts[1])
            elif len(parts) == 1:
                target = getattr(module, parts[0])
            else:
                raise ValueError("Use function or Class.method as entry_point")
            args = copy.deepcopy(config.get("args", []))
            kwargs = copy.deepcopy(config.get("kwargs", {}))
            tracemalloc.start()
            start = time.perf_counter()
            result = target(*args, **kwargs)
            end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            # Keep the returned object alive until after peak collection.
            del result
        record = {"status": "ok", "ET_ms": (end - start) * 1000, "MU_bytes": peak}
    except BaseException as exc:
        if tracemalloc.is_tracing():
            tracemalloc.stop()
        record = {"status": "error", "error": type(exc).__name__}
    write_json(result_path, record)


def measure(config, repeats, timeout):
    records = []
    # Each repetition uses a fresh interpreter and the identical JSON input.
    with tempfile.TemporaryDirectory(prefix="public-metrics-") as temporary:
        directory = Path(temporary)
        config_path, result_path = directory / "case.json", directory / "result.json"
        write_json(config_path, config)
        for _ in range(repeats):
            result_path.unlink(missing_ok=True)
            try:
                env = dict(os.environ)
                env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
                process = subprocess.run(
                    [sys.executable, "-m", "metrics.performance", "--worker",
                     str(config_path), str(result_path)],
                    cwd=directory, env=env, stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL, timeout=timeout)
                if process.returncode != 0 or not result_path.exists():
                    record = {"status": "error", "error": "worker_failed"}
                else:
                    record = json.loads(result_path.read_text(encoding="utf-8"))
            except subprocess.TimeoutExpired:
                record = {"status": "timeout"}
            records.append(record)
    summary = {"status": "ok" if all(r["status"] == "ok" for r in records) else "failed",
               "repetitions": records}
    # A partial run is never silently averaged as a successful measurement.
    if summary["status"] == "ok":
        for metric in ("ET_ms", "MU_bytes"):
            values = [r[metric] for r in records]
            summary[metric] = statistics.mean(values)
            summary[metric + "_sd"] = statistics.stdev(values) if repeats > 1 else None
    return summary


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--worker":
        worker(sys.argv[2], sys.argv[3])
        return
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=Path)
    parser.add_argument("--repeats", type=positive_int, default=5)
    parser.add_argument("--timeout", type=positive_float, default=30)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.case.read_text(encoding="utf-8"))
    source = (args.case.resolve().parent / config["source"]).resolve()
    config["source"] = str(source)
    result = measure(config, args.repeats, args.timeout)
    result.update(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  python=sys.version, platform=platform.platform(),
                  repeats=args.repeats, timeout_seconds=args.timeout,
                  scope="target call only; tracemalloc enabled; no correctness inference")
    write_json(args.output, result)
    if result["status"] != "ok":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
