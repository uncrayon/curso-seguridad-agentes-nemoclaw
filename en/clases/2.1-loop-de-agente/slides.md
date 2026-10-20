## A model is not an agent

:::diagrama modelo-vs-agente

.lead The difference isn't the model: it's the code around it.

Notes:
Open with the question: what does ChatGPT lack to be an agent? The answer is the loop. Click 1: the model alone (text in, text out, once). Click 2: the same model inside a repeating cycle, with tools and memory.

---

## The loop

:::diagrama c21-loop

Notes:
The recipe: you read the step, do it, taste, and keep going. Clicks 1 to 4: observe, decide, act and done yet? (with the "no: one more round" arrow). Click 5: yes, done. Click 6: the step cap. It's almost literally the notebook's correr_agente function (for paso in range(max_pasos)); it never says "maze" or "LLM".

---

## A call has no state

:::diagrama c21-sin-estado

Notes:
Demo: ask "What did I just ask you?". Click 1: a normal call. Click 2: the second call knows nothing about the first. Click 3: every call starts from zero. Click 4: what every answer brings (in the notebook: content, finish_reason and usage; some models also return reasoning_content).

---

## The decision is swappable

:::diagrama c21-cerebros

Notes:
It's the core idea of NVIDIA's lesson 01a: observing and acting don't depend on who decides. Click 1: the loop with a slot where "decide" goes. Clicks 2 to 4: three brains (fixed rule, breadth-first search BFS, LLM). Click 5: the loop doesn't change.

---

## When an LLM decides

:::diagrama c21-decide-llm

Notes:
Click 1: the prompt describes the map as text (position, goal, legal moves) and asks for a single word. Click 2: the model answers. Click 3: we extract the move. Click 4: we validate it against the legal moves. Click 5: only then do we act. Click 6: if it's not legal, we tell it and it retries. Click 7: the schema and the prompt ask; the harness enforces. SIN_RAZONAR turns off Nemotron's long reasoning: it's the "direct" profile in NVIDIA's course.

---

## Common errors

:::diagrama c21-confianza

Notes:
The live error in this class: sloppy prompt + trusting the text → 💥 Movimiento inválido. Click 1: the lane that fails. Click 2: the one that works (extract + validate). Click 3: the golden rule. Other errors: "⛔ Se acabó el presupuesto de pasos" = you took context away from the model (map, strategy); finish_reason=length with no content = the model over-reasoned, raise max_tokens; "Modo: MOCK" with a key = restart the kernel.

---

## Memory is a notebook

:::diagrama c21-libreta

.lead In code, the notebook is called `messages`.

Notes:
Click 1: turn 1. Click 2: in turn 2 everything is resent and it answers "Your name is Ada". Click 3: without the notebook, it doesn't know. Click 4: every turn costs more than the last. All of an agent's memory, context and cost come from this fact.

---

## Project: Soporte NemoClaw v1

:::diagrama c21-soporte-v1

Notes:
Click 1: what it has (system prompt with role and rules, history, never asks for or repeats an API key, max_turnos per session). Clicks 2 and 3: the max_mensajes window; with 4 it forgets the name, with 20 it remembers. Click 4: memory versus cost. In 2.2 we give it ReAct and a tool.

---

## Your practice

:::diagrama c21-practica

Notes:
One click per step. Questions on the class page: steps for "always right" and for the search (section 3), the sloppy prompt's sentence (section 5), how many messages until it forgets your name (section 7). If you code: the "✏️ Tu turno" experiments (no map, no strategy, temperature 1.0), the fact-memory challenge with a window of 4 and, optionally, NVIDIA's lesson 01a (includeHistory:false, profiles direct, reasoning, omni).
