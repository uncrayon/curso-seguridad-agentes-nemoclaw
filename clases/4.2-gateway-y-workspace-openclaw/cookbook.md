# Cookbook 4.2 · Workspace, sesiones y memoria de OpenClaw

Recetas para inspeccionar y editar el workspace de un agente OpenClaw dentro de NemoClaw, como operador. Funcionan en el launchable del curso y en cualquier instalación de NemoClaw.

Convenciones:
- Todo se corre **en la máquina** (`brev shell <instancia>`), salvo que diga **dentro del sandbox**.
- `my-assistant` es el sandbox del launchable; confírmalo con `nemoclaw list`. `[VERIFICAR EN LAB]`
- El workspace está en `/sandbox/.openclaw/workspace/`. Dentro del sandbox, `~` es `/sandbox`.

Basado en la lección 03b-openclaw del curso de NVIDIA DLI (Apache-2.0) y en la documentación de NemoClaw.

---

## Receta 1 · Entra al sandbox

```bash
nemoclaw my-assistant connect            # espera a que esté Ready y arregla llaves SSH viejas
# o, sin las comprobaciones de NemoClaw:
openshell sandbox connect my-assistant
```

**Dentro del sandbox:**

```bash
whoami          # sandbox
pwd             # /sandbox
echo "$HOME"    # /sandbox
exit            # vuelves a la máquina
```

Salida esperada: el usuario `sandbox` y la carpeta `/sandbox`. `connect` imprime una pista al entrar; si abriste la TUI del agente, sal con `/exit` antes de `exit`. `[VERIFICAR EN LAB]`

**Si falla:**
- `connect` se queda mostrando una fase (por ejemplo, la imagen todavía se descarga) → espera; el límite por defecto es 120 s. Súbelo con `NEMOCLAW_CONNECT_TIMEOUT=300 nemoclaw my-assistant connect`.
- `connect` sale porque el gateway está caído → `nemoclaw my-assistant status` y luego `nemoclaw my-assistant recover`.
- Después de reanudar la instancia, `connect` limpia solo las llaves SSH viejas de `~/.ssh/known_hosts`; no necesitas repetir el onboarding.

---

## Receta 2 · Inventario del workspace

**Dentro del sandbox:**

```bash
cd /sandbox/.openclaw/workspace
ls -la
head -n 20 SOUL.md
head -n 30 AGENTS.md
ls -la skills/ memory/ 2>/dev/null
cat MEMORY.md 2>/dev/null || echo "(todavía no hay MEMORY.md)"
```

Salida esperada: `AGENTS.md`, `HEARTBEAT.md`, `IDENTITY.md`, `SOUL.md`, `TOOLS.md`, `USER.md` y `POLICY.md`; `skills/` con las skills de inicio. `MEMORY.md` y `memory/` aparecen cuando el agente guarda memoria por primera vez. `[VERIFICAR EN LAB: lista exacta y skills de inicio]`

**Si falla:** `Permission denied` al leer algo fuera de `/sandbox` o `/tmp` → es la política del sandbox; lo vemos en el módulo 5. Dentro del workspace no debería pasar.

---

## Receta 3 · Lee sin entrar al sandbox

Útil para scripts y para comprobar rápido lo que el agente afirma.

```bash
nemoclaw my-assistant exec --workdir /sandbox/.openclaw/workspace -- ls -la
nemoclaw my-assistant exec -- cat /sandbox/.openclaw/workspace/SOUL.md
nemoclaw my-assistant exec -- grep -n "REF-" /sandbox/.openclaw/workspace/MEMORY.md
```

Salida esperada: la misma información que en la receta 2. `exec` corre como el usuario `sandbox` con `HOME=/sandbox`.

