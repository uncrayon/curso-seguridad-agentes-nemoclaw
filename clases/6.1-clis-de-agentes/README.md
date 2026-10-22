# 6.1 · Compara CLIs de agentes modernos

Aprende a comparar cualquier agente de CLI con cinco preguntas, compruébalas en la terminal real de tu laboratorio y cierra el laboratorio sin gastar de más.

| | |
|---|---|
| **Duración del video** | ≈8 min |
| **Práctica** | Laboratorio en Brev: tablero de NemoClaw + terminal del navegador ([cookbook.md](cookbook.md)) |
| **Habilidad** | Comparar agentes por su superficie de riesgo y elegir según la tarea |
| **Material** | [Diapositivas](slides.html) · [FAQ del curso](../../FAQ.md) |

> Basado en la lección 04b del curso NVIDIA DLI «NemoClaw» (Apache-2.0) y en el repo NVIDIA/NemoClaw.

> **El Módulo 6 es opcional**, y la práctica de laboratorio de esta clase también. Si la haces, hazla en la misma sentada, después de la 5.3 y antes de borrar la instancia (≈20 min, ≈USD 0.08). Si ya la borraste al terminar la 5.3, sáltala: puedes leer esta guía y ver el video sin laboratorio.

## Lo esencial (sin tecnicismos)

**La idea:** Claude Code, Codex, Cursor, Hermes, Deep Agents y OpenClaw funcionan igual por dentro: leen, deciden, usan herramientas y repiten. Lo que cambia es qué pueden hacer desde el primer día y si hay un cuarto cerrado que los frene. Para compararlos bastan cinco preguntas: qué puede escribir, con quién habla, como quién corre, qué recuerda al cerrar y quién lo frena si se equivoca.

**Piénsalo como:** contratar asistentes distintos: todos hacen trámites por ti, pero cambia qué llaves les das el primer día y si trabajan en un cuarto con cerradura o en tu sala.

**Palabras nuevas:** CLI de agente (un [agente](../../GLOSARIO.md) que vive en la [terminal](../../GLOSARIO.md) y trabaja con tus archivos), configuración por defecto o *default* (lo que viene de fábrica, como un celular nuevo), persistencia (lo que queda escrito en la libreta del asistente cuando cierras).

