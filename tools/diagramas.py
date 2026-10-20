"""Diagramas animados para las diapositivas (estilo Platzi Sinapsis).

En slides.md se usan con una línea sola:

    :::diagrama flujo-peticion

build_slides.py la reemplaza por el HTML de DIAGRAMAS["flujo-peticion"](lang).
Cada pieza puede llevar un número de paso: en la presentación aparece con cada clic
(→ o espacio), en el orden de los pasos. Al imprimir se ven todas.

Piezas (CSS en assets/slides.css, sección "Diagramas"):
  nodo(icono, título, sub)   tarjeta con ícono (Material Symbols, ver la lista en el subset)
  flecha("h" | "v")          conector con flujo animado; variante "bad" = bloqueado
  cuarto(etiqueta, ...)      el sandbox: borde punteado con candado
  chips([...])               etiquetas pequeñas
"""
import html

E = html.escape


def _paso(p):
    return f' data-paso="{p}"' if p else ""


def nodo(icono, titulo, sub="", clase="", paso=None, extra=""):
    sub_html = f"<small>{sub}</small>" if sub else ""
    return (f'<div class="dg-node {clase}"{_paso(paso)}><span class="dg-ico">{icono}</span>'
            f"<b>{titulo}</b>{sub_html}{extra}</div>")


def flecha(direccion="h", etiqueta="", clase="", paso=None):
    lab = f'<span class="dg-lab">{etiqueta}</span>' if etiqueta else ""
    # Una flecha con etiqueta mide lo que su texto (≈0.45em por carácter en monoespaciada pequeña)
    ancho = f' style="width:{max(2.6, len(etiqueta) * 0.45 + 1.2):.1f}em"' if etiqueta and direccion == "h" else ""
    return f'<div class="dg-arrow {direccion} {clase}"{_paso(paso)}{ancho}>{lab}</div>'


def chips(items, clase=""):
    return f'<div class="dg-chips {clase}">' + "".join(f'<span class="dg-chip">{x}</span>' for x in items) + "</div>"


def cuarto(etiqueta, contenido, paso=None, clase=""):
    return (f'<div class="dg-room {clase}"{_paso(paso)}><span class="dg-label"><span class="dg-i">lock</span>{etiqueta}</span>'
            f"{contenido}</div>")


def pie(texto, paso=None, icono="info"):
    return f'<p class="dg-note"{_paso(paso)}><span class="dg-i">{icono}</span>{texto}</p>'


