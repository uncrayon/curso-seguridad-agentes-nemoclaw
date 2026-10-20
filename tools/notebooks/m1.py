"""Módulo 1 · notebook de la clase 1.3: el "doctor" del entorno.

Uso:  python3 tools/notebooks/m1.py
Genera: clases/1.3-rutas-de-modelo-y-errores/1.3-rutas-de-modelo-y-errores.ipynb

Corre completo sin key (modo MOCK, con errores simulados) y en vivo con NVIDIA_API_KEY.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from comun import *  # noqa: F401,F403,E402

INTRO = """
Este notebook es el **doctor del curso**: revisa tu entorno de punta a punta y te dice, en español, qué falta y cómo arreglarlo.

Vas a comprobar, una por una, las piezas que usa todo el curso:

1. Tu key `nvapi-` (que exista y tenga buena forma).
2. La ruta de **modelos** (`GET /v1/models`).
3. La ruta de **chat** (`POST /v1/chat/completions`), con latencia y `usage`.
4. Una llamada con **tools** (la base de los módulos 2 y 3).
5. La ruta de **embeddings** (`POST /v1/embeddings`, la base de RAG en la clase 3.2).

Después vas a **romper cosas a propósito** (401, 404 y `finish_reason=length`) para aprender a leer los errores, y vas a escribir un **reintento con backoff** para el 429.

Al final verás uno de dos mensajes: **✅ entorno listo** o una lista de instrucciones precisas.

*Basado en la página de inicio y el panel de configuración del curso de NVIDIA DLI "Securing Agents with OpenShell and NemoClaw" (Apache-2.0).*
"""

EXTRAS = code(r'''
# --- Herramientas del doctor (ejecútala después de las dos celdas anteriores) ---
import time

RESULTADOS = {}   # aquí cada prueba deja su veredicto

def registrar(prueba, estado, detalle, arreglo=""):
    """estado: 'ok' | 'falla' | 'mock'. Imprime una línea y guarda el resultado."""
    icono = {"ok": "✅", "falla": "❌", "mock": "⚪"}[estado]
    RESULTADOS[prueba] = {"estado": estado, "detalle": detalle, "arreglo": arreglo}
    print(f"{icono} {prueba}: {detalle}")
    if arreglo and estado == "falla":
        print(f"   👉 Qué hacer: {arreglo}")

class ErrorSimulado(Exception):
    """Imita un error HTTP de la API (tiene status_code y body, igual que los del SDK de openai)."""
    def __init__(self, status_code, body="(error simulado en modo MOCK)", retry_after=None):
        super().__init__(f"HTTP {status_code}")
        self.status_code, self.body = status_code, body
        self.response = NS(headers={"retry-after": str(retry_after)} if retry_after else {})

def cronometro(fn):
    """Ejecuta fn() y devuelve (resultado, segundos)."""
    t0 = time.perf_counter()
    r = fn()
    return r, time.perf_counter() - t0

# Catálogo simulado (solo se usa en modo MOCK)
MODELOS_MOCK = [MODEL, EMBED_MODEL]

# Reglas del modelo simulado para este notebook
@regla_mock
def _mock_listo(messages, nombres):
    if "palabra: listo" in (messages[-1].get("content") or "").lower():
        return _msg("listo")

@regla_mock
def _mock_tool(messages, nombres):
    if "buscar_faq" in nombres and messages[-1]["role"] == "user":
        return _call("buscar_faq", {"pregunta": messages[-1]["content"]})

if USE_MOCK:
    # En MOCK también simulamos un 404 (modelo inexistente), el corte por max_tokens y un usage aproximado.
    _crear_original = client.chat.completions.create
    def _crear_mock(model=None, messages=None, **kw):
        if model not in MODELOS_MOCK:
            raise ErrorSimulado(404, f"(simulado) Model '{model}' not found")
        r = _crear_original(model=model, messages=messages, **kw)
        palabras = sum(len((m.get("content") or "").split()) for m in messages)
        r.usage = NS(prompt_tokens=int(palabras * 1.4) + 8, completion_tokens=12, total_tokens=int(palabras * 1.4) + 20)
        if kw.get("max_tokens", 4096) < 32:
            r.choices[0].finish_reason = "length"
            r.choices[0].message.content = ""
        return r
    client.chat.completions.create = _crear_mock

print("Doctor listo. Modo:", "MOCK" if USE_MOCK else "EN VIVO")
''')

CELLS = [
    header("1.3", INTRO),
    md("""
