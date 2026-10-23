"""Piezas compartidas por los generadores de notebooks (todo en español).

Un generador típico (tools/notebooks/m2.py):

    from comun import *
    write("2.1", [
        header("2.1", "En este notebook vas a ..."),
        SETUP, MOCK,
        md("## 1 · ..."), code("..."),
    ])

`write(id, cells)` guarda el notebook en clases/<slug>/<slug>.ipynb.
Cada notebook corre de punta a punta SIN API key (modo MOCK) y en vivo con NVIDIA_API_KEY.
"""
import json
import pathlib
import sys
import textwrap

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from course import COURSE, by_id, module  # noqa: E402


def md(s):
    return {"cell_type": "markdown", "metadata": {}, "source": textwrap.dedent(s).strip("\n").splitlines(True)}


def code(s):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": textwrap.dedent(s).strip("\n").splitlines(True)}


def header(cid, intro):
    c = by_id(cid)
    colab = ""
    if COURSE.get("github"):
        url = f"https://colab.research.google.com/github/{COURSE['github']}/blob/main/clases/{c['slug']}/{c['slug']}.ipynb"
        colab = f"\n[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url})\n"
    glosario = (f"https://github.com/{COURSE['github']}/blob/main/GLOSARIO.md" if COURSE.get("github")
                else "../../GLOSARIO.md")
    return md(f"""
# {c['title']}
**{module(c['module'])['title']}** — *{COURSE['title']}* ({COURSE['partner']})
{colab}
{textwrap.dedent(intro).strip()}

> **¿Sin API key?** Ejecuta todo igual: el notebook detecta que no hay key y usa un **modelo simulado (MOCK)** que imita la forma de las respuestas de la API. Con tu key `nvapi-` (clase 1.2), las mismas celdas llaman al modelo real.

> **¿No programas?** No necesitas leer el código. Presiona ▶ en cada celda, en orden, y lee el texto y lo que aparece debajo (o usa **Entorno de ejecución → Ejecutar todo** en Colab). Las celdas con ⚙️ son de preparación: se ejecutan igual, pero no necesitas abrirlas. Las palabras nuevas están en el [glosario]({glosario}).
""")


# Celdas de preparación: en Colab se muestran como "⚙️ <título>" con el código oculto
# (cellView: form). En Jupyter son celdas normales. Las celdas que enseñan quedan visibles.
_PREPARACION = ("Configuración", "Cliente:", "Ayudas de este módulo", "Reglas del modelo simulado",
                "La FAQ del curso", "FAQ del curso", "El índice RAG", "Herramientas del doctor",
                "Simulador: reglas", "Las 4 skills del proyecto", "La base de conocimiento",
                "Workspace temporal")


def _ocultar_preparacion(cells):
    for cell in cells:
        src = cell.get("source") or []
        if cell["cell_type"] != "code" or not src or not src[0].startswith("# --- "):
            continue
        titulo = src[0][6:].strip().rstrip("-").strip()
        if titulo.startswith(_PREPARACION):
            cell["source"] = [f"# @title ⚙️ {titulo}\n"] + src
            cell["metadata"]["cellView"] = "form"
    return cells


