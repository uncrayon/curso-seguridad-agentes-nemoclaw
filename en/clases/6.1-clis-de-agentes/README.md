# 6.1 · Compare modern agent CLIs

> 🇪🇸 Original Spanish guide: [`clases/6.1-clis-de-agentes/README.md`](../../../clases/6.1-clis-de-agentes/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Learn to compare any CLI agent with five questions, check the answers in your lab's real terminal, and close the lab without overspending.

| | |
|---|---|
| **Video** | None: this is supplementary material |
| **Practice** | Brev lab: NemoClaw dashboard + browser terminal ([cookbook.md (Spanish)](../../../clases/6.1-clis-de-agentes/cookbook.md)) |
| **Skill** | Compare agents by their risk surface and choose based on the task |
| **Materials** | [Slides](slides.html) · [FAQ (Spanish)](../../../FAQ.md) |

> Based on lesson 04b of the NVIDIA DLI course "NemoClaw" (Apache-2.0) and on the NVIDIA/NemoClaw repo.

> **This class is supplementary material: it has no video.** You don't need it to follow the course, and its lab practice is optional too. If you do it, do it in the same sitting, after 5.3 and before you delete the instance (≈20 min, ≈USD 0.08). If you already deleted it when you finished 5.3, skip it: you can read this guide without the lab.

## What you'll achieve
- Explain why Claude Code, Codex, Cursor, Hermes, Deep Agents and OpenClaw are **the same loop with different defaults**.
- Compare agents on five axes: **files, network, identity, persistence and default sandbox**.
- Verify those axes in your lab from the **VM TERMINAL** with `openshell` and `nemoclaw`, and choose a tool based on the task and the risk.
- Close the lab: save your work, delete the instance and check your balance.

## Before you start
- Your Brev instance is **Running** and the NemoClaw dashboard is open: in the Brev console, your instance, green **NemoClaw** button (class [4.1](../4.1-laboratorio-nemoclaw-en-brev/README.md)).
- You've done [4.3](../4.3-agentes-siempre-activos/README.md) (you installed the `soporte-nemoclaw` skill) and [5.3](../5.3-sandbox-y-politicas/README.md) (you read your sandbox's policy). Today we use them to compare.
- **Your credit:** this practice takes ≈20 min of your single lab sitting (see [your Brev lab (Spanish)](../../../LABORATORIO.md)). When you finish: if you'll do 6.2's optional lab part, leave the instance running and keep going; if not, save what you want and **Delete**.

## The idea in one minute
All these agents wrap the same things: **a working folder, a palette of tools, a memory, optional unattended execution (cron, long tasks) and a network**. What changes is what comes open by default, and whether there's a runtime underneath that stops a bad call.

> The CLI sets the starting values. The OpenShell sandbox decides how far they reach.

### Table 1 · The CLIs as you install them
Source: NVIDIA lesson 04b. Where it says "see its docs", 04b doesn't cover it: check the docs for the version you install, because defaults change between versions.

