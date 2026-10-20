"""Reconstruye todo lo generado: notebooks, diapositivas y portada.

Uso:  python3 tools/build_all.py   (requiere: pip install -r tools/requirements.txt)
Después, para probar los notebooks sin key:  python tools/check_notebooks.py
"""
import pathlib
import runpy
import sys

TOOLS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(TOOLS / "notebooks"))

print("Notebooks")
for gen in sorted((TOOLS / "notebooks").glob("m*.py")):
    runpy.run_path(str(gen), run_name="__main__")
print("Diapositivas")
runpy.run_path(str(TOOLS / "build_slides.py"), run_name="__main__")
print("Guías (páginas web)")
runpy.run_path(str(TOOLS / "build_guias.py"), run_name="__main__")
print("Portada")
runpy.run_path(str(TOOLS / "build_home.py"), run_name="__main__")
