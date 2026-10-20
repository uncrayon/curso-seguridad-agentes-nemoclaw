# Cookbook 6.1 · Inspecciona tu agente desde la shell del laboratorio

Recetas de terminal para la VM de Brev con NemoClaw. Sirven para esta clase y para cualquier instalación de NemoClaw, en Brev o local.

**Convenciones**
- `<instancia>`: el nombre de tu instancia en Brev (`brev ls`).
- `my-assistant`: el nombre de tu sandbox. Cámbialo por el tuyo (`openshell sandbox list`).
- **[host]** = en la shell de la VM (plano del operador). **[sandbox]** = dentro del sandbox del agente.
- Las salidas exactas cambian entre versiones de NemoClaw. Donde no las confirmamos dice `[VERIFICAR EN LAB]`.

Basado en la lección 04b del curso de NVIDIA DLI (Apache-2.0) y en la documentación de NVIDIA/NemoClaw.

---

## Receta 0 · Entra a la VM
```bash
# en tu computadora
brev ls
brev shell <instancia>
```
**Esperado:** `brev ls` muestra tu instancia en `RUNNING`; luego ves el prompt de la VM.

**Si falla:**
- La instancia está `STOPPED`: `brev start <instancia>` y espera a `RUNNING`.
- `ssh: Could not resolve hostname`: `brev refresh` y reintenta. Si sigue, mueve la línea `Include` de Brev al inicio de `~/.ssh/config`.
- `brev shell --host` se cuelga: usa `brev shell <instancia>` **sin** `--host`.
- `You have run out of credits` pero tienes créditos: estás en otra organización. `brev ls orgs` y `brev set <org>`.

**Sin terminal local:** en la [lección 04b](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/04b-modern-clis.html), sección "Abre un shell real en el launchable", usa los botones `openshell sandbox list`, `openshell status` y `agent ls`. Ahí el prefijo `agent <comando>` corre el comando **dentro** del sandbox. Esa consola no acepta comandos interactivos (`nemoclaw`, `openshell term`, `openclaw tui`).

---

## Receta 1 · ¿Qué sandboxes hay? (OpenShell)
```bash
# [host]
openshell sandbox list
```
**Esperado:** una tabla con tu sandbox (p. ej. `my-assistant`) y su estado. `[VERIFICAR EN LAB]` columnas exactas.

**Si falla:**
- `openshell: command not found`: NemoClaw se instaló sin OpenShell. En un launchable no debería pasar; en local, reinstala con el instalador oficial (clase 6.3).
- La lista está vacía: el gateway no está arriba. Sigue con la Receta 2.

## Receta 2 · ¿Está vivo el gateway de OpenShell?
```bash
# [host]
openshell status
```
**Esperado:** el estado del gateway de OpenShell (el que maneja sandboxes, rutas de inferencia y reenvíos de puertos). `[VERIFICAR EN LAB]` texto exacto.

**Si falla:** después de reiniciar la VM, levanta las piezas en orden:
```bash
sudo systemctl start docker && docker info
nemoclaw my-assistant status        # también arranca el gateway
nemoclaw my-assistant start         # si el sandbox estaba detenido
nemoclaw my-assistant recover       # si el gateway o el reenvío siguen mal
```

## Receta 3 · ¿Qué ve NemoClaw? (registro y agentes)
```bash
# [host]
nemoclaw list            # sandboxes registrados, con modelo, proveedor y presets
nemoclaw agents list     # runtimes de agente instalados (OpenClaw, Hermes, Deep Agents)
nemoclaw status          # inventario del gateway y servicios auxiliares
```
**Esperado:** `nemoclaw list` muestra el mismo sandbox que la Receta 1, con el modelo y el proveedor (NVIDIA Endpoints).

**Si falla:**
- `No sandboxes registered`, pero `openshell sandbox list` sí muestra uno: el registro `~/.nemoclaw/sandboxes.json` se perdió o está dañado. No borres nada; corre `nemoclaw my-assistant status` y revisa la FAQ.
- `Configuration file is present but is not valid JSON`: registro dañado. Ver "Malformed Registry File" en la documentación de NemoClaw.

## Receta 4 · Salud completa de un sandbox
```bash
# [host]
nemoclaw my-assistant status
```
**Esperado:** salud del sandbox, una prueba de inferencia y la política activa. En la fila de inferencia:

| Valor | Significa | Qué hacer |
|---|---|---|
| `healthy` | Todo bien | Nada |
| `unauthorized` | La ruta responde 401/403: credencial | `nemoclaw credentials reset <PROVIDER>` y `nemoclaw onboard` |
| `unreachable` | No llega al proveedor | Revisa red/DNS de la VM y la Receta 2 |

**Si falla:** `sandbox_container_stopped` → `nemoclaw my-assistant recover`. Solo si eso falla: `nemoclaw my-assistant rebuild --yes`.

## Receta 5 · Eje identidad: el mismo comando en dos planos
```bash
# [host]
id
whoami
# [sandbox] (una sola ejecución, sin abrir shell)
nemoclaw my-assistant exec -- id
```
**Esperado:** en el host, tu usuario de la VM (`[VERIFICAR EN LAB]` probablemente `ubuntu`). En el sandbox, `uid=...(sandbox) gid=...(sandbox)`.

**Equivalente con OpenShell puro:** `openshell sandbox exec -n my-assistant -- id`. Úsalo solo para inspeccionar; para operar, prefiere `nemoclaw`.

**Si falla:** `exec` imprime `nemoclaw: recent network policy denial detected for ...`: es un aviso de una denegación reciente, no un error de `exec`. Para silenciarlo: `NEMOCLAW_NO_POLICY_HINT=1`.

