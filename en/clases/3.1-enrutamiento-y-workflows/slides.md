## When isn't a loop enough?

:::diagrama c31-loop-vs-flujo

Notes:
Click 1: the project ticket. Click 2: the loop from class 2.2, where the model figures out what to check one step at a time. Click 3: the workflow, where your code already knows to check key, instance and session. The question for this class: who decides the shape of the work, the model or your code?

---

## Four patterns

:::diagrama c31-patrones

Notes:
One click per pattern: ReAct (you know it, class 2.2), router, ReWOO and fan-out. Click 5: today we build the three on the right, applied to Soporte NemoClaw.

---

## The router: fixed windows

:::diagrama c31-router

Notes:
The clinic receptionist. Click 1: the ticket arrives. Click 2: the router; the model only picks ONE label and answers in a form with fixed fields (strict JSON with an enum, temperature 0). Click 3: the closed list of windows. Click 4: the 401 lands on api_key. Click 5: your code does the sending. Each specialist is the same code with different instructions (the crear_especialista factory, the "specialist factory" from the NVIDIA lesson).

---

## What if the model makes up a label?

:::diagrama c31-etiqueta

Notes:
Live error for this class. Click 1: the model answers "facturacion", which doesn't exist; used as-is, the program crashes (KeyError). Click 2: your code checks it against the list. Click 3: one retry, showing the model its error. Click 4: if it insists, "otro" and a person reviews it. Click 5: never map synonyms by hand. The model's output is untrusted input, just like the user's.

---

## ReWOO: plan once

:::diagrama c31-rewoo

Notes:
The shopping list before you leave. Click 1: the planner writes the whole plan in one call; your code caps it at 4. Click 2: the executor, with no model, runs every search at once (the fifth is cut by the cap). Click 3: the synthesizer answers with citations. Click 4: two model calls, no matter how many searches. Xu et al., 2023. If step 2 needs the answer from step 1, ReWOO doesn't fit: go back to the loop.

---

## Fan-out / fan-in

:::diagrama c31-fanout

Notes:
Click 1: the 401 report. Click 2: two specialists review it at once. Click 3: the security one doesn't answer (we force it on purpose). Click 4: the join merges what arrived and says what's missing. Click 5: the supermarket checkout analogy. A failed branch doesn't sink the result: the opposite of Promise.all. Retry with a wait only for 429, inside the branch; a 401 is never retried.

---

## Measure the time, don't guess it

:::diagrama c31-tiempo

Notes:
Numbers from no-key (simulated) mode. Click 1: searches one after another versus all at once. Click 2: the two model calls; live, each takes seconds. Click 3: if the model dominates the total, parallelizing barely shows. Live numbers depend on the model and load: fill in with the numbers from the dry run.

---

## When NOT to split

:::diagrama c31-dividir

Notes:
Click 1: a single call (the notebook's generalist). Click 2: the same question split into four calls, with its cost. Click 3: when to split. Click 4: when not to. Every boundary is one more call, more waiting and another place to fail. If reading the trace matters more than speed, don't split either.

---

## If something goes wrong

| You see | Do this |
|---|---|
| The label “facturacion” isn't on the list | Expected: one retry, then “otro” |
| The answer comes back cut off or without the form | Give the answer more room (`max_tokens`) |
| Error 400 when asking for the fixed-field form | Continue without the form, but still check |
| Error 429 in a branch | Fewer branches at once and retry with a wait |
| The program crashes looking for the window | Check the label before sending the ticket |

Notes:
Technical messages as they appear in the notebook: "categoria inválida: 'facturacion'", "JSON ilegible" / finish_reason=length, 400 with response_format, 429, KeyError in ESPECIALISTAS.

---

## If you prefer code

```python
CATEGORIAS = ["instalacion", "api_key", "brev", "seguridad", "otro"]
t = clasificar(ticket)                              # the model picks ONE label
respuesta = ESPECIALISTAS[t["categoria"]](ticket)   # the router: a dictionary

with ThreadPoolExecutor(max_workers=3) as pool:     # fan-out: every branch at once
    futuros = {pool.submit(rama, n, reporte): n for n in RAMAS}
```

.lead Optional: all of this is in the class notebook, ready for ▶.

Notes:
For people who code. response_format with json_schema and enum; temperature 0. In the fan-out, each f.result() goes inside try/except: the branch fails and the others keep going.

---

## Project progress

:::diagrama c31-avance

Notes:
One click per new Soporte NemoClaw capability and, at the end, the challenge. Next step: stop the specialists from answering from memory (class 3.2).
