# 2.1 · From a single call to the agent loop

> 🇪🇸 Original Spanish guide: [`clases/2.1-loop-de-agente/README.md`](../../../clases/2.1-loop-de-agente/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Goal: build an agent from scratch and understand what changes when an LLM makes the decision.

| | |
|---|---|
| **Video length** | ≈9 min |
| **Practice** | Notebook (≈45 min), works without a key in MOCK mode |
| **Skill** | Build a basic agent loop |
| **Materials** | [Slides](slides.html) · [Notebook (Spanish)](../../../clases/2.1-loop-de-agente/2.1-loop-de-agente.ipynb) · [FAQ (Spanish)](../../../FAQ.md) |

## What you'll achieve

- Write the **observe → decide → act → stop?** loop and use it with three different "brains": a fixed rule, a search (BFS) and an LLM.
- Validate the model's output before acting, so an invalid move doesn't break your agent.
- Give a chat memory with the `messages` list and put a context limit on it: the first version of **Soporte NemoClaw** (NemoClaw Support).

## Before you start

- Python 3.10 or later on your machine, or a Google account to use Colab.
- Your `nvapi-` API key from class 1.2. **It's optional:** without a key, the notebook runs end to end in MOCK mode (a simulated model).
- The class 1.3 notebook passing, or at least knowing how to read its errors (401, 404, 429, `length`).

## Step by step

### 1. Open the notebook

**In Colab:** upload `2.1-loop-de-agente.ipynb` (File → Upload notebook). To use your key, open the key panel 🔑 (*Secrets*), create `NVIDIA_API_KEY` with your key and turn on notebook access.

**On your machine**, from the root of the course repository:

```bash
python3 -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
echo "NVIDIA_API_KEY=nvapi-xxxxxxxx" > .env    # use your real key; .env isn't pushed to git
jupyter lab clases/2.1-loop-de-agente/2.1-loop-de-agente.ipynb
```

### 2. Run the setup cells

Run the first two cells and the simulator cell.

You should see `Modo: EN VIVO · nvidia/nemotron-3.5-lightning-30b-a3b` (live mode) if your key is fine, or `Modo: MOCK (sin NVIDIA_API_KEY: respuestas simuladas)` (no key: simulated answers) if there's no key. Either one works for what follows.

### 3. Make a single call (section 1)

Run the cell with the question "¿Qué significa que una API de LLM sea 'sin estado'?" (what does it mean for an LLM API to be "stateless"?).

You should see `finish_reason: stop`, a one-sentence answer and, in live mode, the `usage` with the tokens spent. Then change the question to "What did I just ask you?": the model doesn't know, because every call starts from zero.

### 4. Build the environment and an agent without an LLM (sections 2 and 3)

Run the `Laberinto` (maze) cell, then the `correr_agente` (run agent) cell.

You should see that `siempre_derecha` (always right) moves one step and gets stuck: `'derecha' no es válido → no se aplica` ("right" isn't valid, so it isn't applied), until `⛔ Se acabó el presupuesto de 6 pasos sin llegar.` (the 6-step budget ran out without reaching the goal). That cap is what prevents an infinite loop.

Then run `decidir_bfs` (decide with BFS). You should see `✅ Meta en 15 pasos.` (goal in 15 steps) and the map with the path marked with `·`.

Look at `correr_agente` again: it never says "maze" or "BFS". That function won't change for the rest of the class.

### 5. Swap the decision for an LLM (section 4)

Run `decidir_llm` (decide with the LLM). We describe the map to it as text and ask for **one word**.

You should see the agent's steps and, at some point, a line like `⚠ el modelo respondió 'arriba': no es legal. Se lo decimos y reintenta.` (the model answered "up": that's not legal; we tell it and it retries). In MOCK this always happens on the first step; in live mode, when the model makes a mistake. At the end, the comparison `BFS: 15 pasos · LLM: N pasos` (BFS: 15 steps · LLM: N steps).

Do the **✏️ Tu turno** (your turn) experiments: remove the strategy line, remove the map or raise the temperature, and compare how many steps it takes.

### 6. Trigger the error: an invalid move (section 5)

Run `decidir_ingenuo` (naive decision), which uses a sloppy prompt and passes the model's text straight to the environment.

You should see something like:

```text
El modelo dijo: 'Te sugiero ir hacia abajo: a la derecha casi todo es pared...'
💥 Movimiento inválido: 'Te sugiero ir hacia abajo: ...'. Desde (0, 0) solo puedes: ['abajo', 'derecha']
```

The model said "I suggest going down: to the right it's almost all wall…", and the environment rejects that as an invalid move, because from (0, 0) you can only go `abajo` (down) or `derecha` (right).

Run the next cell: `extraer_movimiento` (extract move) pulls out `'abajo'`, validates it against the legal moves and applies it. The lesson: **the model's output is untrusted input; the harness validates it before acting.**

### 7. Check that memory is `messages` (section 6)

Run the "Me llamo Ada" (my name is Ada) cell.

