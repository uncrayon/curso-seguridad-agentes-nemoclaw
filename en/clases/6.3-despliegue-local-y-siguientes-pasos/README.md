# 6.3 · How to run your Brev agent locally

> 🇪🇸 Original Spanish guide: [`clases/6.3-despliegue-local-y-siguientes-pasos/README.md`](../../../clases/6.3-despliegue-local-y-siguientes-pasos/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Run NemoClaw on your Apple Silicon Mac with Colima, close out your project, and choose where to go next. Linux and Windows alternatives are in the cookbook.

| | |
|---|---|
| **Video length** | ≈13 min |
| **Practice** | Guided on this page + [optional local install cookbook (Spanish)](../../../clases/6.3-despliegue-local-y-siguientes-pasos/cookbook.md) (on your own computer, outside Brev) |
| **Skill** | Plan a local deployment and close out an agent project with quality criteria |
| **Materials** | [Slides](slides.html) · [FAQ (Spanish)](../../../FAQ.md) |

> This class doesn't use the Brev lab.

## What you'll achieve
- Know whether your machine can run NemoClaw, what to install, and which inference provider to use.
- Map NVIDIA's production pieces (NIM, NeMo Guardrails, NeMo Retriever, DGX Spark) onto your own project.
- Deliver **Soporte NemoClaw** (NemoClaw Support) with a checklist and a rubric, and choose your next step.

## Before you start
- Your **Soporte NemoClaw** project with the work from classes 2.1 to 5.3, plus 6.1 and 6.2 if you did them (notebooks, skills in [`skill-library/` (Spanish)](../../../skill-library/README.md), the security analysis from 5.x).
- Your Brev lab should already be **deleted**: you closed it at the end of [5.3](../5.3-sandbox-y-politicas/README.md) or, if you did supplementary practices, at the end of the last one you did ([6.1](../6.1-clis-de-agentes/README.md) or the lab part of [6.2](../6.2-biblioteca-de-skills/README.md)). If not, step 7 shows you how.
- Optional, only if you want to install NemoClaw on your own machine: Linux, macOS on Apple Silicon, or Windows with WSL2 (see the table in step 2). You don't need Brev for this.

## Step by step

### 1. Decide where your agent lives
| Option | When it makes sense | Cost | What you take care of |
|---|---|---|---|
| **Stay on Brev** (a new deployment of the NemoClaw launchable) | You want the same environment as the course, with nothing to install | ≈USD 0.25/h while running; stopped, the disk keeps billing ≈USD 1.20 a day | Deleting it (**Delete**) when you're done |
| **Your machine** | You have 16 GB of RAM and want the agent close to your files | Power and disk | Docker, updates, restarts |
| **Your own server or a DGX Spark** | 24/7 agent, local inference, data that stays put | Hardware | Secure remote access (`ssh -L`), backups |

For a separate deployment with hosted models: endpoint `https://integrate.api.nvidia.com/v1` and your NVIDIA key. Check your account's current access and quota.

### 2. Prepare your Mac with Colima

This walkthrough uses **Colima with Docker and NVIDIA Endpoints**. Your agent runs locally; model requests go to NVIDIA's hosted API. You do not need a local NVIDIA GPU.

Docker is the container runtime. The `docker` command is its client; Colima supplies the Linux VM that runs the engine on macOS. Docker Desktop is an alternative that supplies its own VM. Colima is our choice here, not a NemoClaw requirement.

| Resource | Minimum | Recommended |
|---|---|---|
| CPU | 4 vCPU | 4+ vCPU |
| RAM | 8 GB | **16 GB** (with 8 GB, the sandbox image can run out of memory) |
| Free disk | 20 GB | 40 GB |
| Software | Colima + Docker CLI on this Mac, Node.js 22.19+, npm 10+ | Homebrew for the commands below |
| Platforms | Linux (Ubuntu 24.04 validated), macOS on Apple Silicon, Windows WSL2, DGX Spark | Intel Macs are **not** supported |

Check the Mac's resources first. `hw.memsize` reports bytes:

```bash
sysctl -n hw.ncpu
sysctl -n hw.memsize
df -h ~
```

Install [Homebrew](https://brew.sh/) if it is missing. If Xcode Command Line Tools are missing, run `xcode-select --install` and finish the dialog before continuing.

```bash
brew install colima docker
colima start --cpu 4 --memory 12 --disk 100
```

The example gives the VM 4 CPUs, 12 GiB of RAM, and a 100 GiB virtual disk. It is a starting point for the 18 GiB Mac used in this walkthrough, not a guarantee for every workload. Leave memory for macOS and your other apps. The virtual disk limit does not create free space on the Mac; image downloads and builds still need real disk space. If Colima is already running and you need to change its resources, run `colima stop` before the new `colima start` command. This stops all workloads in that VM.

Select the default Colima profile and check the engine:

```bash
unset DOCKER_HOST DOCKER_CONTEXT
docker context use colima
colima status
docker info --format 'CPUs={{.NCPU}} MemoryBytes={{.MemTotal}}'
```

Expect a running Colima VM and **4 CPUs** in Docker's output. Available memory can be slightly below 12 GiB. These engine values, rather than the Mac's totals, determine what the containers can use.

If `docker info` works but NemoClaw or OpenShell still cannot find Docker, set the socket explicitly in the terminal where you will run them:

```bash
unset DOCKER_CONTEXT
export DOCKER_HOST="unix://${HOME}/.colima/default/docker.sock"
docker info
```

`DOCKER_HOST` tells a client where to connect. This is a socket-selection workaround, not proof of a broken Docker installation. The path above is for Colima's default profile; use `colima status` to find a named profile's socket. The export lasts for this terminal session. Repeat it in a new terminal if needed. Before switching runtimes, unset it and select the intended Docker context. See the [Colima socket FAQ](https://colima.run/docs/faq/#where-is-the-docker-socket-located) and [Docker context documentation](https://docs.docker.com/engine/manage-resources/contexts/).

### 3. Install, use, and pause NemoClaw

#### Install with limits that fit the VM

For the 4-CPU/12-GiB VM above, use a sandbox limit of **3 CPUs and 8 GiB**. This leaves capacity for the VM, Docker, and supporting processes. These are sandbox limits, not extra resources allocated outside Colima, and CPU limits do not permanently dedicate physical cores.

We observed NemoClaw v0.0.145 resolve the developer profile's 75% against a 12-CPU/18-GiB Mac, requesting 9 CPUs/13Gi from a smaller VM. Docker rejected that CPU request. The explicit values below avoid this bug. [Issue #14743](https://github.com/NVIDIA/NemoClaw/issues/14743) contains the proposed fix and regression evidence; a patch in a fork does not mean your installed release includes it.

If NemoClaw is not installed, run:

```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | \
  NEMOCLAW_AGENT=openclaw NEMOCLAW_CPU=3 NEMOCLAW_RAM=8Gi bash
```

The variables belong on the **`bash` side** of the pipe, so the installer and onboarding receive them. The installer checks Node.js and npm; verify `node --version` is at least 22.19 and `npm --version` is at least 10. To pin a release, follow Recipe 3 of the [cookbook (Spanish)](../../../clases/6.3-despliegue-local-y-siguientes-pasos/cookbook.md).

If NemoClaw is already installed and you are creating a sandbox, run:

```bash
NEMOCLAW_CPU=3 NEMOCLAW_RAM=8Gi nemoclaw onboard --name my-assistant
```

Choose **OpenClaw**, **NVIDIA Endpoints**, and the **Balanced** policy. Enter your NVIDIA key at the credential prompt. If using an environment variable, use `NVIDIA_INFERENCE_API_KEY` and keep the real value out of shell history and shared files. Onboarding should show the CPU/RAM overrides and finish with `NemoClaw is ready`.

If an earlier attempt failed, read `nemoclaw debug --quick` before choosing recovery. A timeout alone does not identify the cause. After fixing a temporary connection problem, use `nemoclaw onboard --resume`. For the resource-limit failure, start a new attempt with a new name:

```bash
NEMOCLAW_CPU=3 NEMOCLAW_RAM=8Gi \
  nemoclaw onboard --fresh --name my-assistant-fixed
```

`--fresh` discards the onboarding checkpoint; it does not resize an existing sandbox or erase its name. Keep the failed sandbox until you know whether it contains data you need. Use the new name in the commands below if you chose it. You do not need to delete Colima or reinstall Docker to fix a CPU-limit mismatch.

#### Verify and use the agent

```bash
nemoclaw my-assistant status
nemoclaw my-assistant dashboard-url --quiet
nemoclaw launch my-assistant
```

Use the dashboard URL reported by your installation, normally on `127.0.0.1:18789`. Treat a URL containing a token as a password. Port 18080 normally belongs to the OpenShell gateway. To inspect a failure, run `nemoclaw my-assistant logs --follow`; press **Ctrl+C** to leave the log stream. Install the course skills with Recipe 8 of the cookbook.

#### Stop for the day and resume later

To stop only this sandbox while keeping Colima available for other work:

```bash
nemoclaw my-assistant stop
```

To stop the entire Colima VM and every container inside it:

```bash
colima stop
colima status
```

Expect Colima to report that it is not running. The VM and its containers stop using CPU and RAM; their disk data remains. Host processes can remain: a macOS OpenShell gateway service, a local Ollama server, or a terminal tunnel runs outside the VM. Check Activity Monitor and `brew services list`, then stop any such service through the manager that started it. Do not use a blanket process-kill command.

To resume, reuse the saved VM configuration:

```bash
colima start
docker info
nemoclaw my-assistant status
```

Restore `DOCKER_HOST` first if this terminal needs the socket workaround. If the sandbox is stopped, run `nemoclaw my-assistant start`. If it remains unhealthy, inspect the status and run `nemoclaw my-assistant recover`. Status and recovery commands can start supporting services, so use `colima status` to check that the VM remains off.

`colima stop` is the everyday shutdown. `colima delete`, sandbox `destroy`, and uninstall commands are cleanup operations, not shutdown steps. For updates, follow `nemoclaw backup-all`, `nemoclaw update`, and `nemoclaw upgrade-sandboxes --auto`. Let NemoClaw manage its compatible OpenShell version; do not run `openshell self-update` separately.

### 4. Map the production pieces onto your project
| Piece | What it is | What it improves in Soporte NemoClaw |
|---|---|---|
| **NIM** | Model + tokenizer + OpenAI-compatible server in a container, on your infrastructure | You change `BASE_URL` and the model runs on your network. First, test that it supports tool calls and structured output |
| **NeMo Retriever** | Hybrid search (sparse + dense), reranker and chunking, with NIM embeddings | Replaces the in-memory RAG from 3.2 when the FAQ grows |
| **NeMo Guardrails** | Programmable input and output filters at the application layer | Stops the agent from asking for or showing keys, or from discussing off-course topics. It **complements** the sandbox; it doesn't replace it |
| **DGX Spark** | Desktop machine with an NVIDIA GPU; a tested NemoClaw platform with local inference | 24/7 agent with data that never leaves your office. Check out the gallery of [NemoClaw playbooks for Spark](https://build.nvidia.com/spark/nemoclaw-applications) |

For each one, write a line in your project: "I'd use it for ___ when ___".

### 5. Close out your project: delivery checklist
- [ ] **Loop and tools** (2.x): the agent answers with `buscar_faq` (FAQ search) and `estimar_costo_brev` (Brev cost estimate), and validates arguments.
- [ ] **Triage** (3.1): classifies into `instalacion | api_key | brev | seguridad | otro` (installation, API key, Brev, security, other).
- [ ] **RAG with citations** (3.2): every answer includes `Fuente:` (source) from `datos/faq/`.
- [ ] **Diagnostic report** (3.3): the subagents leave their work in files.
- [ ] **Deployment** (4.x): the `soporte-nemoclaw` skill runs in OpenClaw and the cron task leaves the summary.
- [ ] **Security** (5.x): trifecta analysis and sandbox policy documented; no secrets in the repo (`git grep nvapi-` returns no real keys).
- [ ] **Skills** (6.2): 4 skills in `skill-library/`, validated, with a hit rate ≥ 90 % and the table in `docs/evaluacion-skills.md`.
- [ ] **Agent choice** (6.1): `docs/eleccion-de-agente.md`.
- [ ] **Project README**: what it does, how to run it, known limits, and a screenshot (with the token blurred).
- [ ] **Brev**: instance deleted (it no longer shows up under **Compute**) and balance checked in **Billing**.

### 6. Self-assess with the rubric
| Criterion | Beginning (1) | Competent (2) | Outstanding (3) |
|---|---|---|---|
| **Works** | Answers some questions | Answers the FAQ with correct citations | Also says "I don't know" when there's no source, and escalates |
| **Tools and skills** | Tools without validation | Validated tools, 4 valid skills | Hit rate ≥ 90 % measured and documented; a fifth skill |
| **Security** | No analysis | Trifecta identified and sandbox policy read | Mitigation tested (block confirmed in the logs) and no secrets in the git history |
| **Operations** | Only runs by hand | Cron that leaves the daily summary | Knows how to recover it after a restart and documents it (status → start → recover) |
| **Documentation** | No README | README with steps to run it | README + decisions (agent, provider, production pieces) and known limits |

Add up your points: **5–8** keep iterating · **9–12** ready to show · **13–15** publish it and share it.

### 7. Confirm the lab is deleted
Normally you already deleted your instance at the end of your last lab practice ([5.3](../5.3-sandbox-y-politicas/README.md), or the last supplementary practice you did). Check it in the browser:
1. In the Brev console (brev.nvidia.com), open **Compute**. Your instance (`nemoclaw-…`) should no longer show up.
2. If it's still there, save what you want: copy the text from the **VM TERMINAL**, or download everything as a zip with the [first recipe of the cookbook (Spanish)](../../../clases/6.3-despliegue-local-y-siguientes-pasos/cookbook.md#receta-previa--respalda-tu-laboratorio-en-un-zip), then open the instance and click **Delete**. Confirm in the dialog that appears.
3. Open **Billing** in the top menu and check your balance.

Running, the instance costs ≈USD 0.25/h. Stopped (**Stop**), the disk keeps billing ≈USD 0.05/h, about USD 1.20 a day. Deleted (**Delete**), nothing is billed, but you lose what was inside. Details in [your Brev lab (Spanish)](../../../LABORATORIO.md).

## Check that it worked
- [ ] You know whether your machine meets the requirements (or what it's missing).
- [ ] If you installed locally, Docker reports the VM capacity, the agent responds, and you can stop and resume Colima without deleting data.
- [ ] You wrote one line per production piece for your project.
- [ ] You checked off the delivery checklist and have your rubric score.
- [ ] Your Brev instance is deleted and you checked your balance.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| The installer rejects your Mac | Intel Macs (x86_64) aren't supported | Use Brev, a Linux machine or an Apple Silicon Mac |
| Exit 137 / OOM when creating the sandbox | The VM or host ran out of memory | Check both budgets. Increase Colima memory only if the Mac has room; see cookbook Recipe 0 for Linux swap guidance |
| `NEMOCLAW_INSTALL_TAG` "does nothing" | The variable ended up on the `curl` side | `curl ... \| NEMOCLAW_INSTALL_REF= NEMOCLAW_INSTALL_TAG=vX.Y.Z bash` |
| `nemoclaw: command not found` when it finishes | Your shell's `PATH` wasn't updated | Open a new terminal; on macOS with zsh, check `~/.zshrc` and `~/.local/bin` |
| `docker: command not found` after installing Colima | The Docker CLI is missing | `brew install docker` |
| Docker connection fails on macOS | Colima is stopped or the client selected another socket | Follow step 2: `colima status`, check the Docker context, then use `DOCKER_HOST` if needed |
| Docker connection fails on Linux | The daemon is stopped or your user lacks socket access | Follow cookbook Recipe 1; Linux Docker-group commands do not apply to macOS |
| CPU request exceeds Docker's limit, followed by a readiness timeout | A percentage profile used host capacity | Compare `docker info` with the request; retry with the explicit limits in step 3 and a new sandbox name |
| `✗ openshell <version> is above the maximum supported by this NemoClaw release.` | You updated OpenShell outside NemoClaw | Don't use `openshell self-update`; reinstall the supported version |
| Your Brev balance keeps dropping even though you no longer use the lab | The instance is stopped (**Stop**), not deleted: the disk bills | Brev console → **Compute** → your instance → **Delete** |
| `Port 18080 is not available` during a local install | Another process is using the OpenShell gateway port | Close that process or see Recipe 5 of the cookbook |

## Challenge
Pick **one** production piece and write a one-page plan to add it to Soporte NemoClaw: what changes in the code, what risk it reduces, how you'd measure the improvement, and what it does **not** solve.
**Success criterion:** the plan names a metric (e.g. rate of answers with a correct citation, or blocked attempts to ask for a key) and a test that measures it.

## Project milestone · Wrap-up
Your project ends here. Publish it on your GitHub with:
1. The step 5 checklist, completed, in the README.
2. Your rubric score and what you'd improve first.
3. Your deployment decision: Brev, local or server, and with which inference provider.

## Next steps
- **NVIDIA Agentic AI Learning Path**: this course corresponds to lesson 6, *safer autonomous agents with OpenClaw*. The earlier lessons cover building agents, agentic RAG, evaluation, customization and deep agents.
- **Pick an axis to go deeper** (lesson 04c):
  - **The knowledge layer**: chunking, retrieval, answer faithfulness.
  - **The substrate**: MCP, Responses API, OTel GenAI conventions, A2A.
  - **Fleets and containment**: what changes with N agents, and how Landlock, seccomp and network namespaces bound each one.
- **Before you take it to production**: test the application's controls **and** the runtime permissions separately; and verify administrative authority on its own: being able to read doesn't prove you control the agent.

## Resources
- NVIDIA DLI · Going Further (04c). This class is based on lesson 04c of the NVIDIA DLI course (Apache-2.0).
- NemoClaw · [Prerequisites](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/get-started/prerequisites) · [OpenClaw quickstart](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/get-started/quickstart) · [Docker capacity bug and proposed fix](https://github.com/NVIDIA/NemoClaw/issues/14743)
- Colima · [Getting started](https://colima.run/docs/getting-started/) · [Configuration](https://colima.run/docs/configuration/) · [Commands](https://colima.run/docs/commands/)
- NVIDIA · [NIM](https://docs.nvidia.com/nim/) · [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) · [NeMo Curator](https://github.com/NVIDIA/NeMo-Curator) · [AI-Q Blueprint](https://build.nvidia.com/nvidia/aiq)
- NVIDIA · [NemoClaw playbooks for DGX Spark](https://build.nvidia.com/spark/nemoclaw-applications) · [NemoClaw on DGX Spark](https://build.nvidia.com/spark/nemoclaw/instructions)
- NVIDIA · [Agentic AI Learning Path](https://developer.nvidia.com/topics/ai/agentic-ai-learning-path) · [Generative AI blog](https://developer.nvidia.com/blog/category/generative-ai/)
- NVIDIA Blog · [Build a secure, always-on local AI agent with NemoClaw and OpenClaw](https://developer.nvidia.com/blog/build-a-secure-always-on-local-ai-agent-with-nvidia-nemoclaw-and-openclaw/)