## 0 · Configuración

Ejecuta las tres celdas siguientes en orden. La primera busca tu key en este orden:

1. **Colab**: Secrets (icono 🔑 del panel izquierdo), con el nombre `NVIDIA_API_KEY` y el acceso del notebook activado.
2. **Local**: un archivo `.env` en la raíz del repo (copia `.env.example`) o una variable de entorno (`export NVIDIA_API_KEY=...`).

Si no la encuentra, todo corre en **modo MOCK**: verás ⚪ en lugar de ✅ y, al final, las instrucciones para conectarte de verdad.
"""),
    SETUP, MOCK, EXTRAS,

    # ------------------------------------------------------------------ 1. key
    md("""
## 1 · ¿Hay key y tiene buena forma?

La mitad de los problemas del curso empiezan aquí. Los errores típicos al copiar la key son:

- Copiarla **con comillas** (`"nvapi-..."`) o con un espacio o un salto de línea al final.
- Pegar también la palabra `Bearer` delante.
- Pegar solo una parte de la key.

Esta celda revisa todo eso **sin imprimir tu key** (solo muestra el inicio y el final).
"""),
    code('''
def revisar_key(key):
    """Devuelve una lista de problemas de forma. Lista vacía = se ve bien."""
    crudo = os.environ.get("NVIDIA_API_KEY") or ""
    problemas = []
    if crudo != crudo.strip():
        problemas.append("tiene espacios o saltos de línea al inicio o al final")
    if key[:1] in "\\"'" or key[-1:] in "\\"'":
        problemas.append("está entre comillas: quítalas")
    if key.lower().startswith("bearer"):
        problemas.append("empieza con 'Bearer': pega solo la key, el código ya agrega 'Bearer'")
    if "integrate.api.nvidia.com" in BASE_URL and not key.startswith("nvapi-"):
        problemas.append("no empieza con nvapi-")
    if " " in key:
        problemas.append("tiene espacios en medio: ¿pegaste dos cosas juntas?")
    return problemas

def enmascarar(key):
    return key[:6] + "…" + key[-4:] if len(key) > 12 else "(muy corta)"

if USE_MOCK:
    registrar("key", "mock", "no hay NVIDIA_API_KEY en este entorno (modo MOCK)",
              "crea tu key en la clase 1.2 y guárdala en Colab Secrets, en .env o con export")
else:
    problemas = revisar_key(API_KEY)
    if problemas:
        registrar("key", "falla", f"{enmascarar(API_KEY)} → " + "; ".join(problemas),
                  "copia de nuevo la key desde build.nvidia.com y reinicia el kernel")
    else:
        registrar("key", "ok", f"{enmascarar(API_KEY)} ({len(API_KEY)} caracteres)")
'''),

    # ------------------------------------------------------------------ 2. panel
    md("""
## 2 · El panel de configuración del curso de NVIDIA (y su equivalente aquí)

En el curso web de NVIDIA, la configuración vive en la página de inicio (sección **"Cómo introducir tu clave de API"**) y también aparece en la lección 1a. Estos son sus campos y lo que significan en este notebook:

