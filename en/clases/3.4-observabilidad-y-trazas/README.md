# 3.4 · Observe and debug your agent with traces

> 🇪🇸 Original Spanish guide: [`clases/3.4-observabilidad-y-trazas/README.md`](../../../clases/3.4-observabilidad-y-trazas/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Goal: instrument your support agent with OpenTelemetry, see every step as a tree (in the notebook and in Phoenix), and use the trace, not guesswork, to find the failing tool, the stuck loop, the invented citation, and the slow step.

| | |
|---|---|
| **Video length** | ≈9 min |
| **Practice** | Notebook (≈45 min), works without a key in MOCK mode and without Phoenix |
| **Skill** | Instrument and debug agents with traces (OpenTelemetry + Phoenix) |
| **Reference** | [NeMo Agent Toolkit · Observe with Phoenix](https://docs.nvidia.com/nemo/agent-toolkit/latest/run-workflows/observe/observe-workflow-with-phoenix.html) (there's no equivalent lesson in the NVIDIA course) |
| **Materials** | [Slides](slides.html) · [Notebook (Spanish)](../../../clases/3.4-observabilidad-y-trazas/3.4-observabilidad-y-trazas.ipynb) · [FAQ (Spanish)](../../../FAQ.md#trazas) |

## What you'll achieve

- Understand **trace** and **span**, and why OpenTelemetry (OTel) is the standard: it doesn't lock you into one tool.
- **Instrument by hand** the three pieces of your agent: model calls (`LLM`), FAQ search (`RETRIEVER`), and tools (`TOOL`), inside an `AGENT` root span.
- **Debug with code** over the trace: tool errors, repetitions, unsupported citations, and the slowest step.
- **Redact secrets** before saving a trace, and export it as JSON for a bug report.
- Place NVIDIA's options: the **NeMo Agent Toolkit** (exports to Phoenix, Langfuse, LangSmith, Weave, or OTel) and **NemoClaw** sandbox observability.

## Before you start

- You finished class 3.3 and remember the ReAct loop (2.2) and `buscar_faq` (3.2).
- Python 3.10+ or Colab. Your `nvapi-` key is optional: without a key, it runs in MOCK mode.
- **Optional, to see the web UI:** Phoenix on your computer, in another terminal (requires Python 3.11+):

  ```bash
  pip install arize-phoenix
  phoenix serve
  ```

  Or with Docker: `docker run -p 6006:6006 arizephoenix/phoenix:latest`. The UI is at `http://localhost:6006`. In Colab you don't need it: the notebook draws the traces as text.

## Step by step

### 1. Open the notebook and run the setup

```bash
source .venv/bin/activate
jupyter lab clases/3.4-observabilidad-y-trazas/3.4-observabilidad-y-trazas.ipynb
```

Run the first four cells. You should see `Reglas mock de la clase 3.4 listas` (or `Modo: EN VIVO` with your key).

### 2. FAQ, index, and tracer (sections 2 and 3)

Run the FAQ, the index, and the tracer cell. You should see:

```text
Índice listo: 61 vectores de 256 dimensiones
Trazas en memoria: sí · Phoenix: no detectado (todo funciona igual, solo sin la interfaz web)
```

If you started Phoenix, the second line says `Phoenix: http://localhost:6006/v1/traces`. If you started it afterward, run that cell again.

### 3. Redact before saving (section 4)

You should see `mi key es nvapi-*** y mi cookie=***`. Every trace attribute goes through `redactar()` (redact).

### 4. Instrument and run the agent (sections 5 and 6)

Run the instrumentation and the agent with *"Me sale 401 en el laboratorio después de reanudar Brev"* ("I get a 401 in the lab after resuming Brev"). You should see the answer (expired session cookie, with citations to `conexion-laboratorio.md`) and `traza: <32 caracteres> · pasos: 3`.

### 5. Read the trace (section 7)

`ver_traza` (view trace) draws the tree:

```text
✔ AGENT     agente · soporte                 936 ms  pasos=3
├─ ✔ LLM       llm · paso 1                     310 ms  finish=tool_calls · tokens=139
├─ ✔ TOOL      tool · estado_laboratorio          0 ms  args={"instancia": "mi-lab"}
├─ ✔ LLM       llm · paso 2                     311 ms  finish=tool_calls · tokens=179
├─ ✔ TOOL      tool · buscar_faq                  4 ms  args={"consulta": "cookie de acceso vencida al reanudar el launch
│  └─ ✔ RETRIEVER retriever · buscar_faq             4 ms  docs=conexion-laboratorio.md:0.408, ...
└─ ✔ LLM       llm · paso 3                     311 ms  finish=stop · tokens=600
```

With Phoenix open: **Projects → soporte-nemoclaw**, pick the most recent trace, and walk through the same spans. Click `retriever · buscar_faq` and look for the retrieved documents with their scores.

### 6. Metrics (section 8)

You should see a table by span type (`AGENT`, `LLM`, `RETRIEVER`, `TOOL`) with spans, milliseconds, tokens, and errors. In MOCK mode the tokens are estimated.

### 7. 🧯 Debug with the trace (section 9)

- **a) The tool fails.** With `FALLAS["estado_laboratorio"] = "503"`, you should see `✖ TOOL tool · estado_laboratorio` and below it `error: ConnectionError: 503 Service Unavailable...`. The root stays ✔ because the harness turned the error into an observation, and the answer starts with *"No pude verificar el estado de tu instancia"* ("I couldn't verify the status of your instance").
- **b) The stuck loop.** With the invoice question, you should see `✖ AGENT ... error: límite de 5 pasos` and `repeticiones` (repetitions) with the same search at every step.
- **c) The invented citation.** You should see `citas sin respaldo: ['brev.md#la-gpu-es-gratis-para-siempre']` and, for the first trace, `[]`.
- **d) The slow step.** You should see `('tool · estado_laboratorio', 1507)` as the slowest span, far above the model calls.

