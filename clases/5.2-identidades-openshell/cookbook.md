# Cookbook 5.2 · Identidad y límites dentro del sandbox

Recetas para el laboratorio NemoClaw en Brev, todas desde el navegador. Todas son **de solo lectura o se limpian solas**: ninguna cambia la política ni rompe el agente.

**Convenciones**
- `my-assistant` es el nombre del sandbox del launchable. Si el tuyo es otro, cámbialo (receta 0).
- Los comandos van en la **VM TERMINAL** del tablero de tu laboratorio (la terminal de operador, usuario `ubuntu`). `openshell sandbox exec` los ejecuta dentro del sandbox por ti.
- Haz clic dentro del área negra antes de escribir. **Shift + Esc** cierra la terminal.
- Cada `openshell sandbox exec` abre una shell nueva y corta. Si tu comando usa tuberías (`|`) o `&&`, envuélvelo en `sh -c '...'`; si no, el `|` lo interpreta la shell del host.
- Todos los comandos `nemoclaw` imprimen `ExperimentalWarning: SQLite is an experimental feature`. Ignórala.
- Las salidas "esperadas" vienen de una prueba real del laboratorio. Donde una prueba no se repitió, la receta te dice qué buscar en lugar de prometer el texto exacto.

---

## 0 · Abre la terminal de operador y encuentra tu sandbox

En la consola de Brev, ve a **Compute** → tu instancia → botón verde **NemoClaw**. En el tablero, haz clic en **VM TERMINAL**. Estos comandos listan los sandboxes y revisan que el laboratorio esté sano:

```bash
openshell sandbox list
nemoclaw my-assistant status
openshell status
```

Esperado: una fila `my-assistant` con `PHASE Ready`; en `status`, la inferencia `healthy` y la fase `Ready`; en `openshell status`, el gateway `nemoclaw-18080` en `https://127.0.0.1:18080` con `Status Connected`.

**Si falla**
- No aparece `my-assistant`: usa el nombre que sí aparece en `openshell sandbox list` en todas las recetas.
- La fila no está lista: `nemoclaw my-assistant recover` y vuelve a listar.

## 1 · ¿Quién es el agente? Dos terminales, dos poderes

**Dentro del cuarto.** En el tablero, haz clic en **SANDBOX TERMINAL** y escribe:

```bash
whoami
pwd
id
```

Esperado:
```text
sandbox
/sandbox
uid=998(sandbox) gid=998(sandbox) …
```

**Afuera, como operador.** Cierra con **Shift + Esc**, abre la **VM TERMINAL** y escribe:

```bash
whoami
id
```

Esperado: `ubuntu` y `uid=1000(ubuntu) …`, con `sudo` y `docker` entre los grupos. El operador puede administrar la máquina y sus contenedores; el agente no.

**Desde la VM TERMINAL, hacia adentro.** Las dos formas de preguntarle al sandbox sin entrar:

```bash
openshell sandbox exec -n my-assistant -- id
nemoclaw my-assistant exec -- whoami
nemoclaw my-assistant exec -- pwd
```

Esperado: `uid=998(sandbox) gid=998(sandbox)`, `sandbox` y `/sandbox`.

**Y preguntándole al agente** (un turno sin abrir el chat):
```bash
nemoclaw my-assistant agent -m "Usa tu herramienta exec para ejecutar whoami y pwd, y dime en una frase qué usuario eres y dónde estás."
```
Compara con lo que viste tú. En una prueba del curso, desde el chat, el agente dijo que trabajaba en `/sandbox/.openclaw/workspace` pero afirmó ser `gateway-owner`; el usuario real es `sandbox`. Como operador, **verificas** lo que el agente afirma de sí mismo (clase 4.2).

**Si falla**
- `uid=0(root)`: usaste `docker exec` (corre como root). Usa siempre `openshell sandbox exec` o `nemoclaw … exec`.
- El agente no ejecuta nada: puede tener la herramienta `exec` deshabilitada o pedir aprobación. Anótalo: lo que cuenta es lo que viste tú en la terminal.

## 2 · La autoridad del proceso, de un vistazo

```bash
openshell sandbox exec -n my-assistant -- grep -E '^(Uid|Gid|NoNewPrivs|Seccomp|Seccomp_filters|CapEff|CapBnd)' /proc/self/status
```

Esperado (las líneas que importan):
```text
NoNewPrivs:     1          ← no puede ganar privilegios con binarios setuid
Seccomp:        2          ← filtro seccomp activo (modo filter)
CapEff: 0000000000000000   ← sin capacidades efectivas de root
```

Es la forma más segura de comprobar seccomp: **solo lee** un archivo del kernel. No intenta nada peligroso.

**Si falla**
- `Seccomp: 0`: el filtro no está activo para ese proceso. Anótalo y repórtalo; no sigas a la receta 4 suponiendo que seccomp bloquea.

## 3 · Pedir más autoridad y clasificar el mensaje

Primero, las tres pruebas que ya vimos en el laboratorio:

