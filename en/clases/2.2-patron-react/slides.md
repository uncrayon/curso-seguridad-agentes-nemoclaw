## ReAct: reason, act, observe

:::diagrama c22-detective

.lead ReAct stands for *Reasoning + Acting*.

Notes:
Pattern from Yao et al., 2022; it's behind LangChain, OpenClaw and almost every modern agent. Click 1: the question. Click 2: the reason → act → observe cycle (it lights up step by step on its own). Click 3: once it can, it answers. Click 4: the detective comparison.

---

## Tool and tool call

:::diagrama c22-pide

Notes:
Click 1: the model only sees the tool's card (name, description, inputs = the schema). Click 2: it sends a request (tool_call) and your code checks it. Click 3: your code runs the tool. Click 4: the result comes back as text. Click 5: the model runs nothing. Stress it: the harness is what executes. That will be key for security in Module 5.

---

## `finish_reason`: the note when hanging up

:::diagrama c22-finish

Notes:
Demo: the same question without tools (stop) and with tools (tool_calls). Click 1: the model stops writing and leaves a note. Clicks 2 to 4: stop, tool_calls and length, and what the loop does with each. Click 5: if an agent acts weird, check finish_reason first. There's a fourth value, content_filter (safety filter): the loop warns the user.

---

## The ReAct loop, round by round

:::diagrama c22-vueltas

Notes:
"What time is it in UTC?". Click 1: round 1, tool_calls, the clock runs and the request and result are written down with the same id (tool_call_id). Click 2: round 2, stop and the answer. Click 3: the step cap (max_pasos). The three details of the notebook's react function: same tag, validate before running, cap.

---

## How the notebook grows

:::diagrama c22-libreta

Notes:
It's the disclosure in lesson 01b: inspect the order of messages. One click per message: system, user, assistant (asks for get_current_time), tool (the result) and assistant (the answer). Click 6: the tool message is the proof it ran.

---

## Common errors

:::diagrama c22-errores

Notes:
Live error: SISTEMA_TERCO hits the 4-step cap. Click 1: the stubborn agent; without max_pasos it would keep calling the model (and spending credits) forever. Click 2: the broken request (tc_falso cell): broken JSON in arguments, a made-up tool (get_time) or inputs it doesn't accept; each comes back as "ERROR: ..." with the list of available tools, without raising an exception. Click 3: none of them breaks the loop. Others: finish_reason="length" → raise max_tokens, never treat it as a final answer; 400 after a tool → the assistant turn is missing or the tool_call_id doesn't match.

---

## Context rot

:::diagrama c22-context-rot

.lead *Context rot*: a conversation that goes bad from being too long.

Notes:
Show the tokens_aprox cell: from hundreds to thousands of tokens per call. Click 1: every step resends everything, the notebook grows. Clicks 2 to 4: more cost, more waiting, and the model pays less attention to what's in the middle (Liu et al., 2023). Click 5: Module 3 mitigations (plan first, retrieve just enough, delegate to subagents).

---

## Project: Soporte NemoClaw v2

:::diagrama c22-soporte-v2

Notes:
Demo question: "Soy de Bogotá. ¿Qué hora es allá?" (I'm in Bogotá, what time is it there?). One click per piece: the student, Soporte NemoClaw v2 (ReAct loop with a cap and validation of every tool_call), the hora_local(ciudad) tool and the answer. Click 5: the react function didn't change; you only add the schema to TOOLS and the function to REGISTRO. In 2.3: buscar_faq and estimar_costo_brev.

---

## Your practice

:::diagrama c22-practica

Notes:
One click per step. Questions on the class page: the finish_reason without and with the clock (section 2), how many steps until the stubborn agent stops (section 5), which city Soporte NemoClaw asked the time for (section 7). If you code: trigger the three failures; "✏️ Tu turno" (no hint in the question, the capital of France, minutes until 17:00); challenge: minutos_hasta(hora_utc) with a single tool call; optional: NVIDIA's lesson 01b.
