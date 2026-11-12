# Architecture notes

## Recorded deployment versus reference example

The recorded lab used native Ollama instances and Docker-hosted Open WebUI. The optional Compose example in this repository instead shows one isolated 3090 inference service and one UI. It is deliberately a small, newly written reproduction example; it neither replaces nor reconstructs the existing multi-service installation.

The 3090 has 24 GB for the general workload; the 3060 has 12 GB for automation-oriented inference. Five 16 GB P100s provide 80 GB distributed across independent devices. A fifth P100 assignment is not yet documented. Earlier specialist roles included research, creative, developer, and expert; roles describe intended workloads, not automatic model routing.

## Mixed GPU constraints

- P100 is Pascal, while 3090 and 3060 are Ampere. Do not assume one newly released binary supports all cards.
- NVIDIA removed offline compilation and library support for Pascal from CUDA Toolkit 13.0. Existing compatible builds can still run with a supporting driver. A CUDA version shown by `nvidia-smi` is not proof that a framework includes Pascal kernels.
- Record the driver, application build, bundled CUDA runtime, and supported GPU architectures separately. Consult the official references before upgrades; do not change the offline server from this template.
- GPU UUIDs are preferable to unstable numerical indices for local assignment. Keep actual UUIDs in ignored local configuration.
- PCIe link width, NUMA placement, model splitting, and CPU offload affect performance. Physical x16 connectors do not establish electrical x16 links. No unmeasured link topology is asserted here.
- VRAM must cover weights plus context/KV cache and runtime buffers. Quantization and context settings change capacity requirements.
- Passive server accelerators require directed airflow. Verify temperatures and system power under sustained concurrent load; PSU nameplate totals are not measured consumption.

## Tool execution boundary

The automation model may propose an action, but the client must enforce allowed tools, validate arguments, and separately authorize consequential actions. Do not mount a Docker socket or unrestricted host directories into a chat service. Private agent and terminal integrations are outside the included deployment example.
