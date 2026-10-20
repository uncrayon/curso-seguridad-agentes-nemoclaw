# 3.2 · RAG to ground answers in your sources

> 🇪🇸 Original Spanish guide: [`clases/3.2-rag/README.md`](../../../clases/3.2-rag/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Goal: make Soporte NemoClaw (NemoClaw Support) answer from the course FAQ, cite every claim as `[archivo#pregunta]` (`[file#question]`), and say "I don't know" when there's no evidence.

| | |
|---|---|
| **Video length** | ≈9 min |
| **Practice** | Notebook (≈50 min), works without a key in MOCK mode |
| **Skill** | Implement RAG with your own sources |
| **NVIDIA lesson** | [02b · The Index Agent](https://nvdli.github.io/NemoClawDLI/nemoclaw/02b-rag.html) |
| **Materials** | [Slides](slides.html) · [Notebook (Spanish)](../../../clases/3.2-rag/3.2-rag.ipynb) · [FAQ (Spanish)](../../../FAQ.md) · [`datos/faq/` corpus (Spanish)](../../../datos/faq/) |

## What you'll achieve

- Chunk the FAQ by entry (`## P:`), request embeddings with `input_type="passage"` and `"query"`, and search top-K by cosine similarity, in about 25 lines.
- Write a prompt that forces the model to cite `[archivo#pregunta]` and to say "I don't know" without evidence, and check the citations with code.
- Measure retrieval with **Hit@k** and expose it as a **tool** the agent decides when to call.

## Before you start

- You finished class 3.1: you have the Soporte NemoClaw router and specialists.
- Python 3.10+ or Colab. Your `nvapi-` key is optional: without a key, it runs in MOCK mode with a simulated embedding.
- With a key, the embeddings route uses `nvidia/nemotron-3-embed-1b` at `https://integrate.api.nvidia.com/v1` (you set it up in class 1.3).

## Step by step

### 1. Open the notebook and run the setup

```bash
source .venv/bin/activate
jupyter lab clases/3.2-rag/3.2-rag.ipynb
```

Run the first four cells. You should see `Modo: EN VIVO · ...` (or `Modo: MOCK ...`) and `Reglas mock de la clase 3.2 listas`.

### 2. Load and chunk the FAQ (sections 1 and 2)

Run the FAQ cell. Inside the repo you should see `FAQ: datos/faq completa (9 archivos) · 61 entradas`; in Colab, `FAQ: muestra incrustada (7 archivos) · 14 entradas`. The exact numbers change if someone edits the FAQ.

Run the chunks cell. Each chunk has a citable `id`:

```text
id      : api-key.md#dónde-consigo-mi-api-key-de
tema    : API key de NVIDIA Build
pregunta: ¿Dónde consigo mi API key de NVIDIA para el curso?
```

### 3. Request an embedding (section 3)

Run the `embed(..., input_type="passage")` cell. You should see the model, the dimensions, the first values, and the norm. In live mode, `nemotron-3-embed-1b` sets the dimensions (the NVIDIA lesson reports 2048); without a key, the simulated vector has 4096 positions.

### 4. Build the index and search (section 4)

Run the `Indice` (index) class. You should see the top three chunks for each question:

```text
🔎 la cookie del laboratorio venció: session expired
   0.345  conexion-laboratorio.md#me-sale-session-expired-or-unreachable
   ...
🔎 ¿cuál es la capital de Perú?
   0.000  ...
```

Top-K **always** returns K results, even when they're garbage. That's why `MIN_SCORE` exists.

### 5. Generate with citations and "I don't know" (section 5)

Run `responder` (answer). You should see an answer that ends with `[conexion-laboratorio.md#me-sale-session-expired-or-unreachable]` and, for the capital of Peru, `No sé con base en la FAQ del curso. (ningún fragmento superó el umbral)` ("I don't know based on the course FAQ; no chunk passed the threshold"): the model wasn't even called.

Do the **✏️ Tu turno** (Your turn) exercise with "Reanudé Brev y el laboratorio me da 401" ("I resumed Brev and the lab gives me a 401"): the answer is spread across several entries. Class 3.3 solves that.

### 6. Measure with Hit@k (section 6)

Run `evaluar` (evaluate). You should see one line per question (✅ rank 1, 🟡 rank 2-3, ❌ not found) and something like `Hit@1 = 0.88 · Hit@3 = 1.00` without a key. In live mode, write down your numbers: they're your baseline.

### 7. RAG as a tool (section 7)

Run the `agente` (agent). You should see that with "¡Hola!" it does **not** search (`búsquedas: ninguna`), with the lab question it searches and cites, and with the capital of Peru it gets `SIN_EVIDENCIA` (no evidence) and says it doesn't know.

### 8. When something fails (🧯)

- **a)** Run the cell without `input_type`. You should see `422 · Argumentos con formato incorrecto (p. ej. falta input_type en embeddings ...)`.
- **b)** Run `EVAL_EN`. You should see Hit@k drop with English questions over a Spanish FAQ (by a lot without a key).
- **c)** Run `GRANDES` (large). You should see that when you index whole files, the context more than doubles and the citation no longer says which entry it came from.

