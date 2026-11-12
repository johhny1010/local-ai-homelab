# Evidence ledger

| Item | Basis | Publication status |
|---|---|---|
| Five P100s + 3090 + 3060 | Current owner statement | Documented; live inventory pending |
| Board, CPUs, RAM, NVMe | Earlier project records | Documented; maintenance recheck pending |
| Native multi-instance Ollama + Docker UI | Earlier operational records | Historical architecture; no raw exports included |
| General/specialist/security workload separation | Earlier project records | Historical roles; exact current mapping pending |
| Model-family experimentation | Earlier project records | Family names only; no inferred model tags |
| Included Compose and benchmark client | Newly authored portfolio examples | Offline validation only |
| Performance and context capacity | Incomplete historical measurements | No verified result claims published |

The host was offline during repository creation. No SSH access, network scan, deployment, live GPU test, or production security audit occurred. Private transcripts and configuration dumps are intentionally absent.

## Maintenance verification checklist

1. Inspect hardware and GPU memory capacities locally; do not publish UUIDs or serials.
2. Record OS, driver, Ollama, UI and container versions in private notes.
3. Confirm each service's assigned devices and actual GPU offload under load.
4. Verify bindings, authentication, registration settings and access boundaries.
5. Select exact image digests for a separate test deployment; do not reuse existing data volumes.
6. Run synthetic benchmarks with model digest, quantization, context, concurrency and sample count.
7. Review staged files, artifacts and Git history before publishing.
