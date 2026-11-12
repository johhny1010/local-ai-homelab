"""Synthetic loopback-only Ollama timing client; Python standard library."""
import argparse
import ipaddress
import json
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request

PROMPT = "Explain in three short sentences why repeatable measurements matter."


def validate_endpoint(value):
    p = urllib.parse.urlsplit(value)
    if p.scheme != "http" or p.username or p.password or p.query or p.fragment:
        raise ValueError("Use a plain HTTP loopback endpoint without credentials.")
    if p.path not in ("", "/"):
        raise ValueError("Endpoint paths are not accepted.")
    # Numeric addresses only: avoid DNS/proxy surprises.
    if not ipaddress.ip_address(p.hostname or "").is_loopback:
        raise ValueError("Only numeric loopback addresses are accepted.")
    _ = p.port
    return value.rstrip("/")


def metrics(result):
    count, duration = result.get("eval_count"), result.get("eval_duration")
    if not isinstance(count, int) or not isinstance(duration, (int, float)) or count <= 0 or duration <= 0:
        raise ValueError("Missing valid generation timing metadata.")
    fields = ("eval_count", "eval_duration", "prompt_eval_count", "prompt_eval_duration", "load_duration", "total_duration")
    return {**{k: result[k] for k in fields if k in result}, "generation_tokens_per_second": count * 1e9 / duration}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Redirects are disabled.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint", default="http://127.0.0.1:11434")
    parser.add_argument("--model", required=True)
    parser.add_argument("--runs", type=int, default=5, choices=range(1, 21))
    args = parser.parse_args()
    try:
        endpoint = validate_endpoint(args.endpoint)
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
        payload = json.dumps({"model": args.model, "prompt": PROMPT, "stream": False,
                              "options": {"temperature": 0, "seed": 42, "num_ctx": 2048, "num_predict": 128}}).encode()
        rows = []
        for index in range(args.runs + 1):
            request = urllib.request.Request(endpoint + "/api/generate", data=payload, headers={"Content-Type": "application/json"})
            with opener.open(request, timeout=300) as response:
                raw = response.read(2_000_001)
                if len(raw) > 2_000_000:
                    raise ValueError("Response limit exceeded.")
                row = metrics(json.loads(raw))
            if index:
                rows.append(row)
        print(json.dumps({"schema_version": 1, "warmup_excluded": True, "runs": rows,
                          "median_generation_tokens_per_second": statistics.median(r["generation_tokens_per_second"] for r in rows)}, indent=2))
        return 0
    except (ValueError, OSError, urllib.error.URLError, KeyError, TypeError):
        print("Benchmark failed. Check the local service, model and timing metadata privately.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