| Campo en el panel de NVIDIA | Valor por defecto | Qué es | Aquí, en Python |
|---|---|---|---|
| **URL base de la API de chat** (*Chat API base URL*) | `https://integrate.api.nvidia.com/v1` | A dónde se mandan las llamadas de chat. Debe ser HTTPS y terminar en `/v1` | `BASE_URL` / `NVIDIA_BASE_URL` |
| **ID del modelo de chat** (*Chat model ID*) | `nvidia/nemotron-3.5-lightning-30b-a3b` | El modelo que responde. Se copia exacto del catálogo | `MODEL` / `NVIDIA_MODEL` |
| **Clave bearer** | — (empieza con `nvapi-`) | Tu key. En la página de NVIDIA se guarda en `sessionStorage`: **se borra al cerrar la pestaña** | `API_KEY` / `NVIDIA_API_KEY` |
| **Usar el relay de navegador de NVIDIA DLI** (casilla) | Activado en la página del curso | Un relay de CORS: reenvía tus llamadas a la API de NVIDIA para que una página estática pueda hacerlas desde el navegador. No te da key ni acceso a modelos | No hace falta: Python no tiene restricciones de CORS |
| **Ruta de embeddings** (sección desplegable) | `https://integrate.api.nvidia.com/v1` + `nvidia/nemotron-3-embed-1b` | Ruta independiente para convertir texto en vectores (RAG). Si no pones otra key, usa la del chat | `EMBED_MODEL` / `NVIDIA_EMBED_MODEL` |
| **Gestión de la solicitud** (sección desplegable) | espera 60 s (5–300) · reintentos 0 (0–5) | Cuánto esperar una respuesta y cuántas veces reintentar. Los reintentos solo aplican a fallas de red, 429 y 5xx | `OpenAI(timeout=60, max_retries=2)` |
| Botón **Guardar y verificar** (*Save & verify*) | — | Revisa que la key empiece con `nvapi-` y hace una llamada de prueba: *"Reply with the single word: ready"* | Este notebook completo |

Dos ideas para llevarte:

- Más tiempo de espera o más reintentos **nunca** arreglan una key inválida (401/403).
- Si cierras la pestaña del curso de NVIDIA, tienes que volver a pegar la key. La URL y el modelo sí se quedan guardados (en `localStorage`).
"""),
    code('''
# Tu configuración actual, con los nombres del panel de NVIDIA
panel = {
    "URL base de la API de chat": BASE_URL,
    "ID del modelo de chat": MODEL,
    "Clave bearer": "(no configurada → MOCK)" if USE_MOCK else enmascarar(API_KEY),
    "Ruta de embeddings": f"{BASE_URL} · {EMBED_MODEL}",
    "Gestión de la solicitud": "timeout=60 s · max_retries=2 (definidos en la celda del cliente)",
}
for campo, valor in panel.items():
    print(f"{campo:28s} {valor}")

if not BASE_URL.rstrip("/").endswith("/v1"):
    print("\\n⚠  BASE_URL no termina en /v1. Casi seguro vas a ver 404 en todas las llamadas.")
'''),

    # ------------------------------------------------------------------ 3. models
    md("""
## 3 · Ruta de modelos: `GET /v1/models`

Es la llamada más barata: no gasta tokens. Sirve para dos cosas:

- Confirmar que llegas al endpoint.
- Confirmar que el **ID exacto** de tu modelo existe. La mayoría de los 404 son un ID mal copiado.
"""),
    code('''
def listar_modelos():
    if USE_MOCK:
        return list(MODELOS_MOCK)
    return [m.id for m in client.models.list().data]

try:
    ids, seg = cronometro(listar_modelos)
    print(f"{len(ids)} modelos en {seg:.2f} s. Algunos de NVIDIA:")
    for i in [x for x in ids if x.startswith("nvidia/")][:8]:
        print("  ·", i)
    if MODEL in ids:
        registrar("modelos", "mock" if USE_MOCK else "ok", f"/models responde y {MODEL} está en el catálogo")
    else:
        parecidos = [x for x in ids if MODEL.split("/")[-1][:12] in x]
        registrar("modelos", "falla", f"{MODEL} no aparece en /models",
                  f"copia el ID exacto del catálogo. Parecidos: {parecidos[:3] or 'ninguno'}")
    if EMBED_MODEL not in ids:
        print(f"⚠  {EMBED_MODEL} no aparece en /models. Puede ser normal: la prueba de embeddings (sección 6) es la que manda.")
except Exception as e:
    registrar("modelos", "falla", "no se pudo listar /models", diagnostico(e))
'''),

    # ------------------------------------------------------------------ 4. chat
    md("""
