# 6.2 · Build your skill library

> 🇪🇸 Original Spanish guide: [`clases/6.2-biblioteca-de-skills/README.md`](../../../clases/6.2-biblioteca-de-skills/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Write reusable skills, measure whether your agent finds them on its own, and bring them into your NemoClaw sandbox.

| | |
|---|---|
| **Video length** | ≈9 min |
| **Practice** | Notebook · [6.2-biblioteca-de-skills.ipynb (Spanish)](../../../clases/6.2-biblioteca-de-skills/6.2-biblioteca-de-skills.ipynb) (runs without a key, in MOCK mode) · optional last part in the Brev lab (VM TERMINAL) |
| **Skill** | Create reusable agent skills |
| **Materials** | [Slides](slides.html) · [Project library (Spanish)](../../../skill-library/README.md) · [FAQ (Spanish)](../../../FAQ.md) |

> **Module 6 is optional**, and so is this class's last part in the lab. If you do it, do it in the same sitting, after 6.1 (or after 5.3, if you skipped 6.1) and before you delete the instance (≈15 min, ≈USD 0.06). If you already deleted it when you finished 5.3, skip it: the notebook doesn't need the lab.

## What you'll achieve
- Write a correct `SKILL.md`: frontmatter (`name`, `description`) and a runbook an agent can follow.
- Build a mini harness that discovers skills, builds the menu (*progressive disclosure*) and runs them with **explicit** or **automatic** selection.
- Measure the **hit rate** of your descriptions with a set of requests, and bring the `skill-library/` library into your lab.

## Before you start
- Python 3.10+ or Google Colab. The `nvapi-` key is optional: without a key, the notebook uses a simulated model.
- You've done class [2.3](../2.3-funciones-a-herramientas/README.md) (loop with tools) and [4.3](../4.3-agentes-siempre-activos/README.md) (you installed your first skill in OpenClaw).
- For the lab part: your Brev instance **Running**, the NemoClaw dashboard open (green **NemoClaw** button) and the course cloned in `~/curso` (class 4.3).
- **Your credit:** the notebook uses no Brev credit. The lab part is optional and takes ≈15 min of your single sitting, right after the 6.1 practice, or after 5.3 if you skipped 6.1 (see [your Brev lab (Spanish)](../../../LABORATORIO.md)). When you finish it, save what you want and **Delete** your instance.

## The idea in one minute
Every session, your agent starts from scratch. A **skill** is how you say something once and keep it: a folder with a `SKILL.md`.

```
skill-library/diagnostico-api/SKILL.md
---
name: diagnostico-api
description: Diagnostica errores ... 401, 403, 404, 410, 429 o 5xx ... Úsala cuando el usuario pegue un error de la API ...
---
# diagnostico-api
## Pasos
1. Extrae el código HTTP del mensaje.
2. Herramienta: `diagnosticar_http` con `{"codigo": "<codigo>"}`.
3. Responde: qué pasó, causa probable, qué hacer.
```

The course's skill files are in Spanish. This one, `diagnostico-api` (API diagnosis), says: diagnose 401, 403, 404, 410, 429 or 5xx errors, and use it when the user pastes an API error. Its steps: extract the HTTP code from the message; call the `diagnosticar_http` (diagnose HTTP) tool with `{"codigo": "<codigo>"}`; answer with what happened, the likely cause, and what to do.

- **Progressive disclosure:** the agent only sees `name: description` for each skill (the menu). The body loads when it needs it.
- **Explicit selection:** you name the skill (`/diagnostico-api ...` or "read skill X and follow it").
- **Automatic selection:** the model picks it by comparing your request with the descriptions. **That's why the description is the most important line you write.**

The idea comes from *Voyager* (2023): an agent that saved what worked as reusable skills in a library that kept growing.

## Step by step

1. **Open the notebook.** In Colab or locally:
   ```bash
   pip install openai python-dotenv pyyaml
   jupyter notebook clases/6.2-biblioteca-de-skills/6.2-biblioteca-de-skills.ipynb
   ```
   Run the setup cells. You should see `Modo: MOCK (...)` or `Modo: EN VIVO · nvidia/nemotron-3.5-lightning-30b-a3b` (live mode).

2. **Read the anatomy (section 1).** The cell prints the full `diagnostico-api/SKILL.md`. Identify: frontmatter, purpose, steps, limits.

3. **Discover the skills (section 2).** The harness validates each `SKILL.md` with a real YAML parser. You should see 4 ✅.

4. **Compare the menu with the whole book (section 3).** You should see something like `Prompt con menú: ~1400 caracteres` (prompt with menu: ~1400 characters) versus `~7100` for all the skills. With 50 skills, that difference decides whether the prompt fits.

5. **Run the harness (section 6).**
   - Automatic: *"Me sale error 401 cuando llamo al modelo"* ("I get a 401 error when I call the model") → `cargar_skill(diagnostico-api)` (load skill) → `diagnosticar_http(401)`.
   - Explicit: `/lector-seguro-archivos muéstrame notas.txt` ("show me notes.txt", using the safe file reader skill) → the harness injects the skill and there's no `cargar_skill`.

6. **Evaluate your descriptions (section 7).** 15 requests, each with its expected skill. In MOCK you should see `Tasa de acierto: 12/15 = 80%` (hit rate), and with vague descriptions, `13%`.

7. **Fix the misses (✏️ Your turn 2).** Change the descriptions, **not** the runbook, until you reach ≥ 90 %. Then copy the new descriptions to `skill-library/<skill>/SKILL.md`.

8. **Trigger the failures (section 8 · 🧯).** YAML broken by `: `, an invalid name, a skill that doesn't exist, and escape paths (`../.env`).

9. **Bring the library to the lab (section 9).** This part is optional and follows the [6.1](../6.1-clis-de-agentes/README.md) practice (or the [5.3](../5.3-sandbox-y-politicas/README.md) one, if you skipped 6.1), with the instance still running. If you already deleted your instance, skip it: the notebook is enough.

   On the NemoClaw dashboard, click **VM TERMINAL** and click inside the black area. The library is already in the copy of the course you cloned in 4.3, under `~/curso/skill-library/`. If you don't have that folder, clone the course:
   ```bash
   git clone --depth 1 https://github.com/uncrayon/curso-seguridad-agentes-nemoclaw ~/curso
   ```
   To install a skill, give NemoClaw the folder that contains its `SKILL.md`, then check the list:
   ```bash
   nemoclaw my-assistant skill install ~/curso/skill-library/diagnostico-api/
   nemoclaw my-assistant skill list
   ```
   You should see `✓ Validated SKILL.md`, then `Installed diagnostico-api from path -> /sandbox/.openclaw/workspace/skills/diagnostico-api`, and `diagnostico-api` in the list. Repeat with `lector-seguro-archivos` and `resumen-diario`. Ignore the `ExperimentalWarning: SQLite…` line.

   `soporte-nemoclaw` is already installed from 4.3. To swap it for the library version, remove the old one and install the new one:
   ```bash
   nemoclaw my-assistant skill remove soporte-nemoclaw
   nemoclaw my-assistant skill install ~/curso/skill-library/soporte-nemoclaw/
   ```
   If you improved descriptions in the notebook, change them on the VM before installing. Open the file with `nano ~/curso/skill-library/diagnostico-api/SKILL.md`, paste your description, save with Ctrl+O and Enter, and exit with Ctrl+X.

10. **Try both selection modes in a new session.** The safest way to start from scratch is a new session key in the VM TERMINAL. First, automatic (you don't name the skill):
    ```bash
    nemoclaw my-assistant agent --session-key prueba-62a -m 'Me sale 401 al llamar al modelo, ¿qué hago?'
    ```
    Then explicit (you give it the skill's path), in another session:
    ```bash
    nemoclaw my-assistant agent --session-key prueba-62b -m 'Lee /sandbox/.openclaw/workspace/skills/diagnostico-api/SKILL.md y síguela: me sale 401.'
    ```
    You can also try it in the browser with **CHAT WITH AGENT**, in a new conversation.

11. **Close the lab: save and delete.** This is the course's last lab practice. When you delete the instance, everything on the VM is lost.
    - **Save what you want.** The course files (`~/curso`) are already on GitHub. To keep something your agent wrote, print it in the VM TERMINAL (for example, `nemoclaw my-assistant exec -- cat /sandbox/.openclaw/workspace/SOUL.md`), select it with the mouse and paste it into your notes.
    - **Delete the instance.** Close the terminal (**Shift+Escape**) and go to the Brev console: **Compute** → your instance (`nemoclaw-…`) → **Delete**. Confirm in the dialog that appears.
    - **Check your balance.** In the top menu, open **Billing**. Confirm the instance no longer shows up under **Compute**. Stopped, the disk would keep billing ≈USD 1.20 a day; deleted, nothing is billed. Details in [your Brev lab (Spanish)](../../../LABORATORIO.md).

## Check that it worked
- [ ] All 4 skills pass `validar_skill` (validate skill) with no ❌.
- [ ] You saw one automatic selection (`cargar_skill`) and one explicit selection (`/name`).
- [ ] Your hit rate in MOCK is ≥ 90 % after improving the descriptions.
- [ ] The harness rejected `../.env` and `/etc/passwd`.
- [ ] `nemoclaw <sandbox> skill list` shows your skills in the lab.
- [ ] If you did the lab part, you deleted your instance with **Delete** and checked **Billing**.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `YAML inválido en el frontmatter: mapping values are not allowed here` | The description has `: ` (colon and space) without quotes | Put the description in quotes or remove the colon |
| `skill install` doesn't show `✓ Validated SKILL.md` and complains about `SKILL.md` or the `name` | You passed the wrong folder or the frontmatter has no `name` | The path must point to the folder that **contains** `SKILL.md`, with YAML frontmatter and a `name` |
| Name rejected | `name` has spaces, accents or odd capitals | Only letters, numbers, `.`, `-` and `_`. Same as the folder name |
| The skill is installed but the agent doesn't use it on its own | The description doesn't say **when** to use it, or doesn't use the user's words | Rewrite the description and evaluate again. Open a **new session** |
| The agent uses the wrong skill | Two descriptions compete for the same words (e.g. "403") | Add to each one when **not** to use it, plus words that tell them apart |
| `skill install` fails with a skill of the same name (Hermes or Deep Agents) | The fallback doesn't replace an existing skill | `nemoclaw <sandbox> skill remove <name>` and reinstall |
| `skill install` says the path doesn't exist | You didn't clone the course on the VM, or you cloned it into another folder | Check with `ls ~/curso/skill-library`; if it's missing, run the `git clone` from step 9 |
| You type in the VM TERMINAL and nothing shows up | The terminal doesn't have focus | Click inside the black area |

## Challenge
Create the fifth skill, **`estimar-costo-brev`** (Brev cost estimate), which uses the `estimar_costo_brev` tool from class 2.3.
**Success criterion:** `validar_skill` flags no ❌ or ⚠️; you add 3 requests to `PEDIDOS_EVAL` (evaluation requests) and the overall rate stays at **≥ 90 %** without the other 4 skills dropping.

## Project milestone
The **Soporte NemoClaw** (NemoClaw Support) project now has its library in [`skill-library/` (Spanish)](../../../skill-library/README.md):

| Skill | What it's for |
|---|---|
| `soporte-nemoclaw` | Answers with the FAQ and cites the source. It's the skill from 4.3, with its description trimmed so it doesn't compete with `diagnostico-api` |
| `diagnostico-api` | Explains 401/403/404/410/429/5xx errors |
| `lector-seguro-archivos` (safe file reader) | Reads only inside `datos/` |
| `resumen-diario` (daily summary) | The summary that the 4.3 cron triggers |

Deliverable: the 4 skills installed in your sandbox, your evaluation table (before/after) in `docs/evaluacion-skills.md` (skills evaluation), and the improved descriptions in the repo.

## Resources
- NVIDIA DLI · The Always-On Agent (03c). This class is based on lesson 03c of the NVIDIA DLI course (Apache-2.0).
- NemoClaw · `skill install | list | remove` commands in the [command reference](https://docs.nvidia.com/nemoclaw/latest/).
- Anthropic · [Agent Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview): the `SKILL.md` format the course uses.
- Wang et al. 2023 · [Voyager](https://arxiv.org/abs/2305.16291): skill libraries that grow.
- OpenClaw · [Automation and tasks (cron vs. heartbeat)](https://docs.openclaw.ai/cron-vs-heartbeat).
