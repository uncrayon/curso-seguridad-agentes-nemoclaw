# 3.2 · RAG para fundamentar en tus fuentes

Objetivo: que Soporte NemoClaw responda con la FAQ del curso, cite cada afirmación como `[archivo#pregunta]` y diga "no sé" cuando no hay evidencia.

| | |
|---|---|
| **Video** | No tiene: es una clase complementaria |
| **Práctica** | Notebook (≈50 min), funciona sin key en modo MOCK |
| **Habilidad** | Implementar RAG con tus propias fuentes |
| **Material** | [Diapositivas](slides.html) · [Notebook](3.2-rag.ipynb) · [Preguntas frecuentes](../../FAQ.md) · [Corpus `datos/faq/`](../../datos/faq/) |

> **Esta clase es complementaria: no tiene video.** No la necesitas para seguir el curso. Tiene guía y notebook para que profundices a tu ritmo, y no usa el laboratorio de Brev.

## Lo esencial (sin tecnicismos)

**La idea:** Un modelo no conoce los documentos de tu organización, pero responde con mucha seguridad igual. Aquí tu agente primero busca en tus documentos los párrafos que se parecen a la pregunta, responde solo con ellos, dice de dónde salió cada dato y, si no encuentra nada, dice "no sé".

**Piénsalo como:** un examen a libro abierto: responde mejor si le dejas consultar sus apuntes.

**Palabras nuevas:** [RAG](../../GLOSARIO.md), [embedding](../../GLOSARIO.md), [cita](../../GLOSARIO.md).

**Hazlo sin programar (≈10 min):** Abre el notebook en Google Colab (en Colab: menú **Archivo → Subir notebook**). Sin API key funciona con respuestas simuladas y una muestra de la FAQ. Presiona ▶ en cada celda, en orden, de arriba hacia abajo, y mira solo lo que aparece debajo; no hace falta leer el código. Después responde: (1) en la sección 4, para "la cookie del laboratorio venció: session expired", ¿de qué documento salió el resultado de arriba? ¿Y qué pasó con "¿cuál es la capital de Perú?"?; (2) en la sección 5, ¿qué contestó el agente a la pregunta de Perú y por qué no inventó nada?; (3) en la sección 6, ¿cuántas de las ocho preguntas tienen marca verde ✅ (la respuesta correcta quedó primera)?

**Qué te llevas:** Sabes pedirle a un agente que responda con tus propios documentos, que muestre de dónde salió cada dato y que diga "no sé" cuando no tiene evidencia.

## Lo que vas a lograr

- Trocear la FAQ por entrada (`## P:`), pedir embeddings con `input_type="passage"` y `"query"` y buscar top-K por similitud coseno, en unas 25 líneas.
- Escribir un prompt que obliga a citar `[archivo#pregunta]`, a decir "no sé" sin evidencia, y verificar las citas con código.
- Medir la recuperación con **Hit@k** y exponerla como una **herramienta** que el agente decide llamar.

## Antes de empezar

- Terminaste la clase 3.1: tienes el router y los especialistas de Soporte NemoClaw.
- Python 3.10+ o Colab. Tu key `nvapi-` es opcional: sin key corre en MOCK con un embedding simulado.
- Con key, la ruta de embeddings usa `nvidia/nemotron-3-embed-1b` en `https://integrate.api.nvidia.com/v1` (la configuraste en la clase 1.3).

## Paso a paso

### 1. Abre el notebook y ejecuta la configuración

```bash
source .venv/bin/activate
jupyter lab clases/3.2-rag/3.2-rag.ipynb
```

Ejecuta las cuatro primeras celdas. Deberías ver `Modo: EN VIVO · ...` (o `Modo: MOCK ...`) y `Reglas mock de la clase 3.2 listas`.

### 2. Carga y trocea la FAQ (secciones 1 y 2)

Ejecuta la celda de la FAQ. Dentro del repo deberías ver `FAQ: datos/faq completa (9 archivos) · 61 entradas`; en Colab, `FAQ: muestra incrustada (7 archivos) · 14 entradas`. Los números exactos cambian si alguien edita la FAQ.

Ejecuta la celda de los fragmentos. Cada uno tiene un `id` citable:

```text
id      : api-key.md#dónde-consigo-mi-api-key-de
tema    : API key de NVIDIA Build
pregunta: ¿Dónde consigo mi API key de NVIDIA para el curso?
```

### 3. Pide un embedding (sección 3)

Ejecuta la celda de `embed(..., input_type="passage")`. Deberías ver el modelo, las dimensiones, los primeros valores y la norma. En vivo las dimensiones las fija `nemotron-3-embed-1b` (la lección de NVIDIA reporta 2048); sin key, el vector simulado tiene 4096 posiciones.

### 4. Construye el índice y busca (sección 4)

Ejecuta la clase `Indice`. Deberías ver los tres mejores fragmentos por pregunta:

```text
🔎 la cookie del laboratorio venció: session expired
   0.345  conexion-laboratorio.md#me-sale-session-expired-or-unreachable
   ...
🔎 ¿cuál es la capital de Perú?
   0.000  ...
```

Top-K **siempre** devuelve K resultados, aunque sean basura. Por eso existe `MIN_SCORE`.

### 5. Genera con citas y "no sé" (sección 5)

Ejecuta `responder`. Deberías ver una respuesta que termina en `[conexion-laboratorio.md#me-sale-session-expired-or-unreachable]` y, para la capital de Perú, `No sé con base en la FAQ del curso. (ningún fragmento superó el umbral)`: ni siquiera se llamó al modelo.