## 4 · Ruta de chat: una llamada, su latencia y su `usage`

Hacemos la misma prueba que el botón **Guardar y verificar** del curso de NVIDIA: pedirle al modelo que responda una sola palabra.

Fíjate en tres cosas de la respuesta:

- `finish_reason`: por qué paró el modelo (`stop` = terminó bien).
- `usage`: los tokens que gastaste (`prompt_tokens` de entrada y `completion_tokens` de salida). Es lo que consume tu cuota.
- La **latencia**: cuántos segundos tardó. Es útil para comparar modelos y detectar cuándo algo va lento.

> El modelo del curso **razona antes de responder** y ese razonamiento también gasta tokens. Por eso usamos `max_tokens` generoso.
"""),
    code('''
try:
    r, seg = cronometro(lambda: chat([{"role": "user", "content": "Responde solo con la palabra: listo"}], max_tokens=1024))
    ch = r.choices[0]
    print("Respuesta     :", repr(ch.message.content))
    print("finish_reason :", ch.finish_reason)
    print("usage         :", f"entrada={r.usage.prompt_tokens} · salida={r.usage.completion_tokens} · total={r.usage.total_tokens}",
          "(estimado en MOCK)" if USE_MOCK else "")
    razonamiento = getattr(ch.message, "reasoning_content", None)
    if razonamiento:
        print("razonamiento  :", len(razonamiento), "caracteres (no forman parte de la respuesta)")
    print(f"latencia      : {seg:.2f} s")
    LATENCIAS = {"chat": seg}
    if ch.finish_reason == "stop" and ch.message.content:
        registrar("chat", "mock" if USE_MOCK else "ok", f"respondió en {seg:.2f} s")
    else:
        registrar("chat", "falla", f"finish_reason={ch.finish_reason} y contenido={ch.message.content!r}",
                  "si es 'length', sube max_tokens; si no, vuelve a ejecutar la celda una vez")
except RuntimeError as e:
    LATENCIAS = {}
    registrar("chat", "falla", "la llamada de chat falló", str(e))
'''),

    # ------------------------------------------------------------------ 5. tools
    md("""
## 5 · Una llamada con tools

Desde la clase 2.2 el agente va a pedir herramientas. Aquí comprobamos que tu modelo **sabe pedirlas**: le ofrecemos una tool `buscar_faq` (la misma que tendrá nuestro proyecto Soporte NemoClaw en la clase 2.3) y esperamos que responda con `finish_reason="tool_calls"`.

