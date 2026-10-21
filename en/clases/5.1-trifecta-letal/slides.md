## A chatbot talks. An agent acts.

:::diagrama c51-dice-hace

Notes:
Click 1: the chatbot (text in, text out; the worst case is a wrong answer). Click 2: the agent, with files, programs, internet, memory and tasks that run on their own; the worst case is a wrong action with nobody watching. Click 3: the key detail, it takes any text it reads as an order. Earlier we left the agent working on its own: today, what's the worst it can do with the access it already has?

---

## The lethal trifecta

:::diagrama c51-trifecta

Notes:
One click per leg, with the glossary analogy: click 1, private data (the keys to your house); click 2, untrusted content (mail from anyone); click 3, external communication (a phone). Click 4: all three connect in red, that's the attack. Click 5: we remove one leg (here, the output) and the path breaks. Simon Willison's idea, used by NVIDIA in 04a. Stress this: the output includes the model service and the chat reply.

---

## The attack: a poisoned FAQ

:::diagrama c51-faq-envenenada

Notes:
Click 1: someone proposes a "helpful" change to the course FAQ. Click 2: the entry looks normal. Click 3: the hidden comment the page doesn't show. Click 4: the agent reads it as an order. Click 5: the name, prompt injection (indirect: the user doesn't write the order, it comes inside data the agent reads). The student only asked where to store their key.

---

## What happened, step by step

:::diagrama c51-ataque-pasos

Notes:
One click per step: the question; buscar_faq returns the poisoned entry; the model reads the comment as an order; enviar_http sends the internal token (tok-soporte-…) out; the reply to the student is perfect. Click 6: no step was illegal. Demo in the optional notebook. Live, the real model sometimes falls for it and sometimes doesn't. "Sometimes" is not a defense.

---

## Three layers of defense

:::diagrama c51-capas

Notes:
From the inside out, one click per layer: the prompt (what does it want to do?; the model can be tricked), OpenClaw's harness (is the call valid?; only checks what you coded) and OpenShell's sandbox (what does it achieve even if tricked?; doesn't understand the content). Click 4: policy is enforced below the model. Least privilege (Saltzer and Schroeder, 1975). Don't try to prove the model's intent: measure the boundaries.

---

## Four OpenShell mechanisms

:::diagrama c51-mecanismos

Notes:
One click per question, each with its technical name on the label: where does it connect? (isolated network namespace + CONNECT proxy + OPA); which files can it reach? (Landlock); which actions does it ask the system for? (seccomp: no ptrace, mount, setuid); what power does it start with? (sandbox user, no root). Click 5: soon you test user and seccomp; then network and files. Don't read the technical names out loud.

---

## What the sandbox can't see

:::diagrama c51-no-ve

Notes:
Click 1: a reply goes to an allowed site; the guard checks the destination and lets it through. Click 2: your password, hidden in the message, goes out the same way; the guard lets it through too. Click 3: the allow list approves the destination, not the meaning of the bytes. Click 4: what's still needed above. NVIDIA 04a table (aligned with the OWASP Top 10 for Agentic Applications): prompt injection → provenance and human approval; tool misuse → argument validation; identity abuse → least-scope tokens; poisoned memory → reviewable history.

---

## Your trifecta worksheet

:::diagrama c51-hoja

.lead Fill it in for your agent: you'll use it in a future class.

Notes:
The Soporte NemoClaw example, one click per leg: private data (MEMORY.md, cron summaries, the gateway token), untrusted (the FAQ, the questions), output (the model, clawhub.ai, the chat). Click 4: the leg we remove, don't store personal data. The full table and five practice cases are on the class page; ask them to save it as trifecta.md.

---

## Common mistakes

:::bad
"My agent doesn't go online" → the model and the chat are outputs too.
:::

:::bad
"I'll fix it in the prompt" → it's the weakest layer.
:::

:::bad
"The sandbox protects me from everything" → we disprove it with data later.
:::

Notes:
Close with the key idea: removing one leg breaks the attack.