```bash
openshell sandbox exec -n my-assistant -- sudo id
openshell sandbox exec -n my-assistant -- touch /usr/local/bin/prueba-curso
openshell sandbox exec -n my-assistant -- sh -c 'touch /tmp/prueba-curso && echo "tmp: se puede escribir" && rm /tmp/prueba-curso'
```

Esperado: `sudo` da `command not found`; `touch` en `/usr/local/bin` da `Permission denied`; en `/tmp` sí se puede escribir (y el archivo se borra).

Después, más intentos de pedir poder. Todos **deberían fallar**; no hay un texto fijo que esperar. Lee el mensaje de cada uno y clasifícalo con la tabla:

```bash
openshell sandbox exec -n my-assistant -- nsenter -t 1 -m -- id
openshell sandbox exec -n my-assistant -- docker ps
openshell sandbox exec -n my-assistant -- dd if=/proc/1/environ of=/dev/null status=none
```

| Mensaje | Qué significa |
|---|---|
| `command not found` | La herramienta no está en la imagen (NemoClaw quita utilidades). No prueba ningún límite. |
| `Permission denied` (`EACCES`) | Permisos de archivo o Landlock negaron el acceso. |
| `Operation not permitted` (`EPERM`) | El kernel negó la operación: falta de capacidades o seccomp. |

**Si falla** (es decir, si alguna funciona): anota cuál y repórtalo. Que `sudo id` devuelva `uid=0` sería un hallazgo serio.

## 4 · seccomp: `setuid`, `ptrace` y `mount` sin romper nada

Tres llamadas que seccomp excluye, probadas con Python sin efectos secundarios:

```bash
# setuid: intentar volverse root
openshell sandbox exec -n my-assistant -- python3 -c 'import os; os.setuid(0)'

# ptrace: PTRACE_TRACEME sobre el propio proceso, que termina enseguida
openshell sandbox exec -n my-assistant -- python3 -c 'import ctypes, os; l = ctypes.CDLL(None, use_errno=True); r = l.ptrace(0, 0, None, None); print(r, os.strerror(ctypes.get_errno()))'

# mount: montar un tmpfs en un directorio temporal propio
openshell sandbox exec -n my-assistant -- python3 -c 'import ctypes, os, tempfile; l = ctypes.CDLL(None, use_errno=True); d = tempfile.mkdtemp(); r = l.mount(b"none", d.encode(), b"tmpfs", 0, None); print(r, os.strerror(ctypes.get_errno())); os.rmdir(d)'
```

Esperado en `setuid`: `PermissionError: [Errno 1] Operation not permitted`. En `ptrace` y `mount` deberías ver un `-1` con un mensaje de error; clasifícalo con la tabla de la receta 3.

Importante: `EPERM` **no te dice** si lo frenó seccomp o la falta de capacidades. Por eso la receta 2 lee `/proc/self/status`: ahí ves que ambas defensas están puestas.

**Si falla**
- `python3: command not found`: la imagen cambió. Salta esta receta; la receta 2 ya muestra las defensas.
- `ptrace` devuelve `0`: seccomp permitió `PTRACE_TRACEME`. No es grave por sí solo (no da acceso a otros procesos), pero anótalo.

## 5 · Permisos por binario

En la política del laboratorio, `docs.openclaw.ai` está en el grupo `openclaw_docs`, pero ese grupo no deja pasar a `curl`.

```bash
# 5a · curl hacia un destino que la política nombra... para otro programa
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://docs.openclaw.ai; echo "salida=$?"
```
Esperado: `curl: (56) CONNECT tunnel failed, response 403`, `code=000` y `salida=56`. El proxy negó la conexión por el programa.

Ahora intenta engañar al guardia. Según la documentación de NemoClaw, OpenShell no mira el nombre que dice el programa (`argv[0]`, que se puede falsificar): lee la ruta real del ejecutable en `/proc/<pid>/exe`, recorre los procesos padre y guarda un hash SHA256 de cada binario la primera vez que lo ve (*trust-on-first-use*). Pruébalo y anota qué pasa:

```bash
# 5b · Falsificar argv[0]: curl se presenta como "openclaw"
openshell sandbox exec -n my-assistant -- bash -c 'exec -a /usr/local/bin/openclaw curl -sS -m 8 -o /dev/null -w "code=%{http_code}\n" https://docs.openclaw.ai'

# 5c · Copiar curl con el nombre "openclaw" en /tmp (se borra al final)
openshell sandbox exec -n my-assistant -- sh -c 'cp /usr/bin/curl /tmp/openclaw && /tmp/openclaw -sS -m 8 -o /dev/null https://docs.openclaw.ai; echo "salida=$?"; rm -f /tmp/openclaw'
```
Si el guardia funciona como dice la documentación, las dos deberían terminar igual que 5a. Si alguna pasa, anótalo y compártelo en el foro del curso.

```bash
# 5d · ¿Y si reemplazo el binario permitido? /usr es de solo lectura
openshell sandbox exec -n my-assistant -- touch /usr/local/bin/prueba-curso
```
Esperado: `touch: cannot touch '/usr/local/bin/prueba-curso': Permission denied`.

