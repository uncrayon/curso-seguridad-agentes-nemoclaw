"""Diagramas del Módulo 1. Se usan en slides.md con ":::diagrama <nombre>".

Usa las piezas de tools/diagramas.py (nodo, flecha, cuarto, chips, pie) y las clases CSS del kit
(assets/slides.css, sección "Diagramas"). Estilos nuevos solo en assets/diagramas-m1.css.
Cada texto visible va en T["es"] y T["en"].
"""
from diagramas import chips, cuarto, flecha, nodo, pie  # noqa: F401

T = {
    "es": {
        # 1.2 · la tarjeta de acceso
        "tu": "Tú", "tu_sub": "tu cuenta gratuita",
        "key": "API key", "key_sub": "tu tarjeta de acceso",
        "a_tu_nombre": "entra a tu nombre",
        "build_sub": "el catálogo de modelos de NVIDIA",
        "nemotron_sub": "el modelo del curso",
        "como_pass": "Quien tenga tu key entra a tu nombre: trátala como una contraseña",
        # 1.2 · crear cuenta y key
        "cp1": "Entra", "cp1s": "build.nvidia.com, arriba a la derecha",
        "cp2": "Confirma tu correo", "cp2s": "y tu teléfono, si lo pide",
        "cp3": "Genera tu key", "cp3s": "menú de tu cuenta → API Keys",
        "cp4": "Cópiala ya", "cp4s": "después no la ves completa",
        "cp5": "Pruébala", "cp5s": "el cuadro de prueba de Nemotron",
        "sms": "¿Vives fuera de EE. UU.? El SMS puede no llegar. Crea tu key <b>antes</b> de avanzar y, si falla, escribe a help@build.nvidia.com",
        # 1.2 · dónde guardarla
        "seguro": "Aquí sí", "nunca": "Aquí nunca",
        "gestor": "Gestor de contraseñas", "gestor_sub": "o una nota privada",
        "colab": "Colab · la llave", "colab_sub": "nombre: NVIDIA_API_KEY",
        "env": "Archivo privado .env", "env_sub": "nunca se sube a GitHub",
        "panel": "Panel del curso", "panel_sub": "se borra al cerrar la pestaña",
        "chat": "Un chat", "chat_sub": "ni con tu equipo",
        "captura": "Capturas o videos", "captura_sub": "difumínala siempre",
        "doc": "Documentos compartidos", "doc_sub": "otros pueden copiarla",
        "codigo": "El código o GitHub", "codigo_sub": "queda en el historial",
        "colab_pasos": "En Colab: la llave del panel izquierdo → NVIDIA_API_KEY → activa el acceso del notebook",
        # 1.2 · primera llamada
        "pregunta": "Tu pregunta", "pregunta_sub": "«Saluda en una frase»",
        "mas_key": "+ tu key", "piensa": "piensa antes de responder",
        "respuesta": "La respuesta",
        "content_sub": "lo que contestó", "finish_sub": "por qué terminó · stop = bien",
        "usage_sub": "tokens que entraron y salieron",
        "token": "Un token ≈ ¾ de palabra: como las sílabas de un telegrama, que se cobraba por palabra",
        # 1.2 · créditos
        "saldo": "Tus créditos", "saldo_sub": "saldo gratuito, como el prepago",
        "gastas": "gastas tokens",
        "limite": "Te pasas del límite", "limite_sub": "429 · demasiadas solicitudes",
        "espera": "Espera y reintenta", "espera_sub": "el saldo no se pierde",
        "mas_gasta": "Lo que más gasta",
        "g1": "Ciclos sin límite", "g1s": "repiten sin parar",
        "g2": "Celdas en ráfaga", "g2s": "muchos ▶ seguidos",
        "g3": "Respuestas enormes", "g3s": "max_tokens muy alto",
        "retirado": "Los modelos gratuitos cambian: un modelo retirado responde 410",
        # 1.2 · si se filtra
        "filtro": "Se filtró", "filtro_sub": "chat, captura o GitHub",
        "revoca": "Revócala", "revoca_sub": "API Keys → revocar",
        "nueva": "Genera otra", "nueva_sub": "con un nombre nuevo",
        "actualiza": "Actualízala", "actualiza_sub": "Colab, .env, terminal y NemoClaw",
        "no_basta": "Borrar el archivo <b>no basta</b>: la key queda en el historial. Solo revocarla te protege",
        # 1.3 · casi todos los problemas
        "c_key": "Key mal copiada", "c_key_sub": "falta un pedazo o sobra un espacio",
        "c_modelo": "Modelo mal escrito", "c_modelo_sub": "una letra de más",
        "c_limite": "Límite de uso", "c_limite_sub": "demasiadas preguntas seguidas",
        "aviso": "Un aviso con número", "aviso_sub": "como los de un cajero automático",
        "provocamos": "Hoy los provocamos a propósito y dejamos tu entorno verificado",
        # 1.3 · ruta = dirección postal
        "sobre": "Una ruta de modelo",
        "dir": "Dirección", "dir_sub": "a dónde va la pregunta",
        "dest": "Destinatario", "dest_sub": "el modelo exacto",
        "firma": "Tu firma", "firma_sub": "tu key",
        "r_chat": "Ruta de chat", "r_chat_sub": "conversar y usar herramientas",
        "r_emb": "Ruta de embeddings", "r_emb_sub": "textos parecidos · clase 3.2",
        "regresa": "Si un dato está mal escrito, la carta regresa… con un número de error",
        # 1.3 · panel del curso de NVIDIA
        "f_url": "URL base de la API de chat", "f_url_v": "ya viene llena",
        "f_modelo": "ID del modelo de chat", "f_modelo_v": "ya viene lleno",
        "f_key": "Clave bearer", "f_key_v": "pega aquí tu key",
        "f_relay": "Relay de navegador de NVIDIA DLI", "f_relay_v": "solo hace de mensajero",
        "f_emb": "Ruta de embeddings", "f_emb_v": "la segunda ruta",
        "f_gest": "Gestión de la solicitud", "f_gest_v": "espera y reintentos",
        "guardar": "Guardar y verificar",
        "conectado": "✓ Conectado.", "conectado_sub": "una prueba real con tu key",
        "pestana": "Tu key se borra al cerrar la pestaña: es normal que te la pida otra vez",
        # 1.3 · el doctor
        "notebook": "Notebook", "notebook_sub": "un recetario interactivo",
        "config": "Celdas ⚙️", "config_sub": "buscan tu key en la llave",
        "vivo": "EN VIVO", "vivo_sub": "encontró tu key",
        "mock": "MOCK", "mock_sub": "un simulador, sin key",
        "d1": "Tu key", "d1s": "¿tiene buena forma?",
        "d2": "Lista de modelos", "d2s": "¿existe el tuyo?",
        "d3": "Pregunta real", "d3s": "tiempo y tokens",
        "d4": "Herramienta", "d4s": "¿sabe pedirla?",
        "d5": "Embeddings", "d5s": "¿encuentra parecidos?",
        "listo": "Veredicto: «✅ entorno listo» o qué arreglar exactamente",
        # 1.3 · rompe tu entorno
        "rompes": "Lo que rompes", "ves": "Lo que ves", "haces": "Qué haces",
        "x1": "Una key falsa", "x1v": "Key rechazada", "x1h": "Cópiala completa, sin espacios",
        "x2": "Un modelo que no existe", "x2v": "No existe", "x2h": "Copia el nombre exacto",
        "x3": "Solo 8 tokens para escribir", "x3v": "Respuesta vacía", "x3h": "Dale más espacio",
        "diagnostico": "El diagnóstico te dice en español qué pasó y qué hacer",
        # 1.3 · los avisos del cajero
        "corrige": "Corrige algo", "corrige_sub": "reintentar no sirve",
        "esperar": "Espera y reintenta", "esperar_sub": "se arregla solo",
        "e401": "Key rechazada", "a401": "«Tarjeta inválida»",
        "e403": "Sin acceso a ese modelo", "a403": "«Operación no permitida»",
        "e404": "El modelo o la ruta no existe", "a404": "«Cuenta inexistente»",
        "e410": "Modelo retirado", "a410": "«Tarjeta dada de baja»",
        "e429": "Demasiadas solicitudes", "a429": "«Intente más tarde»",
        "e5xx": "Falla del servidor", "a5xx": "«Cajero fuera de servicio»",
        "nunca401": "Más espera o más reintentos <b>nunca</b> arreglan un 401",
        # 1.3 · backoff
        "intento": "Intento", "ok": "✓ responde",
        "espera_s": "espera {} s",
        "limite_intentos": "Siempre con un límite de intentos: 1 s, 2 s, 4 s… y se detiene",
        "no401": "Con un 401 ni lo intenta otra vez: esperar no arregla una key mala",
        # 1.3 · avance del proyecto
        "doctor": "El doctor", "doctor_sub": "tus pruebas y tiempos",
        "reporte": "Reporte del entorno", "reporte_sub": "sin secretos",
        "rep_chips": ["Python", "Modo", "Rutas", "Pruebas", "Tiempo"],
        "pegas": "lo pegas al pedir ayuda",
        "soporte_sub": "en la 3.3 lo lee para diagnosticar",
        "sin_key": "Tu key nunca aparece en el reporte: el notebook lo comprueba",
    },
    "en": {
        "tu": "You", "tu_sub": "your free account",
        "key": "API key", "key_sub": "your access card",
        "a_tu_nombre": "gets in as you",
        "build_sub": "NVIDIA's model catalog",
        "nemotron_sub": "the course model",
        "como_pass": "Whoever has your key gets in as you: treat it like a password",
        "cp1": "Sign in", "cp1s": "build.nvidia.com, top right",
        "cp2": "Confirm your email", "cp2s": "and your phone, if asked",
        "cp3": "Generate your key", "cp3s": "account menu → API Keys",
        "cp4": "Copy it now", "cp4s": "you won't see it again",
        "cp5": "Try it", "cp5s": "Nemotron's test box",
        "sms": "Outside the US? The SMS may never arrive. Create your key <b>before</b> moving on and, if it fails, write to help@build.nvidia.com",
        "seguro": "Yes, here", "nunca": "Never here",
        "gestor": "Password manager", "gestor_sub": "or a private note",
        "colab": "Colab · the key icon", "colab_sub": "name: NVIDIA_API_KEY",
        "env": "Private .env file", "env_sub": "never uploaded to GitHub",
        "panel": "Course panel", "panel_sub": "cleared when the tab closes",
        "chat": "A chat", "chat_sub": "not even with your team",
        "captura": "Screenshots or videos", "captura_sub": "always blur it",
        "doc": "Shared documents", "doc_sub": "others can copy it",
        "codigo": "Code or GitHub", "codigo_sub": "it stays in the history",
        "colab_pasos": "In Colab: the key icon on the left panel → NVIDIA_API_KEY → turn on notebook access",
        "pregunta": "Your question", "pregunta_sub": "«Say hello in one sentence»",
        "mas_key": "+ your key", "piensa": "thinks before answering",
        "respuesta": "The answer",
        "content_sub": "what it answered", "finish_sub": "why it stopped · stop = good",
        "usage_sub": "tokens in and out",
        "token": "A token ≈ ¾ of a word: like the words of a telegram, which was charged per word",
        "saldo": "Your credits", "saldo_sub": "free balance, like prepaid",
        "gastas": "you spend tokens",
        "limite": "You hit the limit", "limite_sub": "429 · too many requests",
        "espera": "Wait and retry", "espera_sub": "your balance isn't lost",
        "mas_gasta": "What burns the most",
        "g1": "Unbounded loops", "g1s": "they repeat nonstop",
        "g2": "Cells in bursts", "g2s": "many ▶ in a row",
        "g3": "Huge answers", "g3s": "max_tokens set very high",
        "retirado": "Free models change: a retired model returns 410",
        "filtro": "It leaked", "filtro_sub": "chat, screenshot or GitHub",
        "revoca": "Revoke it", "revoca_sub": "API Keys → revoke",
        "nueva": "Generate another", "nueva_sub": "with a new name",
        "actualiza": "Update it", "actualiza_sub": "Colab, .env, terminal and NemoClaw",
        "no_basta": "Deleting the file <b>isn't enough</b>: the key stays in the history. Only revoking it protects you",
        "c_key": "Badly copied key", "c_key_sub": "a piece missing or extra space",
        "c_modelo": "Misspelled model", "c_modelo_sub": "one letter too many",
        "c_limite": "Usage limit", "c_limite_sub": "too many questions in a row",
        "aviso": "A numbered message", "aviso_sub": "like the ones at an ATM",
        "provocamos": "Today we trigger them on purpose and leave your setup verified",
        "sobre": "A model route",
        "dir": "Address", "dir_sub": "where the question goes",
        "dest": "Addressee", "dest_sub": "the exact model",
        "firma": "Your signature", "firma_sub": "your key",
        "r_chat": "Chat route", "r_chat_sub": "talk and use tools",
        "r_emb": "Embedding route", "r_emb_sub": "similar texts · class 3.2",
        "regresa": "If one detail is misspelled, the letter comes back… with an error number",
        "f_url": "Chat API base URL", "f_url_v": "already filled in",
        "f_modelo": "Chat model ID", "f_modelo_v": "already filled in",
        "f_key": "Bearer key", "f_key_v": "paste your key here",
        "f_relay": "NVIDIA DLI browser relay", "f_relay_v": "only a messenger",
        "f_emb": "Embedding route", "f_emb_v": "the second route",
        "f_gest": "Request handling", "f_gest_v": "wait and retries",
        "guardar": "Save & verify",
        "conectado": "✓ Connected.", "conectado_sub": "a real test with your key",
        "pestana": "Your key is cleared when the tab closes: it's normal to be asked again",
        "notebook": "Notebook", "notebook_sub": "an interactive recipe book",
        "config": "⚙️ cells", "config_sub": "look for your key",
        "vivo": "LIVE", "vivo_sub": "found your key",
        "mock": "MOCK", "mock_sub": "a simulator, no key",
        "d1": "Your key", "d1s": "is it well formed?",
        "d2": "Model list", "d2s": "does yours exist?",
        "d3": "Real question", "d3s": "time and tokens",
        "d4": "Tool", "d4s": "can it ask for it?",
        "d5": "Embeddings", "d5s": "does it find similar texts?",
        "listo": "Verdict: «✅ entorno listo» (environment ready) or exactly what to fix",
        "rompes": "What you break", "ves": "What you see", "haces": "What you do",
        "x1": "A fake key", "x1v": "Key rejected", "x1h": "Copy it whole, no spaces",
        "x2": "A model that doesn't exist", "x2v": "Doesn't exist", "x2h": "Copy the exact name",
        "x3": "Only 8 tokens to write", "x3v": "Empty answer", "x3h": "Give it more room",
        "diagnostico": "The diagnosis tells you in plain words what happened and what to do",
        "corrige": "Fix something", "corrige_sub": "retrying won't help",
        "esperar": "Wait and retry", "esperar_sub": "it fixes itself",
        "e401": "Key rejected", "a401": "«Invalid card»",
        "e403": "No access to that model", "a403": "«Transaction not allowed»",
        "e404": "Model or route doesn't exist", "a404": "«Account not found»",
        "e410": "Model retired", "a410": "«Card cancelled»",
        "e429": "Too many requests", "a429": "«Try again later»",
        "e5xx": "Server failure", "a5xx": "«ATM out of service»",
        "nunca401": "More waiting or more retries <b>never</b> fix a 401",
        "intento": "Attempt", "ok": "✓ answers",
        "espera_s": "wait {} s",
        "limite_intentos": "Always with a cap on attempts: 1 s, 2 s, 4 s… then it stops",
        "no401": "With a 401 it doesn't even retry: waiting won't fix a bad key",
        "doctor": "The doctor", "doctor_sub": "your checks and timings",
        "reporte": "Environment report", "reporte_sub": "no secrets",
        "rep_chips": ["Python", "Mode", "Routes", "Checks", "Timing"],
        "pegas": "paste it to ask for help",
        "soporte_sub": "in 3.3 it reads it to diagnose",
        "sin_key": "Your key never shows up in the report: the notebook checks it",
    },
}


