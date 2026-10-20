# Cookbook 4.1 · Tu laboratorio NemoClaw desde la terminal de operador

Recetas para revisar, usar y diagnosticar tu laboratorio NemoClaw en Brev. Todas se pegan en la **VM TERMINAL** del tablero: no necesitas instalar nada en tu computadora. Sirven igual en cualquier máquina con NemoClaw.

Convenciones:
- **VM TERMINAL** = la terminal de operador (usuario `ubuntu`, carpeta `/home/ubuntu`). Ábrela desde el tablero de tu laboratorio.
- `my-assistant` es el nombre del sandbox que crea la configuración en el navegador. Si `nemoclaw list` muestra otro, úsalo en su lugar.
- Todos los comandos `nemoclaw` imprimen `ExperimentalWarning: SQLite is an experimental feature`. Ignora esa línea.

Basado en la lección 03a-kickstart del curso NVIDIA DLI «NemoClaw» (Apache-2.0), la documentación de Brev y la de NemoClaw.

---

## Receta 1 · Abre la terminal de operador y úsala bien

1. En el tablero de tu laboratorio (`https://nemoclaw-<tu-id>.gobrev.dev/dashboard`), tarjeta **MY-ASSISTANT**, haz clic en **VM TERMINAL**.
2. Se abre una ventana encima del tablero. **Haz clic dentro del área negra** antes de escribir.
3. Pega con **Ctrl + V** (en Mac, **Cmd + V**) y presiona **Enter**.
4. **Esc** se envía a la terminal. **Shift + Esc** cierra la terminal y lo que esté corriendo en ella.

Comprueba dónde estás:

```bash
whoami
pwd
```

Salida esperada: `ubuntu` y `/home/ubuntu`.

**Si falla:**
- Escribes y no aparece nada, o el tablero reacciona a las teclas → la terminal no tiene el foco. Haz clic dentro del área negra.
- La terminal se cerró → presionaste **Shift + Esc**. Vuelve a abrirla con **VM TERMINAL**.

---

## Receta 2 · Revisa que el laboratorio esté sano

```bash
nemoclaw list                   # sandboxes registrados, con agente, proveedor y políticas
nemoclaw my-assistant status    # salud del sandbox y prueba de inferencia
openshell sandbox list          # estado crudo de los sandboxes en OpenShell
```

Salida esperada:
- `nemoclaw list` muestra `my-assistant` con el agente `openclaw`, el proveedor `nvidia-prod`, las políticas `brew-balanced`, `huggingface`, `npm`, `openclaw-pricing` y `pypi`, y el dashboard en `127.0.0.1:18789`.
- `nemoclaw my-assistant status` reporta la inferencia `healthy` y la fase `Ready`.
- `openshell sandbox list` muestra `my-assistant` con `PHASE` en `Ready`.

**Si falla:**
- La inferencia sale `unauthorized` → la key del proveedor fue rechazada (401/403). Es un problema de credencial, no de red: genera otra key en build.nvidia.com y vuelve a configurar el agente.
- `nemoclaw: command not found` → no estás en la **VM TERMINAL** (quizá abriste **SANDBOX TERMINAL**). Ciérrala y abre la de operador.

---

## Receta 3 · Revisa el gateway de OpenShell

El gateway de OpenShell es la pieza del host que maneja el sandbox y la ruta al modelo. Escucha en el puerto **18080**, solo dentro de la máquina.

```bash
openshell status
openshell gateway info
```

Salida esperada:
- `openshell status` muestra **Server Status** con `Gateway nemoclaw-18080`, `Server https://127.0.0.1:18080`, `Status Connected`, `Authentication Authenticated (mTLS transport)` y la versión `0.0.116`.
- `openshell gateway info` muestra `nemoclaw-18080`, `https://127.0.0.1:18080`, el estado `healthy` y la versión.

**Si falla:** `openshell gateway status` no existe. Usa `openshell gateway info` o `openshell status`.

---

## Receta 4 · Versiones y recursos de la máquina

Útil para reportar un problema en el foro.

```bash
nemoclaw --version
openshell --version
nemoclaw my-assistant exec -- openclaw --version
free -h          # memoria
df -h /          # disco
```

Salida esperada: versiones parecidas a NemoClaw v0.0.135, OpenShell 0.0.116 y OpenClaw v2026.9.2; unos 15 GiB de memoria y más de 260 GB libres en disco. Si tu versión muestra otros números, sigue: el laboratorio se actualiza.

---

## Receta 5 · Operador frente a sandbox: quién es quién

```bash
# Tú, en la máquina
id

# El agente, dentro del cuarto
nemoclaw my-assistant exec -- whoami
nemoclaw my-assistant exec -- pwd
openshell sandbox exec -n my-assistant -- id
```