Ojo: el modelo **no ejecuta** nada. Solo devuelve el nombre de la tool y sus argumentos en JSON. Ejecutarla es trabajo de tu código (eso lo construyes en el Módulo 2).
"""),
    code('''
TOOLS = [{
    "type": "function",
    "function": {
        "name": "buscar_faq",
        "description": "Busca en las preguntas frecuentes del curso. Úsala para cualquier duda sobre API keys, Brev o NemoClaw.",
        "parameters": {
            "type": "object",
            "properties": {"pregunta": {"type": "string", "description": "La duda del estudiante, en sus palabras"}},
            "required": ["pregunta"],
        },
    },
}]

try:
    r, seg = cronometro(lambda: chat([{"role": "user", "content": "¿Qué hago si mi key me da error 401?"}], tools=TOOLS))
    ch = r.choices[0]
    print("finish_reason:", ch.finish_reason, f"· {seg:.2f} s")
    if ch.message.tool_calls:
        tc = ch.message.tool_calls[0]
        args = json.loads(tc.function.arguments)        # si esto falla, el modelo devolvió JSON inválido
        print("tool pedida  :", tc.function.name, args)
        registrar("tools", "mock" if USE_MOCK else "ok", f"el modelo pidió {tc.function.name} con argumentos JSON válidos")
    else:
        registrar("tools", "falla", f"el modelo respondió texto en vez de pedir la tool: {ch.message.content!r:.80}",
                  "vuelve a ejecutar una vez; si persiste, usa el modelo por defecto del curso (algunos modelos no soportan tools)")
except (RuntimeError, json.JSONDecodeError) as e:
    registrar("tools", "falla", "la llamada con tools falló", str(e))
'''),

    # ------------------------------------------------------------------ 6. embeddings
    md("""
## 6 · Ruta de embeddings

Un embedding convierte un texto en un vector de números. Textos con significado parecido quedan cerca. Lo usarás en RAG (clase 3.2).

Los modelos de embeddings de NVIDIA piden un `input_type`:

- `query` para preguntas.
- `passage` para documentos.

La función `embed()` ya lo manda por ti.
"""),
    code('''
def coseno(a, b):
    num = sum(x * y for x, y in zip(a, b))
    return num / ((math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))) or 1)

try:
    (q,), seg = cronometro(lambda: embed("¿Cómo genero mi API key de NVIDIA?", input_type="query"))
    docs = embed(["Para generar tu API key entra a build.nvidia.com y abre API Keys.",
                  "Receta de pozole rojo con maíz cacahuazintle."], input_type="passage")
    print(f"vector de {len(q)} dimensiones en {seg:.2f} s")
    print(f"similitud con el texto sobre la key : {coseno(q, docs[0]):.3f}")
    print(f"similitud con la receta de pozole   : {coseno(q, docs[1]):.3f}   (debería ser menor)")
    registrar("embeddings", "mock" if USE_MOCK else "ok", f"vector de {len(q)} dimensiones")
except RuntimeError as e:
    registrar("embeddings", "falla", f"la ruta de embeddings falló ({EMBED_MODEL})", str(e))
'''),

    # ------------------------------------------------------------------ 7. errores
    md("""
## 7 · 🧯 Cuando algo falla: rompe tu entorno a propósito

La mejor forma de no entrar en pánico ante un error es haberlo visto antes. Vamos a provocar tres fallos reales y a leerlos con `diagnostico()`, la función del curso que traduce cada error a "qué pasó + qué hacer".

| Lo que rompemos | Error esperado |
|---|---|
| Una key falsa | **401** |
| Un modelo que no existe | **404** |
| `max_tokens` diminuto | No es una excepción: llega una respuesta con `finish_reason="length"` |

En modo MOCK los errores son simulados, pero el diagnóstico es el mismo.
"""),
    code('''
# 7.1 · Key falsa → 401
from openai import OpenAI

def llamar_con_key_falsa():
    if USE_MOCK:
        raise ErrorSimulado(401, "(simulado) Unauthorized")
    falso = OpenAI(base_url=BASE_URL, api_key="nvapi-ESTA-KEY-ES-FALSA-000000000000", max_retries=0, timeout=30)
    return falso.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": "hola"}], max_tokens=16)

try:
    llamar_con_key_falsa()
    print("Raro: la key falsa funcionó. ¿BASE_URL apunta a un servidor sin autenticación?")
except Exception as e:
    print("Status:", getattr(e, "status_code", "?"))
    print(diagnostico(e))
'''),
    code('''
# 7.2 · Modelo inexistente → 404
try:
    chat([{"role": "user", "content": "hola"}], model="nvidia/modelo-que-no-existe", max_tokens=16)
except RuntimeError as e:
    print(e)
'''),
    code('''
# 7.3 · max_tokens diminuto → finish_reason="length"
r = chat([{"role": "user", "content": "Explica qué es un agente de IA."}], max_tokens=8)
ch = r.choices[0]
print("finish_reason:", ch.finish_reason)
print("contenido    :", repr(ch.message.content))
print("\\nNo es una excepción: la API respondió 200, pero el modelo se quedó sin tokens.")
print("Con un modelo que razona, a veces el contenido llega VACÍO porque gastó todo pensando.")
print("Arreglo: sube max_tokens (el curso usa 4096 por defecto en chat()).")
'''),
    md("""