### 9. Project milestone

Run `soporte_nemoclaw`. You should see a cited answer and the line `[búsquedas: [...] · citas: 1]`.

### 10. (Optional) Practice in the browser with the NVIDIA lesson

In [lesson 02b](https://nvdli.github.io/NemoClawDLI/nemoclaw/02b-rag.html), with your chat and embeddings routes configured:

1. In **Inspect one embedding**, change `const EXAMPLE = 0;` to `1` and compare the values: the same idea phrased as a question.
2. In **Build an in-memory vector index**, node **User query**, type a question of your own and look at the top-3 scores.
3. In **Expose retrieval as an agent tool**, try `"What is 12 times 8?"`: the agent shouldn't search.
4. In **Try it · retrieval, live**, ask "What does the OpenShell sandbox do?".

`[VERIFY IN LAB]` the cell names.

## Check that it worked

- [ ] Each chunk has an `archivo.md#pregunta` id, and none repeats.
- [ ] The off-topic question answers "I don't know" **without** calling the model.
- [ ] `verificar_citas` (verify citations) shows `inventadas: []` (invented) for your answers.
- [ ] You wrote down your Hit@1 and Hit@3 (without a key and, if you can, live).
- [ ] The agent doesn't search for a greeting and does search for a technical question.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `RuntimeError: 422 · Argumentos con formato incorrecto (p. ej. falta input_type en embeddings ...)` | You called the embeddings API without `input_type` | Use `embed(textos, input_type="passage")` to index and `"query"` to search. See [FAQ (Spanish): 422](../../../FAQ.md#errores-api) |
| Low Hit@k with no error at all | You swapped `query` and `passage`, or the questions are in a different language than the FAQ | Check `input_type` in both calls; write the FAQ in your users' language or translate the question before searching |
| Everything answers "No sé con base en la FAQ del curso." | `MIN_SCORE` is too high for your embeddings model | Print the scores of good and bad questions and set the threshold between them |
| The agent answers with facts that aren't in the FAQ | Threshold too low, or the prompt is missing the "context only" rule | Raise `MIN_SCORE`, keep the 4 rules in `SISTEMA_RAG`, and check `verificar_citas` |
| `inventadas: ['brev.md#...']` | The model wrote an id you didn't give it | Ask it to copy the id "exactly as given" and treat that answer as untrusted |
| The answer ignores the end of a long entry | `truncate="END"` silently cut the chunk | Chunk by entry; no FAQ entry should go past a few hundred words |
| `RuntimeError: 404 · Ese modelo o esa ruta no existen` when indexing | `EMBED_MODEL` is misspelled, or you used a chat route instead of an embeddings route | Use `nvidia/nemotron-3-embed-1b` and a `BASE_URL` ending in `/v1`. See [FAQ (Spanish)](../../../FAQ.md#errores-api) |
| `FAQ: muestra incrustada` even though you're in the repo | The notebook isn't running from `clases/3.2-rag/` | Open it from its folder; the path is `../../datos/faq` |

## Challenge

Add **3 entries of your own** to the FAQ (in `FAQ_MUESTRA` or in `datos/faq/`), using the `## P:` format, and write **4 test questions** for them in `EVAL`.

**Success criteria:** Hit@1 ≥ 0.75 on your 4 questions, every agent answer cites at least one id that exists (`inventadas` is empty), and the agent says "I don't know" to a question outside the FAQ.

## Project milestone

**Soporte NemoClaw v3.2: RAG with citations.** Your agent now answers from the course FAQ, cites every claim with `[archivo#pregunta]`, checks its citations, and says "I don't know" when there's no evidence. Search is a tool: the agent decides when to use it.

Add `Indice`, `responder`, `buscar_faq` (FAQ search, the embeddings version), `verificar_citas`, and `agente` to your `soporte_nemoclaw.py`. In class 3.3, a planner gives this tool to several subagents to build a diagnostic report.

## Resources

- [Lesson 02b · The Index Agent](https://nvdli.github.io/NemoClawDLI/nemoclaw/02b-rag.html), from the NVIDIA DLI course. This class is based on it (Apache-2.0).
- Lewis et al. (2020), [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401).
- NVIDIA Build model catalog: [build.nvidia.com](https://build.nvidia.com) (search for `nemotron-3-embed-1b`).
- Edge et al. (2024), [From Local to Global: A Graph RAG Approach](https://arxiv.org/abs/2404.16130), for when top-K isn't enough.
- [Course FAQ (Spanish)](../../../FAQ.md) and the [`datos/faq/`](../../../datos/faq/) corpus.
