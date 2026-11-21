# Cookbook · NemoClaw en tu propia máquina

Recetas para instalar y operar NemoClaw fuera de Brev. La ruta de macOS usa Apple Silicon, Colima y Docker; también hay alternativas para Linux y Windows con WSL2.
Es **opcional**: el curso se completa en Brev. Úsalo solo si quieres tu agente en tu propia máquina o en un servidor propio. Salvo la [receta previa](#receta-previa--respalda-tu-laboratorio-en-un-zip), que respalda tu laboratorio antes de borrarlo, nada de aquí depende de Brev: todo pasa en tu computadora.

> **Proyecto en *alpha*.** NemoClaw publica versiones cada 1 a 3 días. Fija una versión (Receta 3) y revisa la [documentación oficial](https://docs.nvidia.com/nemoclaw/latest/) antes de instalar. Las salidas cambian entre versiones: si la tuya muestra otro texto, compara la idea y sigue con el siguiente paso.

**Convenciones:** `my-assistant` es el nombre del sandbox (cámbialo por el tuyo). Las keys de ejemplo (`nvapi-xxxxxxxx`) son falsas.

Fuentes: documentación y repo de [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw) (prerequisites, quickstart, commands, troubleshooting) y la lección 04c del curso de NVIDIA DLI (Apache-2.0).

---

## Receta previa · Respalda tu laboratorio en un zip

Haz esto **antes de borrar tu instancia de Brev** si quieres quedarte con lo que tu agente guardó. Dentro del sandbox, `~` es `/sandbox`, así que `~/.openclaw` es la carpeta `/sandbox/.openclaw`. Ahí viven el workspace (`SOUL.md`, `USER.md`, `AGENTS.md`, `MEMORY.md`, `memory/`, `skills/` y lo que escribió tu agente), las tareas programadas (`cron/`) y el historial de conversaciones (`agents/`, `state/`).

El zip **deja fuera** dos cosas:

- **Lo que se reinstala solo:** paquetes de plugins (`npm/`, `extensions/`, `plugin-runtime-deps/`, `plugin-skills/`), `cache/`, `logs/` y `tmp/`. Pesan ≈380 MB y traen enlaces simbólicos que `download` no acepta.
- **Lo secreto:** `credentials/`, `identity/`, `devices/`, los archivos `.key` y `openclaw.json` (con sus copias `.bak`), que guardan el token del gateway y llaves de ese laboratorio. NemoClaw vuelve a escribir `openclaw.json` cuando creas un sandbox nuevo.

**Paso 1 · En el laboratorio.** Con la instancia encendida, abre la **VM TERMINAL** del tablero y pega:

```bash
# 1. Empaca ~/.openclaw dentro del sandbox, sin paquetes ni secretos
nemoclaw my-assistant exec -- tar czf /sandbox/.openclaw/tmp/respaldo.tgz -C /sandbox \
  --exclude=.openclaw/npm --exclude=.openclaw/cache --exclude=.openclaw/plugin-runtime-deps \
  --exclude=.openclaw/extensions --exclude=.openclaw/plugin-skills --exclude=.openclaw/logs \
  --exclude=.openclaw/tmp --exclude=.openclaw/credentials --exclude=.openclaw/identity \
  --exclude=.openclaw/devices --exclude='*.key' --exclude='.openclaw/openclaw.json*' .openclaw

# 2. Pásalo del sandbox a la VM y borra la copia que quedó en el sandbox
nemoclaw my-assistant download /sandbox/.openclaw/tmp/respaldo.tgz ~/
nemoclaw my-assistant exec -- rm /sandbox/.openclaw/tmp/respaldo.tgz

# 3. Conviértelo en zip (la VM no trae el comando zip; Python sí)
rm -rf ~/respaldo && mkdir ~/respaldo && tar xzf ~/respaldo.tgz -C ~/respaldo
mv ~/respaldo/.openclaw ~/respaldo/openclaw
cd ~/respaldo && python3 -m zipfile -c ~/openclaw-respaldo.zip openclaw && cd ~
ls -lh ~/openclaw-respaldo.zip
```

**Esperado:** `✓ Download complete` después del paso 2 y, al final, un archivo `/home/ubuntu/openclaw-respaldo.zip` de cientos de KB (en nuestra prueba, 731K). Las líneas `ExperimentalWarning: SQLite …` no son errores.

**Paso 2 · En tu computadora.** La consola web de Brev no tiene botón de descarga: el archivo se baja con la **Brev CLI**. Instálala una vez:

- **macOS:** `brew install brevdev/homebrew-brev/brev`
- **Linux:** `bash -c "$(curl -fsSL https://raw.githubusercontent.com/brevdev/brev-cli/main/bin/install-latest.sh)"`
- **Windows:** la Brev CLI solo funciona dentro de WSL (Ubuntu). Si no quieres instalar WSL, usa el plan B de abajo.

Luego, en una terminal de tu computadora, dentro de la carpeta donde quieras guardar el zip:

```bash
brev login     # escribe tu correo y termina el inicio de sesión en el navegador
brev ls        # muestra el nombre de tu instancia, por ejemplo nemoclaw-4c4e92
brev copy nemoclaw-xxxxxx:/home/ubuntu/openclaw-respaldo.zip ./
```

Cambia `nemoclaw-xxxxxx` por el nombre de tu instancia. La consola de Brev muestra el mismo comando en **Compute → tu instancia → Access → Copy Files**, eligiendo **Download**.

**Esperado:** unos segundos de `waiting for SSH connection to be available` y luego `✓ Successfully copied nemoclaw-xxxxxx:/home/ubuntu/openclaw-respaldo.zip → ./`. Al abrir el zip verás una carpeta `openclaw/` con `workspace/`, `agents/`, `cron/`, `memory/`, `skills/` y `state/`. La primera vez, Brev agrega a tu `~/.ssh/config` una línea `Include` que apunta a su propia configuración.

**Cuídalo como algo privado:** `agents/` y `state/` guardan todo lo que le escribiste al agente. No lo subas a un repositorio público.

**Plan B, sin instalar nada:** si solo quieres tus textos (`SOUL.md`, los reportes del agente), muéstralos en la VM TERMINAL y cópialos con el mouse, como en [LABORATORIO.md · Al terminar](../../LABORATORIO.md#5--al-terminar).

**Para usarlo después:** descomprime el zip y sube a tu sandbox nuevo (local, Receta 8, o en otro laboratorio) solo lo que quieras, archivo por archivo, por ejemplo `nemoclaw my-assistant upload ./openclaw/workspace/SOUL.md /sandbox/.openclaw/workspace/`. No subas `POLICY.md`: NemoClaw lo escribe solo. Más detalle en [NemoClaw · Transfer State Manually](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/manage-sandboxes/state-and-backups/transfer-state-manually).

**Si falla:**
- `sandbox source path … is outside the sandbox workspace (/sandbox)`: `download` solo acepta rutas dentro de `/sandbox`. Por eso el paquete se arma en `/sandbox/.openclaw/tmp/`, no en `/tmp`.
- `rate limit exceeded` justo después de `Successfully logged in`: el inicio de sesión ya quedó; sigue con `brev ls`.
- `brev copy` se queda esperando o no encuentra la instancia: la instancia tiene que estar **Running**. Si la detuviste, presiona **Start** en la consola, espera a que diga Running y repite.
- `brev: command not found`: abre una terminal nueva después de instalar.

---

## Receta 0 · ¿Tu máquina sirve?

| Recurso | Mínimo | Recomendado |
|---|---|---|
| CPU | 4 vCPU | 4+ vCPU |
| RAM | 8 GB | **16 GB** |
| Disco libre | 20 GB | 40 GB |
| Software | Docker (o Docker Desktop / Colima), Node.js **22.19+** y npm 10+ | |

| Plataforma | Estado |
|---|---|
| Linux Ubuntu 24.04 (Docker) | Probado, plataforma principal |
| DGX Spark (DGX OS) | Probado |
| macOS Apple Silicon (Colima o Docker Desktop) | Probado con limitaciones |
| Windows con WSL2 (Docker Desktop, backend WSL) | Probado con limitaciones |
| **Mac Intel**, distros sin `apt` (Fedora…), Kubernetes, multiusuario | **No soportado** |

La GPU es **opcional** si usas inferencia alojada (NVIDIA Endpoints). La necesitas para NIM local o vLLM.

```bash
# Linux / WSL2
nproc; free -h; df -h ~
docker info >/dev/null && echo "Docker OK"
node --version          # v22.19.0 o mayor
# macOS
sysctl -n hw.ncpu; sysctl -n hw.memsize; df -h ~
```
**Si falla:**
- Una VM con poca RAM puede terminar con OOM (`exit 137`) aunque el Mac tenga más memoria. Revisa la capacidad del motor con `docker info`, además de los recursos del host. Si aumentas la RAM de Colima, deja margen para macOS. Para un host Linux con memoria insuficiente, consulta el swap de al menos 8 GB de los [requisitos oficiales](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/get-started/prerequisites). Los comandos de swap de Linux no aplican a macOS.
- Node viejo: `nvm install 22 && nvm use 22`.

## Receta 1 · Prepara la plataforma

**Linux (Ubuntu):** el instalador puede instalar Docker por ti. Si ya lo tienes, asegúrate de estar en el grupo `docker`:
```bash
sudo usermod -aG docker $USER && newgrp docker
sudo apt-get install -y binutils     # 'strings', para verificar el binario de OpenShell
```

**macOS (Apple Silicon):**

Instala [Homebrew](https://brew.sh/) si te falta. Si faltan las herramientas de Xcode, ejecuta `xcode-select --install` y termina el diálogo. Colima crea la VM Linux y su motor Docker; el paquete `docker` instala el cliente. Docker Desktop es una alternativa, pero esta receta usa Colima.

```bash
brew install colima docker
colima start --cpu 4 --memory 12 --disk 100
unset DOCKER_HOST DOCKER_CONTEXT
docker context use colima
colima status
docker info --format 'CPUs={{.NCPU}} MemoryBytes={{.MemTotal}}'
```

**Esperado:** Colima en ejecución, 4 CPUs y cerca de 12 GiB para Docker. Es el ejemplo usado en un Mac de 18 GiB; ajusta los recursos para dejar memoria al host. `--disk 100` configura el tamaño del disco virtual, pero las imágenes necesitan espacio real en el Mac. Revisa `df -h ~`. Si la VM ya corre y vas a cambiar sus recursos, detenla primero con `colima stop`.

Si Docker funciona pero NemoClaw u OpenShell no encuentran el motor, selecciona el socket en esa misma terminal:

```bash
unset DOCKER_CONTEXT
export DOCKER_HOST="unix://${HOME}/.colima/default/docker.sock"
docker info
```

El `export` identifica el motor para los clientes que no usan el contexto seleccionado. No reinstala Docker ni cambia los recursos de la VM. Dura en esa sesión de terminal; repítelo cuando haga falta. Para otro perfil, usa el socket que muestra `colima status`. Antes de cambiar a Docker Desktop, ejecuta `unset DOCKER_HOST DOCKER_CONTEXT` y elige su contexto con `docker context use`. Consulta la [FAQ de Colima](https://colima.run/docs/faq/#where-is-the-docker-socket-located).

**Windows:** en PowerShell, instala WSL2 y Ubuntu 24.04, y activa en Docker Desktop **Settings > Resources > WSL integration** para Ubuntu:
```powershell
wsl --install --no-distribution
wsl --install -d Ubuntu-24.04
```
Todo lo demás se corre **dentro de Ubuntu (WSL)**.

**Si falla:**
- macOS, el build se cuelga: revisa los recursos de Docker y el espacio del host antes de cambiar límites. Aumentar el timeout no corrige la falta de RAM o disco.
- macOS, `docker: command not found` tras instalar Colima: `brew install colima docker`.
- WSL: "WSL 2 cannot start yet" o "not fully installed": reinicia y activa la virtualización y *Virtual Machine Platform*.
- WSL: `docker info` falla ("Cannot connect to the Docker daemon"): abre Docker Desktop, activa la integración WSL y corre `wsl --shutdown`.

## Receta 2 · Instala (la forma recomendada)

Para la VM de Colima de la Receta 1, crea el sandbox con 3 CPUs y 8 GiB. Esto deja capacidad a la VM y sus servicios. Usa valores que quepan en el motor si elegiste otros recursos.

```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | \
  NEMOCLAW_AGENT=openclaw NEMOCLAW_CPU=3 NEMOCLAW_RAM=8Gi bash
```

En otra plataforma, puedes usar el instalador sin esos límites y elegir los recursos durante el onboarding. Las variables van del lado de `bash`. Si fijas una versión con la Receta 3, agrega allí los mismos límites para Colima.

**Esperado:** el instalador muestra un aviso de software de terceros (acéptalo), instala OpenShell y NemoClaw, y lanza `nemoclaw onboard`. Sigue la etiqueta `lkg` (*last-known-good*).
En DGX Spark, DGX Station y WSL puede preguntar `Run express install with these settings? [Y/n]:` (inferencia local administrada, sandbox `my-assistant`, política Balanced). Para saltarlo: `NEMOCLAW_NO_EXPRESS=1`.

**Si falla:**
- `nemoclaw: command not found` al terminar: abre otra terminal o `source ~/.bashrc` (o `~/.zshrc`). Revisa que `~/.local/bin` esté en el `PATH`.
- `Node.js version` / el shell sigue en Node 20: `source "$NVM_DIR/nvm.sh" && nvm use 22`, o abre otra terminal.
- `Docker is not running`: en macOS, revisa Colima, el contexto y el socket; en Linux, revisa el servicio y los permisos del grupo `docker` (Receta 1).
- npm `EACCES`: no uses `sudo`. `npm config set prefix ~/.npm-global` y agrega `~/.npm-global/bin` al `PATH`.

## Receta 3 · Fija la versión (recomendado para el curso)
```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_REF= NEMOCLAW_INSTALL_TAG=vX.Y.Z bash
```
Cambia `vX.Y.Z` por la versión que quieras fijar. Como referencia, el laboratorio del curso usaba NemoClaw v0.0.135 con OpenShell 0.0.116; revisa en la documentación cuál recomiendan hoy.

> ⚠️ **Ojo:** Las variables van **del lado de `bash`** del pipe. `NEMOCLAW_INSTALL_TAG=... curl ... | bash` **no** funciona: la variable se la queda `curl`.

**Si falla:** `migration N was previously applied` / `is missing in the resolved migrations`: instalaste una etiqueta **más vieja** que la que ya tenías y OpenShell no se puede bajar de versión. Ver "migration" en la página de troubleshooting de NemoClaw; no fuerces la etiqueta vieja.

## Receta 4 · Revisa el host y conoce el onboarding diferido

Para OpenClaw, usa la instalación interactiva de la Receta 2. Con NemoClaw instalado, estos comandos revisan la preparación:

```bash
nemoclaw host probe
nemoclaw doctor
```
**Esperado:** una lista de chequeos con su estado. El formato puede cambiar entre versiones.

`--defer-onboarding` está documentado para Hermes y LangChain Deep Agents Code con el proveedor NVIDIA alojado, cuando faltan credenciales y no hay un sandbox registrado. No es el paso de instalación de OpenClaw. Consulta las condiciones en la [referencia del instalador](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands#--defer-onboarding).

**Si falla:** `host.docker.daemon_unreachable` → `sudo systemctl start docker` (Linux) o abre Docker Desktop / `colima start`.

## Receta 5 · Onboarding interactivo con NVIDIA Endpoints

Si NemoClaw ya está instalado, usa estos límites para la VM de Colima de 4 CPUs y 12 GiB. En otra plataforma, ajusta los valores a la capacidad disponible.

```bash
NEMOCLAW_CPU=3 NEMOCLAW_RAM=8Gi nemoclaw onboard --name my-assistant
```
Introduce la key cuando la pida el asistente. Si la proporcionas por variable de entorno, usa `NVIDIA_INFERENCE_API_KEY` y no guardes la key real en el historial.

**Por qué 3 CPUs si Colima tiene 4:** Colima limita la VM completa; `NEMOCLAW_CPU` y `NEMOCLAW_RAM` limitan el sandbox dentro de ella. El margen queda para Docker y otros procesos. En v0.0.145 observamos que el perfil developer calculaba el 75 % sobre el Mac de 12 CPUs/18 GiB y solicitaba 9 CPUs/13Gi a Docker. Los valores explícitos evitan esa solicitud imposible. El [issue #14743](https://github.com/NVIDIA/NemoClaw/issues/14743) documenta el error, el parche propuesto y las pruebas; no asumas que tu versión instalada ya lo contiene.

El asistente hace: preflight → gateway de OpenShell → agente y proveedor → credencial → nombre del sandbox → revisión (`1 Apply / 2 Edit provider / 3 Edit name / 4 Exit`) → canales opcionales → nivel de política → chequeos finales.

Menú de proveedores:
```
  1) NVIDIA Endpoints
  2) OpenRouter
  3) OpenAI
  4) Other OpenAI-compatible endpoint
  5) Anthropic
  6) Other Anthropic-compatible endpoint
  7) Google Gemini
  8) Local Ollama (localhost:11434)
  9) Model Router (experimental)
  Choose [1]:
```
Elige **1**. Para la política, deja **Balanced** (la opción por defecto). **Personal** abre cualquier host en 80/443 sin aprobaciones: no la uses para un agente que lee contenido de desconocidos.

**Esperado:** el resumen `NemoClaw is ready` con estas líneas (abreviado):
```
Browser:  http://127.0.0.1:18789/
Terminal: nemoclaw launch my-assistant
Status:   nemoclaw my-assistant status
Logs:     nemoclaw my-assistant logs --follow
```

**Si falla:**
- `Invalid sandbox name` (y sugiere `Try: <slug>`): 1–19 caracteres, minúsculas, empieza con letra, guiones simples. Nombres reservados: `onboard`, `list`, `status`, `start`, `stop`, `debug`, `help`…
- `Sandbox 'my-assistant' was created but did not become ready within 180s.`: consulta `nemoclaw debug --quick` y los logs antes de actuar. Si Docker rechaza la cantidad de CPUs, corrige los límites como se indica abajo. Usa `NEMOCLAW_SANDBOX_READY_TIMEOUT=600` solo cuando la causa sea un arranque lento; esperar más no corrige límites inválidos.
- Se cortó a la mitad por una desconexión: resuelve la conexión y usa `nemoclaw onboard --resume`. Evita destruir el sandbox como primer paso.
- `Port 18789 is not available` / `Port 18080 is not available`: otro proceso usa el puerto (18789 es el chat de OpenClaw; 18080, el gateway de OpenShell). `nemoclaw onboard --control-ui-port 19000` o `NEMOCLAW_GATEWAY_PORT=<otro puerto> nemoclaw onboard`. Revisa con `sudo lsof -i :18789 -sTCP:LISTEN -P -n` (o `:18080`).
- La key es correcta pero `status` dice `unauthorized`: `nemoclaw credentials reset <PROVIDER>` y `nemoclaw onboard` otra vez.

Para un intento nuevo después del error de CPU, conserva el sandbox anterior y elige un nombre que no exista:

```bash
NEMOCLAW_CPU=3 NEMOCLAW_RAM=8Gi \
  nemoclaw onboard --fresh --name my-assistant-fixed
```

`--fresh` descarta el checkpoint del onboarding. No cambia los límites de un sandbox existente ni libera su nombre. En adelante, sustituye `my-assistant` por `my-assistant-fixed` si usaste ese nombre. No borres Colima para resolver este error. Antes de eliminar un sandbox fallido, comprueba si contiene datos que quieras conservar.

## Receta 6 · Onboarding sin preguntas (para scripts)

Los límites de este ejemplo corresponden a la VM de Colima de la Receta 1. Ajusta ambos si usas otra capacidad.

```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | \
  NEMOCLAW_NON_INTERACTIVE=1 NEMOCLAW_ACCEPT_THIRD_PARTY_SOFTWARE=1 \
  NEMOCLAW_CPU=3 NEMOCLAW_RAM=8Gi \
  NEMOCLAW_AGENT=openclaw NEMOCLAW_PROVIDER=build \
  NVIDIA_INFERENCE_API_KEY=nvapi-xxxxxxxx NEMOCLAW_SANDBOX_NAME=my-assistant bash
```
Para otro agente: `NEMOCLAW_AGENT=hermes` o `NEMOCLAW_AGENT=langchain-deepagents-code`.

**Si falla:** el modo no interactivo se niega a seguir tras un intento fallido → agrega `--fresh` (`... | bash -s -- --fresh`) o `NEMOCLAW_FRESH=1`.

> ⚠️ **Ojo:** No dejes este comando con tu key real en el historial de la shell ni en un script versionado. Exporta la key desde un gestor de secretos o escríbela solo en la terminal.

## Receta 7 · Día 1: usa tu agente
```bash
nemoclaw my-assistant status                  # salud, prueba de inferencia, política
nemoclaw my-assistant dashboard-url --quiet   # URL del dashboard con token: trátala como contraseña
nemoclaw launch my-assistant                  # preflight + chat en la terminal (openclaw tui)
nemoclaw my-assistant connect                 # shell dentro del sandbox; luego: openclaw tui
nemoclaw my-assistant logs --follow           # logs en vivo
openshell status                              # el gateway de OpenShell (puerto 18080)
```
**Esperado:** en el navegador, `http://127.0.0.1:18789/` abre el dashboard de OpenClaw. `openshell status` muestra el gateway en `https://127.0.0.1:18080` y `Connected`.

**Si falla:**
- Servidor remoto o sin pantalla: el dashboard escucha solo en `127.0.0.1`. Desde tu laptop: `ssh -L 18789:127.0.0.1:18789 <usuario>@<servidor>` y abre `http://127.0.0.1:18789/`.
- "Pairing required" en el dashboard: espera unos minutos y recarga. Si sigue, en `nemoclaw my-assistant connect` corre `openclaw devices list --json` y `openclaw devices approve <requestId>`.

## Receta 8 · Lleva tu proyecto al sandbox local
```bash
# desde la raíz del repo del curso
nemoclaw my-assistant skill install ./skill-library/soporte-nemoclaw/
nemoclaw my-assistant skill install ./skill-library/diagnostico-api/
nemoclaw my-assistant skill install ./skill-library/lector-seguro-archivos/
nemoclaw my-assistant skill install ./skill-library/resumen-diario/
nemoclaw my-assistant skill list
nemoclaw my-assistant upload ./datos/faq/ /sandbox/.openclaw/workspace/
nemoclaw my-assistant exec -- ls /sandbox/.openclaw/workspace/faq   # deben verse los .md dentro de faq/
```
**Esperado:** las 4 skills en `skill list` y los `.md` de la FAQ dentro de `workspace/faq/`. Ojo: si el destino ya termina en `faq/`, `upload` crea `faq/faq/`; por eso subimos a `workspace/`. Abre una **sesión nueva** y pregunta: *"¿Cómo detengo mi instancia de Brev?"*

**Si falla:** el agente no usa la skill → revisa la description (clase 6.2) y que estés en una sesión nueva.

## Receta 9 · Cambia el proveedor de inferencia

| Proveedor | Cómo | Notas |
|---|---|---|
| **NVIDIA Endpoints** | Opción 1 del onboarding · `NEMOCLAW_PROVIDER=build` | Key en `NVIDIA_INFERENCE_API_KEY`. Lo más simple; sin GPU |
| **Ollama local** | Opción 8 · `NEMOCLAW_PROVIDER=ollama` | Modelos validados: `qwen3.6:35b`, `nemotron-3-nano:30b`, `qwen3.5:9b` |
| **vLLM** ya corriendo en `localhost:8000` | `NEMOCLAW_PROVIDER=vllm` | Con limitaciones. Debe devolver `tool_calls` estructurados |
| **NIM local** | `NEMOCLAW_EXPERIMENTAL=1` + `NEMOCLAW_PROVIDER=nim-local` | **Experimental.** GPU NVIDIA, Container Toolkit, CDI y login en NGC |

Ollama, paso a paso:
```bash
ollama pull qwen3.5:9b
OLLAMA_CONTEXT_LENGTH=16384 ollama serve      # en otra terminal; Hermes necesita 64000
nemoclaw onboard                               # elige 8) Local Ollama
```
Cambiar el modelo dentro del mismo proveedor:
```bash
nemoclaw inference get
nemoclaw inference set --provider nvidia-prod --model nvidia/nemotron-3-super-120b-a12b --sandbox my-assistant
```

**Si falla:**
- `Error: listen tcp 127.0.0.1:11434: bind: address already in use`: ya hay un Ollama corriendo como servicio. `sudo systemctl stop ollama` y vuelve a lanzar `ollama serve` con el contexto que quieres.
- Las llamadas a herramientas salen como texto (JSON en la respuesta): tu servidor local no devuelve `tool_calls` estructurados. Usa otro modelo o servidor.
- Timeouts con modelos locales: `export NEMOCLAW_LOCAL_INFERENCE_TIMEOUT=300` (por defecto 180 s).
- `Local NIM unavailable — no GPU detected`: NIM local necesita una GPU NVIDIA real. Usa NVIDIA Endpoints u Ollama.

## Receta 10 · Detén Colima y vuelve después

Para detener solo un sandbox y dejar el motor disponible:

```bash
nemoclaw my-assistant stop
```

Para apagar la VM y todos sus contenedores al terminar:

```bash
colima stop
colima status
```

**Esperado:** Colima indica que no está corriendo. La VM y sus contenedores dejan de consumir CPU y RAM; sus archivos permanecen en disco. El gateway de OpenShell puede correr como servicio de macOS fuera de la VM. Ollama y los túneles también pueden seguir activos en el host. Revisa el Monitor de Actividad y `brew services list`; detén esos procesos con el gestor que los inició si también quieres apagarlos.

Para volver, Colima reutiliza los recursos guardados:

```bash
colima start
docker info
nemoclaw my-assistant status
```

Restaura `DOCKER_HOST` antes de `docker info` si esta terminal necesita el socket de la Receta 1. Si el sandbox está detenido, ejecuta `nemoclaw my-assistant start`. Si queda sin responder, revisa el estado y usa `nemoclaw my-assistant recover`. `status` puede levantar servicios de apoyo: para verificar que Colima siga apagado, usa `colima status`.

En Linux, inicia el motor con `sudo systemctl start docker`; en WSL con Docker Desktop, abre Docker Desktop. Después aplica los mismos comandos del sandbox. Un reinicio normal no requiere repetir el onboarding.

> ⚠️ **Ojo:** `nemoclaw start` y `nemoclaw stop` **globales** están obsoletos desde v0.0.110. Usa siempre `nemoclaw <sandbox> start|stop`.

## Receta 11 · Día 2: actualizar sin romper nada
```bash
nemoclaw backup-all                         # respaldo de todos los sandboxes
nemoclaw update --check                     # ¿hay versión nueva?
nemoclaw update                             # vuelve a correr el instalador (lkg)
nemoclaw upgrade-sandboxes --check
nemoclaw upgrade-sandboxes --auto           # reconstruye los que tengan imagen vieja
```
> ⛔ **Nunca** corras `openshell self-update` ni `npm update -g openshell` en el host, ni `openclaw update` dentro del sandbox. NemoClaw fija una versión exacta de OpenShell (0.0.116 hoy) y de OpenClaw en la imagen.

**Si falla:**
- `✗ openshell <versión> is above the maximum supported by this NemoClaw release.`: alguien actualizó OpenShell por fuera. Actualiza NemoClaw o reinstala la versión de OpenShell soportada.
- `Sandbox is running an outdated agent version`: `nemoclaw my-assistant rebuild`.

## Receta 12 · Limpieza y desinstalación

Para terminar el día usa `colima stop`, como indica la Receta 10. Los comandos siguientes son operaciones independientes de limpieza: elige solo la que necesitas. `destroy` elimina el sandbox y su estado; respalda lo que quieras conservar antes de ejecutarlo. `colima delete` tampoco es un paso del apagado cotidiano.

```bash
nemoclaw gc --dry-run                        # imágenes huérfanas que se borrarían
nemoclaw gc
nemoclaw my-assistant destroy --yes          # borra un sandbox (y su estado)
nemoclaw uninstall --yes                     # quita NemoClaw; --keep-openshell para conservar OpenShell
```
**Si falla:** `uninstall` o `list` bloqueados tras un onboarding interrumpido: queda un `onboard.lock` en `~/.nemoclaw/`. Revisa que no haya otro `nemoclaw` corriendo antes de borrarlo.

## Receta 13 · Reporta un problema bien
```bash
nemoclaw --version
nemoclaw debug --quick --output /tmp/nemoclaw-debug.tar.gz
```
Abre un issue en [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw/issues) con: plataforma, versión, comando exacto, mensaje de error completo y el archivo de `debug`. Antes de subirlo, revisa que no tenga keys ni URLs con `#token=`.

Para un problema con Colima, agrega `colima version`, `colima status` y `docker info --format 'CPUs={{.NCPU}} MemoryBytes={{.MemTotal}}'`. Distingue los recursos del Mac de los que ve Docker. Consulta primero los issues existentes, como el [error de perfiles porcentuales #14743](https://github.com/NVIDIA/NemoClaw/issues/14743).

---

## Errores comunes de la instalación local (resumen)

| Síntoma | Causa | Solución |
|---|---|---|
| `nemoclaw: command not found` | El `PATH` del shell actual no se actualizó | Terminal nueva o `source ~/.bashrc` |
| Docker no conecta en macOS | Colima detenido, contexto o socket incorrectos | Receta 1: revisa Colima y el contexto; usa `DOCKER_HOST` si hace falta |
| Docker no conecta en Linux | Servicio detenido o permisos del socket | Revisa el servicio y el grupo `docker` como indica la Receta 1 |
| Exit 137 / OOM al subir la imagen | Falta de RAM en la VM o el host | Revisa ambos recursos; el swap de Linux no aplica al Mac |
| Docker rechaza la cantidad de CPUs | El perfil calculó el porcentaje sobre el host | Receta 5: límites explícitos que quepan en la VM y un nombre nuevo |
| La variable de entorno "no hace nada" | Quedó del lado de `curl` en el pipe | `curl ... \| VARIABLE=valor bash` |
| `did not become ready within 180s` | El timeout es un síntoma; consulta los logs | Corrige primero la causa. Solo aumenta el timeout si el arranque es lento |
| `Port 18789 is not available` (o `18080`) | Otro proceso (o un `ssh -L` viejo) usa el puerto | `--control-ui-port 19000` o mata el proceso viejo |
| `CONNECT tunnel failed, response 403` | La política bloqueó un host | `openshell term` (la OpenShell TUI: **[r]** reglas, **[a]** aprobar) o `nemoclaw <sb> policy add <preset>` |
| `openshell ... is above the maximum supported` | Se actualizó OpenShell por fuera | No uses `openshell self-update`; reinstala la versión soportada |
| El instalador rechaza la plataforma | Mac Intel o distro sin `apt` | Usa Linux Ubuntu, macOS Apple Silicon, WSL2 o Brev |
