"""Convierte las guías Markdown del curso en páginas web con el estilo Platzi Sinapsis.

Así nadie necesita GitHub ni saber qué es un .md: cada clase tiene su página
(clases/<slug>/index.html), con «Lo esencial» arriba en tarjetas, las palabras del glosario
con su definición al pasar el mouse, botón de copiar en cada comando y navegación entre clases.

Qué convierte:
  clases/<slug>/README.md        -> clases/<slug>/index.html   (la guía de la clase)
  clases/<slug>/*.md (cookbook, guion, skills/**/SKILL.md) -> mismo nombre .html
  en/clases/<slug>/README.md     -> en/clases/<slug>/index.html
  FAQ.md, GLOSARIO.md, LABORATORIO.md, syllabus.md, FUENTES.md -> .html en la raíz
  skill-library/**/*.md y tools/guia-accesible.md -> .html

Los enlaces a otros .md se reescriben a .html (README.md -> index.html), y los notebooks
apuntan a Colab cuando COURSE["github"] está definido.

Requiere:  pip install -r tools/requirements.txt   (markdown y pymdown-extensions)
Uso:       python3 tools/build_guias.py
"""
import hashlib
import html
import pathlib
import re
import sys

import markdown

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from course import CLASSES, COURSE, by_id, module, neighbors  # noqa: E402
from course_en import CLASSES_EN, COURSE_EN, MODULES_EN  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape
VER = hashlib.md5(b"".join((ROOT / "assets" / f).read_bytes() for f in ("sinapsis.css", "guia.css"))).hexdigest()[:8]
PRACTICA = {"es": {"notebook": "Notebook", "lab": "Laboratorio en Brev", "slides": "Diapositivas", "navegador": "Navegador"},
            "en": {"notebook": "Notebook", "lab": "Lab on Brev", "slides": "Slides", "navegador": "Browser"}}
UI = {
    "es": {"home": "Inicio del curso", "glosario": "Glosario", "lab": "Tu laboratorio", "faq": "Preguntas frecuentes",
           "slides": "Ver diapositivas", "nb": "Abrir el notebook", "colab": "Abrir en Colab", "cb": "Recetario de terminal",
           "prev": "Clase anterior", "next": "Clase siguiente", "module": "Módulo", "class": "Clase", "skill": "Habilidad",
           "copy": "Copiar", "copied": "¡Copiado!", "esencial": "Lo esencial", "fondo": "Paso a paso completo",
           "fondo_sub": "Todo el detalle, para hacerlo de principio a fin. Si no programas, quédate con «Lo esencial» y vuelve aquí cuando quieras.",
           "glos": "Ver en el glosario"},
    "en": {"home": "Course home", "glosario": "Glossary (ES)", "lab": "Your lab (ES)", "faq": "FAQ (ES)",
           "slides": "View slides", "nb": "Open the notebook", "colab": "Open in Colab", "cb": "Terminal cookbook (ES)",
           "prev": "Previous class", "next": "Next class", "module": "Module", "class": "Class", "skill": "Skill",
           "copy": "Copy", "copied": "Copied!", "esencial": "The essentials", "fondo": "Full step by step",
           "fondo_sub": "All the detail, start to finish.", "glos": "See in the glossary"},
}
ICONOS_ESENCIAL = [("la idea", "auto_awesome"), ("piénsalo", "interests"), ("palabras", "menu_book"),
                   ("hazlo", "edit_note"), ("qué te llevas", "check_circle"), ("tu crédito", "paid"),
                   ("the idea", "auto_awesome"), ("think of", "interests"), ("new words", "menu_book"),
                   ("do it", "edit_note"), ("what you take", "check_circle"), ("your credit", "paid")]


# ------------------------------------------------------------------ utilidades
def slug_github(texto):
    """Como GitHub: minúsculas, sin puntuación (conserva letras con acento), espacios -> guiones."""
    t = re.sub(r"<[^>]+>", "", texto).strip().lower()
    t = re.sub(r"[^\w\- ]", "", t, flags=re.UNICODE)
    return t.replace(" ", "-")


def normaliza(t):
    t = re.sub(r"[`*]", "", t).lower().strip()
    return re.sub(r"\s*\(.*?\)\s*", " ", t).strip()


