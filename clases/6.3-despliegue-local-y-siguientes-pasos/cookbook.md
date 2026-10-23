# Cookbook · NemoClaw en tu propia máquina

Recetas para instalar y operar NemoClaw fuera de Brev: en Linux, macOS con Apple Silicon o Windows con WSL2.
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
- Con 8 GB de RAM, la subida de la imagen del sandbox (~2.4 GB comprimida) puede terminar con OOM (`exit 137`). Usa 16 GB o agrega al menos 4–8 GB de swap:
  ```bash
  sudo dd if=/dev/zero of=/swapfile bs=1M count=4096 && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile
  ```
- Node viejo: `nvm install 22 && nvm use 22`.

## Receta 1 · Prepara la plataforma

**Linux (Ubuntu):** el instalador puede instalar Docker por ti. Si ya lo tienes, asegúrate de estar en el grupo `docker`:
```bash
sudo usermod -aG docker $USER && newgrp docker
sudo apt-get install -y binutils     # 'strings', para verificar el binario de OpenShell
```

**macOS (Apple Silicon):**
```bash
xcode-select --install
brew install colima docker
colima start --cpu 4 --memory 8
docker info
```

**Windows:** en PowerShell, instala WSL2 y Ubuntu 24.04, y activa en Docker Desktop **Settings > Resources > WSL integration** para Ubuntu:
```powershell
wsl --install --no-distribution
wsl --install -d Ubuntu-24.04
```
Todo lo demás se corre **dentro de Ubuntu (WSL)**.

**Si falla:**
- macOS, el build se cuelga: Colima arranca con 2 vCPU / 2 GiB. `colima stop; colima start --cpu 6 --memory 12 --disk 100`.
- macOS, `docker: command not found` tras instalar Colima: `brew install colima docker`.
- WSL: "WSL 2 cannot start yet" o "not fully installed": reinicia y activa la virtualización y *Virtual Machine Platform*.
- WSL: `docker info` falla ("Cannot connect to the Docker daemon"): abre Docker Desktop, activa la integración WSL y corre `wsl --shutdown`.

## Receta 2 · Instala (la forma recomendada)
```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash
```
**Esperado:** el instalador muestra un aviso de software de terceros (acéptalo), instala OpenShell y NemoClaw, y lanza `nemoclaw onboard`. Sigue la etiqueta `lkg` (*last-known-good*).
En DGX Spark, DGX Station y WSL puede preguntar `Run express install with these settings? [Y/n]:` (inferencia local administrada, sandbox `my-assistant`, política Balanced). Para saltarlo: `NEMOCLAW_NO_EXPRESS=1`.

**Si falla:**
- `nemoclaw: command not found` al terminar: abre otra terminal o `source ~/.bashrc` (o `~/.zshrc`). Revisa que `~/.local/bin` esté en el `PATH`.
- `Node.js version` / el shell sigue en Node 20: `source "$NVM_DIR/nvm.sh" && nvm use 22`, o abre otra terminal.
- `Docker is not running` aunque corre: te falta el grupo `docker` (Receta 1).
- npm `EACCES`: no uses `sudo`. `npm config set prefix ~/.npm-global` y agrega `~/.npm-global/bin` al `PATH`.

## Receta 3 · Fija la versión (recomendado para el curso)
```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_REF= NEMOCLAW_INSTALL_TAG=vX.Y.Z bash
```
Cambia `vX.Y.Z` por la versión que quieras fijar. Como referencia, el laboratorio del curso usaba NemoClaw v0.0.135 con OpenShell 0.0.116; revisa en la documentación cuál recomiendan hoy.

> ⚠️ **Ojo:** Las variables van **del lado de `bash`** del pipe. `NEMOCLAW_INSTALL_TAG=... curl ... | bash` **no** funciona: la variable se la queda `curl`.

**Si falla:** `migration N was previously applied` / `is missing in the resolved migrations`: instalaste una etiqueta **más vieja** que la que ya tenías y OpenShell no se puede bajar de versión. Ver "migration" en la página de troubleshooting de NemoClaw; no fuerces la etiqueta vieja.

