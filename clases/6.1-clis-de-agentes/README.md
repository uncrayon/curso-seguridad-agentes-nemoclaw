# 6.1 · Compara CLIs de agentes modernos

Aprende a comparar cualquier agente de CLI con cinco preguntas, y comprueba las respuestas en la shell real de tu laboratorio.

| | |
|---|---|
| **Duración del video** | ≈8 min |
| **Práctica** | Laboratorio en Brev · [cookbook.md](cookbook.md) |
| **Habilidad** | Comparar agentes por su superficie de riesgo y elegir según la tarea |
| **Material** | [Diapositivas](slides.html) · [FAQ del curso](../../FAQ.md) |

## Lo esencial (sin tecnicismos)

**La idea:** Claude Code, Codex, Cursor, Hermes, Deep Agents y OpenClaw funcionan igual por dentro: leen, deciden, usan herramientas y repiten. Lo que cambia es qué pueden hacer desde el primer día y si hay un cuarto cerrado que los frene. Para compararlos bastan cinco preguntas: qué puede escribir, con quién habla, como quién corre, qué recuerda al cerrar y quién lo frena si se equivoca.

**Piénsalo como:** contratar asistentes distintos: todos hacen trámites por ti, pero cambia qué llaves les das el primer día y si trabajan en un cuarto con cerradura o en tu sala.

**Palabras nuevas:** CLI de agente (un [agente](../../GLOSARIO.md) que vive en la [terminal](../../GLOSARIO.md) y trabaja con tus archivos), configuración por defecto o *default* (lo que viene de fábrica, como un celular nuevo), persistencia (lo que queda escrito en la libreta del asistente cuando cierras).

