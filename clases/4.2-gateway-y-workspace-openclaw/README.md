# 4.2 · Explora el gateway y el workspace de OpenClaw

Abre la carpeta que define a tu agente, compara lo que el agente dice de sí mismo con lo que hay en disco y personalízalo para el proyecto Soporte NemoClaw.

| | |
|---|---|
| Duración del video | ≈8 min |
| Práctica | Laboratorio en Brev: página del curso de NVIDIA + terminal ([cookbook.md](cookbook.md)) |
| Habilidad | Orientación (sin habilidad evaluada) |

Material: [diapositivas](slides.html) · [recetario de terminal](cookbook.md) · [preguntas frecuentes del curso](../../FAQ.md)

> Basado en la lección 03b-openclaw del curso de NVIDIA DLI (Apache-2.0).

## Lo esencial (sin tecnicismos)

**La idea:** Tu agente es lo que dicen unos archivos de texto en su carpeta de trabajo: su personalidad, sus reglas y su memoria. Hoy los abres, comparas lo que el agente dice de sí mismo con lo que de verdad está escrito y le das el puesto de Soporte NemoClaw.

**Piénsalo como:** un edificio de oficinas. La recepción recibe los mensajes (el gateway), el asistente trabaja en su escritorio (el workspace) y sobre el escritorio están el reglamento y la descripción del puesto (SOUL.md).

**Palabras nuevas:** [gateway](../../GLOSARIO.md), [workspace](../../GLOSARIO.md), [SOUL.md](../../GLOSARIO.md).

**Hazlo sin programar (≈10 min):** Escribe en español normal la sección «Proyecto: Soporte NemoClaw» de tu `SOUL.md`: a quién ayuda tu agente, en qué idioma y con qué tono responde, y tres cosas que nunca hace. Si tu laboratorio está encendido, en la [lección 03b](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/03b-openclaw.html) presiona **▶ Ejecutar** en Paso 1 y en Paso 1b, y anota si la lista que da el agente coincide con los archivos reales.

**Qué te llevas:** puedes definir por escrito la personalidad y los límites de un agente, y sabes que lo que el agente dice se comprueba en el archivo.

**Tu crédito:** esta práctica usa ≈20 min de instancia encendida `[VERIFICAR EN LAB]`. Al terminar, detén la instancia (ver [LABORATORIO.md](../../LABORATORIO.md)).

## Lo que vas a lograr

- Nombrar las piezas de OpenClaw (gateway, sesiones, workspace) y qué archivo del workspace moldea cada parte del comportamiento.
- Verificar como operador, con `cat`, lo que el agente afirma sobre sus archivos y su memoria.
- Personalizar `SOUL.md` y `MEMORY.md` para que tu agente se comporte como **Soporte NemoClaw**.

## Antes de empezar

- La clase 4.1 terminada: instancia en `RUNNING` y **Probar conexión** en verde en la [lección 03a](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/03a-kickstart.html). La página 03b reutiliza esa conexión.
- Para la ruta de terminal: `brev shell <instancia>` funcionando (cookbook 4.1, receta 5).
- El nombre de tu sandbox (normalmente `my-assistant`; confírmalo con `nemoclaw list`).

## Las piezas, en una tabla

| Pieza | Dónde vive | Qué hace |
|---|---|---|
| Gateway de OpenClaw | Dentro del sandbox; llega a tu máquina por el puerto 18789 | Recibe cada turno, corre el loop del agente, sirve el dashboard y el WebSocket. |
| Gateway de OpenShell | En el host, puerto 8080 (solo local) | Maneja el ciclo de vida del sandbox, las rutas de inferencia y los puertos. |
| Sesiones | En el gateway de OpenClaw | El historial de cada conversación, identificado por su clave (`sessionKey`). |
| Workspace | `/sandbox/.openclaw/workspace/` | Archivos Markdown que el agente lee **al inicio de cada sesión**. Es su configuración. |

El workspace, archivo por archivo:

| Archivo | Qué define |
|---|---|
| `SOUL.md` | Personalidad, límites, tono y valores. |
| `AGENTS.md` | Instrucciones de operación y reglas: memoria, seguridad, flujo de cada sesión. |
| `IDENTITY.md` | Tarjeta corta: nombre, idioma, emoji. |
| `USER.md` | Quién es la persona a la que ayuda y sus preferencias. Empieza vacío. |
| `TOOLS.md` | Notas de uso de cada herramienta. |
| `HEARTBEAT.md` | Lista de tareas periódicas (lo vemos en 4.3). |
| `POLICY.md` | Resumen de la política de red, escrito por NemoClaw. |
| `memory/` | Notas diarias `AAAA-MM-DD.md` que el agente agrega mientras trabaja. Se crea la primera vez que el agente guarda una nota. |
| `MEMORY.md` | Memoria de largo plazo, depurada. Se carga en la sesión principal. Se crea la primera vez que el agente la usa. |
| `skills/` | Una carpeta por skill, con su `SKILL.md` (lo vemos en 4.3). |

