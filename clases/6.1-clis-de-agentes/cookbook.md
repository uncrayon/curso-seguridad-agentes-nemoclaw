# Cookbook · Inspecciona tu agente desde la terminal del laboratorio

Recetas para la **VM TERMINAL** del tablero de NemoClaw en Brev. Todo se hace en el navegador: no necesitas instalar nada en tu computadora. Las mismas recetas sirven en una instalación local de NemoClaw (clase 6.3).

**Convenciones**
- `my-assistant`: el nombre de tu sandbox. Si el tuyo es otro, cámbialo (lo ves con `openshell sandbox list`).
- **[host]** = en la VM TERMINAL (plano del operador, usuario `ubuntu`). **[sandbox]** = dentro del sandbox del agente, a través de `nemoclaw my-assistant exec -- <comando>`.
- Cada comando de `nemoclaw` imprime la línea `ExperimentalWarning: SQLite is an experimental feature`. Ignórala.
- Las salidas cambian un poco entre versiones. En el laboratorio verás nemoclaw v0.0.135, nemohermes v0.0.135, openshell 0.0.116 y OpenClaw v2026.9.2. Si tu versión muestra otro texto, compara la idea y sigue con la siguiente receta.

Basado en la lección 04b del curso NVIDIA DLI «NemoClaw» (Apache-2.0) y en la documentación de NVIDIA/NemoClaw.

---

## Receta 0 · Abre la terminal de operador
1. En la consola de Brev, tu instancia debe estar en **Running**. Presiona el botón verde **NemoClaw**: se abre `https://nemoclaw-<tu-id>.gobrev.dev` en otra pestaña.
2. En el tablero, en la tarjeta **MY-ASSISTANT**, presiona **VM TERMINAL**.
3. Haz clic dentro del área negra antes de escribir.

**Esperado:** una terminal con el prompt de `ubuntu`. El aviso de arriba dice que **Escape** se envía a la terminal y que **Shift+Escape** cierra la sesión.

**Si falla:**
- Escribes y no aparece nada, o se abre algo del tablero: la terminal no tiene el foco. Haz clic en el área negra.
- La página de NemoClaw no carga: revisa en la consola de Brev que la instancia siga en **Running**.

## Receta 1 · ¿Qué sandboxes hay? (OpenShell)
Para ver los sandboxes que maneja OpenShell:
```bash
# [host]
openshell sandbox list
```
**Esperado:** columnas `NAME`, `CREATED` y `PHASE`, con `my-assistant` en `Ready`.

**Si falla:** la lista está vacía o da error de conexión: el gateway no está arriba. Sigue con la Receta 2.

## Receta 2 · ¿Está vivo el gateway de OpenShell?
Para preguntarle a OpenShell por su recepción (el gateway que maneja sandboxes, rutas de inferencia y credenciales):
```bash
# [host]
openshell status
openshell gateway info
```
**Esperado:** `openshell status` imprime un bloque `Server Status` con el gateway `nemoclaw-18080`, el servidor `https://127.0.0.1:18080`, `Connected`, `Authenticated (mTLS transport)` y la versión `0.0.116`. `openshell gateway info` repite el nombre, la dirección y la versión. El puerto del gateway es **18080**.

**Si falla:**
- `openshell gateway status` da error: ese subcomando no existe. Usa los dos de arriba.
- Después de reiniciar la VM, levanta las piezas en este orden (comandos de la documentación de NemoClaw):
  ```bash
  nemoclaw my-assistant status        # también arranca el gateway
  nemoclaw my-assistant start         # si el sandbox estaba detenido
  nemoclaw my-assistant recover       # si el gateway o el reenvío siguen mal
  ```

## Receta 3 · ¿Qué ve NemoClaw? (registro y agentes)
Para ver los sandboxes que registró NemoClaw y confirmar qué agentes trae la VM:
```bash
# [host]
nemoclaw list
ls /usr/bin/nemohermes /usr/bin/nemo-deepagents
```
**Esperado:** `nemoclaw list` muestra `my-assistant` con el agente `openclaw`, el proveedor `nvidia-prod`, sus presets de política (por ejemplo `brew-balanced`, `huggingface`, `npm`, `openclaw-pricing`, `pypi`) y la dirección del chat `127.0.0.1:18789`. El `ls` imprime las dos rutas: Hermes y Deep Agents vienen instalados.

**Si falla:**
- `No sandboxes registered`, pero `openshell sandbox list` sí muestra uno: el registro `~/.nemoclaw/sandboxes.json` se perdió o está dañado. No borres nada; corre `nemoclaw my-assistant status` y revisa la FAQ.
- `Configuration file is present but is not valid JSON`: registro dañado. Ver "Malformed Registry File" en la documentación de NemoClaw.

