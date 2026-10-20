"""Ejecuta los notebooks de clases/ en modo MOCK (sin API key) y reporta cuáles fallan.

Requiere: pip install nbclient nbformat ipykernel openai python-dotenv
Uso:  python tools/check_notebooks.py                 (todos)
      python tools/check_notebooks.py clases/2.1-*/*.ipynb
      NVIDIA_API_KEY=nvapi-... python tools/check_notebooks.py   (en vivo)
"""
import glob
import os
import pathlib
import sys
import time

import nbformat
from nbclient import NotebookClient

ROOT = pathlib.Path(__file__).resolve().parent.parent
paths = [str(pathlib.Path(x).resolve()) for x in sys.argv[1:]] or sorted(glob.glob(str(ROOT / "clases" / "*" / "*.ipynb")))
if "NVIDIA_API_KEY" not in os.environ:
    os.environ["NVIDIA_API_KEY"] = ""          # fuerza modo MOCK aunque haya un .env
fallas = 0
for p in paths:
    nb = nbformat.read(p, as_version=4)
    t = time.time()
    try:
        NotebookClient(nb, timeout=300, kernel_name="python3",
                       resources={"metadata": {"path": str(pathlib.Path(p).parent)}}).execute()
        print(f"OK    {time.time() - t:5.1f}s  {pathlib.Path(p).relative_to(ROOT)}")
    except Exception as e:
        fallas += 1
        print(f"FALLA {time.time() - t:5.1f}s  {pathlib.Path(p).relative_to(ROOT)}\n      {str(e).splitlines()[-1][:300]}")
sys.exit(1 if fallas else 0)
