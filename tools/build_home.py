"""Construye la portada del curso (fork de la portada del curso de NVIDIA) en dos idiomas:
  index.html     español (principal)
  en/index.html  inglés (textos en tools/course_en.py)

Sirve abierta como archivo local o publicada con GitHub Pages desde la raíz del repo.
Uso:  python3 tools/build_home.py
"""
import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from course import CLASSES, COURSE, MODULES, NV  # noqa: E402
from course_en import CLASSES_EN, COURSE_EN, MODULES_EN  # noqa: E402
from diagramas import DIAGRAMAS  # noqa: E402

NV_EN = "https://nvdli.github.io/NemoClawDLI/nemoclaw/"

ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape

PRACTICA = {"notebook": "Notebook", "lab": "Laboratorio Brev", "slides": "Diapositivas", "navegador": "Navegador"}
PRACTICE_EN = {"notebook": "Notebook", "lab": "Brev lab", "slides": "Slides", "navegador": "Browser"}

# Etiquetas de la interfaz por idioma. En inglés, el material de cada clase sigue en español: se marca (ES).
UI = {
    "es": {"guide": "Guía", "slides": "Diapositivas", "nb": "Colab", "cb": "Recetario",
           "skill": "Habilidad", "module": "Módulo", "classes": "clases",
           "mats": "Material", "names": ("guía", "diapositivas", "notebook", "cookbook")},
    "en": {"guide": "Guide", "slides": "Slides", "nb": "Colab (ES)", "cb": "Cookbook (ES)",
           "skill": "Skill", "module": "Module", "classes": "classes",
           "mats": "Materials (ES)", "names": ("guide", "slides", "notebook", "cookbook")},
}


def repo(path, folder=False, prefix=""):
    """Enlace a un archivo del repo: a GitHub si COURSE['github'] existe, si no, relativo
    (prefix="../" para páginas que viven en una subcarpeta, como en/index.html)."""
    if COURSE.get("github"):
        kind = "tree" if folder else "blob"
        return f"https://github.com/{COURSE['github']}/{kind}/main/{path}"
    return prefix + path + ("/" if folder and not path.endswith("/") else "")


def class_card(c, lang="es"):
    t, pre = UI[lang], ("" if lang == "es" else "../")
    if lang == "es":
        title, promesa, skill_txt, nv, practica = c["title"], c["promesa"], c.get("skill"), NV, PRACTICA
    else:
        title, promesa, skill_txt = CLASSES_EN[c["id"]]
        nv, practica = NV_EN, PRACTICE_EN
    folder = ROOT / "clases" / c["slug"]
    base = f"clases/{c['slug']}"
    en_guide = ROOT / "en" / base / "README.md"
    # Las guías son páginas web (tools/build_guias.py): clases/<slug>/index.html, sin GitHub ni .md
    if lang == "en" and en_guide.exists():
        links = [f'<a href="{base}/index.html"><span class="icon">description</span>Guide</a>']
    else:
        links = [f'<a href="{pre}{base}/index.html"><span class="icon">description</span>{t["guide"]}</a>']
    en_slides = ROOT / "en" / base / "slides.html"
    if lang == "en" and en_slides.exists():         # diapositivas traducidas
        links.append(f'<a href="{base}/slides.html"><span class="icon">pages</span>Slides</a>')
    elif (folder / "slides.html").exists():
        links.append(f'<a href="{pre}{base}/slides.html"><span class="icon">pages</span>{t["slides"]}</a>')
    nb = folder / f"{c['slug']}.ipynb"
    if nb.exists():
        nb_href = (f"https://colab.research.google.com/github/{COURSE['github']}/blob/main/{base}/{nb.name}"
                   if COURSE.get("github") else pre + base + "/" + nb.name)
        links.append(f'<a href="{nb_href}" target="_blank" rel="noopener"><span class="icon">play_arrow</span>{t["nb"]}</a>')
    if (folder / "cookbook.md").exists():
        links.append(f'<a href="{pre}{base}/cookbook.html"><span class="icon">terminal</span>{t["cb"]}</a>')

    have = [True, (folder / "slides.html").exists(), nb.exists(), (folder / "cookbook.md").exists()]
    names = [n for n, h in zip(t["names"], have) if h]
    if lang == "en" and en_guide.exists():
        en_have = ["guide"] + (["slides"] if en_slides.exists() else [])
        es_only = [n for n in names[1:] if n not in en_have]
        rest = f" · {', '.join(es_only)} (ES)" if es_only else ""
        mats = f'<p class="mats">{", ".join(en_have).capitalize()} (EN){rest}</p>'
    else:
        mats = f'<p class="mats">{t["mats"]}: {", ".join(names)}</p>'
    skill = f'<p class="skill">{t["skill"]}: {E(skill_txt)}</p>' if skill_txt else ""
    return (f'<article class="clase"><div class="clase-top"><span class="num">{c["id"]}</span>'
            f'<span class="badge b-{c["practica"]}">{practica[c["practica"]]}</span>'
            f'<span class="min">{c["minutes"]} min</span></div>'
            f'<h4>{E(title)}</h4>'
            f'<ul class="promesa">{"".join(f"<li>{E(p)}</li>" for p in promesa)}</ul>'
            f'{skill}{mats}<nav>{"".join(links)}</nav></article>')