| Agent | Instructions file | Files | Network | Identity | Persistence | Default sandbox |
|---|---|---|---|---|---|---|
| **Claude Code** | `CLAUDE.md` | Tool rules and the permission mode decide what gets edited without asking | See its docs | Your system user (confirm in its docs) | `CLAUDE.md` and project settings | Configurable sandbox settings; don't assume they're on |
| **Codex CLI** | `AGENTS.md` | Edits and runs only within the sandbox limits | Depends on the sandbox settings | Your user (confirm in its docs) | `AGENTS.md` | Sandbox + approval policy |
| **Cursor** | `.cursor/rules/*.mdc` | Edits the workspace in general **without** approval | Whatever your editor and OS allow | Your user | `.mdc` rules | No separate kernel policy; terminal commands ask for approval by default |
| **Hermes** | Skills and persistent memory (in NemoClaw, `SOUL.md`) | Depends on the terminal backend | Messaging integrations (see its docs) | Depends on the backend | Skills, memory, scheduled tasks | The approval mode and the terminal backend decide the isolation |
| **Deep Agents Code** (`dcode`) | See its docs (04b doesn't cover it) | See its docs | See its docs | See its docs | Skills and memory | Tool approval UI (see its docs) |
| **OpenClaw** | `SOUL.md`, `AGENTS.md` | The workspace | Outside a sandbox, whatever the host allows | Outside a sandbox, see its docs | Gateway sessions, cron, skills, `SOUL.md` | In this course it runs **inside OpenShell** |

### Table 2 · The three agents inside NemoClaw
NemoClaw isn't just OpenClaw: it supports **OpenClaw** (the default), **Hermes** (`nemohermes`) and **LangChain Deep Agents Code** (`nemo-deepagents`, binary `dcode`). All three commands come installed on the lab VM. Source: blueprint and policies in the NVIDIA/NemoClaw repo (October 2026).

| Axis | OpenClaw · `nemoclaw` | Hermes · `nemohermes` | Deep Agents · `nemo-deepagents` |
|---|---|---|---|
| **Files** (write) | `/tmp`, `/sandbox/.openclaw`, `/sandbox/.nemoclaw`, workdir. System is read-only | `/sandbox`, `/sandbox/.hermes`, `/tmp` | `/sandbox`, `/sandbox/.deepagents`, `/tmp` |
| **Landlock** | `best_effort` | `best_effort` | `strict`: if it can't be applied, the sandbox **doesn't start** |
| **Network** | Denied by default. Short per-program list: NVIDIA, clawhub, openclaw.ai, npm. In your lab, the `docs.openclaw.ai` group lets neither `curl` nor `node` out | Denied by default. NVIDIA, Nous Research endpoints, PyPI | Denied by default. NVIDIA, GitHub, PyPI. OpenShell sees `dcode` as Python: the permission applies to **all** Python in the sandbox |
| **Identity** | `sandbox` user (uid 998), not root. `ptrace`, `mount` and `setuid` blocked | `sandbox` user | `sandbox` user |
| **Persistence** | Workspace (`SOUL.md`, `AGENTS.md`, `USER.md`…; `MEMORY.md` only if the agent saved memory), skills, cron | `/sandbox/.hermes`: `SOUL.md`, memories, skills, cron, messaging | `/sandbox/.deepagents`: skills, memory, `config.toml` |
| **Interface** | Gateway + browser chat (port 18789) | Gateway, dashboard and OpenAI-compatible API | Terminal only (TUI or `dcode -n`). No gateway or dashboard |
| **Credentials** | The key stays in the OpenShell gateway; it never enters the sandbox | Same | Same |

## Step by step
The full practice, with expected outputs and what to do if something fails, is in the **[cookbook (Spanish)](../../../clases/6.1-clis-de-agentes/cookbook.md)**. Everything happens in the browser: the NemoClaw dashboard and its **VM TERMINAL**, the operator terminal (the host, user `ubuntu`). To run something **inside** the sandbox, the command starts with `nemoclaw my-assistant exec --`.

### Part 1 · Open the operator terminal
1. On the NemoClaw dashboard, on the **MY-ASSISTANT** card, click **VM TERMINAL**. A black window opens over the dashboard.
2. Click inside the black area before typing. If you type without clicking, your keys trigger dashboard shortcuts. To close it later: **Shift+Escape**.
3. Every `nemoclaw` command prints the line `ExperimentalWarning: SQLite is an experimental feature`. Ignore it: it isn't an error.

![The NemoClaw dashboard with the MY-ASSISTANT card and its four buttons; the number marks the VM TERMINAL button](../../../assets/lab/13-panel-nemoclaw.jpg)

### Part 2 · Inventory: which sandboxes and agents exist
1. To see the sandboxes OpenShell manages:
   ```bash
   openshell sandbox list
   ```
   You should see the columns `NAME`, `CREATED` and `PHASE`, with `my-assistant` in `Ready`.
2. To check whether the front desk (the OpenShell gateway) is connected:
   ```bash
   openshell status
   ```
   You should see a `Server Status` block with the gateway `nemoclaw-18080`, the server `https://127.0.0.1:18080`, `Connected`, `Authenticated (mTLS transport)` and version `0.0.116`.
3. To see what NemoClaw has registered and confirm the other two agents are installed:
   ```bash
   nemoclaw list
   ls /usr/bin/nemohermes /usr/bin/nemo-deepagents
   ```
   `nemoclaw list` shows `my-assistant` with the `openclaw` agent, the `nvidia-prod` provider and its policy presets. The `ls` prints both paths: Hermes and Deep Agents are on the VM, even if you don't use them today.

### Part 3 · Sandbox health
To ask NemoClaw whether your agent is healthy:
```bash
nemoclaw my-assistant status
```
Look for inference `healthy` and phase `Ready`. `unauthorized` means a credential problem; `unreachable` means the route to the model.

### Part 4 · The axes, outside and inside
1. **Identity.** To ask "who am I?" on the VM and then inside the sandbox:
   ```bash
   id
   nemoclaw my-assistant exec -- id
   ```
   Outside you see `uid=1000(ubuntu)` with groups like `sudo` and `docker`: the operator has power. Inside you see `uid=998(sandbox) gid=998(sandbox)`: the agent doesn't.
2. **Files.** To try creating an empty file in a system folder and then in the temporary folder:
   ```bash
   nemoclaw my-assistant exec -- touch /usr/prueba
   nemoclaw my-assistant exec -- touch /tmp/prueba
   ```
   The first one answers `Permission denied`; the second prints nothing, because it worked.
3. **Network.** To ask the sandbox for a page that isn't on its list:
   ```bash
   nemoclaw my-assistant exec -- curl -sS https://example.com
   ```
   You should see `curl: (56) CONNECT tunnel failed, response 403`: the network policy blocked it.
4. **Persistence.** To see what survives between sessions:
   ```bash
   nemoclaw my-assistant exec -- ls /sandbox/.openclaw/workspace
   nemoclaw my-assistant skill list
   nemoclaw my-assistant sessions list --json
   ```
   In the workspace you see `AGENTS.md`, `HEARTBEAT.md`, `IDENTITY.md`, `POLICY.md`, `SOUL.md`, `TOOLS.md` and `USER.md`; after 4.3, also `faq`, `reportes` and `skills`. You only see `MEMORY.md` if the agent saved memory. `skill list` shows a summary like `22/57 ready` (the number may change) and includes `soporte-nemoclaw`. With `--json`, sessions come out readable (for example, `"agentId": "main"`).

![The VM TERMINAL with the identity checks: the ubuntu user outside, the sandbox user inside; the numbers mark each output](../../../assets/lab/16-terminal-identidad-sandbox.png)

### Part 5 · Who stops it: logs and the OpenShell TUI
1. To find the block from the network step in the log:
   ```bash
   nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4
   ```
   You should see a line similar to `[OCSF ] [ocsf] NET:OPEN [MED] DENIED /usr/bin/curl(…) -> example.com:443 [policy:- engine:opa] [reason:…]`.
2. (Optional) Close the terminal with **Shift+Escape** and click **OPENSHELL TUI** on the dashboard. Open your sandbox with **[Enter]** and press **[r]** to see the rules. Pending requests show up there, with **[a]** Approve, **[x]** Reject, **[A]** Approve All and **[p]** Policy. If you see the `example.com` one, reject it with **[x]**: you don't need it. Exit with **[q]**.

### Part 6 · Close the lab: save and delete
If you'll do the optional lab part of [6.2](../6.2-biblioteca-de-skills/README.md), leave the instance running and move on to that class: you close the lab there. If not, save what you want and **Delete**. When you delete the instance, everything on the VM is lost.
1. **Save what you want.** The course files (`~/curso`) are already on GitHub. To keep something your agent wrote, print it in the VM TERMINAL, select it with the mouse and paste it into your notes. For example, the report from 4.3:
   ```bash
   nemoclaw my-assistant exec -- cat /sandbox/.openclaw/workspace/reportes/resumen-faq.md
   ```
2. **Delete the instance.** Close the terminal (**Shift+Escape**) and go to the Brev console: **Compute** → your instance (`nemoclaw-…`) → **Delete**. Confirm in the dialog that appears.

   ![The instance page in the Brev console with the Stop, Delete and NemoClaw buttons; the number marks Delete](../../../assets/lab/05-instancia-lista.jpg)

3. **Check your balance.** In the top menu, open **Billing** (or look at the balance in the top bar). Confirm the instance no longer shows up under **Compute**. If something doesn't add up, see [your Brev lab (Spanish)](../../../LABORATORIO.md).

## How to choose a tool
Answer four questions: **who's watching?**, **what does it touch?**, **who does it talk to?** and **what survives?**

| Task | Main risk | Choose | Why |
|---|---|---|---|
| Coding with you alongside, in your repo | Edits or commands you didn't review | Claude Code, Codex or Cursor with approvals on | You're the control: approve commands and review the diff |
| Long, unattended refactor of a repo | Nobody's watching; the agent installs packages and runs code | Deep Agents (`nemo-deepagents`) or a CLI inside OpenShell | `strict` Landlock, minimal network, credentials outside the sandbox |
| 24/7 assistant you message through chat | Untrusted content + data + a way out (trifecta) | OpenClaw or Hermes inside NemoClaw | Deny-by-default policy, network approval in the OpenShell TUI, audit logs |
| Scheduled task (cron) that reads data and writes a report | A poisoned directive repeats every day | Any of them inside a sandbox + a reviewed skill | Persistence (skills, cron) is attack surface |
| Exploring an idea for 10 minutes | Low, if there's no sensitive data | Whatever CLI you already have | Keep it simple; but don't give it your production keys |

Rule of thumb: **if the task combines all three legs of the trifecta (5.1), the agent goes inside a sandbox.** Choosing a tool means choosing which risk you accept.

## Check that it worked
- [ ] `openshell sandbox list` and `nemoclaw list` show the same sandbox, and `openshell status` says `Connected`.
- [ ] `nemoclaw my-assistant status` reports inference as `healthy`.
- [ ] `id` shows `ubuntu` outside and `sandbox` inside the sandbox.
- [ ] Writing to `/usr` failed and writing to `/tmp` worked.
- [ ] `curl` to a host outside the list returned `CONNECT tunnel failed, response 403` and you saw the `DENIED` line in the logs.
- [ ] You filled in the five-axis profile card for an agent you use.
- [ ] You deleted your instance with **Delete** and it no longer shows up under **Compute** (or you left it running to continue with 6.2's lab part).

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| You type and nothing shows up in the terminal, or something on the dashboard opens | The VM TERMINAL doesn't have focus | Click inside the black area and type again |
| `ExperimentalWarning: SQLite is an experimental feature` | A notice every `nemoclaw` command prints | Ignore it: it isn't an error |
| `openclaw: command not found` in the VM TERMINAL | You're on the **host**, not in the sandbox. `openclaw` lives inside the sandbox | Use `nemoclaw my-assistant exec -- <command>` or the **SANDBOX TERMINAL** button |
| `curl: (56) CONNECT tunnel failed, response 403` | The network policy blocked the host. It's not a certificate error | Expected in Part 4. To allow a host: **OPENSHELL TUI** → **[r]** → **[a]** (temporary) or `nemoclaw my-assistant policy add` (persistent, class 5.3) |
| `openshell gateway status` fails | That subcommand doesn't exist | Use `openshell status` or `openshell gateway info` |
| `sessions list` prints an unreadable table | It's too wide for the browser terminal | Use `nemoclaw my-assistant sessions list --json` |
| `nemoclaw list` says there are no sandboxes, but `openshell sandbox list` shows one | The sandbox wasn't created with NemoClaw, or the `~/.nemoclaw/sandboxes.json` registry is corrupted | Check `nemoclaw my-assistant status`. If the sandbox belongs to NemoClaw, don't manage it with `openshell sandbox create/delete` |
| The inference row in `status` says `unauthorized` | The stored credential doesn't work (rotated or expired key) | Check your key at build.nvidia.com. To rotate it: `nemoclaw credentials reset <PROVIDER>`, then `nemoclaw onboard` |
| `openshell logs <sandbox> --tail` never ends | In `openshell`, `--tail` **follows** the log; in `nemoclaw`, it's a number of lines | Exit with Ctrl+C and use `openshell logs <sandbox> -n 20` or `nemoclaw my-assistant logs --tail 20` |

## Challenge
Pick **a CLI agent you use** (or the one that interests you most) and fill in this card **using its official documentation**:

| Axis | Default | Configurable? | Source (link) |
|---|---|---|---|
| Files | | | |
| Network | | | |
| Identity | | | |
| Persistence | | | |
| Default sandbox | | | |

**Success criterion:** all five rows have a source. If you can't find one, write "not documented": that's a security finding too.

## Project milestone
Add a `docs/eleccion-de-agente.md` (agent choice) file to your **Soporte NemoClaw** (NemoClaw Support) project with:
1. Table 2 filled in **with what you saw in your sandbox** (not with what this guide says).
2. One line: why the support agent runs in OpenClaw inside NemoClaw and not as a CLI on your laptop (hint: it reads FAQ entries from strangers 24/7 = untrusted content).
3. Which agent you would use to **code** the project, and with which controls.

## Resources
- NVIDIA DLI · Modern CLI agents (lesson 04b). This class is based on that lesson of the NVIDIA DLI course "NemoClaw" (Apache-2.0).
- NemoClaw · [Platform and agent support](https://docs.nvidia.com/nemoclaw/latest/) (`docs/reference/platform-support.mdx`) and [Hermes / Deep Agents ecosystem](https://github.com/NVIDIA/NemoClaw/tree/main/docs/about).
- Claude Code · [Permissions](https://code.claude.com/docs/en/permissions)
- Codex · [Approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)
- Cursor · [Agent security](https://cursor.com/docs/agent/security)
- Hermes · [Security guide](https://hermes-agent.nousresearch.com/docs/user-guide/security/)
- LangChain · [Deep Agents Code](https://docs.langchain.com/oss/python/deepagents/code/overview)
- Brev · [Console reference](https://docs.nvidia.com/brev/latest/guides/console-reference): instances, Stop, Delete and Billing.
