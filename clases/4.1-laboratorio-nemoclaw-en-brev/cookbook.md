# Cookbook 4.1 · Brev y NemoClaw desde la terminal

Recetas para desplegar, conectarte, revisar y pausar tu laboratorio NemoClaw en Brev. Sirven igual fuera del curso: cualquier launchable de NemoClaw o máquina de Brev funciona así.

Convenciones:
- `<instancia>` es el nombre de tu instancia en Brev (lo ves con `brev ls`).
- `my-assistant` es el nombre habitual del sandbox del launchable. Si `nemoclaw list` muestra otro, úsalo en su lugar. `[VERIFICAR EN LAB]`
- **En tu computadora** = terminal local. **En la máquina** = dentro de `brev shell <instancia>`.

Basado en la lección 03a-kickstart del curso de NVIDIA DLI (Apache-2.0), la documentación de Brev y la de NemoClaw.

---

## Receta 1 · Instala la CLI de Brev

**En tu computadora:**

```bash
# macOS (Homebrew)
brew install brevdev/homebrew-brev/brev

# Linux o WSL: instala en ~/.local/bin. NO uses sudo.
bash -c "$(curl -fsSL https://raw.githubusercontent.com/brevdev/brev-cli/main/bin/install-latest.sh)"
export PATH="$HOME/.local/bin:$PATH"     # si brev no aparece

brev --version
```

Salida esperada: un número de versión, por ejemplo `v0.6.335`.

Windows: la CLI solo corre dentro de WSL. En PowerShell como administrador:

```powershell
wsl --install -d Ubuntu-22.04
```

Reinicia, abre Ubuntu y corre el instalador de Linux. WSL necesita la virtualización (VT-x/AMD-V) activada en el BIOS.

**Si falla:**
- `Error: Failed to fetch release info from GitHub API.` → límite de la API de GitHub (60 llamadas por hora por IP; pasa mucho con VPN). Apaga o cambia la VPN, o exporta un token: `export GITHUB_TOKEN=<tu-token>` y repite.
- `brev: command not found` → falta `~/.local/bin` en tu `PATH`. Agrega el `export` de arriba a tu `~/.bashrc` o `~/.zshrc`.

---

## Receta 2 · Inicia sesión y elige la organización correcta

**En tu computadora:**

```bash
brev login                 # abre el navegador con tu cuenta de NVIDIA
brev ls orgs               # lista tus organizaciones
brev set <org>             # activa la organización que tiene los créditos
```

Salida esperada: `brev login` termina sin errores y crea la carpeta `~/.brev/` (llave SSH `brev.pem`, `ssh_config` y `credentials.json`).

**Si falla:**
- El navegador no termina el login → `brev login --skip-browser` imprime la URL para abrirla a mano. Si sigue, borra las cookies de `brev.nvidia.com` y repite.
- `You have run out of credits ...` aunque tienes saldo → estás en otra organización. Corre `brev ls orgs` y `brev set <org>`.
- Errores feos o un stack trace más adelante → `brev logout && brev login`.

---

## Receta 3 · Encuentra tu instancia

**En tu computadora:**

```bash
brev ls
brev ls --json             # misma información, para scripts
```

Salida esperada: una fila con tu instancia. Los estados posibles son `RUNNING`, `STARTING`, `STOPPING`, `DEPLOYING`, `STOPPED`, `DELETING` y `FAILURE`.

**Si falla:**
- No aparece la instancia que creaste desde la consola → `brev refresh` sincroniza la lista y reescribe `~/.brev/ssh_config`.
- Se queda en `DEPLOYING` mucho tiempo, o ves `rpc error: ... context deadline exceeded` → revisa la pestaña **Activity Logs** en la consola. Si no avanza, elimínala, espera 30 segundos y despliega otra (con otro nombre). Antes de reintentar, confirma con `brev ls` que no quedaron dos instancias: pagarías doble.

---

## Receta 4 · (Opcional) Despliega el launchable desde la CLI

Es lo mismo que el botón de la consola. **Crea una instancia que se cobra**: no lo corras si ya tienes una.

**En tu computadora:**

```bash
brev create <instancia> --launchable env-3Azt0aYgVNFEuz7opyx3gscmowS --detached --timeout 900
brev ls
```

Salida esperada: la instancia aparece en `DEPLOYING` y pasa a `RUNNING`. El CI de NemoClaw espera hasta 900 segundos.

**Si falla:**
- `unexpected EOF` o *deadline exceeded* → puede que sí se haya creado. Corre `brev ls` antes de repetir.
- `build_status=CREATE_FAILED` pero la máquina responde → bug conocido de Brev: el estado se queda pegado. Prueba la receta 5.

---

## Receta 5 · Entra a la máquina y revisa el stack

**En tu computadora:**

```bash
brev shell <instancia>          # alias: brev ssh <instancia>. SIN --host
```

**En la máquina:**

```bash
nemoclaw list                   # sandboxes registrados, con modelo y proveedor
nemoclaw status                 # inventario del gateway de OpenShell y servicios auxiliares
openshell sandbox list          # estado crudo de los sandboxes
nemoclaw my-assistant status    # salud del sandbox, prueba de inferencia y política
```