def carga_glosario():
    """{término normalizado: (slug, definición, analogía)} desde las tablas de GLOSARIO.md."""
    glos = {}
    for ln in (ROOT / "GLOSARIO.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*\*\*(.+?)\*\*(?:\s*\(([^)]*)\))?([^|]*)\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*([\d.]+)\s*\|", ln)
        if not m:
            continue
        termino = m.group(1).strip("`")
        entrada = (slug_github(termino), re.sub(r"[`*]", "", m.group(4)), re.sub(r"[`*]", "", m.group(5)))
        glos[normaliza(termino)] = entrada
        for alias in re.split(r",|/| o ", m.group(1)):
            a = normaliza(alias)
            if a and a not in glos:
                glos[a] = entrada
        if m.group(2):
            glos.setdefault(normaliza(m.group(2)), entrada)
    return glos


GLOS = carga_glosario()


def a_html(rel_md):
    """Ruta de un .md -> la página .html que la reemplaza."""
    if rel_md.endswith("README.md"):
        return rel_md[: -len("README.md")] + "index.html"
    return rel_md[:-3] + ".html"


def reescribe_enlaces(cuerpo, origen):
    """Reescribe href en el HTML ya generado: .md -> .html, glosario con definición, notebooks a Colab."""
    def cambia(m):
        attrs, href, texto = m.group(1), m.group(2), m.group(3)
        if re.match(r"[a-z]+:|#|mailto:", href):
            return m.group(0)
        ruta, _, ancla = href.partition("#")
        nuevo = href
        extra = ""
        if ruta.endswith(".md"):
            nuevo = a_html(ruta) + (f"#{ancla}" if ancla else "")
            if ruta.endswith("GLOSARIO.md"):
                g = GLOS.get(normaliza(re.sub(r"<[^>]+>", "", texto)))
                if g:
                    nuevo = a_html(ruta) + "#" + g[0]
                    extra = f' class="glos" data-def="{E(g[1])} · {E(g[2])}"'
        elif ruta.endswith(".ipynb") and COURSE.get("github"):
            destino = (origen.parent / ruta).resolve().relative_to(ROOT).as_posix()
            nuevo = f"https://colab.research.google.com/github/{COURSE['github']}/blob/main/{destino}"
            extra = ' target="_blank" rel="noopener"'
        return f'<a{attrs} href="{nuevo}"{extra}>{texto}</a>'
    return re.sub(r'<a([^>]*?) href="([^"]+)"[^>]*>(.*?)</a>', cambia, cuerpo, flags=re.S)


def md_a_html(texto):
    texto = re.sub(r"^(\s*)- \[ \] ", r"\1- ☐ ", texto, flags=re.M)
    texto = re.sub(r"^(\s*)- \[x\] ", r"\1- ☑ ", texto, flags=re.M | re.I)
    # superfences: bloques de código dentro de pasos numerados (las guías los usan en casi cada paso)
    md = markdown.Markdown(extensions=["tables", "pymdownx.superfences", "sane_lists", "toc", "md_in_html"],
                           extension_configs={"toc": {"slugify": lambda v, sep: slug_github(v)}})
    return md.convert(texto)


def esencial_html(bloque, lang):
    """La sección «Lo esencial» como tarjetas. Cada **Etiqueta:** abre una tarjeta; los párrafos y listas
    que siguen sin etiqueta (por ejemplo, los pasos de una actividad) se quedan en esa misma tarjeta."""
    grupos = []
    for par in re.split(r"\n\s*\n", bloque.strip()):
        m = re.match(r"\*\*(.+?):\*\*\s*(.*)", par.strip(), re.S)
        if m:
            cuerpo = m.group(2)
            grupos.append([m.group(1), cuerpo[:1].upper() + cuerpo[1:]])
        elif grupos:
            grupos[-1][1] += "\n\n" + par
    tarjetas = []
    for etiqueta, cuerpo in grupos:
        icono = next((ic for k, ic in ICONOS_ESENCIAL if etiqueta.lower().startswith(k)), "info")
        clase = " wide" if icono == "edit_note" else ""
        clase += " credit" if icono == "paid" else ""
        contenido = markdown.markdown(cuerpo, extensions=["sane_lists"])
        tarjetas.append(f'<article class="es-card{clase}"><header><span class="icon">{icono}</span>{E(etiqueta)}</header>{contenido}</article>')
    return f'<div class="esencial-grid">{"".join(tarjetas)}</div>'


