# 5.3 · Restrict tools, files and network

> 🇪🇸 Original Spanish guide: [`clases/5.3-sandbox-y-politicas/README.md`](../../../clases/5.3-sandbox-y-politicas/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Read your sandbox's real policy, predict what it allows and what it blocks, check it live, and change it with NemoClaw commands.

| | |
|---|---|
| Video length | ≈9 min |
| Practice | Brev lab ([`cookbook.md` (Spanish)](../../../clases/5.3-sandbox-y-politicas/cookbook.md)) + [notebook (Spanish)](../../../clases/5.3-sandbox-y-politicas/5.3-sandbox-y-politicas.ipynb) |
| Skill | Define and verify a sandbox in OpenShell |
| NVIDIA lesson | [04a · The OpenShell Sandbox](https://nvdli.github.io/NemoClawDLI/nemoclaw/04a-safety.html) (live policy, map and "Static verdict vs the live sandbox") |

Materials: [slides](slides.html) · [lab cookbook (Spanish)](../../../clases/5.3-sandbox-y-politicas/cookbook.md) · [notebook (Spanish)](../../../clases/5.3-sandbox-y-politicas/5.3-sandbox-y-politicas.ipynb) · [FAQ (Spanish)](../../../FAQ.md)

## What you'll achieve

- Read OpenShell's real YAML (`filesystem_policy`, `landlock`, `process`, `network_policies`) and explain each section.
- Predict and verify network and file blocks, and read a block in the log or in `openshell term`.
- Add and remove a preset on the fly, write the *Soporte NemoClaw* (NemoClaw Support) preset, and explain why the sandbox is only one layer.

## Before you start

- Brev lab running and healthy (`nemoclaw my-assistant status` is green).
- You did class 5.2: you know how to use `openshell sandbox exec -n my-assistant -- …`.
- You have your `trifecta.md` worksheet (5.1) with the "Identity" section (5.2).
- For the notebook: Python 3.10+ or Colab. It needs no API key and no extra PyPI packages: it uses PyYAML if you have it, and an equivalent dict if you don't.

## Step by step

### 1. Read the real policy

On the lab host:

```bash
openshell policy get my-assistant --full
```

You should see a status header, `---`, and the YAML. This is an excerpt of the OpenClaw base policy in NemoClaw (`nemoclaw-blueprint/policies/openclaw-sandbox.yaml`):

```yaml
filesystem_policy:
  include_workdir: true
  read_only: [/usr, /lib, /proc, /dev/urandom, /app, /etc, /var/log, /var/lib/dpkg]
  read_write: [/tmp, /dev/null, /dev/pts, /sandbox/.openclaw, /sandbox/.nemoclaw, /home/linuxbrew]
landlock:
  compatibility: best_effort
process:
  run_as_user: sandbox
  run_as_group: sandbox
network_policies:
  openclaw_docs:
    name: openclaw_docs
    endpoints:
      - host: docs.openclaw.ai
        port: 443
        protocol: rest          # the proxy inspects every HTTP request
        enforcement: enforce
        rules:
          - allow: { method: GET, path: "/**" }
    binaries:
      - { path: /usr/local/bin/openclaw }
```

Read it like this:
- **Network**: everything is closed except the groups under `network_policies`. Each group ties **destinations** (host, port, method, path) to **binaries**.
- **Files**: Landlock allows reading `read_only`, reading and writing `read_write` and `/sandbox`. Everything else is denied.
- **Process**: it runs as `sandbox`. seccomp doesn't appear in this YAML: OpenShell always applies it.

On the 04a page, the same thing is the **"Read your launchable's live policy"** cell (`helpers.policyGet()`), which also draws the map.

### 2. Practice in the notebook: predict → evaluate → score

Open [`5.3-sandbox-y-politicas.ipynb` (Spanish)](../../../clases/5.3-sandbox-y-politicas/5.3-sandbox-y-politicas.ipynb). It uses the real policy in OpenShell format and a Python evaluator (a simplified version of the one NVIDIA's page uses). Write your predictions for 12 actions and run it:

```text
✗ d curl → API de NVIDIA (binario equivocado)  predijiste ALLOW → DENY  | el binario '/usr/bin/curl' no está permitido en 'nvidia'
✗ i ESCRIBIR SOUL.md (la persona)              predijiste DENY  → ALLOW | … está bajo read_write /sandbox/.openclaw
Puntaje: 7/12
```

Row d: you predicted ALLOW for `curl` to the NVIDIA API, but it's DENY because `/usr/bin/curl` isn't allowed in the `nvidia` group. Row i: you predicted DENY for writing `SOUL.md` (the persona), but it's ALLOW because it sits under `read_write /sandbox/.openclaw`. `Puntaje` is your score.

The ✗ rows are the lesson: the permission is **tied to the binary**, L7 rules stop methods, and the policy does **not** protect `SOUL.md`.

### 3. Check it in the sandbox

The simulator predicts; the sandbox decides. Run recipes 3 and 4 from the [cookbook (Spanish)](../../../clases/5.3-sandbox-y-politicas/cookbook.md):

```bash
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://inference.local/v1/models
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://example.com
openshell sandbox exec -n my-assistant -- ls /var/lib/apt/lists
```

You should see: the first one without `CONNECT tunnel failed`; the second with `curl: (56) CONNECT tunnel failed, response 403`; the third with `Permission denied`.

If a prediction doesn't match, check three things before you draw conclusions: the **live** policy (not the notebook's), the real **binary**, and **who** answered (the proxy or the server?).

### 4. Read a block

```bash
nemoclaw my-assistant logs --tail 50
```

Look for the denial: binary, host:port and reason. To watch it live and decide, open `openshell term` in another terminal (recipe 6): `Enter` on your sandbox, `r` for **Network Rules**, `Enter` to see the details, `x` to reject.

### 5. Change the policy on the fly

```bash
nemoclaw my-assistant policy add github --dry-run
nemoclaw my-assistant policy add github --yes
openshell sandbox exec -n my-assistant -- sh -c 'git ls-remote https://github.com/NVIDIA/NemoClaw | head -1'
nemoclaw my-assistant policy remove github --yes
```

Network and inference change **on the fly**. Filesystem and process are fixed when the sandbox is created: to change them, you edit the base policy and recreate the sandbox.

### 6. The wrap-up: the sandbox is one layer

In the notebook (section 9), the poisoned FAQ from 5.1 attacks *Soporte NemoClaw* under the real policy: the `curl` to the attacker's host is blocked, but the send from the agent's runtime to `clawhub.ai` (an allowed host that accepts `POST`) **gets through**. Recipe 8 in the cookbook shows it live with a fake secret: a secret printed by an allowed command has already escaped.

## Check that it worked

- [ ] You saved your policy with `openshell policy get my-assistant --full > ~/politica-antes.txt`.
- [ ] You can point to where each of the four questions lives in the YAML (network, files, process; seccomp is separate).
- [ ] Your notebook score went up after reading the ✗ rows.
- [ ] You saw a live `CONNECT tunnel failed, response 403` and a `Permission denied`, and found them in the log.
- [ ] You added and removed the `github` preset without restarting anything.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `curl: (56) CONNECT tunnel failed, response 403` | The OpenShell proxy denied the connection: host outside the policy or binary not allowed | It's not TLS or DNS. Run `nemoclaw my-assistant logs --tail 50` and check the group with `openshell policy get my-assistant --full` |
| `code=403` **without** "CONNECT tunnel failed" | The connection went through and the server (or an L7 rule) answered | Identify the source before you blame the sandbox. Check the log |
| You added the preset and the agent is still blocked | The preset doesn't include the binary that actually opens the connection (e.g. `node`, not `openclaw`) | Copy the exact binary path from `openshell term` or the log into your preset |
| `DENIED /usr/local/bin/node -> registry.npmjs.org:443 reason: binary '/usr/local/bin/node' not allowed in policy 'npm_registry'` | The base `npm_registry` group only allows `openclaw` | If you really need it: `nemoclaw my-assistant policy add npm --dry-run`, review it and apply it |
| `ls /var/lib/apt/lists` works | Landlock in `best_effort` on a kernel without support (warning `⚠ Landlock: … does not support Landlock (requires ≥5.13)`) | Check `uname -r` inside the sandbox. Network and seccomp are still active |
| You see `upstream_unreachable` in `openshell term` | The policy matched, but the host didn't answer | Don't open the policy further: check the host, DNS or the corporate proxy |
| You added an endpoint with `openshell term` and it "disappeared" | Approvals only live in that sandbox instance; when you recreate it, the base policy comes back | To make it stick, use a preset (`policy add`) |
| The notebook says "Sin PyYAML" ("no PyYAML") | You don't have PyYAML installed | No problem: it uses the equivalent dict. Same content |

## Challenge

In the notebook (🏁 section), complete `PRESET_RETO` (challenge preset) so *Soporte NemoClaw* can read `docs.nvidia.com/nemoclaw/**` and the `build.nvidia.com` home page with `GET` only, without opening anything to `curl`. **Success criterion:** `probar_reto(PRESET_RETO)` (test the challenge) returns **6/6** and `nemoclaw my-assistant policy add --from-file … --dry-run` accepts it in the lab.

## Project milestone

Close the module with the *Soporte NemoClaw* policy:

1. Save `soporte-docs.yaml` (recipe 7e) next to the `soporte-nemoclaw` skill in your repo.
2. Add a **"Policy (class 5.3)"** section to your `trifecta.md`: which groups the project uses, which custom preset you added, and which output channel **is still open** (the inference provider and `clawhub.ai`).
3. Run `nemoclaw my-assistant policy explain --write` so the agent knows its policy and can explain to a student why it can't open a site.

In class 6.2 you'll package this as part of your skill library.

## Resources

- NVIDIA DLI · [04a · The OpenShell Sandbox](https://nvdli.github.io/NemoClawDLI/nemoclaw/04a-safety.html) (Apache-2.0).
- NemoClaw · base policy [`openclaw-sandbox.yaml`](https://github.com/NVIDIA/NemoClaw/blob/main/nemoclaw-blueprint/policies/openclaw-sandbox.yaml), [presets](https://github.com/NVIDIA/NemoClaw/tree/main/nemoclaw-blueprint/policies/presets) and [tiers](https://github.com/NVIDIA/NemoClaw/blob/main/nemoclaw-blueprint/policies/tiers.yaml).
- NemoClaw · [Command reference](https://docs.nvidia.com/nemoclaw/latest/) → `policy add`, `policy list`, `policy remove`, `policy explain`, `logs`.
- NemoClaw · *Approve or Deny Network Requests* (`openshell term`) and *Create Custom Policy Presets*.
- OpenShell · [Policy schema](https://docs.nvidia.com/openshell/latest/reference/policy-schema.html).
- [FAQ (Spanish)](../../../FAQ.md).

---
Based on the 04a-safety lesson of the NVIDIA DLI course (Apache-2.0) and on `nemoclaw-blueprint/policies/` from NVIDIA/NemoClaw (Apache-2.0).