Salida esperada:
- `nemoclaw list` muestra `my-assistant` con su modelo (en el launchable, Nemotron 3 Super 120B) y proveedor.
- `openshell sandbox list` muestra la fila en `Ready` (o `Running`). `NotReady` no cuenta.
- `nemoclaw my-assistant status` reporta la inferencia como `healthy`.

`[VERIFICAR EN LAB: salida exacta de los cuatro comandos]`

**Si falla:**
- `brev shell <instancia> --host` se queda esperando → quita `--host`.
- `brev shell` se queda en "waiting for instance to be ready" aunque la consola dice listo → `brev refresh` y luego `ssh <instancia>`.
- `ssh: connect ... port 22: Connection refused` → ¿está en `RUNNING`? (`brev ls`). Si acabas de reanudar, la IP cambió: `brev refresh`.
- `ssh: Could not resolve hostname <instancia>` → receta 12.
- `Permission denied (publickey)` en macOS → la llave `~/.brev/brev.pem` está dañada. `brev login --token` con el token de https://brev.nvidia.com/settings/cli, o respalda la llave, regenérala, `chmod 600 ~/.brev/brev.pem` y `brev login`.
- La inferencia sale `unauthorized` → la key del proveedor fue rechazada (401/403). Es un problema de credencial, no de red: genera otra key en build.nvidia.com.
- `nemoclaw: command not found` → abre una terminal nueva o corre `source ~/.bashrc`.

---

## Receta 6 · Un turno de agente desde la terminal

Equivale al paso 14 de la página del curso, pero sin navegador.

**En la máquina:**

```bash
# Comandos crudos dentro del sandbox, como el usuario sandbox
nemoclaw my-assistant exec -- whoami
nemoclaw my-assistant exec -- pwd

# Un turno completo del agente (OpenClaw), sin interfaz
nemoclaw my-assistant agent --agent main -m "Usa tu herramienta exec para ejecutar whoami y pwd y dime en una frase qué usuario eres y dónde estás."
```

Salida esperada: `exec` imprime `sandbox` y `/sandbox`. El turno del agente responde algo como "Soy el usuario sandbox y estoy en /sandbox". `[VERIFICAR EN LAB]`

Observa la diferencia: `exec` lo corres tú, como operador. En `agent`, el modelo **decide** usar su herramienta `exec`.

**Si falla:**
- `agent` exige un selector: `--agent`, `--session-id`, `--session-key` o `--to`. Sin uno de ellos, el wrapper se niega.
- El turno se cuelga y nunca usa `exec` → `toolSearch` activado. Corre la **Comprobación de estado** de la página del curso, o revisa los logs (receta 10).

---

## Receta 7 · Prueba que la memoria vive en la clave de sesión

**En la máquina:**

```bash
# 1. Planta un dato en la sesión "prueba-41"
nemoclaw my-assistant agent --session-key prueba-41 -m "Recuerda este código solo en nuestra conversación: CODE-7319. No lo escribas en un archivo."

# 2. Pregunta en la MISMA sesión
nemoclaw my-assistant agent --session-key prueba-41 -m "¿Qué código te di antes? Si no lo sabes, di 'unknown'. No leas archivos."

# 3. Pregunta en OTRA sesión
nemoclaw my-assistant agent --session-key prueba-41-b -m "¿Qué código te di antes? Si no lo sabes, di 'unknown'. No leas archivos."

# 4. Restablece la primera sesión y pregunta otra vez
nemoclaw my-assistant sessions reset prueba-41 --agent main
nemoclaw my-assistant agent --session-key prueba-41 -m "¿Qué código te di antes? Si no lo sabes, di 'unknown'. No leas archivos."
```

Salida esperada: el paso 2 recuerda `CODE-7319`; el 3 y el 4 responden `unknown`. `[VERIFICAR EN LAB: que el alias prueba-41 resuelva a la misma sesión en agent y en sessions reset]`

**Si falla:**
- `sessions reset` rechaza la clave → usa la forma canónica: `nemoclaw my-assistant sessions reset agent:main:prueba-41`.
- Para ver qué sesiones existen: `nemoclaw my-assistant sessions list`.

---

## Receta 8 · Abre el dashboard de OpenClaw en tu navegador local

**En tu computadora (terminal 1, déjala abierta):**

```bash
brev port-forward <instancia> -p 18789:18789
```

**En la máquina (terminal 2):**

```bash
nemoclaw my-assistant dashboard-url --quiet
```

Abre en tu navegador la URL que imprime (empieza con `http://127.0.0.1:18789/`). `[VERIFICAR EN LAB: formato exacto de la URL]`

**Atención:** la URL lleva el token del gateway después de `#token=`. Quien la tenga es operador de tu agente. No la pegues en ningún lado ni la muestres en video.

Alternativa con ssh puro (después de `brev refresh`):

```bash
ssh -N -L 18789:127.0.0.1:18789 <instancia>
```