# ------------------------------------------------------------------------------------------
# Clase 1.2 · Cuenta y API key
# ------------------------------------------------------------------------------------------
def c12_tarjeta(lang):
    t = T[lang]
    tarjeta = '<code class="c12-nvapi">nvapi-••••••••</code>'
    return ('<div class="dg dg-row">'
            + nodo("person", t["tu"], t["tu_sub"], paso=1)
            + flecha("h", paso=2)
            + nodo("key", t["key"], t["key_sub"], clase="is-primary c12-acceso", paso=2, extra=tarjeta)
            + flecha("h", t["a_tu_nombre"], paso=3)
            + nodo("language", "build.nvidia.com", t["build_sub"], paso=3)
            + flecha("h", paso=4)
            + nodo("auto_awesome", "Nemotron", t["nemotron_sub"], clase="ok", paso=4)
            + "</div>" + pie(t["como_pass"], paso=5, icono="lock"))


def c12_pasos_cuenta(lang):
    t = T[lang]
    etapas = [("login", t["cp1"], t["cp1s"]), ("mail", t["cp2"], t["cp2s"]), ("key", t["cp3"], t["cp3s"]),
              ("content_copy", t["cp4"], t["cp4s"]), ("chat", t["cp5"], t["cp5s"])]
    pasos = "".join(f'<div class="dg-stage" data-paso="{i + 1}"><span class="dg-ico">{ic}</span>'
                    f'<b>{a}</b><small>{b}</small></div>' for i, (ic, a, b) in enumerate(etapas))
    return (f'<div class="dg dg-timeline"><div class="dg-track"></div>{pasos}</div>'
            + f'<div class="call warn" data-paso="6"><p>{t["sms"]}</p></div>')


