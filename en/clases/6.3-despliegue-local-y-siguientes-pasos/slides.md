## Where does your agent live?

:::diagrama c63-tres-caminos

Notes:
Like moving from a rented office to your own. Click 1: Brev, the course launchable; you pay per hour while it's on, and for the disk while it exists. Click 2: your computer (16 GB of RAM, Docker, Node 22.19+), close to your files. Click 3: a server or a DGX Spark: 24/7 and local inference, your data stays put. Click 4: the criterion. The lab ends; your project doesn't. This class is a map, not an install tutorial: the step by step is in the optional cookbook.

---

## Requirements to run it locally

:::diagrama c63-requisitos

Notes:
Click 1: minimum 4 vCPU, 8 GB of RAM and 20 GB of disk; recommended 16 GB and 40 GB. Docker and Node 22.19+. Click 2: tested on Linux (Ubuntu 24.04), DGX Spark, macOS on Apple Silicon and WSL2; Intel Macs aren't supported (the installer rejects them). Click 3: how to check your memory without a terminal. With 8 GB, the sandbox image (~2.4 GB compressed) can trigger the OOM killer. The GPU is optional if you use NVIDIA Endpoints. Leave it 20 seconds.

---

## Install in one line (and pin the version)

:::diagrama c63-instalar

.lead It's the operator way: one line installs OpenShell and NemoClaw, then launches the setup assistant.

Notes:
The command: `curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_REF= NEMOCLAW_INSTALL_TAG=vX.Y.Z bash`. Click 1: the variable on the `curl` side (the live error): the installer announces "lkg". Click 2: the variable on the `bash` side: it installs your version. Click 3: the backpack on each side of the bar. Without the tag, it follows "lkg" (last-known-good). NemoClaw ships releases every 1 to 3 days: pinning it makes your install repeatable. The key locally: `NVIDIA_INFERENCE_API_KEY=nvapi-...`.

---

## Onboarding in 9 steps

:::diagrama c63-onboarding

Notes:
Go through it quickly. Click 1: preflight and OpenShell gateway. Click 2: agent (OpenClaw, Hermes or Deep Agents), provider and model, credential, sandbox name (`my-assistant`). Click 3: review (Apply / Edit / Exit), channels and web search (optional), policy. Click 4: Balanced by default. The Personal tier opens any host on 80/443 without approvals: don't use it for an agent that reads messages from strangers.

---

## Inference providers

:::diagrama c63-proveedores

.lead The inference provider lends you the model: the office your agent calls to ask.

Notes:
Click 1: the agent in its room. Click 2: the front desk (gateway) keeps the key: it never enters the sandbox. Click 3: NVIDIA Endpoints, tested, with your `nvapi-` key. Click 4: local ones: Ollama (with a validated model) and vLLM (server on `:8000`) with limitations; local NIM, experimental (NVIDIA GPU + NGC). Validated Ollama models: qwen3.6:35b, nemotron-3-nano:30b, qwen3.5:9b. If tool calls come out as text, the server isn't returning structured tool_calls.

---

## Day 1 and day 2

:::diagrama c63-dias

Notes:
Click 1: day 1, `nemoclaw my-assistant status` · `launch` · `logs --follow`, and `skill install ./skill-library/<skill>/`. Click 2: day 2, after a restart: `status` → `start` → `recover`; to update: `backup-all` → `update` → `upgrade-sandboxes --auto`. Click 3: never `openshell self-update`, `openclaw update` inside the sandbox, or global `nemoclaw start/stop`. NemoClaw pins an exact OpenShell version: updating it on the side breaks compatibility.

---

## If you prefer the terminal: install errors

| Symptom | Fix |
|---|---|
| `nemoclaw: command not found` | New terminal or `source ~/.bashrc` |
| `Docker is not running` | `usermod -aG docker $USER && newgrp docker` |
| Exit 137 (OOM) | 16 GB or 4–8 GB of swap |
| `did not become ready within 180s` | `NEMOCLAW_SANDBOX_READY_TIMEOUT=600` |
| `Port 18789 is not available` | `--control-ui-port 19000` |

.lead It's optional: each one has its recipe on the class page.

Notes:
Each one has a recipe in the class's optional cookbook.

---

## NVIDIA production pieces

:::diagrama c63-piezas

Notes:
The sandbox stays in the middle. Click 1: NIM, the model packaged with an OpenAI-compatible server on your infrastructure; check tool calls and structured output before you switch. Click 2: NeMo Retriever, hybrid search, reranker and chunking: the production version of the in-memory RAG from 3.2. Click 3: NeMo Guardrails, input and output filters in the app. Click 4: DGX Spark, a 24/7 agent with local inference. Click 5: Guardrails complements the sandbox; you want both.

---

## Wrap up your project

:::diagrama c63-rubrica

.lead The full checklist and rubric are on the class page.

Notes:
One click per criterion, with its "Outstanding" level: works, tools and skills (≥ 90 % measured hit rate), security (block confirmed in logs, no secrets in git), operations (cron + documented recovery after restart), documentation (README with decisions and limits). Click 6: ask them to post their score and what they'd improve first. It's the course's final deliverable. Leave it 20 seconds.

---

## Save your work and delete your instance

:::diagrama c63-guarda-borra

Notes:
Click 1: save your skills, your SOUL.md and your notes to your computer or GitHub (operator way: `brev copy`). Click 2: Brev console → GPUs → your instance → Delete (operator way: `brev delete`). Don't delete the recording instance on camera. Click 3: once deleted, nothing is billed. Click 4: stopped, the disk keeps billing; deleted, what's inside is lost.

---

## Where to go next

:::diagrama c63-seguir

Notes:
Click 1: knowledge (chunking, retrieval and faithfulness). Click 2: substrate (MCP, Responses API, OTel GenAI, A2A). Click 3: fleets and containment (N agents bounded with Landlock, seccomp and netns). Click 4: this course is lesson 6 of NVIDIA's agentic AI learning path. Pick the axis your project trips over most. Before production: test the app's controls and the runtime's controls separately.
