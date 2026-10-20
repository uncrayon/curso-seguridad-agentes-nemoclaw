# 2.1 · De una sola llamada al loop de agente

Objetivo: construir un agente desde cero y entender qué cambia cuando la decisión la toma un LLM.

| | |
|---|---|
| **Duración del video** | ≈9 min |
| **Práctica** | Notebook (≈45 min), funciona sin key en modo MOCK |
| **Habilidad** | Construir un loop básico de agente |
| **Material** | [Diapositivas](slides.html) · [Notebook](2.1-loop-de-agente.ipynb) · [Preguntas frecuentes](../../FAQ.md) |

## Lo esencial (sin tecnicismos)

**La idea:** un agente es un modelo que trabaja en ciclo: mira, decide, actúa y revisa si ya terminó. Lo que decide puede ser una regla fija, una búsqueda o un modelo de IA, y el ciclo es el mismo. El modelo no recuerda nada: la memoria es la conversación que le volvemos a enviar cada vez.

**Piénsalo como:** seguir una receta: lees el paso, lo haces, pruebas, y sigues hasta que el platillo está listo. La memoria es como tomar notas en una libreta y releerlas antes de cada llamada.

**Palabras nuevas:** [loop de agente](../../GLOSARIO.md), [memoria](../../GLOSARIO.md), [prompt](../../GLOSARIO.md).

