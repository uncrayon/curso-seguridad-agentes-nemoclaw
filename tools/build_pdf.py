"""Exporta en/index.html a PDF (Letter, con colores y estilos de impresión de assets/home.css).

Requiere Google Chrome instalado. Uso:  python3 tools/build_pdf.py
Salida: en/NemoClaw-Course-Overview.pdf
"""
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CANDIDATES = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              shutil.which("google-chrome") or "", shutil.which("chromium") or ""]
chrome = next((c for c in CANDIDATES if c and pathlib.Path(c).exists()), None)
if not chrome:
    sys.exit("No encontré Chrome/Chromium.")
src, out = ROOT / "en" / "index.html", ROOT / "en" / "NemoClaw-Course-Overview.pdf"
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={out}", src.as_uri()], check=True, capture_output=True)
print("  pdf", out.relative_to(ROOT))
