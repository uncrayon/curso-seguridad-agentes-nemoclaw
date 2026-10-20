## Why a single context breaks

:::diagrama c33-escritorio

.lead The way out isn't a bigger model: it's to stop stacking.

Notes:
The context is the work desk. A single loop researching key, instance and cookie piles everything on the same desk. One click per failure (NVIDIA lesson 02c). Click 1: overflow, it no longer fits in the context window. Click 2: context rot, it fits but the middle carries little weight (Lost in the Middle, 2023). Click 3: interference, reasoning about A pollutes B.

---

## Plan, research, preserve, synthesize

:::diagrama c33-flujo

Notes:
The project lead. Click 1: plan; the planner splits the report into 2 to 4 parts, capped. Click 2: research; one subagent per part, in parallel and with a clean desk. Click 3: preserve; each leaves its draft in a file (/borradores/s1.md). Click 4: synthesize; the synthesizer reads files, not conversations, and writes the report with citations. It's the idea behind libraries like deepagents or LangGraph, here in plain Python.

---

## Each subagent, its own context

:::diagrama c33-escritorios

Notes:
One click per subagent. Each starts with an empty desk: its instructions, the report and its part; nothing from its siblings' history. Tools: buscar_faq (the RAG from 3.2) and escribir_archivo. The harness permission only lets it write to /borradores/<its id>.md. Click 4: don't assume it, check it: the "Comprueba el aislamiento" cell.

---

## The diagnostic report

:::diagrama c33-reporte

Notes:
The report for "I get a 401 in the lab after resuming Brev". Click 1: the report. Click 2: the most likely cause, with its FAQ citation. Click 3: the steps. Click 4: what couldn't be verified, if a subagent failed. Click 5: your code checks every citation: it must be in a draft and exist in the FAQ (revisar_citas).

---

## Caps and failures

:::diagrama c33-topes

Notes:
One click per risk and its protection: MAX_SUBAGENTES = 4; max_pasos = 5; "permiso denegado" returned as an observation; the report says what's missing; revisar_citas. Live error: subagent s9 tries to write to /reporte_diagnostico.md.

---

## Isolated context ≠ sandbox

:::diagrama c33-no-es-sandbox

Notes:
Click 1: today's separate desks; they separate what the agent thinks and your code enforces them. Click 2: but they run in your program: they see your NVIDIA_API_KEY and your disk (the os.environ cell). Click 3: the locked room from class 1.1; it limits what the agent touches and the operating system plus policy enforce it. Click 4: you need both.

---

## What it costs

:::diagrama c33-costo

.lead Use it only when the problem doesn't fit in one conversation or you need several independent investigations.

Notes:
Each circle is one model call. Click 1: the search agent from class 3.2, 2 to 3 calls. Click 2: the deep agent with 3 subagents, about 11.

---

## If something goes wrong

| You see | Do this |
|---|---|
| “El planificador no devolvió subtareas válidas” | Look at what it answered and ask for a clearer format |
| “Terminó sin guardar su borrador” | Remind it to save and check the step cap |
| Error 429 with several subagents | Fewer subagents at once and retry with a wait |
| “no_existen_en_faq” in the review | The report isn't trustworthy: review it |

Notes:
For the 429: lower max_workers and retry with a wait. "Terminó sin guardar": reinforce step 2 of SISTEMA_SUBAGENTE and check max_pasos.

---

## If you prefer code

```python
mensajes = [
  {"role": "system", "content": SISTEMA_SUBAGENTE},
  {"role": "user", "content": f"Reporte: {reporte}\nTu subtarea: {st['objetivo']}"},
]   # nothing from its siblings' history
```

.lead Optional: all of this is in the class notebook, ready for ▶.

Notes:
For people who code: ejecutar_subagente builds this list from scratch for each subagent; escribir_archivo rejects any path outside /borradores/<id>.md.

---

## Project progress

:::diagrama c33-avance

Notes:
One click per new Soporte NemoClaw capability. Click 5: Module 4, where you take it to NemoClaw on Brev; the FAQ goes in the workspace and the soporte-nemoclaw skill runs in a sandbox. Your agent routes, grounds itself and plans; now it needs a safe place to live.
