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
Click 1: the skill uses your same conversation, follows its SKILL.md and starts when you ask. Click 2: cron starts at a set time, in a new, empty conversation (isolated session), with the scheduled message (payload.message). Click 3: heartbeat and subagent, dashed because today they're concept only: no cell in 03c fires them. NemoClaw sets up the heartbeat in an isolated session. Click 4: what we run today.

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
Click 1: the soporte-nemoclaw skill. Click 2: the live error, a copy without name: NemoClaw checks the label before uploading it. Click 3: the good copy lands in skills/ on the desk. Click 4: the FAQ lands in faq/. skill install validates the frontmatter and calls openclaw skills install --agent main --force; reinstalling replaces the one with the same name.

---

## The operator way, in the terminal

```bash
# Install the skill and check it's there
nemoclaw my-assistant skill install ./soporte-nemoclaw/
nemoclaw my-assistant skill list

# Upload the FAQ to the agent's desk and check it
nemoclaw my-assistant upload ./faq/ /sandbox/.openclaw/workspace/faq/
nemoclaw my-assistant exec --workdir /sandbox/.openclaw/workspace -- ls faq
```

.lead Installing the skill is today's only step that goes through the terminal. The rest, with clicks.

Notes:
Before each line, say what it's for. Live error: nemoclaw my-assistant skill install ./soporte-rota/ (a copy without the name: line).

---

## Explicit vs. automatic

:::diagrama c43-explicita

Notes:
Click 1: explicit, you give it the path: proves it can follow it (Step 1 in 03c). Click 2: automatic, you only describe the problem: proves it picks it on its own (the "Test · trigger a skill during the conversation" panel). Click 3: always in a new session. The 03c cell says it: getting the runbook reference doesn't prove automatic selection.

---

## Cron: work without chat

:::diagrama c43-cron

Notes:
One click per stage: the alarm (cron.add with schedule.kind "at"), it rings, a new empty conversation (sessionTarget "isolated"), it follows the message, it leaves the file reportes/resumen-faq-<id>.md. Click 6: toISOString() gives the time in UTC (it ends in Z). The full snippet is on the class page, step 10: paste it into the "Call models.list and cron.list" node in 03a, after "Open the gateway connection". Then cron.runs until you see ok.

---

## You do the proving

:::diagrama c43-prueba

Notes:
Click 1: a status ok in cron.runs isn't enough. Click 2: you read it, as the operator (the Step 1b cell in 03b). Click 3: the file exists. Click 4: nobody typed in the chat. From the terminal: nemoclaw my-assistant exec -- bash -lc 'cat /sandbox/.openclaw/workspace/course-cron-*.txt' (exec doesn't use a shell: for * or &&, wrap it in bash -lc).

---

## It runs even when nobody's watching

:::diagrama c43-nadie-mira

Notes:
Click 1: "Send the daily report" fires even when you're away. Click 2: each fire is an isolated session, but the workspace is shared and affects what comes next. Click 3: each fire spends model credits. Click 4: name your jobs, review cron.list and delete what you don't recognize. Bridge to Module 5: an agent with data, tools and autonomous jobs is the lethal trifecta scenario.

---

## Common errors

| You see | Do this |
|---|---|
| The task doesn't say `ok` in 3 minutes | Check the task list and that the instance is running |
| It ran at a different time | Add your time zone: the agent uses universal time |
| It says `ok`, but you don't see the file | Read it as the operator and search for it by name |
| The agent doesn't pick the skill on its own | Improve the description, reinstall it and start a new conversation |
| `skill install` fails | Check that the label has a `name` |
| "No encuentro la FAQ" | Upload it to `workspace/faq/` (without ending up in `faq/faq/`) |

Notes:
Mexico City time zone: -06:00. With deleteAfterRun, some OpenClaw versions reject cron.remove because the job already deleted itself: confirm with cron.list. Search by name: grep -rl.

---

## Project progress

.lead Soporte NemoClaw now lives in OpenClaw.

- The `soporte-nemoclaw` skill and the FAQ on its desk
- A scheduled task that leaves a summary of the FAQ
- Repeat the 401 question and compare it with the one from class 4.1

What risks did we open? We'll see in Module 5.

Notes:
Save the new answer below the previous one in proyecto/linea-base-4.1.md.
