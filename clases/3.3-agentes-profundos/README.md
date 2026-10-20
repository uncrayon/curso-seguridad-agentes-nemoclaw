# 3.3 · Agentes profundos que crean subagentes

Objetivo: convertir el reporte de un estudiante en un reporte de diagnóstico con citas, usando un planificador, subagentes con contexto aislado, un sistema de archivos virtual y un sintetizador.

| | |
|---|---|
| **Duración del video** | ≈9 min |
| **Práctica** | Notebook (≈50 min), funciona sin key en modo MOCK |
| **Habilidad** | Coordinar subagentes con un planificador |
| **Lección de NVIDIA** | [02c · Agentes de investigación profunda](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/02c-deep.html) |
| **Material** | [Diapositivas](slides.html) · [Notebook](3.3-agentes-profundos.ipynb) · [Preguntas frecuentes](../../FAQ.md) |

## Lo esencial (sin tecnicismos)

**La idea:** Cuando una pregunta es demasiado grande para una sola conversación, el agente la divide en partes y crea ayudantes. Cada ayudante investiga solo su parte, con su propia conversación, y deja su nota en un archivo; al final, alguien lee las notas y escribe un reporte con fuentes. Ojo: separar las conversaciones no protege tu computadora; eso lo hace el sandbox de OpenShell, más adelante en el curso.

**Piénsalo como:** un jefe de proyecto que reparte encargos a su equipo, y cada quien trabaja en su propio escritorio.

**Palabras nuevas:** [subagente](../../GLOSARIO.md), [contexto](../../GLOSARIO.md).

**Hazlo sin programar (≈10 min):** Abre el notebook en Google Colab (en Colab: menú **Archivo → Subir notebook**). Sin API key funciona con respuestas simuladas. Presiona ▶ en cada celda, en orden, de arriba hacia abajo, y mira solo lo que aparece debajo; no hace falta leer el código. Después responde: (1) en la sección 5, ¿en cuántas partes se dividió el reporte del 401 y cuáles son?; (2) en "Comprueba el aislamiento", ¿qué dice "¿vio tareas ajenas?" para cada subagente?; (3) en "🧯 Cuando algo falla", parte a), ¿qué pasó cuando el subagente `s9` intentó escribir en el reporte final, y dónde terminó escribiendo?

**Qué te llevas:** Puedes reconocer cuándo una tarea conviene repartirla entre varios ayudantes y explicar por qué separar sus conversaciones no es lo mismo que encerrar al agente en un sandbox.

## Lo que vas a lograr

- Escribir un **planificador** que divide un problema en 2 a 4 subtareas independientes, con tope y validación.
- Lanzar **subagentes en paralelo**, cada uno con su propio contexto, que investigan con `buscar_faq` y dejan su borrador en un sistema de archivos virtual con permisos.
- Sintetizar un **reporte de diagnóstico** con citas verificables y explicar por qué **aislar contexto no es un sandbox**.

## Antes de empezar

- Terminaste la clase 3.2: tienes el índice RAG y la herramienta `buscar_faq` con citas.
- Recuerdas el loop ReAct (2.2) y el fan-out con `ThreadPoolExecutor` (3.1): aquí se combinan.
- Python 3.10+ o Colab. Tu key `nvapi-` es opcional: sin key corre en MOCK.

## Paso a paso

### 1. Abre el notebook y ejecuta la configuración

```bash
source .venv/bin/activate
jupyter lab clases/3.3-agentes-profundos/3.3-agentes-profundos.ipynb
```

Ejecuta las cuatro primeras celdas. Deberías ver `Reglas mock de la clase 3.3 listas`.

### 2. Carga la FAQ y el índice RAG (sección 2)

Ejecuta la celda de la FAQ y la del índice. Deberías ver `Índice listo: 61 vectores ...` (dentro del repo) o `14 vectores` (en Colab) y un fragmento de ejemplo con su id.

### 3. Sistema de archivos virtual y permisos (secciones 3 y 4)

