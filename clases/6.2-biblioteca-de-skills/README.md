# 6.2 · Construye tu biblioteca de skills

Escribe skills reutilizables, mide si tu agente las encuentra solo y llévalas a tu sandbox de NemoClaw.

| | |
|---|---|
| **Duración del video** | ≈9 min |
| **Práctica** | Notebook · [6.2-biblioteca-de-skills.ipynb](6.2-biblioteca-de-skills.ipynb) (corre sin key, en modo MOCK) · parte final opcional en el laboratorio de Brev (VM TERMINAL) |
| **Habilidad** | Crear skills de agente reutilizables |
| **Material** | [Diapositivas](slides.html) · [Biblioteca del proyecto](../../skill-library/README.md) · [FAQ del curso](../../FAQ.md) |

> **El Módulo 6 es opcional**, y la parte final de esta clase en el laboratorio también. Si la haces, hazla en la misma sentada, después de la 6.1 (o de la 5.3, si te saltaste la 6.1) y antes de borrar la instancia (≈15 min, ≈USD 0.06). Si ya la borraste al terminar la 5.3, sáltala: el notebook no necesita el laboratorio.

## Lo esencial (sin tecnicismos)

**La idea:** Una skill es un archivo de texto con instrucciones paso a paso para una tarea, escrito en español normal. El agente ve solo una lista con el nombre y la descripción de cada skill, y abre la completa cuando tu pedido coincide. Por eso la descripción es la línea más importante: decide si el agente encuentra la skill solo.

**Piénsalo como:** una tarjeta de receta ([skill](../../GLOSARIO.md)).

**Palabras nuevas:** frontmatter (la etiqueta de la tarjeta: nombre y descripción), *progressive disclosure* (el menú primero: el agente ve los nombres de los platillos y abre la receta solo cuando hace falta), selección explícita o automática (pedir el platillo por su nombre, o describir lo que quieres y dejar que el mesero elija).

**Hazlo sin programar (≈10 min):** Escribe una skill para una tarea real de tu trabajo, en español normal y con esta forma: un nombre corto en minúsculas y con guiones (por ejemplo, `responder-cotizaciones`); una descripción de una o dos frases que diga qué hace y "úsala cuando…", con las palabras que usaría quien la pide; de 3 a 6 pasos numerados; y una sección de límites ("nunca…"). Después escribe cinco pedidos que deberían activarla y dos que no, y revisa si tu descripción los distingue. Si la descripción lleva dos puntos, ponla entre comillas. Es configuración real: el mismo texto se instala en tu agente.

**Qué te llevas:** Puedes convertir una tarea repetitiva de tu trabajo en instrucciones que un agente sabe encontrar y seguir, y juzgar si una descripción está bien escrita.

**Tu crédito:** el notebook no usa crédito de Brev. La parte final en el laboratorio es opcional y usa ≈15 min de tu sesión única, justo después de la práctica de la 6.1, o de la 5.3 si te saltaste la 6.1 (ver [LABORATORIO.md](../../LABORATORIO.md)). Al terminarla, guarda lo que quieras y **Delete** tu instancia.

## Lo que vas a lograr
- Escribir un `SKILL.md` correcto: frontmatter (`name`, `description`) y un runbook que un agente puede seguir.
- Construir un mini harness que descubre skills, arma el menú (*progressive disclosure*) y las ejecuta con selección **explícita** o **automática**.
- Medir la **tasa de acierto** de tus descriptions con un set de pedidos y llevar la biblioteca `skill-library/` a tu laboratorio.

## Antes de empezar
- Python 3.10+ o Google Colab. La key `nvapi-` es opcional: sin key, el notebook usa un modelo simulado.
- Haber hecho la clase [2.3](../2.3-funciones-a-herramientas/README.md) (loop con herramientas) y la [4.3](../4.3-agentes-siempre-activos/README.md) (instalaste tu primera skill en OpenClaw).
- Para la parte de laboratorio: tu instancia de Brev en **Running**, el tablero de NemoClaw abierto (botón verde **NemoClaw**) y el curso clonado en `~/curso` (clase 4.3).

## La idea en un minuto
Cada sesión, tu agente empieza de cero. Una **skill** es la forma de decir algo una vez y conservarlo: una carpeta con un `SKILL.md`.

```
skill-library/diagnostico-api/SKILL.md
---
name: diagnostico-api
description: Diagnostica errores ... 401, 403, 404, 410, 429 o 5xx ... Úsala cuando el usuario pegue un error de la API ...
---
# diagnostico-api
## Pasos
1. Extrae el código HTTP del mensaje.
2. Herramienta: `diagnosticar_http` con `{"codigo": "<codigo>"}`.
3. Responde: qué pasó, causa probable, qué hacer.
```

- **Progressive disclosure:** el agente ve solo `nombre: descripción` de cada skill (el menú). El cuerpo se carga cuando lo necesita.
- **Selección explícita:** tú nombras la skill (`/diagnostico-api ...` o "lee la skill X y síguela").
- **Selección automática:** el modelo la elige comparando tu pedido con las descriptions. **Por eso la description es la línea más importante que escribes.**

