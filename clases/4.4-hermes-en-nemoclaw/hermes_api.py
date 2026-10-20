"""Pregúntale a Hermes por su API compatible con OpenAI desde un programa en Python (clase 4.4).

Corre en la máquina de Brev (o en cualquier host con un sandbox de Hermes), no dentro del sandbox.

Uso:
    python3 -m venv ~/venv-hermes && source ~/venv-hermes/bin/activate
    pip install openai
    export HERMES_TOKEN="$(nemohermes mi-hermes gateway-token --quiet)"
    python3 hermes_api.py "Mi notebook responde HTTP 401 cuando llamo al modelo"

Variables opcionales:
    HERMES_BASE_URL   http://127.0.0.1:8642/v1 (revisa el puerto con `openshell forward list`)
    HERMES_MODEL      el id que devuelve /v1/models (si no la pones, usa el primero)

Lo que ves aquí: la respuesta final de Hermes. Las herramientas que Hermes usa DENTRO del sandbox
no aparecen: esas las ves con `nemohermes mi-hermes sessions export`. Es la diferencia entre
lo que ve el cliente y lo que hizo el agente.
"""
import os
import re
import sys
import time

from openai import OpenAI

BASE_URL = os.environ.get("HERMES_BASE_URL", "http://127.0.0.1:8642/v1")
TOKEN = os.environ.get("HERMES_TOKEN", "").strip()

_SECRETOS = [(re.compile(r"nvapi-[A-Za-z0-9_\-]{8,}"), "nvapi-***"),
             (re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]{8,}"), "Bearer ***"),
             (re.compile(r"\b[0-9a-f]{64}\b"), "<token-64-hex>")]     # el API_SERVER_KEY de Hermes


def redactar(texto):
    # Tacha keys y tokens antes de mostrar un mensaje de error en pantalla.
    for patron, reemplazo in _SECRETOS:
        texto = patron.sub(reemplazo, texto)
    return texto


def main():
    if not TOKEN:
        sys.exit('Falta HERMES_TOKEN. Corre: export HERMES_TOKEN="$(nemohermes <sandbox> gateway-token --quiet)"')
    pregunta = " ".join(sys.argv[1:]) or "Mi notebook responde HTTP 401 cuando llamo al modelo"

    # El token va en la cabecera Authorization: Bearer, nunca en los mensajes ni en pantalla.
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

    t0 = time.time()
    try:
        # Hermes decide solo si usa la skill soporte-nemoclaw: la pregunta va tal cual, como en el chat.
        r = cliente.chat.completions.create(model=modelo, messages=[{"role": "user", "content": pregunta}])
        respuesta = r.choices[0].message.content or ""
    except Exception as e:
        sys.exit(f"Hermes respondió con error: {redactar(str(e))[:300]}")

    print(respuesta)
    print(f"\nmodelo: {modelo} · {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