## Receta 4 · Instala sin onboarding y revisa el host
Útil si todavía no tienes la key o quieres revisar todo antes.
```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash -s -- --defer-onboarding
nemoclaw host probe            # reporte de preparación, solo lectura
nemoclaw doctor                # chequeos de host y gateway, solo lectura
```
**Esperado:** una lista de chequeos con su estado. El formato puede cambiar entre versiones.

**Si falla:** `host.docker.daemon_unreachable` → `sudo systemctl start docker` (Linux) o abre Docker Desktop / `colima start`.

## Receta 5 · Onboarding interactivo con NVIDIA Endpoints
```bash
export NVIDIA_INFERENCE_API_KEY=nvapi-xxxxxxxx     # tu key de build.nvidia.com
nemoclaw onboard
```
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
- `Sandbox 'my-assistant' was created but did not become ready within 180s.`: `export NEMOCLAW_SANDBOX_READY_TIMEOUT=600`, borra el sandbox retenido con `nemoclaw my-assistant destroy` y repite (no reintentes el mismo nombre sin borrarlo).
- Se cortó a la mitad: `nemoclaw onboard --resume` (o `--fresh` para empezar de cero).
- `Port 18789 is not available` / `Port 18080 is not available`: otro proceso usa el puerto (18789 es el chat de OpenClaw; 18080, el gateway de OpenShell). `nemoclaw onboard --control-ui-port 19000` o `NEMOCLAW_GATEWAY_PORT=<otro puerto> nemoclaw onboard`. Revisa con `sudo lsof -i :18789 -sTCP:LISTEN -P -n` (o `:18080`).
- La key es correcta pero `status` dice `unauthorized`: `nemoclaw credentials reset <PROVIDER>` y `nemoclaw onboard` otra vez.

## Receta 6 · Onboarding sin preguntas (para scripts)
```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | \
  NEMOCLAW_NON_INTERACTIVE=1 NEMOCLAW_ACCEPT_THIRD_PARTY_SOFTWARE=1 \
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

## Receta 10 · Día 2: después de reiniciar la máquina
```bash
sudo systemctl start docker && docker info     # o abre Docker Desktop / colima start
nemoclaw my-assistant status                   # también levanta el gateway
nemoclaw my-assistant start                    # si el sandbox estaba detenido
nemoclaw my-assistant recover                  # si el gateway o el reenvío siguen mal
```
**Si falla:** `sandbox_container_stopped` → `recover`; solo si falla, `nemoclaw my-assistant rebuild --yes` (conserva el home completo del agente).

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

---

## Errores comunes de la instalación local (resumen)

| Síntoma | Causa | Solución |
|---|---|---|
| `nemoclaw: command not found` | El `PATH` del shell actual no se actualizó | Terminal nueva o `source ~/.bashrc` |
| `Docker is not running` / `permission denied` en el socket | Tu usuario no está en el grupo `docker` | `sudo usermod -aG docker $USER && newgrp docker` |
| Exit 137 / OOM al subir la imagen | Menos de 8 GB de RAM libres | 16 GB o swap de 4–8 GB |
| La variable de entorno "no hace nada" | Quedó del lado de `curl` en el pipe | `curl ... \| VARIABLE=valor bash` |
| `did not become ready within 180s` | VM o disco lentos al primer arranque | `NEMOCLAW_SANDBOX_READY_TIMEOUT=600`, `destroy` y repetir |
| `Port 18789 is not available` (o `18080`) | Otro proceso (o un `ssh -L` viejo) usa el puerto | `--control-ui-port 19000` o mata el proceso viejo |
| `CONNECT tunnel failed, response 403` | La política bloqueó un host | `openshell term` (la OpenShell TUI: **[r]** reglas, **[a]** aprobar) o `nemoclaw <sb> policy add <preset>` |
| `openshell ... is above the maximum supported` | Se actualizó OpenShell por fuera | No uses `openshell self-update`; reinstala la versión soportada |
| El instalador rechaza la plataforma | Mac Intel o distro sin `apt` | Usa Linux Ubuntu, macOS Apple Silicon, WSL2 o Brev |