Un detalle que causa muchos errores: dentro del sandbox, `~` es `/sandbox`, **no** el workspace. `~/SOUL.md` apunta a `/sandbox/SOUL.md`, que el agente no lee como su personalidad. Usa siempre la ruta completa `/sandbox/.openclaw/workspace/SOUL.md`.

## Paso a paso

### Parte A · Pide al agente que se describa (página del curso)

1. **Abre la lección** [El agente OpenClaw](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/03b-openclaw.html). Revisa que la pastilla de arriba diga **OpenClaw ✓**. Si dice **OpenClaw ⚠**, vuelve a la 03a, copia una cookie nueva y repite **Probar conexión**.

2. **Ejecuta Paso 1 · Pide al agente que se describa.** En la celda **Pide a OpenClaw que describa su workspace**, haz clic en **▶ Ejecutar**. El mensaje que envía es:
   > Briefly list the files in your workspace and explain each in one bullet without dumping file contents.

   Si quieres la versión en español, abre el código y cambia el texto de `content:` por:
   ```js
   content: "Enumera brevemente los archivos de tu workspace y explica cada uno en una viñeta, sin volcar su contenido.",
   ```
   Deberías ver: una lista de archivos con una explicación por viñeta. **Anótala**: es lo que el agente *dice*.

### Parte B · Verifica como operador

3. **Ejecuta Paso 1b · Lee el workspace tú mismo.** La celda **Lee el workspace en vivo en la terminal del operador** abre una terminal de operador (por WebSocket) y entra al sandbox con `openshell sandbox connect <nombre>`. El nombre lo saca de `GET /api/agent`. Corre estos comandos:
   ```js
   const commands = [
     "ls .openclaw/workspace",
     "echo '=== SOUL.md ==='; cat .openclaw/workspace/SOUL.md",
     "echo '=== daily memory ==='; ls -1 .openclaw/workspace/memory/ 2>/dev/null",
     "echo '=== MEMORY.md ==='; cat .openclaw/workspace/MEMORY.md 2>/dev/null || echo '(no curated MEMORY.md yet; the agent writes it in a main session)'",
   ];
   ```
   Puedes editar la lista. Por ejemplo, agrega `"cat .openclaw/workspace/AGENTS.md"` o `"ls -la .openclaw/workspace/skills"`.

   Deberías ver: la lista real de archivos y el contenido de `SOUL.md`. Es normal que `MEMORY.md` y `memory/` todavía no existan.

4. **Compara.** ¿El agente mencionó un archivo que no existe? ¿Se le olvidó alguno? Esa diferencia es el punto de la clase: **lo que el agente dice no es evidencia; el archivo sí**.

   Por qué funciona así: el launchable tiene dos planos de autoridad. La terminal de operador corre **fuera** del sandbox. El agente corre **dentro**, con una política más estrecha.

5. **(Ruta de terminal)** Lo mismo desde `brev shell <instancia>`:
   ```bash
   openshell sandbox list
   openshell sandbox connect my-assistant       # o: nemoclaw my-assistant connect
   ```
   Ya dentro del sandbox:
   ```bash
   whoami; pwd
   cd /sandbox/.openclaw/workspace
   ls -la
   cat SOUL.md
   cat AGENTS.md
   exit
   ```
   Detalle en el [cookbook](cookbook.md), recetas 1 a 4.

### Parte C · El agente edita su propia memoria

6. **Ejecuta Paso 3 · El agente edita su propio contexto.** En el flujo **Verifica la memoria en archivos entre sesiones distintas**, haz clic en **▶ Ejecutar todo**:
   - **Guarda y verifica una preferencia:** en una sesión nueva le pide al agente "Añade esta preferencia a MEMORY.md sin sustituir el contenido existente: …" con una etiqueta `course-review-…` y una referencia `REF-…`. Luego **lee el archivo** y falla si la preferencia no está.
   - **Lee desde una conversación nueva:** abre otra sesión y le pide leer `MEMORY.md` e informar la referencia.

   Deberías ver: `Se verificó la nota añadida en disco. Permanece en MEMORY.md para examinarla.` y la referencia recuperada en la segunda sesión.

   Que el agente diga "guardado" no basta. La celda lo comprueba leyendo el archivo.

7. **Hazlo con tu propia preferencia.** En la parte **Prueba · conversa con tu agente activo** de la misma página, escribe:
   > Añade esta línea al final de /sandbox/.openclaw/workspace/MEMORY.md sin borrar nada: "soporte-pref-01: responde en español neutro y cita el archivo de la FAQ que usaste. Referencia REF-4821."

   Verifica con la celda de operador (agrega `"tail -n 5 .openclaw/workspace/MEMORY.md"` a `commands`) y luego, en una conversación nueva, pregunta:
   > Lee MEMORY.md e indica la preferencia y la referencia de soporte-pref-01.

   Deberías ver: `REF-4821` en el archivo y en la respuesta de la sesión nueva.

### Parte D · Personaliza SOUL.md para Soporte NemoClaw

