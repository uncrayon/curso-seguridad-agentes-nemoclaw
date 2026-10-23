# 3.1 · Route work across multiple calls

> 🇪🇸 Original Spanish guide: [`clases/3.1-enrutamiento-y-workflows/README.md`](../../../clases/3.1-enrutamiento-y-workflows/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Goal: make your code, not the model, own the shape of the work: a triage router with a fixed enum, a parallel ReWOO pipeline, and a fan-out that survives a failed branch.

| | |
|---|---|
| **Video** | None: this is supplementary material |
| **Practice** | Notebook (≈50 min), works without a key in MOCK mode |
| **Skill** | Route subtasks across model calls |
| **Materials** | [Slides](slides.html) · [Notebook (Spanish)](../../../clases/3.1-enrutamiento-y-workflows/3.1-enrutamiento-y-workflows.ipynb) · [FAQ (Spanish)](../../../FAQ.md) |

> **This class is supplementary material: it has no video.** You don't need it to follow the course. It has a guide and a notebook so you can go deeper at your own pace, and it doesn't use the Brev lab.

## What you'll achieve

- Classify student tickets with a **closed enum** (`instalacion | api_key | brev | seguridad | otro`, that is, installation, API key, Brev, security, other), validate the JSON, and decide what to do when the model makes up a label.
- Build a **ReWOO** pipeline: plan once, run searches in parallel with `concurrent.futures`, and synthesize once, measuring the latency of each phase.
- Do **fan-out / fan-in** to several specialists, isolate the branch that fails, retry only what is retryable, and know when **not** to split.

## Before you start

- You finished class 2.3: you know a tool is a contract and that errors go back to the model as text.
- Python 3.10+ or Colab. Your `nvapi-` key is optional: without a key, the notebook uses the simulated model (MOCK).
- If you work locally, the environment from [class 2.1](../2.1-loop-de-agente/README.md) already has everything you need (`openai`, `python-dotenv`).

## Step by step

### 1. Open the notebook and run the setup

```bash
source .venv/bin/activate
jupyter lab clases/3.1-enrutamiento-y-workflows/3.1-enrutamiento-y-workflows.ipynb
```

In Colab: **File → Upload notebook**, and save your key in Secrets as `NVIDIA_API_KEY`.

Run the first four cells (setup, client, helpers, and mock rules). You should see:

```text
Modo: EN VIVO · nvidia/nemotron-3.5-lightning-30b-a3b      (o "Modo: MOCK ...")
Cliente listo: https://integrate.api.nvidia.com/v1
Ayudas listas: llm(), llamar(), extraer_json(), ErrorSimulado
Reglas mock de la clase 3.1 listas
```

### 2. Define the enum and the validator (section 2)

Run the cell with `CATEGORIAS` (categories), `ESQUEMA_TRIAGE` (triage schema), and `validar_triage` (validate triage). You should see:

```text
[]
["categoria inválida: 'facturacion'"]
```

An empty list means "valid". The second line is what happens when the model invents a category (`facturacion` means billing).

### 3. Classify with a retry

Run the `clasificar` (classify) cell. Notice the order:

1. Ask for JSON with `response_format` and the schema (if the route doesn't accept it and returns 400, continue with the prompt alone).
2. Extract the JSON even if it comes wrapped in prose.
3. Validate. If it fails, make **one** retry that shows the model its error. If it fails again, use `otro`.

You should see `intento 1: ... -> OK` and a dictionary with `'categoria': 'api_key'`.

### 4. Router and specialists

Run the cell with `crear_especialista` (create specialist) and `soporte` (support). It goes through six tickets. Look for these two cases in the output:

```text
   intento 1: 'Claro, esta es la clasificación:\n{"categoria": "brev", ...' -> OK
   ...
   intento 1: '{"categoria": "facturacion", ...' -> ["categoria inválida: 'facturacion'"]
   intento 2: '{"categoria": "otro", ...' -> OK
→ otro        baja  intentos=2 | Quiero un reembolso, me hicieron un cobro doble
```

The router is a dictionary: `ESPECIALISTAS[t["categoria"]]`. It never fails because you validated first. Do the **✏️ Tu turno** (Your turn) exercise with three tickets of your own, one of them ambiguous.

### 5. ReWOO: plan → run in parallel → synthesize (section 3)

Run the FAQ cell (it loads the sample or, inside the repo, the full `datos/faq/`), and then the cell with `planear` (plan), `ejecutar` (execute), and `sintetizar` (synthesize). You should see something like this:

```text
   (el plan traía 5 consultas; lo recorto a 4)
PLAN (cada consulta → la entrada que encontró):
   'cómo detener la instancia de brev'            → brev.md#cómo-detengo-o-borro-mi-instancia
   'session expired en el laboratorio'            → conexion-laboratorio.md#me-sale-session-expired-or-unreachable
   ...
llamadas al modelo: 2 ['planificador', 'sintetizador']
```

Two model calls, no matter how many searches the plan has.

### 6. Measure the latency

Run the bar-chart cell. You should see the parallel searches (≈0.5 s) against the serial ones (≈2 s). In live mode, look at how much of the total the planner and the synthesizer take: if each one takes 5 s, saving 1.5 s on searches barely shows.

### 7. Fan-out with a failing branch (section 4)

Run the `fan_out` cell. You should see:

```text
  api_key    0.31s ███
  brev       0.31s ███
  seguridad  FALLÓ → TimeoutError: el especialista no respondió a tiempo (simulado)
```

And a joined answer that ends with "Ojo: falta la revisión de seguridad; esta respuesta puede estar incompleta." (a warning that the security review is missing and the answer may be incomplete).

### 8. Compare with a single call (section 5)

Run the `generalista` (generalist) cell. Compare calls and seconds: 1 call against 4. Read the "Divide cuando… / NO dividas cuando…" (Split when… / DON'T split when…) table.

### 9. When something fails (🧯)

- **a)** Run `SALIDAS_MALAS` (bad outputs). You should see that `"Brev"` with a capital letter and the truncated JSON (`{"categoria": "brev", "prio`) are rejected.
- **b)** Run `rama_con_429` (branch with 429): the `seguridad` branch gets a 429 and you'll see the diagnosis `429 · Demasiadas solicitudes por minuto...`. Then run `con_reintento` (with retry): `429 en seguridad (intento 1): espero 0.5s y reintento` and all three branches OK.

### 10. Project milestone

Run `soporte_nemoclaw`. A simple ticket goes to one specialist; the 401 report gets high priority and goes through the fan-out.

## Check that it worked

- [ ] `validar_triage` rejects `facturacion`, `Brev` with a capital letter, and the truncated JSON.
- [ ] The refund ticket ends up in `otro` after 2 attempts and doesn't break the pipeline.
- [ ] ReWOO makes exactly 2 model calls, and the parallel searches take less time than the serial ones.
- [ ] The fan-out delivers an answer even when `seguridad` fails, and the answer says so.
- [ ] With `con_reintento`, the 429 recovers, and a 401 would not be retried.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `["categoria inválida: 'facturacion'"]` (or any label outside the list) | The model invented a category, or the route didn't apply the schema | This is expected: the retry shows the model its error and, if it insists, the ticket goes to `otro`. Never map synonyms by hand |
| `JSON ilegible (ValueError)` or `JSONDecodeError` | The model added prose with no JSON, or `finish_reason=length` cut the JSON off | `extraer_json` (extract JSON) rescues the prose; for the cutoff, raise `max_tokens`. See [FAQ (Spanish): length](../../../FAQ.md#elength) |
| `RuntimeError: 400 · Solicitud inválida` when classifying | The route or the model doesn't accept `response_format` with `json_schema` | `_pedir_triage` retries without a schema; your validator still protects you |
| `RuntimeError: 429 · Demasiadas solicitudes por minuto` in one branch | You launched too many calls in parallel | Lower `max_workers` and wrap the branch with `con_reintento`. See [FAQ (Spanish): 429](../../../FAQ.md#e429) |
| `KeyError: 'facturacion'` when calling the specialist | You used the model's label without validating it | Call `clasificar` (which validates) before the router |
| `ValueError: max_workers must be greater than 0` | The plan came back empty and `ThreadPoolExecutor` got 0 threads | `planear` already raises a clear error if there are no queries; check what the planner returned |
| ReWOO gives a nonsense answer at step 2 | Step 2 depended on the result of step 1 | ReWOO doesn't fit there: use ReAct or a loop inside that stage |

## Challenge

Add the **`costos`** (costs) category (Brev credits and pricing; in class 2.3 you built `estimar_costo_brev`, the Brev cost estimator): add it to `CATEGORIAS`, to the `SISTEMA_TRIAGE` prompt, and to `ESPECIALISTAS`, and write 3 cost tickets and 1 ambiguous one.

**Success criteria:** all 3 cost tickets reach `costos`, the refund ticket still falls into `otro` through validation, and no ticket breaks the pipeline. Without a key, add a rule to the mock; with a key, test it live.

## Project milestone

**Soporte NemoClaw (NemoClaw Support) v3.1: triage + specialists.** Your agent no longer answers everything with the same prompt: it classifies each ticket into `instalacion | api_key | brev | seguridad | otro`, validates the label, and sends it to the right specialist. If the ticket is urgent, it runs the fan-out and joins the reviews, saying what was missing.

Add `clasificar`, `validar_triage`, `ESPECIALISTAS`, `fan_out`, `unir` (join), and `con_reintento` to your `soporte_nemoclaw.py`. In class 3.2, the specialists stop answering from memory: you give them RAG over the FAQ, with citations.

## Resources

- Lesson 02a · The Workflow Agent, from the NVIDIA DLI course. This class is based on it (Apache-2.0).
- Xu et al. (2023), [ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models](https://arxiv.org/abs/2305.18323).
- Yao et al. (2022), [ReAct](https://arxiv.org/abs/2210.03629), for comparison.
- Python documentation: [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html).
- [Course FAQ (Spanish)](../../../FAQ.md#errores-api) and the [`datos/faq/`](../../../datos/faq/) corpus.