**Si falla:**
- `error: --workdir: <dir> does not exist inside the sandbox` → la carpeta no existe; revisa la ruta.
- Ves `nemoclaw: recent network policy denial detected for …` → no es un error de tu comando: es una pista de que la política bloqueó una conexión hace poco. La retomamos en el módulo 5.
- Nunca uses `docker exec` para esto: corre como root con `HOME=/root` y no ve la configuración del agente.

---

## Receta 4 · Pide al agente que se describa y compara

```bash
nemoclaw my-assistant agent --session-id describe-01 -m "Enumera brevemente los archivos de tu workspace y explica cada uno en una viñeta, sin volcar su contenido."
nemoclaw my-assistant exec --workdir /sandbox/.openclaw/workspace -- ls -1
```

Compara las dos listas. Lo que el agente dice es su relato; `ls` es la evidencia.

**Si falla:** `agent` necesita un selector (`--agent`, `--session-id`, `--session-key` o `--to`). Si el turno se cuelga sin usar herramientas, corre la **Comprobación de estado** de la página del curso.

---

## Receta 5 · Lista y administra sesiones

```bash
nemoclaw my-assistant sessions                          # sesiones del agente por defecto
nemoclaw my-assistant sessions list --agent main --json
nemoclaw my-assistant sessions reset describe-01 --agent main
nemoclaw my-assistant sessions export describe-01 --agent main
```

Salida esperada: la lista muestra tus sesiones (por ejemplo `describe-01` y las `quick-3b-…` que creó la página). `reset` archiva el historial y deja la clave apuntando a una sesión nueva. `export` copia los `.jsonl` a `./sessions-my-assistant/`. `[VERIFICAR EN LAB: que el alias describe-01 resuelva a la sesión creada con --session-id]`

**Atención:** los `.jsonl` exportados pueden tener secretos que alguien pegó en el chat. Se guardan con permisos `0600`; no los subas a tu repo.

**Si falla:** `delete` se niega a borrar la sesión principal del agente: es intencional.

---

## Receta 6 · Respalda el workspace (o un archivo)

```bash
mkdir -p ~/respaldo
nemoclaw my-assistant download /sandbox/.openclaw/workspace/SOUL.md ~/respaldo/
nemoclaw my-assistant download /sandbox/.openclaw/workspace/ ~/respaldo/workspace/
ls -la ~/respaldo
```

Salida esperada: los archivos en `~/respaldo`. Haz esto antes de cualquier edición o de eliminar la instancia.

**Si falla:** código de salida `2` → la ruta no existe en el sandbox. Los enlaces simbólicos y archivos especiales se rechazan a propósito.

---

## Receta 7 · Personaliza SOUL.md (download → editar → upload)

```bash
mkdir -p ~/soporte && cd ~/soporte
nemoclaw my-assistant download /sandbox/.openclaw/workspace/SOUL.md ./
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

nemoclaw my-assistant upload ./SOUL.md /sandbox/.openclaw/workspace/SOUL.md
nemoclaw my-assistant exec -- tail -n 9 /sandbox/.openclaw/workspace/SOUL.md
nemoclaw my-assistant exec -- ls -la /sandbox/.openclaw/workspace/SOUL.md
```

Prueba en una sesión **nueva**:

```bash
nemoclaw my-assistant agent --session-id soul-check-01 -m "¿Quién eres, a quién ayudas y qué nunca haces?"
```

Salida esperada: la sección nueva al final del archivo y una respuesta que menciona el curso, el español neutro y la regla de las keys. `[VERIFICAR EN LAB: que el archivo subido quede con dueño y permisos que el agente puede leer]`

Para deshacer:

```bash
nemoclaw my-assistant upload ./SOUL.md.original /sandbox/.openclaw/workspace/SOUL.md
```

**Si falla:**
- El agente no cambia → ¿preguntaste en una sesión nueva? El workspace se lee al inicio de cada sesión.
- Subiste a `/sandbox/SOUL.md` → ruta equivocada. Repite con la ruta del workspace.
- Alternativa sin subir archivos: entra con `nemoclaw my-assistant connect` y usa el mismo `cat >> /sandbox/.openclaw/workspace/SOUL.md <<'EOF' … EOF` dentro del sandbox.

