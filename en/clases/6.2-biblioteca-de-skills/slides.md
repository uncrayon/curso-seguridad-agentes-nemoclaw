## Say it once, keep it forever

:::diagrama c62-sin-con

Notes:
Click 1: without skills, every session starts from scratch and you paste the same rules; each time they come out a bit different. Click 2: with skills, a folder with a `SKILL.md` the agent loads when it needs it: the recipe card. Idea from Voyager (2023): what worked gets saved as a reusable recipe.

---

## Anatomy of a SKILL.md

:::diagrama c62-tarjeta

Notes:
Click 1: the label (frontmatter, between two `---` lines): name and description; it's what the harness always sees. Click 2: the recipe (runbook): numbered steps, with the exact tool. Click 3: the limits; the text asks for them, we'll see who enforces them. The model sees the body only if it picks the skill. The course skills are written in Spanish; the card shows them translated. Leave it 20 seconds: it's the one people screenshot.

---

## Progressive disclosure

:::diagrama c62-menu

.lead A cheap menu; the recipe only when needed.

Notes:
Click 1: the menu (`name: description`), always in the prompt: ~350 tokens for 4 skills. Click 2: the full recipe, only the one ordered. Click 3: loading everything would be ~1,800 tokens with 4 and over 20k with 50 skills, on every call. Numbers from the notebook, section 3.

---

## Explicit vs. automatic

:::diagrama c62-dos-selecciones

Notes:
Click 1: explicit, you name it (`/diagnostico-api ...`); it almost never fails. In lab 03c it's when you give the `SKILL.md` path. Click 2: automatic, the model compares your request with the descriptions; it fails if the description doesn't say when to use it. In 03c it's when you leave out the path. Click 3: NVIDIA says it in 03c: the exercise with the path "doesn't demonstrate automatic selection".

---

## The description is the trigger

:::diagrama c62-disparador

Notes:
Click 1: a vague description ("Useful tool") doesn't say when to use it: nobody picks it. Click 2: the useful one, with its three parts marked. Click 3: what it does + when to use it + the user's words. A description isn't a title: it's a routing rule.

---

## Measure: hit rate

:::diagrama c62-acierto

:::tip
Fix the **description**, not the recipe. And evaluate with the model you'll actually use.
:::

Notes:
One click per bar: vague descriptions 13 %, project descriptions 80 %, after ✏️ Your turn ≥ 90 % (MOCK mode). 15 requests, each with its expected skill. The three misses each teach something: use the user's words, neighboring descriptions compete, and filler words attract requests.

---

## Take it to the lab

:::diagrama c62-al-lab

.lead Without a terminal, your library already works in the notebook. This is the operator path.

Notes:
Click 1: your skill-library folder. Click 2: `brev copy ./skill-library <instance>:/home/ubuntu/skill-library`. Click 3: `brev shell <instance>` and `nemoclaw my-assistant skill install ~/skill-library/diagnostico-api/`; confirm with `nemoclaw my-assistant skill list`. Click 4: new session and try both selection modes (lesson 03c, the block for activating a skill during the conversation). OpenClaw puts it in /sandbox/.openclaw/workspace/skills/<name>. Hermes in /sandbox/.hermes/skills; Deep Agents in /sandbox/.deepagents/agent/skills.

---

## Common errors

:::diagrama c62-errores

Notes:
One click per error. 1: `mapping values are not allowed here` = there's a `: ` inside the description; use quotes (the YAML error is number one; we trigger it live). 2: the name only accepts letters, numbers, `.` `-` `_`. 3: installed but not used on its own: improve the description and open a new session. 4: picks the wrong skill: say when **not** to use it.

---

## A skill is persistence

:::diagrama c62-persistencia

Notes:
Click 1: your library, with a poisoned skill hidden in it. Click 2: a poisoned skill is a poisoned directive that survives across sessions. Clicks 3 to 5: review them like code (diff, owner, pull request); the text asks, the tool and the sandbox enforce; decide who can write to `skills/`. Tie it back to 5.1: persistence makes an injection outlast a conversation.
