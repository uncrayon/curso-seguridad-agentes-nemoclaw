# Cookbook · Skills, FAQ y tareas programadas en NemoClaw

Recetas para instalar skills, cargar archivos de conocimiento al workspace y verificar tareas programadas como operador. Funcionan en el laboratorio del curso y en cualquier sandbox OpenClaw de NemoClaw.

Convenciones:
- Todos los comandos van en la **VM TERMINAL** del tablero de NemoClaw (la terminal de operador, usuario `ubuntu`). Haz clic dentro del área negra antes de escribir.
- Los archivos del curso están en `~/curso` (clase 4.1). Si no, clónalos: `git clone --depth 1 https://github.com/uncrayon/curso-seguridad-agentes-nemoclaw ~/curso`.
- `my-assistant` es el sandbox del laboratorio; confírmalo con `nemoclaw list`.
- Cada comando `nemoclaw` imprime `ExperimentalWarning: SQLite is an experimental feature`. Ignórala.
- `nemoclaw … exec` pasa los argumentos tal cual, **sin shell**. Para usar comodines (`*`), `;` o `&&`, envuélvelos en `bash -lc '…'`.

Basado en la lección 03c del curso NVIDIA DLI «NemoClaw» (Apache-2.0) y en la documentación de NemoClaw.

---

## Receta 1 · Revisa que la skill y la FAQ estén en la máquina

```bash
ls ~/curso/clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/ ~/curso/datos/faq/
head -n 4 ~/curso/clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/SKILL.md
```

Salida esperada: `SKILL.md` en la carpeta de la skill, los `.md` de la FAQ y las primeras líneas de la etiqueta (`---`, `name: soporte-nemoclaw`, `description: …`).

**Si falla:**
- `No such file or directory` → no clonaste el curso. Corre el `git clone` de las convenciones y repite.

---

## Receta 2 · Instala la skill

```bash
nemoclaw my-assistant skill install ~/curso/clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/
```

Salida esperada:

```text
✓ Validated SKILL.md
Installed soporte-nemoclaw from path -> /sandbox/.openclaw/workspace/skills/soporte-nemoclaw
```

Comprueba dónde quedó:

```bash
nemoclaw my-assistant exec -- ls /sandbox/.openclaw/workspace/skills/
nemoclaw my-assistant exec -- head -n 4 /sandbox/.openclaw/workspace/skills/soporte-nemoclaw/SKILL.md
```

`nemoclaw my-assistant skill list` muestra la vista de OpenClaw de todas las skills (antes de instalar, el laboratorio mostró `22/57 ready`).

**Si falla:**
- Falta `SKILL.md` o la etiqueta no tiene `name` → corrige el archivo. El `name` solo admite letras, números, puntos, guiones y guiones bajos.
- Pasaste una carpeta con forma de *plugin* → la CLI imprime una pista de plugin. Las skills y los plugins de OpenClaw son cosas distintas.
- Para reinstalar después de editar: vuelve a correr `skill install`. Si no reemplaza la anterior, quítala primero con `skill remove soporte-nemoclaw` (receta 9).

---

## Receta 3 · Sube la FAQ al workspace

```bash
nemoclaw my-assistant upload ~/curso/datos/faq/ /sandbox/.openclaw/workspace/
nemoclaw my-assistant exec -- ls -la /sandbox/.openclaw/workspace/faq/
```

Salida esperada: los archivos `.md` directamente dentro de `faq/`, con dueño `sandbox`.

El destino es la carpeta **padre** (`workspace/`). `upload` crea `faq/` adentro. Si el destino ya termina en `faq/`, la copia queda anidada en `faq/faq/`.

**Si falla:**
- Quedó en `faq/faq/` → bórrala y sube otra vez con el destino correcto:
  ```bash
  nemoclaw my-assistant exec -- rm -rf /sandbox/.openclaw/workspace/faq
  nemoclaw my-assistant upload ~/curso/datos/faq/ /sandbox/.openclaw/workspace/
  ```
