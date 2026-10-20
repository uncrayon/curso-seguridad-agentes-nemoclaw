# Notebooks, Colab y Python

## P: El notebook dice "Modo: MOCK" aunque configuré mi key, ¿qué pasó?
La celda de configuración no encontró `NVIDIA_API_KEY`.
En Colab, el secreto debe llamarse exactamente `NVIDIA_API_KEY` y tener activado el acceso del notebook.
En tu máquina, el archivo `.env` debe estar en la raíz del repo.
Después de corregirlo, vuelve a ejecutar las dos primeras celdas (configuración y cliente).

## P: Me sale ModuleNotFoundError: No module named 'openai', ¿cómo lo arreglo?
Faltan dependencias en tu entorno local; en Colab la primera celda las instala sola.
En tu máquina crea un entorno con `python3 -m venv .venv`, actívalo con `source .venv/bin/activate` e instala con `pip install -r requirements.txt`.
Luego reinicia el kernel y elige ese intérprete.

## P: Mi agente se quedó en un loop y gastó muchas llamadas, ¿cómo lo evito?
Detén la celda con el botón de interrumpir.
Un loop de agente sin salida sigue llamando al modelo mientras el modelo pida tools.
Agrega siempre un máximo de pasos, por ejemplo `for paso in range(MAX_PASOS):`, y sal cuando `finish_reason` sea `"stop"`.