# ------------------------------------------------------------------------------------------
# Textos por idioma
# ------------------------------------------------------------------------------------------
T = {
    "es": {
        "modelo": "Modelo", "llamada": "Una llamada a un modelo", "agente": "Un agente",
        "entra": "Texto entra", "sale": "Texto sale", "unavez": "Contesta una vez y olvida",
        "observar": "Observar", "decidir": "Decidir", "actuar": "Actuar", "parar": "¿Parar?",
        "herr": "Herramientas", "mem": "Memoria", "loop": "Repite hasta terminar la tarea",
        # seguridad
        "tu_agente": "Tu agente", "archivos": "Lee tus archivos", "comandos": "Ejecuta programas",
        "internet": "Sale a internet", "doc": "Un documento", "doc_sub": "con una instrucción escondida",
        "pregunta": "¿Cómo lo dejo trabajar solo <b>sin</b> darle las llaves de todo?",
        # tres piezas
        "openclaw_sub": "El agente · <em>el asistente</em>",
        "openshell_sub": "El sandbox · <em>el cuarto con cerradura</em>",
        "nemoclaw_sub": "El kit que arma todo · <em>instala y configura</em>",
        "cuarto": "OpenShell · cuarto con cerradura",
        # flujo
        "tu": "Tú", "tu_sub": "escribes una petición", "cli_sub": "la herramienta de NemoClaw",
        "gw": "Gateway de OpenShell", "gw_sub": "la recepción, fuera del cuarto",
        "reglas": "Reglas", "modelos": "Modelos", "llaves": "Llaves",
        "key": "Tu API key se queda aquí", "sandbox": "Sandbox · cuarto con cerradura",
        "oc_sub": "el agente trabaja aquí dentro",
        "nv": "Modelo de NVIDIA", "nv_sub": "build.nvidia.com · la key se agrega afuera",
        "net": "Internet", "net_sub": "bloqueado, salvo la lista permitida",
        # proyecto
        "m": "Módulo", "p2": "Conversa, usa herramientas y busca en la FAQ",
        "p3": "Clasifica, cita sus fuentes, reparte trabajo y deja trazas",
        "p4": "Vive en un laboratorio real y trabaja solo",
        "p5": "Lo revisas y lo encierras con reglas", "p6": "Le das recetas nuevas y lo llevas a tu casa",
        "proy": "Soporte NemoClaw: un agente que responde dudas del curso",
        # mapa
        "m13": "Módulos 1 a 3", "m13_sub": "Navegador y Colab · solo una API key gratis",
        "m46": "Módulos 4 a 6", "m46_sub": "Un laboratorio en la nube · cupón de 1 USD",
        "nada": "No instalas nada en tu computadora",
        "navegador": "Navegador", "agente_corto": "Agente",
        # dónde está todo
        "platzi": "Tu clase en Platzi", "platzi_sub": "el video",
        "pagina": "La página de la clase", "pagina_sub": "un enlace debajo del video",
        "esencial": "Lo esencial", "esencial_sub": "la idea, sin tecnicismos",
        "slides": "Diapositivas", "slides_sub": "lo que ves en el video",
        "practica": "Práctica", "practica_sub": "Colab o laboratorio, paso a paso",
        "glosario": "Glosario", "glosario_sub": "cada palabra nueva",
        "lab": "Tu laboratorio", "lab_sub": "crédito y sesiones",
        "sin_github": "No necesitas GitHub, programar ni instalar nada para empezar",
        # Brev / 4.1
        "consola": "Consola de Brev", "consola_sub": "enciendes y apagas tu máquina",
        "instancia": "Tu instancia", "instancia_sub": "una computadora rentada por horas",
        "launch": "Launchable", "launch_sub": "ya trae NemoClaw instalado",
        "curso": "Página del curso de NVIDIA", "curso_sub": "botones ▶ para cada paso",
        "cookie": "Cookie de sesión", "cookie_sub": "la pulsera que prueba que eres tú",
        "running": "Encendida", "running_sub": "cobra la máquina y el disco",
        "stopped": "Detenida", "stopped_sub": "cobra solo el disco",
        "deleted": "Borrada", "deleted_sub": "no cobra · se pierde todo",
        "credito": "≈ USD 0.15 por hora encendida · tu cupón: 1 USD ≈ 6 horas",
        "ruta_meta": "Tu sesión", "ruta_meta_sub": "¿eres tú?",
        "ruta_gw": "Recepción", "ruta_gw_sub": "¿el agente contesta?",
        "ruta_term": "Terminal", "ruta_term_sub": "¿hay una consola?",
        "ruta_health": "Salud", "ruta_health_sub": "¿todo está sano?",
        "lista": "Conexión lista",
        "pegar": "Pégala solo aquí", "nunca": "Nunca en un chat, captura o video",
        "caduca": "Caduca al reanudar: copia una nueva",
        "b1": "Entra", "b1s": "brev.nvidia.com con tu cuenta de NVIDIA",
        "b2": "Organización", "b2s": "el crédito es de la organización",
        "b3": "Cupón", "b3s": "Billing → Credits → canjéalo",
        "b4": "Launchable", "b4s": "revisa el costo por hora",
        "b5": "Despliega", "b5s": "espera de 5 a 15 minutos",
        "no_retry": "Mientras se configura: no recargues la pestaña ni toques RETRY",
    },
    "en": {
        "modelo": "Model", "llamada": "A call to a model", "agente": "An agent",
        "entra": "Text in", "sale": "Text out", "unavez": "Answers once and forgets",
        "observar": "Observe", "decidir": "Decide", "actuar": "Act", "parar": "Stop?",
        "herr": "Tools", "mem": "Memory", "loop": "Repeats until the task is done",
        "tu_agente": "Your agent", "archivos": "Reads your files", "comandos": "Runs programs",
        "internet": "Goes online", "doc": "A document", "doc_sub": "with a hidden instruction",
        "pregunta": "How do I let it work alone <b>without</b> handing over every key?",
        "openclaw_sub": "The agent · <em>the assistant</em>",
        "openshell_sub": "The sandbox · <em>the locked room</em>",
        "nemoclaw_sub": "The kit that sets it all up · <em>installs and configures</em>",
        "cuarto": "OpenShell · locked room",
        "tu": "You", "tu_sub": "you send a request", "cli_sub": "NemoClaw's tool",
        "gw": "OpenShell gateway", "gw_sub": "the front desk, outside the room",
        "reglas": "Rules", "modelos": "Models", "llaves": "Keys",
        "key": "Your API key stays here", "sandbox": "Sandbox · locked room",
        "oc_sub": "the agent works in here",
        "nv": "NVIDIA model", "nv_sub": "build.nvidia.com · key added outside",
        "net": "Internet", "net_sub": "blocked, except the allow list",
        "m": "Module", "p2": "Talks, uses tools and searches the FAQ",
        "p3": "Classifies, cites sources, splits work and leaves traces",
        "p4": "Lives in a real lab and works on its own",
        "p5": "You review it and lock it in with rules", "p6": "New recipes, and you take it home",
        "proy": "Soporte NemoClaw: an agent that answers course questions",
        "m13": "Modules 1 to 3", "m13_sub": "Browser and Colab · just a free API key",
        "m46": "Modules 4 to 6", "m46_sub": "A lab in the cloud · 1 USD coupon",
        "nada": "You don't install anything on your computer",
        "navegador": "Browser", "agente_corto": "Agent",
        "platzi": "Your Platzi class", "platzi_sub": "the video",
        "pagina": "The class page", "pagina_sub": "a link under the video",
        "esencial": "The essentials", "esencial_sub": "the idea, no jargon",
        "slides": "Slides", "slides_sub": "what you see in the video",
        "practica": "Practice", "practica_sub": "Colab or lab, step by step",
        "glosario": "Glossary", "glosario_sub": "every new word",
        "lab": "Your lab", "lab_sub": "credit and sessions",
        "sin_github": "You don't need GitHub, coding or installing anything to start",
        "consola": "Brev console", "consola_sub": "turn your machine on and off",
        "instancia": "Your instance", "instancia_sub": "a computer rented by the hour",
        "launch": "Launchable", "launch_sub": "NemoClaw comes preinstalled",
        "curso": "NVIDIA course page", "curso_sub": "▶ buttons for each step",
        "cookie": "Session cookie", "cookie_sub": "the wristband that proves it's you",
        "running": "Running", "running_sub": "machine and disk are billed",
        "stopped": "Stopped", "stopped_sub": "only the disk is billed",
        "deleted": "Deleted", "deleted_sub": "nothing billed · everything lost",
        "credito": "≈ USD 0.15 per hour running · your coupon: 1 USD ≈ 6 hours",
        "ruta_meta": "Your session", "ruta_meta_sub": "is it you?",
        "ruta_gw": "Front desk", "ruta_gw_sub": "does the agent answer?",
        "ruta_term": "Terminal", "ruta_term_sub": "is there a console?",
        "ruta_health": "Health", "ruta_health_sub": "is everything healthy?",
        "lista": "Connection ready",
        "pegar": "Paste it only here", "nunca": "Never in a chat, screenshot or video",
        "caduca": "Expires when you resume: copy a new one",
        "b1": "Sign in", "b1s": "brev.nvidia.com with your NVIDIA account",
        "b2": "Organization", "b2s": "credit belongs to the organization",
        "b3": "Coupon", "b3s": "Billing → Credits → redeem it",
        "b4": "Launchable", "b4s": "check the hourly cost",
        "b5": "Deploy", "b5s": "wait 5 to 15 minutes",
        "no_retry": "While it sets up: don't reload the tab or click RETRY",
    },
}


