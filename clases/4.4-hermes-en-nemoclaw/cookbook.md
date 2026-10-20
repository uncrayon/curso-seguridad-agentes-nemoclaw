# Cookbook 4.4 · Hermes Agent en NemoClaw

Recetas para crear, operar, observar y apagar un sandbox de Hermes con NemoClaw. Funcionan en el launchable del curso y en cualquier instalación de NemoClaw (Linux, macOS con Apple Silicon o WSL2).

Convenciones:
- **En tu computadora** = terminal local, desde la raíz del repo del curso. **En la máquina** = dentro de `brev shell <instancia>`.
- `mi-hermes` es el sandbox de esta clase; `my-assistant`, el de OpenClaw del launchable. Confírmalos con `nemoclaw list`.
- `nemohermes` es el CLI de NemoClaw con Hermes seleccionado. `nemohermes <sandbox> <acción>` y `nemoclaw <sandbox> <acción>` operan el mismo registro de sandboxes.
- `nemohermes … exec` pasa los argumentos tal cual, **sin shell**. Para comodines (`*`) o `&&`, usa `bash -lc '…'`.

Basado en la documentación de NemoClaw para Hermes y de Hermes Agent (Nous Research, MIT).

---

## Receta 1 · Antes de empezar: versiones y recursos

**En la máquina:**

```bash
nemoclaw --version
nemohermes --version
nemoclaw list
free -h && df -h /
```

- Anota la versión: NemoClaw publica versiones cada pocos días. `[VERIFICAR EN LAB: versión del launchable y que incluya nemohermes]`
- Un segundo sandbox necesita memoria y disco. Si `free -h` muestra menos de ≈4 GB libres, detén el de OpenClaw mientras trabajas:

```bash
nemoclaw my-assistant stop
```

Lo vuelves a encender con `nemoclaw my-assistant start` (receta 13).

---

## Receta 2 · Crea el sandbox de Hermes (interactivo)

**En la máquina:**

```bash
read -rsp "NVIDIA API key: " NVIDIA_INFERENCE_API_KEY; echo
export NVIDIA_INFERENCE_API_KEY
NEMOCLAW_SANDBOX_NAME=mi-hermes nemohermes onboard
```

`read -rsp` no muestra la key en pantalla ni la deja en el historial de la terminal.

En el asistente:

| Pregunta | Respuesta para el curso |
|---|---|
| Run express install with these settings? | `n` (para elegir nombre, proveedor y modelo) |
| Proveedor de inferencia | **NVIDIA Endpoints** |
| Modelo | El que propone (por ejemplo, `nvidia/nemotron-3-super-120b-a12b`) |
| Búsqueda web | `none` (Hermes solo soporta Tavily) |
| Mensajería | Omitir |
| Nivel de política | El sugerido |
| Aviso de software de terceros | Léelo y acéptalo solo si estás de acuerdo |

Salida esperada: un resumen final con el nombre `mi-hermes`, el puerto del dashboard y el de la API. La primera vez descarga la imagen: puede tardar varios minutos.

**Si se interrumpe:** `nemohermes onboard --resume` continúa; `nemohermes onboard --fresh` descarta el intento y empieza de nuevo.

---

## Receta 3 · Crea el sandbox sin preguntas (para scripts)

**En la máquina:**

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

**En la máquina:**

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
- `Inference: unauthorized` → la key es incorrecta: `nemohermes inference set --provider build --model <modelo>` y vuelve a escribirla `[VERIFICAR EN LAB]`.
- No hay forwards o `curl` no conecta → `nemohermes mi-hermes recover`.
- `status` dice que el sandbox no está listo → espera; la primera vez puede tardar. Revisa `nemohermes mi-hermes logs --tail 50`.

---

## Receta 5 · Conversa con Hermes

**Terminal (en la máquina):**

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

`[VERIFICAR EN LAB: lista de comandos en la versión fijada de Hermes]`

**Dashboard (en tu computadora):**

```bash
brev port-forward <instancia> -p 18789:18789     # usa el puerto del dashboard que mostró forward list
```

Luego, en la máquina, `nemohermes mi-hermes dashboard-url --quiet` te da la URL; ábrela en tu navegador cambiando el host por `127.0.0.1`. Hermes **no** usa `#token=` en la URL: maneja su propia sesión.

---

## Receta 6 · Lleva la skill, la FAQ y el script a la máquina

**En tu computadora** (raíz del repo):

```bash
brev copy ./clases/4.4-hermes-en-nemoclaw/skills/soporte-nemoclaw <instancia>:/home/ubuntu/soporte-nemoclaw-hermes
brev copy ./clases/4.4-hermes-en-nemoclaw/hermes_trazado.py <instancia>:/home/ubuntu/hermes_trazado.py
brev copy ./datos/faq <instancia>:/home/ubuntu/faq        # si no la copiaste en la 4.3
```

