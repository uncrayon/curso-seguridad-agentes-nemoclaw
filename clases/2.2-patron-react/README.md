# 2.2 · Razonamiento con el patrón ReAct

Objetivo: construir desde cero un loop ReAct que pide herramientas, las ejecuta de forma segura y sabe cuándo parar.

| | |
|---|---|
| **Duración del video** | ≈9 min |
| **Práctica** | Notebook (≈45 min), funciona sin key en modo MOCK |
| **Habilidad** | Implementar el patrón ReAct |
| **Lección de NVIDIA** | [01b · El bucle ReAct](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/01b-react.html) |
| **Material** | [Diapositivas](slides.html) · [Notebook](2.2-patron-react.ipynb) · [Preguntas frecuentes](../../FAQ.md) |

## Lo esencial (sin tecnicismos)

**La idea:** un modelo no sabe qué hora es ni puede consultar nada por su cuenta, pero puede pedirle a tu programa que lo haga. Con el patrón ReAct, el agente piensa, pide una herramienta, lee el resultado y vuelve a pensar hasta poder responder. El modelo solo pide; tu programa revisa el pedido y lo ejecuta.

**Piénsalo como:** un detective: piensa una hipótesis, busca una pista, piensa de nuevo. Las herramientas son las apps del celular de tu asistente.

**Palabras nuevas:** [ReAct](../../GLOSARIO.md), [herramienta](../../GLOSARIO.md), `finish_reason` (la razón por la que el modelo dejó de escribir: "terminé", "necesito que ejecutes algo" o "se me acabó el espacio").