PAGINA = """<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo_txt}</title>
<link rel="stylesheet" href="{assets}sinapsis.css?v={ver}">
<link rel="stylesheet" href="{assets}guia.css?v={ver}">
</head><body>
<header class="topbar"><div class="wrap">
  <a class="brand" href="{raiz}{home}"><img src="{assets}brand/platzi-isotype-solid.svg" alt="">{curso}</a>
  <nav>{nav}</nav>
</div></header>
<main class="wrap">
{hero}
{cuerpo}
{pie}
</main>
<footer class="foot"><div class="wrap">{partner} · {curso}</div></footer>
<script>
document.querySelectorAll("pre").forEach(function (pre) {{
  var b = document.createElement("button"); b.className = "copy"; b.type = "button"; b.textContent = "{copy}";
  b.addEventListener("click", function () {{
    navigator.clipboard.writeText(pre.innerText.replace(/{copy}$/, "").trim()).then(function () {{
      b.textContent = "{copied}"; setTimeout(function () {{ b.textContent = "{copy}"; }}, 1500); }});
  }});
  pre.appendChild(b);
}});
</script>
</body></html>
"""


def nav(lang, raiz):
    u = UI[lang]
    base = raiz
    return (f'<a href="{base}GLOSARIO.html"><span class="icon">menu_book</span>{u["glosario"]}</a>'
            f'<a href="{base}LABORATORIO.html"><span class="icon">paid</span>{u["lab"]}</a>'
            f'<a href="{base}FAQ.html"><span class="icon">quiz</span>{u["faq"]}</a>')


def pagina_clase(c, lang):
    u = UI[lang]
    carpeta = (ROOT / "clases" / c["slug"]) if lang == "es" else (ROOT / "en" / "clases" / c["slug"])
    src = carpeta / "README.md"
    texto = src.read_text(encoding="utf-8")
    if lang == "es":
        titulo, skill, mod = c["title"], c.get("skill"), module(c["module"])["title"]
    else:
        titulo, _, skill = CLASSES_EN[c["id"]]
        mod = MODULES_EN[c["module"]][0]
    # quita el H1 y la tabla de datos del encabezado (van al hero)
    texto = re.sub(r"\A# .*\n", "", texto)
    esencial = ""
    m = re.search(r"^## (Lo esencial[^\n]*|The essentials[^\n]*)\n(.*?)(?=^## )", texto, re.S | re.M)
    if m:
        esencial = (f'<section class="esencial" id="lo-esencial"><h2><span class="icon">auto_awesome</span>{u["esencial"]}</h2>'
                    + reescribe_enlaces(esencial_html(m.group(2), lang), src) + "</section>")
        texto = texto[: m.start()] + texto[m.end():]
    cuerpo = reescribe_enlaces(md_a_html(texto), src)
    raiz = "../../" if lang == "es" else "../../../"
    assets = raiz + "assets/"
    acciones = []
    if (carpeta / "slides.html").exists():
        acciones.append(f'<a class="btn primary" href="slides.html"><span class="icon">pages</span>{u["slides"]}</a>')
    es_carpeta = ROOT / "clases" / c["slug"]
    nb = es_carpeta / f"{c['slug']}.ipynb"
    if nb.exists():
        if COURSE.get("github"):
            href = f"https://colab.research.google.com/github/{COURSE['github']}/blob/main/clases/{c['slug']}/{nb.name}"
            acciones.append(f'<a class="btn" href="{href}" target="_blank" rel="noopener"><span class="icon">play_arrow</span>{u["colab"]}</a>')
        else:
            rel = nb.name if lang == "es" else f"../../../clases/{c['slug']}/{nb.name}"
            acciones.append(f'<a class="btn" href="{rel}"><span class="icon">code</span>{u["nb"]}</a>')
    if (es_carpeta / "cookbook.md").exists():
        rel = "cookbook.html" if lang == "es" else f"../../../clases/{c['slug']}/cookbook.html"
        acciones.append(f'<a class="btn" href="{rel}"><span class="icon">terminal</span>{u["cb"]}</a>')
    chips = [f'<span class="chip"><span class="icon">schedule</span>≈{c["minutes"]} min</span>',
             f'<span class="chip"><span class="icon">{"computer" if c["practica"] == "lab" else "play_arrow"}</span>{PRACTICA[lang][c["practica"]]}</span>']
    if skill:
        chips.append(f'<span class="chip primary"><span class="icon">bolt</span>{u["skill"]}: {E(skill)}</span>')
    hero = (f'<section class="hero"><span class="tag">{u["module"]} {c["module"]} · {E(mod)}</span>'
            f'<h1><span class="num">{c["id"]}</span>{E(titulo)}</h1><p class="chips">{"".join(chips)}</p>'
            f'<p class="acciones">{"".join(acciones)}</p></section>')
    fondo = (f'<section class="fondo"><h2 class="fondo-h"><span class="icon">list</span>{u["fondo"]}</h2>'
             f'<p class="fondo-sub">{u["fondo_sub"]}</p><div class="md">{cuerpo}</div></section>')
    prev, nxt = neighbors(c["id"])
    def enlace(x, etiqueta, clase):
        if not x:
            return "<span></span>"
        t = x["title"] if lang == "es" else CLASSES_EN[x["id"]][0]
        return f'<a class="pn {clase}" href="../{x["slug"]}/index.html"><small>{etiqueta}</small>{x["id"]} · {E(t)}</a>'
    pie = f'<nav class="prevnext">{enlace(prev, u["prev"], "prev")}{enlace(nxt, u["next"], "next")}</nav>'
    curso = COURSE["title"] if lang == "es" else COURSE_EN["title"]
    out = PAGINA.format(lang=lang, titulo_txt=E(f'{c["id"]} {titulo} · {curso}'), assets=assets, ver=VER, raiz=raiz,
                        home="index.html" if lang == "es" else "en/index.html", curso=E(curso), nav=nav(lang, raiz),
                        hero=hero, cuerpo=esencial + fondo, pie=pie, partner=E(COURSE["partner"]),
                        copy=u["copy"], copied=u["copied"])
    (carpeta / "index.html").write_text(out, encoding="utf-8")
    return carpeta / "index.html"