You should see that with history it answers "Te llamas Ada" (your name is Ada) and without history it says it doesn't know. Below, you'll see the exact JSON that was sent on turn 2: that list **is** the memory.

### 8. Build Soporte NemoClaw v1 (section 7)

Run the `ChatSoporte` (support chat) cell. The same conversation runs twice: with a 4-message window and with a 20-message window.

You should see that with 4 messages the bot **forgets your name** ("No sé cómo te llamas", I don't know your name) and with 20 it remembers it. If you want to chat with it, set `INTERACTIVO = True` (interactive) in the next cell.

## Check that it worked

- [ ] `siempre_derecha` stops at the step cap and `decidir_bfs` reaches the goal.
- [ ] `decidir_llm` reaches the goal using **the same** `correr_agente` function.
- [ ] You saw the `💥 Movimiento inválido` (invalid move) and fixed it with `extraer_movimiento` + validation.
- [ ] You can explain why "What is my name?" works with history and fails without it.
- [ ] `ChatSoporte` with a window of 4 forgets the name and with a window of 20 remembers it.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `Modo: MOCK (sin NVIDIA_API_KEY: respuestas simuladas)` even though you set up your key | The kernel started before you created `.env`, `.env` isn't at the repo root, or in Colab you didn't turn on secret access | Restart the kernel and run again from the first cell. See [FAQ (Spanish): MOCK mode](../../../FAQ.md#emock) |
| `RuntimeError: 401 · Key rechazada: ...` (key rejected) | Key incomplete, with spaces, or regenerated | Copy the full key again (`nvapi-...`). See [FAQ (Spanish): 401](../../../FAQ.md#e401) |
| `ValueError: Movimiento inválido: 'Te sugiero ir hacia abajo...'` (invalid move) | You passed the model's text straight to `env.actuar` (act) | Extract the move with `extraer_movimiento` and validate it against `obs["legales"]` (legal moves) before acting |
| `⛔ Se acabó el presupuesto de 30 pasos sin llegar.` (30-step budget ran out) | The model goes in circles: you removed the map or the strategy, or the temperature is high | Restore the map in `describir`, lower the temperature to 0 or raise `max_pasos` (max steps). This is the cap doing its job |
| `⚠ finish_reason=length sin contenido: el modelo gastó max_tokens razonando.` (no content: the model spent max_tokens reasoning) | Nemotron reasoned and ran out of `max_tokens` before answering | Keep `extra_body=SIN_RAZONAR` in the call or raise `max_tokens`. See [FAQ (Spanish): length](../../../FAQ.md#elength) |
| `RuntimeError: 400 · Solicitud inválida: ...` (invalid request) when you change `MODEL` | The new model doesn't accept `chat_template_kwargs` | Remove `extra_body=SIN_RAZONAR` from the calls or go back to `nvidia/nemotron-3.5-lightning-30b-a3b` |
| `RuntimeError: 429 · Demasiadas solicitudes por minuto.` (too many requests per minute) | Each maze step is a call; you ran several runs back to back | Wait a few seconds between runs. See [FAQ (Spanish): 429](../../../FAQ.md#e429) |
| Soporte NemoClaw "forgets" what you told it | The window (`max_mensajes`, max messages) no longer includes that message | That's the memory vs. cost trade-off: widen the window or solve the challenge below |

## Challenge: memory of facts

With `max_mensajes=4`, Soporte NemoClaw forgets your name. Make it remember **without widening the window**: when the user says "me llamo X" (my name is X), store `X` in a `hechos` (facts) dictionary and add it to the system prompt on every call.

**Success criteria** (live): with `max_mensajes=4`, the notebook's `CONVERSACION` (conversation) and two extra questions, the bot correctly answers "¿Cómo me llamo?" (what is my name?) and `len(soporte.historial)` never goes above 5. Write your solution in the `ChatSoporteConHechos` cell (support chat with facts).

## Project milestone

**Soporte NemoClaw v1: a chat with memory and limits.** It has a system prompt with its role and rules (it never asks for or repeats an API key), memory in `historial` (history), a `max_mensajes` window and a `max_turnos` (max turns) cap per session.

Copy `SISTEMA_SOPORTE` (support system prompt) and the `ChatSoporte` class into a `soporte_nemoclaw.py` file in your own repository. In class 2.2 you add the ReAct loop and its first tool.

## Resources

- Lesson 01a · The Agent, NVIDIA DLI course. This class is based on it (Apache-2.0).
- [NVIDIA's course repository (NVDLI/NemoClawDLI)](https://github.com/NVDLI/NemoClawDLI): the code for the maze cells.
- Russell and Norvig, *Artificial Intelligence: A Modern Approach*, ch. 2 (agents and environments): the origin of the perceive → reason → act cycle.
- [Course FAQ (Spanish)](../../../FAQ.md), sections [API errors](../../../FAQ.md#errores-api) and [Notebooks](../../../FAQ.md#notebooks).