**Hazlo sin programar (≈10 min):** descarga el notebook de esta clase, súbelo a [Colab](https://colab.research.google.com/) con **Archivo → Subir notebook** y presiona ▶ en cada celda, en orden, sin leer el código (o usa **Entorno de ejecución → Ejecutar todo**) (sin key funciona con respuestas simuladas). Luego responde:

1. En la sección 2, ¿qué `finish_reason` sale sin herramientas y cuál cuando le ofreces el reloj?
2. En la sección 5, ¿en cuántos pasos detiene el tope al agente terco que lee el reloj una y otra vez?
3. En la sección 7, ¿de qué ciudad pidió la hora Soporte NemoClaw?

**Qué te llevas:** entiendes que un agente no hace nada por sí mismo: pide, y alguien decide si se ejecuta. Esa es la base de toda la seguridad del curso.

## Lo que vas a lograr

- Leer `finish_reason` y usarlo como el router del loop: `stop`, `tool_calls` o `length`.
- Escribir un loop ReAct desde cero que valida cada `tool_call`, ejecuta la herramienta y devuelve el resultado como un mensaje `tool`.
- Detectar y contener las tres fallas típicas: `tool_call` mal formado, loop infinito y respuesta cortada por `length`.

## Antes de empezar

- Haber terminado la clase 2.1: sabes qué es el loop y que la memoria es `messages`.
- Python 3.10+ o Colab, y tu key `nvapi-` (opcional: sin key corre en MOCK).
- Abre el notebook igual que en la [clase 2.1](../2.1-loop-de-agente/README.md#1-abre-el-notebook).

## Paso a paso

### 1. Abre el notebook y ejecuta la configuración

```bash
source .venv/bin/activate
jupyter lab clases/2.2-patron-react/2.2-patron-react.ipynb
```

Ejecuta las dos primeras celdas y la del simulador. Deberías ver `Modo: EN VIVO · ...` o `Modo: MOCK ...`, y `Reglas del simulador listas: 1`.

### 2. Define tu primera herramienta (sección 1)

Ejecuta la celda de `get_current_time`. Fíjate en las dos partes: la **función** (`get_current_time`) y el **esquema** (`TOOL_HORA`), que es lo único que ve el modelo.

Deberías ver la hora actual, por ejemplo `2026-10-21 16:05:12 UTC`.

### 3. Lee `finish_reason` (sección 2)

Ejecuta la celda con las dos preguntas.

Deberías ver:

```text
[sin tools] finish_reason = 'stop'
   tool_calls: []
[con tools] finish_reason = 'tool_calls'
   tool_calls: [('get_current_time', '{}')]
```

La herramienta **no se ejecutó**: el modelo solo la pidió. Haz el **✏️ Tu turno**: borra "Usa get_current_time para leer el reloj." de la pregunta 2 y mira si el modelo la sigue pidiendo solo por la descripción.

### 4. Construye el loop ReAct (sección 3)

Lee la función `react` antes de ejecutarla. Tiene tres piezas:

1. El **router**: `length` corta con un error, `tool_calls` ejecuta herramientas y `stop` devuelve la respuesta.
2. La **validación** de cada `tool_call` (`validar_tool_call`): que la herramienta exista y que los argumentos sean un objeto JSON.
3. El **tope** `max_pasos`.

Ejecútala con "¿Qué hora es en UTC?". Deberías ver:

```text
[paso 1] finish_reason='tool_calls' · se enviaron 2 mensajes
   🔧 get_current_time({}) → 2026-10-21 16:05:12 UTC
[paso 2] finish_reason='stop' · se enviaron 4 mensajes
💬 Son las 16:05:12 UTC ...
```

### 5. Mira crecer `messages[]` (sección 4)

Ejecuta `mostrar(traza)`. Deberías ver los turnos `system`, `user`, `assistant` (pide la herramienta), `tool` (el resultado) y `assistant` (la respuesta), más una estimación de tokens.

Haz los dos experimentos de **✏️ Tu turno**: la capital de Francia (termina en el paso 1 con `stop`) y "¿Cuántos minutos faltan para las 17:00 UTC?" (cuenta las llamadas a herramientas).

### 6. Provoca las tres fallas (sección 5)

- **a) `tool_call` mal formado.** Ejecuta la celda de `tc_falso`. Deberías ver cuatro errores en texto, por ejemplo `ERROR: los argumentos no son JSON válido (Expecting property name enclosed in double quotes)`. Ninguno rompe el loop.
- **b) Loop infinito.** Ejecuta `SISTEMA_TERCO`. Deberías ver 4 pasos llamando al reloj y `⛔ Tope de 4 pasos sin respuesta final.`
- **c) `length`.** Ejecuta la pregunta con `max_tokens=20`. Deberías ver `finish_reason='length'` y `⛔ El modelo llegó a su límite de tokens (length).`

### 7. Mide el context rot (sección 6)

Ejecuta la celda de `tokens_aprox`. Deberías ver cómo crecen los tokens por llamada con cada ronda de herramientas (de cientos a miles).

### 8. Avance del proyecto: `hora_local` (sección 7)

Ejecuta la celda de Soporte NemoClaw. Deberías ver `🔧 hora_local({"ciudad": "Bogotá"})` y una respuesta con la hora local. Fíjate en que **no tocaste `react`**: solo agregaste el esquema a `TOOLS_SOPORTE` y la función a `REGISTRO_SOPORTE`.

### 9. (Opcional) Practica en el navegador con la lección de NVIDIA

En la [lección 01b de NVIDIA](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/01b-react.html), con tu key guardada en la lección 01a:

1. En la celda **finish_reason · el campo que determina el siguiente paso**, quita de `QUESTION_2` la frase que pide usar `get_current_time` y vuelve a ejecutar.
2. En **El bucle ReAct completo, construido desde cero**, nodo **Entrada del usuario**, cambia `state.userPrompt` por `"What is the capital of France?"` y mira el `finish_reason` del paso 1.
3. En el mismo nodo, cambia el system prompt por `"You must always call get_current_time once, then answer."` y comprueba si el modelo obedece.
4. Pregunta `"How many minutes until 17:00 UTC?"` y cuenta cuántas veces llama al reloj.
5. En el panel de chat del final, pregunta "¿Cómo decide el loop del reloj cuándo detenerse?".