### Tabla de errores de la API

Guárdala. Es la misma lógica que usa `diagnostico()`.

| Código | Qué significa | ¿Reintentar? | Qué hacer |
|---|---|---|---|
| **401** | La key fue rechazada | ❌ Nunca | Revisa que sea la key completa, que empiece con `nvapi-`, sin comillas ni espacios. Si la regeneraste, la vieja ya no sirve |
| **403** | La key es válida, pero no tiene acceso a ese modelo o a esa ruta | ❌ | Revisa tu cuenta en build.nvidia.com o usa otro modelo |
| **404** | El modelo o la ruta no existen | ❌ | Copia el ID exacto con `/v1/models` y revisa que `BASE_URL` termine en `/v1` |
| **410** | El modelo fue retirado del endpoint gratuito | ❌ | Cambia a un modelo vigente del catálogo. Ya pasó en el curso de NVIDIA con `nvidia/nemotron-3-nano-30b-a3b` |
| **429** | Demasiadas solicitudes: te frenó el límite de uso | ✅ Con espera | Espera y reintenta con backoff (sección 8). No ejecutes celdas en ráfaga |
| **5xx** | Falla del lado del servidor o el modelo está arrancando | ✅ Con espera | Reintenta en 30–60 s; si persiste, prueba otro modelo |
| `finish_reason="length"` | El modelo se quedó sin `max_tokens` | — | Sube `max_tokens` |
| Timeout / sin conexión | No llegó respuesta a tiempo o no hay red | ✅ | Revisa internet, VPN o proxy y `BASE_URL`; reintenta |
"""),

    # ------------------------------------------------------------------ 8. backoff
    md("""
## 8 · Reintento con backoff para el 429

Cuando la API responde **429**, lo correcto es **esperar y reintentar**, y esperar cada vez más (backoff exponencial: 1 s, 2 s, 4 s…). Si el servidor manda el encabezado `Retry-After`, se respeta.

Dos reglas:

- Solo se reintentan **429, 5xx y fallas de red**. Un 401 nunca se arregla solo.
- Siempre con un **límite** de intentos. Un loop infinito de reintentos quema tu cuota.

