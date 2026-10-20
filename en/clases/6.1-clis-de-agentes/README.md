# 6.1 · Compare modern agent CLIs

> 🇪🇸 Original Spanish guide: [`clases/6.1-clis-de-agentes/README.md`](../../../clases/6.1-clis-de-agentes/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Learn to compare any CLI agent with five questions, and check the answers in your lab's real shell.

| | |
|---|---|
| **Video length** | ≈8 min |
| **Practice** | Brev lab · [cookbook.md (Spanish)](../../../clases/6.1-clis-de-agentes/cookbook.md) |
| **Skill** | Compare agents by their risk surface and choose based on the task |
| **NVIDIA lesson** | [Modern CLI Agents (04b)](https://nvdli.github.io/NemoClawDLI/nemoclaw/04b-modern-clis.html) |
| **Materials** | [Slides](slides.html) · [FAQ (Spanish)](../../../FAQ.md) |

## What you'll achieve
- Explain why Claude Code, Codex, Cursor, Hermes, Deep Agents and OpenClaw are **the same loop with different defaults**.
- Compare agents on five axes: **files, network, identity, persistence and default sandbox**.
- Verify those axes in your lab with `openshell` and `nemoclaw`, and choose a tool based on the task and the risk.

## Before you start
- Your NemoClaw lab on Brev is working (class [4.1](../4.1-laboratorio-nemoclaw-en-brev/README.md)). If you stopped it, start it with `brev start <instance>`.
- The Brev CLI is logged in (`brev ls` shows your instance).
- You've read your sandbox's policy (class [5.3](../5.3-sandbox-y-politicas/README.md)). Today we use it to compare.

## The idea in one minute
All these agents wrap the same things: **a working folder, a palette of tools, a memory, optional unattended execution (cron, long tasks) and a network**. What changes is what comes open by default, and whether there's a runtime underneath that stops a bad call.

> The CLI sets the starting values. The OpenShell sandbox decides how far they reach.

### Table 1 · The CLIs as you install them
Source: NVIDIA lesson 04b. Anything 04b doesn't say is marked `[VERIFY]`: check it in the docs for the version you install, because defaults change between versions.

| Agent | Instructions file | Files | Network | Identity | Persistence | Default sandbox |
|---|---|---|---|---|---|---|
| **Claude Code** | `CLAUDE.md` | Tool rules and the permission mode decide what gets edited without asking | `[VERIFY]` | Your system user `[VERIFY]` | `CLAUDE.md`, project settings `[VERIFY]` | Configurable sandbox settings; don't assume they're on `[VERIFY]` |
| **Codex CLI** | `AGENTS.md` | Edits and runs only within the sandbox limits | Depends on the sandbox settings `[VERIFY]` | Your user `[VERIFY]` | `AGENTS.md` `[VERIFY]` | Sandbox + approval policy |
| **Cursor** | `.cursor/rules/*.mdc` | Edits the workspace in general **without** approval | Whatever your editor and OS allow | Your user | `.mdc` rules | No separate kernel policy; terminal commands ask for approval by default |
| **Hermes** | Skills and persistent memory (in NemoClaw, `SOUL.md`) | Depends on the terminal backend | Messaging integrations `[VERIFY]` | Depends on the backend `[VERIFY]` | Skills, memory, scheduled tasks | The approval mode and the terminal backend decide the isolation |
| **Deep Agents Code** (`dcode`) | `[VERIFY]` (04b doesn't cover it) | `[VERIFY]` | `[VERIFY]` | `[VERIFY]` | Skills and memory | Tool approval UI `[VERIFY]` |
| **OpenClaw** | `SOUL.md`, `AGENTS.md` | The workspace | Whatever the host allows `[VERIFY]` | `[VERIFY]` | Gateway sessions, cron, skills, `SOUL.md` | In this course it runs **inside OpenShell** |

### Table 2 · The three agents inside NemoClaw
NemoClaw isn't just OpenClaw: it supports **OpenClaw** (the default), **Hermes** (`nemohermes`) and **LangChain Deep Agents Code** (`nemo-deepagents`, binary `dcode`). Source: blueprint and policies in the NVIDIA/NemoClaw repo (October 2026).

| Axis | OpenClaw · `nemoclaw` | Hermes · `nemohermes` | Deep Agents · `nemo-deepagents` |
|---|---|---|---|
| **Files** (write) | `/tmp`, `/sandbox/.openclaw`, `/sandbox/.nemoclaw`, workdir. System is read-only | `/sandbox`, `/sandbox/.hermes`, `/tmp` | `/sandbox`, `/sandbox/.deepagents`, `/tmp` |
| **Landlock** | `best_effort` | `best_effort` | `strict`: if it can't be applied, the sandbox **doesn't start** |
| **Network** | Denied by default. Short list: NVIDIA, clawhub, openclaw.ai, npm (only the `openclaw` binary) | Denied by default. NVIDIA, Nous Research endpoints, PyPI | Denied by default. NVIDIA, GitHub, PyPI. OpenShell sees `dcode` as Python: the permission applies to **all** Python in the sandbox |
| **Identity** | `sandbox` user, not root. `ptrace`, `mount` and `setuid` blocked | `sandbox` user | `sandbox` user |
| **Persistence** | Workspace (`SOUL.md`, `AGENTS.md`, `MEMORY.md`), skills, cron | `/sandbox/.hermes`: `SOUL.md`, memories, skills, cron, messaging | `/sandbox/.deepagents`: skills, memory, `config.toml` |
| **Interface** | Gateway + dashboard (port 18789) | Gateway, dashboard and OpenAI-compatible API | Terminal only (TUI or `dcode -n`). No gateway or dashboard |
| **Credentials** | The key stays in the OpenShell gateway; it never enters the sandbox | Same | Same |

## Step by step
The full practice, with expected outputs and what to do if something fails, is in the **[cookbook (Spanish)](../../../clases/6.1-clis-de-agentes/cookbook.md)**. Summary:

1. **Connect to the VM.**
   ```bash
   brev ls
   brev shell <instance>
   ```
   You should see the VM prompt. No local terminal? Use the "Open a real shell on your launchable" cell in [lesson 04b](https://nvdli.github.io/NemoClawDLI/nemoclaw/04b-modern-clis.html).

2. **Inventory: which agents and sandboxes exist.**
   ```bash
   openshell sandbox list
   openshell status
   nemoclaw list
   nemoclaw agents list
   ```
   You should see your sandbox (e.g. `my-assistant`), the active gateway, and the installed agent (OpenClaw).

3. **Sandbox health.**
   ```bash
   nemoclaw my-assistant status
   ```
   Look for the inference row: `healthy` is what you expect. `unauthorized` = credential; `unreachable` = route.

4. **Identity axis: the same command on two planes.**
   ```bash
   id
   nemoclaw my-assistant exec -- id
   ```
   You should see your VM user in the first one and `sandbox` in the second.

5. **Files axis.**
   ```bash
   nemoclaw my-assistant exec -- touch /usr/prueba
   nemoclaw my-assistant exec -- touch /tmp/prueba
   ```
   The first one fails (read-only system); the second one works.

6. **Network axis.**
   ```bash
   nemoclaw my-assistant exec -- curl -sS https://example.com
   ```
   You should see `curl: (56) CONNECT tunnel failed, response 403`: the network policy blocked it.

7. **Persistence axis.**
   ```bash
   nemoclaw my-assistant exec -- ls /sandbox/.openclaw/workspace
   nemoclaw my-assistant skill list
   ```
   That's where `SOUL.md`, `AGENTS.md`, `MEMORY.md` and the skills live: what survives between sessions.

8. **Logs: where to look when something gets blocked.**
   ```bash
   nemoclaw my-assistant logs --tail 50
   ```
   You should see the `example.com` denial from step 6.

9. **Fill in your profile card** (see Challenge) and **stop the instance** when you're done: `brev stop <instance>`.

## How to choose a tool
Answer four questions: **who's watching?**, **what does it touch?**, **who does it talk to?** and **what survives?**

| Task | Main risk | Choose | Why |
|---|---|---|---|
| Coding with you alongside, in your repo | Edits or commands you didn't review | Claude Code, Codex or Cursor with approvals on | You're the control: approve commands and review the diff |
| Long, unattended refactor of a repo | Nobody's watching; the agent installs packages and runs code | Deep Agents (`nemo-deepagents`) or a CLI inside OpenShell | `strict` Landlock, minimal network, credentials outside the sandbox |
| 24/7 assistant you message through chat | Untrusted content + data + a way out (trifecta) | OpenClaw or Hermes inside NemoClaw | Deny-by-default policy, network approval in `openshell term`, audit logs |
| Scheduled task (cron) that reads data and writes a report | A poisoned directive repeats every day | Any of them inside a sandbox + a reviewed skill | Persistence (skills, cron) is attack surface |
| Exploring an idea for 10 minutes | Low, if there's no sensitive data | Whatever CLI you already have | Keep it simple; but don't give it your production keys |

Rule of thumb: **if the task combines all three legs of the trifecta (5.1), the agent goes inside a sandbox.** Choosing a tool means choosing which risk you accept.

## Check that it worked
- [ ] `openshell sandbox list` and `nemoclaw list` show the same sandbox.
- [ ] `nemoclaw <sandbox> status` reports inference as `healthy`.
- [ ] `id` inside the sandbox shows the `sandbox` user.
- [ ] Writing to `/usr` failed and writing to `/tmp` worked.
- [ ] `curl` to a host outside the list returned `CONNECT tunnel failed, response 403` and you saw it in the logs.
- [ ] You filled in the five-axis profile card for an agent you use.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `openclaw: command not found` in the VM shell | You're on the **host**, not in the sandbox. `openclaw` lives inside the sandbox | Use `nemoclaw <sandbox> exec -- <command>` or `nemoclaw <sandbox> connect` |
| `curl: (56) CONNECT tunnel failed, response 403` | The network policy blocked the host. It's not a TLS error | Expected in step 6. To allow a host: `openshell term` (temporary) or `nemoclaw <sandbox> policy add` (persistent) |
| `nemoclaw list` says there are no sandboxes, but `openshell sandbox list` shows one | The sandbox wasn't created with NemoClaw, or the `~/.nemoclaw/sandboxes.json` registry is corrupted | Check `nemoclaw <sandbox> status`. If the sandbox belongs to NemoClaw, don't manage it with `openshell sandbox create/delete` |
| `ssh: Could not resolve hostname <instance>` | The IP changed after a restart, or Brev's `Include` is missing from `~/.ssh/config` | `brev refresh`; if it persists, move Brev's `Include` line to the top of `~/.ssh/config` |
| `brev shell <instance> --host` hangs | The `--host` path changed in recent CLI versions | Use `brev shell <instance>` without `--host` |
| The inference row in `status` says `unauthorized` | The stored credential doesn't work (rotated or expired key) | Rotate the key: `nemoclaw credentials reset <PROVIDER>`, then `nemoclaw onboard` |
| `openshell logs <sandbox> --tail` never ends | In `openshell`, `--tail` **follows** the log; in `nemoclaw`, it's a number of lines | Use `openshell logs <sandbox> -n 20` or `nemoclaw <sandbox> logs --tail 20` |

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
- NVIDIA DLI · [Modern CLI Agents (04b)](https://nvdli.github.io/NemoClawDLI/nemoclaw/04b-modern-clis.html). This class is based on lesson 04b of the NVIDIA DLI course (Apache-2.0).
- NemoClaw · [Platform and agent support](https://docs.nvidia.com/nemoclaw/latest/) (`docs/reference/platform-support.mdx`) and [Hermes / Deep Agents ecosystem](https://github.com/NVIDIA/NemoClaw/tree/main/docs/about).
- Claude Code · [Permissions](https://code.claude.com/docs/en/permissions)
- Codex · [Approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)
- Cursor · [Agent security](https://cursor.com/docs/agent/security)
- Hermes · [Security guide](https://hermes-agent.nousresearch.com/docs/user-guide/security/)
- LangChain · [Deep Agents Code](https://docs.langchain.com/oss/python/deepagents/code/overview)
