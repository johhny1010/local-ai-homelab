# Optional reference deployment

This is a new two-container example for a separate test environment, not the recorded native Ollama setup. Do not run it over existing services or use it to upgrade the offline server. It targets one RTX 3090 only; Pascal runtime compatibility requires separate verification.

Prerequisites: a maintained Docker Engine with Compose GPU support, NVIDIA Container Toolkit, and a compatible host driver. Read upstream security/version notes and select exact images that you have evaluated. No current image versions are asserted to be secure or compatible.

1. Copy `.env.example` to `.env` and restrict its permissions (`chmod 600 .env` on Linux).
2. Privately identify the 3090 UUID using `nvidia-smi -L`; set `PRIMARY_GPU_ID` in `.env`.
3. Set both image variables to evaluated `repository@sha256:...` references. Generate a fresh `WEBUI_SECRET_KEY` locally with `python -c "import secrets; print(secrets.token_hex(32))"`. Do not commit the result.
4. Validate interpolation privately with `docker compose -f compose.example.yaml config --quiet`. Avoid publishing rendered configuration because it contains the secret.
5. For a fresh isolated test volume only, temporarily set `ENABLE_SIGNUP=true`, start the stack, and create the initial admin account at `http://127.0.0.1:3000` from the host. Then set it back to `false` and recreate the UI container. Verify registration is actually disabled in the application's admin settings; some settings persist in its database.
6. Start using `docker compose -f compose.example.yaml up -d`. Pull an explicitly chosen model through the Ollama container: `docker compose -f compose.example.yaml exec ollama ollama pull MODEL_TAG`. Replace `MODEL_TAG` with a real model you have evaluated and are licensed to use.
7. Confirm authentication, GPU execution and network reachability before use. No host-side benchmark API port is provided by this Compose example.

To stop the test services use `docker compose -f compose.example.yaml down`. Named data volumes remain. This repository intentionally provides no destructive cleanup command.

Remote access and the existing server's multi-service connectivity are outside this example. No firewall, router or public exposure changes are included.