def c12_donde_guardar(lang):
    t = T[lang]
    si = [("password", t["gestor"], t["gestor_sub"]), ("key", t["colab"], t["colab_sub"]),
          ("description", t["env"], t["env_sub"]), ("language", t["panel"], t["panel_sub"])]
    no = [("chat", t["chat"], t["chat_sub"]), ("image", t["captura"], t["captura_sub"]),
          ("share", t["doc"], t["doc_sub"]), ("code", t["codigo"], t["codigo_sub"])]
    izq = "".join(nodo(ic, a, b, clase="mini ok") for ic, a, b in si)
    der = "".join(nodo(ic, a, b, clase="mini bad") for ic, a, b in no)
    return ('<div class="dg dg-two c12-two">'
            + f'<div class="dg-card is-primary" data-paso="1"><h3><span class="dg-i">verified</span> {t["seguro"]}</h3>'
              f'<div class="c12-grid2">{izq}</div></div>'
            + f'<div class="dg-card c12-nunca" data-paso="2"><h3><span class="dg-i">block</span> {t["nunca"]}</h3>'
              f'<div class="c12-grid2">{der}</div></div>'
            + "</div>" + pie(t["colab_pasos"], paso=3, icono="key"))


def c12_primera_llamada(lang):
    t = T[lang]
    filas = [(3, "article", "content", t["content_sub"]), (4, "flag", "finish_reason", t["finish_sub"]),
             (5, "token", "usage", t["usage_sub"])]
    leyenda = "".join(f'<div class="dg-legend-row" data-paso="{p}"><span class="dg-ico">{ic}</span>'
                      f'<div><b class="c12-campo">{n}</b><small>{sub}</small></div></div>' for p, ic, n, sub in filas)
    return ('<div class="dg dg-row">'
            + nodo("chat", t["pregunta"], t["pregunta_sub"], paso=1)
            + flecha("h", t["mas_key"], paso=1)
            + nodo("auto_awesome", "Nemotron", t["piensa"], clase="is-primary", paso=2)
            + flecha("h", paso=3)
            + f'<div class="dg-card c12-respuesta" data-paso="3"><h3><span class="dg-i">output</span> {t["respuesta"]}</h3>'
              f'<div class="dg-legend">{leyenda}</div></div>'
            + "</div>" + pie(t["token"], paso=6, icono="token"))