- `upload` dice que el sandbox no está vivo → `nemoclaw my-assistant status` (debe decir `Phase Ready` e Inference `healthy`).

---

## Receta 4 · Usa la skill de forma explícita

```bash
nemoclaw my-assistant agent --session-key skill-explicita-01 -m 'Lee /sandbox/.openclaw/workspace/skills/soporte-nemoclaw/SKILL.md y síguelo para esta duda de un estudiante: "Si detengo mi instancia de Brev, ¿me siguen cobrando?"'
```

Salida esperada: una respuesta con **Categoría:**, pasos numerados y **Fuente:** `faq/<archivo>.md`.

Lo mismo funciona en el chat (**CHAT WITH AGENT**): pega el texto que va entre las comillas simples.

**Si falla:**
- "No encuentro la FAQ del curso en el workspace" → receta 3.
- La respuesta no tiene el formato → el agente no leyó el `SKILL.md`. Revisa la ruta (receta 2) y los logs: `nemoclaw my-assistant logs --tail 50`.

---

## Receta 5 · Prueba el descubrimiento automático

```bash
nemoclaw my-assistant agent --session-key prueba-43 -m 'Mi API key de NVIDIA me da 401, ¿qué hago?'
```

Salida esperada: el formato de la skill **sin** que le hayas dado la ruta. En la prueba del curso: **Categoría:** `api_key`, pasos numerados y **Fuente:** `faq/errores-api.md` y `faq/api-key.md`. La sesión `prueba-43` aparece luego en la barra lateral del chat.

**Si falla:** el agente decide con la `description`. Hazla concreta: qué resuelve, para quién y con qué palabras pregunta la gente (errores, comandos, productos). Edita, reinstala (receta 2) y prueba con un `--session-key` nuevo.

Para comparar a propósito (el reto de la clase), instala una versión con descripción vaga y luego restaura la buena:

```bash
cp -r ~/curso/clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw ~/soporte-vaga
sed -i 's/^description: .*/description: Skill de soporte./' ~/soporte-vaga/SKILL.md
nemoclaw my-assistant skill remove soporte-nemoclaw
nemoclaw my-assistant skill install ~/soporte-vaga/                 # mismo name, descripción vaga
nemoclaw my-assistant agent --session-key skill-auto-02 -m 'Un estudiante dice: "Mi notebook responde HTTP 401". ¿Qué le respondes?'
nemoclaw my-assistant skill remove soporte-nemoclaw
nemoclaw my-assistant skill install ~/curso/clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/   # restaura la buena
```

---

## Receta 6 · Programa el resumen en Automations (navegador)

La tarea se programa con clics, en el chat de OpenClaw: **CHAT WITH AGENT** → barra lateral **Automations** → **New automation**.

| Campo | Valor | Para qué |
|---|---|---|
| **Prompt** | El texto de abajo | La directiva: lo que el agente hará. |
| **Action** · **Model** · **Reasoning** | **Run agent task** · **Default** · **low** | Una ejecución normal del agente. |
| **Name** | `soporte-resumen-faq` | Para reconocerla en la lista y en `cron list`. |
| **Runs in** | **Isolated session** | Una sesión nueva en cada disparo: no hereda tu chat. |
| **Repeat** | **Once** | Una sola vez. |
| **Run at** | Hoy, tu hora + 2 minutos | Hora local de tu navegador. |
| **Delivery → Mode** | **None (internal)** | No publica nada en el chat. |
| **Advanced → Delete after run** | Encendido (viene así con **Once**) | La tarea se borra sola después de correr. |

Prompt:

```text
Usa la skill soporte-nemoclaw. Lee los archivos de faq/ y escribe en reportes/resumen-faq.md un resumen de 5 líneas: qué temas cubre la FAQ y cuál es la pregunta más útil para alguien nuevo. No cambies ningún otro archivo.
```

