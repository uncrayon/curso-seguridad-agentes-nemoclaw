# 5.2 · Identities and boundaries with OpenShell

> 🇪🇸 Original Spanish guide: [`clases/5.2-identidades-openshell/README.md`](../../../clases/5.2-identidades-openshell/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Prove with evidence who your agent is inside the sandbox, which binaries can reach the network, and where your API key is (and isn't).

| | |
|---|---|
| Video length | ≈9 min |
| Practice | Brev lab ([`cookbook.md` (Spanish)](../../../clases/5.2-identidades-openshell/cookbook.md)) |
| Skill | Configure agent identities in OpenShell |

Materials: [slides](slides.html) · [lab cookbook (Spanish)](../../../clases/5.2-identidades-openshell/cookbook.md) · [FAQ (Spanish)](../../../FAQ.md)

## What you'll achieve

- Show that the agent runs as the `sandbox` user, without root, with seccomp active and no way to escalate.
- Explain why OpenShell grants network permissions **per binary** (real path + hash) and why faking `argv[0]` doesn't work.
- Show that the real API key never enters the sandbox: inside, there's only a placeholder.

## Before you start

- Your NemoClaw lab on Brev is running and the class 4.1 check is green.
- You know how to get into the host with `brev shell <your-instance>` (class 4.1).
- Your sandbox is called `my-assistant` (or you wrote down the name that `openshell sandbox list` shows).
- You made your `trifecta.md` worksheet in class 5.1.

## Step by step

### 1. Three different identities

Before you type anything, be clear about who we're talking about:

| Identity | Who it is | What power it has |
|---|---|---|
| **The agent process** | The `sandbox` user inside the container | Whatever Landlock, seccomp and the network policy allow |
| **The binary** | The real path of the executable that opens the connection (`/usr/local/bin/openclaw`, `/usr/bin/curl`) | The destinations its policy group allows |
| **The operator** | You, in the host terminal, with `nemoclaw` and `openshell` | Change policies, approve egress, read the gateway token |

### 2. Who is the agent?

On the lab host:

```bash
openshell sandbox exec -n my-assistant -- whoami
openshell sandbox exec -n my-assistant -- id
openshell sandbox exec -n my-assistant -- pwd
```

You should see `sandbox`, a `uid` other than 0, and `/sandbox`. Then ask the agent the same thing:

```bash
nemoclaw my-assistant agent -m "Use your exec tool to run whoami and pwd, and tell me in one sentence which user you are and where you are."
```

Compare its answer with what you saw. As the operator, you **verify** what the agent says.

### 3. Read its authority in `/proc/self/status`

```bash
openshell sandbox exec -n my-assistant -- grep -E '^(Uid|Gid|NoNewPrivs|Seccomp|Seccomp_filters|CapEff|CapBnd)' /proc/self/status
```

You should see `NoNewPrivs: 1`, `Seccomp: 2` and `CapEff: 0000000000000000`: no new privileges, a seccomp filter, and no root capabilities. This test is safe: it only reads a file.

### 4. Try to escalate (and read the error carefully)

Run NVIDIA's tests from [recipe 3 (Spanish)](../../../clases/5.2-identidades-openshell/cookbook.md#3--pedir-más-autoridad-catálogo-de-nvidia-04a) and the seccomp tests from [recipe 4 (Spanish)](../../../clases/5.2-identidades-openshell/cookbook.md#4--seccomp-ptrace-mount-y-setuid-sin-romper-nada):

```bash
openshell sandbox exec -n my-assistant -- sudo id
openshell sandbox exec -n my-assistant -- python3 -c 'import os; os.setuid(0)'
```

You should see failures. Tell the messages apart:
- `command not found`: the tool doesn't exist in the image. It doesn't prove any boundary.
- `Permission denied` (`EACCES`): file permissions or Landlock.
- `Operation not permitted` (`EPERM`): the kernel denied the operation (missing capabilities or seccomp).

A failure on its own doesn't tell you which mechanism caused it. That's why step 3 reads the process state.

### 5. The network permission is tied to the binary

In the base policy, `docs.openclaw.ai` is only allowed for `/usr/local/bin/openclaw`. Test it with `curl`, then try to trick OpenShell:

```bash
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://docs.openclaw.ai
openshell sandbox exec -n my-assistant -- bash -c 'exec -a /usr/local/bin/openclaw curl -sS -m 8 -o /dev/null -w "code=%{http_code}\n" https://docs.openclaw.ai'
```

You should see `curl: (56) CONNECT tunnel failed, response 403` twice. OpenShell identifies the binary through `/proc/<pid>/exe` (the path the kernel guarantees), walks up the parent processes, and stores a SHA256 hash of each binary the first time it sees it (*trust-on-first-use*). `argv[0]` can be faked, so it doesn't count. The "copy curl as openclaw" and "replace the binary" variants are in [recipe 5 (Spanish)](../../../clases/5.2-identidades-openshell/cookbook.md#5--permisos-por-binario-el-host-está-permitido-el-binario-no).

Then ask the agent, which does use the allowed binary:

```bash
nemoclaw my-assistant agent -m "Open https://docs.openclaw.ai and tell me in one line what the page is about."
```

### 6. Look for your API key inside the sandbox

```bash
openshell sandbox exec -n my-assistant -- sh -c 'env | grep -iE "key|token" | sed -E "s/=(openshell:resolve:env:).*/=\1…/; t; s/=.*/=<oculto>/"'
openshell sandbox exec -n my-assistant -- sh -c 'grep -rIl "nvapi-" /sandbox 2>/dev/null | wc -l'
```

You should see something like `NVIDIA_INFERENCE_API_KEY=openshell:resolve:env:…` and a `0`. (Any other value is masked as `<oculto>`, "hidden".) The real key lives in the OpenShell gateway, on the host. The L7 proxy swaps the placeholder for the key **only** when the request goes out through the allowed route. If the agent prints that variable or sends it somewhere else, what leaks is worthless text.

On the host, check where the real key lives (values are never shown):

```bash
nemoclaw credentials list
```

### 7. The same thing, from NVIDIA's 04a page

If you prefer the browser, open [lesson 04a](https://nvdli.github.io/NemoClawDLI/nemoclaw/04a-safety.html) with your launchable connected and follow [recipe 7 (Spanish)](../../../clases/5.2-identidades-openshell/cookbook.md#7--en-la-página-04a-de-nvidia): add `["Who am I?", ["whoami", "id", "pwd"]]` to the "ask the box anything, in code" cell and change the binary in the policy map.

## Check that it worked

- [ ] `whoami` says `sandbox` and `id` shows a `uid` other than 0.
- [ ] `/proc/self/status` shows `NoNewPrivs: 1` and `Seccomp: 2`.
- [ ] `sudo id` and `os.setuid(0)` fail, and you know what each message means.
- [ ] `curl` to `docs.openclaw.ai` returns 403 even when you fake `argv[0]`.
- [ ] There's no `nvapi-` anywhere inside the sandbox: only an `openshell:resolve:env:…` placeholder.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `curl: (56) CONNECT tunnel failed, response 403` | The policy denied the connection (host or binary not allowed). That's expected in step 5 | It's not a TLS problem. Check `nemoclaw my-assistant logs --tail 30` to see the binary and the reason |
| `nemoclaw: recent network policy denial detected for docs.openclaw.ai:443 …` | An informational hint from `nemoclaw … exec` after a denial | Read it and move on. Silence it with `NEMOCLAW_NO_POLICY_HINT=1` |
| `whoami` says `root` | You used `docker exec` on the container (it runs as root, `HOME=/root`) | Use `openshell sandbox exec -n …` or `nemoclaw my-assistant exec -- …` |
| A command with a pipe (`grep … \| wc`) runs on the host | `openshell sandbox exec` takes arguments, not a shell line | Wrap the whole command in `-- sh -c '…'` |
| No `…KEY` variable shows up in step 6 | Sandbox created before NemoClaw v0.0.132: it uses the `inference.local` route and doesn't even get the placeholder | That's normal. The key isn't inside either |
| The 04a page says "Keep your launchable open in another tab, then re-run. Check the sandbox name with: openshell sandbox list" | The page lost its session with your launchable | Reopen the launchable, reconnect in 03a and run 🩺 Health check |
| `python3: command not found` | The image changed | Use the cell on the 04a page or skip recipe 4 |

## Challenge

Find **one host your policy allows for `curl`** and another that it only allows for `openclaw`, using only read commands (`openshell policy get my-assistant --full` helps; you'll go deep on it in 5.3). Success criterion: two `curl` commands from the sandbox, one with `code=200` (or whatever code the server returns) and one with `CONNECT tunnel failed, response 403`, plus one sentence that explains the difference.

## Project milestone

Add an **"Identity"** section to your *Soporte NemoClaw* (NemoClaw Support) `trifecta.md` with what you verified:

```markdown
## Identity (class 5.2)
- Runs as: sandbox (uid …), NoNewPrivs 1, Seccomp 2
- Binaries that reach the network: /usr/local/bin/openclaw, /usr/local/bin/node
- Where the API key lives: OpenShell gateway (host). In the sandbox: openshell:resolve:env:…
- Remaining risk: the OpenClaw gateway token is readable inside the sandbox
```

In class 5.3 you'll read the full policy and write the project's preset.

## Resources

- NVIDIA DLI · [04a · The OpenShell Sandbox](https://nvdli.github.io/NemoClawDLI/nemoclaw/04a-safety.html) (Apache-2.0).
- NemoClaw · [Security Best Practices](https://docs.nvidia.com/nemoclaw/latest/) → "Binary-Scoped Endpoint Rules" (identification through `/proc/<pid>/exe` and a SHA256 hash).
- NemoClaw · Credential Storage (`docs/security/credential-storage.mdx`): `openshell:resolve:env:<KEY>` placeholders.
- NemoClaw · Process Controls (`docs/security/process-controls.mdx`): `no-new-privileges`, capabilities, `ulimit -u 512`.
- Linux kernel · [seccomp filter](https://docs.kernel.org/userspace-api/seccomp_filter.html) · man7 · [capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html).
- [FAQ (Spanish)](../../../FAQ.md).

---
Based on the 04a-safety lesson of the NVIDIA DLI course (Apache-2.0).