## Receta 4 · Salud completa de un sandbox
Para preguntarle a NemoClaw si tu agente está sano:
```bash
# [host]
nemoclaw my-assistant status
```
**Esperado:** la inferencia en `healthy` y la fase en `Ready`. Si ves otro valor en la inferencia:

| Valor | Significa | Qué hacer |
|---|---|---|
| `healthy` | Todo bien | Nada |
| `unauthorized` | La ruta responde 401/403: credencial | Revisa tu key en build.nvidia.com. Para rotarla: `nemoclaw credentials reset <PROVIDER>` y `nemoclaw onboard` |
| `unreachable` | No llega al proveedor | Revisa la Receta 2 |

**Si falla:** `sandbox_container_stopped` → `nemoclaw my-assistant recover`.

## Receta 5 · Eje identidad: el mismo comando en dos planos
Para preguntar "¿quién soy?" afuera y adentro:
```bash
# [host]
id
# [sandbox] (una sola ejecución, sin abrir shell)
nemoclaw my-assistant exec -- id
nemoclaw my-assistant exec -- pwd
```
**Esperado:** en el host, `uid=1000(ubuntu)` con grupos como `sudo` y `docker`: el operador tiene poder. En el sandbox, `uid=998(sandbox) gid=998(sandbox)` y la carpeta `/sandbox`.

**Equivalente con OpenShell puro:** `openshell sandbox exec -n my-assistant -- id`. Úsalo para inspeccionar; para operar, prefiere `nemoclaw`.

**Compáralo con lo que dice el agente:** en **CHAT WITH AGENT**, pregúntale "¿Como qué usuario corres?". Puede responder un nombre que no es `sandbox` (por ejemplo, `gateway-owner`). La respuesta del operador es la que vale: nunca confíes en lo que el agente dice de sí mismo.

**Si falla:** `exec` imprime `nemoclaw: recent network policy denial detected for ...`: es un aviso de una denegación reciente, no un error de `exec`.

## Receta 6 · Eje archivos: dónde puede escribir el agente
Para intentar escribir en el sistema, en la carpeta temporal y listar el workspace:
```bash
# [sandbox]
nemoclaw my-assistant exec -- touch /usr/prueba       # debe FALLAR
nemoclaw my-assistant exec -- touch /tmp/prueba       # debe funcionar
nemoclaw my-assistant exec -- ls -la /sandbox/.openclaw/workspace
```
**Esperado:** el primero responde `Permission denied`; el segundo no imprime nada; el tercero lista `AGENTS.md`, `HEARTBEAT.md`, `IDENTITY.md`, `POLICY.md`, `SOUL.md`, `TOOLS.md` y `USER.md`, y después de la 4.3 también `faq/`, `reportes/` y `skills/`. Solo hay `MEMORY.md` si el agente guardó memoria.

**Si falla:** si `touch /usr/prueba` **funciona**, Landlock no se está aplicando. Anótalo: es un hallazgo.

## Receta 7 · Eje red: qué se bloquea y dónde lo ves
Para pedir una página fuera de la lista y luego buscar el bloqueo:
```bash
# [sandbox]
nemoclaw my-assistant exec -- curl -sS https://example.com
# [host]
nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4
nemoclaw my-assistant policy list
```
**Esperado:** `curl: (56) CONNECT tunnel failed, response 403`. En los logs, una línea parecida a:
```
[OCSF ] [ocsf] NET:OPEN [MED] DENIED /usr/bin/curl(…) -> example.com:443 [policy:- engine:opa] [reason:…]
```
`policy list` muestra los presets: los activos con `●` (por ejemplo `brew-balanced`, `huggingface`, `npm`, `pypi` y `openclaw-pricing`) y los disponibles con `○`.

![La VM TERMINAL con una línea DENIED del log; los números marcan el programa bloqueado, el destino y la razón](../../assets/lab/18-terminal-denegacion-log.png)

**Quieres permitir el host:**
- Temporal: en el tablero, **OPENSHELL TUI** → entra al sandbox con **[Enter]** → **[r]** para ver las reglas → la solicitud pendiente → **[a]** Approve (o **[x]** Reject).
- Persistente: `nemoclaw my-assistant policy add <preset> --dry-run` y luego `--yes` (clase 5.3).
- No uses el tier **Personal** salvo para cargas de confianza: abre cualquier host en 80/443 sin aprobaciones.

![La OpenShell TUI en la vista de reglas, con una solicitud pendiente; los números marcan las teclas Approve y Reject](../../assets/lab/21-openshell-tui-reglas-pendientes.jpg)

## Receta 8 · Eje persistencia: lo que sobrevive
Para ver las skills, la persona del agente y las sesiones guardadas:
```bash
# [host]
nemoclaw my-assistant skill list
nemoclaw my-assistant exec -- cat /sandbox/.openclaw/workspace/SOUL.md
nemoclaw my-assistant sessions list --json
```
**Esperado:** `skill list` da un resumen como `22/57 ready` (el número puede cambiar) e incluye `soporte-nemoclaw` de la 4.3. `SOUL.md` es la persona del agente. `sessions list --json` imprime JSON legible, con campos como `"agentId": "main"`, `"modelProvider": "inference"` y `"kind": "direct"`.