`[VERIFICAR EN LAB: que brev copy acepte carpetas y que el inicio sea /home/ubuntu]`. Si `brev copy` falla, la receta 1 del cookbook 4.3 trae el método con heredoc: usa el `SKILL.md` de esta clase.

**En la máquina:**

```bash
ls ~/soporte-nemoclaw-hermes ~/faq ~/hermes_trazado.py
```

---

## Receta 7 · SOUL.md: la personalidad de Hermes

Hermes lee su personalidad de `/sandbox/SOUL.md` (en OpenClaw era `/sandbox/.openclaw/workspace/SOUL.md`).

**En la máquina:**

```bash
mkdir -p ~/hermes && cd ~/hermes
nemohermes mi-hermes download /sandbox/SOUL.md ./
cp SOUL.md SOUL.md.original
cat >> SOUL.md <<'EOF'

## Proyecto: Soporte NemoClaw
- Ayudas a estudiantes del curso "Seguridad de agentes con OpenShell y NemoClaw".
- Respondes en español neutro, con frases cortas y pasos numerados.
- Antes de responder, clasificas la duda en una categoría: instalacion, api_key, brev, seguridad u otro.
- Si usas la FAQ del curso, citas el archivo de donde sale la respuesta.
- Nunca pides, repites ni guardas API keys, tokens o cookies. Si alguien pega una, le pides que la revoque.
- Si no sabes algo, lo dices y sugieres abrir un issue o preguntar en el foro del curso.
EOF
nemohermes mi-hermes upload ./SOUL.md /sandbox/SOUL.md
nemohermes mi-hermes exec -- tail -n 8 /sandbox/SOUL.md
```

Pruébalo en una sesión nueva: *"¿Quién eres, a quién ayudas y qué nunca haces?"*.

Volver al original: `nemohermes mi-hermes upload ./SOUL.md.original /sandbox/SOUL.md`.

`SOUL.md` sobrevive a `rebuild` y a actualizaciones (es parte del *home* persistente del sandbox). `destroy` lo borra.

---

## Receta 8 · Instala la skill y sube la FAQ

**En la máquina:**

```bash
nemohermes mi-hermes skill install ~/soporte-nemoclaw-hermes/
nemohermes mi-hermes skill list
nemohermes mi-hermes upload ~/faq/ /sandbox/faq/
nemohermes mi-hermes exec -- bash -lc 'ls /sandbox/faq; head -n 6 /sandbox/.hermes/skills/soporte-nemoclaw/SKILL.md'
```

Salida esperada: `soporte-nemoclaw` en `skill list`, los `.md` de la FAQ en `/sandbox/faq` y el frontmatter de la skill.

- Hermes no tiene un comando nativo para instalar una carpeta local. NemoClaw valida el `SKILL.md` (frontmatter con `name`) y copia la carpeta a `/sandbox/.hermes/skills/<name>/`. Hermes la descubre al iniciar una sesión.
- Para reemplazarla: `nemohermes mi-hermes skill remove soporte-nemoclaw` y vuelve a instalar. `skill install` no sobrescribe una carpeta con el mismo nombre.
- Si la FAQ quedó en `/sandbox/faq/faq/`, bórrala con `nemohermes mi-hermes exec -- rm -rf /sandbox/faq` y sube los archivos: `nemohermes mi-hermes upload ~/faq/. /sandbox/faq/` `[VERIFICAR EN LAB: cómo anida upload una carpeta]`.

**Prueba (sesión nueva):**

> Un estudiante dice: "Mi notebook responde HTTP 401 cuando llamo al modelo". ¿Qué le respondes?

Debe responder con **Categoría**, **Qué hacer** y **Fuente:** `faq/errores-api.md`.

---

## Receta 9 · Memoria y skills que Hermes escribe solo

Hermes **aprende**: guarda notas en su memoria y puede crear o mejorar skills con su herramienta `skill_manage`. Es útil y es un riesgo: una instrucción maliciosa puede quedar guardada y afectar sesiones futuras (lo verás en el Módulo 5).

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

**Léela como operador (en la máquina):**

```bash
nemohermes mi-hermes exec -- bash -lc 'cat /sandbox/.hermes/memories/MEMORY.md 2>/dev/null || echo "(sin memoria todavía)"'
```

`[VERIFICAR EN LAB: que memories/ exista en la versión fijada y que la aprobación persista tras rebuild]`

---

## Receta 10 · Sesiones: lista, exporta y borra

**En la máquina:**

```bash
nemohermes mi-hermes sessions list --limit 5
nemohermes mi-hermes sessions export --out ./sesiones-mi-hermes.jsonl
ls -l ./sesiones-mi-hermes.jsonl
head -c 600 ./sesiones-mi-hermes.jsonl; echo
```

