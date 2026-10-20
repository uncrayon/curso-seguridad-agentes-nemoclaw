# 4.3 · Agents in continuous and scheduled operation

> 🇪🇸 Original Spanish guide: [`clases/4.3-agentes-siempre-activos/README.md`](../../../clases/4.3-agentes-siempre-activos/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Install the `soporte-nemoclaw` skill with the course FAQ, schedule a task that writes a summary without anyone typing in the chat, and learn to describe any automation with 3 controls.

| | |
|---|---|
| Video length | ≈8 min |
| Practice | Lab on Brev: NVIDIA course page + terminal ([cookbook.md (Spanish)](../../../clases/4.3-agentes-siempre-activos/cookbook.md)) |
| Skill | Operate agents in continuous mode |

Materials: [slides](slides.html) · [terminal cookbook (Spanish)](../../../clases/4.3-agentes-siempre-activos/cookbook.md) · [soporte-nemoclaw skill (Spanish)](../../../clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/SKILL.md) · [FAQ (Spanish)](../../../FAQ.md)

> Based on lesson 03c-always-on from the NVIDIA DLI course (Apache-2.0).

## What you'll achieve

- Install a skill (a folder with a `SKILL.md`) in your agent and check that it uses it, first explicitly and then automatically.
- Schedule a task with the gateway's cron that writes a file without any chat message, and verify it as the operator.
- Describe any "always-on" mechanism with 3 controls: session, directive, and trigger.

## Before you start

- Classes 4.1 and 4.2 finished: instance in `RUNNING`, **Test connection** green in [lesson 03a](https://nvdli.github.io/NemoClawDLI/nemoclaw/03a-kickstart.html), and a customized `SOUL.md`.
- `brev shell <instancia>` working.
- On your computer, the course repository with:
  - the skill: [`clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/SKILL.md`](../../../clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/SKILL.md) (Spanish)
  - the course FAQ: `datos/faq/*.md`

## The 3 controls

Every agent run, whether you asked for it or not, is described by three questions:

- **Session:** what context does the run inherit?
- **Directive:** where do its instructions come from?
- **Trigger:** what makes it start?

| Mechanism | Session | The directive lives in | Trigger | In this class |
|---|---|---|---|---|
| Skill | Reuses the caller's | `workspace/skills/<nombre>/SKILL.md` | A request in the conversation | You install it and use it |
| Heartbeat | A session dedicated to the heartbeat | `HEARTBEAT.md` | Gateway timer, every 30 min by default | Concept only |
| Cron | Isolated: a new session on every fire | The job's `payload.message` | A scheduled time | You schedule it and verify it |
| Subagent | New; the parent agent keeps the handle | The instructions the parent gives it | The parent agent decides mid-turn | Concept only |

## Step by step

### Part A · See what a skill looks like (course page)

1. **Open the lesson** [The Always-On Agent](https://nvdli.github.io/NemoClawDLI/nemoclaw/03c-always-on.html). Check that the pill says **OpenClaw ✓**.

2. **Run Step 1 · Read a skill and its runbook.** In the **Install a practice skill, then explicitly read it in a fresh session** flow, click **▶ Run all**:
   - **Install and verify the fixture** creates `/sandbox/.openclaw/workspace/skills/course-triage-<id>/` with a `SKILL.md` and a `runbook.md`, and reads them back.
   - **Use the installed skill** opens a new session and asks the agent to read that `SKILL.md` and follow it for a practice incident.

   Open the code of the first node and look at the shape of the `SKILL.md`:
   ```markdown
   ---
   name: course-triage-<id>
   description: Review a checkout-service incident using the bundled practice runbook; propose changes without executing them.
   ---
   Read runbook.md in this skill directory. Confirm service and time window. ...
   ```
   You should see: the agent's answer with the runbook's `BOOK-…` reference. The cell warns you: this proves **explicit use** (you gave it the path), not that the agent discovers the skill on its own.

### Part B · Install the soporte-nemoclaw skill (terminal)

3. **Bring the skill and the FAQ to the Brev machine.** Pick one option (details in the [cookbook (Spanish)](../../../clases/4.3-agentes-siempre-activos/cookbook.md), recipe 1):
   ```bash
   # On your computer, from the root of the course repo
   brev copy ./clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw <instancia>:/home/ubuntu/soporte-nemoclaw
   brev copy ./datos/faq <instancia>:/home/ubuntu/faq
   ```
   `[VERIFY IN LAB: that brev copy accepts folders and that home is /home/ubuntu]`. If not, the cookbook has the skill ready to paste with a heredoc.

4. **Install it in the sandbox.** In `brev shell <instancia>`:
   ```bash
   cd ~
   nemoclaw my-assistant skill install ./soporte-nemoclaw/
   nemoclaw my-assistant skill list
   ```
   NemoClaw checks that the folder has a `SKILL.md` with frontmatter and a `name`, and then calls OpenClaw's native command (`openclaw skills install … --agent main --force`).
   You should see: `soporte-nemoclaw` in the list. `[VERIFY IN LAB: output of skill install and skill list]`

5. **Copy the FAQ into the workspace:**
   ```bash
   nemoclaw my-assistant upload ./faq/ /sandbox/.openclaw/workspace/faq/
   nemoclaw my-assistant exec --workdir /sandbox/.openclaw/workspace -- ls -la faq
   ```
   You should see: the FAQ `.md` files inside `faq/` (not in `faq/faq/`). `[VERIFY IN LAB: how upload nests a folder]`

### Part C · Check that the agent uses it

6. **Explicit use.** On the 03c page, scroll down to **Try it · trigger a skill in conversation** and type (or use cookbook recipe 4):
   > Read /sandbox/.openclaw/workspace/skills/soporte-nemoclaw/SKILL.md and follow it for this student question: "brev shell gives me ssh: Could not resolve hostname".

   You should see: an answer with **Categoría:** (category) `brev`, numbered steps, and **Fuente:** (source) `faq/<archivo>.md`. The skill is written in Spanish, so its labels are too. Check the `⚙️` rows: the agent ran `ls`, `grep`, or `cat` on `faq/`. `[VERIFY IN LAB: path where the skill was installed]`

7. **Automatic use.** Open a **new** conversation and ask **without** giving the path:
   > A student says: "My notebook returns HTTP 401 when I call the model". What do you tell them?

   If the agent uses the skill on its own, the answer follows the skill's format and cites the FAQ. If not, the description wasn't good enough: that's this class's challenge.

### Part D · Watch a scheduled write (course page)

8. **Run Step 2 · Inspect your running agent.** In the **Observe one scheduled write and remove the owned job** flow, click **▶ Run** on the **Schedule, verify, and clean up** node. The cell calls the gateway with:
   ```js
   state.call("cron.add", {
     name, schedule: {kind: "at", at: new Date(Date.now() + 15000).toISOString()}, deleteAfterRun: true,
     sessionTarget: "isolated", wakeMode: "now",
     delivery: {mode: "none"},
     payload: {kind: "agentTurn", message: "Write the file specified by the JSON object below. …", timeoutSeconds: 120}
   });
   ```
   Then it queries `cron.runs` every 5 seconds, for up to 3 minutes.

   **Don't type anything in the chat while it waits.** Leave the tab open until the cleanup finishes.

   You should see: `Scheduled run: Ns elapsed; ok` and the message `Verified a successful scheduled run and its new file. No new chat message was sent when it fired.`

9. **Read it yourself, as the operator.** In `brev shell <instancia>`:
   ```bash
   nemoclaw my-assistant exec -- bash -lc 'ls -la /sandbox/.openclaw/workspace/course-cron-*.txt; cat /sandbox/.openclaw/workspace/course-cron-*.txt'
   ```
   You should see: a `course-cron-<id>.txt` file with `CRON-<id>` as its content. Nobody typed in the chat, and the file exists: that's the proof.

### Part E · Schedule the Soporte NemoClaw summary

10. **Open lesson 03a** and scroll down to the **Gateway · WebSocket protocol, step by step** flow.
    1. Run **Open the gateway connection**.
    2. Open the code of the **Call models.list and cron.list** node, delete its contents, and paste this:

    ```js
    // Soporte NemoClaw scheduled job: a FAQ summary, with no chat messages.
    if (!state.call) { helpers.log("Ejecuta primero el nodo Abre la conexión del gateway."); return; }

    const id = helpers.randomId();
    const archivo = "/sandbox/.openclaw/workspace/reportes/resumen-faq-" + id + ".md";
    const cuando = new Date(Date.now() + 60000).toISOString(); // 60 s from now, in UTC (ends in Z)

    const job = await state.call("cron.add", {
      name: "soporte-resumen-" + id,
      schedule: { kind: "at", at: cuando },
      deleteAfterRun: true,        // deletes itself after it runs
      sessionTarget: "isolated",   // a new session on every fire
      wakeMode: "now",
      delivery: { mode: "none" },  // doesn't send messages to any channel
      payload: {
        kind: "agentTurn",
        timeoutSeconds: 180,
        message: "Read /sandbox/.openclaw/workspace/skills/soporte-nemoclaw/SKILL.md and follow its Modo reporte section. " +
          "Write the FAQ summary to " + archivo + ". Do not modify other files or send messages."
      }
    });
    if (!job?.id) throw new Error("cron.add no devolvió un id; revisa cron.list");
    helpers.log({ jobId: job.id, programadaPara: cuando, archivo });

    // Check the run history every 5 s, for up to 4 minutes
    const limite = Date.now() + 240000;
    while (Date.now() < limite) {
      const historial = await state.call("cron.runs", { id: job.id, limit: 20 });
      const corridas = historial?.entries || historial?.runs || [];
      helpers.log("estado: " + (corridas[0]?.status || "todavía no corre"));
      if (corridas.some(c => c.status === "ok")) { helpers.log("Listo. Ahora léelo como operador."); return { archivo }; }
      const mala = corridas.find(c => c.status === "error" || c.status === "skipped");
      if (mala) { helpers.log.details("corrida fallida", mala); throw new Error("La ejecución programada falló: " + (mala.error || mala.status)); }
      await helpers.delay(5000, helpers.signal);
    }
    throw new Error("No hubo una ejecución correcta en 4 minutos; revisa cron.list y la hora programada");
    ```

    The prompt points the agent to the skill's `Modo reporte` (report mode) section, so keep that name exactly as written. The log and error strings are in Spanish, like the rest of the course code: `estado` is the run status, and `Listo. Ahora léelo como operador.` means "Done. Now read it as the operator."

    3. Click **▶ Run** on that node. Don't type in the chat.

    `[VERIFY IN LAB: this snippet reuses the same cron.add parameters as lesson 03c; test it before recording]`

    To get the node's original code back, use **↺ Reset**. Running it afterward shows you `cron.list`: your job should no longer appear, because `deleteAfterRun` deletes it.

11. **Read the summary as the operator:**
    ```bash
    nemoclaw my-assistant exec -- bash -lc 'ls -la /sandbox/.openclaw/workspace/reportes/ && cat /sandbox/.openclaw/workspace/reportes/resumen-faq-*.md'
    ```
    You should see: a Markdown file with one section per category, questions with their source file, and the line "Generado por la skill soporte-nemoclaw" ("Generated by the soporte-nemoclaw skill").

### Part F · Heartbeat and subagents (concept only)

- **Heartbeat:** every so often (30 min by default in OpenClaw), the agent wakes up in a dedicated session, checks pending items, and reads `HEARTBEAT.md` if it exists. NemoClaw configures that isolated session so your normal activity doesn't replace it. Don't change it in the lab; in your own install, you adjust it with `NEMOCLAW_AGENT_HEARTBEAT_EVERY` before onboarding, or with `openclaw config set agents.defaults.heartbeat.every 2h` inside the sandbox (`0m` turns it off). No step in this class fires it: don't wait for it.
- **Subagents:** the parent agent launches a child with a new session and passes it task instructions, like the subagents from class 3.3. The difference: here the child runs inside the same sandbox, under the same policy.

**Warning:** a scheduled job runs even when nobody is watching. An instruction like "send the daily report" fires all the same. Each fire uses an isolated session, but shared files in the workspace can still influence future runs. Name your jobs, review `cron.list`, and delete the ones you don't recognize.

## Check that it worked

- [ ] The 03c practice skill flow finished with the `BOOK-…` reference.
- [ ] `nemoclaw my-assistant skill list` shows `soporte-nemoclaw`.
- [ ] `faq/` is in the workspace with the FAQ files.
- [ ] A question with the skill path returns **Categoría**, steps, and **Fuente: faq/…**.
- [ ] The 03c cron finished in `ok`, and you read `course-cron-<id>.txt` as the operator.
- [ ] Your `soporte-resumen-…` cron left `reportes/resumen-faq-<id>.md`, and you read it as the operator.
- [ ] You can explain skill, heartbeat, cron, and subagent in terms of session, directive, and trigger.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `No successful scheduled run observed within three minutes` (or your snippet runs out its 4 min) | The `at` time ended up in the past or too far away, the gateway restarted, or the instance was paused. | Check `cron.list` (the original 03a node). Always use `new Date(Date.now() + 60000).toISOString()`. Run **Test connection** again and retry. |
| The cron fired at a different time | You wrote the time without a time zone. `toISOString()` always returns UTC (it ends in `Z`); Mexico City is at UTC-6. | Write the time with an explicit offset, for example `"2026-10-20T09:00:00-06:00"`, or compute it from `Date.now()`. `[VERIFY IN LAB: how the gateway interprets a time without an offset]` |
| `Scheduled agent run reported an error: …` | The agent turn failed (model, timeout, or permissions). | Read the run details. Raise `timeoutSeconds`. Run the **Health check** (the *Detect & recover* flow). |
| The job "ran" but there's no file | The agent reported success without writing, or wrote to another path. | Cron proves nothing on its own: read the file as the operator. Look with `nemoclaw my-assistant exec -- bash -lc 'ls -la /sandbox/.openclaw/workspace/reportes/'`. |
| `Inspect/remove the prior owned job before starting another` | The page saved the ID of a previous job that wasn't cleaned up. | Run the **Retry removal of the owned job** node. |
| `Cleanup incomplete; run Remove owned job. Retained id: …` | You closed the tab, or `cron.remove` failed. | Use the ID with **Retry removal of the owned job**. With `deleteAfterRun`, some OpenClaw versions reject `cron.remove` because the job already deleted itself: confirm with `cron.list`. |
| The agent doesn't use the skill unless you give it the path | The frontmatter `description` is vague ("skill de soporte", support skill) and doesn't match the question. | Rewrite the `description`: what it does, who it's for, and the words a student would use to ask. Reinstall with `skill install` (it replaces the one with the same name) and test in a **new** session. |
| `skill install` fails because of the `SKILL.md` | The frontmatter is missing, `name` is missing, or the name has characters that aren't allowed. | YAML frontmatter between `---` with `name` (only letters, numbers, dots, hyphens, and underscores) and `description`. Files that start with `.` are skipped. |
| The skill answers "No encuentro la FAQ del curso en el workspace" ("I can't find the course FAQ in the workspace") | You didn't copy the FAQ, or it ended up in `faq/faq/`. | `nemoclaw my-assistant exec --workdir /sandbox/.openclaw/workspace -- ls -R faq` and fix it with `upload`. |

## Challenge

**Get the agent to discover the skill on its own.** Temporarily replace the `description` in your `SKILL.md` with `Skill de soporte.` (support skill), reinstall it, and ask the step 7 question in a new session. Then restore a good description (the original or a better one) and repeat.

Success criteria: with the vague description, the agent doesn't follow the skill's format; with the good one, in a new session and **without giving it the path**, it answers with **Categoría**, steps, and **Fuente:** `faq/…`. Write down both answers.

## Project milestone

**Soporte NemoClaw (NemoClaw Support) is now deployed on OpenClaw:**

- The `soporte-nemoclaw` skill installed, with the course FAQ in `faq/` inside the workspace.
- A scheduled job that leaves `reportes/resumen-faq-<id>.md` with no intervention.

Repeat the 4.1 baseline question ("My notebook returns HTTP 401") and compare. Save the new answer in `proyecto/linea-base-4.1.md`, below the previous one, and write down the difference: does it cite the FAQ now? Does it follow the categories from the class 3.1 router? In Module 5 you'll review the risks all this opened up: an agent with data, tools, and jobs that run on their own.

## Resources

- [Lesson 03c · The Always-On Agent (NVIDIA DLI)](https://nvdli.github.io/NemoClawDLI/nemoclaw/03c-always-on.html)
- [NemoClaw · Command reference: `skill install`, `skill list`, `skill remove`, `upload`](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands.md)
- [NemoClaw · Configure agent heartbeats](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/configure-agents/configure-agent-heartbeats.md)
- [OpenClaw · Automation: cron vs. heartbeat](https://docs.openclaw.ai/cron-vs-heartbeat)
- [Anthropic · Agent Skills](https://www.anthropic.com/news/skills) and [Voyager (arXiv 2305.16291)](https://arxiv.org/abs/2305.16291)
- `man 8 cron` for classic Unix cron (the idea is the same: a time and a command)
