## Who is acting?

:::diagrama c52-quien

Notes:
Three answers, three levels of power. Click 1: the user the agent runs as (sandbox, no root). Click 2: each program that opens a connection (/usr/local/bin/openclaw, /usr/bin/curl…), with its own permissions. Click 3: you, the operator, on the host with nemoclaw and openshell. Click 4: least privilege, the key to its office and not the master key. If the answer were "root with a token that can do anything", no policy below would save you.

---

## Asking for more authority

:::diagrama c52-pedir-mas

Notes:
From the VM TERMINAL with openshell sandbox exec (recipes 3 and 4). In the lab: sudo id → command not found; os.setuid(0) → PermissionError [Errno 1] Operation not permitted; touch /usr/local/bin/… → Permission denied. One click per message: command not found (not there, proves nothing), Permission denied (files / Landlock), Operation not permitted (kernel / seccomp). nsenter, docker ps and ptrace/mount are in the cookbook to classify with the same table. Click 4: an EPERM doesn't tell you whether it was seccomp or missing capabilities. The seccomp tests use Python with ctypes, have no side effects and are in recipe 4.

---

## The network permission is tied to the program

:::diagrama c52-por-programa

Notes:
The rule names programs, not "the agent". Click 1: the program the openclaw_docs rule lists gets through. Click 2: curl, to the same destination, gets CONNECT tunnel failed, response 403 (verified in the lab, exit 56). Click 3: same destination, another program, another answer. Mind what we saw in the lab: when the agent tried, it went out through curl and through node, and the guard denied both. The rules are visible in the OPENSHELL TUI (Enter on my-assistant).

---

## Ask the sandbox

:::diagrama c52-verifica

Notes:
Click 1: first the operator asks the system (SANDBOX TERMINAL, or openshell sandbox exec … id from the VM TERMINAL): sandbox, uid=998, /sandbox. Click 2: then you ask the agent in the chat. Click 3: if they don't match, the terminal wins. Real case from the lab: the agent said it was "gateway-owner"; the real user is sandbox. Compare with the VM TERMINAL: ubuntu, with sudo and docker.

---

## Its authority, in one file

:::diagrama c52-ficha

Notes:
grep -E '^(NoNewPrivs|Seccomp|CapEff)' /proc/self/status inside the sandbox. A safe test: it only reads. One click per line: NoNewPrivs 1 (no escalation via setuid), Seccomp 2 (syscall filter active), CapEff all zeros (no root capabilities). These are the values we saw in the lab.

---

## What if I trick OpenShell?

:::diagrama c52-enganar

Notes:
One click per trick, according to the NemoClaw docs: spoofing argv[0] (exec -a /usr/local/bin/openclaw curl …) doesn't change the real program; copying the binary (cp curl /tmp/openclaw) leaves a different path; replacing the real one isn't possible: touch in /usr/local/bin gives Permission denied (seen in the lab). Click 4: OpenShell reads /proc/<pid>/exe, walks the parent processes and stores a SHA256 hash the first time (trust-on-first-use). The first two tricks are in recipe 5 so students can try them and write down the result.

---

## An answer is not proof

```text
DENIED /usr/bin/curl(11932) -> docs.openclaw.ai:443
  reason: binary '/usr/bin/curl' not allowed in policy 'openclaw_docs'
  (ancestors: /usr/bin/bash -> /usr/local/bin/node -> /usr/bin/bash)
DENIED /usr/local/bin/node(11950) -> docs.openclaw.ai:443
  reason: binary '/usr/local/bin/node' not allowed in policy 'openclaw_docs'
```

.lead The agent answered anyway, from memory. What proves access is the log.

Notes:
What happened in the lab: we asked the agent to open docs.openclaw.ai. It tried curl and then node; the guard denied both. It still answered with a believable sentence about OpenClaw. Command: nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4. Read the line: who (binary and PID), its parent processes (ancestors: the agent runs on node), where to (host:port) and why (the openclaw_docs policy doesn't list that binary). The same request shows up pending in the OPENSHELL TUI, key r (Rules).

---

## Your API key isn't inside

:::diagrama c52-key-afuera

Notes:
Click 1: inside the sandbox the agent only has a placeholder: NVIDIA_INFERENCE_API_KEY=openshell:resolve:env:… (seen in the lab). Click 2: the L7 proxy (the front desk) swaps it for the real key. Click 3: only on the allowed route to NVIDIA. Click 4: if the agent leaks that variable, it leaks worthless text. It removes the private-data leg for the key, not for everything: the OpenClaw gateway token is in the sandbox (OPENCLAW_GATEWAY_TOKEN). Always use the filtered env from recipe 6.

---

## The operator sits above

:::diagrama c52-operador

Notes:
Click 1: your terminal changes policies and approves egress. Click 2: the gateway token (operator.admin) reads persona, cron and sessions. Click 3: egress rules don't see this authority. Click 4: least-scope, short-lived, rotated tokens. Remember: in the lab, the operator is ubuntu with sudo and docker.

---

## If you prefer the terminal

```bash
openshell sandbox list                                      # the exact sandbox name
openshell sandbox exec -n my-assistant -- whoami            # sandbox
openshell sandbox exec -n my-assistant -- grep -E '^(NoNewPrivs|Seccomp|CapEff)' /proc/self/status
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://docs.openclaw.ai
nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4   # who was denied and why
```

.lead Paste them in the dashboard's VM TERMINAL. The chat and the OPENSHELL TUI show the same with clicks.

Notes:
The operator way: the dashboard's VM TERMINAL (user ubuntu). Click the black area before typing. Never unfiltered env, and never a pipe without sh -c '…': it would run on the host. The long commands (filtered env, seccomp, exec -a) are in the cookbook.

---

## Common errors

| Symptom | Cause |
|---|---|
| `whoami` → `root` | You used `docker exec` |
| The pipe runs on the host | Missing `sh -c '…'` |
| No `…KEY` variable | Sandbox older than v0.0.132 |
| "recent network policy denial detected" | Informational hint |
| The agent "opened" the page | Check the log: it may be memory |

Notes:
The full table is on the class page.