```bash
# 5e · Ahora se lo pides al agente
nemoclaw my-assistant agent -m "Abre https://docs.openclaw.ai y dime en una línea de qué trata la página."
```
Lo que pasó en la prueba del curso: el agente intentó con `curl` y después con `node`; el guardia **negó los dos**. Aun así, el agente respondió con una frase creíble sobre OpenClaw, sacada de lo que ya sabía. Una respuesta no prueba que hubo acceso. La prueba está en el registro:

```bash
# 5f · El registro te dice quién fue bloqueado y por qué
nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4
```
Esperado, algo como esto (recortado):
```text
[sandbox] [OCSF ] [ocsf] NET:OPEN [MED] DENIED /usr/bin/curl(11932) -> docs.openclaw.ai:443 [policy:- engine:opa] [reason:binary '/usr/bin/curl' not allowed in policy 'openclaw_docs' (ancestors: [/usr/bin/bash -> /usr/local/bin/node -> /usr/bin/bash], cmdline: …
… DENIED /usr/local/bin/node(11950) -> docs.openclaw.ai:443 … [reason:binary '/usr/local/bin/node' not allowed in policy 'openclaw_docs' …
```
Léela así: **quién** (el binario y su número de proceso), **sus procesos padre** (`ancestors`: aquí se ve que el `curl` lo lanzó el agente, que corre sobre `node`), **a dónde** (`docs.openclaw.ai:443`) y **por qué** (el binario no está en `openclaw_docs`).

**Si falla**
- 5a responde `code=200`: tu política permite `docs.openclaw.ai` para curl (tier o preset distinto). Mira la política (clase 5.3, receta 1) y elige otro destino.
- Ves `nemoclaw: recent network policy denial detected for …`: es una pista informativa de `nemoclaw … exec`, no un error nuevo.
- 5f no muestra nada: el agente quizá no intentó salir y respondió de memoria. Pídeselo otra vez, más explícito («usa una herramienta para descargar la página»), y repite 5f.
- No cambies la política para "arreglar" 5e: eso es la clase 5.3.

## 6 · Las credenciales reales nunca entran al sandbox

```bash
# Nombres de variables con key/token. Muestra el placeholder y oculta cualquier otro valor.
openshell sandbox exec -n my-assistant -- sh -c 'env | grep -iE "key|token" | sed -E "s/=(openshell:resolve:env:).*/=\1…/; t; s/=.*/=<oculto>/"'
```
Esperado, entre otras líneas:
```text
NVIDIA_INFERENCE_API_KEY=openshell:resolve:env:…
OPENCLAW_GATEWAY_TOKEN=<oculto>
```
La primera es un **placeholder**. El proxy L7 de OpenShell lo cambia por la key real solo cuando la petición sale por la ruta permitida hacia NVIDIA. La segunda es el token del gateway de OpenClaw: ese sí vive en el sandbox (no es la credencial del proveedor, pero es un secreto). Por eso el filtro lo tapa.

```bash
# ¿Hay alguna key nvapi- escrita en el sandbox?
openshell sandbox exec -n my-assistant -- sh -c 'grep -rIl "nvapi-" /sandbox 2>/dev/null | wc -l'
```
Deberías ver `0`.

```bash
# En la VM TERMINAL: qué credenciales guarda NemoClaw (los valores no se muestran)
nemoclaw credentials list
openshell provider list
```
Deberías ver nombres de credenciales y proveedores, sin valores. Si tu versión muestra otro formato, busca que ninguna línea imprima una `nvapi-` completa.

**Si falla**
- No sale ninguna variable `…KEY`: los sandboxes que usan la ruta `inference.local` no reciben ni el placeholder. La key tampoco está dentro.
- El conteo de `nvapi-` es mayor que 0: **detente**. Alguien pegó una key en un archivo del workspace. Rótala en build.nvidia.com y bórrala del archivo.
- Nunca corras `env` sin filtro frente a cámara, en un chat ni en la SANDBOX TERMINAL: imprime el token del gateway.

## 7 · Las reglas, en el panel del guardia (OPENSHELL TUI)

Es la forma visual de ver lo mismo que las recetas 2 a 5.

1. En el tablero, haz clic en **OPENSHELL TUI**.
2. Pantalla principal: **Tab** cambia de panel, **j**/**k** mueven la selección, **Enter** abre, **:** abre la línea de comandos y **q** sale. Selecciona `my-assistant` y presiona **Enter**.
3. Vista del sandbox: muestra las carpetas de solo lectura y de lectura y escritura, y las reglas de red. Teclas: **h** cambia de pestaña, **s** abre una shell, **l** muestra el registro, **r** abre las reglas y **d** borra el sandbox. **No presiones d.**
4. Presiona **r** (Rules). Si hiciste la receta 5, verás peticiones pendientes, por ejemplo de `openclaw_docs` con `curl`. Las teclas son **a** (Approve), **x** (Reject), **A** (Approve All) y **p** (Policy). En esta clase solo las miras; decidir es tema de la clase 5.3.

**Si falla**
- El panel se ve cortado: agranda la ventana del navegador.
- No ves peticiones pendientes: provoca una con la receta 5a y vuelve a presionar **r**.
