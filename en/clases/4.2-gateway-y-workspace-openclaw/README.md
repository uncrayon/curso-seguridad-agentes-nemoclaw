# 4.2 · Explore the OpenClaw gateway and workspace

> 🇪🇸 Original Spanish guide: [`clases/4.2-gateway-y-workspace-openclaw/README.md`](../../../clases/4.2-gateway-y-workspace-openclaw/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Open the folder that defines your agent, compare what the agent says about itself with what's on disk, and customize it for the Soporte NemoClaw (NemoClaw Support) project.

| | |
|---|---|
| Video length | ≈8 min |
| Practice | Lab on Brev: NVIDIA course page + terminal ([cookbook.md (Spanish)](../../../clases/4.2-gateway-y-workspace-openclaw/cookbook.md)) |
| Skill | Orientation (no assessed skill) |

Materials: [slides](slides.html) · [terminal cookbook (Spanish)](../../../clases/4.2-gateway-y-workspace-openclaw/cookbook.md) · [FAQ (Spanish)](../../../FAQ.md)

> Based on lesson 03b-openclaw from the NVIDIA DLI course (Apache-2.0).

## What you'll achieve

- Name the pieces of OpenClaw (gateway, sessions, workspace) and which workspace file shapes each part of the behavior.
- Verify as the operator, with `cat`, what the agent claims about its files and its memory.
- Customize `SOUL.md` and `MEMORY.md` so your agent behaves like **Soporte NemoClaw**.

## Before you start

- Class 4.1 finished: instance in `RUNNING` and **Test connection** green in [lesson 03a](https://nvdli.github.io/NemoClawDLI/nemoclaw/03a-kickstart.html). The 03b page reuses that connection.
- For the terminal route: `brev shell <instancia>` working (4.1 cookbook, recipe 5).
- Your sandbox name (usually `my-assistant`; confirm it with `nemoclaw list`).

## The pieces, in one table

| Piece | Where it lives | What it does |
|---|---|---|
| OpenClaw gateway | Inside the sandbox; it reaches your machine on port 18789 | Receives every turn, runs the agent loop, serves the dashboard and the WebSocket. |
| OpenShell gateway | On the host, port 8080 (local only) | Manages the sandbox lifecycle, the inference routes, and the ports. |
| Sessions | In the OpenClaw gateway | The history of each conversation, identified by its key (`sessionKey`). |
| Workspace | `/sandbox/.openclaw/workspace/` | Markdown files the agent reads **at the start of every session**. They are its configuration. |

The workspace, file by file:

| File | What it defines |
|---|---|
| `SOUL.md` | Personality, boundaries, tone, and values. |
| `AGENTS.md` | Operating instructions and rules: memory, safety, the flow of each session. |
| `IDENTITY.md` | A short card: name, language, emoji. |
| `USER.md` | Who the person it helps is, and their preferences. Starts empty. |
| `TOOLS.md` | Usage notes for each tool. |
| `HEARTBEAT.md` | A list of periodic tasks (we cover it in 4.3). |
| `POLICY.md` | A summary of the network policy, written by NemoClaw. |
| `memory/` | Daily `AAAA-MM-DD.md` (YYYY-MM-DD) notes the agent appends as it works. Created the first time the agent saves a note. |
| `MEMORY.md` | Curated long-term memory. Loaded in the main session. Created the first time the agent uses it. |
| `skills/` | One folder per skill, with its `SKILL.md` (we cover it in 4.3). |

One detail causes a lot of errors: inside the sandbox, `~` is `/sandbox`, **not** the workspace. `~/SOUL.md` points to `/sandbox/SOUL.md`, which the agent doesn't read as its personality. Always use the full path `/sandbox/.openclaw/workspace/SOUL.md`.

## Step by step

### Part A · Ask the agent to describe itself (course page)

1. **Open the lesson** [The OpenClaw Agent](https://nvdli.github.io/NemoClawDLI/nemoclaw/03b-openclaw.html). Check that the pill at the top says **OpenClaw ✓**. If it says **OpenClaw ⚠**, go back to 03a, copy a new cookie, and repeat **Test connection**.

2. **Run Step 1 · Ask the agent to describe itself.** In the **Ask OpenClaw to describe its workspace** cell, click **▶ Run**. The message it sends is:
   > Briefly list the files in your workspace and explain each in one bullet without dumping file contents.

   The message is already in English. If you want to try another language, open the code and change the `content:` text. For example, the Spanish version is:
   ```js
   content: "Enumera brevemente los archivos de tu workspace y explica cada uno en una viñeta, sin volcar su contenido.",
   ```
   You should see: a list of files with one explanation per bullet. **Write it down**: this is what the agent *says*.

### Part B · Verify as the operator

3. **Run Step 1b · Read the workspace yourself.** The **Read the live workspace over the operator terminal** cell opens an operator terminal (over WebSocket) and enters the sandbox with `openshell sandbox connect <nombre>`. It gets the name from `GET /api/agent`. It runs these commands:
   ```js
   const commands = [
     "ls .openclaw/workspace",
     "echo '=== SOUL.md ==='; cat .openclaw/workspace/SOUL.md",
     "echo '=== daily memory ==='; ls -1 .openclaw/workspace/memory/ 2>/dev/null",
     "echo '=== MEMORY.md ==='; cat .openclaw/workspace/MEMORY.md 2>/dev/null || echo '(no curated MEMORY.md yet; the agent writes it in a main session)'",
   ];
   ```
   You can edit the list. For example, add `"cat .openclaw/workspace/AGENTS.md"` or `"ls -la .openclaw/workspace/skills"`.

   You should see: the real list of files and the contents of `SOUL.md`. It's normal for `MEMORY.md` and `memory/` not to exist yet.

4. **Compare.** Did the agent mention a file that doesn't exist? Did it forget one? That gap is the point of this class: **what the agent says is not evidence; the file is**.

   Why it works this way: the launchable has two planes of authority. The operator terminal runs **outside** the sandbox. The agent runs **inside**, under a narrower policy.

5. **(Terminal route)** The same thing from `brev shell <instancia>`:
   ```bash
   openshell sandbox list
   openshell sandbox connect my-assistant       # or: nemoclaw my-assistant connect
   ```
   Once inside the sandbox:
   ```bash
   whoami; pwd
   cd /sandbox/.openclaw/workspace
   ls -la
   cat SOUL.md
   cat AGENTS.md
   exit
   ```
   Details in the [cookbook (Spanish)](../../../clases/4.2-gateway-y-workspace-openclaw/cookbook.md), recipes 1 to 4.

### Part C · The agent edits its own memory

6. **Run Step 3 · The agent edits its own context.** In the **Verify file memory across separate sessions** flow, click **▶ Run all**:
   - **Save and verify a preference:** in a new session, it asks the agent "Append this preference to MEMORY.md without replacing existing content: …" with a `course-review-…` label and a `REF-…` reference. Then it **reads the file** and fails if the preference isn't there.
   - **Read from a fresh conversation:** it opens another session and asks the agent to read `MEMORY.md` and report the reference.

   You should see: `Verified the appended note on disk. It remains in MEMORY.md for inspection.` and the reference recovered in the second session.

   The agent saying "saved" isn't enough. The cell checks by reading the file.

7. **Do it with your own preference.** In the **Try it · chat with your live agent** part of the same page, type:
   > Append this line to the end of /sandbox/.openclaw/workspace/MEMORY.md without deleting anything: "soporte-pref-01: answer in plain English and cite the FAQ file you used. Reference REF-4821."

   Verify with the operator cell (add `"tail -n 5 .openclaw/workspace/MEMORY.md"` to `commands`) and then, in a new conversation, ask:
   > Read MEMORY.md and report the preference and the reference for soporte-pref-01.

   You should see: `REF-4821` in the file and in the answer from the new session.

### Part D · Customize SOUL.md for Soporte NemoClaw

8. **Back up and edit as the operator.** From `brev shell <instancia>`:
   ```bash
   mkdir -p ~/soporte && cd ~/soporte
   nemoclaw my-assistant download /sandbox/.openclaw/workspace/SOUL.md ./
   cp SOUL.md SOUL.md.original
   cat >> SOUL.md <<'EOF'

   ## Project: Soporte NemoClaw
   - You help students of the course "Securing Agents with OpenShell and NemoClaw".
   - You answer in plain English, with short sentences and numbered steps.
   - Before answering, you classify the question into one category: instalacion, api_key, brev, seguridad, or otro.
   - If you use the course FAQ, you cite the file the answer comes from.
   - You never ask for, repeat, or store API keys, tokens, or cookies. If someone pastes one, you ask them to revoke it.
   - If you don't know something, you say so and suggest opening an issue or asking in the course forum.
   EOF
   nemoclaw my-assistant upload ./SOUL.md /sandbox/.openclaw/workspace/SOUL.md
   nemoclaw my-assistant exec -- tail -n 9 /sandbox/.openclaw/workspace/SOUL.md
   ```
   You should see: the last lines with the "Project: Soporte NemoClaw" section.

9. **Check the change in a new session.** The agent reads the workspace at the start of every session, so ask it in a new conversation (in **Try it · chat with your live agent** or with cookbook recipe 7):
   > Who are you, who do you help, and what do you never do?

   You should see: it mentions the course, plain English, and that it never asks for API keys.

   If you want to go back to the original: `nemoclaw my-assistant upload ./SOUL.md.original /sandbox/.openclaw/workspace/SOUL.md`.

## Check that it worked

- [ ] You wrote down the list of files the agent gave you and the real `ls` list, and you know whether they match.
- [ ] You read `SOUL.md` and `AGENTS.md` as the operator.
- [ ] The **Verify file memory across separate sessions** flow finished green.
- [ ] `REF-4821` is in `MEMORY.md`, and a new session recovers it.
- [ ] `SOUL.md` has the "Project: Soporte NemoClaw" section, and a new session reflects it.
- [ ] You have `SOUL.md.original` as a backup.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| The agent says "done, I saved it" but the file didn't change | The model reports an action it didn't take, or it wrote to another path. | Always verify with `cat` as the operator. Ask again with the full path and have it read the file back. |
| You edited `~/SOUL.md` and the agent didn't change | `~` is `/sandbox`, not the workspace. You wrote `/sandbox/SOUL.md`. | Use `/sandbox/.openclaw/workspace/SOUL.md` (or `$OPENCLAW_WORKSPACE_DIR/SOUL.md`). Delete the stray file. |
| You changed `SOUL.md` and the open conversation stays the same | The workspace is read at the start of each session. | Open a new session to test. |
| `MEMORY.md` or `memory/` doesn't exist | The agent hasn't saved any memory yet. | That's normal. They're created the first time the agent saves something. |
| `Pairing required` / `Device pairing required` in the dashboard | OpenClaw requires pairing the device (since OpenClaw 2026.9.1 it can't be skipped). | Wait a few minutes and reload, or **Overview → Gateway Access → Connect**. If it persists: cookbook recipe 9 (`openclaw devices list --json` and `openclaw devices approve <requestId>`). |
| `gateway connect failed: GatewayClientRequestError: scope upgrade pending approval (requestId: ...)` | A connection is asking for more permissions and waiting for approval. | Approve it the same way as pairing: cookbook recipe 9. |
| You ran `openclaw update` inside the sandbox and it hung | OpenClaw is pinned in the sandbox image. It isn't updated in place. | Don't do it. Cancel with `Ctrl+C`. In your own install, you update with `nemoclaw update` and then `nemoclaw <nombre> rebuild`; in the course launchable, don't touch versions. |
| `No valid connected sandbox name.` in the operator cell | The page didn't get the sandbox name from `/api/agent`. | Go back to 03a and repeat **Test connection**. |
| `File readback did not contain the saved preference` | The agent didn't write the line, or it replaced it somewhere else. | Check the turn's trace (`⚙️` rows). Run **Health check** and retry. |

## Challenge

**Make the agent prove what it saves.** Add this rule to the end of `AGENTS.md` (with the same download, edit, and upload method from step 8):

```text
- Every time you say you saved something to a file, read it back and quote the exact line that was written.
```

Success criteria: in a new session, you ask it to save a preference to `MEMORY.md`, its answer includes the line it read back, and `cat` as the operator confirms that line exists.

## Project milestone

Your agent now has the **Soporte NemoClaw** identity:

- `SOUL.md` with the project section (language, triage categories, the no-keys rule).
- `MEMORY.md` with the `soporte-pref-01` preference (cite the FAQ file).

Save `proyecto/SOUL-soporte.md` in your repo with the section you added, and repeat the 4.1 baseline question ("My notebook returns HTTP 401"). Write down in `proyecto/linea-base-4.1.md` what changed. It doesn't know the FAQ yet: that comes in 4.3 with the `soporte-nemoclaw` skill.

## Resources

- [Lesson 03b · The OpenClaw Agent (NVIDIA DLI)](https://nvdli.github.io/NemoClawDLI/nemoclaw/03b-openclaw.html)
- [NemoClaw · Sandbox state and workspace files](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/manage-sandboxes/workspace-files.md)
- [NemoClaw · Command reference](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands.md) (`connect`, `exec`, `agent`, `sessions`, `download`, `upload`)
- [NemoClaw · Troubleshooting](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/troubleshooting.md) (pairing, `openclaw update`)
- [MemGPT: tiered memory for LLMs (arXiv 2310.08560)](https://arxiv.org/abs/2310.08560)
