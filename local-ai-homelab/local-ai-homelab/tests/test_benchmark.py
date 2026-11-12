import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("benchmark", Path(__file__).resolve().parents[1] / "scripts" / "benchmark.py")
benchmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark)


class BenchmarkTests(unittest.TestCase):
    def test_rejects_remote_and_credential_endpoints(self):
        for endpoint in ("http://example.com", "http://0.0.0.0:11434", "http://user:pass@127.0.0.1", "http://127.0.0.1/custom", "https://127.0.0.1", "http://127.0.0.1?x=1"):
            with self.subTest(endpoint=endpoint), self.assertRaises(ValueError):
                benchmark.validate_endpoint(endpoint)

    def test_accepts_loopback(self):
        self.assertEqual(benchmark.validate_endpoint("http://127.0.0.1:11434/"), "http://127.0.0.1:11434")

    def test_nanoseconds_and_response_redaction(self):
        result = benchmark.metrics({"eval_count": 40, "eval_duration": 2_000_000_000, "response": "private text"})
        self.assertEqual(result["generation_tokens_per_second"], 20)
        self.assertNotIn("response", result)

    def test_invalid_timing(self):
        with self.assertRaises(ValueError):
            benchmark.metrics({"eval_count": 40, "eval_duration": 0})

    def test_redirect_blocked(self):
        with self.assertRaises(ValueError):
            benchmark.NoRedirect().redirect_request(None, None, 302, "", {}, "http://example.com")