def modules_html(lang="es"):
    t = UI[lang]
    out = []
    for m in MODULES:
        cls = [c for c in CLASSES if c["module"] == m["n"]]
        mins = sum(c["minutes"] for c in cls)
        title, outcome, where = (m["title"], m["outcome"], m["where"]) if lang == "es" else MODULES_EN[m["n"]]
        out.append(f'<section class="modulo" id="modulo-{m["n"]}"><header><span class="mnum">{t["module"]} {m["n"]}</span>'
                   f'<h3>{E(title)}</h3><p>{E(outcome)}</p>'
                   f'<p class="meta">{len(cls)} {t["classes"]} · ≈{mins} min · {E(where)}</p></header>'
                   f'<div class="clases">{"".join(class_card(c, lang) for c in cls)}</div></section>')
    return "\n".join(out)


ERRORES = [
    ("401 Unauthorized", "La key está mal copiada, tiene espacios o fue revocada.", "Cópiala completa (empieza con <code>nvapi-</code>) y vuelve a correr la celda de configuración."),
    ("403 Forbidden", "Key válida pero sin acceso al modelo o sin créditos.", "Revisa tu cuenta en build.nvidia.com o cambia de modelo."),
    ("404 / 410", "El modelo no existe o fue retirado del endpoint gratuito.", "Copia el ID exacto del catálogo; actualiza <code>NVIDIA_MODEL</code>."),
    ("429 Too Many Requests", "Demasiadas solicitudes por minuto.", "Espera unos segundos; reintenta con backoff."),
    ("finish_reason = length", "El modelo razonó hasta agotar <code>max_tokens</code>.", "Sube <code>max_tokens</code> (los modelos que razonan lo necesitan)."),
    ("OpenClaw is starting / 503", "El launchable sigue arrancando.", "Espera; la verificación reintenta sola hasta 30 min."),
    ("OpenClaw ⚠ sesión expirada", "La cookie de acceso de Brev caducó o reanudaste la instancia.", "Vuelve a abrir el launchable, copia la cookie nueva y repite la verificación."),
    ("Out of credits en Brev", "A menudo es la organización equivocada activa.", "Cambia de organización en Brev antes de desplegar."),
]