def c12_creditos(lang):
    t = T[lang]
    medidor = '<span class="c12-meter" aria-hidden="true"><span></span></span>'
    gastos = [("replay", t["g1"], t["g1s"]), ("bolt", t["g2"], t["g2s"]), ("article", t["g3"], t["g3s"])]
    return ('<div class="dg dg-row">'
            + nodo("paid", t["saldo"], t["saldo_sub"], clase="is-primary", paso=1, extra=medidor)
            + flecha("h", t["gastas"], paso=2)
            + nodo("speed", t["limite"], t["limite_sub"], clase="warn", paso=2)
            + flecha("h", paso=3)
            + nodo("schedule", t["espera"], t["espera_sub"], clase="ok", paso=3)
            + "</div>"
            + f'<div class="dg dg-row c12-gasta" data-paso="4"><span class="c12-tit">{t["mas_gasta"]}</span>'
            + "".join(nodo(ic, a, b, clase="mini warn") for ic, a, b in gastos)
            + "</div>" + pie(t["retirado"], paso=5, icono="update"))


def c12_filtrada(lang):
    t = T[lang]
    return ('<div class="dg dg-row">'
            + nodo("warning", t["filtro"], t["filtro_sub"], clase="bad", paso=1)
            + flecha("h", paso=2)
            + nodo("block", t["revoca"], t["revoca_sub"], clase="is-primary", paso=2)
            + flecha("h", paso=3)
            + nodo("key", t["nueva"], t["nueva_sub"], paso=3)
            + flecha("h", paso=4)
            + nodo("refresh", t["actualiza"], t["actualiza_sub"], clase="ok", paso=4)
            + "</div>"
            + f'<div class="call bad" data-paso="5"><p>{t["no_basta"]}</p></div>')