---

## Receta 8 · Edita MEMORY.md por medio del agente y verifícalo

```bash
# 1. El agente escribe (sesión A)
nemoclaw my-assistant agent --session-id memoria-a -m "Añade esta preferencia a /sandbox/.openclaw/workspace/MEMORY.md sin sustituir el contenido existente: soporte-pref-01: responde en español neutro y cita el archivo de la FAQ que usaste; referencia REF-4821. Después léelo de vuelta y cita la línea."

# 2. Tú verificas como operador
nemoclaw my-assistant exec -- grep -n "REF-4821" /sandbox/.openclaw/workspace/MEMORY.md

# 3. Otra sesión lo recupera desde el archivo (sesión B)
nemoclaw my-assistant agent --session-id memoria-b -m "Lee MEMORY.md e indica la preferencia y la referencia de soporte-pref-01."
```

Salida esperada: `grep` imprime la línea con `REF-4821` y la sesión B responde con esa referencia.

**Si falla:**
- `grep` no encuentra nada aunque el agente dijo que guardó → no le creas. Revisa si escribió en otra ruta: `nemoclaw my-assistant exec -- grep -rn "REF-4821" /sandbox/.openclaw/`.
- La sesión B no la encuentra → pídele explícitamente que lea `MEMORY.md`. Por defecto `MEMORY.md` entra al contexto de la sesión principal, no de todas: que no lo "recuerde" no significa que no pueda leerlo.

---

## Receta 9 · Resuelve `Pairing required`

Desde OpenClaw 2026.9.1 el emparejamiento de dispositivos es obligatorio. `NEMOCLAW_DISABLE_DEVICE_AUTH=1` ya no lo salta.

Primero, en el dashboard: espera un par de minutos y recarga, o ve a **Overview → Gateway Access → Connect**.

Si sigue:

```bash
nemoclaw my-assistant connect
```

**Dentro del sandbox:**

```bash
openclaw devices list --json              # busca la solicitud pendiente y su requestId
openclaw devices approve <requestId>
exit
```

Salida esperada: la solicitud pasa a aprobada y el dashboard deja de pedir pairing. `[VERIFICAR EN LAB]`

**Si falla:** hay un bug abierto (v0.0.133) en el que la autoaprobación rechaza scopes adicionales. Aprueba a mano como arriba y aprueba solo solicitudes que tú iniciaste. Referencia: [NemoClaw #13092](https://github.com/NVIDIA/NemoClaw/issues/13092).

---

## Receta 10 · Mira qué pasa en el gateway

```bash
nemoclaw my-assistant logs --tail 50
nemoclaw my-assistant logs --since 5m
nemoclaw my-assistant logs --follow       # Ctrl+C para salir
```

Salida esperada: los turnos recientes del gateway y la auditoría de OpenShell (por ejemplo, conexiones denegadas).

---

## Receta 11 · Comandos que NO debes correr (en la máquina ni en el sandbox)

| Comando | Por qué no | Qué hacer en su lugar |
|---|---|---|
| `openclaw update` | OpenClaw viene fijado en la imagen. Se cuelga o agota el tiempo. | En una instalación propia: `nemoclaw update` y luego `nemoclaw my-assistant rebuild`. En el launchable del curso: no cambies versiones. |
| `openshell self-update` / `npm update -g openshell` | NemoClaw exige una versión exacta de OpenShell. | Deja que el instalador de NemoClaw maneje OpenShell. |
| `openshell sandbox create` | Crea un sandbox fuera del control de NemoClaw. | `nemoclaw onboard` (fuera del alcance de este curso). |
| Escribir en `~/SOUL.md` | `~` es `/sandbox`, no el workspace. | Usa `/sandbox/.openclaw/workspace/SOUL.md`. |
