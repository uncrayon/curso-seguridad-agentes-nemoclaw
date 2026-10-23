# Cookbook · Workspace, sesiones y memoria de OpenClaw

Recetas para inspeccionar y editar el workspace de un agente OpenClaw dentro de NemoClaw, como operador. Funcionan en el laboratorio del curso y en cualquier instalación de NemoClaw.

Convenciones:
- Todo se pega en la **VM TERMINAL** del tablero (la terminal de operador, usuario `ubuntu`), salvo que diga **SANDBOX TERMINAL**.
- `my-assistant` es el sandbox del laboratorio; confírmalo con `nemoclaw list`.
- El workspace está en `/sandbox/.openclaw/workspace/`. Dentro del sandbox, `~` es `/sandbox`.
- Ignora la línea `ExperimentalWarning: SQLite is an experimental feature` que imprime cada comando `nemoclaw`.

Basado en la lección 03b-openclaw del curso NVIDIA DLI «NemoClaw» (Apache-2.0) y en la documentación de NemoClaw.

---

## Receta 1 · Inventario del workspace

```bash
nemoclaw my-assistant exec -- ls -la /sandbox/.openclaw/workspace
```

Salida esperada en un laboratorio recién creado: `AGENTS.md`, `HEARTBEAT.md`, `IDENTITY.md`, `POLICY.md`, `SOUL.md`, `TOOLS.md` y `USER.md`. Todavía no hay `MEMORY.md`, `memory/` ni `skills/`: aparecen cuando el agente guarda memoria o cuando instalas una skill (clase 4.3).

Para ver cuántas skills trae el agente de fábrica (no viven en el workspace):

```bash
nemoclaw my-assistant skill list
```

Salida esperada: una lista con un resumen parecido a `22/57 ready`.

**Si falla:**
- `exec` necesita el separador `--` antes del comando.
- Ves `nemoclaw: recent network policy denial detected for …` → no es un error de tu comando: es una pista de que la política bloqueó una conexión hace poco. La retomamos en «Seguridad agéntica con OpenShell».

---

## Receta 2 · Lee los archivos que definen al agente

```bash
nemoclaw my-assistant exec -- cat /sandbox/.openclaw/workspace/SOUL.md
nemoclaw my-assistant exec -- head -n 30 /sandbox/.openclaw/workspace/AGENTS.md
nemoclaw my-assistant exec -- cat /sandbox/.openclaw/workspace/IDENTITY.md
nemoclaw my-assistant exec -- cat /sandbox/.openclaw/workspace/POLICY.md
```

Salida esperada: el texto de cada archivo. `exec` corre como el usuario `sandbox`, el mismo que el agente.

**Si falla:** `No such file or directory` → revisa la ruta completa. Nunca uses `docker exec` para esto: corre como root y no ve la configuración del agente.

---

## Receta 3 · Mira el escritorio desde adentro (SANDBOX TERMINAL)

En el tablero, haz clic en **SANDBOX TERMINAL**. Esa terminal está dentro del cuarto.

```bash
whoami; pwd; echo "$HOME"
cd /sandbox/.openclaw/workspace
ls -la
```

Salida esperada: `sandbox`, `/sandbox`, `/sandbox` y la lista de archivos de la receta 1.

Fíjate en `$HOME`: dentro del cuarto, `~` es `/sandbox`, no el workspace.

---

## Receta 4 · Pide al agente que se describa y compara

```bash
nemoclaw my-assistant agent --session-key describe-42 -m 'Enumera brevemente los archivos de tu workspace y explica cada uno en una viñeta, sin volcar su contenido.'
nemoclaw my-assistant exec -- ls -1 /sandbox/.openclaw/workspace
```

Compara las dos listas. Lo que el agente dice es su relato; `ls` es la evidencia.

**Si falla:** `agent` necesita un selector (`--agent`, `--session-id`, `--session-key` o `--to`). Usa comillas simples alrededor del mensaje.

---

## Receta 5 · Personaliza SOUL.md (archivo en la máquina → upload → agregar)

```bash
# 1. Escribe tu sección en la máquina
cat > ~/soul-extra.md <<'EOF'

## Proyecto: Soporte NemoClaw
- Ayudas a estudiantes del curso "Agentes Seguros con NemoClaw".
- Respondes en español neutro, con frases cortas y pasos numerados.
- Antes de responder, clasificas la duda en una categoría: instalacion, api_key, brev, seguridad u otro.
- Si usas la FAQ del curso, citas el archivo de donde sale la respuesta.
- Nunca pides, repites ni guardas API keys, tokens o cookies. Si alguien pega una, le pides que la revoque.
- Si no sabes algo, lo dices y sugieres preguntar en el foro del curso.
EOF

# 2. Copia de seguridad del original, dentro del sandbox
nemoclaw my-assistant exec -- cp /sandbox/.openclaw/workspace/SOUL.md /tmp/SOUL.md.original

# 3. Sube tu sección al sandbox y comprueba que llegó
nemoclaw my-assistant upload ~/soul-extra.md /tmp/
nemoclaw my-assistant exec -- ls -la /tmp/soul-extra.md

# 4. Agrégala al final de SOUL.md y léelo de vuelta
nemoclaw my-assistant exec -- sh -c 'cat /tmp/soul-extra.md >> /sandbox/.openclaw/workspace/SOUL.md'
nemoclaw my-assistant exec -- tail -n 9 /sandbox/.openclaw/workspace/SOUL.md
nemoclaw my-assistant exec -- ls -la /sandbox/.openclaw/workspace/SOUL.md
```

