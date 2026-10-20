## A recipe and an alarm clock

:::diagrama c43-receta-alarma

Notes:
The two new words. Click 1: the skill, a recipe card the agent reads when it needs it. Click 2: the scheduled task (cron), the alarm clock: at the set time, the agent works alone. Click 3: that's the whole point and the whole risk.

---

## The 3 controls

:::diagrama c43-controles

Notes:
One click per question: session (what conversation does it remember?), directive (what instructions does it follow?), trigger (what makes it start?). Click 4: together they describe an always-on agent. Click 5: they work for any automation, from OpenClaw or any other tool. In Module 6 we use them to compare CLIs.

---

## Four mechanisms, same questions

:::diagrama c43-mecanismos

Notes:
Click 1: the skill uses your same conversation, follows its SKILL.md and starts when you ask. Click 2: cron starts at a set time, in a new, empty conversation (Isolated session), with the automation's Prompt. Click 3: heartbeat and subagent, dashed because today they're concept only. The heartbeat shows up in Automations as heartbeat-main, every 30 min; in the lab its history says Skipped · no-route, and that's normal. Click 4: what we run today.

---

## Anatomy of a skill

:::diagrama c43-anatomia

Notes:
The soporte-nemoclaw recipe card, part by part. Click 1: the label (the frontmatter), with name and description. Click 2: the steps. Click 3: the rules. Click 4: the description decides whether the agent discovers it on its own. The name only allows letters, numbers, dots, hyphens and underscores. The full skill (in Spanish) is on the class page.

---

## Install: procedure + knowledge

:::diagrama c43-instalar

.lead The skill is the procedure. The FAQ is the knowledge.

Notes:
Click 1: the soporte-nemoclaw skill. Click 2: the live error, a copy without name: NemoClaw checks the label before uploading it. Click 3: the good copy lands in skills/ on the desk: "✓ Validated SKILL.md" and "Installed soporte-nemoclaw from path -> /sandbox/.openclaw/workspace/skills/soporte-nemoclaw". Click 4: the FAQ lands in faq/. Careful with upload: the target is workspace/, not faq/, or you get faq/faq.

---

## The operator way, in the terminal

```bash
# Install the skill
nemoclaw my-assistant skill install ~/curso/clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/

# Upload the FAQ to the agent's desk (the target is workspace/)
nemoclaw my-assistant upload ~/curso/datos/faq/ /sandbox/.openclaw/workspace/

# Check it from inside the room
nemoclaw my-assistant exec -- ls /sandbox/.openclaw/workspace/skills/ /sandbox/.openclaw/workspace/faq/
```

.lead Installing goes through the VM TERMINAL. Scheduling the task, with clicks in Automations.

Notes:
On the NemoClaw dashboard, VM TERMINAL; click inside the black area before typing. Before each line, say what it's for. The SQLite ExperimentalWarning line is harmless. Live error: nemoclaw my-assistant skill install ~/soporte-rota/ (a copy without the name: line).

---

## Explicit vs. automatic

:::diagrama c43-explicita

Notes:
Click 1: explicit, you give it the path in the chat (CHAT WITH AGENT): proves it can follow it. Click 2: automatic, you only describe the problem: proves it picks it on its own. In the VM TERMINAL: nemoclaw my-assistant agent --session-key prueba-43 -m 'Mi API key de NVIDIA me da 401, ¿qué hago?' answered Categoría api_key, steps, and Fuente: faq/errores-api.md, faq/api-key.md. Click 3: always in a new session. Following a path you gave it doesn't prove it picks it on its own.

---

## Cron: work without chat

:::diagrama c43-cron

Notes:
One click per stage: the alarm (Automations → New automation, Repeat Once, Run at 2 minutes from now), it rings, a new empty conversation (Runs in: Isolated session), it follows the Prompt with the skill, it leaves the file reportes/resumen-faq.md. Click 6: Run at uses your browser's local time; the date inside the file is in UTC. Name soporte-resumen-faq, Delivery None, Advanced → Delete after run on. The list says in 2m, then Running, and Run history says OK with ≈112k tokens.

---

## You do the proving

:::diagrama c43-prueba

Notes:
Click 1: an OK in Run history isn't enough. Click 2: you read it, as the operator, in the VM TERMINAL: nemoclaw my-assistant exec -- bash -lc 'ls -la /sandbox/.openclaw/workspace/reportes/; cat /sandbox/.openclaw/workspace/reportes/resumen-faq.md'. Click 3: the file exists, owned by sandbox, with the line "Generado por la skill soporte-nemoclaw.". Click 4: nobody typed in the chat. And nemoclaw my-assistant exec -- openclaw cron list confirms the task deleted itself.

---

## It runs even when nobody's watching

:::diagrama c43-nadie-mira

Notes:
Click 1: "Send the daily report" fires even when you're away. Click 2: each fire is an isolated session, but the workspace is shared and affects what comes next. Click 3: each fire spends model credits: our task used ≈112k tokens. Never leave an Interval of a few minutes running. Click 4: name your tasks, review Automations, and pause or delete from the ⋯ menu what you don't recognize. Bridge to Module 5: an agent with data, tools and autonomous jobs is the lethal trifecta scenario.

---

## Common errors

| You see | Do this |
|---|---|
| **NEXT RUN** doesn't say `in 2m` | **Run at** uses your browser's time: set your time + 2 min |
| It stays in **Running** for a long time | Wait and check **Run history**; make sure inference is healthy |
| It says **OK**, but you don't see the file | Read it as the operator and search for it by name |
| The agent doesn't pick the skill on its own | Improve the description, reinstall it and start a new conversation |
| `skill install` fails | Check that the label has a `name` |
| "No encuentro la FAQ" | Upload it to `workspace/faq/` (without ending up in `faq/faq/`) |

Notes:
The file's time is in UTC (Mexico City is 6 hours behind). heartbeat-main in Skipped · no-route is normal in the lab. Search by name: grep -rl "Generado por la skill soporte-nemoclaw". Inference status: nemoclaw my-assistant status.

---

## Project progress

.lead Soporte NemoClaw now lives in OpenClaw.

- The `soporte-nemoclaw` skill and the FAQ on its desk
- A task in Automations that left a summary of the FAQ
- Repeat the 401 question and compare it with the one from class 4.1

What risks did we open? We'll see in Module 5.

Notes:
Save the new answer below the previous one in proyecto/linea-base-4.1.md. If you stop for today: Stop in the Brev console and come back soon.
