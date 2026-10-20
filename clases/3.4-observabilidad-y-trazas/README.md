# 3.4 · Observa y depura tu agente con trazas

Objetivo: instrumentar tu agente de soporte con OpenTelemetry, ver cada paso como un árbol (en el notebook y en Phoenix) y encontrar con la traza, no a ojo, la herramienta que falla, el loop atascado, la cita inventada y el paso lento.

| | |
|---|---|
| **Duración del video** | ≈9 min |
| **Práctica** | Notebook (≈45 min), funciona sin key en modo MOCK y sin Phoenix |
| **Habilidad** | Instrumentar y depurar agentes con trazas (OpenTelemetry + Phoenix) |
| **Referencia** | [NeMo Agent Toolkit · Observar con Phoenix](https://docs.nvidia.com/nemo/agent-toolkit/latest/run-workflows/observe/observe-workflow-with-phoenix.html) (no hay lección equivalente en el curso de NVIDIA) |
| **Material** | [Diapositivas](slides.html) · [Notebook](3.4-observabilidad-y-trazas.ipynb) · [Preguntas frecuentes](../../FAQ.md#trazas) |

## Lo esencial (sin tecnicismos)

**La idea:** Cuando un agente responde mal, la pregunta es en qué paso se equivocó. Una traza guarda cada paso que dio (cada pregunta al modelo, cada herramienta, cada búsqueda) con cuánto tardó y si salió bien o mal. Así encuentras el paso exacto que falló, que tardó o que inventó algo, sin adivinar. Y antes de guardarla, se tachan las contraseñas.

**Piénsalo como:** el historial de rastreo de un paquete: dónde estuvo, cuándo y si hubo un problema.

**Palabras nuevas:** [traza](../../GLOSARIO.md), [span](../../GLOSARIO.md), [Phoenix](../../GLOSARIO.md).

**Hazlo sin programar (≈10 min):** Lee esta traza, tal como la dibuja el notebook. Cada línea es un paso; ✔ es "salió bien", ✖ es "hubo un error" y ms son milésimas de segundo. Responde: (1) ¿qué paso falló?; (2) según la línea de `error`, ¿por qué falló?; (3) la primera línea tiene ✔: ¿el agente se detuvo o siguió?, y ¿qué debería decirle al estudiante en su respuesta? Para confirmar, abre el notebook en Google Colab (menú **Archivo → Subir notebook**), presiona ▶ en cada celda en orden, sin leer el código, y busca la misma traza en la sección 9, parte a).

```text
✔ AGENT     agente · soporte                  952 ms  pasos=3
├─ ✔ LLM       llm · paso 1                     310 ms  finish=tool_calls · tokens=141
├─ ✖ TOOL      tool · estado_laboratorio          1 ms  args={"instancia": "mi-lab"}
│     └ error: ConnectionError: 503 Service Unavailable desde la API de Brev (simulado)
├─ ✔ LLM       llm · paso 2                     312 ms  finish=tool_calls · tokens=176
├─ ✔ TOOL      tool · buscar_faq                  4 ms  args={"consulta": "cookie de acceso vencida al reanudar el launch
│  └─ ✔ RETRIEVER retriever · buscar_faq             4 ms  docs=conexion-laboratorio.md:0.408, ...
└─ ✔ LLM       llm · paso 3                     318 ms  finish=stop · tokens=590
```

**Qué te llevas:** Puedes leer el recorrido de un agente paso por paso y señalar dónde falló, en lugar de adivinar o culpar al modelo.

## Lo que vas a lograr

- Entender **traza** y **span**, y por qué OpenTelemetry (OTel) es el estándar: no te amarra a una herramienta.
- **Instrumentar a mano** las tres piezas de tu agente: llamadas al modelo (`LLM`), búsqueda en la FAQ (`RETRIEVER`) y herramientas (`TOOL`), dentro de un span raíz `AGENT`.
- **Depurar con código** sobre la traza: errores de herramientas, repeticiones, citas sin respaldo y el paso más lento.
- **Tachar los secretos** (con la función `redactar`) antes de guardar una traza y exportarla en JSON para un reporte de error.
- Ubicar las opciones de NVIDIA: el **NeMo Agent Toolkit** (exporta a Phoenix, Langfuse, LangSmith, Weave u OTel) y la observabilidad del sandbox de **NemoClaw**.

## Antes de empezar

- Terminaste la clase 3.3 y recuerdas el loop ReAct (2.2) y `buscar_faq` (3.2).
- Python 3.10+ o Colab. Tu key `nvapi-` es opcional: sin key corre en MOCK.
- **Opcional, para ver la interfaz web:** Phoenix en tu computadora, en otra terminal (requiere Python 3.11+):

  ```bash
  pip install arize-phoenix
  phoenix serve
  ```

  O con Docker: `docker run -p 6006:6006 arizephoenix/phoenix:latest`. La interfaz queda en `http://localhost:6006`. En Colab no la necesitas: el notebook dibuja las trazas en texto.

## Paso a paso

### 1. Abre el notebook y ejecuta la configuración

```bash
source .venv/bin/activate
jupyter lab clases/3.4-observabilidad-y-trazas/3.4-observabilidad-y-trazas.ipynb
```

Ejecuta las cuatro primeras celdas. Deberías ver `Reglas mock de la clase 3.4 listas` (o `Modo: EN VIVO` con tu key).

### 2. FAQ, índice y tracer (secciones 2 y 3)

Ejecuta la FAQ, el índice y la celda del tracer. Deberías ver:

```text
Índice listo: 61 vectores de 256 dimensiones
Trazas en memoria: sí · Phoenix: no detectado (todo funciona igual, solo sin la interfaz web)
```

Si levantaste Phoenix, la segunda línea dice `Phoenix: http://localhost:6006/v1/traces`. Si lo levantaste después, vuelve a ejecutar esa celda.

### 3. Tacha los secretos antes de guardar (sección 4)

Deberías ver `mi key es nvapi-*** y mi cookie=***`. Todo atributo de una traza pasa por `redactar()`.

### 4. Instrumenta y corre el agente (secciones 5 y 6)

Ejecuta la instrumentación y el agente con *"Me sale 401 en el laboratorio después de reanudar Brev"*. Deberías ver la respuesta (cookie de sesión vencida, con citas a `conexion-laboratorio.md`) y `traza: <32 caracteres> · pasos: 3`.

### 5. Lee la traza (sección 7)

`ver_traza` dibuja el árbol:

```text
✔ AGENT     agente · soporte                 936 ms  pasos=3
├─ ✔ LLM       llm · paso 1                     310 ms  finish=tool_calls · tokens=139
├─ ✔ TOOL      tool · estado_laboratorio          0 ms  args={"instancia": "mi-lab"}
├─ ✔ LLM       llm · paso 2                     311 ms  finish=tool_calls · tokens=179
├─ ✔ TOOL      tool · buscar_faq                  4 ms  args={"consulta": "cookie de acceso vencida al reanudar el launch
│  └─ ✔ RETRIEVER retriever · buscar_faq             4 ms  docs=conexion-laboratorio.md:0.408, ...
└─ ✔ LLM       llm · paso 3                     311 ms  finish=stop · tokens=600
```

Con Phoenix abierto: **Projects → soporte-nemoclaw**, elige la traza más reciente y recorre los mismos spans. Haz clic en `retriever · buscar_faq` y busca los documentos recuperados con su puntaje.

### 6. Métricas (sección 8)

Deberías ver una tabla por tipo de span (`AGENT`, `LLM`, `RETRIEVER`, `TOOL`) con spans, milisegundos, tokens y errores. En MOCK los tokens son estimados.

### 7. 🧯 Depura con la traza (sección 9)

- **a) La herramienta falla.** Con `FALLAS["estado_laboratorio"] = "503"`, deberías ver `✖ TOOL tool · estado_laboratorio` y debajo `error: ConnectionError: 503 Service Unavailable...`. La raíz queda en ✔ porque el harness convirtió el error en observación, y la respuesta empieza con *"No pude verificar el estado de tu instancia"*.
- **b) El loop atascado.** Con la pregunta de la factura, deberías ver `✖ AGENT ... error: límite de 5 pasos` y `repeticiones` con la misma búsqueda en cada paso.
- **c) La cita inventada.** Deberías ver `citas sin respaldo: ['brev.md#la-gpu-es-gratis-para-siempre']` y, para la primera traza, `[]`.
- **d) El paso lento.** Deberías ver `('tool · estado_laboratorio', 1507)` como el span más lento, muy por encima de las llamadas al modelo.