> El cliente `openai` ya reintenta 2 veces por su cuenta (`max_retries=2`). Esta función es para entender el mecanismo y para cuando necesites más control.
"""),
    code('''
import random

def debe_reintentarse(e):
    status = getattr(e, "status_code", None)
    if status is None:                                   # sin status: ¿falla de red o timeout?
        return any(p in type(e).__name__ for p in ("Timeout", "Connection"))
    return status == 429 or 500 <= status < 600

def con_reintentos(fn, intentos=4, base=1.0, tope=30.0):
    """Ejecuta fn(). Si falla con un error reintentable, espera (backoff exponencial + jitter) y reintenta."""
    for intento in range(1, intentos + 1):
        try:
            return fn()
        except Exception as e:
            if not debe_reintentarse(e) or intento == intentos:
                print(f"   ✋ No reintento (intento {intento}): {diagnostico(e).splitlines()[0]}")
                raise
            espera = min(tope, base * 2 ** (intento - 1)) + random.uniform(0, base / 4)
            headers = getattr(getattr(e, "response", None), "headers", None) or {}
            if headers.get("retry-after"):
                espera = min(tope, float(headers["retry-after"]))
            print(f"   ⏳ intento {intento} falló con {getattr(e, 'status_code', type(e).__name__)}; espero {espera:.2f} s")
            time.sleep(espera)
'''),
    code('''
# Demo con un servicio simulado que responde 429 dos veces y luego funciona
llamadas = {"n": 0}
def servicio_saturado():
    llamadas["n"] += 1
    if llamadas["n"] <= 2:
        raise ErrorSimulado(429, "(simulado) Too Many Requests")
    return "respuesta al tercer intento"

print("Caso 429:", con_reintentos(servicio_saturado, base=0.2))

# Un 401 NO se reintenta: falla de inmediato
print("\\nCaso 401:")
def key_mala():
    raise ErrorSimulado(401, "(simulado) Unauthorized")
try:
    con_reintentos(key_mala, base=0.2)
except ErrorSimulado:
    print("   Correcto: el 401 no se reintentó.")
'''),
    code('''
# En vivo: tu ping de chat, protegido con reintentos (usa el cliente directo para ver el status real)
if USE_MOCK:
    print("⚪ En MOCK no hay llamada real. Con tu key, esta celda hace un ping con reintentos.")
else:
    r = con_reintentos(lambda: client.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": "Responde solo con la palabra: listo"}], max_tokens=1024))
    print("Respuesta con reintentos:", r.choices[0].message.content)
'''),

    # ------------------------------------------------------------------ 9. tu turno
    md("""
## 9 · ✏️ Tu turno

**1. Compara modelos.** Cambia `OTRO_MODELO` por otro ID de la lista de la sección 3 (por ejemplo, uno más grande) y compara latencia y tokens. ¿Vale la pena el modelo grande para responder "listo"?
"""),
    code('''
OTRO_MODELO = MODEL        # ✏️ pon aquí otro ID del catálogo

for modelo in [MODEL, OTRO_MODELO]:
    try:
        r, seg = cronometro(lambda: chat([{"role": "user", "content": "Responde solo con la palabra: listo"}], model=modelo, max_tokens=1024))
        print(f"{modelo:45s} {seg:5.2f} s · {r.usage.total_tokens} tokens · {r.choices[0].message.content!r}")
    except RuntimeError as e:
        print(f"{modelo:45s} ❌ {str(e).splitlines()[0]}")
'''),
    md("""
**2. Clasifica errores.** Completa `que_hago(status)` para que devuelva `"reintentar"`, `"arreglar key"`, `"arreglar modelo"` o `"revisar cuenta"`. La celda te dice cuántas aciertas. Usa la tabla de la sección 7.
"""),
    code('''
def que_hago(status):
    # ✏️ Completa con if/elif. Ahora todo devuelve "reintentar", y eso es un error caro con un 401.
    return "reintentar"

casos = {401: "arreglar key", 403: "revisar cuenta", 404: "arreglar modelo",
         410: "arreglar modelo", 429: "reintentar", 503: "reintentar"}
aciertos = sum(que_hago(s) == esperado for s, esperado in casos.items())
for s, esperado in casos.items():
    print(f"{s}: tu respuesta={que_hago(s)!r:20s} esperada={esperado!r}  {'✅' if que_hago(s) == esperado else '❌'}")
print(f"\\n{aciertos}/{len(casos)} correctas")
'''),

    # ------------------------------------------------------------------ 10. proyecto
    md("""
## 10 · Avance del proyecto: el reporte de entorno de Soporte NemoClaw

Nuestro proyecto del curso es **Soporte NemoClaw**, un agente que responde dudas de estudiantes. La duda número uno siempre es "no me funciona la API". Por eso su primera pieza es un **reporte de entorno**: un resumen sin secretos que el estudiante puede pegar al pedir ayuda.

