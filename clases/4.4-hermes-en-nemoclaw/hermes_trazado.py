"""Pregúntale a Hermes por su API compatible con OpenAI y deja la traza en Phoenix (clase 4.4).

Corre en la máquina de Brev (o en cualquier host con un sandbox de Hermes), no dentro del sandbox.

Uso:
    python3 -m venv ~/venv-trazas && source ~/venv-trazas/bin/activate
    pip install openai opentelemetry-sdk opentelemetry-exporter-otlp-proto-http openinference-instrumentation-openai
    export HERMES_TOKEN="$(nemohermes mi-hermes gateway-token --quiet)"
    python3 hermes_trazado.py "Mi notebook responde HTTP 401 cuando llamo al modelo"

Variables opcionales:
    HERMES_BASE_URL              http://127.0.0.1:8642/v1 (revisa el puerto con `openshell forward list`)
    HERMES_MODEL                 el id que devuelve /v1/models (si no la pones, usa el primero)
    PHOENIX_COLLECTOR_ENDPOINT   http://127.0.0.1:6006 (Phoenix en Docker en la misma máquina)

Lo que ves en Phoenix: un span AGENT "hermes · pregunta" con un span LLM automático dentro.
Las herramientas que Hermes usa DENTRO del sandbox no aparecen aquí: esas las ves con
`nemohermes mi-hermes sessions export`. Es la diferencia entre trazar el cliente y trazar el agente.
"""
import os
import re
import sys
import time

from openai import OpenAI
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Status, StatusCode
from openinference.instrumentation.openai import OpenAIInstrumentor

BASE_URL = os.environ.get("HERMES_BASE_URL", "http://127.0.0.1:8642/v1")
TOKEN = os.environ.get("HERMES_TOKEN", "").strip()
PHOENIX = os.environ.get("PHOENIX_COLLECTOR_ENDPOINT", "http://127.0.0.1:6006").rstrip("/")
PROYECTO = "soporte-nemoclaw-hermes"

_SECRETOS = [(re.compile(r"nvapi-[A-Za-z0-9_\-]{8,}"), "nvapi-***"),
             (re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]{8,}"), "Bearer ***"),
             (re.compile(r"\b[0-9a-f]{64}\b"), "<token-64-hex>")]     # el API_SERVER_KEY de Hermes


def redactar(texto):
    for patron, reemplazo in _SECRETOS:
        texto = patron.sub(reemplazo, texto)
    return texto


def main():
    if not TOKEN:
        sys.exit('Falta HERMES_TOKEN. Corre: export HERMES_TOKEN="$(nemohermes <sandbox> gateway-token --quiet)"')
    pregunta = " ".join(sys.argv[1:]) or "Mi notebook responde HTTP 401 cuando llamo al modelo"

    proveedor = TracerProvider(resource=Resource.create({"service.name": PROYECTO,
                                                         "openinference.project.name": PROYECTO}))
    proveedor.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=PHOENIX + "/v1/traces")))
    # La auto-instrumentación crea el span LLM de cada llamada. Ojo: guarda los mensajes completos,
    # así que nunca pegues una key en la pregunta. El token va en una cabecera, no en los mensajes.
    OpenAIInstrumentor().instrument(tracer_provider=proveedor)
    tracer = proveedor.get_tracer("curso.hermes")

    cliente = OpenAI(base_url=BASE_URL, api_key=TOKEN, timeout=300, max_retries=0)
    try:
        modelo = os.environ.get("HERMES_MODEL") or cliente.models.list().data[0].id
    except Exception as e:
        codigo = getattr(e, "status_code", None)
        if codigo == 401:
            sys.exit("401: el token no es válido. Vuelve a leerlo con `nemohermes <sandbox> gateway-token --quiet` "
                     "(cambia si reconstruiste el sandbox).")
        sys.exit(f"No pude hablar con Hermes en {BASE_URL} ({type(e).__name__}). "
                 "Revisa el puerto con `openshell forward list` y la salud con `curl -sf http://127.0.0.1:8642/health`.")

    with tracer.start_as_current_span("hermes · pregunta") as raiz:
        raiz.set_attribute("openinference.span.kind", "AGENT")
        raiz.set_attribute("input.value", redactar(pregunta))
        raiz.set_attribute("hermes.base_url", BASE_URL)
        t0 = time.time()
        try:
            r = cliente.chat.completions.create(model=modelo, messages=[{"role": "user", "content": pregunta}])
            respuesta = r.choices[0].message.content or ""
        except Exception as e:
            raiz.record_exception(e)
            raiz.set_status(Status(StatusCode.ERROR, redactar(f"{type(e).__name__}: {e}")[:200]))
            proveedor.force_flush()
            sys.exit(f"Hermes respondió con error: {redactar(str(e))[:300]}")
        raiz.set_attribute("output.value", redactar(respuesta))
        traza = format(raiz.get_span_context().trace_id, "032x")
    proveedor.force_flush()

    print(respuesta)
    print(f"\nmodelo: {modelo} · {time.time() - t0:.1f} s · traza: {traza}")
    print(f"Phoenix: proyecto '{PROYECTO}' en {PHOENIX}")


if __name__ == "__main__":
    main()