## Comprueba que funcionó

- [ ] Puedes explicar qué hace el loop con cada `finish_reason`: `stop`, `tool_calls`, `length`.
- [ ] `react("¿Qué hora es en UTC?")` termina en 2 pasos y el historial tiene un mensaje `tool`.
- [ ] Los cuatro `tc_falso` devuelven un `ERROR: ...` en texto, sin excepción.
- [ ] `SISTEMA_TERCO` se detiene por el tope de pasos.
- [ ] Soporte NemoClaw responde la hora de tu ciudad usando `hora_local`.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| El modelo responde una hora inventada sin llamar a `get_current_time` | La descripción o el system prompt no dejan claro que no tiene reloj | Refuerza la descripción ("tú no tienes reloj") y revisa el historial: si no hay un mensaje `tool`, la herramienta no se ejecutó |
| `⛔ Tope de 6 pasos sin respuesta final.` | El modelo pide herramientas una y otra vez | Revisa el historial con `mostrar(t)`; corrige el system prompt o el resultado de la herramienta. No quites el tope. Ver [FAQ: loop](../../FAQ.md#notebooks) |
| `⛔ El modelo llegó a su límite de tokens (length).` | `max_tokens` muy bajo; Nemotron gasta tokens razonando antes de responder | Sube `max_tokens` (el helper usa 4096) o pide respuestas más cortas. Ver [FAQ: length](../../FAQ.md#elength) |
| `ERROR: los argumentos no son JSON válido (Expecting property name enclosed in double quotes)` | El modelo mandó JSON roto en `arguments` | El harness ya lo devuelve como observación para que el modelo corrija. Si se repite, simplifica el esquema |
| `AttributeError: 'types.SimpleNamespace' object has no attribute 'get'` | Agregaste `c.message` tal cual a `messages` en lugar de un dict | Usa `messages.append(a_dict(c.message))` |
| `RuntimeError: 400 · Solicitud inválida: ...` después de ejecutar una herramienta | Agregaste el mensaje `tool` sin el turno `assistant` que lo pidió, o con otro `tool_call_id` | Agrega primero `a_dict(c.message)` y luego un `tool` por cada `tool_call`, con el mismo `tc.id` |
| `RuntimeError: 429 · Demasiadas solicitudes por minuto.` | Cada paso del loop es una llamada y ejecutaste muchas seguidas | Espera unos segundos; no quites el tope de pasos. Ver [FAQ: 429](../../FAQ.md#e429) |

## Reto: evitar llamadas redundantes

Agrega `minutos_hasta(hora_utc)`, que recibe `"17:00"` y devuelve cuántos minutos faltan desde ahora en UTC.

**Criterio de éxito** (en vivo): con la herramienta en `TOOLS_SOPORTE` y `REGISTRO_SOPORTE`, "¿Cuántos minutos faltan para las 17:00 UTC?" se responde con **una sola** llamada a herramienta y el número coincide con tu cálculo a mano.

## Avance del proyecto

**Soporte NemoClaw v2: ReAct con una herramienta nueva.** Ya no es solo un chat: decide cuándo pedir una herramienta, la ejecuta con validación y tiene un tope de pasos. Su herramienta nueva es `hora_local(ciudad)`, para estudiantes de toda Latinoamérica.

Agrega `react`, `validar_tool_call`, `a_dict`, `hora_local` y su esquema a tu `soporte_nemoclaw.py`. En la clase 2.3 le das sus herramientas de verdad: `buscar_faq` y `estimar_costo_brev`.

## Recursos

- [Lección 01b · El bucle ReAct](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/01b-react.html), curso de NVIDIA DLI en español. Esta clase está basada en ella (Apache-2.0).
- Yao et al. (2022), [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629).
- Liu et al. (2023), [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172): la evidencia del context rot.
- Lilian Weng (2023), [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/): modelo, memoria, planeación y herramientas.
- [Preguntas frecuentes del curso](../../FAQ.md#errores-api).