En la clase 3.3, los subagentes de Soporte NemoClaw van a leer reportes como este para armar un diagnóstico. Guárdalo.
"""),
    code('''
import platform, datetime

def reporte_entorno():
    """Resumen del entorno SIN la key: seguro para pegar en un foro o en un issue."""
    return {
        "fecha": datetime.datetime.now().isoformat(timespec="seconds"),
        "python": platform.python_version(),
        "colab": "google.colab" in sys.modules,
        "modo": "MOCK" if USE_MOCK else "EN VIVO",
        "base_url": BASE_URL,
        "modelo_chat": MODEL,
        "modelo_embeddings": EMBED_MODEL,
        "key": "ausente" if USE_MOCK else ("forma ok" if not revisar_key(API_KEY) else "forma incorrecta"),
        "pruebas": {k: v["estado"] for k, v in RESULTADOS.items()},
        "latencia_chat_s": round(LATENCIAS.get("chat", 0), 2),
    }

REPORTE = reporte_entorno()
texto = json.dumps(REPORTE, ensure_ascii=False, indent=2)
assert API_KEY == "" or API_KEY not in texto, "¡El reporte nunca debe contener la key!"
print(texto)
'''),

    # ------------------------------------------------------------------ 11. veredicto
    md("## 11 · Veredicto del doctor"),
    code('''
PRUEBAS = ["key", "modelos", "chat", "tools", "embeddings"]
fallas = [p for p in PRUEBAS if RESULTADOS.get(p, {}).get("estado") != "ok"]

if not USE_MOCK and not fallas:
    print("✅ entorno listo")
    print(f"   Modelo {MODEL} · latencia de chat {LATENCIAS.get('chat', 0):.2f} s · embeddings OK.")
    print("   Ya puedes empezar el Módulo 2.")
elif USE_MOCK:
    print("⚪ El notebook funciona, pero tu entorno TODAVÍA NO está listo: no encontré NVIDIA_API_KEY.\\n")
    print("Haz UNA de estas opciones y vuelve a ejecutar todo (Entorno de ejecución → Reiniciar y ejecutar todo):")
    print("  • Colab : icono 🔑 (Secrets) → nombre NVIDIA_API_KEY → pega tu key → activa 'Acceso del notebook'.")
    print("  • Local : copia .env.example como .env en la raíz del repo y pega tu key en NVIDIA_API_KEY.")
    print("  • Terminal: export NVIDIA_API_KEY=nvapi-...  y abre Jupyter desde esa misma terminal.")
    print("¿Aún no tienes key? Mira la clase 1.2.")
else:
    print(f"❌ Tu entorno no está listo: fallaron {len(fallas)} prueba(s). Arréglalas en este orden:\\n")
    for p in fallas:
        r = RESULTADOS.get(p, {"detalle": "no se ejecutó", "arreglo": "ejecuta todas las celdas en orden"})
        print(f"• {p}: {r['detalle']}")
        print(f"  👉 {r['arreglo'] or 'vuelve a ejecutar la celda de esa sección'}\\n")
    print("Si sigues atorado, pega el REPORTE de la sección 10 (no tiene tu key) al pedir ayuda.")
'''),
    md("""
## Reto

Convierte este notebook en **una sola función** `doctor()` que corra las cinco pruebas y devuelva el reporte.

**Criterio de éxito:**

1. Con tu configuración normal, `doctor()` termina en "✅ entorno listo".
2. Si cambias `MODEL = "nvidia/nemotron-3.5-lightning"` (un ID incompleto) y la vuelves a ejecutar, el reporte marca `modelos` y `chat` como falla y el arreglo menciona el ID exacto.
3. El reporte nunca contiene tu key.

Pista: reutiliza `registrar()`, `listar_modelos()`, `chat()`, `embed()` y `reporte_entorno()`.

---
*Basado en la página de inicio del curso de NVIDIA DLI "Securing Agents with OpenShell and NemoClaw" (Apache-2.0). Adaptación al español para Platzi.*
"""),
]

write("1.3", CELLS)
