## Who is acting?

:::diagrama c52-quien

Notes:
Three answers, three levels of power. Click 1: the user the agent runs as (sandbox, no root). Click 2: each program that opens a connection (/usr/local/bin/openclaw, /usr/bin/curl…), with its own permissions. Click 3: you, the operator, on the host with nemoclaw and openshell. Click 4: least privilege, the key to its office and not the master key. If the answer were "root with a token that can do anything", no policy below would save you.

---

## Asking for more authority

:::diagrama c52-pedir-mas

Notes:
This is the "What happens when these commands ask for more permissions?" block on the 04a page. The tests: sudo id, nsenter -t 1 -m -- id, docker ps, and with Python os.setuid(0), ptrace and mount. One click per message: command not found (not there, proves nothing), Permission denied (files / Landlock), Operation not permitted (kernel / seccomp). Click 4: an EPERM doesn't tell you whether it was seccomp or missing capabilities. The seccomp tests use Python with ctypes, have no side effects and are in recipe 4.

---

## The network permission is tied to the program

:::diagrama c52-por-programa

Notes:
This is the map on the 04a page with the "calling binary" selector. Click 1: openclaw gets through to docs.openclaw.ai. Click 2: curl, to the same destination, gets CONNECT tunnel failed, response 403. Click 3: same destination, another program, another answer. In the base policy, openclaw_docs only lists /usr/local/bin/openclaw.

---

## Ask the sandbox

:::diagrama c52-verifica

Notes:
Click 1: first the operator asks the system (openshell sandbox exec … whoami, id, pwd): sandbox, uid other than 0, /sandbox. Click 2: then you ask the agent with nemoclaw my-assistant agent -m. Click 3: if they don't match, the terminal wins. The commands are on the "If you prefer the terminal" slide.

---

## Its authority, in one file

:::diagrama c52-ficha

Notes:
grep -E '^(NoNewPrivs|Seccomp|CapEff)' /proc/self/status inside the sandbox. A safe test: it only reads. One click per line: NoNewPrivs 1 (no escalation via setuid), Seccomp 2 (syscall filter active), CapEff all zeros (no root capabilities). Values to confirm in the dry run.

---

## What if I trick OpenShell?

:::diagrama c52-enganar

Notes:
One click per trick: spoofing argv[0] (exec -a /usr/local/bin/openclaw curl …) → 403; copying the binary (cp curl /tmp/openclaw) → 403; replacing the real one → /usr is read-only, EACCES. Click 4: OpenShell reads /proc/<pid>/exe, walks the parent processes and stores a SHA256 hash the first time (trust-on-first-use). If the binary changes while the sandbox runs, the hash doesn't match and the request is denied.

---

## Your API key isn't inside

:::diagrama c52-key-afuera

Notes:
Click 1: inside the sandbox the agent only has a placeholder: NVIDIA_INFERENCE_API_KEY=openshell:resolve:env:…. Click 2: the L7 proxy (the front desk) swaps it for the real key. Click 3: only on the allowed route to integrate.api.nvidia.com. Click 4: if the agent leaks that variable, it leaks worthless text. It removes the private-data leg for the key, not for everything: the OpenClaw gateway token is in the sandbox. Always use the filtered env from recipe 6.

---

## The operator sits above

:::diagrama c52-operador

Notes:
Click 1: your terminal changes policies and approves egress. Click 2: the gateway token (operator.admin) reads persona, cron and sessions. Click 3: egress rules don't see this authority. Click 4: least-scope, short-lived, rotated tokens. Cell "What can an operator.admin token see?" on the 04a page: reads only.

---

## If you prefer the terminal

```bash
openshell sandbox list                                      # the exact sandbox name
openshell sandbox exec -n my-assistant -- whoami            # sandbox
openshell sandbox exec -n my-assistant -- grep -E '^(NoNewPrivs|Seccomp|CapEff)' /proc/self/status
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://docs.openclaw.ai
nemoclaw credentials list                                   # the key lives outside
```

.lead It's optional: the same thing you saw on the NVIDIA page, written as instructions.

Notes:
The operator way, from the lab host with brev shell. Never unfiltered env, and never a pipe without sh -c '…': it would run on the host. The long commands (exec -a, filtered env, seccomp) are in the cookbook.

---

## Common errors

| Symptom | Cause |
|---|---|
| `whoami` → `root` | You used `docker exec` |
| The pipe runs on the host | Missing `sh -c '…'` |
| No `…KEY` variable | Sandbox older than v0.0.132 |
| "recent network policy denial detected" | Informational hint |

Notes:
The full table is on the class page.