ERRORS_EN = [
    ("401 Unauthorized", "The key was copied wrong, has spaces, or was revoked.", "Copy it in full (it starts with <code>nvapi-</code>) and rerun the setup cell."),
    ("403 Forbidden", "Valid key, but no access to the model or no credits left.", "Check your account at build.nvidia.com or switch models."),
    ("404 / 410", "The model doesn't exist or was retired from the free endpoint.", "Copy the exact ID from the catalog; update <code>NVIDIA_MODEL</code>."),
    ("429 Too Many Requests", "Too many requests per minute.", "Wait a few seconds; retry with backoff."),
    ("finish_reason = length", "The model reasoned until it ran out of <code>max_tokens</code>.", "Raise <code>max_tokens</code> (reasoning models need it)."),
    ("OpenClaw is starting / 503", "The launchable is still starting up.", "Wait; the check retries on its own for up to 30 min."),
    ("OpenClaw ⚠ session expired", "Your Brev access cookie expired or you resumed the instance.", "Reopen the launchable, copy the new cookie, and rerun the check."),
    ("Out of credits on Brev", "Often the wrong organization is active.", "Switch organizations in Brev before deploying."),
]


def estilos(pre):
    import hashlib
    ver = hashlib.md5(b"".join((ROOT / "assets" / f).read_bytes() for f in ("sinapsis.css", "diagramas.css", "home.css"))).hexdigest()[:8]
    return "\n".join(f'<link rel="stylesheet" href="{pre}assets/{f}?v={ver}">' for f in ("sinapsis.css", "diagramas.css", "home.css"))


def cabecera(lang, pre, n_clases, horas):
    es = lang == "es"
    title = COURSE["title"] if es else COURSE_EN["title"]
    sub = COURSE["subtitle"] if es else COURSE_EN["subtitle"]
    start = f"{pre}clases/{CLASSES[0]['slug']}/index.html" if es else f"clases/{CLASSES[0]['slug']}/index.html"
    links = [(f"{pre}GLOSARIO.html", "menu_book", "Glosario" if es else "Glossary (ES)"),
             (f"{pre}LABORATORIO.html", "paid", "Tu laboratorio" if es else "Your lab (ES)"),
             (f"{pre}FAQ.html", "quiz", "Preguntas frecuentes" if es else "FAQ (ES)"),
             ("en/index.html" if es else "../index.html", "translate", "English" if es else "Español")]
    nav = "".join(f'<a href="{h}"><span class="icon">{i}</span>{E(t)}</a>' for h, i, t in links)
    chips = ([f"6 módulos", f"{n_clases} clases", f"≈{horas} h de video", "en español", f"instructor: {COURSE['instructor']}"] if es else
             [f"6 modules", f"{n_clases} classes", f"≈{horas} h of video", "taught in Spanish", f"instructor: {COURSE['instructor']}"])
    iconos = ["view_kanban", "school", "smart_display", "translate", "person"]
    facts = "".join(f'<span class="chip"><span class="icon">{i}</span>{E(c)}</span>' for i, c in zip(iconos, chips))
    cta = ([("primary", start, "play_arrow", "Empieza con la clase 1.1", False),
            ("", COURSE["build"], "key", "Consigue tu API key ↗", True),
            ("", COURSE["launchable"], "computer", "Laboratorio en Brev ↗", True)] if es else
           [("primary", start, "play_arrow", "Start with class 1.1", False),
            ("", COURSE["build"], "key", "Get your API key ↗", True),
            ("", COURSE["launchable"], "computer", "Brev lab ↗", True)])
    botones = "".join(f'<a class="btn {c}" href="{h}"' + (' target="_blank" rel="noopener"' if ext else "") + f'><span class="icon">{i}</span>{E(t)}</a>'
                      for c, h, i, t, ext in cta)
    formas = "".join(f'<img src="{pre}assets/brand/{f}.svg" alt="">' for f in ("forma-4", "forma-1", "forma-8", "forma-3"))
    edicion = "" if es else '<p class="edition printonly">Course overview · v1.0 · October 2026 · launch: NVIDIA AI Day Mexico City</p>'
    return (f'<nav class="topbar"><div class="wrap"><a class="brand" href="{"index.html" if es else "index.html"}">'
            f'<img src="{pre}assets/brand/platzi-isotype-solid.svg" alt="">{E(title)}</a><span class="links">{nav}</span></div></nav>'
            f'<header class="hero"><div class="shapes" aria-hidden="true">{formas}</div><div class="wrap">'
            f'<img class="logo" src="{pre}assets/brand/platzi-logo-new.svg" alt="Platzi">{edicion}'
            f'<p class="tag">{E(COURSE["partner"])}</p><h1>{E(title)}</h1><p class="sub">{E(sub)}</p>'
            f'<p class="cta">{botones}</p><p class="facts">{facts}</p></div></header>')


