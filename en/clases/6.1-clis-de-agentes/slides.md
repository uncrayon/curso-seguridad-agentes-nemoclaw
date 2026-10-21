## Same loop, different defaults

:::diagrama c61-cinco-piezas

Notes:
Open with the strong idea: we're not going to memorize products, we're going to learn to compare them. Five clicks, one piece each: working folder, tools (terminal, editing, search, MCP), memory, unattended tasks (cron, long tasks, queues) and network. Click 6: what changes is what comes open by default. The loop is the one you already know.

---

## Five questions for any agent

:::diagrama c61-cinco-preguntas

Notes:
One click per axis: files, network, identity, persistence and default sandbox, each with its "for the assistant" version for non-coders. Click 6: the degrees of freedom are the attack surface. These five questions outlive the next product launch. Ask them to write them down.

---

## The CLIs as you install them

:::diagrama c61-asistentes

.lead Different assistants: what changes is the key you hand them on day one.

Notes:
Source: NVIDIA lesson 04b. Click 1: Claude Code, Codex CLI and Cursor (Cursor: `.cursor/rules/*.mdc`; edits without approval, the terminal asks). Click 2: Hermes and Deep Agents (Deep Agents' tool approval outside NemoClaw isn't in 04b: don't state it). Click 3: OpenClaw, the only one that lives in the room here (gateway and cron inside OpenShell). Click 4: the sentence to always say. Defaults change with every release. Leave the slide on screen for 20 seconds.

---

## NemoClaw isn't just OpenClaw

:::diagrama c61-tres-agentes

Notes:
Click 1: OpenClaw (`nemoclaw`), the usual one, with gateway and dashboard; Landlock `best_effort`. Click 2: Hermes (`nemohermes`); network to NVIDIA, Nous and PyPI. Click 3: Deep Agents (`nemo-deepagents`, `dcode` binary); Landlock `strict`: if it can't apply the lock, it won't start. Click 4: what all three share. From the NemoClaw repo; all three commands come installed on the lab VM. Subtle detail: OpenShell sees dcode as Python, so a network permission applies to all Python in the sandbox.

---

## The CLI sets the default; the sandbox sets the limit

:::diagrama c61-dos-planos

Notes:
Click 1: the application plane (CLAUDE.md, AGENTS.md, approvals, modes): the agent or a prompt can change it. Click 2: the system plane (Landlock, seccomp, netns, network proxy): only the operator changes it. Click 3: an approval isn't a kernel boundary. NVIDIA also documents OpenShell for Codex, Cursor and OpenCode. Tie it back to what you saw about security: prompt, harness, sandbox.

---

## Which side of the door?

:::diagrama c61-de-que-lado

Notes:
Click 1: outside, you in the dashboard's VM TERMINAL (`id` answers `uid=1000(ubuntu)`, with the `sudo` and `docker` groups). Click 2: `nemoclaw my-assistant exec` goes into the room: inside, the agent is the sandbox user (`uid=998`). Click 3: the agent tries to reach example.com and the rule answers 403 (`CONNECT tunnel failed, response 403`): it's the class's live error. Click 4: the forum's most common error, `openclaw: command not found`, because you're outside. Demo from the cookbook, recipes 5 to 7, all in the VM TERMINAL.

---

## If you prefer the terminal

```bash
# in the VM TERMINAL of the NemoClaw dashboard
id                                     # outside: you, the operator
nemoclaw my-assistant exec -- id       # inside: sandbox user
nemoclaw my-assistant skill list       # not "openclaw ...": it lives inside
nemoclaw my-assistant exec -- curl -sS https://example.com
# curl: (56) CONNECT tunnel failed, response 403
nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4
```

.lead It's optional: the same as the previous drawing, written as instructions.

Notes:
Other common errors: typing without clicking the black area (dashboard shortcuts fire); the `ExperimentalWarning: SQLite` line (ignore it); `openshell gateway status` doesn't exist (use `openshell status` or `openshell gateway info`); `openshell logs --tail` never ends (in openshell `--tail` follows: use `-n 20`); inference `unauthorized` in `status` (check the key); 403 from network policy (OPENSHELL TUI → [r] → [a], or `policy add`). The host/sandbox mix-up is the number one question in the forum.

---

## How to choose by task and risk

:::diagrama c61-elegir

Notes:
One click per task, from less to more risk. Click 1: coding with you alongside: Claude Code, Codex or Cursor with approvals. Click 2: unattended refactor: Deep Agents or a CLI inside OpenShell. Click 3: 24/7 chat assistant: OpenClaw or Hermes in NemoClaw. Click 4: cron that reads data and reports: sandbox and a reviewed skill. Click 5: the lethal trifecta sends it to the sandbox. The criterion isn't "which is best", it's "who's watching, what does it touch, who does it talk to, what survives".

---

## Your five-axis card

:::diagrama c61-ficha

Notes:
It's the class challenge. Have them do it with the agent they use at work, reading its official docs in the browser, with one link per row. Click 1: the empty card. Click 2: if it isn't documented, that's the finding. Close with the reminder: if they'll do the optional lab part about the skill library, they leave the instance running and keep going; if not, they save what they want and delete the instance in the Brev console with Delete (stopped, the disk keeps billing ≈USD 1.20 a day). Then check Billing.