Haz clic en **Create automation**. La lista muestra **NEXT RUN** `in 2m`, luego **Running**, y en **Run history** una ejecución **OK** con el modelo, los tokens (≈112 mil en la prueba del curso) y el resumen. No escribas en el chat mientras espera.

Las otras opciones de **Repeat**: **Interval** (cada N minutos u horas) y **Cron** (una expresión como `0 3 * * *`, todos los días a las 3:00). **Create & run now** la ejecuta en el acto, además de programarla.

---

## Receta 7 · Verifica la tarea como operador

```bash
nemoclaw my-assistant exec -- bash -lc 'ls -la /sandbox/.openclaw/workspace/reportes/; cat /sandbox/.openclaw/workspace/reportes/resumen-faq.md'
nemoclaw my-assistant exec -- openclaw cron list
```

Salida esperada:
- `-rw-r--r-- 1 sandbox sandbox … resumen-faq.md`, un texto que empieza con `# Resumen FAQ -` y la fecha (UTC) y termina con `Generado por la skill soporte-nemoclaw.`
- `cron list`: una tabla con columnas ID, Declaration, Name, Schedule, Next, Last y Status. Aparecen `heartbeat:main` (every 30m), la tarea de memoria (`cron 0 3 * * *`) y `skill-collection-review` (every 7d). Tu tarea ya no está, por **Delete after run**.

**Si falla:**
- **Run history** dice **OK** pero no hay archivo → el agente dijo que lo hizo y no lo hizo, o lo escribió en otra ruta:
  ```bash
  nemoclaw my-assistant exec -- bash -lc 'grep -rl "Generado por la skill soporte-nemoclaw" /sandbox/.openclaw/workspace/'
  ```
- La hora quedó mal → **Run at** usa la hora de tu navegador; la hora de los archivos está en UTC. Para ver la hora UTC de la máquina: `date -u`.

---

## Receta 8 · Heartbeat: referencia para tu propia instalación

**No lo cambies en el laboratorio del curso**: cada heartbeat es un turno del modelo que consume créditos. En el laboratorio, `heartbeat-main` aparece como **Skipped** · `no-route`, y eso es normal.

En una instalación propia de NemoClaw:

```bash
# Antes del onboarding
export NEMOCLAW_AGENT_HEARTBEAT_EVERY=2h     # entero + s, m o h; 0m lo apaga
nemoclaw onboard

# En un sandbox existente
nemoclaw <sandbox> connect
openclaw config set agents.defaults.heartbeat.every 2h
openclaw config unset agents.defaults.heartbeat.every    # vuelve al valor por defecto (30 min)
```

En cada intervalo, el agente despierta en una sesión dedicada y lee `HEARTBEAT.md` si existe.

---

## Receta 9 · Diagnóstico, pausa y limpieza

Si una tarea no corre o tarda:

```bash
nemoclaw my-assistant status                     # Phase Ready e Inference healthy
nemoclaw my-assistant logs --tail 100            # turnos recientes, incluidos los de las tareas
nemoclaw my-assistant exec -- openclaw cron list # qué tareas existen y cuándo corren
date -u                                          # hora UTC de la máquina
```

Para **pausar** o **borrar** una tarea, usa el menú **⋯** de su fila en **Automations**. Nunca dejes una tarea con **Interval** de pocos minutos encendida: cada disparo gasta créditos del modelo (≈112 mil tokens en la prueba del curso).

Para quitar la skill y el reporte:

```bash
nemoclaw my-assistant skill remove soporte-nemoclaw     # usa el name de la etiqueta
nemoclaw my-assistant exec -- rm -f /sandbox/.openclaw/workspace/reportes/resumen-faq.md
```

No la quites si vas a seguir con «Seguridad agéntica con OpenShell» (o con la clase 4.4, material complementario): ahí la vuelves a usar. Si paras por hoy, detén la instancia en la consola de Brev con **Stop** y vuelve pronto; al final de todo el laboratorio, **Delete** (ver [LABORATORIO.md](../../LABORATORIO.md)).