8. **Respalda y edita como operador.** Desde `brev shell <instancia>`:
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
   ```
   Deberías ver: las últimas líneas con la sección "Proyecto: Soporte NemoClaw".

9. **Comprueba el cambio en una sesión nueva.** El agente lee el workspace al inicio de cada sesión, así que pregúntale en una conversación nueva (en **Prueba · conversa con tu agente activo** o con la receta 7 del cookbook):
   > ¿Quién eres, a quién ayudas y qué nunca haces?

   Deberías ver: menciona el curso, el español neutro y que nunca pide API keys.

   Si quieres volver al original: `nemoclaw my-assistant upload ./SOUL.md.original /sandbox/.openclaw/workspace/SOUL.md`.

## Comprueba que funcionó

- [ ] Tienes anotada la lista de archivos que dio el agente y la lista real de `ls`, y sabes si coinciden.
- [ ] Leíste `SOUL.md` y `AGENTS.md` como operador.
- [ ] El flujo **Verifica la memoria en archivos entre sesiones distintas** terminó en verde.
- [ ] `REF-4821` está en `MEMORY.md` y una sesión nueva lo recupera.
- [ ] `SOUL.md` tiene la sección "Proyecto: Soporte NemoClaw" y una sesión nueva la refleja.
- [ ] Tienes `SOUL.md.original` como respaldo.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| El agente dice "listo, lo guardé" pero el archivo no cambió | El modelo reporta una acción que no hizo, o escribió en otra ruta. | Verifica siempre con `cat` como operador. Pídele de nuevo con la ruta completa y que lea el archivo de vuelta. |
| Editaste `~/SOUL.md` y el agente no cambió | `~` es `/sandbox`, no el workspace. Escribiste `/sandbox/SOUL.md`. | Usa `/sandbox/.openclaw/workspace/SOUL.md` (o `$OPENCLAW_WORKSPACE_DIR/SOUL.md`). Borra el archivo suelto. |
| Cambiaste `SOUL.md` y la conversación abierta sigue igual | El workspace se lee al iniciar cada sesión. | Abre una sesión nueva para probar. |
| `MEMORY.md` o `memory/` no existen | El agente aún no ha guardado memoria. | Es normal. Se crean la primera vez que el agente guarda algo. |
| `Pairing required` / `Device pairing required` en el dashboard | OpenClaw exige emparejar el dispositivo (desde OpenClaw 2026.9.1 no se puede saltar). | Espera unos minutos y recarga, o **Overview → Gateway Access → Connect**. Si sigue: receta 9 del cookbook (`openclaw devices list --json` y `openclaw devices approve <requestId>`). |
| `gateway connect failed: GatewayClientRequestError: scope upgrade pending approval (requestId: ...)` | Una conexión pide más permisos y espera aprobación. | Apruébala igual que el pairing: receta 9 del cookbook. |
| Corriste `openclaw update` dentro del sandbox y se colgó | OpenClaw viene fijado en la imagen del sandbox. No se actualiza en el lugar. | No lo hagas. Cancela con `Ctrl+C`. En una instalación propia se actualiza con `nemoclaw update` y luego `nemoclaw <nombre> rebuild`; en el launchable del curso, no toques versiones. |
| `No hay un nombre válido de sandbox conectado.` en la celda de operador | La página no obtuvo el nombre del sandbox desde `/api/agent`. | Vuelve a la 03a y repite **Probar conexión**. |
| `La lectura del archivo no contenía la preferencia guardada` | El agente no escribió la línea, o la reemplazó en otra parte. | Revisa el trace del turno (filas ⚙️). Ejecuta **Comprobación de estado** y reintenta. |

## Reto

**Haz que el agente demuestre lo que guarda.** Agrega esta regla al final de `AGENTS.md` (con el mismo método de download, edición y upload del paso 8):

```text
- Cada vez que digas que guardaste algo en un archivo, léelo de vuelta y cita la línea exacta que quedó escrita.
```

Criterio de éxito: en una sesión nueva le pides guardar una preferencia en `MEMORY.md`, su respuesta incluye la línea leída de vuelta y `cat` como operador confirma que esa línea existe.

## Avance del proyecto

Tu agente ya tiene la identidad de **Soporte NemoClaw**:

- `SOUL.md` con la sección del proyecto (idioma, categorías de triage, regla de no pedir keys).
- `MEMORY.md` con la preferencia `soporte-pref-01` (citar el archivo de la FAQ).

Guarda en tu repo `proyecto/SOUL-soporte.md` con la sección que agregaste y repite la pregunta de la línea base de 4.1 ("Mi notebook responde HTTP 401"). Anota en `proyecto/linea-base-4.1.md` qué cambió. Todavía no conoce la FAQ: eso llega en 4.3 con la skill `soporte-nemoclaw`.

## Recursos

- [Lección 03b · El agente OpenClaw (NVIDIA DLI, español)](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/03b-openclaw.html)
- [NemoClaw · Estado del sandbox y archivos del workspace](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/manage-sandboxes/workspace-files.md)
- [NemoClaw · Referencia de comandos](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands.md) (`connect`, `exec`, `agent`, `sessions`, `download`, `upload`)
- [NemoClaw · Troubleshooting](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/troubleshooting.md) (pairing, `openclaw update`)
- [MemGPT: memoria por niveles para LLMs (arXiv 2310.08560)](https://arxiv.org/abs/2310.08560)
