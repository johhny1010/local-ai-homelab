# Repeatable local benchmark

No measured results are included. The client is new example code, not a recovered lab script.

For an existing, deliberately loopback-bound native Ollama service with a model already installed:

```bash
python scripts/benchmark.py --model MODEL_TAG --runs 5
```

The optional Compose stack does not publish this API; do not expose it simply to run this example. The client refuses non-loopback endpoints, proxies, credentials, custom paths and redirects. It uses a fixed synthetic prompt, non-streaming generation, a bounded context and output limit. Error output omits server responses and addresses. It prints JSON to stdout; output is not automatically committed.

Record the model digest and quantization, runtime versions, GPU model, context length, prompt, output token cap, concurrency, warm/cold state, and date separately. The model tag is not an immutable identifier. The first request is a warm-up and excluded. Runs are sequential, not a concurrency test.

Generation throughput = `eval_count / (eval_duration / 1e9)`. Prompt processing, loading and end-to-end latency are different metrics. The JSON includes their raw timing/count fields when available and median generation throughput. These values are server-reported and do not prove GPU execution. Verify utilization separately without uploading raw diagnostics.
