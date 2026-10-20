## When the answer comes out wrong

:::diagrama c34-print-vs-traza

.lead With print you see loose fragments. With a trace you see every step, in order.

Notes:
The 3.3 agent makes about 11 calls per question. If the answer comes out wrong, which one failed? Click 1: with print, loose messages, mixed up and with no timing. Click 2: with a trace, every step with its time and status, like a parcel's tracking; it shows which tool it called, what we sent the model, what the search found and where it broke.

---

## Trace and span

:::diagrama c34-paquete

Notes:
Click 1: a parcel's tracking history. Click 2: the whole history is the trace; each line is a span (start, end, ok or error status, and a parent except the root). Click 3: the same for your agent, drawn as a tree. Click 4: the standards; OpenTelemetry produces and sends, OpenInference gives each step a type (AGENT, LLM, TOOL, RETRIEVER). Phoenix (Arize, open source) receives OTel traces and shows them as a tree.

---

## What each step stores

:::diagrama c34-tipos

Notes:
What the "5 · Instrumenta las tres piezas del agente" cell does. One click per step type: LLM (model, messages, finish_reason, tokens), TOOL (arguments, output and the error if it fails), RETRIEVER (each document with its score). Click 4: the type label tells you where to look.

---

## Redact before saving

:::diagrama c34-tachar

Notes:
Like a black marker on a photocopy. Click 1: a message with a pasted key. Click 2: redactar() crosses it out. Click 3: what gets saved: "nvapi-***". Click 4: that's what reaches the trace and Phoenix. Click 5: why it matters. Same rule as class 1.2. Every attribute goes through poner(), which calls redactar().

---

## The trace of one question

:::diagrama c34-arbol

.lead In Phoenix: Projects → soporte-nemoclaw → the trace → the step you care about.

Notes:
The 401 question. Click 1: the root, the whole agent (936 ms, 3 steps). Click 2: the model asks to check the lab and the tool answers. Click 3: the model asks to search the FAQ; the search brings back conexion-laboratorio.md with score 0.408. Click 4: the model answers (finish=stop). Each bar shows when the step started and how long it took. In Phoenix, click "retriever · buscar_faq" to see documents and scores.

---

## Four bugs, one trace

:::diagrama c34-cuatro-bugs

Notes:
Live error: the four cases from section 9, in that order. Click 1: the tool fails (503), ver_traza. Click 2: the loop never ends, the same invoice search five times until the cap, repeticiones. Click 3: an invented citation, an id no tool returned, citas_sin_respaldo. Click 4: it took too long, and the slow part is the tool (1.5 s), not the model, mas_lentos.

---

## Error ≠ broken answer

:::diagrama c34-error-ok

Notes:
The trace from part a) of section 9. Click 1: the tool step in ✖, with the exact error; the harness returns it to the agent as an observation. Click 2: the agent kept going and the root stays ✔. Click 3: the answer says "No pude verificar…". That's correct, as long as the answer says so; without a trace you'd only see an incomplete answer.

---

## Observability in the NVIDIA stack

:::diagrama c34-nvidia

Notes:
Click 1: for the agent you code, the NeMo Agent Toolkit sends traces with a short YAML to Phoenix, Langfuse, LangSmith, Weave or OTel. Click 2: for the sandbox, NemoClaw keeps its logs: messages, OpenShell blocks and conversation history (nemoclaw <sandbox> logs, sessions export, openshell term). NemoClaw with Deep Agents has --observability, which sends OTLP traces to a collector on the host. Click 3: you use it from Module 4.

---

## If something goes wrong

| You see | Do this |
|---|---|
| “Phoenix: no detectado” | Start Phoenix and run the cell that connects it again |
| No new traces show up | Pick the **soporte-nemoclaw** project and refresh |
| Phoenix won't install | It needs Python 3.11 or later; or use it with Docker |
| Your key shows up in a trace | Save everything with `poner()` and add the missing pattern |

Notes:
Phoenix starts with phoenix serve. The missing pattern goes into _SECRETOS.

---

## If you prefer code and the terminal

```yaml
general:
  telemetry:
    tracing:
      phoenix: {_type: phoenix, endpoint: http://localhost:6006/v1/traces, project: soporte-nemoclaw}
```

```bash
nemoclaw <sandbox> logs              # what happened in the sandbox
nemoclaw <sandbox> sessions export   # the conversation history
openshell term                       # OpenShell blocks, live
```

.lead Optional: the YAML belongs to the NeMo Agent Toolkit; you use the commands from Module 4.

Notes:
For people who code. The YAML goes in the NeMo Agent Toolkit config. The commands run in the Brev lab, with NemoClaw installed.

---

## Project milestone

:::diagrama c34-avance

Notes:
One click per new Soporte NemoClaw capability: each answer's trace, the automatic review of citations, repeats and errors, and a JSON with redacted secrets in trazas/. Click 4: Module 4. Your agent routes, grounds itself, plans, and now you can see what it does inside.
