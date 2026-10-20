## Don't ask "is it safe?"

.lead Ask: what exactly can it reach, and have I tested it?

:::diagrama c53-ciclo

Notes:
This is the flow of the 04a page: Predict, Confirm, Compare. The cycle lights up on its own; one click per step in the list: read the real policy, predict, test in the sandbox, compare and, if it doesn't match, investigate.

---

## The real policy

:::diagrama c53-reglamento

Notes:
On the 04a page it's the "Read the launchable's active policy" cell; in the terminal, openshell policy get my-assistant --full. One click per section, with its technical name on the right: filesystem_policy (include_workdir, read_only, read_write), landlock (compatibility: best_effort), process (run_as_user: sandbox) and network_policies (nvidia, managed_inference, clawhub…). Click 5: seccomp isn't listed because OpenShell always applies it. Save it before changing anything.

---

## A network group

:::diagrama c53-grupo

Notes:
Click 1: a request from openclaw arrives. Click 2: the openclaw_docs group and its five details (host docs.openclaw.ai, port 443, method GET, path /**, binaries /usr/local/bin/openclaw). Click 3: they all match, it goes through. Click 4: if one is missing, it's denied. protocol: rest turns on L7 inspection: the proxy checks every request, not just the host.

---

## Files: what it reads and where it writes

:::diagrama c53-archivos

Notes:
One click per group: read only (/usr, /etc, /proc), read-write (/tmp, /sandbox, /sandbox/.openclaw), not even read (/var/lib/apt, /root). The rule with the longest prefix wins. /var/lib/apt is readable by any Linux user; Landlock denies it. Click 4: SOUL.md lives in /sandbox/.openclaw and the policy doesn't protect the persona.

---

## Predict, then test

:::diagrama c53-predice

Notes:
Click 1: the five requests appear with a "?": ask students for their prediction. Clicks 2 to 6, one verdict per click: inference.local goes through; example.com gets a 403 from the proxy; integrate.api.nvidia.com with curl is blocked because the group is for the openclaw binary; /var/lib/apt gives EACCES; writing SOUL.md is allowed (the surprise). Notebook: 12 scored actions. Lab: recipes 3 and 4. A match only backs that one action.

---

## Read a block

:::diagrama c53-bloqueo

Notes:
Click 1: curl to example.com and the proxy answers curl: (56) CONNECT tunnel failed, response 403. Click 2: it shows up in nemoclaw my-assistant logs --tail 50. Click 3: openshell term (Enter → r → Enter → a / x). Click 4: the approval lasts as long as that sandbox instance. Two kinds of block: policy_denied (didn't match, approve it?) and upstream_unreachable (matched, the host didn't answer). A 403 can come from the proxy or the server: CONNECT tunnel failed is from the proxy.

---

## Changing the policy

:::diagrama c53-preset

Notes:
Click 1: the github preset is stapled to the rulebook. One click per action: policy add github --dry-run (dry run), --yes (applies live), policy remove github --yes (removes). Click 4: the live error, the preset opens GitHub for /usr/bin/git, not for curl. Click 5: network and inference change live; files, Landlock and process need the sandbox recreated. openshell term approvals last as long as that instance; to make them persist, use a preset.

---

## The Soporte NemoClaw preset

:::diagrama c53-preset-soporte

Notes:
One click per rule: method GET; host docs.nvidia.com, port 443, protocol rest, path /nemoclaw/**; binaries /usr/local/bin/openclaw. We validate it in the notebook with validar_preset() and apply it with policy add --from-file soporte-docs.yaml --dry-run first.

---

## The sandbox is one layer

:::diagrama c53-una-capa

Notes:
Click 1: the 5.1 attack steps against this policy, each with its "?". Clicks 2 to 5: reading the poisoned FAQ, allowed; reading MEMORY.md, allowed; curl to the attacker's host, blocked; node → clawhub.ai with POST, allowed. Click 6: a secret printed by an allowed command has already escaped. An allow list approves the destination, not the meaning of the bytes. Above: provenance, human approval, secrets outside the sandbox.

---

## If you prefer the terminal

```bash
openshell policy get my-assistant --full > ~/politica-antes.txt   # save the policy
nemoclaw my-assistant logs --tail 50                             # recent blocks
openshell term                                                   # live panel: x rejects, a approves
nemoclaw my-assistant policy add github --dry-run                # dry run
nemoclaw my-assistant policy add github --yes                    # applies live
nemoclaw my-assistant policy add --from-file soporte-docs.yaml --dry-run
nemoclaw my-assistant policy remove github --yes                 # back to how it was
```

.lead It's optional: the same thing you saw on the NVIDIA page and in the notebook, written as instructions.

Notes:
The operator way, from the lab host with brev shell. Don't approve example.com in openshell term: always use x.

---

## Common errors

| Symptom | Cause |
|---|---|
| `CONNECT tunnel failed, response 403` | Policy: host or program |
| `code=403` without CONNECT | The server answered |
| Preset applied, still blocked | Wrong program in the preset |
| The approval "disappeared" | The sandbox was recreated |

Notes:
The full table is on the class page.