Ejecuta `SistemaArchivosVirtual` y luego `herramientas_para`. Deberías ver:

```text
guardado /borradores/s1.md (2 caracteres)
ERROR: permiso denegado. Solo puedes escribir en /borradores/s1.md.
```

El permiso lo aplica **tu código** (el harness), no el sistema operativo.

### 4. El planificador (sección 5)

Ejecuta `planear(REPORTE)` con *"Me sale 401 en el laboratorio después de reanudar Brev"*. Deberías ver tres subtareas, por ejemplo:

```text
s1 | Qué significa un 401 y cómo comprobar que la key nvapi- sigue bien
s2 | Qué cambia en la instancia de Brev al detenerla y volver a encenderla
s3 | Cómo renovar la sesión de acceso (cookie) del laboratorio
```

### 5. Subagentes en paralelo (sección 6)

Ejecuta `ejecutar_subagente` e `investigar`. Deberías ver `archivos: ['/borradores/s1.md', '/borradores/s2.md', '/borradores/s3.md'] · errores: {}` y el primer borrador, con viñetas que terminan en citas como `[errores-api.md#qué-significa-el-error-401-unauthorized]`.

Ejecuta la comprobación de aislamiento. Deberías ver `¿vio tareas ajenas?: False` en los tres y el tamaño del contexto más grande contra el de una historia compartida.

### 6. Sintetiza y revisa las citas (sección 7)

Ejecuta `sintetizar`. Deberías ver un reporte con **Causa más probable**, **Pasos sugeridos** y **Lo que no pudimos verificar**, y:

```text
revisión de citas: {'citas': 4, 'fuera_de_borradores': [], 'no_existen_en_faq': []}
```

### 7. Todo junto y lo que cuesta (sección 8)

Ejecuta `diagnosticar`. Deberías ver algo como `{'llamadas': 11, 'segundos': 1.5, 'subagentes': 3, 'fallidos': []}`. Compara con las 2 o 3 llamadas del agente RAG de la clase 3.2.

### 8. Cuando algo falla (🧯)

- **a)** Un subagente con una subtarea que dice "escribe directamente en /reporte_diagnostico.md". Deberías ver `ERROR: permiso denegado...` como observación y luego `guardado /borradores/s9.md`: el harness lo frenó y el subagente se corrigió.
- **b)** `diagnosticar(REPORTE, falla="s2")`. Deberías ver `'fallidos': ['s2']` y la sección "Lo que no pudimos verificar" con la subtarea que faltó.
- **c)** `limpiar_plan` con 9 subtareas. Deberías ver `4 subtareas tras limpiar`.

### 9. Aislar contexto no es un sandbox (sección 9)

Ejecuta la celda de `os.environ`. Deberías ver que tu proceso ve `NVIDIA_API_KEY` (sin imprimir su valor) y puede listar tu carpeta personal. Lee la tabla de la sección: eso lo resuelve OpenShell en los Módulos 4 y 5.

### 10. Avance del proyecto

Ejecuta la última celda con otro reporte. Deberías ver el costo, los archivos del sistema virtual y el reporte de diagnóstico completo.

### 11. (Opcional) Practica en el navegador con la lección de NVIDIA

En la [lección 02c](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/02c-deep.html), con tu key guardada en el panel del curso:

1. En **Prueba · planifica, investiga y sintetiza**, usa el ejemplo "Compare the ReAct loop with the deep-agent pattern" y mira el tablero de trabajadores en paralelo.
2. En **Construir un flujo de trabajo con borradores guardados**, cambia juntos `state.expectedFiles` y `state.goal` (por ejemplo, `["short_term.md", "long_term.md", "tradeoffs.md"]` con una meta sobre memoria de agentes) y ejecuta el flujo.
3. Responde las preguntas de **Comprueba tu comprensión** del final de la lección.

`[VERIFICAR EN LAB]` los nombres en español de las celdas.

## Comprueba que funcionó