**Por qué importa:** todo lo que se escribe aquí vuelve a entrar al contexto en la próxima sesión. Si un atacante logra escribir una skill o editar `SOUL.md`, su instrucción sobrevive.

**Si falla:**
- `sessions list` sin `--json` imprime una tabla demasiado ancha para la terminal del navegador. Usa `--json`.
- `cat: ... No such file`: lista primero con `nemoclaw my-assistant exec -- ls /sandbox/.openclaw`.

## Receta 9 · Logs: OpenShell vs. NemoClaw (cuidado con `--tail`)
Para leer el registro de distintas formas:
```bash
# [host]
nemoclaw my-assistant logs --tail 50          # 50 líneas y termina
nemoclaw my-assistant logs --follow           # en vivo; sal con Ctrl+C
openshell logs my-assistant -n 20             # 20 líneas, OpenShell puro
```
**Esperado:** logs del gateway y la auditoría de OpenShell (denegaciones de política). En la VM TERMINAL, **Ctrl+C** detiene el comando; **Shift+Escape** cierra la ventana.

**Si falla:** `openshell logs my-assistant --tail` se queda abierto: en `openshell`, `--tail` **sigue** el log. Sal con Ctrl+C y usa `-n`.

## Receta 10 · Lee la política real (para la ficha comparativa)
**Con clics:** en el tablero, **OPENSHELL TUI** → tu sandbox con **[Enter]**. La vista del sandbox muestra las rutas de solo lectura y de lectura-escritura, y las reglas de red. Cambia de pestaña con **[h]**.

**En la terminal:**
```bash
# [host]
openshell policy get my-assistant --full | head -60
```
**Esperado:** el YAML vivo: `filesystem_policy` (`read_only`, `read_write`), `landlock`, `process` (`run_as_user: sandbox`) y `network_policies`. Con esto llenas la Tabla 2 del README **con datos de tu sandbox**.

**Si falla:** el nombre del sandbox está mal. Confírmalo con `openshell sandbox list`.

## Receta 11 · Diagnóstico rápido para reportar un problema
Para juntar información antes de pedir ayuda (comandos de la documentación de NemoClaw):
```bash
# [host]
nemoclaw doctor                       # chequeos del host y del gateway (solo lectura)
nemoclaw my-assistant doctor          # Docker, OpenShell, contenedor, puertos, sandbox
```
**Esperado:** una lista de chequeos con su estado.

**Si falla:** antes de pegar una salida en un foro público, revisa que no tenga tokens ni URLs con `#token=`.

## Receta 12 (opcional) · Conoce otro agente de NemoClaw
Hermes y Deep Agents vienen instalados en la VM (`/usr/bin/nemohermes` y `/usr/bin/nemo-deepagents`). Crear un segundo sandbox usa memoria de la VM, minutos de tu sesión y tu key de NVIDIA. Si quieres probar Hermes, sigue la clase [4.4](../4.4-hermes-en-nemoclaw/README.md) **antes** de cerrar el laboratorio.

## Receta 13 · Cierra el laboratorio: guarda y borra
Si vas a hacer la parte opcional de laboratorio de la [6.2](../6.2-biblioteca-de-skills/README.md), deja la instancia encendida y sigue con esa clase. Si no, guarda lo que quieras y **Delete**. Al borrar la instancia, todo lo que hay en la VM se pierde.

1. **Guarda lo que quieras.** Los archivos del curso (`~/curso`) ya están en GitHub. Para conservar algo que escribió tu agente, muéstralo y copia el texto a tus notas (selecciónalo con el mouse):
   ```bash
   # [sandbox]
   nemoclaw my-assistant exec -- cat /sandbox/.openclaw/workspace/reportes/resumen-faq.md
   nemoclaw my-assistant exec -- cat /sandbox/.openclaw/workspace/SOUL.md
   ```
2. **Cierra la terminal** con **Shift+Escape**.
3. **Borra la instancia.** En la consola de Brev: **Compute** → tu instancia (`nemoclaw-…`) → **Delete**. Confirma en el aviso que aparece.
4. **Revisa tu saldo.** En el menú de arriba, **Billing**, o el saldo en la barra superior. La instancia ya no debe aparecer en **Compute**.

**Por qué Delete y no Stop:** encendida, la instancia cuesta ≈USD 0.25/h. Detenida, el disco sigue cobrando ≈USD 0.05/h, unos USD 1.20 al día: más que tu cupón. Borrada, ya no cobra nada. Detalles en [LABORATORIO.md](../../LABORATORIO.md).
