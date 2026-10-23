# Cookbook · Hermes Agent en NemoClaw

Recetas para crear, operar, observar y apagar un sandbox de Hermes con NemoClaw. Funcionan en el laboratorio del curso y en cualquier instalación de NemoClaw (Linux, macOS con Apple Silicon o WSL2).

> **La clase 4.4 es material complementario: no tiene video.** No la necesitas para seguir el curso. Si la haces, suma ≈30 min (≈USD 0.13) a tu sentada de laboratorio. Al terminar, vuelve a encender OpenClaw (`my-assistant`) antes de seguir: la receta 14 te dice cómo.

Convenciones:
- Todos los comandos van en la **VM TERMINAL** del tablero de NemoClaw (la terminal de operador, usuario `ubuntu`). Ahí está `nemohermes`; la **SANDBOX TERMINAL** no lo tiene. Haz clic dentro del área negra antes de escribir y no presiones **Shift+Escape** mientras corre un comando largo: cierra la terminal y sus procesos.
- Los archivos del curso están en `~/curso` (clase 4.1). Si no, clónalos: `git clone --depth 1 https://github.com/uncrayon/curso-seguridad-agentes-nemoclaw ~/curso`.
- `mi-hermes` es el sandbox de esta clase; `my-assistant`, el de OpenClaw del laboratorio. Confírmalos con `nemoclaw list`.
- Cada comando `nemoclaw` o `nemohermes` imprime una línea `ExperimentalWarning` de SQLite. Ignórala.
- `nemohermes` es el CLI de NemoClaw con Hermes seleccionado. `nemohermes <sandbox> <acción>` y `nemoclaw <sandbox> <acción>` operan el mismo registro de sandboxes.
- `nemohermes … exec` pasa los argumentos tal cual, **sin shell**. Para comodines (`*`) o `&&`, usa `bash -lc '…'`.

Basado en la documentación de NemoClaw para Hermes y de Hermes Agent (Nous Research, MIT).

---

## Receta 1 · Antes de empezar: versiones y recursos

```bash
nemoclaw --version
nemohermes --version
nemoclaw list
free -h && df -h /
```

- Anota la versión: NemoClaw publica versiones cada pocos días. En la prueba del curso, `nemoclaw` y `nemohermes` eran `v0.0.135`, y la VM tenía 15 GiB de memoria y 267 G de disco libre.
- Un segundo sandbox necesita memoria y disco. Para ir seguro, detén el de OpenClaw mientras trabajas con Hermes:

```bash
nemoclaw my-assistant stop
```

Lo vuelves a encender con `nemoclaw my-assistant start` (receta 14). No lo olvides: las prácticas de «Seguridad agéntica con OpenShell» lo usan.

---

## Receta 2 · Crea el sandbox de Hermes (interactivo)

```bash
read -rsp "NVIDIA API key: " NVIDIA_INFERENCE_API_KEY; echo
export NVIDIA_INFERENCE_API_KEY
NEMOCLAW_SANDBOX_NAME=mi-hermes nemohermes onboard
```

`read -rsp` no muestra la key en pantalla ni la deja en el historial de la terminal.

En el asistente, las preguntas pueden variar un poco según la versión; elige:

| Pregunta | Respuesta para el curso |
|---|---|
| Run express install with these settings? | `n` (para elegir nombre, proveedor y modelo) |
| Proveedor de inferencia | **NVIDIA Endpoints** |
| Modelo | El que propone (por ejemplo, `nvidia/nemotron-3-super-120b-a12b`) |
| Búsqueda web | `none` (Hermes solo soporta Tavily) |
| Mensajería | Omitir |
| Nivel de política | El sugerido |
| Aviso de software de terceros | Léelo y acéptalo solo si estás de acuerdo |

Salida esperada: un resumen final con el nombre `mi-hermes`, el puerto del dashboard y el de la API. La primera vez descarga la imagen: puede tardar varios minutos. No cierres la terminal mientras tanto.

Alternativa para un laboratorio nuevo: en la configuración del navegador (**Connect to AI**) puedes elegir **Hermes** como agente desde el principio. En este curso lo creas como segundo cuarto para conservar `my-assistant`.

**Si se interrumpe:** `nemohermes onboard --resume` continúa; `nemohermes onboard --fresh` descarta el intento y empieza de nuevo.

---