def errores_html(lang="es"):
    data = ERRORES if lang == "es" else ERRORS_EN
    head = ("Síntoma", "Causa probable", "Qué hacer") if lang == "es" else ("Symptom", "Likely cause", "What to do")
    rows = "".join(f"<tr><td><code>{E(s)}</code></td><td>{c}</td><td>{f}</td></tr>" for s, c, f in data)
    return (f"<table><thead><tr><th>{head[0]}</th><th>{head[1]}</th><th>{head[2]}</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>")


PAGE_ES = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · {partner}</title>
<meta name="description" content="{subtitle}">
{estilos}
</head><body>
{cabecera}

<main class="wrap">
<section id="para-todos">
  <h2>¿No programas? Este curso también es para ti</h2>
  <div class="pasos">
    <div class="paso"><span>1</span><h3>Empieza por «Lo esencial»</h3><p>Cada clase abre con la idea en palabras simples, una comparación cotidiana y una actividad que haces sin programar. El detalle técnico queda abajo, para quien lo quiera.</p></div>
    <div class="paso"><span>2</span><h3>Notebooks con un botón</h3><p>En Colab presionas ▶ y lees lo que pasa. Las celdas de preparación (⚙️) están ocultas. Funcionan aunque todavía no tengas API key.</p></div>
    <div class="paso"><span>3</span><h3>Laboratorio desde el navegador</h3><p>Sin instalar nada. Con tu crédito de 1 USD alcanza si sigues el <a href="{laboratorio}">plan de 3 sesiones</a> y detienes la instancia al terminar.</p></div>
  </div>
  <p class="note">¿Una palabra que no entiendes? Está en el <a href="{glosario}">glosario en palabras simples</a>, con una comparación para cada término.</p>
</section>

<section id="como">
  <h2>Cómo funciona el curso</h2>
  <div class="pasos">
    <div class="paso"><span>1</span><h3>Tu acceso a modelos</h3><p>Creas una cuenta gratuita en NVIDIA Build y una API key <code>nvapi-</code>. Es lo único que necesitas en los módulos 1 a 3.</p></div>
    <div class="paso"><span>2</span><h3>Notebooks en Colab o local</h3><p>Construyes el agente desde cero en Python: loop, ReAct, herramientas, enrutamiento, RAG y subagentes. Sin key también corren, con un modelo simulado.</p></div>
    <div class="paso"><span>3</span><h3>Laboratorio real en Brev</h3><p>Desde el módulo 4 lanzas NemoClaw en una máquina en la nube: OpenClaw dentro de un sandbox de OpenShell. Lo operas desde el navegador; la terminal es opcional, para quien la quiera.</p></div>
  </div>
  <p class="note">Cada clase trae <strong>guía paso a paso</strong>, <strong>diapositivas</strong>, <strong>notebook o cookbook</strong> y una tabla de <strong>errores comunes</strong>. Las diapositivas empiezan con lo que aprendimos la clase pasada y terminan con lo que viene.</p>
</section>

<section id="stack">
  <h2>El stack en un vistazo</h2>
  <div class="stack">
    <div class="pieza"><h3>OpenClaw</h3><p class="rol">El agente · el asistente</p><p>Runtime con memoria, herramientas, sesiones y un workspace de archivos (<code>SOUL.md</code>, <code>AGENTS.md</code>, <code>MEMORY.md</code>, <code>skills/</code>).</p></div>
    <div class="pieza"><h3>OpenShell</h3><p class="rol">El sandbox · el cuarto con cerradura</p><p>Aísla al agente: red con lista de permitidos, archivos con Landlock, syscalls con seccomp, usuario sin privilegios. Enruta la inferencia sin meter tu key al sandbox.</p></div>
    <div class="pieza"><h3>NemoClaw</h3><p class="rol">El blueprint · el kit que arma todo</p><p>La pila de referencia de NVIDIA que instala, configura y opera OpenClaw dentro de OpenShell, con la CLI <code>nemoclaw</code> y políticas versionadas.</p></div>
  </div>
  <div class="home-dg">{diagrama_flujo}</div>
