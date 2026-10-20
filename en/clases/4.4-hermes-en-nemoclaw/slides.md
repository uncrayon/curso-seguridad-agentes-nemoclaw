## Swap the agent, not the security

:::diagrama c44-mismo-cuarto

Notes:
Same locked room, different assistant. Click 1: OpenClaw, the one from classes 4.1 to 4.3. Click 2: you swap it for Hermes (Nous Research, MIT license). Click 3: what stays the same: the OpenShell sandbox, the network policies, managed inference with the key on the host. Click 4: what's new, Hermes keeps memory across sessions and creates its own skills. NemoClaw ≠ OpenClaw: it's the question from class 1.1, now proven in the lab. It can also carry LangChain Deep Agents.

---

## Create the sandbox

:::diagrama c44-crear

Notes:
One click per step. 1: nemoclaw my-assistant stop (it stops, it isn't deleted). 2: the key with read -rsp, it doesn't show on screen or in the history. 3: NEMOCLAW_SANDBOX_NAME=mi-hermes nemohermes onboard; nemohermes is the NemoClaw CLI with Hermes as the default; provider NVIDIA Endpoints, web search none, suggested rules. 4: nemohermes mi-hermes status. 5: the new door on port 8642 (openshell forward list, curl /health). Click 6: the credit; before starting, check the balance in Billing.

---

## The operator way, in the terminal

```bash
nemoclaw my-assistant stop                        # pauses OpenClaw, doesn't delete it
read -rsp "NVIDIA API key: " NVIDIA_INFERENCE_API_KEY; echo
export NVIDIA_INFERENCE_API_KEY
NEMOCLAW_SANDBOX_NAME=mi-hermes nemohermes onboard
nemohermes mi-hermes status                       # is it healthy?
curl -sf http://127.0.0.1:8642/health             # does the new door answer?
```

.lead In this class the terminal is the way: before each line, say what it's for.

Notes:
In the onboarding questions: NVIDIA Endpoints, the model it suggests, web search none and the suggested rules. Onboarding takes several minutes the first time: cut in editing.

---

## OpenClaw vs. Hermes

:::diagrama c44-comparar

Notes:
Where each thing lives. One click per row: personality, memory (the diary, with a character limit), skills (Hermes also creates its own), conversations (SQLite in state.db; sessions export dumps them as JSONL) and the door for programs (OpenAI-compatible API on 8642, with a Bearer token). Click 6: what doesn't change. Web search changes too: Brave in OpenClaw, Tavily in Hermes. NemoClaw writes config.yaml: don't edit it by hand. To see it as the operator: nemohermes mi-hermes exec -- bash -lc 'ls -la /sandbox; ls -la /sandbox/.hermes'.

---

## The same skill, another agent

:::diagrama c44-misma-skill

.lead SKILL.md is an open format: both agents understand it.

Notes:
Click 1: the soporte-nemoclaw skill from class 4.3. Click 2: in OpenClaw it lives in skills/ on the desk. Click 3: in Hermes only two paths change (the FAQ in /sandbox/faq). Click 4: the result, without giving it the path. Commands: nemohermes mi-hermes skill install ~/soporte-nemoclaw-hermes/, nemohermes mi-hermes upload ~/faq/ /sandbox/faq/, nemohermes launch mi-hermes. Every skill is also a chat command: /soporte-nemoclaw. Standard: agentskills.io.

---

## An agent that learns on its own

:::diagrama c44-aprobacion

Notes:
Live error. Click 1: without approval, "remember X" is saved to MEMORY.md without asking you (read it as the operator). Click 2: if whoever asks is a malicious text, it's saved too and stays for every future conversation. Click 3: with /memory approval on, every note waits for your yes; /memory pending shows them and /memory reject rejects them. Click 4: same for the skills it creates. If the pinned version already ships with approval on, show /memory pending directly and say so.

---

## The OpenAI-compatible API

:::diagrama c44-dos-capas

Notes:
Click 1: your Python program talks to Hermes through the new door (base_url http://127.0.0.1:8642/v1), with the gateway token: TOKEN="$(nemohermes mi-hermes gateway-token --quiet)", never on screen. Click 2: layer 1, the instrumentor from class 3.4 (OpenAIInstrumentor) sends the trace to Phoenix: project soporte-nemoclaw-hermes. Click 3: layer 2, what Hermes did inside (its grep and cat calls) doesn't show up in Phoenix: it's in its history, nemohermes mi-hermes sessions export. Click 4: two layers of observability. Script: hermes_trazado.py.

---

## Common errors

| You see | Do this |
|---|---|
| `nemohermes: command not found` | Use `NEMOCLAW_AGENT=hermes nemoclaw onboard` |
| `Port 18789 is not available` | Use the next free port (check it in `openshell forward list`) |
| `401` when talking through the new door | Get the token again and keep it in a variable, without showing it |
| The skill doesn't show up in the chat | Leave with `/exit` and start a new conversation |
| `skill install` doesn't replace the old one | Remove it with `skill remove` and install it again |

Notes:
The token: TOKEN="$(nemohermes mi-hermes gateway-token --quiet)". Never show the output of gateway-token on camera.

---

## Project progress

:::diagrama c44-avance

.lead Shut down what you're not using: the Hermes room and Phoenix.

Notes:
Click 1: Soporte NemoClaw runs on two agents, with the same skill and the same personality, inside the same kind of room, plus a Python client with traces. Click 2: what we opened for Module 5: memory that writes itself, skills the agent creates and an API with a token. To shut down: docker stop phoenix, nemohermes mi-hermes stop, nemoclaw my-assistant start.