- El archivo queda con permisos `0600`. Contiene prompts, salidas de herramientas y lo que el estudiante haya pegado: no lo subas a tu repo.
- Borrar una sesión: `nemohermes mi-hermes sessions delete <id>` (el id sale de `sessions list`, por ejemplo `20260727_130357_cb2b61`).
- A diferencia de OpenClaw, no exporta por clave ni en `tar`: Hermes guarda todo en SQLite y lo saca como un solo JSONL.

---

## Receta 11 · La API compatible con OpenAI

**En la máquina:**

```bash
TOKEN="$(nemohermes mi-hermes gateway-token --quiet)"
curl -fsS -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8642/v1/models
curl -fsS -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  http://127.0.0.1:8642/v1/chat/completions \
  -d '{"model":"<id de /v1/models>","messages":[{"role":"user","content":"¿Qué haces si un estudiante te pega su API key?"}]}'
```

- El token es el `API_SERVER_KEY` del sandbox: trátalo como contraseña. Se mantiene entre reinicios y cambia si reconstruyes el sandbox.
- La API escucha solo en `127.0.0.1`. Para usarla desde tu computadora: `brev port-forward <instancia> -p 8642:8642`. No la abras a internet.
- Cualquier cliente de OpenAI sirve: `base_url="http://127.0.0.1:8642/v1"` y `api_key=<token>`.

`[VERIFICAR EN LAB: id del modelo que devuelve /v1/models]`

---

## Receta 12 · Trazas con Phoenix (clase 3.4)

**En la máquina:**

```bash
docker run -d --name phoenix -p 127.0.0.1:6006:6006 arizephoenix/phoenix:latest
python3 -m venv ~/venv-trazas && source ~/venv-trazas/bin/activate
pip install -q openai opentelemetry-sdk opentelemetry-exporter-otlp-proto-http openinference-instrumentation-openai
export HERMES_TOKEN="$(nemohermes mi-hermes gateway-token --quiet)"
python3 ~/hermes_trazado.py "Mi notebook responde HTTP 401 cuando llamo al modelo"
```

Salida esperada: la respuesta de Hermes y una línea `modelo: … · N s · traza: <id>`.

**En tu computadora:**

```bash
brev port-forward <instancia> -p 6006:6006
```

Abre `http://127.0.0.1:6006` → **Projects → soporte-nemoclaw-hermes**. Verás un span `AGENT` (`hermes · pregunta`) con un span `LLM` automático dentro, con la pregunta, la respuesta, la latencia y los tokens que reporte Hermes.

Lo que **no** verás: los `grep` y `cat` que Hermes ejecutó dentro del sandbox. Esos están en las sesiones (receta 10). Trazar el cliente y trazar el agente son capas distintas.

**Si falla:**
- `401: el token no es válido` → vuelve a leer el token (cambia si reconstruiste).
- `No pude hablar con Hermes` → el puerto no es `8642`: `export HERMES_BASE_URL=http://127.0.0.1:<puerto>/v1`.
- Phoenix no muestra nada → `docker logs phoenix`; revisa que el puerto `6006` del contenedor esté en `127.0.0.1`.
- `python3 -m venv` falla → `sudo apt-get install -y python3-venv` `[VERIFICAR EN LAB]`.

Nunca publiques el puerto `6006` a internet: las trazas contienen las preguntas y respuestas completas.

---

## Receta 13 · Logs, política y bloqueos

**En la máquina:**

```bash
nemohermes mi-hermes logs --tail 50          # gateway + auditoría de OpenShell
nemohermes mi-hermes logs --follow           # en vivo; Ctrl+C para salir
nemohermes mi-hermes policy list             # presets activos (Hermes tiene su propia base)
openshell term                               # conexiones, bloqueos y estado de la inferencia
```

Una línea `DENIED` en los logs significa que OpenShell bloqueó una conexión de salida: es la política funcionando, igual que con OpenClaw.

---

## Receta 14 · Apaga, enciende y limpia

**En la máquina:**

```bash
docker stop phoenix && docker rm phoenix     # cuando ya no lo uses
nemohermes mi-hermes stop                    # detiene el sandbox y su dashboard
nemohermes mi-hermes start                   # lo vuelve a encender
nemoclaw my-assistant start                  # si detuviste el de OpenClaw
```

Para borrar el sandbox de Hermes **y todo su estado** (SOUL.md, memoria, skills, sesiones):

```bash
nemohermes mi-hermes destroy
```

`destroy` no se puede deshacer. Exporta antes las sesiones que quieras conservar (receta 10). Y recuerda detener la instancia de Brev al terminar (cookbook 4.1).
