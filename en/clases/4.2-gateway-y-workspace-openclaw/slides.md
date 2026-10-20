## The three pieces of OpenClaw

:::diagrama c42-edificio

Notes:
The office building. Click 1: you write. Click 2: the front desk (gateway) takes every turn and keeps the conversations. Click 3: the locked room with the assistant inside. Click 4: its desk (workspace). Click 5: the idea of the class, the directory is the configuration. There are two gateways: OpenShell's on the host (port 18080, local only, sandbox lifecycle; you see it with openshell gateway info) and OpenClaw's inside the sandbox (18789, the agent and its chat). Today we talk about OpenClaw's.

---

## The workspace, file by file

:::diagrama c42-escritorio

Notes:
Click 1: SOUL.md, the rulebook and the job description. Click 2: AGENTS.md, USER.md and TOOLS.md. Click 3: HEARTBEAT.md and the skills folder (class 4.3). Click 4: two-tier memory, memory/ and MEMORY.md. Click 5: it rereads it at the start of every conversation. IDENTITY.md (name, emoji) and POLICY.md (policy summary, written by NemoClaw) are there too. In a fresh lab, MEMORY.md, memory/ and skills/ don't exist yet: they show up when they're needed.

---

## Two-tier memory

:::diagrama c42-memoria

Notes:
Click 1: the conversation lives at the front desk and is lost when the session resets (nemoclaw my-assistant sessions reset <key>). Click 2: the files, daily notes in memory/YYYY-MM-DD.md. Click 3: what matters goes into MEMORY.md. Click 4: the files survive the reset. Not being in context doesn't stop the agent from reading the file. Inspired by MemGPT.

---

## Two planes of authority

:::diagrama c42-planos

Notes:
Click 1: the room, with the agent inside (user sandbox, narrower policy); it can only tell you what it did. Click 2: the operator, outside, with the dashboard's VM TERMINAL. Click 3: the operator reads the files directly (nemoclaw my-assistant exec -- ls / cat). Click 4: the rule. This separation is the foundation of Module 5: an agent that rewrites its own workspace can influence its future runs.

---

## Verify as the operator

:::diagrama c42-dice-vs-archivo

Notes:
Click 1: what the agent says about itself, in CHAT WITH AGENT ("Briefly list the files in your workspace…"). Click 2: what the VM TERMINAL shows with nemoclaw my-assistant exec -- ls -la /sandbox/.openclaw/workspace. Click 3: compare. In a fresh lab the real list is AGENTS.md, HEARTBEAT.md, IDENTITY.md, POLICY.md, SOUL.md, TOOLS.md and USER.md; if the agent mentions MEMORY.md, it doesn't exist yet.

---

## The agent edits its memory

:::diagrama c42-dos-sesiones

Notes:
Click 1: the memoria-a session asks to append a preference (REF-4821) to MEMORY.md without deleting anything. Click 2: the operator doesn't trust it and searches for the line with grep in the VM TERMINAL. Click 3: after resetting memoria-a, a new session (memoria-b) finds it on disk. Click 4: the rule. Commands in Part E of the README and in cookbook recipe 8.

---

## Customize SOUL.md

:::diagrama c42-soul

Notes:
Click 1: the "Proyecto: Soporte NemoClaw" section, written in plain language (it's the no-code activity). Click 2: it's appended to the end of SOUL.md: you write it in ~/soul-extra.md on the machine, upload it to the sandbox's /tmp, and append it with sh -c 'cat … >> …'. Click 3: in a new session (soul-42), the agent knows its job. Click 4: the workspace is read at the start of each conversation; one that's already open doesn't change.

---

## Watch out for the tilde

:::diagrama c42-tilde

Notes:
The live error. Click 1: you append the section to ~/SOUL.md, inside the sandbox. Click 2: inside the room, ~ is /sandbox: you get a stray file nobody reads. Click 3: with the full path (/sandbox/.openclaw/workspace/SOUL.md) it reaches the real rulebook. Click 4: always use the full path and verify as the operator with tail. Delete the stray file: nemoclaw my-assistant exec -- rm /sandbox/SOUL.md.

---

## Operator commands

```bash
# Look at the agent's desk
nemoclaw my-assistant exec -- ls -la /sandbox/.openclaw/workspace

# Append your section to SOUL.md without relying on the agent
nemoclaw my-assistant upload ~/soul-extra.md /tmp/
nemoclaw my-assistant exec -- sh -c 'cat /tmp/soul-extra.md >> /sandbox/.openclaw/workspace/SOUL.md'

# Test it in a new session
nemoclaw my-assistant agent --session-key soul-42 -m 'Who are you?'
```

.lead You paste them in the dashboard's VM TERMINAL.

Notes:
Cookbook recipe 5: ~/soul-extra.md with cat > … <<'EOF', a backup in /tmp/SOUL.md.original, upload, cat >> and tail. Two signs >>: with just one, SOUL.md is wiped. To see sessions: sessions list --json (recipe 7).

---

## Common errors

| You see | Do this |
|---|---|
| The agent says "I saved it" and it isn't there | Read it as the operator and ask for the full path |
| You wrote `~/SOUL.md` and nothing changed | Use the desk: `/sandbox/.openclaw/workspace/` |
| An open conversation doesn't change | Use a new session |
| `SOUL.md` ended up with only your section | You used `>`: restore the copy and use `>>` |
| `openclaw update` hangs | Don't use it: the version is pinned |

Notes:
The lab's chat comes already paired: if "Pairing required" ever showed up, close the tab and open CHAT WITH AGENT again from the dashboard. In your own install, updating is nemoclaw update and then nemoclaw <name> rebuild. In the lab, don't touch versions.

---

## Project progress

.lead Your agent is now Soporte NemoClaw.

- In `SOUL.md`: who it helps, what language it answers in and what it never does
- In `MEMORY.md`: a preference, checked in the file
- Repeat the 401 question from class 4.1 and write down what changed

It still lacks knowledge: in class 4.3 the skill with the FAQ arrives.

Notes:
Copy the SOUL.md section into your project notes. The project's memory preference is soporte-pref-01: cite the FAQ file. Repeat the 401 question in a new session (linea-base-42).