**Si falla:**
- `localhost:18789` rechaza la conexión → revisa el orden `local:remoto`, o que el puerto local no esté ocupado. Usa otro local: `brev port-forward <instancia> -p 19000:18789` y abre `http://127.0.0.1:19000`.
- Aparece `Pairing required` → ve a **Overview → Gateway Access → Connect** en el dashboard, o espera un par de minutos y recarga. Si sigue, receta 9 de la clase 4.2.
- `brev port-forward` acepta un solo `-p` por comando; si repites `-p`, solo vale el último.
- Nunca abras el puerto 8080 (el gateway de OpenShell) a internet ni uses `brev ports open ... --public` para el dashboard.

---

## Receta 9 · Pausa y reanuda sin perder tu laboratorio

**En tu computadora:**

```bash
brev stop <instancia>
brev ls                         # espera a ver STOPPED
```

Para volver:

```bash
brev start <instancia>
brev ls                         # espera a ver RUNNING
brev refresh                    # la IP puede cambiar al reanudar
brev shell <instancia>
```

**En la máquina, después de reanudar:**

```bash
sudo systemctl start docker && docker info    # por si Docker no arrancó solo
nemoclaw my-assistant status
nemoclaw my-assistant start                   # solo si el sandbox quedó detenido
openshell sandbox list
nemoclaw my-assistant connect --probe-only    # prueba de salud; exit 0 = bien
nemoclaw my-assistant recover                 # si el gateway o el reenvío de puertos no están sanos
```

Luego, en la página del curso, copia una cookie nueva y repite **Probar conexión**.

Costos (lista pública de NVIDIA): una instancia de 4 vCPU / 16 GB cuesta unos 0.15 USD por hora corriendo. Detenida, solo pagas el disco: 0.0001314 USD por GB-hora. `[VERIFICAR EN LAB: precio real y tamaño de disco del launchable; puede aparecer como Free]`

**Si falla:**
- `instance "<instancia>" does not support stop.` → el tipo de instancia no se puede pausar. Respalda (receta 11) y elimina.
- `brev start` falla → no hay capacidad en ese proveedor y región. Reintenta más tarde. Tus datos quedan inaccesibles, no borrados, hasta que vuelva la capacidad.
- Recuerda: `/tmp` se borra al detener. Todo lo demás del disco se conserva.

---

## Receta 10 · Diagnóstico rápido

**En la máquina:**

```bash
nemoclaw my-assistant doctor              # chequeos de Docker, OpenShell, gateway, puertos y sandbox
nemoclaw my-assistant logs --tail 100     # logs del gateway + auditoría de OpenShell (denegaciones)
nemoclaw my-assistant logs --follow       # en vivo; Ctrl+C para salir
nemoclaw doctor                           # chequeos del host, sin sandbox
sudo tail -n 50 /tmp/launch-plugin.log    # log del arranque del launchable
```

`[VERIFICAR EN LAB: que /tmp/launch-plugin.log exista en la imagen actual]`

Cuidado con `openshell logs`: ahí `--tail` **sigue** el log en vivo, mientras que en `nemoclaw … logs` `--tail N` es un número de líneas.

---

## Receta 11 · Respalda tu workspace antes de eliminar

**En la máquina:**

```bash
nemoclaw my-assistant download /sandbox/.openclaw/workspace/ ./respaldo-workspace/
ls -la ./respaldo-workspace/
```

**En tu computadora:**

```bash
brev copy <instancia>:/home/ubuntu/respaldo-workspace ./respaldo-workspace
brev delete <instancia>          # irreversible: borra la máquina y sus volúmenes
brev ls
```

`[VERIFICAR EN LAB: que la carpeta de inicio en la máquina sea /home/ubuntu y que brev copy acepte directorios]`

**Si falla:**
- `download` termina con estado `2` → la ruta no existe dentro del sandbox. Revisa con `nemoclaw my-assistant exec -- ls /sandbox/.openclaw/`.
- No puedes detener ni eliminar, o la instancia se reinicia sola → escribe a brev-support@nvidia.com con el ID de organización, el nombre de la instancia y la hora.

---

## Receta 12 · Arregla `ssh: Could not resolve hostname <instancia>`

Problema abierto en NemoClaw (octubre de 2026): Brev agrega una línea `Include` a tu `~/.ssh/config`, pero si quedó **dentro** de un bloque `Host` que ya tenías, ssh la ignora. La CLI solo revisa que la línea exista.

**En tu computadora:**

```bash
cp ~/.ssh/config ~/.ssh/config.bak       # respaldo
grep -n "Include\|^Host\|^Match" ~/.ssh/config
```

Abre `~/.ssh/config` con tu editor y mueve la línea `Include` que apunta a `.brev/ssh_config` hasta **arriba del archivo**, antes del primer `Host` o `Match`. Guarda y prueba:

```bash
brev refresh
ssh <instancia>
```

Salida esperada: entras a la máquina.

**Si falla:** restaura tu archivo con `cp ~/.ssh/config.bak ~/.ssh/config`, revisa que exista `~/.brev/ssh_config` (si no, `brev refresh` lo regenera) y mientras tanto usa la ruta del navegador (página del curso). Referencia: [NemoClaw #13090](https://github.com/NVIDIA/NemoClaw/issues/13090).
