# Cookbook 5.2 · Identidad y límites dentro del sandbox

Recetas de terminal para el laboratorio NemoClaw en Brev. Todas son **de solo lectura o se limpian solas**: ninguna cambia la política ni rompe el agente.

**Convenciones**
- `my-assistant` es el nombre del sandbox del launchable. Si el tuyo es otro, cámbialo (receta 0).
- Corre los comandos en el **host** del lab (no dentro del sandbox). `openshell sandbox exec` los ejecuta dentro por ti.
- Cada `openshell sandbox exec` abre una shell nueva y corta. Si tu comando usa tuberías (`|`) o `&&`, envuélvelo en `sh -c '...'`; si no, el `|` lo interpreta la shell del host.
- Las salidas "esperadas" vienen de la documentación de NemoClaw y de la lección 04a de NVIDIA. Las marcadas `[VERIFICAR EN LAB]` se confirman en la prueba previa.

---

## 0 · Conéctate y encuentra tu sandbox

```bash
brev shell <tu-instancia>          # sin --host en el launchable de NemoClaw
openshell sandbox list
nemoclaw my-assistant status
```

Deberías ver una fila `my-assistant` en estado listo, y en `status` la inferencia como `healthy`.

**Si falla**
- `brev shell` se queda en "waiting for instance to be ready": `brev refresh` y reintenta (FAQ de Brev, clase 4.1).
- No aparece `my-assistant`: usa el nombre que sí aparece en `openshell sandbox list` en todas las recetas.
- La fila no está lista: `nemoclaw my-assistant recover` y vuelve a listar.

## 1 · ¿Quién es el agente? (`whoami`, `id`, `pwd`)

```bash
openshell sandbox exec -n my-assistant -- whoami
openshell sandbox exec -n my-assistant -- id
openshell sandbox exec -n my-assistant -- pwd
```

Esperado:
```text
sandbox
uid=…(sandbox) gid=…(sandbox) groups=…(sandbox)
/sandbox
```
`[VERIFICAR EN LAB]` los números de `uid`/`gid` y el `pwd` exacto de `openshell sandbox exec` (con `nemoclaw … exec` el `HOME` es `/sandbox`).

Lo mismo con la CLI de NemoClaw (corre como el usuario `sandbox` con `HOME=/sandbox`):
```bash
nemoclaw my-assistant exec -- id
```

Y preguntándole **al agente** (un turno sin abrir el chat):
```bash
nemoclaw my-assistant agent -m "Usa tu herramienta exec para ejecutar whoami y pwd, y dime en una frase qué usuario eres y dónde estás."
```
Esperado: una frase como "Soy el usuario sandbox y estoy en /sandbox". Compara con lo que viste tú: como operador, **verificas** lo que el agente afirma (clase 4.2).

**Si falla**
- `uid=0(root)`: estás en un contenedor equivocado o usaste `docker exec` (corre como root). Usa siempre `openshell sandbox exec` o `nemoclaw … exec`.
- El agente no ejecuta nada: puede tener la herramienta `exec` deshabilitada o pedir aprobación. Revisa la página 04a, celda "🩺 Health check" (receta 7), que lista aprobaciones pendientes.

## 2 · La autoridad del proceso, de un vistazo

```bash
openshell sandbox exec -n my-assistant -- grep -E '^(Uid|Gid|NoNewPrivs|Seccomp|Seccomp_filters|CapEff|CapBnd)' /proc/self/status
```

Esperado `[VERIFICAR EN LAB]`:
```text
Uid:    …  (no 0)
NoNewPrivs:     1          ← no puede ganar privilegios con binarios setuid
Seccomp:        2          ← filtro seccomp activo (modo filter)
Seccomp_filters:        1 o más
CapEff: 0000000000000000   ← sin capacidades efectivas de root
```

Es la forma más segura de comprobar seccomp: **solo lee** un archivo del kernel. No intenta nada peligroso.

**Si falla**
- `Seccomp: 0`: el filtro no está activo para ese proceso. Anótalo y repórtalo; no sigas a la receta 4 suponiendo que seccomp bloquea.

## 3 · Pedir más autoridad (catálogo de NVIDIA 04a)

```bash
openshell sandbox exec -n my-assistant -- sudo id
openshell sandbox exec -n my-assistant -- nsenter -t 1 -m -- id
openshell sandbox exec -n my-assistant -- docker ps
openshell sandbox exec -n my-assistant -- dd if=/proc/1/environ of=/dev/null status=none
```

