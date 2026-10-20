## Don't ask "is it safe?"

.lead Ask: what exactly can it reach, and have I tested it?

:::diagrama c53-ciclo

Notes:
This is the flow of the whole class. The cycle lights up on its own; one click per step in the list: read the real policy, predict, test in the sandbox, compare and, if it doesn't match, investigate.

---

## The real policy

:::diagrama c53-reglamento

Notes:
On the dashboard: OPENSHELL TUI → my-assistant → Enter (folders and network rules); in the VM TERMINAL: openshell policy get my-assistant --full. One click per section, with its technical name on the right: filesystem_policy (include_workdir, read_only, read_write), landlock (compatibility: best_effort), process (run_as_user: sandbox) and network_policies (in the lab, 13 groups: nvidia, managed_inference, native_nvidia_inference, clawhub, openclaw_docs, pypi…). Click 5: seccomp isn't listed because OpenShell always applies it. Save it before changing anything.

---

## A network group

:::diagrama c53-grupo

Notes:
Click 1: a request from openclaw arrives. Click 2: the openclaw_docs group and its five details (host docs.openclaw.ai, port 443, method GET, path /**, binaries /usr/local/bin/openclaw). Click 3: they all match, it goes through. Click 4: if one is missing, it's denied. protocol: rest turns on L7 inspection: the proxy checks every request, not just the host. Recall 5.2: in the lab, when the agent asked for docs.openclaw.ai it went out through curl and through node, and this group denied both.

---

## Files: what it reads and where it writes

:::diagrama c53-archivos

Notes:
One click per group: read only (/usr, /etc, /proc), read-write (/tmp, /sandbox, /sandbox/.openclaw), not even read (/var/lib/apt, /root). The rule with the longest prefix wins. In the lab: ls /var/lib/dpkg works; ls /var/lib/apt/lists gives Permission denied (readable by any Linux user; Landlock denies it); touch in /usr and /etc, Permission denied; /tmp is writable. Click 4: SOUL.md lives in /sandbox/.openclaw and the policy doesn't protect the persona.

---

## Predict, then test

:::diagrama c53-predice

Notes:
Click 1: the five requests appear with a "?": ask students for their prediction. Clicks 2 to 6, one verdict per click: inference.local gets through the proxy (code=503: the internal route answers, the lab doesn't use it); example.com gets CONNECT tunnel failed, 403 from the proxy; integrate.api.nvidia.com with curl GOES THROUGH (code=200): NVIDIA's native inference profile opens it, even though the notebook (base policy) says DENY. It's a real finding, not a failure; /var/lib/apt gives Permission denied; writing SOUL.md is allowed (the other surprise). Notebook: 12 scored actions. Lab: recipes 3 and 4. A match only backs that one action.

---

## Read a block

:::diagrama c53-bloqueo

Notes:
Click 1: curl to example.com and the proxy answers curl: (56) CONNECT tunnel failed, response 403. Click 2: with nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4. Click 3: OPENSHELL TUI → my-assistant → Enter → r (Rules) → select → x rejects, a approves. Click 4: approving there is temporary, it applies to that sandbox; for something lasting, a preset. Two kinds of block: policy_denied (didn't match, approve it?) and upstream_unreachable (matched, the host didn't answer). A 403 can come from the proxy or the server: CONNECT tunnel failed is from the proxy.

---

## Changing the policy

:::diagrama c53-preset

Notes:
Click 1: a preset from the list (github, one of the many that policy list shows) is stapled to the rulebook. One click per action: --dry-run (dry run), --yes (applies live), policy remove … --yes (removes). Click 4: a preset is tied to programs too: the github one names git, not curl. Click 5: network and inference change live; files, Landlock and process need the sandbox recreated. In the video the full cycle is done with soporte-docs (next slide); github stays as optional recipe 7c. OPENSHELL TUI approvals are temporary; to make them persist, use a preset.

---

## The Soporte NemoClaw preset

:::diagrama c53-preset-soporte

Notes:
One click per rule: method GET; host docs.nvidia.com, port 443, protocol rest, path /nemoclaw/**; binaries /usr/local/bin/openclaw and /usr/local/bin/node (the agent reaches the network through node). We validate it in the notebook with validar_preset(). In the lab: --dry-run prints the policy, the "custom preset targets are not vetted" warning and "not applied"; --yes → "Applied preset: soporte-docs"; policy list marks it [user-added]; the agent answered in two lines with no denials; policy remove soporte-docs --yes → "Removed preset: soporte-docs".

---

## The sandbox is one layer

:::diagrama c53-una-capa

Notes:
Click 1: the 5.1 attack steps against this policy, each with its "?". Clicks 2 to 5: reading the poisoned FAQ, allowed; reading MEMORY.md, allowed; curl to the attacker's host, blocked; node → clawhub.ai with POST, allowed. Click 6: a secret printed by an allowed command has already escaped. And another real channel from the lab: curl reaches integrate.api.nvidia.com. An allow list approves the destination, not the meaning of the bytes. Above: provenance, human approval, secrets outside the sandbox.

---

## If you prefer the terminal

```bash
openshell policy get my-assistant --full > ~/politica-antes.txt   # save the policy
nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4   # recent blocks
nemoclaw my-assistant policy list                                # active and available presets
nemoclaw my-assistant policy add --from-file ~/soporte-docs.yaml --dry-run   # dry run
nemoclaw my-assistant policy add --from-file ~/soporte-docs.yaml --yes       # applies live
nemoclaw my-assistant policy remove soporte-docs --yes           # back to how it was
```

.lead Paste them in the dashboard's VM TERMINAL. The OPENSHELL TUI shows the policy and the pending requests with keys.

Notes:
The operator way: the dashboard's VM TERMINAL (user ubuntu). In the OPENSHELL TUI: r (Rules), select, x rejects. Don't approve example.com: always use x. Never d in the sandbox view.

---

## Common errors

| Symptom | Cause |
|---|---|
| `CONNECT tunnel failed, response 403` | Policy: host or program |
| `code=403` without CONNECT | The server answered |
| Preset applied, still blocked | Wrong program in the preset |
| The approval "disappeared" | The sandbox was recreated |
| curl → NVIDIA API returns 200 | NVIDIA native profile |

Notes:
The full table is on the class page.
