# 2.3 · Turn functions into tools

> 🇪🇸 Original Spanish guide: [`clases/2.3-funciones-a-herramientas/README.md`](../../../clases/2.3-funciones-a-herramientas/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Goal: turn Python functions into tools the model uses well, with validated arguments and errors the agent can correct.

| | |
|---|---|
| **Video length** | ≈9 min |
| **Practice** | Notebook (≈50 min), works without a key in MOCK mode |
| **Skill** | Turn functions into agent tools |
| **NVIDIA lesson** | [01c · Tools at Scale](https://nvdli.github.io/NemoClawDLI/nemoclaw/01c-tools.html) |
| **Materials** | [Slides](slides.html) · [Notebook (Spanish)](../../../clases/2.3-funciones-a-herramientas/2.3-funciones-a-herramientas.ipynb) · [FAQ (Spanish)](../../../FAQ.md) |

## What you'll achieve

- Generate a tool's contract (name, description, schema) from a function's signature and docstring.
- Validate arguments with hand-written JSON Schema and return each error as an observation the model can correct.
- Give Soporte NemoClaw (NemoClaw Support) its first real tools, `buscar_faq` (FAQ search) and `estimar_costo_brev` (Brev cost estimate), and know when to use a subagent or an MCP server (and what risk it brings).

## Before you start

- You've finished class 2.2: you have a ReAct loop with validation and a step cap.
- Python 3.10+ or Colab, and your `nvapi-` key (optional: without a key it runs in MOCK).
- If you run the notebook from the repo, it loads the full FAQ from `datos/faq/`. In Colab it uses an embedded sample of 9 questions; either option works.

## Step by step

### 1. Open the notebook and run the setup

```bash
source .venv/bin/activate
jupyter lab clases/2.3-funciones-a-herramientas/2.3-funciones-a-herramientas.ipynb
```

Run the first two cells and the simulator cell.

### 2. Load the FAQ (section 2)

Run the `cargar_faq` (load FAQ) cell. You should see one of these two lines:

```text
FAQ completa: 61 entradas de 9 archivos en datos/faq/
FAQ de muestra incrustada: 9 entradas (no encontré datos/faq/)
```

The first means the full FAQ loaded (61 entries from 9 files); the second, that it fell back to the embedded sample (9 entries, `datos/faq/` not found).

(The exact number of entries depends on the repo version.) Each file's format is `# Tema` (topic), then `## P: pregunta` (Q: question) and the answer below it.

### 3. Turn functions into tools (section 3)

Read the `@herramienta` (tool) decorator and the project's two functions. Run the cell.

You should see the FAQ entry about the 401 error, the calculation `72 h × $0.15/h ≈ $10.80 USD de cómputo...` (of compute) and the JSON schema for `estimar_costo_brev`, with `"type": "number"`, `"minimum": 0.1` and `"additionalProperties": false`. That JSON is the only thing the model sees.

### 4. See how the model chooses (section 4)

Run the `PREGUNTAS` (questions) cell. You should see:

```text
👤 ¿Qué hago si me sale error 401?
   → [('buscar_faq', '{"consulta": "..."}')]
👤 ¿Cuánto me cuesta dejar Brev prendido 10 horas a 0.15 la hora?
   → [('estimar_costo_brev', '{"horas": 10.0, "tarifa_hora": 0.15}')]
👤 Hola, ¿cómo estás?
   → (responde sin herramienta)
```

The three questions are "What do I do if I get a 401 error?" (routed to `buscar_faq`), "How much does it cost to leave Brev on for 10 hours at 0.15 an hour?" (routed to `estimar_costo_brev`) and "Hi, how are you?" (answered without a tool).

With your key, do the **✏️ Tu turno** (your turn): change the `buscar_faq` description to `"Tool 1."`, run `PREGUNTAS` again and compare. Then restore the description by running the section 3 cell again.

### 5. Validate arguments and break things on purpose (section 5)

Run `validar_args` (validate arguments) and `ejecutar` (execute), then the `casos` (cases) cell. You should see six errors as text, for example:

```text
estimar_costo_brev({"horas": "tres días", "tarifa_hora": 0.15})
   → ERROR de validación: 'horas' debe ser number, llegó str ('tres días'). Corrige los argumentos y vuelve a llamar.
borrar_instancia({"nombre": "mi-lab"})
   → ERROR: la herramienta 'borrar_instancia' no existe o no está permitida. Usa una de: [...]
```

The first is a validation error: `horas` (hours) must be a number but got the string "tres días" (three days), so the model should fix the arguments and call again. The second says the tool `borrar_instancia` (delete instance) doesn't exist or isn't allowed.

None of them raises an exception. And notice `borrar_instancia`: the model can request any name, but only what's in your registry gets run.

### 6. Run Soporte NemoClaw with real tools (section 6)

Run the `agente` (agent) cell with the three questions. In the "tres días" (three days) one you should see the recovery:

```text
🔧 estimar_costo_brev({"horas": "tres días", ...}) → ERROR de validación: 'horas' debe ser number...
🔧 estimar_costo_brev({"horas": 72, "tarifa_hora": 0.15}) → 72 h × $0.15/h ≈ $10.80 USD...
```

The model read the error and corrected itself. In live mode, many models send `72` on the first try; the harness protects you for when they don't.

### 7. Swap the backend without touching the loop (section 7)

Run the `buscar_faq_semantica` (semantic FAQ search) cell. Switch the registry to the embeddings version (`nvidia/nemotron-3-embed-1b`), run the agent, and switch back to the original backend. The schema didn't change and the model never notices.

With your key, try questions with synonyms ("mi llave", my key; "no la acepta", it won't accept it) and compare the two backends. Keep them in Spanish, since the FAQ is in Spanish.

### 8. Hide a subagent behind a tool (section 8)

Run the `consultar_experto_brev` (ask the Brev expert) cell. You should see `↳ principal → subagente: ...` (main → subagent) and `↳ subagente → principal: ...` (subagent → main): the main agent only sees one tool; the subagent has its own prompt and only `estimar_costo_brev`.

### 9. Discover tools with MCP and filter them (section 9)

Run the two `ServidorMCPSimulado` (simulated MCP server) cells. You should see:

```text
✅ faq_curso: aceptada
🚫 sincronizar_notas: rechazada · fuera de la lista blanca=True · alertas=['api key', 'antes de responder', 'historial completo']
```

`faq_curso` (course FAQ) is accepted. `sincronizar_notas` (sync notes) is rejected: it's outside the allowlist, and it raised alerts for "api key", "antes de responder" (before answering) and "historial completo" (full history).

`tools/list` returned a tool with an instruction hidden in its description. Your allowlist rejected it before the model could read it.

### 10. (Optional) Practice in the browser with the NVIDIA lesson

In [NVIDIA lesson 01c](https://nvdli.github.io/NemoClawDLI/nemoclaw/01c-tools.html), with your key saved in lesson 01a:

1. In **two tools, the model routes**, edit the descriptions of `calculate` and `explain_concept` (the **Tool A · calculate** and **Tool B · explain_concept** nodes) and run the **LLM call · the model routes** node again with each question in `EXAMPLES`.
2. In **agents as tools · ask a sub-agent about customer data**, ask "Who opened the most tickets in the last 30 days?" and read what the subagent returns to the main agent.
3. In **MCP-shaped tool server · discovery + dispatch**, run the `tools/list` node and compare the discovered schemas with the ones in this notebook.
4. In the chat panel at the bottom, try "What is 17.5% of 2,480?" and "What is a vector database?".

NVIDIA's glossary is in English, so search with English terms ("vector database", "AI agent"). Queries in other languages may return no results.

## Check that it worked

- [ ] `json.dumps(TOOLS[1])` shows the `estimar_costo_brev` schema with types, limits and descriptions.
- [ ] The six `casos` return an `ERROR ...` as text, with no exception.
- [ ] Soporte NemoClaw cites the FAQ (topic and question) and recovers from the "tres días" (three days) error.
- [ ] You swapped the `buscar_faq` backend without touching `agente` or the schema.
- [ ] You can explain why `tools/list` is untrusted input.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `FAQ de muestra incrustada: 9 entradas (no encontré datos/faq/)` (embedded sample FAQ) and you expected the full FAQ | You opened the notebook in Colab or from another folder | That's normal in Colab. On your machine, open the notebook from `clases/2.3-funciones-a-herramientas/`. See [FAQ (Spanish): notebooks](../../../FAQ.md#notebooks) |
| The model answers from memory and never calls `buscar_faq` | The description doesn't say when to use it, or the system prompt doesn't forbid guessing | Write **when** to use it in the description ("for any question about…") and add "never make up data" to the system prompt |
| `ERROR de validación: 'horas' debe ser number, llegó str ('tres días')` (validation error) over and over | The model doesn't understand the format | Put an example in the parameter description ("72 for 3 days"); the step cap prevents an infinite loop |
| `Sin resultados en la FAQ para '...'` (no results in the FAQ) | The keyword search found no matches (synonyms, typos) | Try other words or the semantic backend from section 7. The agent should say it didn't find it, not guess |
| `KeyError: 'buscar_faq'` or `StopIteration` in `ejecutar` | You ran cells out of order and `TOOLS` or `REGISTRO` (registry) ended up empty | Run the section 3 cell again (the decorator resets `TOOLS` and `REGISTRO`) |
| `RuntimeError: 422 · Argumentos con formato incorrecto ...` (malformed arguments) on embeddings | You called `client.embeddings.create` without `input_type` | Use the `embed(textos, input_type="query" o "passage")` helper, which already adds it |
| `RuntimeError: 400 · Solicitud inválida: ...` (invalid request) when sending the tools | A malformed schema (for example, a type that doesn't exist) | Print `json.dumps(TOOLS, indent=2)` and check the types (`string`, `number`, `integer`, `boolean`) and `required` |

## Challenge: a tool with an `enum`

Add `tarifa_instancia(tipo: str)` (instance rate by type) with an `enum` of three types (`"2 vCPU / 4 GB"`, `"4 vCPU / 16 GB"`, `"8 vCPU / 32 GB"`) that returns a reference hourly rate. Take the values from [NVIDIA's launchables pricing page](https://www.nvidia.com/en-us/launchables/pricing) and note the date you checked them.

**Success criteria** (live): with `tools_de("buscar_faq", "estimar_costo_brev", "tarifa_instancia")`, the question "How much does it cost to use a 4 vCPU / 16 GB instance for 8 hours?" produces **two** calls in order (`tarifa_instancia`, then `estimar_costo_brev`) and a correct final number. Also, `tarifa_instancia` with a type outside the `enum` returns an `ERROR de validación` (validation error), not an exception.

## Project milestone

**Soporte NemoClaw v3: real tools.** It now answers from the course FAQ (`buscar_faq`, citing topic and question) and calculates Brev costs (`estimar_costo_brev`), with validated arguments and errors that fix themselves. You also know how to delegate to a subagent (`consultar_experto_brev`) and how to filter tools discovered through MCP.

Add the `herramienta` decorator, `validar_args`, `ejecutar`, `agente` and the two tools to your `soporte_nemoclaw.py`. In class 3.1 you add a triage router with the categories `instalacion | api_key | brev | seguridad | otro` (installation, API key, Brev, security, other).

## Resources

- [Lesson 01c · Tools at Scale](https://nvdli.github.io/NemoClawDLI/nemoclaw/01c-tools.html), NVIDIA DLI course. This class is based on it (Apache-2.0).
- [MCP (Model Context Protocol) specification](https://modelcontextprotocol.io/specification) and its [security best practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices) guide.
- [JSON Schema specification](https://json-schema.org/specification).
- Schick et al. (2023), [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761).
- [NVIDIA launchables pricing](https://www.nvidia.com/en-us/launchables/pricing) (for `estimar_costo_brev`) and the course's [Brev FAQ (Spanish)](../../../FAQ.md#brev).