La idea viene de *Voyager* (2023): un agente que guardaba lo que le funcionaba como habilidades reutilizables en una biblioteca que crecía.

## Paso a paso

1. **Abre el notebook.** En Colab o local:
   ```bash
   pip install openai python-dotenv pyyaml
   jupyter notebook clases/6.2-biblioteca-de-skills/6.2-biblioteca-de-skills.ipynb
   ```
   Ejecuta las celdas de configuración. Deberías ver: `Modo: MOCK (...)` o `Modo: EN VIVO · nvidia/nemotron-3.5-lightning-30b-a3b`.

2. **Lee la anatomía (sección 1).** La celda imprime `diagnostico-api/SKILL.md` completo. Identifica: frontmatter, propósito, pasos, límites.

3. **Descubre las skills (sección 2).** El harness valida cada `SKILL.md` con un parser YAML real. Deberías ver 4 ✅.

4. **Compara el menú con el libro completo (sección 3).** Deberías ver algo como `Prompt con menú: ~1400 caracteres` contra `~7100` de todas las skills. Con 50 skills, esa diferencia decide si el prompt cabe.

5. **Corre el harness (sección 6).**
   - Automática: *"Me sale error 401 cuando llamo al modelo"* → `cargar_skill(diagnostico-api)` → `diagnosticar_http(401)`.
   - Explícita: `/lector-seguro-archivos muéstrame notas.txt` → el harness inyecta la skill y no hay `cargar_skill`.

6. **Evalúa tus descriptions (sección 7).** 15 pedidos con la skill esperada. En MOCK deberías ver `Tasa de acierto: 12/15 = 80%`, y con descriptions vagas, `13%`.

7. **Arregla los fallos (✏️ Tu turno 2).** Cambia las descriptions, **no** el runbook, hasta llegar a ≥ 90 %. Luego copia las descriptions nuevas a `skill-library/<skill>/SKILL.md`.

8. **Provoca las fallas (sección 8 · 🧯).** YAML roto por `: `, nombre inválido, skill inexistente y rutas de escape (`../.env`).

9. **Lleva la biblioteca al laboratorio (sección 9).** Esta parte es opcional y sigue a la práctica de la [6.1](../6.1-clis-de-agentes/README.md) (o a la de la [5.3](../5.3-sandbox-y-politicas/README.md), si te saltaste la 6.1), con la instancia todavía encendida. Si ya borraste tu instancia, sáltala: el notebook basta.

   En el tablero de NemoClaw, presiona **VM TERMINAL** y haz clic dentro del área negra. La biblioteca ya está en la copia del curso que clonaste en la 4.3, en `~/curso/skill-library/`. Si no tienes esa carpeta, clona el curso:
   ```bash
   git clone --depth 1 https://github.com/uncrayon/curso-seguridad-agentes-nemoclaw ~/curso
   ```
   Para instalar una skill, le das a NemoClaw la carpeta que contiene su `SKILL.md`, y luego revisas la lista:
   ```bash
   nemoclaw my-assistant skill install ~/curso/skill-library/diagnostico-api/
   nemoclaw my-assistant skill list
   ```
   Deberías ver `✓ Validated SKILL.md`, luego `Installed diagnostico-api from path -> /sandbox/.openclaw/workspace/skills/diagnostico-api`, y `diagnostico-api` en la lista. Repite con `lector-seguro-archivos` y `resumen-diario`. Ignora la línea `ExperimentalWarning: SQLite…`.

   `soporte-nemoclaw` ya está instalada desde la 4.3. Para cambiarla por la versión de la biblioteca, quita la vieja e instala la nueva:
   ```bash
   nemoclaw my-assistant skill remove soporte-nemoclaw
   nemoclaw my-assistant skill install ~/curso/skill-library/soporte-nemoclaw/
   ```
   Si mejoraste descriptions en el notebook, cámbialas en la VM antes de instalar. Abre el archivo con `nano ~/curso/skill-library/diagnostico-api/SKILL.md`, pega tu description, guarda con Ctrl+O y Enter, y sal con Ctrl+X.

10. **Prueba las dos selecciones en una sesión nueva.** La forma más segura de empezar de cero es una clave de sesión nueva en la VM TERMINAL. Primero, automática (no nombras la skill):
    ```bash
    nemoclaw my-assistant agent --session-key prueba-62a -m 'Me sale 401 al llamar al modelo, ¿qué hago?'
    ```
    Después, explícita (le das la ruta de la skill), en otra sesión:
    ```bash
    nemoclaw my-assistant agent --session-key prueba-62b -m 'Lee /sandbox/.openclaw/workspace/skills/diagnostico-api/SKILL.md y síguela: me sale 401.'
    ```
    También puedes probar en el navegador con **CHAT WITH AGENT**, en una conversación nueva.