**Hazlo sin programar (≈10 min):** Elige un agente que uses o que te interese y llena la ficha de cinco ejes del [Reto](#reto) leyendo su documentación oficial en el navegador: qué archivos puede tocar, con qué sitios habla, como quién corre, qué recuerda y qué lo frena, con un enlace por fila. Si no encuentras una respuesta, escribe "no documentado": también es un hallazgo. Si tienes tu laboratorio encendido, compara con tu agente usando solo clics: en el tablero de NemoClaw, mira el estado de seguridad (sitios permitidos y políticas de red); presiona **OPENSHELL TUI**, entra a tu sandbox y mira qué carpetas son de solo lectura y cuáles de escritura; y en **CHAT WITH AGENT** pregúntale "¿Como qué usuario corres y en qué carpeta trabajas?". Anota su respuesta: en la práctica vas a comprobar que un agente no siempre dice la verdad sobre sí mismo.

**Qué te llevas:** Puedes elegir un agente para una tarea según el riesgo que estás dispuesto a aceptar, no según la publicidad.

**Tu crédito:** esta práctica usa ≈20 min de tu sesión única de laboratorio (ver [LABORATORIO.md](../../LABORATORIO.md)). Al terminar: si vas a hacer la parte opcional de laboratorio de la 6.2, deja la instancia encendida y sigue; si no, guarda lo que quieras y **Delete**.

## Lo que vas a lograr
- Explicar por qué Claude Code, Codex, Cursor, Hermes, Deep Agents y OpenClaw son **el mismo loop con distintos defaults**.
- Comparar agentes con cinco ejes: **archivos, red, identidad, persistencia y sandbox por defecto**.
- Verificar esos ejes en tu laboratorio desde la **VM TERMINAL** con `openshell` y `nemoclaw`, y elegir herramienta según la tarea y el riesgo.
- Cerrar el laboratorio: guardar lo tuyo, borrar la instancia y revisar tu saldo.

## Antes de empezar
- Tu instancia de Brev en **Running** y el tablero de NemoClaw abierto: en la consola de Brev, tu instancia, botón verde **NemoClaw** (clase [4.1](../4.1-laboratorio-nemoclaw-en-brev/README.md)).
- Haber hecho la [4.3](../4.3-agentes-siempre-activos/README.md) (instalaste la skill `soporte-nemoclaw`) y la [5.3](../5.3-sandbox-y-politicas/README.md) (leíste la política de tu sandbox). Hoy las usamos para comparar.

## La idea en un minuto
Todos estos agentes envuelven lo mismo: **una carpeta de trabajo, una paleta de herramientas, una memoria, ejecución desatendida opcional (cron, tareas largas) y una red**. Lo que cambia es qué viene abierto por defecto y si hay un runtime debajo que frene una llamada mala.

> La CLI fija los valores iniciales. El sandbox de OpenShell decide hasta dónde llegan.

### Tabla 1 · Los CLIs tal como los instalas
Fuente: lección 04b de NVIDIA. Donde dice "ver su documentación", 04b no lo cubre: revísalo en la documentación de la versión que instales, porque los defaults cambian entre versiones.

| Agente | Archivo de instrucciones | Archivos | Red | Identidad | Persistencia | Sandbox por defecto |
|---|---|---|---|---|---|---|
| **Claude Code** | `CLAUDE.md` | Reglas de herramientas y modo de permisos deciden qué se edita sin preguntar | Ver su documentación | Tu usuario del sistema (confírmalo en su documentación) | `CLAUDE.md` y configuración del proyecto | Ajustes de sandbox configurables; no asumas que vienen activos |
| **Codex CLI** | `AGENTS.md` | Edita y ejecuta solo dentro de los límites del sandbox | Según la configuración del sandbox | Tu usuario (confírmalo en su documentación) | `AGENTS.md` | Sandbox + política de aprobación |
| **Cursor** | `.cursor/rules/*.mdc` | Edita el workspace en general **sin** aprobación | Lo que permitan tu editor y tu SO | Tu usuario | Reglas `.mdc` | No hay política de kernel aparte; los comandos de terminal piden aprobación por defecto |
| **Hermes** | Skills y memoria persistente (en NemoClaw, `SOUL.md`) | Depende del backend de terminal | Integraciones de mensajería (ver su documentación) | Depende del backend | Skills, memoria, tareas programadas | El modo de aprobación y el backend de terminal deciden el aislamiento |
| **Deep Agents Code** (`dcode`) | Ver su documentación (04b no lo cubre) | Ver su documentación | Ver su documentación | Ver su documentación | Skills y memoria | UI de aprobación de herramientas (ver su documentación) |
| **OpenClaw** | `SOUL.md`, `AGENTS.md` | El workspace | Fuera de un sandbox, lo que permita el host | Fuera de un sandbox, ver su documentación | Sesiones del gateway, cron, skills, `SOUL.md` | En este curso corre **dentro de OpenShell** |

### Tabla 2 · Los tres agentes dentro de NemoClaw
NemoClaw no es solo OpenClaw: soporta **OpenClaw** (por defecto), **Hermes** (`nemohermes`) y **LangChain Deep Agents Code** (`nemo-deepagents`, binario `dcode`). Los tres comandos vienen instalados en la VM del laboratorio. Fuente: blueprint y políticas del repo NVIDIA/NemoClaw (octubre 2026).

| Eje | OpenClaw · `nemoclaw` | Hermes · `nemohermes` | Deep Agents · `nemo-deepagents` |
|---|---|---|---|
| **Archivos** (escritura) | `/tmp`, `/sandbox/.openclaw`, `/sandbox/.nemoclaw`, workdir. Sistema en solo lectura | `/sandbox`, `/sandbox/.hermes`, `/tmp` | `/sandbox`, `/sandbox/.deepagents`, `/tmp` |
| **Landlock** | `best_effort` | `best_effort` | `strict`: si no se puede aplicar, el sandbox **no arranca** |
| **Red** | Denegada por defecto. Lista corta por programa: NVIDIA, clawhub, openclaw.ai, npm. En tu laboratorio, el grupo de `docs.openclaw.ai` no deja salir ni a `curl` ni a `node` | Denegada por defecto. NVIDIA, endpoints de Nous Research, PyPI | Denegada por defecto. NVIDIA, GitHub, PyPI. OpenShell ve a `dcode` como Python: el permiso aplica a **todo** Python del sandbox |
| **Identidad** | Usuario `sandbox` (uid 998), no root. `ptrace`, `mount` y `setuid` bloqueados | Usuario `sandbox` | Usuario `sandbox` |
| **Persistencia** | Workspace (`SOUL.md`, `AGENTS.md`, `USER.md`…; `MEMORY.md` solo si el agente guardó memoria), skills, cron | `/sandbox/.hermes`: `SOUL.md`, memorias, skills, cron, mensajería | `/sandbox/.deepagents`: skills, memoria, `config.toml` |
| **Interfaz** | Gateway + chat en el navegador (puerto 18789) | Gateway, dashboard y API compatible con OpenAI | Solo terminal (TUI o `dcode -n`). Sin gateway ni dashboard |
| **Credenciales** | La key queda en el gateway de OpenShell; nunca entra al sandbox | Igual | Igual |

## Paso a paso
La práctica completa, con salidas esperadas y qué hacer si falla, está en **[cookbook.md](cookbook.md)**. Todo pasa en el navegador: el tablero de NemoClaw y su **VM TERMINAL**, la terminal de operador (el host, usuario `ubuntu`). Para correr algo **dentro** del sandbox, el comando empieza con `nemoclaw my-assistant exec --`.

### Parte 1 · Abre la terminal de operador
1. En el tablero de NemoClaw, en la tarjeta **MY-ASSISTANT**, presiona **VM TERMINAL**. Se abre una ventana negra encima del tablero.
2. Haz clic dentro del área negra antes de escribir. Si escribes sin hacer clic, tus teclas activan atajos del tablero. Para cerrarla más tarde: **Shift+Escape**.
3. Cada comando de `nemoclaw` imprime la línea `ExperimentalWarning: SQLite is an experimental feature`. Ignórala: no es un error.

![El tablero de NemoClaw con la tarjeta MY-ASSISTANT y sus cuatro botones; el número marca el botón VM TERMINAL](../../assets/lab/13-panel-nemoclaw.jpg)

### Parte 2 · Inventario: qué sandboxes y agentes hay
1. Para ver los sandboxes que maneja OpenShell:
   ```bash
   openshell sandbox list
   ```
   Deberías ver las columnas `NAME`, `CREATED` y `PHASE`, con `my-assistant` en `Ready`.
2. Para saber si la recepción (el gateway de OpenShell) está conectada:
   ```bash
   openshell status
   ```
   Deberías ver un bloque `Server Status` con el gateway `nemoclaw-18080`, el servidor `https://127.0.0.1:18080`, `Connected`, `Authenticated (mTLS transport)` y la versión `0.0.116`.
3. Para ver lo que registra NemoClaw y confirmar que los otros dos agentes vienen instalados:
   ```bash
   nemoclaw list
   ls /usr/bin/nemohermes /usr/bin/nemo-deepagents
   ```
   `nemoclaw list` muestra `my-assistant` con el agente `openclaw`, el proveedor `nvidia-prod` y sus presets de política. El `ls` imprime las dos rutas: Hermes y Deep Agents están en la VM, aunque hoy no los uses.

### Parte 3 · Salud del sandbox
Para preguntarle a NemoClaw si tu agente está sano:
```bash
nemoclaw my-assistant status
```
Busca la inferencia en `healthy` y la fase en `Ready`. Si dice `unauthorized`, el problema es la credencial; si dice `unreachable`, la ruta hacia el modelo.

### Parte 4 · Los ejes, afuera y adentro
1. **Identidad.** Para preguntar "¿quién soy?" en la VM y luego dentro del sandbox:
   ```bash
   id
   nemoclaw my-assistant exec -- id
   ```
   Afuera ves `uid=1000(ubuntu)` con grupos como `sudo` y `docker`: el operador tiene poder. Adentro ves `uid=998(sandbox) gid=998(sandbox)`: el agente no.
2. **Archivos.** Para intentar crear un archivo vacío en una carpeta del sistema y luego en la carpeta temporal:
   ```bash
   nemoclaw my-assistant exec -- touch /usr/prueba
   nemoclaw my-assistant exec -- touch /tmp/prueba
   ```
   El primero responde `Permission denied`; el segundo no imprime nada, porque funcionó.
3. **Red.** Para pedirle al sandbox una página que no está en su lista:
   ```bash
   nemoclaw my-assistant exec -- curl -sS https://example.com
   ```
   Deberías ver `curl: (56) CONNECT tunnel failed, response 403`: la política de red lo bloqueó.
4. **Persistencia.** Para ver lo que sobrevive entre sesiones:
   ```bash
   nemoclaw my-assistant exec -- ls /sandbox/.openclaw/workspace
   nemoclaw my-assistant skill list
   nemoclaw my-assistant sessions list --json
   ```
   En el workspace ves `AGENTS.md`, `HEARTBEAT.md`, `IDENTITY.md`, `POLICY.md`, `SOUL.md`, `TOOLS.md` y `USER.md`; después de la 4.3, también `faq`, `reportes` y `skills`. Solo verás `MEMORY.md` si el agente guardó memoria. `skill list` da un resumen como `22/57 ready` (el número puede cambiar) e incluye `soporte-nemoclaw`. Con `--json`, las sesiones salen legibles (por ejemplo, `"agentId": "main"`).

![La VM TERMINAL con las comprobaciones de identidad: afuera el usuario ubuntu, adentro el usuario sandbox; los números marcan cada salida](../../assets/lab/16-terminal-identidad-sandbox.png)

### Parte 5 · Quién lo frena: logs y OpenShell TUI
1. Para encontrar el bloqueo del paso de red en el registro:
   ```bash
   nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4
   ```
   Deberías ver una línea parecida a `[OCSF ] [ocsf] NET:OPEN [MED] DENIED /usr/bin/curl(…) -> example.com:443 [policy:- engine:opa] [reason:…]`.
2. (Opcional) Cierra la terminal con **Shift+Escape** y presiona **OPENSHELL TUI** en el tablero. Entra a tu sandbox con **[Enter]** y presiona **[r]** para ver las reglas. Ahí aparecen las solicitudes pendientes, con **[a]** Approve, **[x]** Reject, **[A]** Approve All y **[p]** Policy. Si ves la de `example.com`, recházala con **[x]**: no la necesitas. Sal con **[q]**.

### Parte 6 · Cierra el laboratorio: guarda y borra
Si vas a hacer la parte opcional de laboratorio de la [6.2](../6.2-biblioteca-de-skills/README.md), deja la instancia encendida y sigue con esa clase: allí cierras el laboratorio. Si no, guarda lo que quieras y **Delete**. Al borrar la instancia, todo lo que hay en la VM se pierde.
1. **Guarda lo que quieras.** Los archivos del curso (`~/curso`) ya están en GitHub. Para conservar algo que escribió tu agente, muéstralo en la VM TERMINAL, selecciónalo con el mouse y pégalo en tus notas. Por ejemplo, el reporte de la 4.3:
   ```bash
   nemoclaw my-assistant exec -- cat /sandbox/.openclaw/workspace/reportes/resumen-faq.md
   ```
2. **Borra la instancia.** Cierra la terminal (**Shift+Escape**) y ve a la consola de Brev: **Compute** → tu instancia (`nemoclaw-…`) → **Delete**. Confirma en el aviso que aparece.

   ![La página de la instancia en la consola de Brev con los botones Stop, Delete y NemoClaw; el número marca Delete](../../assets/lab/05-instancia-lista.jpg)

3. **Revisa tu saldo.** En el menú de arriba, abre **Billing** (o mira el saldo en la barra superior). Confirma que la instancia ya no aparece en **Compute**. Si algo no cuadra, revisa [LABORATORIO.md](../../LABORATORIO.md).

## Cómo elegir herramienta
Responde cuatro preguntas: **¿quién mira?**, **¿qué toca?**, **¿con quién habla?** y **¿qué sobrevive?**

| Tarea | Riesgo principal | Elige | Por qué |
|---|---|---|---|
| Programar contigo al lado, en tu repo | Ediciones o comandos que no revisaste | Claude Code, Codex o Cursor con aprobaciones activas | Tú eres el control: aprueba comandos y revisa el diff |
| Refactor largo y desatendido de un repo | Nadie mira; el agente instala paquetes y ejecuta código | Deep Agents (`nemo-deepagents`) o un CLI dentro de OpenShell | Landlock `strict`, red mínima, credenciales fuera del sandbox |
| Asistente 24/7 al que le escribes por chat | Contenido no confiable + datos + salida al exterior (trifecta) | OpenClaw o Hermes dentro de NemoClaw | Política deny-by-default, aprobación de red en la OpenShell TUI, logs de auditoría |
| Tarea programada (cron) que lee datos y escribe un reporte | Una directiva envenenada se repite cada día | Cualquiera dentro de un sandbox + skill revisada | La persistencia (skills, cron) es superficie de ataque |
| Explorar una idea en 10 minutos | Bajo, si no hay datos sensibles | El CLI que ya tengas | No compliques; pero no le des tus keys de producción |

Regla práctica: **si la tarea junta las tres patas de la trifecta (5.1), el agente va dentro de un sandbox.** Elegir herramienta es elegir qué riesgo aceptas.

## Comprueba que funcionó
- [ ] `openshell sandbox list` y `nemoclaw list` muestran el mismo sandbox, y `openshell status` dice `Connected`.
- [ ] `nemoclaw my-assistant status` reporta la inferencia como `healthy`.
- [ ] `id` afuera muestra `ubuntu` y dentro del sandbox muestra `sandbox`.
- [ ] Escribir en `/usr` falló y en `/tmp` funcionó.
- [ ] `curl` a un host fuera de la lista dio `CONNECT tunnel failed, response 403` y viste el `DENIED` en los logs.
- [ ] Llenaste la ficha de cinco ejes para un agente que usas.
- [ ] Borraste tu instancia con **Delete** y ya no aparece en **Compute** (o la dejaste encendida para seguir con la parte de laboratorio de la 6.2).

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Escribes y no aparece nada en la terminal, o se abre algo del tablero | La VM TERMINAL no tiene el foco | Haz clic dentro del área negra y vuelve a escribir |
| `ExperimentalWarning: SQLite is an experimental feature` | Un aviso que imprime cada comando de `nemoclaw` | Ignóralo: no es un error |
| `openclaw: command not found` en la VM TERMINAL | Estás en el **host**, no en el sandbox. `openclaw` vive dentro del sandbox | Usa `nemoclaw my-assistant exec -- <comando>` o el botón **SANDBOX TERMINAL** |
| `curl: (56) CONNECT tunnel failed, response 403` | La política de red bloqueó el host. No es un error de certificados | Es lo esperado en la Parte 4. Para permitir un host: **OPENSHELL TUI** → **[r]** → **[a]** (temporal) o `nemoclaw my-assistant policy add` (persistente, clase 5.3) |
| `openshell gateway status` da error | Ese subcomando no existe | Usa `openshell status` o `openshell gateway info` |
| `sessions list` imprime una tabla ilegible | Es demasiado ancha para la terminal del navegador | Usa `nemoclaw my-assistant sessions list --json` |
| `nemoclaw list` dice que no hay sandboxes, pero `openshell sandbox list` sí muestra uno | El sandbox no se creó con NemoClaw, o el registro `~/.nemoclaw/sandboxes.json` está dañado | Revisa `nemoclaw my-assistant status`. Si el sandbox es de NemoClaw, no lo gestiones con `openshell sandbox create/delete` |
| La inferencia en `status` dice `unauthorized` | La credencial guardada no sirve (key rotada o vencida) | Revisa tu key en build.nvidia.com. Para rotarla: `nemoclaw credentials reset <PROVIDER>` y luego `nemoclaw onboard` |
| `openshell logs <sandbox> --tail` no termina | En `openshell`, `--tail` **sigue** el log; en `nemoclaw`, es un número de líneas | Sal con Ctrl+C y usa `openshell logs <sandbox> -n 20` o `nemoclaw my-assistant logs --tail 20` |

## Reto
Elige **un agente de CLI que uses** (o el que más te interese) y llena esta ficha **con su documentación oficial**:

| Eje | Default | ¿Configurable? | Fuente (enlace) |
|---|---|---|---|
| Archivos | | | |
| Red | | | |
| Identidad | | | |
| Persistencia | | | |
| Sandbox por defecto | | | |

**Criterio de éxito:** las cinco filas tienen fuente. Si una no la encuentras, escribe "no documentado": eso también es un hallazgo de seguridad.

## Avance del proyecto
Agrega a tu proyecto **Soporte NemoClaw** un archivo `docs/eleccion-de-agente.md` con:
1. La Tabla 2 llenada **con lo que viste en tu sandbox** (no con lo que dice esta guía).
2. Una línea: por qué el agente de soporte corre en OpenClaw dentro de NemoClaw y no en un CLI en tu laptop (pista: lee FAQ de desconocidos 24/7 = contenido no confiable).
3. Qué agente usarías tú para **programar** el proyecto, y con qué controles.

## Recursos
- NVIDIA DLI · Agentes de CLI modernos (lección 04b). Esta clase está basada en esa lección del curso NVIDIA DLI «NemoClaw» (Apache-2.0).
- NemoClaw · [Soporte de plataformas y agentes](https://docs.nvidia.com/nemoclaw/latest/) (`docs/reference/platform-support.mdx`) y [Ecosistema Hermes / Deep Agents](https://github.com/NVIDIA/NemoClaw/tree/main/docs/about).
- Claude Code · [Permisos](https://code.claude.com/docs/en/permissions)
- Codex · [Aprobaciones y seguridad](https://learn.chatgpt.com/docs/agent-approvals-security)
- Cursor · [Seguridad del agente](https://cursor.com/docs/agent/security)
- Hermes · [Guía de seguridad](https://hermes-agent.nousresearch.com/docs/user-guide/security/)
- LangChain · [Deep Agents Code](https://docs.langchain.com/oss/python/deepagents/code/overview)
- Brev · [Referencia de la consola](https://docs.nvidia.com/brev/latest/guides/console-reference): instancias, Stop, Delete y Billing.
