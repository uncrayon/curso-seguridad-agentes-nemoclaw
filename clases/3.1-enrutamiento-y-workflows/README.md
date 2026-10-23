# 3.1 · Enruta trabajo entre varias llamadas

Objetivo: que tu código, y no el modelo, sea dueño de la forma del trabajo: un router de triage con enum fijo, un pipeline ReWOO en paralelo y un fan-out que sobrevive a una rama caída.

| | |
|---|---|
| **Video** | No tiene: es una clase complementaria |
| **Práctica** | Notebook (≈50 min), funciona sin key en modo MOCK |
| **Habilidad** | Enrutar subtareas entre llamadas a modelos |
| **Material** | [Diapositivas](slides.html) · [Notebook](3.1-enrutamiento-y-workflows.ipynb) · [Preguntas frecuentes](../../FAQ.md) |

> **Esta clase es complementaria: no tiene video.** No la necesitas para seguir el curso. Tiene guía y notebook para que profundices a tu ritmo, y no usa el laboratorio de Brev.

## Lo esencial (sin tecnicismos)

**La idea:** Cuando ya sabes cómo se reparte un trabajo, no hace falta que el modelo lo decida todo. Tu código reparte: clasifica cada petición, lanza varias búsquedas a la vez y junta las respuestas. Y siempre revisa lo que contesta el modelo antes de usarlo.

**Piénsalo como:** la recepcionista que te dice a qué ventanilla ir.

**Palabras nuevas:** [router](../../GLOSARIO.md), ReWOO (planear todo primero y después hacer las búsquedas a la vez, como la lista del súper antes de salir), fan-out (mandar la misma consulta a varios especialistas al mismo tiempo y juntar sus notas).

**Hazlo sin programar (≈10 min):** Abre el notebook en Google Colab (en Colab: menú **Archivo → Subir notebook**). Sin API key funciona con respuestas simuladas. Presiona ▶ en cada celda, en orden, de arriba hacia abajo, y mira solo lo que aparece debajo; no hace falta leer el código. Después responde: (1) en la lista de seis tickets, ¿a qué categoría fue el mensaje del 401 y a cuál el del reembolso?; (2) ¿qué etiqueta inventó el modelo para el reembolso y en cuál terminó después del segundo intento?; (3) en la sección 4, ¿qué especialista "no contestó" y qué dice la respuesta final sobre eso?

**Qué te llevas:** Puedes decidir cuándo conviene repartir un trabajo entre varias llamadas al modelo y cuándo basta con una, y sabes que lo que contesta el modelo siempre se revisa.

## Lo que vas a lograr

- Clasificar tickets de estudiantes con un **enum cerrado** (`instalacion | api_key | brev | seguridad | otro`), validar el JSON y decidir qué hacer cuando el modelo inventa una etiqueta.
- Construir un pipeline **ReWOO**: planear una vez, ejecutar búsquedas en paralelo con `concurrent.futures` y sintetizar una vez, midiendo la latencia de cada fase.
- Hacer **fan-out / fan-in** a varios especialistas, aislar la rama que falla, reintentar solo lo reintentable y saber cuándo **no** dividir.

## Antes de empezar

- Terminaste la clase 2.3: sabes que una herramienta es un contrato y que los errores vuelven al modelo como texto.
- Python 3.10+ o Colab. Tu key `nvapi-` es opcional: sin key, el notebook usa el modelo simulado (MOCK).
- Si trabajas en local, el entorno de la [clase 2.1](../2.1-loop-de-agente/README.md) ya tiene todo lo que necesitas (`openai`, `python-dotenv`).

## Paso a paso

### 1. Abre el notebook y ejecuta la configuración

```bash
source .venv/bin/activate
jupyter lab clases/3.1-enrutamiento-y-workflows/3.1-enrutamiento-y-workflows.ipynb
```

En Colab: **Archivo → Subir notebook** y guarda tu key en Secrets como `NVIDIA_API_KEY`.

Ejecuta las cuatro primeras celdas (configuración, cliente, ayudas y reglas mock). Deberías ver:

```text
Modo: EN VIVO · nvidia/nemotron-3.5-lightning-30b-a3b      (o "Modo: MOCK ...")
Cliente listo: https://integrate.api.nvidia.com/v1
Ayudas listas: llm(), llamar(), extraer_json(), ErrorSimulado
Reglas mock de la clase 3.1 listas
```

### 2. Define el enum y el validador (sección 2)

Ejecuta la celda de `CATEGORIAS`, `ESQUEMA_TRIAGE` y `validar_triage`. Deberías ver:

```text
[]
["categoria inválida: 'facturacion'"]
```

Una lista vacía significa "válido". La segunda línea es lo que pasa cuando el modelo inventa una categoría.

### 3. Clasifica con reintento

Ejecuta la celda de `clasificar`. Fíjate en el orden:

1. Pide JSON con `response_format` y el esquema (si la ruta no lo acepta y responde 400, sigue solo con el prompt).
2. Extrae el JSON aunque venga con prosa alrededor.
3. Valida. Si falla, **un** reintento que le muestra al modelo su error. Si vuelve a fallar, `otro`.

Deberías ver `intento 1: ... -> OK` y un diccionario con `'categoria': 'api_key'`.

### 4. Router y especialistas

Ejecuta la celda de `crear_especialista` y `soporte`. Recorre seis tickets. Busca estos dos casos en la salida:

```text
   intento 1: 'Claro, esta es la clasificación:\n{"categoria": "brev", ...' -> OK
   ...
   intento 1: '{"categoria": "facturacion", ...' -> ["categoria inválida: 'facturacion'"]
   intento 2: '{"categoria": "otro", ...' -> OK
→ otro        baja  intentos=2 | Quiero un reembolso, me hicieron un cobro doble
```

El router es un diccionario: `ESPECIALISTAS[t["categoria"]]`. Nunca falla porque validaste antes. Haz el **✏️ Tu turno** con tres tickets tuyos, uno ambiguo.

### 5. ReWOO: planear → ejecutar en paralelo → sintetizar (sección 3)

Ejecuta la celda de la FAQ (carga la muestra o, dentro del repo, `datos/faq/` completa) y luego la celda de `planear`, `ejecutar` y `sintetizar`. Deberías ver algo así:

```text
   (el plan traía 5 consultas; lo recorto a 4)
PLAN (cada consulta → la entrada que encontró):
   'cómo detener la instancia de brev'            → brev.md#cómo-detengo-o-borro-mi-instancia
   'session expired en el laboratorio'            → conexion-laboratorio.md#me-sale-session-expired-or-unreachable
   ...
llamadas al modelo: 2 ['planificador', 'sintetizador']
```

Dos llamadas al modelo, sin importar cuántas búsquedas tenga el plan.

### 6. Mide la latencia

Ejecuta la celda de las barras. Deberías ver las búsquedas en paralelo (≈0.5 s) contra en serie (≈2 s). En vivo, mira cuánto pesan el planificador y el sintetizador en el total: si tardan 5 s cada uno, ahorrar 1.5 s en búsquedas casi no se nota.

### 7. Fan-out con una rama que falla (sección 4)

Ejecuta la celda de `fan_out`. Deberías ver:

```text
  api_key    0.31s ███
  brev       0.31s ███
  seguridad  FALLÓ → TimeoutError: el especialista no respondió a tiempo (simulado)
```

Y una respuesta unida que termina en "Ojo: falta la revisión de seguridad; esta respuesta puede estar incompleta."

### 8. Compara con una sola llamada (sección 5)

Ejecuta la celda del `generalista`. Compara llamadas y segundos: 1 llamada contra 4. Lee la tabla "Divide cuando… / NO dividas cuando…".

### 9. Cuando algo falla (🧯)

- **a)** Ejecuta `SALIDAS_MALAS`. Deberías ver que `"Brev"` con mayúscula y el JSON cortado (`{"categoria": "brev", "prio`) se rechazan.
- **b)** Ejecuta `rama_con_429`: la rama `seguridad` recibe un 429 y verás el diagnóstico `429 · Demasiadas solicitudes por minuto...`. Luego `con_reintento`: `429 en seguridad (intento 1): espero 0.5s y reintento` y las tres ramas OK.

### 10. Avance del proyecto