# ------------------------------------------------------------------------------------------
# Clase 1.3 · Rutas de modelo y errores
# ------------------------------------------------------------------------------------------
def c13_causas(lang):
    t = T[lang]
    causas = [(1, "key", t["c_key"], t["c_key_sub"]), (2, "edit", t["c_modelo"], t["c_modelo_sub"]),
              (3, "speed", t["c_limite"], t["c_limite_sub"])]
    col = "".join(f'<div class="c13-causa" data-paso="{p}"><span class="dg-ico">{ic}</span>'
                  f'<div><b>{a}</b><small>{b}</small></div></div>' for p, ic, a, b in causas)
    return ('<div class="dg dg-row">'
            + f'<div class="c13-causas">{col}</div>'
            + flecha("h", paso=4)
            + nodo("account_balance", t["aviso"], t["aviso_sub"], clase="is-primary big", paso=4,
                   extra=chips(["401", "404", "429"], "c13-codigos"))
            + "</div>" + pie(t["provocamos"], paso=5, icono="verified"))


def c13_ruta_postal(lang):
    t = T[lang]
    lineas = [(1, "home", t["dir"], t["dir_sub"], "integrate.api.nvidia.com/v1"),
              (2, "person", t["dest"], t["dest_sub"], "nvidia/nemotron-3.5-lightning-30b-a3b"),
              (3, "key", t["firma"], t["firma_sub"], "nvapi-••••••••")]
    sobre = "".join(f'<div class="c13-linea" data-paso="{p}"><span class="dg-i">{ic}</span>'
                    f'<div><b>{a}</b> <small>· {b}</small><code>{v}</code></div></div>' for p, ic, a, b, v in lineas)
    return ('<div class="dg dg-row">'
            + f'<div class="c13-sobre"><span class="c13-sello dg-i">mail</span><h3>{t["sobre"]}</h3>{sobre}</div>'
            + flecha("h", paso=4)
            + '<div class="dg-col c13-rutas">'
            + nodo("chat", t["r_chat"], t["r_chat_sub"], clase="mini ok", paso=4)
            + nodo("search", t["r_emb"], t["r_emb_sub"], clase="mini ok", paso=4)
            + "</div></div>" + pie(t["regresa"], paso=5, icono="undo"))


