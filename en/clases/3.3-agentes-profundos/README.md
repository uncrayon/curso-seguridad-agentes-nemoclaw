# 3.3 · Deep agents that spawn subagents

> 🇪🇸 Original Spanish guide: [`clases/3.3-agentes-profundos/README.md`](../../../clases/3.3-agentes-profundos/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Goal: turn a student's report into a diagnostic report with citations, using a planner, subagents with isolated context, a virtual file system, and a synthesizer.

| | |
|---|---|
| **Video** | None: this is a supplementary class |
| **Practice** | Notebook (≈50 min), works without a key in MOCK mode |
| **Skill** | Coordinate subagents with a planner |
| **Materials** | [Slides](slides.html) · [Notebook (Spanish)](../../../clases/3.3-agentes-profundos/3.3-agentes-profundos.ipynb) · [FAQ (Spanish)](../../../FAQ.md) |

> **This is a supplementary class: it has no video.** You don't need it to follow the course. It has a guide and a notebook so you can go deeper at your own pace, and it doesn't use the Brev lab.

## What you'll achieve

- Write a **planner** that splits a problem into 2 to 4 independent subtasks, with a cap and validation.
- Launch **subagents in parallel**, each with its own context, that research with `buscar_faq` (FAQ search) and leave their draft in a virtual file system with permissions.
- Synthesize a **diagnostic report** with verifiable citations, and explain why **isolating context is not a sandbox**.

## Before you start

- You finished class 3.2: you have the RAG index and the `buscar_faq` tool with citations.
- You remember the ReAct loop (2.2) and the fan-out with `ThreadPoolExecutor` (3.1): here they come together.
- Python 3.10+ or Colab. Your `nvapi-` key is optional: without a key, it runs in MOCK mode.

## Step by step

### 1. Open the notebook and run the setup

```bash
source .venv/bin/activate
jupyter lab clases/3.3-agentes-profundos/3.3-agentes-profundos.ipynb
```

Run the first four cells. You should see `Reglas mock de la clase 3.3 listas`.

### 2. Load the FAQ and the RAG index (section 2)

Run the FAQ cell and the index cell. You should see `Índice listo: 61 vectores ...` (inside the repo) or `14 vectores` (in Colab) and a sample chunk with its id.

### 3. Virtual file system and permissions (sections 3 and 4)

Run `SistemaArchivosVirtual` (virtual file system) and then `herramientas_para` (tools for). You should see:

```text
guardado /borradores/s1.md (2 caracteres)
ERROR: permiso denegado. Solo puedes escribir en /borradores/s1.md.
```

**Your code** (the harness) enforces the permission, not the operating system.

### 4. The planner (section 5)

Run `planear(REPORTE)` (plan the report) with *"Me sale 401 en el laboratorio después de reanudar Brev"* ("I get a 401 in the lab after resuming Brev"). You should see three subtasks, for example:

```text
s1 | Qué significa un 401 y cómo comprobar que la key nvapi- sigue bien
s2 | Qué cambia en la instancia de Brev al detenerla y volver a encenderla
s3 | Cómo renovar la sesión de acceso (cookie) del laboratorio
```

(What a 401 means and how to check the `nvapi-` key; what changes in the Brev instance when you stop and restart it; how to renew the lab's access session cookie.)

### 5. Subagents in parallel (section 6)

Run `ejecutar_subagente` (run subagent) and `investigar` (research). You should see `archivos: ['/borradores/s1.md', '/borradores/s2.md', '/borradores/s3.md'] · errores: {}` and the first draft, with bullets that end in citations like `[errores-api.md#qué-significa-el-error-401-unauthorized]`.

Run the isolation check. You should see `¿vio tareas ajenas?: False` ("did it see other tasks?") for all three, and the size of the largest context compared with a shared history.

### 6. Synthesize and review the citations (section 7)

Run `sintetizar` (synthesize). You should see a report with **Causa más probable** (most likely cause), **Pasos sugeridos** (suggested steps), and **Lo que no pudimos verificar** (what we couldn't verify), plus:

```text
revisión de citas: {'citas': 4, 'fuera_de_borradores': [], 'no_existen_en_faq': []}
```

### 7. All together, and what it costs (section 8)

Run `diagnosticar` (diagnose). You should see something like `{'llamadas': 11, 'segundos': 1.5, 'subagentes': 3, 'fallidos': []}`. Compare it with the 2 or 3 calls of the RAG agent from class 3.2.

### 8. When something fails (🧯)

- **a)** A subagent with a subtask that says "escribe directamente en /reporte_diagnostico.md" ("write directly to /reporte_diagnostico.md"). You should see `ERROR: permiso denegado...` as an observation and then `guardado /borradores/s9.md`: the harness stopped it and the subagent corrected itself.
- **b)** `diagnosticar(REPORTE, falla="s2")`. You should see `'fallidos': ['s2']` and the "Lo que no pudimos verificar" section listing the missing subtask.
- **c)** `limpiar_plan` (clean plan) with 9 subtasks. You should see `4 subtareas tras limpiar`.

