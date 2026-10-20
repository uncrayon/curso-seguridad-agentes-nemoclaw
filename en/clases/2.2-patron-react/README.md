# 2.2 · Reasoning with the ReAct pattern

> 🇪🇸 Original Spanish guide: [`clases/2.2-patron-react/README.md`](../../../clases/2.2-patron-react/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Goal: build a ReAct loop from scratch that requests tools, runs them safely and knows when to stop.

| | |
|---|---|
| **Video length** | ≈9 min |
| **Practice** | Notebook (≈45 min), works without a key in MOCK mode |
| **Skill** | Implement the ReAct pattern |
| **NVIDIA lesson** | [01b · The ReAct Loop](https://nvdli.github.io/NemoClawDLI/nemoclaw/01b-react.html) |
| **Materials** | [Slides](slides.html) · [Notebook (Spanish)](../../../clases/2.2-patron-react/2.2-patron-react.ipynb) · [FAQ (Spanish)](../../../FAQ.md) |

## What you'll achieve

- Read `finish_reason` and use it as the loop's router: `stop`, `tool_calls` or `length`.
- Write a ReAct loop from scratch that validates each `tool_call`, runs the tool and returns the result as a `tool` message.
- Detect and contain the three typical failures: a malformed `tool_call`, an infinite loop, and an answer cut off by `length`.

## Before you start

- You've finished class 2.1: you know what the loop is and that memory is `messages`.
- Python 3.10+ or Colab, and your `nvapi-` key (optional: without a key it runs in MOCK).
- Open the notebook the same way as in [class 2.1](../2.1-loop-de-agente/README.md#1-open-the-notebook).

## Step by step

### 1. Open the notebook and run the setup

```bash
source .venv/bin/activate
jupyter lab clases/2.2-patron-react/2.2-patron-react.ipynb
```

Run the first two cells and the simulator cell. You should see `Modo: EN VIVO · ...` (live mode) or `Modo: MOCK ...`, and `Reglas del simulador listas: 1` (simulator rules ready: 1).

### 2. Define your first tool (section 1)

Run the `get_current_time` cell. Notice its two parts: the **function** (`get_current_time`) and the **schema** (`TOOL_HORA`, the time tool), which is the only thing the model sees.

You should see the current time, for example `2026-10-21 16:05:12 UTC`.

### 3. Read `finish_reason` (section 2)

Run the cell with the two questions.

You should see:

```text
[sin tools] finish_reason = 'stop'
   tool_calls: []
[con tools] finish_reason = 'tool_calls'
   tool_calls: [('get_current_time', '{}')]
```

(`sin tools` means without tools; `con tools`, with tools.)

The tool **wasn't run**: the model only requested it. Do the **✏️ Tu turno** (your turn): delete "Usa get_current_time para leer el reloj." (use get_current_time to read the clock) from question 2 and see whether the model still requests it based on the description alone.

### 4. Build the ReAct loop (section 3)

Read the `react` function before you run it. It has three pieces:

1. The **router**: `length` stops with an error, `tool_calls` runs tools and `stop` returns the answer.
2. The **validation** of each `tool_call` (`validar_tool_call`, validate tool call): the tool must exist and the arguments must be a JSON object.
3. The `max_pasos` (max steps) **cap**.

Run it with "¿Qué hora es en UTC?" (what time is it in UTC?). You should see:

```text
[paso 1] finish_reason='tool_calls' · se enviaron 2 mensajes
   🔧 get_current_time({}) → 2026-10-21 16:05:12 UTC
[paso 2] finish_reason='stop' · se enviaron 4 mensajes
💬 Son las 16:05:12 UTC ...
```

Step 1 sends 2 messages and requests the tool; step 2 sends 4 messages and answers with the time.

### 5. Watch `messages[]` grow (section 4)

Run `mostrar(traza)` (show trace). You should see the `system`, `user`, `assistant` (requests the tool), `tool` (the result) and `assistant` (the answer) turns, plus a token estimate.

Do the two **✏️ Tu turno** experiments: ask for the capital of France (it ends at step 1 with `stop`) and ask "How many minutes until 17:00 UTC?" (count the tool calls).

### 6. Trigger the three failures (section 5)

- **a) Malformed `tool_call`.** Run the `tc_falso` (fake tool call) cell. You should see four errors as text, for example `ERROR: los argumentos no son JSON válido (Expecting property name enclosed in double quotes)` (the arguments aren't valid JSON). None of them breaks the loop.
- **b) Infinite loop.** Run `SISTEMA_TERCO` (stubborn system prompt). You should see 4 steps calling the clock and `⛔ Tope de 4 pasos sin respuesta final.` (4-step cap with no final answer).
- **c) `length`.** Run the question with `max_tokens=20`. You should see `finish_reason='length'` and `⛔ El modelo llegó a su límite de tokens (length).` (the model hit its token limit).

### 7. Measure context rot (section 6)

Run the `tokens_aprox` (approximate tokens) cell. You should see how the tokens per call grow with each round of tools (from hundreds to thousands).

### 8. Project milestone: `hora_local` (section 7)

Run the Soporte NemoClaw cell. You should see `🔧 hora_local({"ciudad": "Bogotá"})` (local time for a city) and an answer with the local time. Notice that **you didn't touch `react`**: you only added the schema to `TOOLS_SOPORTE` and the function to `REGISTRO_SOPORTE` (support tool registry).

### 9. (Optional) Practice in the browser with the NVIDIA lesson

In [NVIDIA lesson 01b](https://nvdli.github.io/NemoClawDLI/nemoclaw/01b-react.html), with your key saved in lesson 01a:

1. In the **finish_reason · the one field the loop reads to decide what to do next** cell, remove the sentence that asks to use `get_current_time` from `QUESTION_2` and run it again.
2. In **The complete ReAct loop, built from scratch**, **User input** node, change `state.userPrompt` to `"What is the capital of France?"` and look at the `finish_reason` of step 1.
3. In the same node, change the system prompt to `"You must always call get_current_time once, then answer."` and check whether the model obeys.
4. Ask `"How many minutes until 17:00 UTC?"` and count how many times it calls the clock.
5. In the chat panel at the bottom, ask "How does the clock loop decide when to stop?".

## Check that it worked

- [ ] You can explain what the loop does with each `finish_reason`: `stop`, `tool_calls`, `length`.
- [ ] `react("¿Qué hora es en UTC?")` finishes in 2 steps and the history has a `tool` message.
- [ ] The four `tc_falso` return an `ERROR: ...` as text, with no exception.
- [ ] `SISTEMA_TERCO` stops at the step cap.
- [ ] Soporte NemoClaw (NemoClaw Support) answers your city's time using `hora_local`.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| The model answers with a made-up time without calling `get_current_time` | The description or the system prompt doesn't make it clear that the model has no clock | Strengthen the description ("you don't have a clock") and check the history: if there's no `tool` message, the tool didn't run |
| `⛔ Tope de 6 pasos sin respuesta final.` (6-step cap with no final answer) | The model requests tools over and over | Check the history with `mostrar(t)`; fix the system prompt or the tool result. Don't remove the cap. See [FAQ (Spanish): loop](../../../FAQ.md#notebooks) |
| `⛔ El modelo llegó a su límite de tokens (length).` (the model hit its token limit) | `max_tokens` too low; Nemotron spends tokens reasoning before it answers | Raise `max_tokens` (the helper uses 4096) or ask for shorter answers. See [FAQ (Spanish): length](../../../FAQ.md#elength) |
| `ERROR: los argumentos no son JSON válido (Expecting property name enclosed in double quotes)` (the arguments aren't valid JSON) | The model sent broken JSON in `arguments` | The harness already returns it as an observation so the model can correct it. If it keeps happening, simplify the schema |
| `AttributeError: 'types.SimpleNamespace' object has no attribute 'get'` | You appended `c.message` as is to `messages` instead of a dict | Use `messages.append(a_dict(c.message))` |
| `RuntimeError: 400 · Solicitud inválida: ...` (invalid request) after running a tool | You appended the `tool` message without the `assistant` turn that requested it, or with a different `tool_call_id` | First append `a_dict(c.message)`, then one `tool` message per `tool_call`, with the same `tc.id` |
| `RuntimeError: 429 · Demasiadas solicitudes por minuto.` (too many requests per minute) | Each step of the loop is a call and you ran many in a row | Wait a few seconds; don't remove the step cap. See [FAQ (Spanish): 429](../../../FAQ.md#e429) |

## Challenge: avoid redundant calls

Add `minutos_hasta(hora_utc)` (minutes until), which takes `"17:00"` and returns how many minutes are left from now, in UTC.

**Success criteria** (live): with the tool in `TOOLS_SOPORTE` and `REGISTRO_SOPORTE`, "How many minutes until 17:00 UTC?" is answered with **a single** tool call, and the number matches your own calculation.

## Project milestone

**Soporte NemoClaw v2: ReAct with a new tool.** It's no longer just a chat: it decides when to request a tool, runs it with validation and has a step cap. Its new tool is `hora_local(ciudad)` (local time for a city), for students all over Latin America.

Add `react`, `validar_tool_call`, `a_dict`, `hora_local` and its schema to your `soporte_nemoclaw.py`. In class 2.3 you give it its real tools: `buscar_faq` (FAQ search) and `estimar_costo_brev` (Brev cost estimate).

## Resources

- [Lesson 01b · The ReAct Loop](https://nvdli.github.io/NemoClawDLI/nemoclaw/01b-react.html), NVIDIA DLI course. This class is based on it (Apache-2.0).
- Yao et al. (2022), [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629).
- Liu et al. (2023), [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172): the evidence for context rot.
- Lilian Weng (2023), [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/): model, memory, planning and tools.
- [Course FAQ (Spanish)](../../../FAQ.md#errores-api).
