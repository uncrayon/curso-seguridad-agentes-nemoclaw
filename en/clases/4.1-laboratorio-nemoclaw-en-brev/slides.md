## What you'll spin up today

:::diagrama brev-laboratorio

.lead Your rented office comes with everything: the agent, the locked room and the kit. The model runs in NVIDIA's cloud.

Notes:
Click 1: the Brev console. Click 2: your instance with the launchable. Click 3: the NVIDIA course page, where we'll do almost everything. The instance is CPU-only because the model runs outside.

---

## Brev from scratch

:::diagrama brev-pasos

Notes:
One click per step. Expected instance: n2d-standard-4, 4 vCPU / 16 GiB, marked Free or ≈USD 0.15/h. VERIFY IN LAB. RETRY rebuilds the whole sandbox; the red card is usually a visual bug.

---

## The session cookie, calmly

:::diagrama cookie-segura

| Your URL contains | Look for the cookie |
|---|---|
| `brevlab.com` | `CF_Authorization` |
| `apps.run.brev.nvidia.com` | `_pomerium` |
| `gobrev.dev` | `__Host-skybridge-brev-prd` |

Notes:
The event wristband. Chrome/Edge: F12 → Application → Storage → Cookies → the launchable's URL → double-click on Value. Firefox: Storage → Cookies. Safari: turn on developer features. Blur the value when recording.

---

## The 4 checks

:::diagrama cuatro-rutas

.lead If one turns red, open that check: it tells you what to do.

Notes:
Your session = metadata (/api/agent, hands over the gateway token). Front desk = gateway (/cli/gateway). Terminal = /ws/terminal. Health = /healthz. The gateway token is a second credential; we come back to it in Module 5.

---

## Control, agent and memory

:::cols
**1 · Control**
The model alone
It answers, no tools
|||
**2 · Agent**
Uses a tool
The ⚙️ and ✓ rows are its actions
|||
**3 · Memory**
Remembers a code
You reset the conversation and it forgets
:::

.lead The front desk (the gateway) keeps the conversation, not your browser.

Notes:
Workspace files survive the reset: that's class 4.2.

---

## If you prefer the terminal

```bash
brev ls                         # your instances and their state
brev shell <instancia>          # get into the machine
nemoclaw list                   # your agent's sandbox
nemoclaw my-assistant status    # is the agent healthy?
```

.lead It's optional: the same thing you did with clicks, written as instructions.

Notes:
brev shell without --host (issue #11534). The dashboard URL carries the token after #token=: treat it as a password.

---

## What each state costs

:::diagrama estados-instancia

:::tip
When you're done for the day: Brev console → your instance → **Stop**. When you resume, copy a fresh cookie.
:::

Notes:
Disk: 0.0001314 USD per GB-hour while the instance exists. If there's no capacity, Start fails and the data is out of reach until it comes back. Without credits, Brev pauses the instances that can be stopped.

---

## If something goes wrong

| You see | Do this |
|---|---|
| `OpenClaw is starting…` | Wait: it retries on its own |
| **OpenClaw ⚠** or session expired | Copy a fresh cookie and try again |
| "out of credits" with a balance | Switch to the right organization in Brev |
| Red **RETRY** card | Don't touch it: check whether the log is moving |

Notes:
nemoclaw deploy no longer exists (removed in v0.0.117). If an old tutorial mentions it, ignore it. "Could not resolve hostname": recipe 12 in the cookbook.

---

## Project progress

.lead Soporte NemoClaw has a home now. Measure how it answers today.

- Ask it: *"A student says: 'My notebook returns HTTP 401'. What do you tell them?"*
- Copy the answer into your project notes
- In class 4.3 you give it the FAQ and compare

Notes:
The no-skill baseline is what we'll improve with the course FAQ.