</section>

<section id="proyecto">
  <h2>Proyecto del curso: «Soporte NemoClaw»</h2>
  <p>Un solo agente que crece contigo: responde dudas de estudiantes sobre NemoClaw, Brev y el curso usando nuestras <a href="{faq}">preguntas frecuentes</a> como base de conocimiento.</p>
  <div class="home-dg">{diagrama_proyecto}</div>
</section>

<section id="clases">
  <h2>Clase por clase</h2>
  {modules}
</section>

<section id="errores">
  <h2>Los errores que más vas a ver</h2>
  {errores}
  <p>Hay más de 50 casos resueltos en las <a href="{faq}">preguntas frecuentes</a>. Antes de pedir ayuda, revisa la sección «Cómo pedir ayuda bien».</p>
</section>

<section id="objetivos">
  <h2>Objetivos de aprendizaje</h2>
  <p>Los cinco objetivos oficiales del curso de NVIDIA (en inglés, tal cual) y dónde se cubren:</p>
  <table><thead><tr><th>Objetivo (NVIDIA)</th><th>En español</th><th>Dónde</th></tr></thead><tbody>
    <tr><td>Build a basic agent loop and identify its core components.</td><td>Construir un loop básico de agente e identificar sus componentes</td><td>Módulo 2</td></tr>
    <tr><td>Implement reliable tool use and function calling within an agent system.</td><td>Implementar un uso confiable de herramientas y llamadas a funciones</td><td>Módulo 2</td></tr>
    <tr><td>Design and coordinate multi-agent systems using structured routing patterns.</td><td>Diseñar y coordinar sistemas multiagente con enrutamiento estructurado</td><td>Módulo 3</td></tr>
    <tr><td>Utilize OpenShell to configure agent identities and ensure safe, sandboxed operations.</td><td>Usar OpenShell para configurar identidades y operar en un sandbox seguro</td><td>Módulo 5</td></tr>
    <tr><td>Deploy and manage autonomous agents while building persistent skill libraries.</td><td>Desplegar y operar agentes autónomos con bibliotecas de skills persistentes</td><td>Módulos 4 y 6</td></tr>
  </tbody></table>
</section>
</main>

<footer><div class="wrap">
  <p>Basado en el curso open source <a href="{nvrepo}">«Securing Agents with OpenShell and NemoClaw»</a> de NVIDIA Deep Learning Institute (Apache-2.0) y en <a href="{nemoclaw}">NVIDIA NemoClaw</a>.</p>
  <p>NVIDIA, NemoClaw y OpenShell son marcas de NVIDIA Corporation. Este material es una adaptación de Platzi; no es un producto oficial de NVIDIA.</p>