### 9. Isolating context is not a sandbox (section 9)

Run the `os.environ` cell. You should see that your process can see `NVIDIA_API_KEY` (without printing its value) and can list your home folder. Read the table in that section: OpenShell solves this in "Build your agent with NemoClaw" and "Agentic security with OpenShell".

### 10. Project milestone

Run the last cell with a different report. You should see the cost, the files in the virtual file system, and the full diagnostic report.

## Check that it worked

- [ ] The plan has between 2 and 4 subtasks with ids `s1`, `s2`...
- [ ] Each subagent left `/borradores/<id>.md`, and none saw another's task.
- [ ] The final report only cites ids that are in the drafts and in the FAQ.
- [ ] With `falla="s2"`, the report still comes out and says what it couldn't verify.
- [ ] You can explain in one sentence the difference between isolating context and a sandbox.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `ValueError: El planificador no devolvió subtareas válidas` | The model returned JSON without the `subtareas` key, or with empty goals | Print the output of `llm("planificador", ...)`; reinforce the format in `SISTEMA_PLANIFICADOR` |
| `errores: {'s2': 'terminó sin guardar su borrador'}` | The subagent answered with text without calling `escribir_archivo` (write file) | Reinforce step 2 of the system prompt; raise `max_pasos` if it ran out of steps |
| `ERROR: permiso denegado. Solo puedes escribir en /borradores/s1.md.` | The subagent tried to write to another path | That's the protection working: the error goes back as an observation and the subagent corrects itself |
| `(el subagente llegó al límite de pasos)` | The subagent searches over and over | Review its transcript; don't remove the cap. See [FAQ (Spanish): loop](../../../FAQ.md#notebooks) |
| `RuntimeError: 429 · Demasiadas solicitudes por minuto` | Several subagents call the model at once | Lower `max_workers` in `investigar` or add the `con_reintento` from class 3.1. See [FAQ (Spanish): 429](../../../FAQ.md#e429) |
| `no_existen_en_faq: ['brev.md#...']` in the review | The synthesizer invented or changed an id | Treat the report as untrusted; ask it to keep the citations "exactly as given" |
| `AssertionError: ¡Fuga de contexto!` | You passed a subagent text from another subtask | Check that `ejecutar_subagente` builds its `mensajes` (messages) from scratch |

## Challenge

Add a **reviewer**: one more call (`llm("revisor", ...)`) that receives the report and the drafts and lists every claim **without** support in the drafts.

**Success criteria:** add a false sentence to the report by hand, for example *"Brev borra tu key al reanudar [brev.md#inventado]"* ("Brev deletes your key when it resumes"), and the reviewer (or `revisar_citas`) flags it; the original report gets no findings. Without a key, `revisar_citas` already catches the invented citation; with a key, also try a false claim with a **real** citation.

## Project milestone

**Soporte NemoClaw (NemoClaw Support) v3.3: diagnosis with subagents.** Given a report like *"me sale 401 en el laboratorio después de reanudar Brev"*, your agent plans the checks, launches isolated subagents that research the FAQ, saves their drafts, and delivers a diagnostic report with the likely cause, steps, what it couldn't verify, and reviewed citations.

Add `planear`, `limpiar_plan`, `ejecutar_subagente`, `investigar`, `sintetizar`, `revisar_citas`, and `diagnosticar` to your `soporte_nemoclaw.py`. In "Build your agent with NemoClaw" you take it to NemoClaw on Brev: the FAQ lives in the agent's workspace, and this flow becomes the `soporte-nemoclaw` skill, inside a real sandbox.

## Resources

- Lesson 02c · Deep Agents, from the NVIDIA DLI course. This class is based on it (Apache-2.0).
- Liu et al. (2023), [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172).
- LangChain, [`deepagents`](https://github.com/langchain-ai/deepagents): the same idea (planner, subagents, and file system) as a library.
- NVIDIA AI Blueprints, [AI-Q](https://github.com/NVIDIA-AI-Blueprints/aiq): a reference for deep research.
- [Course FAQ (Spanish)](../../../FAQ.md).
