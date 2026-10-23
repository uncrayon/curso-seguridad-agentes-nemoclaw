"""Construye clases/<slug>/slides.html a partir de clases/<slug>/slides.md.

Cada presentación queda así:
  1. Portada (generada desde tools/course.py)
  2. "La clase pasada aprendimos"  (generada: los aprendizajes de la clase anterior)
  3. ... tus diapositivas de slides.md (separadas por una línea con ---) ...
  4. "En la próxima clase aprenderemos" (generada: la promesa de la clase siguiente)

Dentro de una diapositiva, todo lo que va después de una línea "Notas:" son notas del
instructor (se ven con la tecla N). Sintaxis disponible: ver tools/mdlite.py.
Diagramas animados: una línea ":::diagrama <nombre>" (ver tools/diagramas.py).

Uso:  python3 tools/build_slides.py            (todas, español e inglés)
      python3 tools/build_slides.py 2.1 2.2    (solo esas)

Inglés: lee en/clases/<slug>/slides.md (si existe) y escribe en/clases/<slug>/slides.html,
con los textos de tools/course_en.py. En inglés, la línea de notas es "Notes:".
"""
import html
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from course import CLASSES, COURSE, by_id, module, neighbors  # noqa: E402
from mdlite import inline, render  # noqa: E402
from course_en import CLASSES_EN, COURSE_EN, LEARNED_EN, MODULES_EN  # noqa: E402
from diagramas import registro  # noqa: E402

DIAGRAMAS = registro()

# Textos de las diapositivas generadas, por idioma
T = {
    "es": {"lang": "es", "guia": "Guía de la clase", "module": "Módulo", "class": "Clase", "skill": "Habilidad", "help": "← → navegar · N notas · F pantalla completa",
           "prev": "La clase pasada aprendimos", "next": "En la próxima clase aprenderemos",
           "first_h": "Antes de empezar", "first": ["No necesitas saber programar: cada clase empieza con «Lo esencial», sin tecnicismos",
                                                   "Una cuenta gratuita de NVIDIA Build (te mostramos cómo crearla)",
                                                   "Para el laboratorio, una cuenta de Brev y tu cupón de 1 USD",
                                                   "Todo el material está en la página de cada clase: el enlace está debajo del video"],
           "last_h": "¿Y ahora qué?", "last": ["Guarda tu proyecto: tu SOUL.md, tus skills y tus notas",
                                               "Borra tu instancia de Brev para que deje de cobrar el disco",
                                               "Sigue con la ruta de IA agéntica de NVIDIA y los cursos de Platzi",
                                               "Comparte tu agente con la comunidad: cuéntanos qué construiste"]},
    "en": {"lang": "en", "guia": "Class guide", "module": "Module", "class": "Class", "skill": "Skill", "help": "← → navigate · N notes · F full screen",
           "prev": "Last class we learned", "next": "Next class we'll learn",
           "first_h": "Before we start", "first": ["You don't need to code: every class starts with «The essentials», no jargon",
                                                   "A free NVIDIA Build account (we show you how to create it)",
                                                   "For the lab, a Brev account and your 1 USD coupon",
                                                   "All the material is on each class page: the link is under the video"],
           "last_h": "What now?", "last": ["Save your project: your SOUL.md, your skills and your notes",
                                           "Delete your Brev instance so the disk stops billing",
                                           "Continue with NVIDIA's agentic AI learning path and Platzi's courses",
                                           "Share your agent with the community: tell us what you built"]},
}


def L(c, lang):
    """Título, promesa y aprendizajes de una clase en el idioma pedido."""
    if lang == "es":
        return {"title": c["title"], "promesa": c["promesa"], "aprendimos": c["aprendimos"], "skill": c.get("skill"),
                "module": module(c["module"])["title"]}
    title, promesa, skill = CLASSES_EN[c["id"]]
    return {"title": title, "promesa": promesa, "aprendimos": LEARNED_EN[c["id"]], "skill": skill,
            "module": MODULES_EN[c["module"]][0]}

OPCIONAL = {"es": "Material complementario · sin video", "en": "Supplementary material · no video"}
ROOT = pathlib.Path(__file__).resolve().parent.parent
# Versión de los assets: cambia cuando cambian el CSS o el JS, para que el navegador no use una copia vieja
import hashlib  # noqa: E402
VER = hashlib.md5(b"".join(p.read_bytes() for p in sorted((ROOT / "assets").glob("*.*s")) if p.suffix in (".css", ".js"))).hexdigest()[:8]

PAGE = """<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title_txt}</title>
<link rel="preload" href="{assets}fonts/material-symbols-rounded-subset.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{assets}sinapsis.css?v={ver}">
<link rel="stylesheet" href="{assets}diagramas.css?v={ver}">
<link rel="stylesheet" href="{assets}slides.css?v={ver}">
{modulos_css}
</head><body>
<span class="help">{help}</span>
{slides}
<div class="foot"><span><img src="{assets}brand/platzi-isotype-solid.svg" alt=""></span><span class="foot-r"><a class="guia" href="index.html">{guia}</a><span id="counter"></span></span></div>
<div class="bar"></div>
<script src="{assets}slides.js?v={ver}"></script>
</body></html>
"""


SHAPES = ["forma-4", "forma-1", "forma-8", "forma-3", "forma-7"]