Ejecuta `soporte_nemoclaw`. Un ticket simple va a un especialista; el reporte del 401 tiene prioridad alta y pasa por el fan-out.

## Comprueba que funcionó

- [ ] `validar_triage` rechaza `facturacion`, `Brev` con mayúscula y el JSON cortado.
- [ ] El ticket de reembolso termina en `otro` después de 2 intentos y no rompe el pipeline.
- [ ] ReWOO hace exactamente 2 llamadas al modelo y las búsquedas en paralelo tardan menos que en serie.
- [ ] El fan-out entrega una respuesta aunque `seguridad` falle, y la respuesta lo dice.
- [ ] Con `con_reintento`, el 429 se recupera y un 401 no se reintentaría.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `["categoria inválida: 'facturacion'"]` (o cualquier etiqueta fuera de la lista) | El modelo inventó una categoría o la ruta no aplicó el esquema | Es esperado: el reintento le muestra su error y, si insiste, va a `otro`. Nunca mapees sinónimos a mano |
| `JSON ilegible (ValueError)` o `JSONDecodeError` | El modelo agregó prosa sin JSON o `finish_reason=length` cortó el JSON | `extraer_json` rescata la prosa; para el corte, sube `max_tokens`. Ver [FAQ: length](../../FAQ.md#elength) |
| `RuntimeError: 400 · Solicitud inválida` al clasificar | La ruta o el modelo no acepta `response_format` con `json_schema` | `_pedir_triage` reintenta sin esquema; tu validador sigue protegiéndote |
| `RuntimeError: 429 · Demasiadas solicitudes por minuto` en una rama | Lanzaste muchas llamadas en paralelo | Baja `max_workers` y envuelve la rama con `con_reintento`. Ver [FAQ: 429](../../FAQ.md#e429) |
| `KeyError: 'facturacion'` al llamar al especialista | Usaste la etiqueta del modelo sin validar | Llama a `clasificar` (que valida) antes del router |
| `ValueError: max_workers must be greater than 0` | El plan llegó vacío y `ThreadPoolExecutor` recibió 0 hilos | `planear` ya lanza un error claro si no hay consultas; revisa lo que devolvió el planificador |
| ReWOO responde algo sin sentido en el paso 2 | El paso 2 dependía del resultado del paso 1 | ReWOO no sirve ahí: usa ReAct o un loop dentro de esa etapa |

## Reto

Agrega la categoría **`costos`** (créditos y precio de Brev; en la clase 2.3 hiciste `estimar_costo_brev`): súmala a `CATEGORIAS`, al prompt `SISTEMA_TRIAGE` y a `ESPECIALISTAS`, y escribe 3 tickets de costos y 1 ambiguo.

**Criterio de éxito:** los 3 tickets de costos llegan a `costos`, el de reembolso sigue cayendo en `otro` por validación y ningún ticket rompe el pipeline. Sin key, agrega una regla al mock; con key, pruébalo en vivo.

## Avance del proyecto

**Soporte NemoClaw v3.1: triage + especialistas.** Tu agente ya no responde todo con el mismo prompt: clasifica cada ticket en `instalacion | api_key | brev | seguridad | otro`, valida la etiqueta y lo manda al especialista correcto. Si el ticket es urgente, corre el fan-out y une las revisiones, diciendo qué faltó.

Agrega `clasificar`, `validar_triage`, `ESPECIALISTAS`, `fan_out`, `unir` y `con_reintento` a tu `soporte_nemoclaw.py`. En la clase 3.2 los especialistas dejan de responder de memoria: les das RAG sobre la FAQ, con citas.

## Recursos

- Lección 02a · El agente de flujo de trabajo, curso de NVIDIA DLI en español. Esta clase está basada en ella (Apache-2.0).
- Xu et al. (2023), [ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models](https://arxiv.org/abs/2305.18323).
- Yao et al. (2022), [ReAct](https://arxiv.org/abs/2210.03629), para comparar.
- Documentación de Python: [`concurrent.futures`](https://docs.python.org/es/3/library/concurrent.futures.html).
- [Preguntas frecuentes del curso](../../FAQ.md#errores-api) y el corpus [`datos/faq/`](../../datos/faq/).