Salida esperada:
- `id` en la máquina: `uid=1000(ubuntu)`, con grupos como `sudo` y `docker`. El operador tiene poder.
- Dentro del sandbox: `sandbox`, `/sandbox` y `uid=998(sandbox) gid=998(sandbox)`. El agente no lo tiene.

Si el chat te dijo que el agente es otro usuario (por ejemplo `gateway-owner`), gana lo que muestra el sistema.

**Si falla:** `exec` necesita el separador `--` antes del comando. Sin él, NemoClaw intenta interpretar el comando como una opción suya.

---

## Receta 6 · Un turno de agente desde la terminal

`exec` lo corres tú, como operador. Con `agent`, el modelo decide qué hacer.

```bash
nemoclaw my-assistant agent --session-key prueba-41 -m '¿Quien eres y en que carpeta trabajas? Responde en una frase.'
```

Salida esperada: una frase del agente. Compárala con la receta 5.

**Si falla:**
- `agent` exige un selector: `--agent`, `--session-id`, `--session-key` o `--to`. Sin uno de ellos, se niega.
- Usa comillas simples alrededor del mensaje. Si tu mensaje lleva un apóstrofo, cámbialo por otra palabra.

---

## Receta 7 · Prueba que la memoria vive en la clave de sesión

```bash
# 1. Planta un dato en la sesión memo-41
nemoclaw my-assistant agent --session-key memo-41 -m 'Recuerda este codigo: CODE-7Q4. No lo escribas en ningun archivo. Responde solo OK.'

# 2. Pregunta en la MISMA sesión
nemoclaw my-assistant agent --session-key memo-41 -m 'Cual era el codigo que te di? Responde solo el codigo.'

# 3. Reinicia la sesión
nemoclaw my-assistant sessions reset memo-41

# 4. Pregunta otra vez
nemoclaw my-assistant agent --session-key memo-41 -m 'Cual era el codigo que te di? Si no lo sabes, responde: no lo se.'
```

Salida esperada: `OK`, luego `CODE-7Q4`, luego `Reset session 'agent:main:memo-41' on agent 'main' via the OpenClaw gateway.` y al final `no lo se`.

Para ver qué sesiones existen, en un formato fácil de leer:

```bash
nemoclaw my-assistant sessions list --json
```

Salida esperada: un JSON con campos como `"agentId": "main"`, `"kind": "direct"` y `"contextTokens": 131072`. Sin `--json`, la tabla es muy ancha para la terminal del navegador.

**Si falla:** `sessions reset` rechaza la clave → usa la forma completa: `nemoclaw my-assistant sessions reset agent:main:memo-41`.

---

## Receta 8 · Trae los archivos del curso

```bash
git clone --depth 1 https://github.com/uncrayon/curso-seguridad-agentes-nemoclaw ~/curso
ls ~/curso
ls ~/curso/datos/faq/
```

Salida esperada: la carpeta `~/curso` con `clases/`, `datos/` y los demás archivos del curso; en `datos/faq/`, los `.md` de la FAQ.

**Si falla:**
- `destination path '/home/ubuntu/curso' already exists` → ya lo clonaste. Para traer la versión más nueva: `cd ~/curso && git pull && cd ~`.
- No conecta → revisa que la instancia esté en **Running** y vuelve a intentar en un minuto.

---

## Receta 9 · Mira los registros

En el navegador: el panel de registros del tablero tiene los filtros **All**, **VM**, **Gateway** y **Agent**.

En la terminal:

```bash
nemoclaw my-assistant logs --tail 100                       # últimas 100 líneas: gateway y auditoría de OpenShell
nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4   # solo las últimas conexiones bloqueadas
```

Salida esperada: los turnos recientes y, si la política bloqueó algo, líneas con `DENIED`. Las leemos en el Módulo 5.

Cuidado con `openshell logs`: ahí `--tail` **sigue** el log en vivo, mientras que en `nemoclaw … logs` `--tail N` es un número de líneas.

---

## Receta 10 · Guarda lo importante antes de borrar

**Delete** borra la máquina y todo su disco. Antes, imprime lo que quieras conservar y cópialo a tus notas. Por ejemplo, la personalidad de tu agente (clase 4.2):

```bash
nemoclaw my-assistant exec -- cat /sandbox/.openclaw/workspace/SOUL.md
```

Selecciona el texto en la terminal, cópialo y pégalo en tus notas.

Después, en la consola de Brev: **Compute** → tu instancia → **Delete**. Es irreversible.

**Si falla:** no puedes detener ni borrar la instancia, o se enciende sola → escribe a brev-support@nvidia.com con el ID de tu organización, el nombre de la instancia y la hora.
