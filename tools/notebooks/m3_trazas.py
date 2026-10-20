"""Módulo 3 · notebook de la clase 3.4 (observabilidad: trazas con OpenTelemetry y Phoenix).

Uso:  python3 tools/notebooks/m3_trazas.py
Genera:  clases/3.4-observabilidad-y-trazas/3.4-observabilidad-y-trazas.ipynb

Corre completo sin key (modo MOCK) y sin Phoenix: las trazas se guardan en memoria y se dibujan
como árbol en el notebook. Si hay un Phoenix escuchando (http://localhost:6006 o
PHOENIX_COLLECTOR_ENDPOINT), las mismas trazas también se envían ahí.
Reutiliza la FAQ y el índice RAG de las clases 3.2 y 3.3 (tools/notebooks/m3.py).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from comun import *  # noqa: F401,F403,E402
from m3 import AYUDAS, FAQ_CELDA, INDICE_COMPACTO  # noqa: E402

MOCK_34 = code(r'''
# --- Reglas del modelo simulado para ESTE notebook (solo se usan sin API key) -----
# No necesitas leerlas. Imitan a un agente de soporte con herramientas y, a propósito,
# reproducen los tres errores que vas a cazar con las trazas: herramienta que falla,
# loop atascado y cita inventada.
_ID = re.compile(r"\[([\w.\-]+\.md#[\w\-]+)\]")

def _ids_en(textos):
    vistos = []
    for t in textos:
        for i in _ID.findall(t or ""):
            if i not in vistos:
                vistos.append(i)
    return vistos

def _primera_respuesta(texto):
    m = re.search(r"\nR: (.+)", texto or "")
    return _primeras(m.group(1), 2) if m else ""

@regla_mock
def _mock_soporte_trazado(messages, nombres):
    if _rol(messages) != "soporte-trazado":
        return None
    pregunta = next((m["content"] for m in messages if m["role"] == "user"), "")
    p = pregunta.lower()
    salidas = [m["content"] for m in messages if m["role"] == "tool"]
    n = len(salidas)
    # Caso loop: una pregunta que la FAQ no cubre; el "modelo" repite la misma búsqueda
    if "factura" in p:
        return _call("buscar_faq", {"consulta": "factura de Brev en pesos mexicanos", "k": 3})
    # Caso cita inventada: responde con una cita real y una que no salió de ninguna herramienta
    if "gratis para siempre" in p:
        if n == 0:
            return _call("buscar_faq", {"consulta": "créditos de Brev gratis launchable", "k": 2})
        reales = _ids_en(salidas)[:1]
        citas = " ".join(f"[{i}]" for i in reales + ["brev.md#la-gpu-es-gratis-para-siempre"])
        return _msg("**Qué pasa:** el launchable incluye GPU gratis para siempre, sin límite de horas.\n"
                    f"**Fuente:** {citas}")
    # Caso laboratorio: primero revisa la instancia y luego busca en la FAQ
    sobre_lab = any(w in p for w in ("laboratorio", "instancia", "brev"))
    if sobre_lab and n == 0:
        return _call("estado_laboratorio", {"instancia": "mi-lab"})
    if n == (1 if sobre_lab else 0):
        # Un buen agente reformula la búsqueda con lo que ya observó
        if sobre_lab:
            consulta = "cookie de acceso vencida al reanudar el launchable"
        elif "401" in p:
            consulta = "error 401 key rechazada notebook"
        else:
            consulta = pregunta[:90]
        return _call("buscar_faq", {"consulta": consulta, "k": 3})
    # Respuesta final: lo que dijeron las herramientas, con sus citas
    ids = _ids_en(salidas)[:2]
    estado = next((s for s in salidas if s.startswith("{") or s.startswith("ERROR")), "")
    partes = []
    if estado.startswith("ERROR"):
        partes.append("No pude verificar el estado de tu instancia (la herramienta falló).")
    elif "vencida" in estado:
        partes.append("Tu instancia está RUNNING, pero la cookie de sesión del laboratorio venció al reanudar.")
    if ids:
        partes.append("**Qué pasa:** " + _primera_respuesta(next(s for s in salidas if "[" in s)))
        partes.append("**Fuente:** " + " ".join(f"[{i}]" for i in ids))
    else:
        partes.append("La FAQ no cubre esto.")
    return _msg("\n".join(partes))

print("Reglas mock de la clase 3.4 listas")
''')

NB34 = [
    header("3.4", """