def c13_panel(lang):
    t = T[lang]

    def campo(p, etiqueta, valor, clase=""):
        return (f'<div class="c13-campo {clase}" data-paso="{p}"><span class="c13-etq">{etiqueta}</span>'
                f'<span class="c13-valor">{valor}</span></div>')

    def despliega(p, ic, etiqueta, valor, clase=""):
        return (f'<div class="c13-despl {clase}" data-paso="{p}"><span class="dg-i">{ic}</span>'
                f'<b>{etiqueta}</b><small>{valor}</small></div>')

    formulario = ('<div class="c13-form">'
                  + campo(1, t["f_url"], t["f_url_v"])
                  + campo(1, t["f_modelo"], t["f_modelo_v"])
                  + campo(1, t["f_key"], t["f_key_v"], "c13-clave")
                  + despliega(2, "check_circle", t["f_relay"], t["f_relay_v"])
                  + despliega(3, "expand_more", t["f_emb"], t["f_emb_v"])
                  + despliega(3, "expand_more", t["f_gest"], t["f_gest_v"])
                  + "</div>")
    return ('<div class="dg dg-row">'
            + formulario
            + flecha("h", t["guardar"], paso=4)
            + nodo("check_circle", t["conectado"], t["conectado_sub"], clase="ok", paso=4)
            + "</div>" + pie(t["pestana"], paso=5, icono="tab"))