11. **Cierra el laboratorio: guarda y borra.** Esta es la última práctica de laboratorio del curso. Al borrar la instancia, todo lo que hay en la VM se pierde.
    - **Guarda lo que quieras.** Los archivos del curso (`~/curso`) ya están en GitHub. Para conservar algo que escribió tu agente, muéstralo en la VM TERMINAL (por ejemplo, `nemoclaw my-assistant exec -- cat /sandbox/.openclaw/workspace/SOUL.md`), selecciónalo con el mouse y pégalo en tus notas.
    - **Borra la instancia.** Cierra la terminal (**Shift+Escape**) y ve a la consola de Brev: **Compute** → tu instancia (`nemoclaw-…`) → **Delete**. Confirma en el aviso que aparece.
    - **Revisa tu saldo.** En el menú de arriba, abre **Billing**. Confirma que la instancia ya no aparece en **Compute**. Detenida, el disco seguiría cobrando ≈USD 1.20 al día; borrada, ya no cobra nada. Detalles en [LABORATORIO.md](../../LABORATORIO.md).

## Comprueba que funcionó
- [ ] Las 4 skills pasan `validar_skill` sin ❌.
- [ ] Viste una selección automática (`cargar_skill`) y una explícita (`/nombre`).
- [ ] Tu tasa de acierto en MOCK es ≥ 90 % después de mejorar las descriptions.
- [ ] El harness rechazó `../.env` y `/etc/passwd`.
- [ ] `nemoclaw <sandbox> skill list` muestra tus skills en el laboratorio.
- [ ] Si hiciste la parte de laboratorio, borraste tu instancia con **Delete** y revisaste **Billing**.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `YAML inválido en el frontmatter: mapping values are not allowed here` | La description tiene `: ` (dos puntos y espacio) sin comillas | Pon la description entre comillas o quita los dos puntos |
| `skill install` no muestra `✓ Validated SKILL.md` y se queja de `SKILL.md` o del `name` | Pasaste la carpeta equivocada o el frontmatter no tiene `name` | La ruta debe apuntar a la carpeta que **contiene** `SKILL.md`, con frontmatter YAML y `name` |
| Nombre rechazado | `name` con espacios, tildes o mayúsculas raras | Solo letras, números, `.`, `-` y `_`. Igual al nombre de la carpeta |
| La skill está instalada pero el agente no la usa sola | La description no dice **cuándo** usarla, o no usa las palabras del usuario | Reescribe la description y vuelve a evaluar. Abre una **sesión nueva** |
| El agente usa la skill equivocada | Dos descriptions compiten por las mismas palabras (p. ej. "403") | Agrega a cada una cuándo **no** usarla y palabras que las distingan |
| `skill install` falla con una skill del mismo nombre (Hermes o Deep Agents) | El fallback no reemplaza una skill existente | `nemoclaw <sandbox> skill remove <nombre>` y reinstala |
| `skill install` dice que la ruta no existe | No clonaste el curso en la VM, o lo clonaste en otra carpeta | Revisa con `ls ~/curso/skill-library`; si no existe, corre el `git clone` del paso 9 |
| Escribes en la VM TERMINAL y no aparece nada | La terminal no tiene el foco | Haz clic dentro del área negra |

## Reto
Crea la quinta skill, **`estimar-costo-brev`**, que use la herramienta `estimar_costo_brev` de la clase 2.3.
**Criterio de éxito:** `validar_skill` no marca ❌ ni ⚠️; agregas 3 pedidos a `PEDIDOS_EVAL` y la tasa total queda en **≥ 90 %** sin que bajen las otras 4 skills.

## Avance del proyecto
El proyecto **Soporte NemoClaw** ya tiene su biblioteca en [`skill-library/`](../../skill-library/README.md):

| Skill | Para qué |
|---|---|
| `soporte-nemoclaw` | Responde con la FAQ y cita la fuente. Es la skill de la 4.3 con la description recortada para no competir con `diagnostico-api` |
| `diagnostico-api` | Explica errores 401/403/404/410/429/5xx |
| `lector-seguro-archivos` | Lee solo dentro de `datos/` |
| `resumen-diario` | El resumen que dispara el cron de la 4.3 |

Entrega: las 4 skills instaladas en tu sandbox, tu tabla de evaluación (antes/después) en `docs/evaluacion-skills.md` y las descriptions mejoradas en el repo.

## Recursos
- NVIDIA DLI · El agente siempre activo (03c). Esta clase está basada en la lección 03c del curso de NVIDIA DLI (Apache-2.0).
- NemoClaw · comandos `skill install | list | remove` en la [referencia de comandos](https://docs.nvidia.com/nemoclaw/latest/).
- Anthropic · [Agent Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview): el formato de `SKILL.md` que usa el curso.
- Wang et al. 2023 · [Voyager](https://arxiv.org/abs/2305.16291): bibliotecas de habilidades que crecen.
- OpenClaw · [Automatización y tareas (cron vs. heartbeat)](https://docs.openclaw.ai/cron-vs-heartbeat).