Tu agente ya enruta, busca en la FAQ y lanza subagentes. Cuando algo sale mal, `print` ya no alcanza: no sabes **qué paso** falló, **con qué argumentos**, **cuánto tardó** ni **de dónde salió** una cita. En este notebook le pones **trazas** a tu agente de soporte:

1. **Instrumentar** el loop con OpenTelemetry: un *span* por el agente, por cada llamada al modelo y por cada herramienta.
2. **Ver** la traza como árbol aquí mismo y, si lo tienes corriendo, en **Phoenix**.
3. **Depurar** tres errores reales solo con la traza: una herramienta que falla, un loop atascado y una cita inventada. Y encontrar el paso lento.
4. **Proteger** la traza: tachar las keys antes de guardarla, porque una traza guarda prompts completos.

Lo aplicas al proyecto **Soporte NemoClaw**: cada respuesta del agente queda con su traza, lista para adjuntar a un reporte de error.

*Clase nueva de la adaptación de Platzi: no tiene lección equivalente en el curso de NVIDIA DLI. Usa estándares abiertos (OpenTelemetry, OpenInference) y Arize Phoenix, que también es uno de los destinos del NeMo Agent Toolkit de NVIDIA.*
"""),
    SETUP, MOCK, AYUDAS, MOCK_34,
    md("""
## 1 · Por qué `print` no alcanza
Un agente toma decisiones en varios pasos. Cuando la respuesta final está mal, la causa puede estar en cualquiera:

| Pregunta al depurar | Dónde está la respuesta |
|---|---|
| ¿Qué herramienta llamó y con qué argumentos? | Span de la herramienta (`TOOL`) |
| ¿Qué le mandamos al modelo y qué contestó? | Span de la llamada (`LLM`) |
| ¿Qué fragmentos recuperó la búsqueda y con qué puntaje? | Span de recuperación (`RETRIEVER`) |
| ¿Qué paso tardó más? ¿Cuántos tokens gastó? | Duración y atributos de cada span |
| ¿Dónde se rompió? | El span marcado con **error** |

Vocabulario mínimo:
- **Traza:** todo lo que pasó para responder **una** pregunta. Es un árbol.
- **Span:** una operación dentro de la traza, con inicio, fin, atributos y estado (ok o error). Cada span tiene un padre, salvo la raíz.
- **OpenTelemetry (OTel):** el estándar abierto para producir y enviar trazas. No depende de ningún proveedor.
- **OpenInference:** convenciones sobre OTel para aplicaciones de IA: `openinference.span.kind` = `AGENT`, `LLM`, `TOOL`, `RETRIEVER`, `CHAIN`...
- **Phoenix** (Arize, código abierto): una interfaz que recibe trazas OTel y las muestra como árbol, con filtros y métricas.

## 2 · La FAQ y la herramienta de búsqueda (clases 3.2 y 3.3)
"""),
    FAQ_CELDA,
    INDICE_COMPACTO,
    md("""
## 3 · Configura el tracer
Usamos el SDK de OpenTelemetry con **dos destinos**:
- **En memoria** (siempre): para dibujar la traza aquí y analizarla con código. No necesitas nada más.
- **Phoenix** (si lo encuentra): exporta por OTLP/HTTP a `http://localhost:6006/v1/traces` o a la URL de `PHOENIX_COLLECTOR_ENDPOINT`.