Salida esperada: `soul-extra.md` en `/tmp` con dueño `sandbox`, la sección nueva al final de `SOUL.md` y el archivo con dueño `sandbox`.

Las comillas simples en `sh -c '…'` importan: hacen que `>>` y las rutas se interpreten **dentro** del sandbox, no en la máquina.

Para deshacer:

```bash
nemoclaw my-assistant exec -- cp /tmp/SOUL.md.original /sandbox/.openclaw/workspace/SOUL.md
```

**Si falla:**
- `SOUL.md` quedó solo con tu sección → usaste `>` en vez de `>>`. Deshaz con el comando de arriba y repite.
- La terminal muestra `>` y espera → falta la línea `EOF` final. Escríbela sola, al inicio de la línea, y presiona **Enter**.
- `Permission denied` al agregar → revisa el dueño con el último `ls -la` y anota la salida para el foro del curso.
- Prefieres un editor → `nano ~/soul-extra.md`; guarda con **Ctrl + O**, **Enter**; sal con **Ctrl + X**.

---

## Receta 6 · Prueba el cambio en una sesión nueva

```bash
nemoclaw my-assistant agent --session-key soul-42 -m '¿Quien eres, a quien ayudas y que nunca haces?'
```

Salida esperada: menciona el curso, el español neutro y la regla de las keys.

**Si falla:** el agente no cambia → ¿usaste una clave de sesión nueva? El workspace se lee al inicio de cada sesión. Si reutilizas una clave, primero `nemoclaw my-assistant sessions reset <clave>`.

---

## Receta 7 · Lista y reinicia sesiones

```bash
nemoclaw my-assistant sessions list --json      # formato legible en la terminal del navegador
nemoclaw my-assistant sessions reset soul-42    # borra el historial de esa conversación
nemoclaw my-assistant sessions --help           # todas las opciones
```

Salida esperada:
- `sessions list --json`: un JSON con tus sesiones y campos como `"agentId": "main"`, `"modelProvider": "inference"`, `"contextTokens": 131072` y `"kind": "direct"`.
- `sessions reset`: `Reset session 'agent:main:soul-42' on agent 'main' via the OpenClaw gateway.`

`sessions` le pasa la orden a `openclaw sessions` dentro del sandbox. Las sesiones internas de arranque de NemoClaw no se muestran.

**Si falla:**
- Sin `--json`, la tabla es tan ancha que se lee mal en la terminal del navegador.
- `reset` rechaza la clave → usa la forma completa: `agent:main:soul-42`.

---

## Receta 8 · Memoria en archivos: el agente escribe, tú verificas

```bash
# 1. El agente escribe (sesión A)
nemoclaw my-assistant agent --session-key memoria-a -m 'Agrega esta linea al final de /sandbox/.openclaw/workspace/MEMORY.md sin borrar nada: "soporte-pref-01: responde en español neutro y cita el archivo de la FAQ que usaste. Referencia REF-4821." Despues leelo de vuelta y cita la linea.'

# 2. Tú verificas como operador
nemoclaw my-assistant exec -- grep -n "REF-4821" /sandbox/.openclaw/workspace/MEMORY.md

# 3. Reinicias la sesión A y preguntas desde otra (sesión B)
nemoclaw my-assistant sessions reset memoria-a
nemoclaw my-assistant agent --session-key memoria-b -m 'Lee /sandbox/.openclaw/workspace/MEMORY.md e indica la preferencia y la referencia de soporte-pref-01.'
```

Salida esperada: `grep` imprime la línea con `REF-4821` y la sesión B responde con esa referencia. La conversación se reinició; el archivo no.

**Si falla:**
- `grep` no encuentra nada aunque el agente dijo que guardó → no le creas. Busca si escribió en otra ruta: `nemoclaw my-assistant exec -- grep -rn "REF-4821" /sandbox/.openclaw/`.
- La sesión B no la encuentra → pídele explícitamente que lea el archivo con la ruta completa. Que no lo «recuerde» no significa que no pueda leerlo.

---

## Receta 9 · Mira qué pasa en el gateway

En el navegador: el panel de registros del tablero, con el filtro **Gateway** o **Agent**.

En la terminal:

```bash
nemoclaw my-assistant logs --tail 50
openshell gateway info
```

Salida esperada: los turnos recientes del gateway y la auditoría de OpenShell; y el gateway de OpenShell `nemoclaw-18080` en `https://127.0.0.1:18080`, `healthy`. El chat de OpenClaw escucha en el puerto 18789, dentro del sandbox.

---

## Receta 10 · Comandos que NO debes correr (en la máquina ni en el sandbox)

| Comando | Por qué no | Qué hacer en su lugar |
|---|---|---|
| `openclaw update` | OpenClaw viene fijado en la imagen. Se cuelga o agota el tiempo. | En el laboratorio del curso, no cambies versiones. En una instalación propia: `nemoclaw update` y luego `nemoclaw my-assistant rebuild`. |
| `openshell self-update` / `npm update -g openshell` | NemoClaw exige una versión exacta de OpenShell. | Deja que NemoClaw maneje OpenShell. |
| `openshell sandbox create` | Crea un sandbox fuera del control de NemoClaw. | `nemoclaw onboard` (fuera del alcance de este curso). |
| Escribir en `~/SOUL.md` dentro del sandbox | `~` es `/sandbox`, no el workspace. | Usa `/sandbox/.openclaw/workspace/SOUL.md`. |
| `cat … > SOUL.md` (un solo `>`) | Borra el contenido anterior. | Usa `>>` para agregar al final. |
