# 6.3 · Next steps and local deployment

> 🇪🇸 Original Spanish guide: [`clases/6.3-despliegue-local-y-siguientes-pasos/README.md`](../../../clases/6.3-despliegue-local-y-siguientes-pasos/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Wrap up your project, learn what you need to run NemoClaw on your own machine, and choose where to go next.

| | |
|---|---|
| **Video length** | ≈8 min |
| **Practice** | Guided on this page + [optional local install cookbook (Spanish)](../../../clases/6.3-despliegue-local-y-siguientes-pasos/cookbook.md) |
| **Skill** | Plan a local deployment and close out an agent project with quality criteria |
| **Materials** | [Slides](slides.html) · [FAQ (Spanish)](../../../FAQ.md) |

## What you'll achieve
- Know whether your machine can run NemoClaw, what to install, and which inference provider to use.
- Map NVIDIA's production pieces (NIM, NeMo Guardrails, NeMo Retriever, DGX Spark) onto your own project.
- Deliver **Soporte NemoClaw** (NemoClaw Support) with a checklist and a rubric, and choose your next step.

## Before you start
- Your **Soporte NemoClaw** project with the work from classes 2.1 to 6.2 (notebooks, skills in [`skill-library/` (Spanish)](../../../skill-library/README.md), the security analysis from 5.x).
- Your Brev lab: today you'll leave it **stopped or deleted**.
- Optional, for a local install: a machine with Linux, macOS on Apple Silicon, or Windows with WSL2 (see the table in step 2).

## Step by step

### 1. Decide where your agent lives
| Option | When it makes sense | Cost | What you take care of |
|---|---|---|---|
| **Stay on Brev** (NemoClaw launchable) | You want the same environment as the course, with nothing to install | Credits per hour while running; disk while it exists | Stopping it when you're done |
| **Your machine** | You have 16 GB of RAM and want the agent close to your files | Power and disk | Docker, updates, restarts |
| **Your own server or a DGX Spark** | 24/7 agent, local inference, data that stays put | Hardware | Secure remote access (`ssh -L`), backups |

For a separate deployment with hosted models: endpoint `https://integrate.api.nvidia.com/v1` and your NVIDIA key. Check your account's current access and quota.

### 2. Check your machine in 2 minutes
| Resource | Minimum | Recommended |
|---|---|---|
| CPU | 4 vCPU | 4+ vCPU |
| RAM | 8 GB | **16 GB** (with 8 GB, the sandbox image can run out of memory) |
| Free disk | 20 GB | 40 GB |
| Software | Docker, Node.js 22.19+, npm 10+ | |
| Platforms | Linux (Ubuntu 24.04 validated), macOS on Apple Silicon, Windows WSL2, DGX Spark | Intel Macs are **not** supported |

```bash
nproc; free -h; df -h ~        # on macOS: sysctl -n hw.ncpu; sysctl -n hw.memsize; df -h ~
docker info >/dev/null && echo "Docker OK"
node --version                 # v22.19.0 or later
```
You should see: 4 or more CPUs, 8 GB or more of RAM, 20 GB or more free, `Docker OK` and Node 22.19+. If something's missing, the [cookbook (Spanish)](../../../clases/6.3-despliegue-local-y-siguientes-pasos/cookbook.md) (Recipes 0 and 1) tells you how to fix it.

### 3. (Optional) Install NemoClaw locally
Follow the [cookbook (Spanish)](../../../clases/6.3-despliegue-local-y-siguientes-pasos/cookbook.md). The short path:
```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_REF= NEMOCLAW_INSTALL_TAG=vX.Y.Z bash
```
- The variables go **on the `bash` side** of the pipe.
- During onboarding, the key is read from `NVIDIA_INFERENCE_API_KEY` (not from `NVIDIA_API_KEY`).
- Providers: **NVIDIA Endpoints** (no GPU), local **Ollama**, local **vLLM**, local **NIM** (experimental, requires an NVIDIA GPU).

Day 1 and day 2 in one table:

| When | Commands |
|---|---|
| Day 1 · use | `nemoclaw my-assistant status` · `dashboard-url --quiet` · `nemoclaw launch my-assistant` · `logs --follow` |
| Day 1 · your project | `nemoclaw my-assistant skill install ./skill-library/<skill>/` · `skill list` |
| Day 2 · restart | `nemoclaw my-assistant status` → `start` → `recover` |
| Day 2 · update | `nemoclaw backup-all` → `nemoclaw update` → `nemoclaw upgrade-sandboxes --auto` |
| Never | `openshell self-update` · `openclaw update` inside the sandbox · global `nemoclaw start/stop` (deprecated) |

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
- [ ] **Brev**: instance stopped or deleted (`brev ls`).

### 6. Self-assess with the rubric
| Criterion | Beginning (1) | Competent (2) | Outstanding (3) |
|---|---|---|---|
| **Works** | Answers some questions | Answers the FAQ with correct citations | Also says "I don't know" when there's no source, and escalates |
| **Tools and skills** | Tools without validation | Validated tools, 4 valid skills | Hit rate ≥ 90 % measured and documented; a fifth skill |
| **Security** | No analysis | Trifecta identified and sandbox policy read | Mitigation tested (block confirmed in the logs) and no secrets in the git history |
| **Operations** | Only runs by hand | Cron that leaves the daily summary | Knows how to recover it after a restart and documents it (status → start → recover) |
| **Documentation** | No README | README with steps to run it | README + decisions (agent, provider, production pieces) and known limits |

Add up your points: **5–8** keep iterating · **9–12** ready to show · **13–15** publish it and share it.

### 7. Shut down the lab
```bash
brev ls
brev stop <instance>      # or, if you won't use it again: brev delete <instance>
brev ls                   # confirm STOPPED or that it's gone
```
Running = you pay for compute · stopped = disk only · deleted = nothing, but you lose the data. Copy anything you want to keep first: `brev copy <instance>:/path ./local`.

## Check that it worked
- [ ] You know whether your machine meets the requirements (or what it's missing).
- [ ] You wrote one line per production piece for your project.
- [ ] You checked off the delivery checklist and have your rubric score.
- [ ] Your Brev instance is stopped or deleted.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| The installer rejects your Mac | Intel Macs (x86_64) aren't supported | Use Brev, a Linux machine or an Apple Silicon Mac |
| Exit 137 / OOM when creating the sandbox | 8 GB of RAM or less | 16 GB, or add 4–8 GB of swap (cookbook, Recipe 0) |
| `NEMOCLAW_INSTALL_TAG` "does nothing" | The variable ended up on the `curl` side | `curl ... \| NEMOCLAW_INSTALL_REF= NEMOCLAW_INSTALL_TAG=vX.Y.Z bash` |
| `nemoclaw: command not found` when it finishes | Your shell's `PATH` wasn't updated | Open a new terminal or run `source ~/.bashrc` |
| `Docker is not running` even though Docker is running | Your user isn't in the `docker` group | `sudo usermod -aG docker $USER && newgrp docker` |
| `✗ openshell <version> is above the maximum supported by this NemoClaw release.` | You updated OpenShell outside NemoClaw | Don't use `openshell self-update`; reinstall the supported version |
| `brev stop` answers `does not support stop` | That instance type can't be stopped | Save your work and use `brev delete <instance>` |

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
- NemoClaw · [Documentation](https://docs.nvidia.com/nemoclaw/latest/) · [Prerequisites](https://docs.nvidia.com/nemoclaw/latest/get-started/prerequisites) · [Repo and issues](https://github.com/NVIDIA/NemoClaw)
- NVIDIA · [NIM](https://docs.nvidia.com/nim/) · [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) · [NeMo Curator](https://github.com/NVIDIA/NeMo-Curator) · [AI-Q Blueprint](https://build.nvidia.com/nvidia/aiq)
- NVIDIA · [NemoClaw playbooks for DGX Spark](https://build.nvidia.com/spark/nemoclaw-applications) · [NemoClaw on DGX Spark](https://build.nvidia.com/spark/nemoclaw/instructions)
- NVIDIA · [Agentic AI Learning Path](https://developer.nvidia.com/topics/ai/agentic-ai-learning-path) · [Generative AI blog](https://developer.nvidia.com/blog/category/generative-ai/)
- NVIDIA Blog · [Build a secure, always-on local AI agent with NemoClaw and OpenClaw](https://developer.nvidia.com/blog/build-a-secure-always-on-local-ai-agent-with-nvidia-nemoclaw-and-openclaw/)