Haz el **✏️ Tu turno** con "Reanudé Brev y el laboratorio me da 401": la respuesta está repartida en varias entradas. Eso lo resuelve la clase 3.3.

### 6. Mide con Hit@k (sección 6)

Ejecuta `evaluar`. Deberías ver una línea por pregunta (✅ rank 1, 🟡 rank 2-3, ❌ fuera) y algo como `Hit@1 = 0.88 · Hit@3 = 1.00` sin key. En vivo, anota tus números: son tu línea base.

### 7. RAG como herramienta (sección 7)

Ejecuta el `agente`. Deberías ver que con "¡Hola!" **no** busca (`búsquedas: ninguna`), con la duda del laboratorio busca y cita, y con la capital de Perú recibe `SIN_EVIDENCIA` y dice que no sabe.

### 8. Cuando algo falla (🧯)

- **a)** Ejecuta la celda sin `input_type`. Deberías ver `422 · Argumentos con formato incorrecto (p. ej. falta input_type en embeddings ...)`.
- **b)** Ejecuta `EVAL_EN`. Deberías ver que Hit@k baja con preguntas en inglés sobre una FAQ en español (sin key, mucho).
- **c)** Ejecuta `GRANDES`. Deberías ver que, indexando archivos completos, el contexto crece más del doble y la cita ya no dice qué entrada.

### 9. Avance del proyecto

Ejecuta `soporte_nemoclaw`. Deberías ver una respuesta citada y la línea `[búsquedas: [...] · citas: 1]`.

## Comprueba que funcionó

- [ ] Cada fragmento tiene un id `archivo.md#pregunta` y ninguno se repite.
- [ ] La pregunta fuera de tema responde "no sé" **sin** llamar al modelo.
- [ ] `verificar_citas` muestra `inventadas: []` en tus respuestas.
- [ ] Tienes tu Hit@1 y Hit@3 anotados (sin key y, si puedes, en vivo).
- [ ] El agente no busca para un saludo y sí busca para una duda técnica.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `RuntimeError: 422 · Argumentos con formato incorrecto (p. ej. falta input_type en embeddings ...)` | Llamaste a la API de embeddings sin `input_type` | Usa `embed(textos, input_type="passage")` para indexar y `"query"` para buscar. Ver [FAQ: 422](../../FAQ.md#errores-api) |
| Hit@k bajo sin ningún error | Invertiste `query` y `passage`, o las preguntas están en otro idioma que la FAQ | Revisa el `input_type` en las dos llamadas; escribe la FAQ en el idioma de tus usuarios o traduce la pregunta antes de buscar |
| Todo responde "No sé con base en la FAQ del curso." | `MIN_SCORE` muy alto para tu modelo de embeddings | Imprime los puntajes de preguntas buenas y malas y pon el umbral entre ambos |
| El agente responde con datos que no están en la FAQ | Umbral muy bajo o prompt sin la regla "solo el contexto" | Sube `MIN_SCORE`, conserva las 4 reglas de `SISTEMA_RAG` y revisa `verificar_citas` |
| `inventadas: ['brev.md#...']` | El modelo escribió un id que no le diste | Pide copiar el id "tal cual" y trata esa respuesta como no confiable |
| La respuesta ignora el final de una entrada larga | `truncate="END"` cortó el fragmento en silencio | Trocea por entrada; ninguna entrada de la FAQ debería pasar de unos cientos de palabras |
| `RuntimeError: 404 · Ese modelo o esa ruta no existen` al indexar | `EMBED_MODEL` mal escrito o ruta de chat en lugar de embeddings | Usa `nvidia/nemotron-3-embed-1b` y `BASE_URL` terminada en `/v1`. Ver [FAQ](../../FAQ.md#errores-api) |
| `FAQ: muestra incrustada` aunque estás en el repo | El notebook no corre desde `clases/3.2-rag/` | Ábrelo desde su carpeta; la ruta es `../../datos/faq` |

## Reto

Agrega **3 entradas propias** a la FAQ (en `FAQ_MUESTRA` o en `datos/faq/`), con el formato `## P:`, y escribe **4 preguntas** de prueba para ellas en `EVAL`.

**Criterio de éxito:** Hit@1 ≥ 0.75 en tus 4 preguntas, cada respuesta del agente cita al menos un id que existe (`inventadas` vacío) y el agente dice "no sé" ante una pregunta fuera de la FAQ.

## Avance del proyecto

**Soporte NemoClaw v3.2: RAG con citas.** Tu agente ya responde con la FAQ del curso, cita cada afirmación con `[archivo#pregunta]`, verifica sus citas y dice "no sé" cuando no hay evidencia. La búsqueda es una herramienta: el agente decide cuándo usarla.

Agrega `Indice`, `responder`, `buscar_faq` (la versión con embeddings), `verificar_citas` y `agente` a tu `soporte_nemoclaw.py`. En la clase 3.3, un planificador le da esta herramienta a varios subagentes para armar un reporte de diagnóstico.

## Recursos

- Lección 02b · El agente de indexación, curso de NVIDIA DLI en español. Esta clase está basada en ella (Apache-2.0).
- Lewis et al. (2020), [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401).
- Catálogo de modelos de NVIDIA Build: [build.nvidia.com](https://build.nvidia.com) (busca `nemotron-3-embed-1b`).
- Edge et al. (2024), [From Local to Global: A Graph RAG Approach](https://arxiv.org/abs/2404.16130), para cuando top-K no alcanza.
- [Preguntas frecuentes del curso](../../FAQ.md) y el corpus [`datos/faq/`](../../datos/faq/).