# ------------------------------------------------------------------------------------------
# Diagramas
# ------------------------------------------------------------------------------------------
def modelo_vs_agente(lang):
    t = T[lang]
    izq = (f'<div class="dg-card" data-paso="1"><h3>{t["llamada"]}</h3><div class="dg-col">'
           + chips([t["entra"]]) + flecha("v") + nodo("auto_awesome", t["modelo"]) + flecha("v") + chips([t["sale"]])
           + f'</div>{pie(t["unavez"], icono="history")}</div>')
    pasos = [("visibility", t["observar"]), ("insights", t["decidir"]), ("bolt", t["actuar"]), ("flag", t["parar"])]
    anillo = "".join(f'<div class="dg-loop-step s{i}"><span class="dg-ico">{ic}</span><b>{tx}</b></div>'
                     for i, (ic, tx) in enumerate(pasos))
    der = (f'<div class="dg-card is-primary" data-paso="2"><h3>{t["agente"]}</h3>'
           f'<div class="dg-loop"><div class="dg-loop-ring"></div>{anillo}'
           f'<div class="dg-loop-center">{nodo("auto_awesome", t["modelo"], clase="mini")}</div></div>'
           + chips([f'<span class="dg-i">settings</span>{t["herr"]}', f'<span class="dg-i">edit_note</span>{t["mem"]}'], "dg-pop")
           + pie(t["loop"], icono="replay") + "</div>")
    return f'<div class="dg dg-two">{izq}{der}</div>'