**Hazlo sin programar (≈10 min):** Elige un agente que uses o que te interese y llena la ficha de cinco ejes del [Reto](#reto) leyendo su documentación oficial en el navegador: qué archivos puede tocar, con qué sitios habla, como quién corre, qué recuerda y qué lo frena, con un enlace por fila. Si no encuentras una respuesta, escribe "no documentado": también es un hallazgo. Si tienes tu instancia encendida, presiona los botones de **Abre un shell real en el launchable** en la [lección 04b](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/04b-modern-clis.html) y anota qué ves.

**Qué te llevas:** Puedes elegir un agente para una tarea según el riesgo que estás dispuesto a aceptar, no según la publicidad.

**Tu crédito:** esta práctica usa ≈20 min de instancia encendida `[VERIFICAR EN LAB]`. Al terminar, detén la instancia (ver [LABORATORIO.md](../../LABORATORIO.md)).

## Lo que vas a lograr
- Explicar por qué Claude Code, Codex, Cursor, Hermes, Deep Agents y OpenClaw son **el mismo loop con distintos defaults**.
- Comparar agentes con cinco ejes: **archivos, red, identidad, persistencia y sandbox por defecto**.
- Verificar esos ejes en tu laboratorio con `openshell` y `nemoclaw`, y elegir herramienta según la tarea y el riesgo.

## Antes de empezar
- Tu laboratorio NemoClaw en Brev funcionando (clase [4.1](../4.1-laboratorio-nemoclaw-en-brev/README.md)). Si lo detuviste, enciéndelo con `brev start <instancia>`.
- La CLI de Brev con sesión iniciada (`brev ls` muestra tu instancia).
- Haber leído la política de tu sandbox (clase [5.3](../5.3-sandbox-y-politicas/README.md)). Hoy la usamos para comparar.

## La idea en un minuto
Todos estos agentes envuelven lo mismo: **una carpeta de trabajo, una paleta de herramientas, una memoria, ejecución desatendida opcional (cron, tareas largas) y una red**. Lo que cambia es qué viene abierto por defecto y si hay un runtime debajo que frene una llamada mala.

> La CLI fija los valores iniciales. El sandbox de OpenShell decide hasta dónde llegan.

### Tabla 1 · Los CLIs tal como los instalas
Fuente: lección 04b de NVIDIA. Lo que 04b no dice está marcado `[VERIFICAR]`: revísalo en la documentación de la versión que instales, porque los defaults cambian entre versiones.

| Agente | Archivo de instrucciones | Archivos | Red | Identidad | Persistencia | Sandbox por defecto |
|---|---|---|---|---|---|---|
| **Claude Code** | `CLAUDE.md` | Reglas de herramientas y modo de permisos deciden qué se edita sin preguntar | `[VERIFICAR]` | Tu usuario del sistema `[VERIFICAR]` | `CLAUDE.md`, configuración del proyecto `[VERIFICAR]` | Ajustes de sandbox configurables; no asumas que vienen activos `[VERIFICAR]` |
| **Codex CLI** | `AGENTS.md` | Edita y ejecuta solo dentro de los límites del sandbox | Según la configuración del sandbox `[VERIFICAR]` | Tu usuario `[VERIFICAR]` | `AGENTS.md` `[VERIFICAR]` | Sandbox + política de aprobación |
| **Cursor** | `.cursor/rules/*.mdc` | Edita el workspace en general **sin** aprobación | Lo que permitan tu editor y tu SO | Tu usuario | Reglas `.mdc` | No hay política de kernel aparte; los comandos de terminal piden aprobación por defecto |
| **Hermes** | Skills y memoria persistente (en NemoClaw, `SOUL.md`) | Depende del backend de terminal | Integraciones de mensajería `[VERIFICAR]` | Depende del backend `[VERIFICAR]` | Skills, memoria, tareas programadas | El modo de aprobación y el backend de terminal deciden el aislamiento |
| **Deep Agents Code** (`dcode`) | `[VERIFICAR]` (04b no lo cubre) | `[VERIFICAR]` | `[VERIFICAR]` | `[VERIFICAR]` | Skills y memoria | UI de aprobación de herramientas `[VERIFICAR]` |
| **OpenClaw** | `SOUL.md`, `AGENTS.md` | El workspace | Lo que permita el host `[VERIFICAR]` | `[VERIFICAR]` | Sesiones del gateway, cron, skills, `SOUL.md` | En este curso corre **dentro de OpenShell** |

### Tabla 2 · Los tres agentes dentro de NemoClaw
NemoClaw no es solo OpenClaw: soporta **OpenClaw** (por defecto), **Hermes** (`nemohermes`) y **LangChain Deep Agents Code** (`nemo-deepagents`, binario `dcode`). Fuente: blueprint y políticas del repo NVIDIA/NemoClaw (octubre 2026).

| Eje | OpenClaw · `nemoclaw` | Hermes · `nemohermes` | Deep Agents · `nemo-deepagents` |
|---|---|---|---|
| **Archivos** (escritura) | `/tmp`, `/sandbox/.openclaw`, `/sandbox/.nemoclaw`, workdir. Sistema en solo lectura | `/sandbox`, `/sandbox/.hermes`, `/tmp` | `/sandbox`, `/sandbox/.deepagents`, `/tmp` |
| **Landlock** | `best_effort` | `best_effort` | `strict`: si no se puede aplicar, el sandbox **no arranca** |
| **Red** | Denegada por defecto. Lista corta: NVIDIA, clawhub, openclaw.ai, npm (solo el binario `openclaw`) | Denegada por defecto. NVIDIA, endpoints de Nous Research, PyPI | Denegada por defecto. NVIDIA, GitHub, PyPI. OpenShell ve a `dcode` como Python: el permiso aplica a **todo** Python del sandbox |
| **Identidad** | Usuario `sandbox`, no root. `ptrace`, `mount` y `setuid` bloqueados | Usuario `sandbox` | Usuario `sandbox` |
| **Persistencia** | Workspace (`SOUL.md`, `AGENTS.md`, `MEMORY.md`), skills, cron | `/sandbox/.hermes`: `SOUL.md`, memorias, skills, cron, mensajería | `/sandbox/.deepagents`: skills, memoria, `config.toml` |
| **Interfaz** | Gateway + dashboard (puerto 18789) | Gateway, dashboard y API compatible con OpenAI | Solo terminal (TUI o `dcode -n`). Sin gateway ni dashboard |
| **Credenciales** | La key queda en el gateway de OpenShell; nunca entra al sandbox | Igual | Igual |

## Paso a paso
La práctica completa, con salidas esperadas y qué hacer si falla, está en **[cookbook.md](cookbook.md)**. Resumen:

1. **Conéctate a la VM.**
   ```bash
   brev ls
   brev shell <instancia>
   ```
   Deberías ver el prompt de la VM. Alternativa sin terminal local: la celda "Abre un shell real en el launchable" de la [lección 04b](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/04b-modern-clis.html).

2. **Inventario: qué agentes y sandboxes hay.**
   ```bash
   openshell sandbox list
   openshell status
   nemoclaw list
   nemoclaw agents list
   ```
   Deberías ver tu sandbox (p. ej. `my-assistant`), el gateway activo y el agente instalado (OpenClaw).

3. **Salud del sandbox.**
   ```bash
   nemoclaw my-assistant status
   ```
   Busca la fila de inferencia: `healthy` es lo esperado. `unauthorized` = credencial; `unreachable` = ruta.

4. **Eje identidad: el mismo comando en dos planos.**
   ```bash
   id
   nemoclaw my-assistant exec -- id
   ```
   Deberías ver tu usuario de la VM en el primero y `sandbox` en el segundo.

5. **Eje archivos.**
   ```bash
   nemoclaw my-assistant exec -- touch /usr/prueba
   nemoclaw my-assistant exec -- touch /tmp/prueba
   ```
   El primero falla (sistema de solo lectura); el segundo funciona.

6. **Eje red.**
   ```bash
   nemoclaw my-assistant exec -- curl -sS https://example.com
   ```
   Deberías ver `curl: (56) CONNECT tunnel failed, response 403`: la política de red lo bloqueó.

7. **Eje persistencia.**
   ```bash
   nemoclaw my-assistant exec -- ls /sandbox/.openclaw/workspace
   nemoclaw my-assistant skill list
   ```
   Ahí viven `SOUL.md`, `AGENTS.md`, `MEMORY.md` y las skills: lo que sobrevive entre sesiones.

8. **Logs: dónde mirar cuando algo se bloquea.**
   ```bash
   nemoclaw my-assistant logs --tail 50
   ```
   Deberías ver la denegación de `example.com` del paso 6.

9. **Llena tu ficha** (ver Reto) y **detén la instancia** al terminar: `brev stop <instancia>`.

## Cómo elegir herramienta
Responde cuatro preguntas: **¿quién mira?**, **¿qué toca?**, **¿con quién habla?** y **¿qué sobrevive?**

| Tarea | Riesgo principal | Elige | Por qué |
|---|---|---|---|
| Programar contigo al lado, en tu repo | Ediciones o comandos que no revisaste | Claude Code, Codex o Cursor con aprobaciones activas | Tú eres el control: aprueba comandos y revisa el diff |
| Refactor largo y desatendido de un repo | Nadie mira; el agente instala paquetes y ejecuta código | Deep Agents (`nemo-deepagents`) o un CLI dentro de OpenShell | Landlock `strict`, red mínima, credenciales fuera del sandbox |
| Asistente 24/7 al que le escribes por chat | Contenido no confiable + datos + salida al exterior (trifecta) | OpenClaw o Hermes dentro de NemoClaw | Política deny-by-default, aprobación de red en `openshell term`, logs de auditoría |
| Tarea programada (cron) que lee datos y escribe un reporte | Una directiva envenenada se repite cada día | Cualquiera dentro de un sandbox + skill revisada | La persistencia (skills, cron) es superficie de ataque |
| Explorar una idea en 10 minutos | Bajo, si no hay datos sensibles | El CLI que ya tengas | No compliques; pero no le des tus keys de producción |

Regla práctica: **si la tarea junta las tres patas de la trifecta (5.1), el agente va dentro de un sandbox.** Elegir herramienta es elegir qué riesgo aceptas.

## Comprueba que funcionó
- [ ] `openshell sandbox list` y `nemoclaw list` muestran el mismo sandbox.
- [ ] `nemoclaw <sandbox> status` reporta la inferencia como `healthy`.
- [ ] `id` dentro del sandbox muestra el usuario `sandbox`.
- [ ] Escribir en `/usr` falló y en `/tmp` funcionó.
- [ ] `curl` a un host fuera de la lista dio `CONNECT tunnel failed, response 403` y lo viste en los logs.
- [ ] Llenaste la ficha de cinco ejes para un agente que usas.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `openclaw: command not found` en la shell de la VM | Estás en el **host**, no en el sandbox. `openclaw` vive dentro del sandbox | Usa `nemoclaw <sandbox> exec -- <comando>` o `nemoclaw <sandbox> connect` |
| `curl: (56) CONNECT tunnel failed, response 403` | La política de red bloqueó el host. No es un error de TLS | Es lo esperado en el paso 6. Para permitir un host: `openshell term` (temporal) o `nemoclaw <sandbox> policy add` (persistente) |
| `nemoclaw list` dice que no hay sandboxes, pero `openshell sandbox list` sí muestra uno | El sandbox no se creó con NemoClaw, o el registro `~/.nemoclaw/sandboxes.json` está dañado | Revisa `nemoclaw <sandbox> status`. Si el sandbox es de NemoClaw, no lo gestiones con `openshell sandbox create/delete` |
| `ssh: Could not resolve hostname <instancia>` | La IP cambió tras reiniciar o falta el `Include` de Brev en `~/.ssh/config` | `brev refresh`; si sigue, mueve la línea `Include` de Brev al inicio de `~/.ssh/config` |
| `brev shell <instancia> --host` se queda colgado | La ruta `--host` cambió en versiones recientes de la CLI | Usa `brev shell <instancia>` sin `--host` |
| La fila de inferencia en `status` dice `unauthorized` | La credencial guardada no sirve (key rotada o vencida) | Rota la key: `nemoclaw credentials reset <PROVIDER>` y luego `nemoclaw onboard` |
| `openshell logs <sandbox> --tail` no termina | En `openshell`, `--tail` **sigue** el log; en `nemoclaw`, es un número de líneas | Usa `openshell logs <sandbox> -n 20` o `nemoclaw <sandbox> logs --tail 20` |

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
- NVIDIA DLI · [Agentes de CLI modernos (04b)](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/04b-modern-clis.html). Esta clase está basada en la lección 04b del curso de NVIDIA DLI (Apache-2.0).
- NemoClaw · [Soporte de plataformas y agentes](https://docs.nvidia.com/nemoclaw/latest/) (`docs/reference/platform-support.mdx`) y [Ecosistema Hermes / Deep Agents](https://github.com/NVIDIA/NemoClaw/tree/main/docs/about).
- Claude Code · [Permisos](https://code.claude.com/docs/en/permissions)
- Codex · [Aprobaciones y seguridad](https://learn.chatgpt.com/docs/agent-approvals-security)
- Cursor · [Seguridad del agente](https://cursor.com/docs/agent/security)
- Hermes · [Guía de seguridad](https://hermes-agent.nousresearch.com/docs/user-guide/security/)
- LangChain · [Deep Agents Code](https://docs.langchain.com/oss/python/deepagents/code/overview)