Para levantar Phoenix en tu máquina, en otra terminal: `pip install arize-phoenix` y `phoenix serve` (o `docker run -p 6006:6006 arizephoenix/phoenix:latest`). Luego vuelve a ejecutar esta celda. En Colab, deja que use solo la memoria: todo el notebook funciona igual.
"""),
    code(r'''
# --- Tracer de OpenTelemetry: memoria siempre, Phoenix si está disponible -----------
_instala("opentelemetry-sdk", "opentelemetry.sdk")
_instala("opentelemetry-exporter-otlp-proto-http", "opentelemetry.exporter.otlp.proto.http")
import socket
from urllib.parse import urlparse
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, BatchSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import Status, StatusCode

PROYECTO = "soporte-nemoclaw"

def _phoenix_url():
    """URL del colector de Phoenix, o None si no hay uno escuchando."""
    url = os.environ.get("PHOENIX_COLLECTOR_ENDPOINT", "").strip()
    if url:
        return url.rstrip("/") + ("" if url.rstrip("/").endswith("/v1/traces") else "/v1/traces")
    u = urlparse("http://localhost:6006")
    try:
        socket.create_connection((u.hostname, u.port), timeout=0.3).close()
        return "http://localhost:6006/v1/traces"
    except OSError:
        return None

MEMORIA = InMemorySpanExporter()
# openinference.project.name agrupa las trazas por proyecto en Phoenix
PROVEEDOR = TracerProvider(resource=Resource.create({"service.name": PROYECTO, "openinference.project.name": PROYECTO}))
PROVEEDOR.add_span_processor(SimpleSpanProcessor(MEMORIA))
PHOENIX = _phoenix_url()
if PHOENIX:
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    cabeceras = {"authorization": f"Bearer {os.environ['PHOENIX_API_KEY']}"} if os.environ.get("PHOENIX_API_KEY") else {}
    PROVEEDOR.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=PHOENIX, headers=cabeceras)))
tracer = PROVEEDOR.get_tracer("curso.soporte")
print("Trazas en memoria: sí · Phoenix:", PHOENIX or "no detectado (todo funciona igual, solo sin la interfaz web)")
''' ),
    md("""
## 4 · Tacha los secretos antes de guardar
Una traza guarda **prompts completos**. Si un estudiante pega su key en el chat, la key termina en tu herramienta de observabilidad, en texto plano. Por eso **todo** atributo pasa por `redactar()` antes de guardarse. Es la misma regla de la clase 1.2, aplicada a la observabilidad.
"""),
    code(r'''
_SECRETOS = [
    (re.compile(r"nvapi-[A-Za-z0-9_\-]{8,}"), "nvapi-***"),
    (re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]{8,}"), "Bearer ***"),
    (re.compile(r"(?i)(cookie|token|password|contraseña)(\s*[:=]\s*)\S+"), r"\1\2***"),
]
MAX_ATRIBUTO = 4000     # los colectores recortan atributos enormes; mejor recortar nosotros

def redactar(valor):
    texto = valor if isinstance(valor, str) else json.dumps(valor, ensure_ascii=False, default=str)
    for patron, reemplazo in _SECRETOS:
        texto = patron.sub(reemplazo, texto)
    return texto if len(texto) <= MAX_ATRIBUTO else texto[:MAX_ATRIBUTO] + f"… (+{len(texto) - MAX_ATRIBUTO} caracteres)"

def poner(span, **atributos):
    """Pone atributos en un span, redactados. Los nombres con '_' se convierten a '.' (input_value -> input.value)."""
    for k, v in atributos.items():
        if v is None:
            continue
        clave = k.replace("__", "·").replace("_", ".").replace("·", "_")
        span.set_attribute(clave, v if isinstance(v, (int, float, bool)) else redactar(v))

print(redactar("mi key es nvapi-AbCdEf1234567890xyz y mi cookie=abc123def456"))
'''),
    md("""
