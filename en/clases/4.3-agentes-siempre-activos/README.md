# 4.3 · Agents in continuous and scheduled operation

> 🇪🇸 Original Spanish guide: [`clases/4.3-agentes-siempre-activos/README.md`](../../../clases/4.3-agentes-siempre-activos/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Install the `soporte-nemoclaw` skill with the course FAQ, schedule a task that writes a summary without anyone typing in the chat, and learn to describe any automation with 3 controls.

| | |
|---|---|
| Video length | ≈8 min |
| Practice | Lab on Brev: NemoClaw dashboard + browser terminal ([cookbook.md (Spanish)](../../../clases/4.3-agentes-siempre-activos/cookbook.md)) |
| Skill | Operate agents in continuous mode |

Materials: [slides](slides.html) · [terminal cookbook (Spanish)](../../../clases/4.3-agentes-siempre-activos/cookbook.md) · [soporte-nemoclaw skill (Spanish)](../../../clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/SKILL.md) · [FAQ (Spanish)](../../../FAQ.md)

> Based on lesson 03c of the NVIDIA DLI course "NemoClaw" (Apache-2.0).

## What you'll achieve

- Install a skill (a folder with a `SKILL.md`) in your agent and check that it uses it, first explicitly and then automatically.
- Schedule a task in **Automations** that writes a file without any chat message, and verify it as the operator.
- Describe any "always-on" mechanism with 3 controls: session, directive, and trigger.

## Before you start

- Classes 4.1 and 4.2 finished: instance **Running** in the Brev console, the NemoClaw dashboard open through the green **NemoClaw** button, and a customized `SOUL.md`.
- The course files on the machine, in `~/curso`. You cloned them in class 4.1. If they're missing, open **VM TERMINAL** on the dashboard, click inside the black area, and paste:
  ```bash
  git clone --depth 1 https://github.com/uncrayon/curso-seguridad-agentes-nemoclaw ~/curso
  ```
  That brings the skill (`~/curso/clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/`) and the course FAQ (`~/curso/datos/faq/`).
- Every `nemoclaw` command prints an `ExperimentalWarning: SQLite is an experimental feature` line. It's harmless: ignore it.
- Your credit: this practice uses ≈25 min of your single lab sitting (see [LABORATORIO.md (Spanish)](../../../LABORATORIO.md)). The scheduled task also spends model credits on build.nvidia.com, not Brev credit: one run used ≈112k tokens. If you stop for today, click **Stop** and come back soon; at the very end of the lab (after 6.1), **Delete**.

## The 3 controls

Every agent run, whether you asked for it or not, is described by three questions:

- **Session:** what context does the run inherit?
- **Directive:** where do its instructions come from?
- **Trigger:** what makes it start?

| Mechanism | Session | The directive lives in | Trigger | In this class |
|---|---|---|---|---|
| Skill | Reuses the caller's | `workspace/skills/<nombre>/SKILL.md` | A request in the conversation | You install it and use it |
| Heartbeat | A session dedicated to the heartbeat | `HEARTBEAT.md` | Gateway timer, every 30 min by default | Concept only |
| Cron (Automations) | Isolated: a new session on every fire | The automation's **Prompt** | Scheduled time (**Once**, **Interval**, or **Cron**) | You schedule it and verify it |
| Subagent | New; the parent agent keeps the handle | The instructions the parent gives it | The parent agent decides mid-turn | Concept only |

## Step by step

### Part A · See what a skill looks like (course page)

1. **Open the skill** [soporte-nemoclaw (Spanish)](../../../clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/SKILL.md) on the course site. Notice its three parts:
   - **The label** (between the two `---` lines): `name` is the skill's name and `description` says what it solves and the words a student would use to ask. The agent uses that description to decide whether the recipe fits.
   - **The steps:** classify the question, search the FAQ, answer in a fixed format, and cite the source.
   - **The rules:** never ask for keys, never invent commands, and only write inside `reportes/`.

   That's all a skill is: a folder with a `SKILL.md` file written in plain language.

### Part B · Install the skill and the FAQ (VM TERMINAL)

2. **Open the operator terminal.** On the NemoClaw dashboard, on the **MY-ASSISTANT** card, click **VM TERMINAL**. Click inside the black area before typing; otherwise your keys trigger dashboard shortcuts.

3. **Install the skill in the agent.** This command asks NemoClaw to check the skill folder and copy it onto the agent's desk:
   ```bash
   nemoclaw my-assistant skill install ~/curso/clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/
   ```
   You should see:
   ```text
   ✓ Validated SKILL.md
   Installed soporte-nemoclaw from path -> /sandbox/.openclaw/workspace/skills/soporte-nemoclaw
   ```
   NemoClaw checks that the folder has a `SKILL.md` with a label and a `name` before installing it.

4. **Upload the FAQ to the agent's desk.** This command copies the course's `faq/` folder into the workspace:
   ```bash
   nemoclaw my-assistant upload ~/curso/datos/faq/ /sandbox/.openclaw/workspace/
   ```
   The target ends in `workspace/`, not `faq/`. If you use `/sandbox/.openclaw/workspace/faq/` as the target, the folder ends up nested as `faq/faq/` and the skill can't find it.

5. **Check both.** This command lists, from inside the sandbox, the installed skill and the FAQ files:
   ```bash
   nemoclaw my-assistant exec -- ls /sandbox/.openclaw/workspace/skills/ /sandbox/.openclaw/workspace/faq/
   ```
   You should see `soporte-nemoclaw` in `skills/` and the FAQ `.md` files (`api-key.md`, `brev.md`, `errores-api.md`…) directly in `faq/`.

### Part C · Check that the agent uses it

6. **Explicit use (in the chat).** On the dashboard, click **CHAT WITH AGENT**. The OpenClaw chat opens in another tab. Type:
   > Lee /sandbox/.openclaw/workspace/skills/soporte-nemoclaw/SKILL.md y síguelo para esta duda de un estudiante: "Si detengo mi instancia de Brev, ¿me siguen cobrando?"

   (Read that SKILL.md and follow it for this student question: "If I stop my Brev instance, do they keep charging me?") You should see an answer with **Categoría:**, numbered steps, and **Fuente:** `faq/<archivo>.md`. This proves the agent follows the recipe when you give it the path.

7. **Automatic use (without the path).** Now ask in a **new** conversation, without mentioning the skill. You have two ways:
   - **In the chat:** open a new session from the sidebar (the **+** button next to **SESSIONS**) and type: *"Mi API key de NVIDIA me da 401, ¿qué hago?"* (My NVIDIA API key gives me a 401, what do I do?)
   - **In the VM TERMINAL:** this command asks the agent the same question in a session named `prueba-43`:
     ```bash
     nemoclaw my-assistant agent --session-key prueba-43 -m 'Mi API key de NVIDIA me da 401, ¿qué hago?'
     ```

   If the agent picks the skill on its own, the answer follows the skill's format. In the course test run it answered with **Categoría:** `api_key`, numbered steps, and **Fuente:** `faq/errores-api.md` and `faq/api-key.md`. The `prueba-43` session also shows up later in the chat sidebar.

   ![The agent's answer in the VM TERMINAL: number 1 marks the line Categoría api_key and number 2 marks the numbered steps taken from the FAQ](../../../assets/lab/15-terminal-respuesta-skill.png)

   If it doesn't use the skill, the description wasn't good enough: that's this class's challenge.

### Part D · Schedule a task in Automations

Now the agent will work without anyone typing to it. You'll schedule a task that runs **once**, 2 minutes from now, and deletes itself.

8. **Open Automations.** In the OpenClaw chat, click **Automations** in the sidebar. You'll see the list *Scheduled tasks and recurring agent runs* with the tasks the agent already has: `heartbeat-main` (**Every 30m**), **Memory Dreaming Promotion** (**Cron 0 3 \* \* \***), and `skill-collection-review-main` (**Every 7d**). Click **New automation**, top right.

   ![Automations page with the three built-in tasks; number 1 marks the New automation button](../../../assets/lab/24-automations-lista.jpg)

9. **Write the instruction.** In **Prompt**, paste:
   > Usa la skill soporte-nemoclaw. Lee los archivos de faq/ y escribe en reportes/resumen-faq.md un resumen de 5 líneas: qué temas cubre la FAQ y cuál es la pregunta más útil para alguien nuevo. No cambies ningún otro archivo.

   (Use the soporte-nemoclaw skill, read the faq/ files, and write a 5-line summary to reportes/resumen-faq.md: what topics the FAQ covers and the most useful question for a newcomer. Don't change any other file.) Leave **Action** on **Run agent task**, **Model** on **Default**, and **Reasoning** on **low**.

   ![New automation form: number 1 marks the Prompt field, 2 the Name field, and 4 the Create automation button](../../../assets/lab/25-automation-nueva.jpg)

10. **Give it a name and a schedule.**
    - In **GENERAL → Name**, type `soporte-resumen-faq`. Leave **Agent** on `main` and **Runs in** on **Isolated session**.
    - In **SCHEDULE → Repeat**, choose **Once**.
    - In **Run at**, set today's date and a time **2 minutes after** your clock. This field uses your browser's local time.
    - In **DELIVERY → Mode**, leave **None (internal)**: the result isn't posted to the chat.
    - Open **ADVANCED** and check that **Delete after run** is on. With **Once** it comes on.

    ![Form with Name soporte-resumen-faq (2) and, under SCHEDULE, the Once option with its Run at field (3)](../../../assets/lab/27-automation-una-vez.jpg)

11. **Create the task.** Click **Create automation** (not **Create & run now**). You should see `soporte-resumen-faq` in the list, with **NEXT RUN** at `in 2m`.

    ![Automations list with soporte-resumen-faq scheduled; the NEXT RUN column says in 2m](../../../assets/lab/28-automation-programada.jpg)

12. **Wait without typing in the chat.** Take your hands off the keyboard. At the set time, the task shows **Running** with a spinner. Then open the **Run history** tab. You should see a run with status **OK**, the model, the token count (≈112k in the course test run), and the summary the agent wrote, with an **Open run chat** link. Because it had **Delete after run**, the task no longer appears in the **All** list.

    ![Run history tab (1) with the run in OK status (2) and the agent's summary below](../../../assets/lab/30-automation-historial-ok.jpg)

### Part E · Check it as the operator (VM TERMINAL)

An **OK** in the history says the run finished, not that the file exists. You provide that proof.

13. **Read the file.** In the VM TERMINAL, this command lists the `reportes/` folder and prints the summary:
    ```bash
    nemoclaw my-assistant exec -- bash -lc 'ls -la /sandbox/.openclaw/workspace/reportes/; cat /sandbox/.openclaw/workspace/reportes/resumen-faq.md'
    ```
    You should see `resumen-faq.md` owned by `sandbox` (the room's user) and a text that starts with `# Resumen FAQ -` and the date, and ends with `Generado por la skill soporte-nemoclaw.` Nobody typed in the chat and the file exists: that's the proof.

    ![VM TERMINAL: number 1 marks the resumen-faq.md file owned by sandbox and 2 marks the summary ending in Generado por la skill soporte-nemoclaw](../../../assets/lab/31-resumen-operador.jpg)

    The file's time is in UTC, universal time. That's why it may not match your clock.

14. **Check the task list as the operator.** This command shows the agent's scheduled tasks, seen from inside the sandbox:
    ```bash
    nemoclaw my-assistant exec -- openclaw cron list
    ```
    You should see a table with `heartbeat:main` (every 30m), the memory task (`cron 0 3 * * *`), and `skill-collection-review` (every 7d). Your `soporte-resumen-faq` is gone: it deleted itself.

**Mind the model credit.** That run used ≈112k tokens. Never leave a task with an **Interval** of a few minutes running: it would spend that on every fire. To pause or delete a task, use the **⋯** menu on its row in **Automations**.

### Part F · Heartbeat and subagents (concept only)

- **Heartbeat:** every so often (30 min by default in OpenClaw) the agent wakes up in a dedicated session, checks pending items, and reads `HEARTBEAT.md` if it exists. In **Automations** it's the `heartbeat-main` task (**Every 30m**). In the lab, its history says **Skipped** with `heartbeat skipped: no-route`: that's normal, don't fix it. On your own install you adjust it with `NEMOCLAW_AGENT_HEARTBEAT_EVERY` before onboarding (details in the [cookbook (Spanish)](../../../clases/4.3-agentes-siempre-activos/cookbook.md), recipe 8).
- **Subagents:** the parent agent launches a child with a new session and passes it task instructions, like the subagents in class 3.3. The difference: here the child runs inside the same sandbox, under the same policy.

**Heads-up:** a scheduled task runs even when nobody's watching. An instruction like "send the daily report" fires anyway. Each fire uses an isolated session, but the shared files in the workspace can influence future runs. Name your tasks, review **Automations**, and delete the ones you don't recognize.

## Check that it worked

- [ ] `skill install` answered `✓ Validated SKILL.md` and `Installed soporte-nemoclaw`.
- [ ] `faq/` is in the workspace with the FAQ files (not in `faq/faq/`).
- [ ] A question with the skill path returns **Categoría**, steps, and **Fuente: faq/…**.
- [ ] A question **without** the path, in a new session, also follows the skill's format.
- [ ] Your `soporte-resumen-faq` automation ended in **OK** in **Run history**.
- [ ] You read `reportes/resumen-faq.md` as the operator, owned by `sandbox`.
- [ ] `openclaw cron list` no longer shows your task.
- [ ] You can explain skill, heartbeat, cron, and subagent in terms of session, directive, and trigger.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| **NEXT RUN** says `in 2h`, `in 6h`, or an odd date instead of `in 2m` | **Run at** uses your browser's local time and you set a different time or day. | Delete the task from the **⋯** menu and create it again with your clock's time plus 2 minutes. |
| **Run history** says **OK**, but there's no file | The agent said it finished without writing, or wrote to another path. | OK proves nothing on its own: read it as the operator (step 13). To search for it: `nemoclaw my-assistant exec -- bash -lc 'grep -rl "Generado por la skill soporte-nemoclaw" /sandbox/.openclaw/workspace/'`. |
| The task stays in **Running** for a long time | The model is slow to answer or the run hit its time limit. | Wait a few minutes and check **Run history**. If there's an error, check that **Inference** says `healthy` with `nemoclaw my-assistant status` and create the task again. |
| `heartbeat-main` says **Skipped** · `no-route` | That's how the heartbeat behaves in this lab. | It's normal. It isn't your task or your mistake. |
| The agent doesn't use the skill unless you give it the path | The label's `description` is vague ("skill de soporte", support skill) and doesn't match the question. | Rewrite the `description`: what it does, who it's for, and the words a student would use to ask. Reinstall with `skill install` and test in a **new** session. |
| `skill install` fails because of the `SKILL.md` | The label is missing, `name` is missing, or the name has characters that aren't allowed. | Label between `---` with `name` (only letters, numbers, dots, hyphens, and underscores) and `description`. |
| The skill answers "No encuentro la FAQ del curso en el workspace" ("I can't find the course FAQ in the workspace") | You didn't upload the FAQ, or it ended up in `faq/faq/` because the target ended in `faq/`. | Check with `nemoclaw my-assistant exec -- ls -R /sandbox/.openclaw/workspace/faq/` and upload again with target `/sandbox/.openclaw/workspace/`. |
| You type in the VM TERMINAL and odd things happen on the dashboard | The terminal didn't have focus and your keys triggered dashboard shortcuts. | Click inside the black area before typing. **Shift+Escape** closes the terminal and its processes. |

## Challenge

**Get the agent to discover the skill on its own.** Temporarily replace the `description` in your `SKILL.md` with `Skill de soporte.` (support skill), reinstall it, and ask the step 7 question in a new session. Then restore a good description (the original or a better one) and repeat. The commands are in the [cookbook (Spanish)](../../../clases/4.3-agentes-siempre-activos/cookbook.md), recipe 5.

Success criteria: with the vague description, the agent doesn't follow the skill's format; with the good one, in a new session and **without giving it the path**, it answers with **Categoría**, steps, and **Fuente:** `faq/…`. Write down both answers.

## Project milestone

**Soporte NemoClaw (NemoClaw Support) is now deployed on OpenClaw:**

- The `soporte-nemoclaw` skill installed, with the course FAQ in `faq/` inside the workspace.
- A scheduled task in **Automations** that left `reportes/resumen-faq.md` with no intervention.

Repeat the 4.1 baseline question ("My notebook returns HTTP 401") and compare. Save the new answer in your project notes (`proyecto/linea-base-4.1.md`), below the previous one, and write down the difference: does it cite the FAQ now? Does it follow the categories from the class 3.1 router? In Module 5 you'll review the risks all this opened up: an agent with data, tools, and jobs that run on their own.

## Resources

- [NemoClaw · Command reference: `skill install`, `skill list`, `skill remove`, `upload`](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands.md)
- [NemoClaw · Configure agent heartbeats](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/configure-agents/configure-agent-heartbeats.md)
- [OpenClaw · Automation: cron vs. heartbeat](https://docs.openclaw.ai/cron-vs-heartbeat)
- [Anthropic · Agent Skills](https://www.anthropic.com/news/skills) and [Voyager (arXiv 2305.16291)](https://arxiv.org/abs/2305.16291)
- `man 8 cron` for classic Unix cron (the idea is the same: a time and a command)