## Receta 6 · Eje archivos: dónde puede escribir el agente
```bash
# [sandbox]
nemoclaw my-assistant exec -- touch /usr/prueba       # debe FALLAR
nemoclaw my-assistant exec -- touch /tmp/prueba       # debe funcionar
nemoclaw my-assistant exec -- ls -la /sandbox/.openclaw/workspace
```
**Esperado:** el primero da `Permission denied` o `Read-only file system` `[VERIFICAR EN LAB]`; el segundo no imprime nada; el tercero lista `SOUL.md`, `AGENTS.md`, `MEMORY.md`, `skills/`…

**Si falla:** si el `touch /usr/prueba` **funciona**, Landlock no se está aplicando (kernel menor a 5.13 o modo `best_effort` degradado). Revisa los logs de arranque del sandbox y anótalo: es un hallazgo.

## Receta 7 · Eje red: qué se bloquea y dónde lo ves
```bash
# [sandbox]
nemoclaw my-assistant exec -- curl -sS https://example.com
# [host]
nemoclaw my-assistant logs --tail 50
nemoclaw my-assistant policy list
```
**Esperado:** `curl: (56) CONNECT tunnel failed, response 403`. En los logs aparece la denegación de `example.com:443`. `policy list` muestra los presets con su origen (p. ej. `[from balanced tier]`).

**Si falla / quieres permitir el host:**
- Temporal (solo esta instancia del sandbox): `openshell term` → elige el sandbox → `r` → la solicitud pendiente → `a` para aprobar. `[VERIFICAR EN LAB]` teclas en OpenShell 0.0.116.
- Persistente: `nemoclaw my-assistant policy add <preset> --dry-run` y luego `--yes`.
- No uses el tier **Personal** salvo para cargas de confianza: abre cualquier host en 80/443 sin aprobaciones.

## Receta 8 · Eje persistencia: lo que sobrevive
```bash
# [host]
nemoclaw my-assistant skill list
nemoclaw my-assistant exec -- cat /sandbox/.openclaw/workspace/SOUL.md
nemoclaw my-assistant sessions list
```
**Esperado:** las skills instaladas (en la 4.3 instalaste `soporte-nemoclaw`), la persona del agente y las sesiones guardadas. `[VERIFICAR EN LAB]` formato de `sessions list`.

**Por qué importa:** todo lo que se escribe aquí vuelve a entrar al contexto en la próxima sesión. Si un atacante logra escribir una skill o editar `SOUL.md`, su instrucción sobrevive.

**Si falla:** `cat: ... No such file`: tu workspace puede tener otro nombre. Lista primero con `nemoclaw my-assistant exec -- ls /sandbox/.openclaw`.

## Receta 9 · Logs: OpenShell vs. NemoClaw (cuidado con `--tail`)
```bash
# [host]
nemoclaw my-assistant logs --tail 50          # 50 líneas y termina
nemoclaw my-assistant logs --since 5m         # últimos 5 minutos
nemoclaw my-assistant logs --follow           # en vivo; sal con Ctrl+C
openshell logs my-assistant -n 20             # 20 líneas, OpenShell puro
```
**Esperado:** logs del gateway y la auditoría de OpenShell (denegaciones de política).

**Si falla:** `openshell logs my-assistant --tail` se queda abierto: en `openshell`, `--tail` **sigue** el log. Sal con Ctrl+C y usa `-n`.

## Receta 10 · Lee la política real (para la ficha comparativa)
```bash
# [host]
openshell policy get my-assistant --full | head -60
```
**Esperado:** el YAML vivo: `filesystem_policy` (`read_only`, `read_write`), `landlock`, `process` (`run_as_user: sandbox`) y `network_policies`. Con esto llenas la Tabla 2 del README **con datos de tu sandbox**.

**Si falla:** el nombre del sandbox está mal. Confírmalo con `openshell sandbox list`.

## Receta 11 · Diagnóstico rápido para reportar un problema
```bash
# [host]
nemoclaw doctor                       # chequeos del host y del gateway (solo lectura)
nemoclaw my-assistant doctor          # Docker, OpenShell, contenedor, puertos, sandbox
nemoclaw debug --quick                # paquete de diagnóstico para un issue
```
**Esperado:** una lista de chequeos con su estado. `debug` genera un archivo para adjuntar a un issue.

**Si falla:** antes de subir el paquete de `debug` a un issue público, revisa que no tenga tokens ni URLs con `#token=`.

## Receta 12 (opcional) · Conoce otro agente de NemoClaw
Solo si tienes tiempo y créditos: crear un segundo sandbox usa disco y memoria de la VM.
```bash
# [host]
nemoclaw onboard --agent hermes                       # o: nemohermes onboard
nemoclaw onboard --agent langchain-deepagents-code    # o: nemo-deepagents onboard
```
**Esperado:** el asistente de onboarding, con el agente ya elegido. Al final, `nemoclaw list` muestra dos sandboxes.

**Si falla:**
- `Invalid sandbox name`: usa de 1 a 19 caracteres, minúsculas, que empiece con letra (p. ej. `mi-hermes`).
- Errores de memoria al crear el sandbox: la VM no aguanta dos sandboxes. Borra el de prueba con `nemoclaw <nombre> destroy --yes`.
- `[VERIFICAR EN LAB]` si los alias `nemohermes` y `nemo-deepagents` vienen instalados en la imagen del launchable.

## Receta 13 · Cierra sin gastar de más
```bash
exit                         # sal de la VM
brev stop <instancia>        # en tu computadora
brev ls                      # confirma STOPPED
```
**Si falla:** `instance "<instancia>" does not support stop.` → guarda tu trabajo (`brev copy <instancia>:/ruta ./local`) y usa `brev delete <instancia>`. Encendida = se cobra cómputo; detenida = solo disco; eliminada = nada, pero pierdes los datos.