## 5 · Instrumenta las tres piezas del agente
- **`llamar_trazado`**: cada llamada al modelo es un span `LLM` con el modelo, los mensajes de entrada, la salida, `finish_reason` y los tokens.
- **`buscar_faq_trazado`**: la búsqueda es un span `RETRIEVER` con cada documento recuperado y su puntaje.
- **`estado_laboratorio`**: una herramienta simulada que consulta tu instancia de Brev. Le puedes **inyectar fallas** (`FALLAS`) para practicar.
"""),
    code(r'''
FALLAS = {"estado_laboratorio": None}     # None | "503" | "lento"

def _tokens(r, mensajes):
    u = getattr(r, "usage", None)
    if u and getattr(u, "total_tokens", 0):
        return u.prompt_tokens, u.completion_tokens
    # MOCK: la respuesta simulada no trae tokens; estimamos ≈ 4 caracteres por token
    entrada = sum(len(str(m.get("content") or "")) for m in mensajes) // 4
    m = r.choices[0].message
    salida = len((m.content or "") + json.dumps([t.function.arguments for t in (m.tool_calls or [])])) // 4
    return entrada, salida

def llamar_trazado(mensajes, herramientas=None, paso=0):
    with tracer.start_as_current_span(f"llm · paso {paso}") as s:
        poner(s, openinference_span_kind="LLM", llm_model__name=MODEL,
              input_value=mensajes[-3:], input_mime__type="application/json",
              llm_invocation__parameters={"temperature": 0, "tools": [t["function"]["name"] for t in herramientas or []]})
        t0 = time.time()
        if USE_MOCK:
            time.sleep(LATENCIA_MOCK)
        try:
            r = chat(mensajes, tools=herramientas, temperature=0)
        except Exception as e:
            s.record_exception(e)
            s.set_status(Status(StatusCode.ERROR, str(e).splitlines()[0]))
            raise
        m = r.choices[0].message
        entrada, salida = _tokens(r, mensajes)
        poner(s, output_value=m.content or [{"tool": t.function.name, "args": t.function.arguments} for t in m.tool_calls or []],
              llm_finish__reason=r.choices[0].finish_reason,
              llm_token__count_prompt=entrada, llm_token__count_completion=salida,
              llm_token__count_total=entrada + salida)
        LLAMADAS.append(("soporte-trazado", round(time.time() - t0, 2)))
        return r

def buscar_faq_trazado(consulta, k=3):
    with tracer.start_as_current_span("retriever · buscar_faq") as s:
        poner(s, openinference_span_kind="RETRIEVER", input_value=consulta, tool_name="buscar_faq")
        if not isinstance(consulta, str) or not consulta.strip():
            s.set_status(Status(StatusCode.ERROR, "consulta vacía"))
            return "ERROR: 'consulta' debe ser texto no vacío"
        hits = INDICE.buscar(consulta, k=max(1, min(int(k), 5)), minimo=MIN_SCORE)
        for i, h in enumerate(hits):
            poner(s, **{f"retrieval_documents_{i}_document_id": h["id"],
                        f"retrieval_documents_{i}_document_score": h["score"],
                        f"retrieval_documents_{i}_document_content": h["respuesta"][:300]})
        salida = armar_contexto(hits) if hits else "SIN_EVIDENCIA: ningún fragmento supera el umbral."
        poner(s, output_value=salida)
        return salida

def estado_laboratorio(instancia):
    """Herramienta simulada: el estado de tu instancia de Brev."""
    if not isinstance(instancia, str) or not instancia.strip():
        return "ERROR: 'instancia' debe ser el nombre de tu instancia (texto)"
    if FALLAS["estado_laboratorio"] == "503":
        raise ConnectionError("503 Service Unavailable desde la API de Brev (simulado)")
    if FALLAS["estado_laboratorio"] == "lento":
        time.sleep(1.5)
    return json.dumps({"instancia": instancia, "estado": "RUNNING", "reanudada_hace_min": 12,
                       "cookie_de_sesion": "vencida"}, ensure_ascii=False)

HERRAMIENTAS = [
    {"type": "function", "function": {
        "name": "buscar_faq",
        "description": "Busca en la FAQ del curso. Devuelve fragmentos con un id [archivo.md#pregunta] para citar, o SIN_EVIDENCIA.",
        "parameters": {"type": "object", "properties": {"consulta": {"type": "string"},
                                                        "k": {"type": "integer", "minimum": 1, "maximum": 5}},
                       "required": ["consulta"]}}},
    {"type": "function", "function": {
        "name": "estado_laboratorio",
        "description": "Consulta el estado de la instancia de Brev del estudiante (RUNNING, STOPPED...) y de su sesión del laboratorio.",
        "parameters": {"type": "object", "properties": {"instancia": {"type": "string"}}, "required": ["instancia"]}}},
]
IMPLEMENTACIONES = {"buscar_faq": buscar_faq_trazado, "estado_laboratorio": estado_laboratorio}

def ejecutar_herramienta(nombre, argumentos):
    """Un span TOOL por herramienta. Los errores vuelven al modelo como observación, y quedan en la traza."""
    with tracer.start_as_current_span(f"tool · {nombre}") as s:
        poner(s, openinference_span_kind="TOOL", tool_name=nombre, input_value=argumentos)
        try:
            args = json.loads(argumentos or "{}")
            salida = IMPLEMENTACIONES[nombre](**args)
        except Exception as e:
            s.record_exception(e)
            s.set_status(Status(StatusCode.ERROR, f"{type(e).__name__}: {e}"))
            salida = f"ERROR: {type(e).__name__}: {e}"
        if salida.startswith("ERROR") and s.status.status_code != StatusCode.ERROR:
            s.set_status(Status(StatusCode.ERROR, salida[:120]))
        poner(s, output_value=salida)
        return salida

print("Instrumentación lista: LLM, RETRIEVER y TOOL")
'''),
    md("""