def c13_doctor(lang):
    t = T[lang]
    arriba = ('<div class="dg-row">'
              + nodo("menu_book", t["notebook"], t["notebook_sub"], clase="mini", paso=1)
              + flecha("h", paso=1)
              + nodo("settings", t["config"], t["config_sub"], clase="mini", paso=1)
              + flecha("h", paso=2)
              + '<div class="dg-col c13-modos" data-paso="2">'
              + nodo("bolt", t["vivo"], t["vivo_sub"], clase="mini ok")
              + nodo("simulation", t["mock"], t["mock_sub"], clase="mini warn")
              + "</div></div>")
    etapas = [("key", t["d1"], t["d1s"]), ("list", t["d2"], t["d2s"]), ("chat", t["d3"], t["d3s"]),
              ("settings", t["d4"], t["d4s"]), ("search", t["d5"], t["d5s"])]
    pasos = "".join(f'<div class="dg-stage" data-paso="{i + 3}"><span class="dg-ico">{ic}</span>'
                    f'<b>{a}</b><small>{b}</small></div>' for i, (ic, a, b) in enumerate(etapas))
    return (f'<div class="dg c13-doctor">{arriba}'
            + f'<div class="dg dg-timeline"><div class="dg-track"></div>{pasos}</div></div>'
            + pie(t["listo"], paso=8, icono="check_circle"))