Todas deberían fallar. **Lee el mensaje**, porque cada uno cuenta una historia distinta:

| Mensaje | Qué significa |
|---|---|
| `command not found` | La herramienta no está en la imagen (NemoClaw quita utilidades). No prueba ningún límite. |
| `Permission denied` (`EACCES`) | Permisos de archivo o Landlock negaron el acceso. |
| `Operation not permitted` (`EPERM`) | El kernel negó la operación: falta de capacidades o seccomp. |

`[VERIFICAR EN LAB]` el mensaje y el código de salida de cada una en la imagen actual.

**Si falla** (es decir, si alguna funciona): anota cuál y repórtalo. Que `sudo id` devuelva `uid=0` sería un hallazgo serio.

## 4 · seccomp: `ptrace`, `mount` y `setuid` sin romper nada

Tres llamadas que seccomp excluye, probadas con Python sin efectos secundarios:

```bash
# setuid: intentar volverse root
openshell sandbox exec -n my-assistant -- python3 -c 'import os; os.setuid(0)'

# ptrace: PTRACE_TRACEME sobre el propio proceso, que termina enseguida
openshell sandbox exec -n my-assistant -- python3 -c 'import ctypes, os; l = ctypes.CDLL(None, use_errno=True); r = l.ptrace(0, 0, None, None); print(r, os.strerror(ctypes.get_errno()))'

# mount: montar un tmpfs en un directorio temporal propio
openshell sandbox exec -n my-assistant -- python3 -c 'import ctypes, os, tempfile; l = ctypes.CDLL(None, use_errno=True); d = tempfile.mkdtemp(); r = l.mount(b"none", d.encode(), b"tmpfs", 0, None); print(r, os.strerror(ctypes.get_errno())); os.rmdir(d)'
```

Esperado `[VERIFICAR EN LAB]`:
```text
PermissionError: [Errno 1] Operation not permitted
-1 Operation not permitted
-1 Operation not permitted
```

Importante: `EPERM` **no te dice** si lo frenó seccomp o la falta de capacidades. Por eso la receta 2 lee `/proc/self/status`: ahí ves que ambas defensas están puestas.

**Si falla**
- `python3: command not found`: la imagen cambió. Usa la celda de la página 04a (receta 7) o salta esta receta.
- `ptrace` devuelve `0`: seccomp permitió `PTRACE_TRACEME`. No es grave por sí solo (no da acceso a otros procesos), pero anótalo para la prueba previa.

## 5 · Permisos por binario: el host está permitido, el binario no

En la política base, `docs.openclaw.ai` solo se permite para `/usr/local/bin/openclaw`.

```bash
# 5a · curl hacia un host permitido... para otro binario
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://docs.openclaw.ai
```
Esperado: `curl: (56) CONNECT tunnel failed, response 403`. El proxy negó la conexión porque el binario es `curl`.

```bash
# 5b · Falsificar argv[0]: curl se presenta como "openclaw"
openshell sandbox exec -n my-assistant -- bash -c 'exec -a /usr/local/bin/openclaw curl -sS -m 8 -o /dev/null -w "code=%{http_code}\n" https://docs.openclaw.ai'
```
Esperado: el mismo 403. OpenShell no mira `argv[0]` (se puede falsificar). Lee la ruta real del ejecutable en `/proc/<pid>/exe`, recorre los procesos padre y calcula un hash SHA256 de cada binario la primera vez que lo ve (*trust-on-first-use*).

```bash
# 5c · Copiar curl con el nombre "openclaw" en /tmp (se borra al final)
openshell sandbox exec -n my-assistant -- sh -c 'cp /usr/bin/curl /tmp/openclaw && /tmp/openclaw -sS -m 8 -o /dev/null https://docs.openclaw.ai; echo "salida=$?"; rm -f /tmp/openclaw'
```
Esperado: 403 y `salida=56`. La ruta real es `/tmp/openclaw`, no `/usr/local/bin/openclaw`.

```bash
# 5d · ¿Y si reemplazo el binario permitido? /usr es de solo lectura
openshell sandbox exec -n my-assistant -- touch /usr/local/bin/prueba-curso
```
Esperado: `touch: cannot touch '/usr/local/bin/prueba-curso': Permission denied`. Y si alguien lograra cambiar el binario, el hash ya no coincidiría y OpenShell negaría la solicitud.