## 6 · El agente de soporte, con una traza por pregunta
Es el loop ReAct de la clase 2.2. Lo único nuevo: un span raíz `AGENT` envuelve todo, y cada paso queda como hijo.
"""),
    code(r'''
SISTEMA = """ROL: soporte-trazado
Eres el agente de soporte del curso Seguridad de agentes con OpenShell y NemoClaw.
- Si la duda es sobre la instancia o el laboratorio, primero usa estado_laboratorio con la instancia "mi-lab".
- Busca en la FAQ con buscar_faq. Cita los ids [archivo.md#...] tal cual aparecen; no inventes ids.
- Si buscar_faq devuelve SIN_EVIDENCIA, di "La FAQ no cubre esto" y no repitas la misma búsqueda.
- Responde en español con: Qué pasa, Qué hacer (pasos) y Fuente."""

def agente(pregunta, max_pasos=5):
    """Responde una pregunta y devuelve {'respuesta', 'traza', 'pasos'}."""
    with tracer.start_as_current_span("agente · soporte") as raiz:
        poner(raiz, openinference_span_kind="AGENT", input_value=pregunta)
        mensajes = [{"role": "system", "content": SISTEMA}, {"role": "user", "content": pregunta}]
        respuesta = None
        for paso in range(1, max_pasos + 1):
            r = llamar_trazado(mensajes, HERRAMIENTAS, paso=paso)
            m = r.choices[0].message
            if not m.tool_calls:
                respuesta = m.content or ""
                break
            mensajes.append({"role": "assistant", "content": m.content or "",
                             "tool_calls": [{"id": t.id, "type": "function",
                                             "function": {"name": t.function.name, "arguments": t.function.arguments}}
                                            for t in m.tool_calls]})
            for t in m.tool_calls:
                salida = ejecutar_herramienta(t.function.name, t.function.arguments)
                mensajes.append({"role": "tool", "tool_call_id": t.id, "content": salida})
        if respuesta is None:
            respuesta = "(el agente llegó al límite de pasos sin responder)"
            raiz.set_status(Status(StatusCode.ERROR, f"límite de {max_pasos} pasos"))
        poner(raiz, output_value=respuesta, agente_pasos=paso)
        traza = format(raiz.get_span_context().trace_id, "032x")
    PROVEEDOR.force_flush()      # que Phoenix la reciba ya
    return {"respuesta": respuesta, "traza": traza, "pasos": paso}

REPORTE = "Me sale 401 en el laboratorio después de reanudar Brev"
r1 = agente(REPORTE)
print(r1["respuesta"])
print("\ntraza:", r1["traza"], "· pasos:", r1["pasos"])
'''),
    md("""
## 7 · Lee la traza como árbol
`ver_traza` reconstruye el árbol con los spans guardados en memoria: tipo, nombre, duración, lo más importante de sus atributos y ✖ si terminó en error. Es lo mismo que muestra Phoenix, en texto.
"""),
    code(r'''
def spans_de(traza):
    return [s for s in MEMORIA.get_finished_spans() if format(s.context.trace_id, "032x") == traza]

def _resumen(s):
    a = s.attributes
    tipo = a.get("openinference.span.kind", "")
    if tipo == "LLM":
        return f"finish={a.get('llm.finish_reason')} · tokens={a.get('llm.token_count.total')}"
    if tipo == "RETRIEVER":
        docs = [f"{a.get(f'retrieval.documents.{i}.document.id', '').split('#')[0]}:{a.get(f'retrieval.documents.{i}.document.score')}"
                for i in range(5) if f"retrieval.documents.{i}.document.id" in a]
        return "docs=" + (", ".join(docs) or "ninguno")
    if tipo == "TOOL":
        return "args=" + str(a.get("input.value", ""))[:60]
    if tipo == "AGENT":
        return f"pasos={a.get('agente.pasos')}"
    return ""

def ver_traza(traza):
    spans = spans_de(traza)
    hijos = {}
    for s in spans:
        hijos.setdefault(s.parent.span_id if s.parent else None, []).append(s)
    def pinta(s, prefijo="", ultimo=True, raiz=False):
        ms = (s.end_time - s.start_time) / 1e6
        marca = "✖" if s.status.status_code == StatusCode.ERROR else "✔"
        rama = "" if raiz else ("└─ " if ultimo else "├─ ")
        tipo = s.attributes.get("openinference.span.kind", "")
        print(f"{prefijo}{rama}{marca} {tipo:9s} {s.name:28s} {ms:7.0f} ms  {_resumen(s)}")
        if s.status.status_code == StatusCode.ERROR and s.status.description:
            print(f"{prefijo}{'' if raiz else ('   ' if ultimo else '│  ')}   └ error: {s.status.description[:90]}")
        hs = sorted(hijos.get(s.context.span_id, []), key=lambda x: x.start_time)
        for i, h in enumerate(hs):
            pinta(h, prefijo + ("" if raiz else ("   " if ultimo else "│  ")), i == len(hs) - 1)
    for r in hijos.get(None, []):
        pinta(r, raiz=True)

ver_traza(r1["traza"])
'''),
    md("""
## 8 · Métricas que salen de la traza
Con los spans ya no adivinas el costo: lo cuentas. Tiempo y tokens por tipo de paso.
"""),
    code(r'''
def metricas(traza):
    filas = {}
    for s in spans_de(traza):
        tipo = s.attributes.get("openinference.span.kind", "?")
        f = filas.setdefault(tipo, {"spans": 0, "ms": 0, "tokens": 0, "errores": 0})
        f["spans"] += 1
        f["ms"] += round((s.end_time - s.start_time) / 1e6)
        f["tokens"] += s.attributes.get("llm.token_count.total", 0) or 0
        f["errores"] += s.status.status_code == StatusCode.ERROR
    print(f"{'tipo':10s} {'spans':>5s} {'ms':>7s} {'tokens':>7s} {'errores':>7s}")
    for tipo, f in sorted(filas.items()):
        print(f"{tipo:10s} {f['spans']:5d} {f['ms']:7d} {f['tokens']:7d} {f['errores']:7d}")
    if USE_MOCK:
        print("(MOCK: tokens estimados ≈ caracteres/4; en vivo vienen de usage)")
    return filas

_ = metricas(r1["traza"])
'''),
    md("""
## 9 · 🧯 Depura con la traza
Cuatro problemas típicos. En cada uno, **primero mira la traza** y luego lee la explicación.

### a) La herramienta falla
La API de Brev responde 503. ¿El agente lo oculta, o lo dice? ¿Dónde quedó el error?
"""),
    code(r'''
FALLAS["estado_laboratorio"] = "503"
ra = agente("¿Mi instancia de Brev está encendida? Me sale 401 en el laboratorio")
FALLAS["estado_laboratorio"] = None
print(ra["respuesta"], "\n")
ver_traza(ra["traza"])
'''),
    md("""
El span `tool · estado_laboratorio` quedó con ✖ y el mensaje exacto (`ConnectionError: 503 ...`). La raíz terminó en ✔ porque el **harness** convirtió el error en observación y el agente siguió. Eso es correcto, **siempre que la respuesta lo diga**: revisa que diga "No pude verificar el estado de tu instancia". Sin traza, verías solo una respuesta incompleta y no sabrías por qué.

### b) El loop atascado
Una pregunta que la FAQ no cubre. El agente busca, no encuentra y vuelve a buscar **lo mismo**.
"""),
    code(r'''
def repeticiones(traza, minimo=2):
    """Llamadas a herramientas con los mismos argumentos repetidas en una traza."""
    cuenta = {}
    for s in spans_de(traza):
        if s.attributes.get("openinference.span.kind") == "TOOL":
            clave = (s.attributes.get("tool.name"), s.attributes.get("input.value"))
            cuenta[clave] = cuenta.get(clave, 0) + 1
    return {f"{n} {a}": c for (n, a), c in cuenta.items() if c >= minimo}

rb = agente("¿Me pueden mandar la factura de Brev en pesos?")
print(rb["respuesta"], "\n")
ver_traza(rb["traza"])
print("\nrepeticiones:", repeticiones(rb["traza"]))
'''),
    md("""
La raíz termina con ✖ `límite de 5 pasos`: el tope de la clase 2.2 te salvó, pero gastaste 5 llamadas en nada. `repeticiones` muestra la causa: la misma búsqueda, con los mismos argumentos, en cada paso. **Arreglo:** en el harness, si una herramienta recibe los mismos argumentos dos veces seguidas, devuelve una observación como *"ya buscaste esto; responde con lo que tienes"*. En vivo, el modelo real puede rendirse antes; la traza te lo dice igual.

### c) La cita inventada
La respuesta "se ve bien" y trae citas. ¿Todas salieron de una herramienta?
"""),
    code(r'''
def citas_sin_respaldo(traza):
    """Ids citados en la respuesta final que NO aparecen en ninguna salida de herramienta de la traza."""
    spans = spans_de(traza)
    raiz = next(s for s in spans if s.parent is None)
    citadas = set(_ID.findall(raiz.attributes.get("output.value", "")))
    vistas = set()
    for s in spans:
        if s.attributes.get("openinference.span.kind") in ("TOOL", "RETRIEVER"):
            vistas |= set(_ID.findall(s.attributes.get("output.value", "")))
    return sorted(citadas - vistas)

rc = agente("¿Es cierto que el launchable de Brev trae GPU gratis para siempre?")
print(rc["respuesta"], "\n")
print("citas sin respaldo:", citas_sin_respaldo(rc["traza"]))
print("citas sin respaldo en la primera traza:", citas_sin_respaldo(r1["traza"]))
'''),
    md("""
`brev.md#la-gpu-es-gratis-para-siempre` no salió de ninguna búsqueda: el modelo la inventó. Con la traza lo compruebas **con código**, no a ojo. Es la `revisar_citas` de la clase 3.3, ahora sobre la traza, y sirve igual para cualquier agente instrumentado.

### d) ¿Por qué tardó tanto?
"""),
    code(r'''
def mas_lentos(traza, n=3):
    spans = sorted(spans_de(traza), key=lambda s: s.end_time - s.start_time, reverse=True)
    return [(s.name, round((s.end_time - s.start_time) / 1e6)) for s in spans if s.parent is not None][:n]

FALLAS["estado_laboratorio"] = "lento"
rd = agente("Mi instancia de Brev no responde después de reanudar")
FALLAS["estado_laboratorio"] = None
print("los 3 spans más lentos (ms):", mas_lentos(rd["traza"]))
'''),
    md("""
El cuello de botella es `tool · estado_laboratorio`, no el modelo. Sin traza, la reacción típica es "el modelo es lento, cambiemos de modelo". Con traza, arreglas lo que de verdad tarda.

## 10 · Phoenix y la auto-instrumentación
Hasta aquí instrumentaste **a mano**: entiendes qué es cada span. En proyectos reales también usas **auto-instrumentación**: una librería que envuelve el cliente de OpenAI y crea los spans `LLM` sola.

```bash
pip install arize-phoenix openinference-instrumentation-openai
phoenix serve            # interfaz en http://localhost:6006
```

Con tu key, la celda siguiente activa `OpenAIInstrumentor` sobre el mismo `PROVEEDOR`: los spans automáticos aparecen **dentro** de tu span `AGENT`. Sin key no hace nada (el `MockClient` no es el cliente de OpenAI).

En Phoenix: abre **Projects → soporte-nemoclaw**, elige una traza y recorre el árbol. A la derecha ves los atributos de cada span: los mismos que imprime `ver_traza`.
"""),
    code(r'''
if USE_MOCK:
    print("MOCK: la auto-instrumentación necesita el cliente real de OpenAI. Con tu key, esta celda la activa.")
else:
    _instala("openinference-instrumentation-openai", "openinference.instrumentation.openai")
    from openinference.instrumentation.openai import OpenAIInstrumentor
    OpenAIInstrumentor().instrument(tracer_provider=PROVEEDOR)
    r_auto = agente(REPORTE)
    ver_traza(r_auto["traza"])
    print("\nVerás spans 'ChatCompletion' (automáticos) dentro de tus spans 'llm · paso N'.")
'''),
    md("""
### ¿Y NVIDIA tiene algo propio?
Sí, en dos niveles:

| Dónde | Herramienta de NVIDIA | Qué hace |
|---|---|---|
| Tu código de agente | **NeMo Agent Toolkit** (`nvidia-nat`) | Instrumenta flujos de agentes y exporta trazas a Phoenix, Langfuse, LangSmith, Weave u OTel con unas líneas de YAML. |
| El sandbox de NemoClaw | `nemoclaw <sandbox> logs`, `sessions export` y `openshell term` | Bitácoras del gateway, eventos de auditoría de OpenShell (bloqueos de política) y el historial de sesiones del agente. |
| NemoClaw con Deep Agents | `--observability` en el onboarding | Exporta trazas OTLP a un colector en el host, con el preset de red `observability-otlp-local`. |

Con el NeMo Agent Toolkit, mandar las trazas a Phoenix es configuración, no código:

```yaml
general:
  telemetry:
    tracing:
      phoenix:
        _type: phoenix
        endpoint: http://localhost:6006/v1/traces
        project: soporte-nemoclaw
```

Las trazas que hiciste aquí y las del toolkit hablan el mismo idioma (OTel + OpenInference): las ves en el mismo Phoenix.

## 11 · Una traza también es un dato sensible
"""),
    code(r'''
rs = agente("Me sale 401 en el laboratorio. Mi key es nvapi-ESTOESUNAKEYFALSA1234567890")
filtrada = any("ESTOESUNAKEYFALSA" in str(v) for s in spans_de(rs["traza"]) for v in s.attributes.values())
print("¿la key quedó en la traza?:", filtrada)
assert not filtrada, "¡La key llegó a la traza! Revisa que todos los atributos pasen por redactar()"
print(spans_de(rs["traza"])[-1].attributes["input.value"])
'''),
    md("""
La key no llegó a la traza: `poner()` tacha todo con `redactar()`. Aun así, trata tus trazas como datos privados: contienen preguntas de estudiantes, rutas de archivos y salidas de herramientas. No publiques un Phoenix sin autenticación y no compartas trazas completas en un foro.

## 12 · Avance del proyecto
**Soporte NemoClaw v3.4: cada respuesta con su traza.** `exportar_traza` guarda la traza, con los secretos tachados, en JSON, lista para adjuntar a un reporte de error o comparar antes y después de un cambio.
"""),
    code(r'''
def exportar_traza(traza, carpeta="trazas"):
    pathlib.Path(carpeta).mkdir(exist_ok=True)
    datos = [{"nombre": s.name, "span_id": format(s.context.span_id, "016x"),
              "padre": format(s.parent.span_id, "016x") if s.parent else None,
              "ms": round((s.end_time - s.start_time) / 1e6), "estado": s.status.status_code.name,
              "error": s.status.description, "atributos": dict(s.attributes)}
             for s in sorted(spans_de(traza), key=lambda s: s.start_time)]
    ruta = pathlib.Path(carpeta) / f"{traza}.json"
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    return ruta

def soporte_nemoclaw(pregunta):
    r = agente(pregunta)
    problemas = {"citas_sin_respaldo": citas_sin_respaldo(r["traza"]), "repeticiones": repeticiones(r["traza"]),
                 "errores": [s.name for s in spans_de(r["traza"]) if s.status.status_code == StatusCode.ERROR]}
    return {**r, "problemas": problemas, "archivo": str(exportar_traza(r["traza"]))}

final = soporte_nemoclaw("¿Por qué mi notebook responde HTTP 401 cuando llamo al modelo?")
print(final["respuesta"])
print("\nproblemas:", final["problemas"])
print("traza guardada en:", final["archivo"])
'''),
    md("""
## Resumen
- Una **traza** es el árbol de lo que pasó para responder una pregunta; un **span**, cada paso.
- Instrumentaste tu agente con **OpenTelemetry** y convenciones **OpenInference** (`AGENT`, `LLM`, `RETRIEVER`, `TOOL`).
- Con la traza encontraste una herramienta que falla, un loop atascado, una cita inventada y el paso lento, **con código**.
- **Tachas los secretos** antes de guardar: una traza es tan sensible como el chat.
- Phoenix y el **NeMo Agent Toolkit** consumen el mismo formato.

En el Módulo 4 tu agente se va a NemoClaw. En la clase 4.4 vas a trazar las llamadas a Hermes con este mismo `PROVEEDOR`.
"""),
]

if __name__ == "__main__":
    write("3.4", NB34)