## Receta 3 · Crea el sandbox sin preguntas (para scripts)

```bash
read -rsp "NVIDIA API key: " NVIDIA_INFERENCE_API_KEY; echo
export NVIDIA_INFERENCE_API_KEY
export NEMOCLAW_AGENT=hermes
export NEMOCLAW_SANDBOX_NAME=mi-hermes
export NEMOCLAW_PROVIDER=build
export NEMOCLAW_WEB_SEARCH_PROVIDER=none
export NEMOCLAW_NON_INTERACTIVE=1
export NEMOCLAW_ACCEPT_THIRD_PARTY_SOFTWARE=1   # solo si ya leíste y aceptas el aviso
nemohermes onboard
```

Al terminar, borra la key de la sesión: `unset NVIDIA_INFERENCE_API_KEY`. NemoClaw ya la guardó en el host; el sandbox solo recibe un marcador.

---

## Receta 4 · Comprueba que está sano

```bash
nemohermes mi-hermes status
openshell forward list
curl -sf http://127.0.0.1:8642/health && echo " API ok"
```

Salida esperada:
- `status`: la línea principal **Inference** en `healthy`; el proceso del agente corriendo.
- `forward list`: dos entradas de `mi-hermes`, el dashboard (`18789` o el siguiente libre) y la API (`8642` o el siguiente libre).
- `API ok`.

**Si falla:**
- `Inference: unauthorized` → la key es incorrecta. Vuelve a crear el cuarto con `nemohermes onboard --fresh` y escribe la key con cuidado.
- No hay forwards o `curl` no conecta → `nemohermes mi-hermes recover`.
- `status` dice que el sandbox no está listo → espera; la primera vez puede tardar. Revisa `nemohermes mi-hermes logs --tail 50`.

---

## Receta 5 · Conversa con Hermes

```bash
nemohermes launch mi-hermes          # abre Hermes directamente
# o, si quieres una terminal dentro del sandbox:
nemohermes mi-hermes connect
hermes
```

Comandos útiles dentro de Hermes:

| Comando | Para qué |
|---|---|
| `/new` | Sesión nueva (carga memoria y skills actualizadas) |
| `/skills` o `/<nombre-de-skill>` | Ver o usar una skill |
| `/memory pending` · `/memory approve <id>` · `/memory reject <id>` | Revisar escrituras de memoria en espera |
| `/memory approval on` · `/skills approval on` | Exigir aprobación antes de escribir memoria o skills |
| `/reset` | Limpiar la conversación si hay un error de contexto |
| `/exit` | Salir y volver al host |

Los comandos pueden cambiar entre versiones de Hermes: `/help` muestra la lista de la tuya.

Hermes también trae su propio dashboard en el navegador (sin `#token=` en la URL: maneja su propia sesión). El tablero del laboratorio y su botón **CHAT WITH AGENT** se armaron para `my-assistant`, así que en este curso hablas con Hermes en la terminal. En una instalación propia, `nemohermes mi-hermes dashboard-url --quiet` te da la dirección.

---

## Receta 6 · Revisa que la skill, la FAQ y el script estén en la máquina

Todo llega con el `git clone` de la clase 4.1. Para actualizarlo si ya lo tenías: `git -C ~/curso pull`.

```bash
ls ~/curso/clases/4.4-hermes-en-nemoclaw/skills/soporte-nemoclaw/ ~/curso/datos/faq/ ~/curso/clases/4.4-hermes-en-nemoclaw/hermes_api.py
```

Salida esperada: `SKILL.md`, los `.md` de la FAQ y el script.

---

## Receta 7 · SOUL.md: la personalidad de Hermes

Hermes lee su personalidad de `/sandbox/SOUL.md` (en OpenClaw era `/sandbox/.openclaw/workspace/SOUL.md`).

```bash
mkdir -p ~/hermes && cd ~/hermes
nemohermes mi-hermes download /sandbox/SOUL.md ./
cp SOUL.md SOUL.md.original
cat >> SOUL.md <<'EOF'

## Proyecto: Soporte NemoClaw
- Ayudas a estudiantes del curso "Agentes Seguros con NemoClaw".
- Respondes en español neutro, con frases cortas y pasos numerados.
- Antes de responder, clasificas la duda en una categoría: instalacion, api_key, brev, seguridad u otro.
- Si usas la FAQ del curso, citas el archivo de donde sale la respuesta.
- Nunca pides, repites ni guardas API keys, tokens o cookies. Si alguien pega una, le pides que la revoque.
- Si no sabes algo, lo dices y sugieres preguntar en el foro del curso.
EOF
nemohermes mi-hermes upload ./SOUL.md /sandbox/SOUL.md
nemohermes mi-hermes exec -- tail -n 8 /sandbox/SOUL.md
```