def agente_sin_cerradura(lang):
    t = T[lang]
    return ('<div class="dg dg-star">'
            + nodo("description", t["doc"], t["doc_sub"], clase="warn", paso=3)
            + flecha("h", clase="warn", paso=3)
            + nodo("auto_awesome", t["tu_agente"], clase="is-primary big")
            + '<div class="dg-fan">'
            + "".join(f'<div class="dg-fan-row" data-paso="{p}">{flecha("h")}{nodo(ic, tx, clase="mini")}</div>'
                      for p, ic, tx in [(1, "folder_open", t["archivos"]), (1, "terminal", t["comandos"]),
                                        (2, "public", t["internet"])])
            + "</div></div>"
            + f'<div class="call warn" data-paso="4"><p>{t["pregunta"]}</p></div>')


def tres_piezas(lang):
    t = T[lang]
    agente = nodo("assistant", "OpenClaw", clase="is-primary big")
    grafico = ('<div class="dg-kit" data-paso="3"><span class="dg-label"><span class="dg-i">category</span>NemoClaw</span>'
               + cuarto("OpenShell", f'<div data-paso="1">{agente}</div>', paso=2) + "</div>")
    filas = [(1, "assistant", "OpenClaw", t["openclaw_sub"], "is-primary"),
             (2, "lock", "OpenShell", t["openshell_sub"], "room"),
             (3, "category", "NemoClaw", t["nemoclaw_sub"], "kit")]
    leyenda = "".join(f'<div class="dg-legend-row {c}" data-paso="{p}"><span class="dg-ico">{ic}</span>'
                      f'<div><b>{n}</b><small>{sub}</small></div></div>' for p, ic, n, sub, c in filas)
    return f'<div class="dg dg-pieces">{grafico}<div class="dg-legend">{leyenda}</div></div>'


