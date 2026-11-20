"""Behavior checks using synthetic inputs."""
import importlib.util
import math
from pathlib import Path
import tempfile
import unittest

from metrics.correctness import estimate_pass_at_k, summarize
from metrics.performance import measure
from third_party.lcd_execution import check_correctness


class CorrectnessTests(unittest.TestCase):
    def test_estimator_against_combinations(self):
        for n in range(1, 12):
            for c in range(n + 1):
                for k in range(1, n + 1):
                    expected = 1 - (math.comb(n - c, k) if n - c >= k else 0) / math.comb(n, k)
                    self.assertAlmostEqual(estimate_pass_at_k(n, c, k), expected)

    def test_invalid_sample_counts(self):
        for values in [(1, 2, 1), (1, 0, 2), (0, 0, 1)]:
            with self.assertRaises(ValueError):
                estimate_pass_at_k(*values)

    def test_macro_and_micro_denominators(self):
        result = summarize([{"task_id": "a", "passed": True},
                            {"task_id": "b", "passed": False},
                            {"task_id": "b", "passed": False}], [1, 2])
        self.assertAlmostEqual(result["sample_pass_rate"], 1 / 3)
        self.assertEqual(result["pass_at_k"], {"pass@1": 0.5})
        self.assertEqual(result["unavailable_k"], [2])

    def test_real_execution_pass_fail_and_timeout(self):
        problem = {"task_id": "toy", "prompt": "", "entry_point": "candidate",
                   "test": "def check(f):\n    assert f(2) == 4"}
        for completion, expected in [("def candidate(x): return x * 2", True),
                                     ("def candidate(x): return x", False)]:
            result = check_correctness(problem, completion, 2)
            self.assertEqual(result["passed"], expected)
        result = check_correctness(problem, "def candidate(x):\n    while True: pass", 0.1)
        self.assertFalse(result["passed"])
        self.assertEqual(result["result"], "timed out")


class PerformanceTests(unittest.TestCase):
    def run_code(self, code, repeats=2, timeout=3):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "candidate.py"
            path.write_text(code, encoding="utf-8")
            return measure({"source": str(path), "entry_point": "f", "args": []}, repeats, timeout)

    def test_fresh_processes_and_traced_peak(self):
        result = self.run_code("state = []\ndef f():\n    assert not state\n    state.append(1)\n    return bytearray(100000)")
        self.assertEqual(result["status"], "ok")
        self.assertGreaterEqual(result["MU_bytes"], 100000)
        self.assertEqual(len(result["repetitions"]), 2)
        self.assertGreaterEqual(result["ET_ms"], 0)

    def test_no_summary_on_exception(self):
        result = self.run_code("def f(): raise RuntimeError('toy failure')")
        self.assertEqual(result["status"], "failed")
        self.assertNotIn("ET_ms", result)

    def test_timeout(self):
        result = self.run_code("def f():\n    while True: pass", repeats=1, timeout=0.2)
        self.assertEqual(result["repetitions"][0]["status"], "timeout")
        self.assertNotIn("MU_bytes", result)


@unittest.skipUnless(importlib.util.find_spec("radon"), "Radon not installed")
class MaintainabilityTests(unittest.TestCase):
    def test_plain_function_and_invalid_source(self):
        from radon.metrics import mi_visit
        value = mi_visit("def identity(value):\n    return value\n", multi=True)
        self.assertTrue(0 <= value <= 100)
        with self.assertRaises(SyntaxError):
            mi_visit("def broken(", multi=True)


@unittest.skipUnless(importlib.util.find_spec("scipy"), "SciPy not installed")
class AgreementTests(unittest.TestCase):
    def test_ties_and_undefined(self):
        from metrics.agreement import correlation
        result = correlation([1, 2, 2, 4], [1, 2, 3, 4])
        self.assertAlmostEqual(result["spearman_rho"], 0.9486832980505138)
        self.assertAlmostEqual(result["kendall_tau_b"], 0.9128709291752769)
        self.assertEqual(correlation([1, 1], [1, 2])["status"], "undefined_constant_vector")
        with self.assertRaises(ValueError):
            correlation([1, float("nan")], [1, 2])


if __name__ == "__main__":
    unittest.main()