**Hazlo sin programar (≈10 min):** descarga el notebook de esta clase, súbelo a [Colab](https://colab.research.google.com/) con **Archivo → Subir notebook** y presiona ▶ en cada celda, en orden, sin leer el código (o usa **Entorno de ejecución → Ejecutar todo**) (sin key funciona con respuestas simuladas). Luego responde:

1. En la sección 3, ¿cuántos pasos da el agente de "siempre a la derecha" antes de detenerse, y cuántos el de la búsqueda?
2. En la sección 5, ¿qué frase respondió el modelo con el prompt flojo y por qué el laberinto no la aceptó?
3. En la sección 7, ¿con cuántos mensajes de memoria el asistente olvida tu nombre?

**Qué te llevas:** sabes por qué todo agente necesita un límite de pasos, por qué lo que dice el modelo se revisa antes de obedecerlo y que recordar más cuesta más.

## Lo que vas a lograr

- Escribir el loop **observar → decidir → actuar → ¿parar?** y usarlo con tres "cerebros" distintos: una regla fija, una búsqueda (BFS) y un LLM.
- Validar la salida del modelo antes de actuar, para que un movimiento inválido no rompa tu agente.
- Darle memoria a un chat con la lista `messages` y ponerle un límite de contexto: la primera versión de **Soporte NemoClaw**.

## Antes de empezar

- Python 3.10 o superior en tu máquina, o una cuenta de Google para usar Colab.
- Tu API key `nvapi-` de la clase 1.2. **Es opcional:** sin key, el notebook corre completo en modo MOCK (un modelo simulado).
- El notebook de la clase 1.3 en verde, o al menos saber leer sus errores (401, 404, 429, `length`).

## Paso a paso

### 1. Abre el notebook

**En Colab:** sube `2.1-loop-de-agente.ipynb` (Archivo → Subir notebook). Para usar tu key, abre el panel de la llave 🔑 (*Secrets*), crea `NVIDIA_API_KEY` con tu key y activa el acceso del notebook.

**En tu máquina**, desde la raíz del repositorio del curso:

```bash
python3 -m venv .venv
source .venv/bin/activate          # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
echo "NVIDIA_API_KEY=nvapi-xxxxxxxx" > .env    # pon tu key real; .env no se sube a git
jupyter lab clases/2.1-loop-de-agente/2.1-loop-de-agente.ipynb
```

### 2. Ejecuta las celdas de configuración

Ejecuta las dos primeras celdas y la del simulador.

Deberías ver `Modo: EN VIVO · nvidia/nemotron-3.5-lightning-30b-a3b` si tu key está bien, o `Modo: MOCK (sin NVIDIA_API_KEY: respuestas simuladas)` si no hay key. Las dos opciones sirven para seguir.

### 3. Haz una sola llamada (sección 1)

Ejecuta la celda de la pregunta "¿Qué significa que una API de LLM sea 'sin estado'?".

Deberías ver `finish_reason: stop`, una respuesta de una oración y, en vivo, el `usage` con los tokens gastados. Luego cambia la pregunta por "¿Qué te pregunté hace un momento?": el modelo no lo sabe, porque cada llamada empieza de cero.

### 4. Construye el entorno y un agente sin LLM (secciones 2 y 3)

Ejecuta la celda del `Laberinto` y luego la de `correr_agente`.

Deberías ver que `siempre_derecha` avanza un paso y se atora: `'derecha' no es válido → no se aplica`, hasta `⛔ Se acabó el presupuesto de 6 pasos sin llegar.` Ese tope es lo que impide un loop infinito.

Luego ejecuta `decidir_bfs`. Deberías ver `✅ Meta en 15 pasos.` y el mapa con el camino marcado con `·`.

Mira `correr_agente` otra vez: no dice "laberinto" ni "BFS" en ningún lado. Esa función no va a cambiar en toda la clase.

### 5. Cambia la decisión por un LLM (sección 4)

Ejecuta `decidir_llm`. Le describimos el mapa en texto y le pedimos **una palabra**.

Deberías ver los pasos del agente y, en algún momento, una línea como `⚠ el modelo respondió 'arriba': no es legal. Se lo decimos y reintenta.` (en MOCK pasa siempre en el primer paso; en vivo, cuando el modelo se equivoca). Al final, la comparación `BFS: 15 pasos · LLM: N pasos`.

Haz los experimentos de **✏️ Tu turno**: quita la línea de estrategia, quita el mapa o sube la temperatura, y compara cuántos pasos tarda.

### 6. Provoca el error: un movimiento inválido (sección 5)

Ejecuta `decidir_ingenuo`, que usa un prompt flojo y pasa el texto del modelo directo al entorno.

Deberías ver algo como:

```text
El modelo dijo: 'Te sugiero ir hacia abajo: a la derecha casi todo es pared...'
💥 Movimiento inválido: 'Te sugiero ir hacia abajo: ...'. Desde (0, 0) solo puedes: ['abajo', 'derecha']
```

Ejecuta la celda siguiente: `extraer_movimiento` saca `'abajo'`, se valida contra los movimientos legales y se aplica. La lección: **la salida del modelo es una entrada no confiable; el harness la valida antes de actuar.**

### 7. Comprueba que la memoria es `messages` (sección 6)

Ejecuta la celda de "Me llamo Ada".

Deberías ver que con historial responde "Te llamas Ada" y sin historial dice que no lo sabe. Abajo aparece el JSON exacto que se envió en el turno 2: esa lista **es** la memoria.

### 8. Construye Soporte NemoClaw v1 (sección 7)

Ejecuta la celda de `ChatSoporte`. La misma conversación corre dos veces: con una ventana de 4 mensajes y con una de 20.

Deberías ver que con 4 mensajes el bot **olvida tu nombre** ("No sé cómo te llamas") y con 20 lo recuerda. Si quieres conversar, pon `INTERACTIVO = True` en la celda siguiente.

## Comprueba que funcionó

- [ ] `siempre_derecha` se detiene por el tope de pasos y `decidir_bfs` llega a la meta.
- [ ] `decidir_llm` llega a la meta usando **la misma** función `correr_agente`.
- [ ] Viste el `💥 Movimiento inválido` y lo arreglaste con `extraer_movimiento` + validación.
- [ ] Puedes explicar por qué "¿Cómo me llamo?" funciona con historial y falla sin él.
- [ ] `ChatSoporte` con ventana de 4 olvida el nombre y con ventana de 20 lo recuerda.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `Modo: MOCK (sin NVIDIA_API_KEY: respuestas simuladas)` aunque configuraste tu key | El kernel arrancó antes de crear el `.env`, el `.env` no está en la raíz del repo o en Colab no activaste el acceso al secret | Reinicia el kernel y vuelve a ejecutar desde la primera celda. Ver [FAQ: Modo MOCK](../../FAQ.md#emock) |
| `RuntimeError: 401 · Key rechazada: ...` | Key incompleta, con espacios o regenerada | Copia otra vez la key completa (`nvapi-...`). Ver [FAQ: 401](../../FAQ.md#e401) |
| `ValueError: Movimiento inválido: 'Te sugiero ir hacia abajo...'` | Pasaste el texto del modelo directo a `env.actuar` | Extrae el movimiento con `extraer_movimiento` y valida contra `obs["legales"]` antes de actuar |
| `⛔ Se acabó el presupuesto de 30 pasos sin llegar.` | El modelo da vueltas: le quitaste el mapa o la estrategia, o la temperatura es alta | Restaura el mapa en `describir`, baja la temperatura a 0 o sube `max_pasos`. Es el comportamiento esperado del tope |
| `⚠ finish_reason=length sin contenido: el modelo gastó max_tokens razonando.` | Nemotron razonó y se acabó `max_tokens` antes de responder | Deja `extra_body=SIN_RAZONAR` en la llamada o sube `max_tokens`. Ver [FAQ: length](../../FAQ.md#elength) |
| `RuntimeError: 400 · Solicitud inválida: ...` al cambiar `MODEL` | El modelo nuevo no acepta `chat_template_kwargs` | Quita `extra_body=SIN_RAZONAR` de las llamadas o vuelve a `nvidia/nemotron-3.5-lightning-30b-a3b` |
| `RuntimeError: 429 · Demasiadas solicitudes por minuto.` | Cada paso del laberinto es una llamada; ejecutaste varias corridas seguidas | Espera unos segundos entre corridas. Ver [FAQ: 429](../../FAQ.md#e429) |
| Soporte NemoClaw "olvida" lo que le dijiste | La ventana (`max_mensajes`) ya no incluye ese mensaje | Es el intercambio memoria vs. costo: agranda la ventana o resuelve el reto de abajo |

## Reto: memoria de hechos

Con `max_mensajes=4`, Soporte NemoClaw olvida tu nombre. Haz que lo recuerde **sin agrandar la ventana**: cuando el usuario diga "me llamo X", guarda `X` en un diccionario `hechos` y agrégalo al system prompt en cada llamada.

**Criterio de éxito** (en vivo): con `max_mensajes=4`, la `CONVERSACION` del notebook y dos preguntas extra, el bot responde bien "¿Cómo me llamo?" y `len(soporte.historial)` nunca pasa de 5. Escribe tu solución en la celda `ChatSoporteConHechos`.

## Avance del proyecto

**Soporte NemoClaw v1: un chat con memoria y límites.** Tiene un system prompt con su rol y reglas (nunca pide ni repite una API key), memoria en `historial`, una ventana de `max_mensajes` y un tope de `max_turnos` por sesión.

Copia `SISTEMA_SOPORTE` y la clase `ChatSoporte` a un archivo `soporte_nemoclaw.py` en tu propio repositorio. En la clase 2.2 le agregas el loop ReAct y su primera herramienta.

## Recursos

- Lección 01a · Agente, curso de NVIDIA DLI en español. Esta clase está basada en ella (Apache-2.0).
- [Repositorio del curso de NVIDIA (NVDLI/NemoClawDLI)](https://github.com/NVDLI/NemoClawDLI): código de las celdas del laberinto.
- Russell y Norvig, *Artificial Intelligence: A Modern Approach*, cap. 2 (agentes y entornos): el origen del ciclo percibir → razonar → actuar.
- [Preguntas frecuentes del curso](../../FAQ.md), secciones [Errores de la API](../../FAQ.md#errores-api) y [Notebooks](../../FAQ.md#notebooks).
