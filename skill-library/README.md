# skill-library · Biblioteca de skills del proyecto "Soporte NemoClaw"

Cuatro skills en español para el agente del proyecto del curso. Las construimos y evaluamos en la clase **6.2** ([guía](../clases/6.2-biblioteca-de-skills/README.md) · [notebook](../clases/6.2-biblioteca-de-skills/6.2-biblioteca-de-skills.ipynb)).

```
skill-library/
  README.md
  soporte-nemoclaw/SKILL.md         # responde dudas con la FAQ del curso y cita la fuente
  diagnostico-api/SKILL.md          # explica errores 401/403/404/410/429/5xx de la API
  lector-seguro-archivos/SKILL.md   # lee solo dentro de datos/ y rechaza lo demás
  resumen-diario/SKILL.md           # resumen del día para una tarea programada (cron)
```

| Skill | Cuándo se activa | Herramienta que usa | Clase de origen |
|---|---|---|---|
| `soporte-nemoclaw` | Dudas de instalación, Brev, conexión, curso | `buscar_faq` (en OpenClaw: `ls`/`grep` sobre `faq/`) | 4.3 (evoluciona en 6.2) |
| `diagnostico-api` | El usuario pega un error HTTP de la API | `diagnosticar_http` | 1.3 |
| `lector-seguro-archivos` | "Abre / lee / muestra el archivo…" | `leer_archivo` (limitada a `datos/`) | 5.3 |
| `resumen-diario` | "Resumen del día" o una tarea cron | `leer_archivo` | 4.3 |

> **`soporte-nemoclaw` viene de la clase 4.3** ([versión original](../clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/SKILL.md)). Esta versión mantiene la ruta de la FAQ, el formato de respuesta, las reglas y el "Modo reporte" que usa el cron de la 4.3. Solo cambia la description: ya no menciona errores HTTP, porque ahora los atiende `diagnostico-api`. Para cambiar la versión de la 4.3 por esta, quita la vieja con `skill remove soporte-nemoclaw` e instala esta (ver abajo).

## Anatomía de una skill
Una carpeta por skill y un `SKILL.md` adentro. El archivo empieza con un **frontmatter** YAML:

```yaml
---
name: diagnostico-api          # único; igual al nombre de la carpeta
description: Diagnostica ... Úsala cuando ...   # QUÉ hace y CUÁNDO usarla
---
```

Después viene el cuerpo: **propósito**, **cuándo NO usarla**, **pasos** numerados (el runbook) y **límites**. Una skill puede traer archivos extra junto a `SKILL.md` (plantillas, scripts, referencias).

Reglas que conviene cumplir siempre:
- `name` solo con letras, números, puntos, guiones y guiones bajos. Es la regla que valida `nemoclaw <sandbox> skill install`.
- `description` en una sola línea y sin `: ` (dos puntos seguidos de espacio). Si necesitas dos puntos, pon la descripción entre comillas. Si no, el YAML se rompe.
- La descripción dice **cuándo** usar la skill con las palabras que usaría un estudiante. No es un título.

## Cómo la descubre un agente (progressive disclosure)
1. Al arrancar, el harness lee **solo el frontmatter** de cada `SKILL.md`.
2. Pone `nombre: descripción` de cada skill en el prompt de sistema. Ese es el "menú".
3. Si el pedido coincide, el modelo pide cargar esa skill y el harness le entrega el `SKILL.md` completo:
   - **Selección explícita:** el usuario nombra la skill (`/diagnostico-api ...` o "usa la skill diagnostico-api").
   - **Selección automática:** el modelo la elige solo, comparando el pedido con las descripciones.
4. El modelo sigue el runbook con sus herramientas normales.

Por eso la descripción es la línea más importante: si no dice cuándo usar la skill, la selección automática falla. En el notebook de la 6.2 la medimos con un set de pedidos (tasa de acierto).

## Llevarla al laboratorio (Brev + NemoClaw)
Todo en el navegador: en el tablero de NemoClaw de tu instancia, presiona **VM TERMINAL** y haz clic dentro del área negra. Esta biblioteca viene en la copia del curso que clonaste en la clase 4.3 (`~/curso/skill-library/`). Si no la tienes:

```bash
git clone --depth 1 https://github.com/uncrayon/curso-seguridad-agentes-nemoclaw ~/curso
```

Después, en la misma terminal:

```bash
openshell sandbox list                                   # nombre del sandbox (p. ej. my-assistant)
nemoclaw my-assistant skill remove soporte-nemoclaw      # solo si ya instalaste la versión de la 4.3
nemoclaw my-assistant skill install ~/curso/skill-library/soporte-nemoclaw/
nemoclaw my-assistant skill install ~/curso/skill-library/diagnostico-api/
nemoclaw my-assistant skill install ~/curso/skill-library/lector-seguro-archivos/
nemoclaw my-assistant skill install ~/curso/skill-library/resumen-diario/
nemoclaw my-assistant skill list
```

Cada instalación responde `✓ Validated SKILL.md` e `Installed <nombre> from path -> /sandbox/.openclaw/workspace/skills/<nombre>`. Ignora la línea `ExperimentalWarning: SQLite…`. Es la parte opcional de laboratorio de la clase 6.2: al terminarla, guarda lo que quieras y borra la instancia (**Delete**) en la consola de Brev.

- Con OpenClaw, `skill install` llama a `openclaw skills install` y la skill queda en `/sandbox/.openclaw/workspace/skills/<nombre>`.
- Con Hermes queda en `/sandbox/.hermes/skills/<nombre>`; con Deep Agents, en `/sandbox/.deepagents/agent/skills/<nombre>`.
- Abre una **sesión nueva** del agente para que la vea. NemoClaw no garantiza que la skill quede activa: la autoridad es `skill list` y una sesión nueva.

Para quitar una: `nemoclaw my-assistant skill remove resumen-diario`.

## Seguridad
Una skill son **instrucciones persistentes**: sobreviven entre sesiones. Una skill envenenada es una directiva envenenada que no se va.
- Revisa las skills como revisas código (pull request, diff, dueño).
- Pon los límites en las herramientas y en el sandbox, no solo en el texto de la skill.
- Decide quién puede escribir en la carpeta `skills/` del agente (Módulos 4 y 5).

---
Las skills de ejemplo adaptan la idea de las skills de práctica del curso de NVIDIA DLI *Seguridad de agentes con OpenShell y NemoClaw*, lección 03c (Apache-2.0), y el formato de [Agent Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview).