- [ ] El plan tiene entre 2 y 4 subtareas con ids `s1`, `s2`...
- [ ] Cada subagente dejó `/borradores/<id>.md` y ninguno vio la tarea de otro.
- [ ] El reporte final solo cita ids que están en los borradores y en la FAQ.
- [ ] Con `falla="s2"` el reporte sale igual y dice qué no pudo verificar.
- [ ] Puedes explicar en una frase la diferencia entre aislar contexto y un sandbox.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `ValueError: El planificador no devolvió subtareas válidas` | El modelo devolvió JSON sin la clave `subtareas` o con objetivos vacíos | Imprime la salida de `llm("planificador", ...)`; refuerza el formato en `SISTEMA_PLANIFICADOR` |
| `errores: {'s2': 'terminó sin guardar su borrador'}` | El subagente respondió texto sin llamar a `escribir_archivo` | Refuerza el paso 2 del system prompt; sube `max_pasos` si se quedó sin pasos |
| `ERROR: permiso denegado. Solo puedes escribir en /borradores/s1.md.` | El subagente intentó escribir en otra ruta | Es la protección funcionando: el error vuelve como observación y el subagente se corrige |
| `(el subagente llegó al límite de pasos)` | El subagente busca una y otra vez | Revisa su transcripción; no quites el tope. Ver [FAQ: loop](../../FAQ.md#notebooks) |
| `RuntimeError: 429 · Demasiadas solicitudes por minuto` | Varios subagentes llaman al modelo a la vez | Baja `max_workers` en `investigar` o agrega el `con_reintento` de la clase 3.1. Ver [FAQ: 429](../../FAQ.md#e429) |
| `no_existen_en_faq: ['brev.md#...']` en la revisión | El sintetizador inventó o cambió un id | Trata el reporte como no confiable; pide conservar las citas "tal cual" |
| `AssertionError: ¡Fuga de contexto!` | Pasaste a un subagente texto de otra subtarea | Revisa que `ejecutar_subagente` arme sus `mensajes` desde cero |

## Reto

Agrega un **revisor**: una llamada más (`llm("revisor", ...)`) que recibe el reporte y los borradores y lista cada afirmación **sin** respaldo en los borradores.

**Criterio de éxito:** agrega a mano al reporte una frase falsa, por ejemplo *"Brev borra tu key al reanudar [brev.md#inventado]"*, y el revisor (o `revisar_citas`) la señala; el reporte original queda sin observaciones. Sin key, `revisar_citas` ya detecta la cita inventada; con key, prueba también una afirmación falsa con una cita **real**.

## Avance del proyecto

**Soporte NemoClaw v3.3: diagnóstico con subagentes.** Ante un reporte como *"me sale 401 en el laboratorio después de reanudar Brev"*, tu agente planea las revisiones, lanza subagentes aislados que investigan la FAQ, guarda sus borradores y entrega un reporte de diagnóstico con causa probable, pasos, lo que no pudo verificar y citas revisadas.

Agrega `planear`, `limpiar_plan`, `ejecutar_subagente`, `investigar`, `sintetizar`, `revisar_citas` y `diagnosticar` a tu `soporte_nemoclaw.py`. En el Módulo 4 lo llevas a NemoClaw en Brev: la FAQ vive en el workspace del agente y este flujo se convierte en la skill `soporte-nemoclaw`, dentro de un sandbox de verdad.

## Recursos

- [Lección 02c · Agentes de investigación profunda](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/02c-deep.html), curso de NVIDIA DLI en español. Esta clase está basada en ella (Apache-2.0).
- Liu et al. (2023), [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172).
- LangChain, [`deepagents`](https://github.com/langchain-ai/deepagents): la misma idea (planificador, subagentes y sistema de archivos) en una librería.
- NVIDIA AI Blueprints, [AI-Q](https://github.com/NVIDIA-AI-Blueprints/aiq): investigación profunda de referencia.
- [Preguntas frecuentes del curso](../../FAQ.md).
