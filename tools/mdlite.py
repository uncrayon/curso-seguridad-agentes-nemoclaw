"""Markdown mínimo, sin dependencias, para las diapositivas y la portada.

Soporta: # / ## / ###, párrafos, listas (- y 1.) con un nivel de anidación (2 espacios),
bloques ``` de código, tablas con |, > citas, **negrita**, *cursiva*, `código`, [enlaces](url),
y estos bloques propios:

    :::cols            columnas en tarjetas; separa columnas con una línea  |||
    ...
    |||
    ...
    :::

    :::warn | :::tip | :::bad     recuadro de aviso / consejo / error
    ...
    :::

    .lead Texto        párrafo destacado en gris
"""
import html
import re

_INLINE_CODE = re.compile(r"`([^`]+)`")


def inline(s: str) -> str:
    parts = _INLINE_CODE.split(s)
    out = []
    for k, p in enumerate(parts):
        if k % 2:
            out.append("<code>" + html.escape(p) + "</code>")
            continue
        p = html.escape(p, quote=False)
        p = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', p)
        p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
        p = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", p)
        out.append(p)
    return "".join(out)


def _table(rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], [r for r in cells[1:] if not all(re.fullmatch(r":?-{2,}:?", c) for c in r)]
    h = "".join(f"<th>{inline(c)}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    return f"<table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>"


def _list(lines):
    """lines: raw lines of one list block (top-level items + 2-space nested items)."""
    ordered = bool(re.match(r"\s*\d+\.\s", lines[0]))
    tag = "ol" if ordered else "ul"
    out, cur_sub, sub_tag = [f"<{tag}>"], [], None
    item_open = False

    def flush_sub():
        nonlocal cur_sub
        if cur_sub:
            out.append(f"<{sub_tag}>" + "".join(f"<li>{inline(x)}</li>" for x in cur_sub) + f"</{sub_tag}>")
            cur_sub = []

    for ln in lines:
        m_top = re.match(r"(?:[-*]|\d+\.)\s+(.*)", ln)
        m_sub = re.match(r"\s{2,}(?:([-*])|\d+\.)\s+(.*)", ln)
        if m_sub:
            sub_tag = "ul" if m_sub.group(1) else "ol"
            cur_sub.append(m_sub.group(2))
        elif m_top:
            flush_sub()
            if item_open:
                out.append("</li>")
            out.append("<li>" + inline(m_top.group(1)))
            item_open = True
        else:  # continuation line
            out.append(" " + inline(ln.strip()))
    flush_sub()
    if item_open:
        out.append("</li>")
    out.append(f"</{tag}>")
    return "".join(out)


def render(md: str) -> str:
    lines = md.splitlines()
    out, i = [], 0
    stack = []  # open ::: blocks
    para = []

    def flush_para():
        nonlocal para
        if para:
            sep = "<br>" if stack and stack[-1] == "cols" else " "   # en tarjetas, cada línea es una línea
            out.append("<p>" + sep.join(inline(x.strip()) for x in para) + "</p>")
            para = []

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith("```"):
            flush_para()
            lang = s[3:].strip()
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                buf.append(lines[j])
                j += 1
            cls = f' class="lang-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>" + html.escape("\n".join(buf)) + "</code></pre>")
            i = j + 1
            continue
        if s.startswith(":::"):
            flush_para()
            kind = s[3:].strip()
            if kind == "":
                closing = stack.pop() if stack else None
                out.append("</div></div>" if closing == "cols" else "</div>")
            elif kind == "cols":
                stack.append("cols")
                out.append('<div class="cols"><div class="col">')
            else:
                stack.append(kind)
                out.append(f'<div class="call {html.escape(kind)}">')
            i += 1
            continue
        if s == "|||" and stack and stack[-1] == "cols":
            flush_para()
            out.append('</div><div class="col">')
            i += 1
            continue
        if not s:
            flush_para()
            i += 1
            continue
        m = re.match(r"(#{1,3})\s+(.*)", s)
        if m:
            flush_para()
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            i += 1
            continue
        if s.startswith(".lead "):
            flush_para()
            out.append(f'<p class="lead">{inline(s[6:])}</p>')
            i += 1
            continue
        if s.startswith("|"):
            flush_para()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(_table(rows))
            continue
        if s.startswith(">"):
            flush_para()
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote>" + inline(" ".join(buf)) + "</blockquote>")
            continue
        if re.match(r"(?:[-*]|\d+\.)\s+", s) and not ln.startswith("  "):
            flush_para()
            buf = []
            while i < len(lines) and lines[i].strip() and (
                re.match(r"(?:[-*]|\d+\.)\s+", lines[i].strip()) or lines[i].startswith("  ")
            ):
                buf.append(lines[i])
                i += 1
            out.append(_list(buf))
            continue
        para.append(ln)
        i += 1
    flush_para()
    while stack:
        out.append("</div></div>" if stack.pop() == "cols" else "</div>")
    return "\n".join(out)
