# Corpus de preguntas frecuentes (`datos/faq/`)

Esta carpeta es la base de conocimiento del proyecto del curso, el agente **Soporte NemoClaw**. La usan:

- la tool `buscar_faq` (clase 2.3),
- el router de triage (clase 3.1),
- el RAG con citas (clase 3.2),
- la skill `soporte-nemoclaw` en OpenClaw (clases 4.x y 6.2).

Es una versión condensada, en tono de respuesta directa, de la [FAQ completa del curso](../../FAQ.md), que tiene además las causas, los comandos en bloques y las fuentes.

## Archivos

| Archivo | Tema | Categoría del router (3.1) |
|---|---|---|
| `api-key.md` | Cuenta y API key de NVIDIA Build | `api_key` |
| `errores-api.md` | Errores HTTP del modelo, timeouts, `finish_reason` | `api_key` |
| `notebooks.md` | Notebooks, Colab y Python | `otro` |
| `brev.md` | Brev: costos, cupón, plan de crédito, stop/delete | `brev` |
| `conexion-laboratorio.md` | Cómo entrar al laboratorio: botón NemoClaw, tablero y terminales | `brev` |
| `openclaw.md` | Gateway, dashboard, pairing, workspace, sesiones | `otro` |
| `openshell-politicas.md` | Sandbox, red bloqueada, presets, Landlock | `seguridad` |
| `instalacion-local.md` | NemoClaw en tu máquina: requisitos, Docker, puertos | `instalacion` |
| `seguridad.md` | Keys, cookies, tokens y qué hacer si se filtran | `seguridad` |

## Formato (estricto, para poder trocearlo con código)

```markdown
# Tema del archivo

## P: <pregunta como la escribiría un estudiante>
<respuesta autocontenida de 2 a 6 líneas, con los comandos clave en `código`>

## P: <siguiente pregunta>
...
```

Reglas:

- Un solo `#` por archivo: el tema.
- Cada entrada empieza con `## P: ` y termina donde empieza la siguiente.
- La respuesta se entiende sola, sin leer otras entradas: un chunk = una entrada.
- Una oración por línea. Sin bloques de código, tablas ni enlaces relativos.

Ejemplo para trocear en Python:

```python
import pathlib, re

def cargar_faq(carpeta="datos/faq"):
    entradas = []
    for archivo in sorted(pathlib.Path(carpeta).glob("*.md")):
        if archivo.name == "README.md":
            continue
        texto = archivo.read_text(encoding="utf-8")
        tema = texto.splitlines()[0].lstrip("# ").strip()
        for bloque in re.split(r"\n(?=## P: )", texto)[1:]:
            pregunta, _, respuesta = bloque.partition("\n")
            entradas.append({"archivo": archivo.name, "tema": tema,
                             "pregunta": pregunta.removeprefix("## P: ").strip(),
                             "respuesta": respuesta.strip()})
    return entradas
```

## Origen y licencia

- Contenido **propio del curso** "Seguridad de agentes con OpenShell y NemoClaw" (Platzi × NVIDIA DLI), escrito en español por el equipo del curso. No copia texto de terceros: resume y cita, en `FAQ.md`, la documentación pública de NVIDIA NemoClaw (Apache-2.0), el curso NVDLI/NemoClawDLI (Apache-2.0), la documentación de NVIDIA Brev y issues públicos de GitHub.
- Se distribuye con la misma licencia que el resto de este repositorio. `[VERIFICAR licencia final con Platzi]`
- Revisado contra NemoClaw v0.0.134 y OpenShell 0.0.116 (14 de octubre de 2026), y probado en el laboratorio de Brev con NemoClaw v0.0.135 (20 de octubre de 2026). NemoClaw cambia cada pocos días: actualiza el corpus cuando cambie un comando.