def flujo_peticion(lang):
    t = T[lang]
    gw_extra = chips([t["reglas"], t["modelos"], t["llaves"]])
    fila = (nodo("person", t["tu"], t["tu_sub"], paso=1)
            + flecha("h", paso=1)
            + nodo("terminal", "nemoclaw", t["cli_sub"], paso=1)
            + flecha("h", paso=2)
            + nodo("domain", t["gw"], t["gw_sub"], paso=2, extra=gw_extra)
            + flecha("h", paso=3)
            + cuarto(t["sandbox"], nodo("assistant", "OpenClaw", t["oc_sub"], clase="is-primary"), paso=3))
    abajo = (f'<div class="dg-key" data-paso="2"><span class="dg-i">key</span>{t["key"]}</div>'
             + '<div class="dg-branches">'
             + f'<div class="dg-branch" data-paso="4">{flecha("v")}{nodo("auto_awesome", t["nv"], t["nv_sub"], clase="ok mini")}</div>'
             + f'<div class="dg-branch" data-paso="5">{flecha("v", clase="bad")}{nodo("public", t["net"], t["net_sub"], clase="bad mini")}</div>'
             + "</div>")
    return f'<div class="dg dg-flowgrid">{fila}{abajo}</div>'


def proyecto_crece(lang):
    t = T[lang]
    etapas = [(2, "chat", t["p2"]), (3, "route", t["p3"]), (4, "computer", t["p4"]), (5, "lock", t["p5"]), (6, "menu_book", t["p6"])]
    pasos = "".join(f'<div class="dg-stage" data-paso="{i + 1}"><span class="dg-ico">{ic}</span>'
                    f'<span class="dg-stage-m">{t["m"]} {m}</span><b>{tx}</b></div>'
                    for i, (m, ic, tx) in enumerate(etapas))
    return f'<div class="dg dg-timeline"><div class="dg-track"></div>{pasos}</div>' + pie(t["proy"], icono="forum")


def mapa_curso(lang):
    t = T[lang]
    return ('<div class="dg dg-two">'
            + f'<div class="dg-card" data-paso="1"><h3>{t["m13"]}</h3><div class="dg-row tight">'
            + nodo("language", t["navegador"])
            + nodo("code", "Colab") + nodo("key", "API key") + f'</div>{pie(t["m13_sub"], icono="check_circle")}</div>'
            + f'<div class="dg-card is-primary" data-paso="2"><h3>{t["m46"]}</h3><div class="dg-row tight">'
            + nodo("computer", "Brev") + nodo("lock", "OpenShell") + nodo("assistant", t["agente_corto"])
            + f'</div>{pie(t["m46_sub"], icono="paid")}</div>'
            + "</div>" + pie(t["nada"], paso=3, icono="verified"))


def donde_esta_todo(lang):
    t = T[lang]
    tiles = [("auto_awesome", t["esencial"], t["esencial_sub"]), ("pages", t["slides"], t["slides_sub"]),
             ("play_arrow", t["practica"], t["practica_sub"]), ("menu_book", t["glosario"], t["glosario_sub"]),
             ("paid", t["lab"], t["lab_sub"])]
    grid = "".join(nodo(ic, a, b, clase="mini") for ic, a, b in tiles)
    return ('<div class="dg dg-flow">'
            + '<div class="dg-row">'
            + nodo("smart_display", t["platzi"], t["platzi_sub"], paso=1)
            + flecha("h", paso=2)
            + f'<div class="dg-card is-primary" data-paso="2"><h3><span class="dg-i">web</span> {t["pagina"]}</h3>'
              f'<small class="dg-card-sub">{t["pagina_sub"]}</small><div class="dg-grid">{grid}</div></div>'
            + "</div></div>" + pie(t["sin_github"], paso=3, icono="verified"))


def brev_laboratorio(lang):
    t = T[lang]
    return ('<div class="dg dg-flow"><div class="dg-row">'
            + nodo("dashboard", t["consola"], t["consola_sub"], paso=1)
            + flecha("h", paso=2)
            + cuarto(t["instancia"], f'<small class="dg-room-sub">{t["instancia_sub"]}</small>'
                     + nodo("rocket_launch", t["launch"], t["launch_sub"], clase="is-primary mini"), paso=2)
            + flecha("h", paso=3)
            + nodo("language", t["curso"], t["curso_sub"], paso=3)
            + "</div></div>")