Pruébalo en una sesión nueva: *"¿Quién eres, a quién ayudas y qué nunca haces?"*.

Volver al original: `nemohermes mi-hermes upload ./SOUL.md.original /sandbox/SOUL.md`.

`SOUL.md` sobrevive a `rebuild` y a actualizaciones (es parte del *home* persistente del sandbox). `destroy` lo borra.

---

## Receta 8 · Instala la skill y sube la FAQ

```bash
nemohermes mi-hermes skill install ~/curso/clases/4.4-hermes-en-nemoclaw/skills/soporte-nemoclaw/
nemohermes mi-hermes skill list
nemohermes mi-hermes upload ~/curso/datos/faq/ /sandbox/
nemohermes mi-hermes exec -- bash -lc 'ls /sandbox/faq; head -n 6 /sandbox/.hermes/skills/soporte-nemoclaw/SKILL.md'
```

Salida esperada: `soporte-nemoclaw` en `skill list`, los `.md` de la FAQ en `/sandbox/faq` y el frontmatter de la skill.

- Hermes no tiene un comando nativo para instalar una carpeta local. NemoClaw valida el `SKILL.md` (frontmatter con `name`) y copia la carpeta a `/sandbox/.hermes/skills/<name>/`. Hermes la descubre al iniciar una sesión.
- Para reemplazarla: `nemohermes mi-hermes skill remove soporte-nemoclaw` y vuelve a instalar. `skill install` no sobrescribe una carpeta con el mismo nombre.
- El destino de `upload` es la carpeta padre (`/sandbox/`): `upload` crea `faq/` adentro, como en la 4.3. Si la FAQ quedó en `/sandbox/faq/faq/`, bórrala con `nemohermes mi-hermes exec -- rm -rf /sandbox/faq` y sube otra vez con destino `/sandbox/`.

**Prueba (sesión nueva):**

> Un estudiante dice: "Mi notebook responde HTTP 401 cuando llamo al modelo". ¿Qué le respondes?

Debe responder con **Categoría**, **Qué hacer** y **Fuente:** `faq/errores-api.md`.

---

## Receta 9 · Memoria y skills que Hermes escribe solo

Hermes **aprende**: guarda notas en su memoria y puede crear o mejorar skills con su herramienta `skill_manage`. Es útil y es un riesgo: una instrucción maliciosa puede quedar guardada y afectar sesiones futuras (lo verás en «Seguridad agéntica con OpenShell»).

| Archivo | Qué guarda | Límite |
|---|---|---|
| `/sandbox/.hermes/memories/MEMORY.md` | Notas del agente | ≈2,200 caracteres |
| `/sandbox/.hermes/memories/USER.md` | Perfil del usuario | ≈1,375 caracteres |
| `/sandbox/.hermes/skills/` | Skills instaladas y creadas por el agente | — |
| `/sandbox/.hermes/state.db` | Sesiones (SQLite, con búsqueda de texto) | — |

**Exige aprobación (dentro de Hermes):**

```text
/memory approval on
/skills approval on
```

**Prueba:** pídele *"Recuerda que mi instancia de Brev se llama lab-prueba"*. Luego:

```text
/memory pending
/memory approve <id>      # o /memory reject <id>
```

Los cambios de memoria entran al prompt en la **siguiente** sesión (`/new`).

**Léela como operador:**

```bash
nemohermes mi-hermes exec -- bash -lc 'cat /sandbox/.hermes/memories/MEMORY.md 2>/dev/null || echo "(sin memoria todavía)"'
```

---

## Receta 10 · Sesiones: lista, exporta y borra

```bash
nemohermes mi-hermes sessions list --limit 5
nemohermes mi-hermes sessions export --out ~/sesiones-mi-hermes.jsonl
ls -l ~/sesiones-mi-hermes.jsonl
head -c 600 ~/sesiones-mi-hermes.jsonl; echo
```