def c13_rompe(lang):
    t = T[lang]
    filas = [(1, "key", t["x1"], "401", t["x1v"], t["x1h"], "bad"),
             (2, "search", t["x2"], "404", t["x2v"], t["x2h"], "bad"),
             (3, "edit_note", t["x3"], "length", t["x3v"], t["x3h"], "warn")]
    cab = (f'<div class="c13-cab"><span>{t["rompes"]}</span><span></span><span>{t["ves"]}</span>'
           f'<span></span><span>{t["haces"]}</span></div>')
    cuerpo = "".join(
        f'<div class="c13-fila" data-paso="{p}">'
        f'<div class="c13-celda"><span class="dg-ico">{ic}</span><b>{a}</b></div>'
        + flecha("h")
        + f'<div class="c13-celda {c}"><span class="c13-cod">{cod}</span><b>{v}</b></div>'
        + flecha("h")
        + f'<div class="c13-celda ok"><span class="dg-i">check_circle</span><b>{h}</b></div></div>'
        for p, ic, a, cod, v, h, c in filas)
    return f'<div class="dg c13-tabla">{cab}{cuerpo}</div>' + pie(t["diagnostico"], paso=4, icono="translate")


def c13_avisos(lang):
    t = T[lang]

    def aviso(p, cod, sig, cajero):
        return (f'<div class="c13-aviso" data-paso="{p}"><span class="c13-cod">{cod}</span>'
                f'<div><b>{sig}</b><small>{cajero}</small></div></div>')

    izq = "".join(aviso(p, c, t["e" + c], t["a" + c]) for p, c in [(1, "401"), (2, "403"), (3, "404"), (4, "410")])
    der = "".join(aviso(p, c, t["e" + c], t["a" + c]) for p, c in [(5, "429"), (6, "5xx")])
    return ('<div class="dg dg-two c13-two">'
            + f'<div class="dg-card c13-corrige"><h3><span class="dg-i">edit</span> {t["corrige"]}</h3>'
              f'<small class="dg-card-sub">{t["corrige_sub"]}</small><div class="c13-avisos">{izq}</div></div>'
            + f'<div class="dg-card is-primary"><h3><span class="dg-i">schedule</span> {t["esperar"]}</h3>'
              f'<small class="dg-card-sub">{t["esperar_sub"]}</small><div class="c13-avisos">{der}</div></div>'
            + "</div>"
            + f'<div class="call warn" data-paso="7"><p>{t["nunca401"]}</p></div>')


def c13_backoff(lang):
    t = T[lang]
    fila = (nodo("send", f'{t["intento"]} 1', "429", clase="mini warn", paso=1)
            + flecha("h", t["espera_s"].format(1), paso=2)
            + nodo("send", f'{t["intento"]} 2', "429", clase="mini warn", paso=2)
            + flecha("h", t["espera_s"].format(2), paso=3)
            + nodo("send", f'{t["intento"]} 3', t["ok"], clase="ok", paso=3))
    return (f'<div class="dg dg-row">{fila}</div>'
            + pie(t["limite_intentos"], paso=4, icono="timer")
            + f'<div class="call bad" data-paso="5"><p>{t["no401"]}</p></div>')


def c13_reporte(lang):
    t = T[lang]
    return ('<div class="dg dg-row">'
            + nodo("assessment", t["doctor"], t["doctor_sub"], paso=1)
            + flecha("h", paso=2)
            + nodo("description", t["reporte"], t["reporte_sub"], clase="is-primary", paso=2,
                   extra=chips(t["rep_chips"]))
            + flecha("h", t["pegas"], paso=3)
            + nodo("forum", "Soporte NemoClaw", t["soporte_sub"], clase="ok", paso=3)
            + "</div>" + pie(t["sin_key"], paso=4, icono="lock"))


DIAGRAMAS = {
    "c12-tarjeta": c12_tarjeta,
    "c12-pasos-cuenta": c12_pasos_cuenta,
    "c12-donde-guardar": c12_donde_guardar,
    "c12-primera-llamada": c12_primera_llamada,
    "c12-creditos": c12_creditos,
    "c12-filtrada": c12_filtrada,
    "c13-causas": c13_causas,
    "c13-ruta-postal": c13_ruta_postal,
    "c13-panel": c13_panel,
    "c13-doctor": c13_doctor,
    "c13-rompe": c13_rompe,
    "c13-avisos": c13_avisos,
    "c13-backoff": c13_backoff,
    "c13-reporte": c13_reporte,
}