def pagina_doc(src, lang="es"):
    """Cualquier otro .md: glosario, laboratorio, FAQ, recetarios, guiones, skills."""
    u = UI[lang]
    texto = src.read_text(encoding="utf-8")
    m = re.match(r"\A# (.+)\n", texto)
    titulo = m.group(1).strip() if m else src.stem
    texto = texto[m.end():] if m else texto
    cuerpo = reescribe_enlaces(md_a_html(texto), src)
    if src.name == "GLOSARIO.md":                      # cada fila con su ancla, para enlazar términos
        cuerpo = re.sub(r"<tr>\s*<td><strong>(.+?)</strong>",
                        lambda mm: f'<tr id="{slug_github(mm.group(1))}"><td><strong>{mm.group(1)}</strong>', cuerpo)
    prof = len(src.parent.relative_to(ROOT).parts)
    raiz = "../" * prof
    curso = COURSE["title"]
    hero = f'<section class="hero doc"><h1>{E(re.sub(r"[`*]", "", titulo))}</h1></section>'
    out = PAGINA.format(lang=lang, titulo_txt=E(f"{titulo} · {curso}"), assets=raiz + "assets/", ver=VER, raiz=raiz,
                        home="index.html", curso=E(curso), nav=nav("es", raiz), hero=hero,
                        cuerpo=f'<div class="md">{cuerpo}</div>', pie="", partner=E(COURSE["partner"]),
                        copy=u["copy"], copied=u["copied"])
    dest = src.with_name("index.html") if src.name == "README.md" else src.with_suffix(".html")
    dest.write_text(out, encoding="utf-8")
    return dest


def build():
    hechas = []
    for c in CLASSES:
        hechas.append(pagina_clase(c, "es"))
        if (ROOT / "en" / "clases" / c["slug"] / "README.md").exists():
            hechas.append(pagina_clase(c, "en"))
        for md in sorted((ROOT / "clases" / c["slug"]).rglob("*.md")):
            if md.name not in ("README.md", "slides.md"):
                hechas.append(pagina_doc(md))
    for nombre in ("GLOSARIO.md", "LABORATORIO.md", "FAQ.md", "syllabus.md", "FUENTES.md", "tools/guia-accesible.md"):
        hechas.append(pagina_doc(ROOT / nombre))
    for md in sorted((ROOT / "skill-library").rglob("*.md")):
        hechas.append(pagina_doc(md))
    print(f"  guías: {len(hechas)} páginas")


if __name__ == "__main__":
    build()
