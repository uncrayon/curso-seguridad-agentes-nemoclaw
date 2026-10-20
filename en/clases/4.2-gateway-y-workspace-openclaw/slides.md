## The three pieces of OpenClaw

:::diagrama c42-edificio

Notes:
The office building. Click 1: you write. Click 2: the front desk (gateway) takes every turn and keeps the conversations. Click 3: the locked room with the assistant inside. Click 4: its desk (workspace). Click 5: the idea of the class, the directory is the configuration. There are two gateways: OpenShell's on the host (8080, local only, sandbox lifecycle) and OpenClaw's inside the sandbox (18789, the agent). Today we talk about OpenClaw's.

---

## The workspace, file by file

:::diagrama c42-escritorio

Notes:
Click 1: SOUL.md, the rulebook and the job description. Click 2: AGENTS.md, USER.md and TOOLS.md. Click 3: HEARTBEAT.md and the skills folder (class 4.3). Click 4: two-tier memory, memory/ and MEMORY.md. Click 5: it rereads it at the start of every conversation. IDENTITY.md (name, emoji) and POLICY.md (policy summary, written by NemoClaw) are there too. MEMORY.md and memory/ are created the first time the agent saves memory.

---

## Two-tier memory

:::diagrama c42-memoria

Notes:
Click 1: the conversation lives at the front desk and is lost when the session resets (sessions.reset). Click 2: the files, daily notes in memory/YYYY-MM-DD.md. Click 3: what matters goes into MEMORY.md. Click 4: the files survive the restart. By default MEMORY.md goes into the main session's context, not every session's; not being in context doesn't stop the agent from reading it. Inspired by MemGPT.

---

## Two planes of authority

:::diagrama c42-planos

Notes:
Click 1: the room, with the agent inside (user sandbox, narrower policy); it can only tell you what it did. Click 2: the operator, outside, at the machine's terminal. Click 3: the operator reads the files directly (openshell sandbox connect, nemoclaw … exec, cat). Click 4: the rule. This separation is the foundation of Module 5: an agent that rewrites its own workspace can influence its future runs.

---

## Verify as the operator

:::diagrama c42-dice-vs-archivo

Notes:
Click 1: what the agent says about itself (Step 1 in 03b). Click 2: what the operator cell shows (Step 1b, "Read the live workspace over the operator terminal"). Click 3: compare. The example is on purpose: the agent mentions MEMORY.md, which doesn't exist yet, and forgets USER.md. The commands are on the "If you prefer the terminal" slide.

---

## The agent edits its memory

:::diagrama c42-dos-sesiones

Notes:
In 03b: the "Verify file memory across separate sessions" flow, ▶ Run all. Click 1: conversation A asks to append a preference to MEMORY.md without deleting anything. Click 2: the cell doesn't trust it and reads the file. Click 3: a new conversation finds it on disk. Click 4: the rule. The cell fails if reading the file back doesn't contain the preference.

---

## Customize SOUL.md

:::diagrama c42-soul

Notes:
Click 1: the "Project: Soporte NemoClaw" section, written in plain language (it's the no-code activity). Click 2: it's appended to SOUL.md, on the desk. Click 3: in a new conversation, the agent knows its job. Click 4: the workspace is read at the start of each conversation; one that's already open doesn't change.

---

## Watch out for the tilde

:::diagrama c42-tilde

Notes:
The live error. Click 1: you ask the agent to append the section to ~/SOUL.md. Click 2: inside the room, ~ is /sandbox: it writes a stray file nobody reads. Click 3: with the full path (/sandbox/.openclaw/workspace/SOUL.md) it reaches the real rulebook. Click 4: always ask for the full path and verify as the operator with tail. Delete the stray file with the operator cell (rm ~/SOUL.md).

---

## If you prefer the terminal

```bash
# Look at the agent's desk, as the operator
openshell sandbox connect my-assistant
cd /sandbox/.openclaw/workspace && ls -la

# Append your section to SOUL.md without relying on the agent
nemoclaw my-assistant download /sandbox/.openclaw/workspace/SOUL.md ./
cp SOUL.md SOUL.md.original
cat >> SOUL.md <<'EOF'
## Project: Soporte NemoClaw
- You answer in plain English …
EOF
nemoclaw my-assistant upload ./SOUL.md /sandbox/.openclaw/workspace/SOUL.md
```

.lead It's optional: the same thing you did with clicks and in the chat, written as instructions.

Notes:
Cookbook recipe 7 (download → cp … .original → cat >> → upload → tail). To find the saved preference: nemoclaw my-assistant exec -- grep -n "REF-" /sandbox/.openclaw/workspace/MEMORY.md (recipe 8). Test it in a new conversation.

---

## Common errors

| You see | Do this |
|---|---|
| The agent says "I saved it" and it isn't there | Read it as the operator and ask for the full path |
| You edited `~/SOUL.md` and nothing changed | Use the desk: `/sandbox/.openclaw/workspace/` |
| An open conversation doesn't change | Start a new conversation |
| `Pairing required` on the dashboard | Wait and reload; the steps are on the class page |
| `openclaw update` hangs | Don't use it: the version is pinned |

Notes:
Pairing: Overview → Gateway Access → Connect, or openclaw devices approve (recipe 9). In your own install, updating is nemoclaw update and then nemoclaw <name> rebuild. In the launchable, don't touch versions.

---

## Project progress

.lead Your agent is now Soporte NemoClaw.

- In `SOUL.md`: who it helps, what language it answers in and what it never does
- In `MEMORY.md`: a preference, checked in the file
- Repeat the 401 question from class 4.1 and write down what changed

It still lacks knowledge: in class 4.3 the skill with the FAQ arrives.

Notes:
Save the section in proyecto/SOUL-soporte.md. The project's memory preference is soporte-pref-01: cite the FAQ file.
