# 1.3 · Configura rutas de modelo y diagnostica errores

Objetivo: dejar tu entorno verificado (chat, tools y embeddings) y saber leer cualquier error de la API.

| | |
|---|---|
| **Duración del video** | ≈7 min |
| **Práctica** | Notebook [`1.3-rutas-de-modelo-y-errores.ipynb`](1.3-rutas-de-modelo-y-errores.ipynb) (≈30 min) |
| **Habilidad** | Configurar rutas de modelo; diagnosticar errores 401, 403, 404, 429 y 5xx |
| **Material** | [Diapositivas](slides.html) · [Preguntas frecuentes](../../FAQ.md) |

## Lo esencial (sin tecnicismos)

**La idea:** para hablar con un modelo hay que darle tres datos: a qué dirección escribir, qué modelo quieres y tu key. Cuando uno está mal, NVIDIA responde con un número de error. Cada número dice qué arreglar, y hoy los provocas a propósito para que no te asusten.

**Piénsalo como:** los avisos de un cajero automático: "tarjeta inválida", "fondos insuficientes", "intente más tarde". Y la ruta de modelo es como la dirección postal de una oficina: si está mal escrita, la carta regresa.

**Palabras nuevas:** [ruta de modelo](../../GLOSARIO.md), [errores 401, 403, 404, 429](../../GLOSARIO.md), [notebook y Colab](../../GLOSARIO.md).

