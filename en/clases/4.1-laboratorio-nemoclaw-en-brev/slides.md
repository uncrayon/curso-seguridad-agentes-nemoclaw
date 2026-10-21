## What you'll spin up today

:::diagrama brev-laboratorio

.lead Your rented office comes with everything: the agent, the locked room and the kit. The model runs in NVIDIA's cloud.

Notes:
Click 1: the Brev console. Click 2: your instance with the launchable. Click 3: the NemoClaw dashboard, where we'll do everything: chat and terminal in the browser. The instance is CPU-only (4 CPUs, 16 GiB) because the model runs outside.

---

## Brev from scratch

:::diagrama brev-pasos

Notes:
One click per step. Top menu: Compute, Agents, Launchables, Team, Billing, Docs. Coupon: Billing → Credits → Redeem Code. Organization selector at the top right. Deploy NemoClaw button. Under Compute, the instance turns Running in ≈1 min and shows $0.26/hr. RETRY rebuilds the whole sandbox; the red card is usually a visual bug.

---

## Set up your agent in the browser

1. Green **NemoClaw** button → new tab → sign in with NVIDIA
2. **SET UP IN THIS BROWSER** → **OPEN BROWSER SETUP →**
3. Agent **OpenClaw** · provider: from OpenRouter to **NVIDIA CLOUD**
4. Paste your `nvapi-` key → **CREATE AGENT**
5. **Building your agent** (≈3 min) → **YOUR AGENT IS LIVE**

:::tip
Your key goes only in that field. Never in the chat, a screenshot or a video.
:::

Notes:
Each student signs in with their own account. While it builds: don't reload the tab; if RETRY shows up and the log is moving, don't touch it. At the end: agent my-assistant, model nvidia/nemotron-3.5-super-vl-120b-a12b. Back to overview takes you to the dashboard.

---

## Your dashboard: 4 buttons

| Button | What it opens |
|---|---|
| **CHAT WITH AGENT** | The OpenClaw chat, to talk to your agent |
| **SANDBOX TERMINAL** | A terminal inside the room (user `sandbox`) |
| **VM TERMINAL** | The operator terminal, outside the room (user `ubuntu`) |
| **OPENSHELL TUI** | The guard's panel: policy and pending access |

.lead The operator terminal is where you paste the guides' commands.

Notes:
At the top of the dashboard: processor, memory, disk and the security status (20 allowed sites, 13 network policies). At the bottom, logs with All / VM / Gateway / Agent filters. In the VM TERMINAL: click inside the black area before typing; Shift+Esc closes it. The SQLite ExperimentalWarning line can be ignored.

---

## Verify as the operator

:::cols
**What the agent says**
"I work in /sandbox/.openclaw/workspace"
It may say it's `gateway-owner`
|||
**What the system shows**
`nemoclaw my-assistant exec -- whoami`
→ `sandbox`
:::

.lead What the agent says about itself is not evidence. The system is.

Notes:
In the chat: "Who are you and which folder do you work in?". In the VM TERMINAL: nemoclaw list, nemoclaw my-assistant status (inference healthy, phase Ready) and exec -- whoami / pwd (sandbox, /sandbox). This idea comes back in the next classes, especially when we cover security.

---

## Memory lives in the session

:::cols
**1 · Plant a fact**
Session `memo-41`
"Remember CODE-7Q4" → OK
|||
**2 · Ask**
Same session
→ CODE-7Q4
|||
**3 · Reset and ask**
`sessions reset memo-41`
→ "no lo se" (I don't know)
:::

.lead The front desk (the gateway) keeps the conversation, not the model.

Notes:
The four commands are in Part D of the README and in cookbook recipe 7. The chat behaves the same: under Sessions, a new conversation doesn't know the code. Workspace files survive the reset: we'll see that soon.

---

## Operator commands

```bash
nemoclaw list                         # your agent's sandbox
nemoclaw my-assistant status          # is the agent healthy?
nemoclaw my-assistant exec -- whoami  # who is it, really?
git clone --depth 1 https://github.com/uncrayon/curso-seguridad-agentes-nemoclaw ~/curso
```

.lead You paste them in the dashboard's VM TERMINAL. You don't install anything on your computer.

Notes:
The git clone puts the course files in ~/curso; a later class uses them (FAQ and skill). The OpenShell gateway listens on 18080 (openshell gateway info); the OpenClaw chat, on 18789.

---

## What each state costs

:::diagrama estados-instancia

:::tip
Do the whole lab in a single sitting. If you stop, **Stop** and come back soon. When you finish the lab practices, **Delete**.
:::

Notes:
Running ≈USD 0.25/h (the page shows $0.26/hr). Stopped, the disk bills ≈USD 0.05/h, ≈USD 1.20 per day: more than the coupon. Questions to the model are paid with build.nvidia.com credits, not Brev.

---

## If something goes wrong

| You see | Do this |
|---|---|
| It asks you to sign in again | Normal: use the same account |
| Red **RETRY** card | Don't touch it: check whether the log is moving |
| "out of credits" with a balance | Switch to the right organization in Brev |
| You type and the terminal doesn't react | Click inside the black area |
| `503 … no_healthy_upstream` | Wait a couple of minutes and reload |

Notes:
nemoclaw deploy no longer exists (removed in v0.0.117). The SQLite ExperimentalWarning line is not an error. Shift+Esc closes the terminal.

---

## Project progress

.lead Soporte NemoClaw has a home now. Measure how it answers today.

- Ask it: *"A student says: 'My notebook returns HTTP 401'. What do you tell them?"*
- Copy the answer into your project notes
- Later you give it the FAQ and compare

Notes:
You can ask in the chat or with nemoclaw my-assistant agent --session-key linea-base -m '…'. The no-skill baseline is what we'll improve with the course FAQ.