def estados_instancia(lang):
    t = T[lang]
    return ('<div class="dg dg-row states">'
            + nodo("play_arrow", t["running"], t["running_sub"], clase="ok", paso=1)
            + flecha("h", "Stop", paso=2)
            + nodo("pause", t["stopped"], t["stopped_sub"], clase="warn", paso=2)
            + flecha("h", "Delete", paso=3)
            + nodo("delete", t["deleted"], t["deleted_sub"], clase="bad", paso=3)
            + "</div>" + pie(t["credito"], paso=4, icono="paid"))


def cuatro_rutas(lang):
    t = T[lang]
    rutas = [("badge", t["ruta_meta"], t["ruta_meta_sub"]), ("domain", t["ruta_gw"], t["ruta_gw_sub"]),
             ("terminal", t["ruta_term"], t["ruta_term_sub"]), ("favorite", t["ruta_health"], t["ruta_health_sub"])]
    fila = ""
    for i, (ic, a, b) in enumerate(rutas, 1):
        if i > 1:
            fila += flecha("h", paso=i)
        fila += nodo(ic, a, b, clase="mini", paso=i)
    return (f'<div class="dg dg-row">{fila}{flecha("h", paso=5)}'
            + nodo("check_circle", t["lista"], clase="ok", paso=5) + "</div>")


def cookie_segura(lang):
    t = T[lang]
    return ('<div class="dg dg-row">'
            + nodo("rocket_launch", t["launch"], clase="mini", paso=1)
            + flecha("h", "F12 → Application → Cookies", paso=1)
            + nodo("cookie", t["cookie"], t["cookie_sub"], clase="is-primary", paso=1)
            + flecha("h", paso=2)
            + nodo("language", t["curso"], t["pegar"], clase="ok", paso=2)
            + "</div>"
            + '<div class="dg-row tight">'
            + pie(t["nunca"], paso=3, icono="block")
            + pie(t["caduca"], paso=4, icono="refresh")
            + "</div>")


def brev_pasos(lang):
    t = T[lang]
    etapas = [("login", t["b1"], t["b1s"]), ("groups", t["b2"], t["b2s"]), ("paid", t["b3"], t["b3s"]),
              ("rocket_launch", t["b4"], t["b4s"]), ("play_arrow", t["b5"], t["b5s"])]
    pasos = "".join(f'<div class="dg-stage" data-paso="{i + 1}"><span class="dg-ico">{ic}</span>'
                    f'<b>{a}</b><small>{b}</small></div>' for i, (ic, a, b) in enumerate(etapas))
    return (f'<div class="dg dg-timeline"><div class="dg-track"></div>{pasos}</div>'
            + f'<div class="call warn" data-paso="6"><p>{t["no_retry"]}</p></div>')


DIAGRAMAS = {
    "brev-pasos": brev_pasos,
    "modelo-vs-agente": modelo_vs_agente,
    "agente-sin-cerradura": agente_sin_cerradura,
    "tres-piezas": tres_piezas,
    "flujo-peticion": flujo_peticion,
    "proyecto-crece": proyecto_crece,
    "mapa-curso": mapa_curso,
    "donde-esta-todo": donde_esta_todo,
    "brev-laboratorio": brev_laboratorio,
    "estados-instancia": estados_instancia,
    "cuatro-rutas": cuatro_rutas,
    "cookie-segura": cookie_segura,
}


def registro():
    """Todos los diagramas: los de este archivo más los de tools/diagramas_m1.py … diagramas_m6.py
    (cada módulo del curso tiene su archivo, con su propio diccionario DIAGRAMAS)."""
    import importlib
    todos = dict(DIAGRAMAS)
    for m in range(1, 7):
        try:
            mod = importlib.import_module(f"diagramas_m{m}")
        except ModuleNotFoundError:
            continue
        repetidos = set(todos) & set(mod.DIAGRAMAS)
        if repetidos:
            raise ValueError(f"diagramas_m{m}: nombres repetidos {sorted(repetidos)}")
        todos.update(mod.DIAGRAMAS)
    return todos