### 8. Auto-instrumentación y NVIDIA (sección 10)

Sin key, la celda dice que necesita el cliente real. Con key, activa `OpenAIInstrumentor` y verás spans `ChatCompletion` automáticos **dentro** de tus spans `llm · paso N`. Lee la tabla de opciones de NVIDIA y el YAML del NeMo Agent Toolkit.

### 9. Una traza es un dato sensible (sección 11)

Deberías ver `¿la key quedó en la traza?: False` y la pregunta con `nvapi-***`.

### 10. Avance del proyecto (sección 12)

Deberías ver la respuesta a *"¿Por qué mi notebook responde HTTP 401...?"*, `problemas: {'citas_sin_respaldo': [], 'repeticiones': {}, 'errores': []}` y la ruta `trazas/<id>.json`.

## Comprueba que funcionó

- [ ] `ver_traza` muestra un árbol con `AGENT`, `LLM`, `TOOL` y `RETRIEVER`.
- [ ] Ubicaste el span con ✖ del caso **a** y leíste el error exacto.
- [ ] `repeticiones` encontró el loop del caso **b** y sabes cómo cortarlo en el harness.
- [ ] `citas_sin_respaldo` detectó la cita inventada del caso **c**.
- [ ] `mas_lentos` apuntó a la herramienta, no al modelo, en el caso **d**.
- [ ] La key falsa de la sección 11 no aparece en ningún atributo.
- [ ] (Opcional) Viste tus trazas en Phoenix, en el proyecto `soporte-nemoclaw`.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `Phoenix: no detectado` aunque `phoenix serve` está corriendo | Ejecutaste la celda del tracer antes de levantar Phoenix, o Phoenix usa otro puerto | Vuelve a ejecutar la celda del tracer. Si usas otro puerto o un Phoenix remoto: `export PHOENIX_COLLECTOR_ENDPOINT=http://<host>:<puerto>` |
| La interfaz de Phoenix no muestra trazas nuevas | Las trazas van en lotes (`BatchSpanProcessor`) o miras otro proyecto | `agente()` ya llama a `PROVEEDOR.force_flush()`; refresca y elige el proyecto **soporte-nemoclaw** |
| `pip install arize-phoenix` falla con un error de versión de Python | Phoenix requiere Python 3.11 o mayor | Usa Docker (`arizephoenix/phoenix`) o un entorno con Python 3.11+. El notebook funciona igual sin Phoenix |
| `Overriding of current TracerProvider is not allowed` | Otro código llamó a `trace.set_tracer_provider` dos veces | El notebook no usa el proveedor global; si lo mezclas con otra librería, reinicia el kernel |
| `ModuleNotFoundError: No module named 'opentelemetry'` | La celda del tracer no pudo instalar el SDK | `pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http` y reinicia el kernel |
| `401 Unauthorized` al exportar a un Phoenix remoto | El Phoenix tiene autenticación | Define `PHOENIX_API_KEY` antes de la celda del tracer. `[VERIFICAR EN LAB]` el formato de la cabecera con tu despliegue |
| La traza muestra tu key o tu cookie | Pusiste un atributo sin pasar por `poner()` | Usa siempre `poner(span, ...)`; agrega el patrón que falte en `_SECRETOS` |
| En vivo, los casos b y c salen "limpios" | El modelo real no repitió la búsqueda ni inventó la cita esta vez | Es normal: las funciones de revisión siguen sirviendo. En MOCK los errores siempre se reproducen |

