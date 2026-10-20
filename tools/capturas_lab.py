"""Reemplaza los marcadores de capturas `](lab:NN)` por la ruta real en assets/lab/.

Las guías se escriben con `![texto](lab:07)`; este script busca el archivo
assets/lab/07-*.{jpg,png} y escribe la ruta relativa correcta para cada .md.
Es idempotente: si ya no hay marcadores, no cambia nada.

Uso: python3 tools/capturas_lab.py
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LAB = RAIZ / "assets" / "lab"
MARCA = re.compile(r"\]\(lab:(\d{2})\)")


def archivos_lab():
    mapa = {}
    for f in sorted(LAB.glob("[0-9][0-9]-*")):
        if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            mapa.setdefault(f.name[:2], f)
    return mapa


def main():
    mapa = archivos_lab()
    faltan = set()
    cambiados = []
    for md in RAIZ.rglob("*.md"):
        if any(p in md.parts for p in (".git", "reference", "node_modules")):
            continue
        texto = md.read_text(encoding="utf-8")
        if "](lab:" not in texto:
            continue

        def ruta(m):
            n = m.group(1)
            if n not in mapa:
                faltan.add(n)
                return m.group(0)
            rel = Path(*[".."] * len(md.parent.relative_to(RAIZ).parts)) / mapa[n].relative_to(RAIZ)
            return f"]({rel.as_posix()})"

        nuevo = MARCA.sub(ruta, texto)
        if nuevo != texto:
            md.write_text(nuevo, encoding="utf-8")
            cambiados.append(md.relative_to(RAIZ))
    for c in cambiados:
        print("actualizado:", c)
    if faltan:
        print("sin captura para:", ", ".join(sorted(faltan)), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