</div></footer>
</body></html>
"""

PAGE_EN = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · {partner}</title>
<meta name="description" content="{subtitle}">
{estilos}
</head><body>
{cabecera}

<main class="wrap">
<p class="note">This is the English overview of a Spanish-language course. Class guides and slides are available in English; notebooks and cookbooks are in Spanish and marked <strong>(ES)</strong>.</p>

<section id="como">
  <h2>How the course works</h2>
  <div class="pasos">
    <div class="paso"><span>1</span><h3>Access to models</h3><p>You create a free NVIDIA Build account and an <code>nvapi-</code> API key. That's all you need for modules 1 to 3.</p></div>
    <div class="paso"><span>2</span><h3>Notebooks in Colab or locally</h3><p>You build the agent from scratch in Python: loop, ReAct, tools, routing, RAG and subagents. They also run without a key, using a simulated model.</p></div>
    <div class="paso"><span>3</span><h3>A real lab on Brev</h3><p>From module 4 you launch NemoClaw on a cloud machine: OpenClaw inside an OpenShell sandbox. You operate it from the browser and the terminal.</p></div>
  </div>
  <p class="note">Every class comes with a <strong>step-by-step guide</strong>, <strong>slides</strong>, a <strong>notebook or cookbook</strong>, and a table of <strong>common errors</strong>. The slides open with what we learned last class and close with what comes next.</p>
</section>

<section id="stack">
  <h2>The stack at a glance</h2>
  <div class="stack">
    <div class="pieza"><h3>OpenClaw</h3><p class="rol">The agent</p><p>A runtime with memory, tools, sessions and a file workspace (<code>SOUL.md</code>, <code>AGENTS.md</code>, <code>MEMORY.md</code>, <code>skills/</code>).</p></div>
    <div class="pieza"><h3>OpenShell</h3><p class="rol">The sandbox</p><p>Isolates the agent: allowlisted network, Landlock for files, seccomp for syscalls, an unprivileged user. It routes inference without putting your key inside the sandbox.</p></div>
    <div class="pieza"><h3>NemoClaw</h3><p class="rol">The blueprint</p><p>NVIDIA's reference stack that installs, configures and operates OpenClaw inside OpenShell, with the <code>nemoclaw</code> CLI and versioned policies.</p></div>
  </div>
  <div class="home-dg">{diagrama_flujo}</div>
</section>

<section id="proyecto">
  <h2>Course project: “Soporte NemoClaw”</h2>
  <p>One agent that grows with you: it answers student questions about NemoClaw, Brev and the course, using our <a href="{faq}">FAQ</a> as its knowledge base.</p>
  <div class="home-dg">{diagrama_proyecto}</div>
</section>

<section id="adaptacion">
  <h2>What this adaptation adds</h2>
  <table><thead><tr><th>NVIDIA DLI course</th><th>Platzi adaptation</th></tr></thead><tbody>
    <tr><td>12 interactive web lessons with JavaScript cells in the browser</td><td>20 short video classes in Spanish, each with a step-by-step guide, slides, hands-on practice and a common-errors table</td></tr>
    <tr><td>Exercises scoped to each lesson</td><td>One course project, “Soporte NemoClaw”, that grows from a chat loop to a skill running inside a sandbox</td></tr>
    <tr><td>Browser exercises that need an API key</td><td>Python notebooks for Colab or local use that also run offline with a simulated model; NVIDIA's browser lessons stay as complementary practice</td></tr>
    <tr><td>Lab driven from the browser</td><td>Lab driven from both the browser and the terminal (<code>brev</code>, <code>nemoclaw</code>, <code>openshell</code>) with reusable cookbooks</td></tr>
    <tr><td>Troubleshooting inside lesson messages</td><td>An 80-entry FAQ built from the NemoClaw docs and real GitHub issues, plus an error diagnoser inside every notebook</td></tr>
    <tr><td>Glossary and search in English</td><td>A Spanish knowledge base, used for RAG in the course project</td></tr>
  </tbody></table>
</section>

<section id="objetivos">
  <h2>Learning objectives</h2>
  <p>The five official objectives of the NVIDIA course, and where each one is covered:</p>
  <table><thead><tr><th>Objective (NVIDIA)</th><th>Where</th></tr></thead><tbody>
    <tr><td>Build a basic agent loop and identify its core components.</td><td>Module 2</td></tr>
    <tr><td>Implement reliable tool use and function calling within an agent system.</td><td>Module 2</td></tr>
    <tr><td>Design and coordinate multi-agent systems using structured routing patterns.</td><td>Module 3</td></tr>
    <tr><td>Utilize OpenShell to configure agent identities and ensure safe, sandboxed operations.</td><td>Module 5</td></tr>
    <tr><td>Deploy and manage autonomous agents while building persistent skill libraries.</td><td>Modules 4 and 6</td></tr>
  </tbody></table>
</section>

<section id="clases">
  <h2>Class by class</h2>
  {modules}
</section>

<section id="errores">
  <h2>The errors you'll see most</h2>
  {errores}
  <p>The <a href="{faq}">FAQ</a> (in Spanish) has more than 50 solved cases. Before asking for help, read its “Cómo pedir ayuda bien” (how to ask for help) section.</p>
</section>


</main>

<footer><div class="wrap">
  <p>Based on NVIDIA Deep Learning Institute's open-source course <a href="{nvrepo}">“Securing Agents with OpenShell and NemoClaw”</a> (Apache-2.0) and on <a href="{nemoclaw}">NVIDIA NemoClaw</a>.</p>
  <p>NVIDIA, NemoClaw and OpenShell are trademarks of NVIDIA Corporation. This material is an adaptation by Platzi; it is not an official NVIDIA product.</p>
</div></footer>
</body></html>
"""