### 8. Auto-instrumentation and NVIDIA (section 10)

Without a key, the cell says it needs the real client. With a key, it enables `OpenAIInstrumentor` and you'll see automatic `ChatCompletion` spans **inside** your `llm · paso N` spans. Read the table of NVIDIA options and the NeMo Agent Toolkit YAML.

### 9. A trace is sensitive data (section 11)

You should see `¿la key quedó en la traza?: False` and the question with `nvapi-***`.

### 10. Project milestone (section 12)

You should see the answer to *"¿Por qué mi notebook responde HTTP 401...?"* ("Why does my notebook return HTTP 401...?"), `problemas: {'citas_sin_respaldo': [], 'repeticiones': {}, 'errores': []}`, and the path `trazas/<id>.json`.

## Check that it worked

- [ ] `ver_traza` shows a tree with `AGENT`, `LLM`, `TOOL`, and `RETRIEVER`.
- [ ] You found the ✖ span in case **a** and read the exact error.
- [ ] `repeticiones` found the loop in case **b**, and you know how to cut it in the harness.
- [ ] `citas_sin_respaldo` (unsupported citations) detected the invented citation in case **c**.
- [ ] `mas_lentos` (slowest) pointed to the tool, not the model, in case **d**.
- [ ] The fake key from section 11 doesn't appear in any attribute.
- [ ] (Optional) You saw your traces in Phoenix, in the `soporte-nemoclaw` project.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `Phoenix: no detectado` even though `phoenix serve` is running | You ran the tracer cell before starting Phoenix, or Phoenix uses another port | Run the tracer cell again. If you use another port or a remote Phoenix: `export PHOENIX_COLLECTOR_ENDPOINT=http://<host>:<puerto>` |
| The Phoenix UI doesn't show new traces | Traces are sent in batches (`BatchSpanProcessor`), or you're looking at another project | `agente()` already calls `PROVEEDOR.force_flush()`; refresh and pick the **soporte-nemoclaw** project |
| `pip install arize-phoenix` fails with a Python version error | Phoenix requires Python 3.11 or later | Use Docker (`arizephoenix/phoenix`) or an environment with Python 3.11+. The notebook works the same without Phoenix |
| `Overriding of current TracerProvider is not allowed` | Other code called `trace.set_tracer_provider` twice | The notebook doesn't use the global provider; if you mix it with another library, restart the kernel |
| `ModuleNotFoundError: No module named 'opentelemetry'` | The tracer cell couldn't install the SDK | `pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http` and restart the kernel |
| `401 Unauthorized` when exporting to a remote Phoenix | That Phoenix has authentication | Set `PHOENIX_API_KEY` before the tracer cell. `[VERIFY IN LAB]` the header format with your deployment |
| The trace shows your key or your cookie | You set an attribute without going through `poner()` (set) | Always use `poner(span, ...)`; add the missing pattern to `_SECRETOS` |
| Live, cases b and c come out "clean" | The real model didn't repeat the search or invent the citation this time | That's normal: the review functions still work. In MOCK mode the errors always reproduce |

## Challenge

**Cut the loop in the harness.** Modify `ejecutar_herramienta` (run tool) so that, if a tool receives **the same arguments** as in the previous call, it doesn't run it and returns: *"Ya buscaste esto y no hubo evidencia nueva. Responde con lo que tienes o di que la FAQ no lo cubre."* ("You already searched for this and there was no new evidence. Answer with what you have or say the FAQ doesn't cover it.")

**Success criteria:** run case **b** again. In the trace, the `RETRIEVER` span appears **only once** (the real search), and the repeated `TOOL` spans carry the new observation in `output.value`. In MOCK mode the agent still hits the cap (its rules are fixed); with a key, the real model should answer as soon as it reads the observation.

## Project milestone

**Soporte NemoClaw (NemoClaw Support) v3.4: every answer with its trace.** `soporte_nemoclaw(pregunta)` returns the answer, the trace, an automatic review (`citas_sin_respaldo`, `repeticiones`, `errores`), and a redacted JSON in `trazas/`. Add `redactar`, `poner`, `llamar_trazado`, `buscar_faq_trazado`, `ejecutar_herramienta`, `ver_traza`, and `exportar_traza` to your `soporte_nemoclaw.py`.

In Module 4 your agent moves to NemoClaw: there, observability has two layers, the agent's (traces) and the sandbox's (OpenShell logs, sessions, and blocks). In class 4.4 you trace calls to Hermes with this same code.

## Resources

- [OpenTelemetry · Trace concepts](https://opentelemetry.io/docs/concepts/signals/traces/)
- [OpenInference · Semantic conventions](https://github.com/Arize-ai/openinference/tree/main/spec) (the `openinference.span.kind` values and the `llm.*`, `retrieval.*`, `tool.*` attributes)
- [Arize Phoenix · Documentation](https://arize.com/docs/phoenix) and [repository](https://github.com/Arize-ai/phoenix) (open source)
- [NVIDIA NeMo Agent Toolkit · Observe workflows](https://docs.nvidia.com/nemo/agent-toolkit/latest/run-workflows/observe/observe.html) and [with Phoenix](https://docs.nvidia.com/nemo/agent-toolkit/latest/run-workflows/observe/observe-workflow-with-phoenix.html)
- [NemoClaw · Monitor sandbox activity](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/monitoring/monitor-sandbox-activity) and [export Deep Agents traces](https://docs.nvidia.com/nemoclaw/latest/user-guide/deepagents/monitoring/set-up-deepagents-trace-export)
- [Course FAQ (Spanish)](../../../FAQ.md#trazas)