def deco(c, n, assets):
    """n formas de marca Sinapsis detrás del contenido; cambian según la clase."""
    k = CLASSES.index(c)
    imgs = "".join(f'<img src="{assets}brand/{SHAPES[(k + j) % len(SHAPES)]}.svg" alt="">' for j in range(n))
    return f'<div class="deco" aria-hidden="true">{imgs}</div>'


def li(items):
    return "<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>"


def opcional(lang):
    return f'<span class="chip opt"><span class="icon">menu_book</span>{OPCIONAL[lang]}</span>'


def anterior(c):
    """La clase anterior para el repaso. Una clase obligatoria repasa la última obligatoria, no una opcional."""
    prev, _ = neighbors(c["id"])
    while prev is not None and prev.get("opcional") and not c.get("opcional"):
        prev, _ = neighbors(prev["id"])
    return prev


def portada(c, lang="es", assets=""):
    t, l = T[lang], L(c, lang)
    chips = f'<span class="chip"><span class="icon">person</span>{html.escape(COURSE["instructor"])}</span>'
    if c.get("opcional"):
        chips = opcional(lang) + chips
    if l["skill"]:
        chips += f'<span class="chip primary"><span class="icon">bolt</span>{t["skill"]}: {html.escape(l["skill"])}</span>'
    return (f'<section class="slide portada">{deco(c, 3, assets)}'
            f'<img class="logo" src="{assets}brand/platzi-logo-new.svg" alt="Platzi">'
            f"<h1>{html.escape(l['title'])}</h1>"
            f'<p class="lead">{html.escape(l["module"])}</p>'
            f'<p class="meta">{chips}</p></section>')


def repaso(c, lang="es", assets=""):
    t = T[lang]
    prev = anterior(c)
    if prev is None:
        body = f"<h2>{t['first_h']}</h2>" + li(t["first"])
    else:
        lp = L(prev, lang)
        body = (f"<h2>{t['prev']}</h2>"
                f'<p class="lead">{html.escape(lp["title"])}</p>' + li(lp["aprendimos"]))
    return f'<section class="slide repaso">{deco(c, 2, assets)}{body}</section>'


def siguiente(c, lang="es", assets=""):
    t = T[lang]
    _, nxt = neighbors(c["id"])
    if nxt is None:
        body = f"<h2>{t['last_h']}</h2>" + li(t["last"])
    else:
        ln = L(nxt, lang)
        body = (f"<h2>{t['next']}</h2>"
                f'<p class="prox">{html.escape(ln["title"])}{opcional(lang) if nxt.get("opcional") else ""}</p>' + li(ln["promesa"]))
    return f'<section class="slide siguiente">{deco(c, 2, assets)}{body}</section>'


def authored(c, md_text, lang="es"):
    out = []
    chunks, cur, in_code = [], [], False
    for ln in md_text.splitlines():          # separa por '---', pero no dentro de bloques ```
        if ln.strip().startswith("```"):
            in_code = not in_code
        if not in_code and re.fullmatch(r"---\s*", ln):
            chunks.append("\n".join(cur))
            cur = []
        else:
            cur.append(ln)
    chunks.append("\n".join(cur))
    for ch in chunks:
        if not ch.strip():
            continue
        parts = re.split(r"^(?:Notas|Notes):\s*$", ch, maxsplit=1, flags=re.M)
        diagramas = []

        def _marca(m):                       # ":::diagrama nombre" -> marcador que mdlite deja en un <p>
            diagramas.append(DIAGRAMAS[m.group(1)](lang))
            return f"@@DIAGRAMA{len(diagramas) - 1}@@"
        cuerpo = re.sub(r"^:::diagrama\s+(\S+)\s*$", _marca, parts[0], flags=re.M)
        body = render(cuerpo)
        for n, d in enumerate(diagramas):
            body = body.replace(f"<p>@@DIAGRAMA{n}@@</p>", d)
        notes = f'<aside class="notes">{render(parts[1])}</aside>' if len(parts) > 1 else ""
        out.append(f'<section class="slide">{body}{notes}</section>')
    return out


def build(c, lang="es"):
    folder = ROOT / "clases" / c["slug"] if lang == "es" else ROOT / "en" / "clases" / c["slug"]
    src = folder / "slides.md"
    if not src.exists():
        print(f"  (sin slides.md) {lang} {c['id']}")
        return False
    assets = "../../assets/" if lang == "es" else "../../../assets/"
    slides = [portada(c, lang, assets), repaso(c, lang, assets), *authored(c, src.read_text(encoding="utf-8"), lang),
              siguiente(c, lang, assets)]
    title = COURSE["title"] if lang == "es" else COURSE_EN["title"]
    page = PAGE.format(
        lang=lang, help=T[lang]["help"], guia=T[lang]["guia"], assets=assets, ver=VER,
        modulos_css="".join(f'<link rel="stylesheet" href="{assets}diagramas-m{m}.css?v={VER}">\n' for m in range(1, 7)),
        title_txt=html.escape(f"{L(c, lang)['title']} · {title}"),
        slides="\n".join(slides),
    )
    (folder / "slides.html").write_text(page, encoding="utf-8")
    print(f"  slides {lang} {c['id']}: {len(slides)}")
    return True


if __name__ == "__main__":
    ids = sys.argv[1:] or [c["id"] for c in CLASSES]
    for cid in ids:
        build(by_id(cid), "es")
        build(by_id(cid), "en")