def write(cid, cells):
    c = by_id(cid)
    cells = _ocultar_preparacion(cells)
    book = {"cells": cells, "nbformat": 4, "nbformat_minor": 5,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}}}
    folder = ROOT / "clases" / c["slug"]
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{c['slug']}.ipynb"
    path.write_text(json.dumps(book, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("  notebook", path.relative_to(ROOT))


# ------------------------------------------------------------------ configuración compartida
SETUP = code('''
# --- Configuración (ejecútala siempre primero) ---------------------------------
import os, sys, json, subprocess

def _instala(paquete, modulo=None):
    try:
        __import__(modulo or paquete)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", paquete])

_instala("openai")
_instala("python-dotenv", "dotenv")

# 1) Google Colab: guarda tu key en Secrets (icono de llave 🔑) con el nombre NVIDIA_API_KEY
try:
    from google.colab import userdata
    os.environ.setdefault("NVIDIA_API_KEY", userdata.get("NVIDIA_API_KEY") or "")
except Exception:
    pass
# 2) Local: archivo .env en la raíz del repo (copia .env.example) o `export NVIDIA_API_KEY=nvapi-...`
from dotenv import load_dotenv
load_dotenv(); load_dotenv("../../.env")

BASE_URL    = os.environ.get("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
MODEL       = os.environ.get("NVIDIA_MODEL", "nvidia/nemotron-3.5-lightning-30b-a3b")
EMBED_MODEL = os.environ.get("NVIDIA_EMBED_MODEL", "nvidia/nemotron-3-embed-1b")
API_KEY     = (os.environ.get("NVIDIA_API_KEY") or "").strip()
USE_MOCK    = not API_KEY

if API_KEY and "integrate.api.nvidia.com" in BASE_URL and not API_KEY.startswith("nvapi-"):
    print("⚠  Tu key no empieza con 'nvapi-'. ¿Copiaste la key completa de build.nvidia.com?")
print("Modo:", "MOCK (sin NVIDIA_API_KEY: respuestas simuladas)" if USE_MOCK else f"EN VIVO · {MODEL}")
''')

MOCK = code(r'''
# --- Cliente: modelo real o simulado, con errores explicados en español --------
import re, time, math, hashlib
from types import SimpleNamespace as NS

def _msg(content):
    m = NS(content=content, tool_calls=None, role="assistant", reasoning_content=None)
    return NS(choices=[NS(message=m, finish_reason="stop")], usage=NS(prompt_tokens=0, completion_tokens=0, total_tokens=0))

def _call(name, args):
    tc = NS(id="call_" + hashlib.md5((name + json.dumps(args)).encode()).hexdigest()[:8], type="function",
            function=NS(name=name, arguments=json.dumps(args, ensure_ascii=False)))
    m = NS(content=None, tool_calls=[tc], role="assistant", reasoning_content=None)
    return NS(choices=[NS(message=m, finish_reason="tool_calls")], usage=NS(prompt_tokens=0, completion_tokens=0, total_tokens=0))

class MockClient:
    """Imita la FORMA de la API de chat completions. No es inteligente: sigue reglas.
    Cada notebook puede agregar reglas propias con  @regla_mock  (ver más abajo)."""
    reglas = []
    def __init__(self):
        self.chat = NS(completions=NS(create=self._create))
        self.embeddings = NS(create=self._embed)
    def _create(self, model=None, messages=None, tools=None, **kw):
        nombres = [t["function"]["name"] for t in (tools or [])]
        for r in self.reglas:
            out = r(messages, nombres)
            if out is not None:
                return out
        ultimo = messages[-1]
        texto = (ultimo.get("content") or "")
        if ultimo["role"] == "tool":
            return _msg("Según la herramienta: " + str(ultimo["content"]))
        if re.search(r"c[oó]mo me llamo|what is my name", texto, re.I):
            vistos = [re.search(r"(?:me llamo|my name is)\s+(\w+)", m.get("content") or "", re.I)
                      for m in messages[:-1] if m["role"] == "user"]
            vistos = [v.group(1) for v in vistos if v]
            return _msg(f"Te llamas {vistos[-1]}." if vistos else "No sé cómo te llamas: no me lo has dicho en esta conversación.")
        return _msg("(mock) Respuesta simulada. Configura NVIDIA_API_KEY para hablar con el modelo real.")
    def _embed(self, model=None, input=None, **kw):
        textos = [input] if isinstance(input, str) else list(input)
        return NS(data=[NS(embedding=_vector_bolsa(t), index=i) for i, t in enumerate(textos)])

def regla_mock(f):
    """Decorador: agrega una regla al modelo simulado. f(messages, nombres_de_tools) -> respuesta | None"""
    MockClient.reglas.append(f)
    return f

_VACIAS = set("que qué como cómo para por con una uno los las del este esta eso esto hago hace tengo puedo sale mis tus sus the and you what how".split())

def _vector_bolsa(texto, dim=256):
    """Embedding simulado: bolsa de palabras con hashing. Sirve para que RAG funcione offline."""
    v = [0.0] * dim
    for w in re.findall(r"\w+", texto.lower()):
        if len(w) > 2 and w not in _VACIAS:
            w = w[:6]                       # raíz burda: "reanudar" ~ "reanudé"
            v[int(hashlib.md5(w.encode()).hexdigest(), 16) % dim] += 1.0
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]

def diagnostico(e):
    """Traduce un error de la API a: qué pasó + qué hacer. Es el 'FAQ' en código."""
    status = getattr(e, "status_code", None)
    cuerpo = str(getattr(e, "body", "") or e)[:300]
    tabla = {
        400: "400 · Solicitud inválida: algún parámetro no le gusta al modelo (¿tools en un modelo que no las soporta? ¿max_tokens muy alto?). Lee el cuerpo del error.",
        401: "401 · Key rechazada: revisa que NVIDIA_API_KEY sea la key completa (empieza con nvapi-), sin espacios ni comillas. Si la regeneraste, la vieja ya no sirve.",
        403: "403 · Tu key es válida pero no tiene acceso a ese modelo o se acabaron tus créditos. Revisa tu cuenta en build.nvidia.com o prueba otro modelo.",
        404: "404 · Ese modelo o esa ruta no existen. Revisa MODEL / EMBED_MODEL (copia el ID exacto del catálogo) y que BASE_URL termine en /v1.",
        410: "410 · El modelo fue retirado del endpoint gratuito. Cambia MODEL por uno vigente del catálogo de build.nvidia.com.",
        422: "422 · Argumentos con formato incorrecto (p. ej. falta input_type en embeddings o un esquema de tool inválido).",
        429: "429 · Demasiadas solicitudes por minuto. Espera unos segundos y reintenta; no ejecutes celdas en ráfaga.",
    }
    if status in tabla:
        return f"{tabla[status]}\n   Detalle del servidor: {cuerpo}"
    if status and 500 <= status < 600:
        return f"{status} · Falla del lado del servidor o el modelo está arrancando. Reintenta en 30-60 s; si persiste, prueba otro modelo.\n   Detalle: {cuerpo}"
    nombre = type(e).__name__
    if "Timeout" in nombre:
        return "Timeout · El modelo tardó demasiado. Reintenta, baja max_tokens o usa un modelo más rápido."
    if "Connection" in nombre:
        return "Sin conexión · No se pudo llegar a BASE_URL. Revisa tu internet, VPN/proxy corporativo o el valor de BASE_URL."
    return f"{nombre}: {cuerpo}"

if USE_MOCK:
    client = MockClient()
else:
    from openai import OpenAI
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY, timeout=60, max_retries=2)

def chat(messages, tools=None, model=None, **kw):
    """Una llamada al modelo. Devuelve la respuesta cruda (choices[0].message, finish_reason, usage)."""
    kw.setdefault("max_tokens", 4096)          # los modelos que razonan gastan tokens antes de responder
    if tools:
        kw["tools"] = tools
    try:
        r = client.chat.completions.create(model=model or MODEL, messages=messages, **kw)
    except Exception as e:
        raise RuntimeError(diagnostico(e)) from None
    ch = r.choices[0]
    if ch.finish_reason == "length" and not (ch.message.content or ch.message.tool_calls):
        print("⚠  finish_reason=length sin contenido: el modelo gastó max_tokens razonando. Sube max_tokens.")
    return r

def embed(textos, input_type="passage", model=None):
    """Embeddings. input_type='query' para preguntas, 'passage' para documentos."""
    textos = [textos] if isinstance(textos, str) else list(textos)
    try:
        r = client.embeddings.create(model=model or EMBED_MODEL, input=textos,
                                     extra_body={"input_type": input_type, "truncate": "END"}) if not USE_MOCK \
            else client.embeddings.create(model=model or EMBED_MODEL, input=textos)
    except Exception as e:
        raise RuntimeError(diagnostico(e)) from None
    return [d.embedding for d in r.data]

print("Cliente listo:", "MockClient" if USE_MOCK else BASE_URL)
''')