**Hazlo sin programar (≈10 min):** descarga el archivo del notebook de esta clase, entra a [Colab](https://colab.research.google.com/) y súbelo desde el menú **Archivo → Subir notebook**. Presiona ▶ en cada celda, en orden, sin leer el código (o usa **Entorno de ejecución → Ejecutar todo**) (funciona aunque no tengas key: usa respuestas simuladas). Luego responde:

1. ¿La primera celda dice "EN VIVO" o "MOCK"? ¿Qué significa en tu caso?
2. En la sección 7, ¿qué número de error sale con la key falsa y qué te recomienda el diagnóstico?
3. ¿Qué dice el veredicto de la última celda?

**Qué te llevas:** cuando veas un 401, un 404 o un 429, sabes si hay que corregir algo o solo esperar.

## Lo que vas a lograr

- Configurar las dos rutas que usa todo el curso: **chat** y **embeddings**, en el panel del curso de NVIDIA y en Python.
- Correr el **doctor del curso**: un notebook que comprueba key, modelos, chat, tools y embeddings, mide latencia y muestra `usage`.
- Provocar y resolver los errores 401, 404 y `finish_reason=length`, y reintentar un 429 con backoff.

## Antes de empezar

- Tu API key `nvapi-` de la clase 1.2, guardada en `.env`, en una variable de entorno o en los Secrets de Colab.
- Una de estas dos opciones:
  - **Google Colab**: sube el notebook o ábrelo desde GitHub. La primera celda instala todo.
  - **Tu máquina**: Python 3.10 o superior y, desde la raíz del repo:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab clases/1.3-rutas-de-modelo-y-errores/
```

¿Sin key todavía? El notebook corre igual en **modo MOCK** (respuestas y errores simulados) y al final te dice qué falta.

## Las ideas clave

### Una ruta de modelo = URL base + ID del modelo + key

| Ruta | URL base | Modelo | Para qué |
|---|---|---|---|
| **Chat** | `https://integrate.api.nvidia.com/v1` | `nvidia/nemotron-3.5-lightning-30b-a3b` | Conversación y tools (módulos 2 a 6) |
| **Embeddings** | `https://integrate.api.nvidia.com/v1` | `nvidia/nemotron-3-embed-1b` | Convertir texto en vectores para RAG (clase 3.2) |

En Python se configuran con `NVIDIA_BASE_URL`, `NVIDIA_MODEL`, `NVIDIA_EMBED_MODEL` y `NVIDIA_API_KEY` (ver `.env.example` en la raíz del repo).

### El panel de configuración del curso de NVIDIA

Está en la portada del curso (sección **"Cómo introducir tu clave de API"**) y también en la lección 1a. Sus campos:

| Campo | Valor por defecto | Qué hace |
|---|---|---|
| **URL base de la API de chat** | `https://integrate.api.nvidia.com/v1` | A dónde van las llamadas. HTTPS y terminada en `/v1` |
| **ID del modelo de chat** | `nvidia/nemotron-3.5-lightning-30b-a3b` | El modelo que responde |
| **Clave bearer** | — | Tu key `nvapi-`. Vive en `sessionStorage`: se borra al cerrar la pestaña |
| **Usar el relay de navegador de NVIDIA DLI** | Activado en la página del curso | Relay de CORS: reenvía tus llamadas a la API de NVIDIA para que una página estática pueda hacerlas. No te da key ni acceso a modelos |
| **Ruta de embeddings** (desplegable) | Misma URL · `nvidia/nemotron-3-embed-1b` | Ruta independiente; si no le pones key, usa la del chat |
| **Gestión de la solicitud** (desplegable) | Espera 60 s (5–300) · reintentos 0 (0–5) | Los reintentos solo aplican a fallas de red, 429 y 5xx |
| Botón **Guardar y verificar** | — | Revisa el prefijo `nvapi-` y hace una llamada de prueba. Si sale bien, verás "✓ Conectado." |

## Paso a paso

### 1. Configura el panel del curso de NVIDIA

1. Abre <https://nvdli.github.io/NemoClawDLI/es/nemoclaw/index.html> y baja a **"Cómo introducir tu clave de API"**.
2. Deja la URL base y el modelo como están. Pega tu key en el campo de la clave.
3. Abre **Ruta de embeddings** y confirma que el modelo sea `nvidia/nemotron-3-embed-1b`.
4. Abre **Gestión de la solicitud**: deja la espera en 60 s y sube los reintentos a 2.
5. Haz clic en **Guardar y verificar**.

Deberías ver: "✓ Conectado." con la respuesta del modelo, y en la barra superior la etiqueta de key con una palomita. Debajo, un resumen: "✓ Clave de API disponible en esta pestaña", la ruta de chat y la ruta de embeddings.

### 2. Abre el notebook y ejecuta la configuración

1. Abre [`1.3-rutas-de-modelo-y-errores.ipynb`](1.3-rutas-de-modelo-y-errores.ipynb).
2. Ejecuta las tres primeras celdas.

Deberías ver: `Modo: EN VIVO · nvidia/nemotron-3.5-lightning-30b-a3b` (o `MOCK` si no hay key) y `Doctor listo`.

### 3. Corre las cinco pruebas del doctor

Ejecuta las secciones 1 a 6 en orden. Cada una imprime una línea:

```text
✅ key: nvapi-…abcd (<N> caracteres)
✅ modelos: /models responde y nvidia/nemotron-3.5-lightning-30b-a3b está en el catálogo
✅ chat: respondió en <X> s
✅ tools: el modelo pidió buscar_faq con argumentos JSON válidos
✅ embeddings: vector de <N> dimensiones
```

(Los números de tu salida serán distintos: longitud de la key, latencia y dimensiones del vector.)

En la sección 4 fíjate en el bloque `usage` (tokens de entrada y salida) y en la latencia.

### 4. Rompe tu entorno a propósito

En la sección 7 vas a provocar tres fallos y a leerlos con `diagnostico()`:

```python
# key falsa → 401
OpenAI(base_url=BASE_URL, api_key="nvapi-ESTA-KEY-ES-FALSA-000000000000").chat.completions.create(...)
# modelo inexistente → 404
chat([{"role": "user", "content": "hola"}], model="nvidia/modelo-que-no-existe")
# max_tokens diminuto → finish_reason="length"
chat([{"role": "user", "content": "Explica qué es un agente de IA."}], max_tokens=8)
```

Deberías ver: para el 401, "Key rechazada: revisa que NVIDIA_API_KEY sea la key completa…"; para el 404, "Ese modelo o esa ruta no existen…"; y para el tercero, `finish_reason: length` con el contenido vacío o cortado.

### 5. Reintenta un 429 con backoff

La sección 8 define `con_reintentos()`: espera 1 s, 2 s, 4 s… (y respeta `Retry-After` si llega), solo para 429, 5xx y fallas de red. Deberías ver:

```text
   ⏳ intento 1 falló con 429; espero 0.21 s
   ⏳ intento 2 falló con 429; espero 0.41 s
Caso 429: respuesta al tercer intento
Caso 401:
   ✋ No reintento (intento 1): 401 · Key rechazada: …
```

### 6. Lee el veredicto

La última celda imprime **✅ entorno listo** o la lista de pruebas que fallaron, cada una con su arreglo.

### Tabla de errores de la API

| Código | Qué significa | ¿Reintentar? | Qué hacer |
|---|---|---|---|
| **401** | Key rechazada | Nunca | Key completa, con `nvapi-`, sin comillas ni espacios. Si la regeneraste, la vieja ya no sirve |
| **403** | Key válida sin acceso a ese modelo o ruta | No | Revisa tu cuenta en build.nvidia.com o usa otro modelo |
| **404** | Modelo o ruta inexistente | No | Copia el ID exacto de `/v1/models`; `BASE_URL` debe terminar en `/v1` |
| **410** | Modelo retirado del endpoint gratuito | No | Cambia `NVIDIA_MODEL` por un modelo vigente |
| **429** | Límite de solicitudes | Sí, con espera | Backoff exponencial; no ejecutes celdas en ráfaga |
| **5xx** | Falla del servidor o modelo arrancando | Sí, con espera | Reintenta en 30–60 s; si sigue, otro modelo |
| `finish_reason="length"` | Se acabó `max_tokens` | — | Sube `max_tokens` |

Más tiempo de espera o más reintentos **nunca** arreglan un 401 o un 403.

## Comprueba que funcionó

- [ ] "Guardar y verificar" en la página de NVIDIA mostró "✓ Conectado.".
- [ ] El notebook terminó en **✅ entorno listo** (o sé exactamente qué me falta).
- [ ] Vi la latencia y el bloque `usage` de una llamada.
- [ ] Provoqué un 401, un 404 y un `finish_reason=length`, y entendí cada diagnóstico.
- [ ] Sé qué errores se reintentan (429, 5xx) y cuáles no (401, 403, 404, 410).

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| El notebook dice `Modo: MOCK` aunque creaste el `.env` | El `.env` no está en la raíz del repo, o abriste Jupyter desde otra carpeta, o no reiniciaste el kernel | Pon `.env` en la raíz del repo (junto a `.env.example`) y reinicia el kernel. En Colab usa Secrets |
| En Colab: `Modo: MOCK` con el secreto creado | El nombre no es exactamente `NVIDIA_API_KEY` o falta activar el acceso del notebook | Revisa el nombre y el interruptor en el panel 🔑 y vuelve a ejecutar todo |
| `401 · Key rechazada` | Key incompleta, con comillas, con espacios o revocada | La sección 1 del notebook te dice cuál de estos es. Copia la key de nuevo |
| `404 · Ese modelo o esa ruta no existen` | ID del modelo mal copiado o `BASE_URL` sin `/v1` | Copia el ID de la lista de la sección 3 |
| `⚠ finish_reason=length sin contenido` | `max_tokens` demasiado bajo para un modelo que razona | Sube `max_tokens` (1024 o más) |
| En la página de NVIDIA: "La clave debe comenzar por nvapi-" | Pegaste otra cosa o con un espacio al inicio | Copia la key completa desde build.nvidia.com |
| En la página de NVIDIA: "Connection failed: …" al guardar | La prueba de conexión falló; el panel deshace los cambios | Lee el mensaje: 401/403 es la key; 429, espera; 5xx, el proveedor o el relay. Vuelve a intentar una vez |
| "La URL base de la API de modelos debe usar HTTPS" o 404 en todo | Cambiaste la URL base por error | Restablece `https://integrate.api.nvidia.com/v1` |
| La celda de tools dice que el modelo respondió texto en vez de pedir la tool | El modelo a veces no usa la tool, o elegiste un modelo sin soporte de tools | Ejecuta la celda una vez más; si persiste, vuelve al modelo por defecto |

## Reto

Convierte el notebook en una sola función `doctor()` que corra las cinco pruebas y devuelva el reporte de entorno.

**Criterio de éxito:** con tu configuración normal termina en "✅ entorno listo"; con `MODEL = "nvidia/nemotron-3.5-lightning"` (ID incompleto) el reporte marca `modelos` y `chat` como falla y el arreglo habla del ID exacto; y el reporte nunca contiene tu key.

## Avance del proyecto

Soporte NemoClaw gana su primera pieza de código: **`reporte_entorno()`** (sección 10 del notebook). Devuelve un resumen sin secretos: versión de Python, modo, rutas, estado de cada prueba y latencia. Es lo que un estudiante pegará al pedir ayuda, y en la clase 3.3 los subagentes de Soporte NemoClaw lo van a leer para armar un diagnóstico. Guarda tu función.

## Recursos

- Página de inicio y panel de configuración del curso de NVIDIA DLI en español. Esta clase está basada en ellos (Apache-2.0).
- [NVIDIA Build: catálogo de modelos](https://build.nvidia.com/?ncid=ref-dli-146986)
- [Issue #106 de NemoClawDLI: el modelo retirado que devolvía 410](https://github.com/NVDLI/NemoClawDLI/issues/106)
- [Preguntas frecuentes del curso](../../FAQ.md)

---
*Basado en la página de inicio y el panel de configuración del curso de NVIDIA DLI "Securing Agents with OpenShell and NemoClaw" (Apache-2.0).*