## Reto

**Corta el loop en el harness.** Modifica `ejecutar_herramienta` para que, si una herramienta recibe **los mismos argumentos** que en la llamada anterior, no la ejecute y devuelva: *"Ya buscaste esto y no hubo evidencia nueva. Responde con lo que tienes o di que la FAQ no lo cubre."*

**Criterio de éxito:** vuelve a correr el caso **b**. En la traza, el span `RETRIEVER` aparece **una sola vez** (la búsqueda real) y los `TOOL` repetidos traen la observación nueva en `output.value`. En MOCK el agente igual llega al tope (sus reglas son fijas); con key, el modelo real debería responder en cuanto lee la observación.

## Avance del proyecto

**Soporte NemoClaw v3.4: cada respuesta con su traza.** `soporte_nemoclaw(pregunta)` devuelve la respuesta, la traza, una revisión automática (`citas_sin_respaldo`, `repeticiones`, `errores`) y un JSON con los secretos tachados en `trazas/`. Agrega `redactar`, `poner`, `llamar_trazado`, `buscar_faq_trazado`, `ejecutar_herramienta`, `ver_traza` y `exportar_traza` a tu `soporte_nemoclaw.py`.

En el Módulo 4 tu agente se va a NemoClaw: ahí la observabilidad tiene dos capas, la del agente (trazas) y la del sandbox (logs, sesiones y bloqueos de OpenShell). En la clase 4.4 trazas con este mismo código las llamadas a Hermes.

## Recursos

- [OpenTelemetry · Conceptos de trazas](https://opentelemetry.io/docs/concepts/signals/traces/)
- [OpenInference · Convenciones semánticas](https://github.com/Arize-ai/openinference/tree/main/spec) (los `openinference.span.kind` y atributos `llm.*`, `retrieval.*`, `tool.*`)
- [Arize Phoenix · Documentación](https://arize.com/docs/phoenix) y [repositorio](https://github.com/Arize-ai/phoenix) (código abierto)
- [NVIDIA NeMo Agent Toolkit · Observar flujos](https://docs.nvidia.com/nemo/agent-toolkit/latest/run-workflows/observe/observe.html) y [con Phoenix](https://docs.nvidia.com/nemo/agent-toolkit/latest/run-workflows/observe/observe-workflow-with-phoenix.html)
- [NemoClaw · Monitorear la actividad del sandbox](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/monitoring/monitor-sandbox-activity) y [exportar trazas de Deep Agents](https://docs.nvidia.com/nemoclaw/latest/user-guide/deepagents/monitoring/set-up-deepagents-trace-export)
- [Preguntas frecuentes del curso](../../FAQ.md#trazas)