def readme_table():
    """Tabla de clases para README.md (entre los marcadores clases:inicio / clases:fin)."""
    rows = ["| Clase | Título | Práctica | Min | Material |", "|---|---|---|---|---|"]
    for m in MODULES:
        rows.append(f"| **M{m['n']}** | **{m['title']}** | | | |")
        for c in (c for c in CLASSES if c["module"] == m["n"]):
            folder = ROOT / "clases" / c["slug"]
            base = f"clases/{c['slug']}"
            mats = [f"[guía]({base}/README.md)"]
            if (folder / "slides.html").exists():
                mats.append(f"[slides]({base}/slides.html)")
            if (folder / f"{c['slug']}.ipynb").exists():
                mats.append(f"[notebook]({base}/{c['slug']}.ipynb)")
            if (folder / "cookbook.md").exists():
                mats.append(f"[cookbook]({base}/cookbook.md)")

            rows.append(f"| {c['id']} | {c['title']} | {PRACTICA[c['practica']]} | {c['minutes']} | {' · '.join(mats)} |")
    return "\n".join(rows)


def update_readme():
    p = ROOT / "README.md"
    s = p.read_text(encoding="utf-8")
    a, b = "<!-- clases:inicio -->", "<!-- clases:fin -->"
    if a in s and b in s:
        s = s[: s.index(a) + len(a)] + "\n" + readme_table() + "\n" + s[s.index(b):]
        p.write_text(s, encoding="utf-8")
        print("  tabla de clases en README.md")


def build(lang):
    if lang == "es":
        tpl, pre, out = PAGE_ES, "", ROOT / "index.html"
        title, subtitle, nvcourse = COURSE["title"], COURSE["subtitle"], COURSE["nvidia_course_es"]
    else:
        tpl, pre, out = PAGE_EN, "../", ROOT / "en" / "index.html"
        title, subtitle, nvcourse = COURSE_EN["title"], COURSE_EN["subtitle"], NV_EN + "index.html"
    page = tpl.format(
        title=E(title), partner=E(COURSE["partner"]), subtitle=E(subtitle),
        instructor=E(COURSE["instructor"]), build=COURSE["build"], launchable=COURSE["launchable"],
        start=f"{pre}clases/{CLASSES[0]['slug']}/index.html", faq=f"{pre}FAQ.html",
        modules=modules_html(lang), errores=errores_html(lang),
        nvrepo=COURSE["nvidia_repo"], nemoclaw=COURSE["nemoclaw_repo"], nvcourse=nvcourse,
        glosario=f"{pre}GLOSARIO.html", laboratorio=f"{pre}LABORATORIO.html",
        n_clases=len(CLASSES), horas=f"{sum(c['minutes'] for c in CLASSES) / 60:.1f}",
        estilos=estilos(pre), cabecera=cabecera(lang, pre, len(CLASSES), f"{sum(c['minutes'] for c in CLASSES) / 60:.1f}"),
        diagrama_flujo=DIAGRAMAS["flujo-peticion"](lang), diagrama_proyecto=DIAGRAMAS["proyecto-crece"](lang),
    )
    out.write_text(page, encoding="utf-8")
    print(f"  portada {out.relative_to(ROOT)}")


if __name__ == "__main__":
    update_readme()
    build("es")
    build("en")