- El archivo queda en la VM con permisos `0600`. Contiene prompts, salidas de herramientas y lo que el estudiante haya pegado: no lo subas a ningún repositorio. Al borrar la instancia (**Delete**) desaparece con ella.
- Borrar una sesión: `nemohermes mi-hermes sessions delete <id>` (el id sale de `sessions list`, por ejemplo `20260727_130357_cb2b61`).
- A diferencia de OpenClaw, no exporta por clave ni en `tar`: Hermes guarda todo en SQLite y lo saca como un solo JSONL.

---

## Receta 11 · La API compatible con OpenAI

```bash
TOKEN="$(nemohermes mi-hermes gateway-token --quiet)"
curl -fsS -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8642/v1/models
curl -fsS -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  http://127.0.0.1:8642/v1/chat/completions \
  -d '{"model":"<id de /v1/models>","messages":[{"role":"user","content":"¿Qué haces si un estudiante te pega su API key?"}]}'
```

- El token es el `API_SERVER_KEY` del sandbox: trátalo como contraseña. Se mantiene entre reinicios y cambia si reconstruyes el sandbox.
- La API escucha solo en `127.0.0.1` de la VM: los programas que la usan corren en la misma VM. No la abras a internet.
- Cualquier cliente de OpenAI sirve: `base_url="http://127.0.0.1:8642/v1"` y `api_key=<token>`.
- Usa en `"model"` el id que devolvió `/v1/models`.

---

## Receta 12 · Llama a Hermes desde Python

Todo corre en la VM, no dentro del sandbox.

```bash
python3 -m venv ~/venv-hermes && source ~/venv-hermes/bin/activate
pip install -q openai
export HERMES_TOKEN="$(nemohermes mi-hermes gateway-token --quiet)"
python3 ~/curso/clases/4.4-hermes-en-nemoclaw/hermes_api.py "Mi notebook responde HTTP 401 cuando llamo al modelo"
```

Salida esperada: la respuesta de Hermes (con **Categoría** y **Fuente:** si usó la skill) y una línea `modelo: … · N s`.

El script usa el cliente normal de OpenAI con `base_url="http://127.0.0.1:8642/v1"` y lee el token de la variable `HERMES_TOKEN`: nunca lo imprime. Si un mensaje de error trae una key o un token, lo tacha antes de mostrarlo.

Lo que **no** verás: los `grep` y `cat` que Hermes ejecutó dentro del sandbox. Esos están en las sesiones (receta 10). Lo que ve el cliente y lo que hizo el agente son capas distintas.

**Si falla:**
- `Falta HERMES_TOKEN` → corre otra vez la línea `export HERMES_TOKEN=…` en la misma terminal.
- `401: el token no es válido` → vuelve a leer el token (cambia si reconstruiste).
- `No pude hablar con Hermes` → el puerto no es `8642`: `export HERMES_BASE_URL=http://127.0.0.1:<puerto>/v1`.
- `python3 -m venv` falla → `sudo apt-get install -y python3-venv` y repite.

---

## Receta 13 · Logs, política y bloqueos

```bash
nemohermes mi-hermes logs --tail 50          # gateway + auditoría de OpenShell
nemohermes mi-hermes logs --follow           # en vivo; Ctrl+C para salir
nemohermes mi-hermes policy list             # presets activos (Hermes tiene su propia base)
openshell term                               # la misma vista que el botón OPENSHELL TUI del tablero
```

Una línea `DENIED` en los logs significa que OpenShell bloqueó una conexión de salida: es la política funcionando, igual que con OpenClaw.

---

## Receta 14 · Apaga, enciende y limpia

```bash
nemohermes mi-hermes stop                    # detiene el sandbox y su dashboard
nemohermes mi-hermes start                   # lo vuelve a encender
nemoclaw my-assistant start                  # si detuviste el de OpenClaw
nemoclaw my-assistant status                 # debe decir Phase Ready e Inference healthy
```

Para borrar el sandbox de Hermes **y todo su estado** (SOUL.md, memoria, skills, sesiones):

```bash
nemohermes mi-hermes destroy
```

`destroy` no se puede deshacer. Exporta antes las sesiones que quieras conservar (receta 10).

Si paras por hoy, detén la instancia en la consola de Brev con **Stop** y vuelve pronto; al final de todo el laboratorio (después de la 5.3, o de la última práctica complementaria que hagas), **Delete** (ver [LABORATORIO.md](../../LABORATORIO.md)).