```bash
# 5e · Ahora el binario correcto: se lo pides al agente
nemoclaw my-assistant agent -m "Abre https://docs.openclaw.ai y dime en una línea de qué trata la página."
```
Esperado `[VERIFICAR EN LAB]`: el agente responde con el contenido. Mismo destino, otro binario, otra respuesta.

```bash
# 5f · El log te dice quién fue bloqueado y por qué
nemoclaw my-assistant logs --tail 30
```
Busca una línea de denegación con el binario `/usr/bin/curl` y el host `docs.openclaw.ai:443`. `[VERIFICAR EN LAB]` el formato exacto de la línea.

**Si falla**
- 5a responde `code=200`: tu política permite `docs.openclaw.ai` para curl (tier o preset distinto). Mira la política (clase 5.3, receta 1) y elige otro host que solo tenga `openclaw`.
- Ves `nemoclaw: recent network policy denial detected for …`: es una pista informativa de `nemoclaw … exec`, no un error nuevo. Se silencia con `NEMOCLAW_NO_POLICY_HINT=1`.
- 5e falla: el agente quizá no tiene herramienta de navegación activa. No cambies la política para "arreglarlo"; anótalo.

## 6 · Las credenciales reales nunca entran al sandbox

```bash
# Nombres de variables con key/token. Muestra el placeholder y oculta cualquier otro valor.
openshell sandbox exec -n my-assistant -- sh -c 'env | grep -iE "key|token" | sed -E "s/=(openshell:resolve:env:).*/=\1…/; t; s/=.*/=<oculto>/"'
```
Esperado `[VERIFICAR EN LAB]`:
```text
NVIDIA_INFERENCE_API_KEY=openshell:resolve:env:…
```
Es un **placeholder**. El proxy L7 de OpenShell lo cambia por la key real solo cuando la petición sale por la ruta permitida hacia `integrate.api.nvidia.com`. Puede que veas otras variables `<oculto>` (por ejemplo, el token del gateway de OpenClaw, que sí vive en el sandbox y no es una credencial del proveedor).

```bash
# ¿Hay alguna key nvapi- escrita en el sandbox?
openshell sandbox exec -n my-assistant -- sh -c 'grep -rIl "nvapi-" /sandbox 2>/dev/null | wc -l'
```
Esperado: `0`.

```bash
# En el HOST: dónde vive la key de verdad (los valores nunca se muestran)
nemoclaw credentials list
openshell provider list
```

**Si falla**
- No sale ninguna variable `…KEY`: los sandboxes creados antes de NemoClaw v0.0.132 usan la ruta `inference.local`, donde el sandbox no recibe ni el placeholder. La key tampoco está dentro.
- El conteo de `nvapi-` es mayor que 0: **detente**. Alguien pegó una key en un archivo del workspace. Rótala en build.nvidia.com y bórrala del archivo.
- Nunca corras `env` sin filtro frente a cámara o en un chat: imprime tokens.

## 7 · En la página 04a de NVIDIA

Abre [04a · El sandbox de OpenShell](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/04a-safety.html) con el launchable abierto en otra pestaña y conectado desde la página 03a (Kickstart).

1. **Salud primero.** En el bloque "Detect & recover", ejecuta **🩺 Health check**. Si sale `✗ DEGRADED`, ejecuta **🛠 Recover** y repite.
2. **Identidad.** En la celda **"Pregunta cualquier cosa al entorno, en código"**, abre el código y agrega esta línea al inicio del arreglo `questions`:
   ```js
   ["¿Quién soy?", ["whoami", "id", "pwd"]],
   ```
   Ejecuta. Lee el bloque "¿Qué ocurre cuando estos comandos solicitan más permisos?": son las pruebas de la receta 3, con su código de salida.
3. **Binario.** Ejecuta **"Lee la política activa del launchable"**. En el mapa que se dibuja abajo, cambia el **binario que llama** de `curl` a `openclaw` y mira cómo cambian los destinos permitidos.
4. En el selector de escenarios elige **"reach the inference API as a stray curl, not the runtime"** (está en inglés). Pulsa **Predecir** y luego **Confirmar**. `[VERIFICAR EN LAB]` el resultado de Confirmar con la ruta nativa del proveedor de NVIDIA.

**Si falla**
- "Mantén el launchable abierto en otra pestaña, vuelve a ejecutar y comprueba el nombre con: openshell sandbox list": la página perdió la sesión con tu launchable. Reabre el launchable y reconéctate en 03a.
- "No exit status arrived. Check the runtime before running more probes.": ejecuta 🩺 Health check y 🛠 Recover antes de seguir.
