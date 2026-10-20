# 4.3 · Agentes en operación continua y programada

Instala la skill `soporte-nemoclaw` con la FAQ del curso, programa una tarea que escribe un resumen sin que nadie escriba en el chat y aprende a describir cualquier automatización con 3 controles.

| | |
|---|---|
| Duración del video | ≈8 min |
| Práctica | Laboratorio en Brev: página del curso de NVIDIA + terminal ([cookbook.md](cookbook.md)) |
| Habilidad | Operar agentes en modo continuo |
| Lección de NVIDIA | [El agente siempre activo (03c-always-on)](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/03c-always-on.html) |

Material: [diapositivas](slides.html) · [recetario de terminal](cookbook.md) · [skill soporte-nemoclaw](skills/soporte-nemoclaw/SKILL.md) · [preguntas frecuentes del curso](../../FAQ.md)

> Basado en la lección 03c-always-on del curso de NVIDIA DLI (Apache-2.0).

## Lo esencial (sin tecnicismos)

**La idea:** Tu agente aprende una tarea nueva leyendo una receta escrita en texto, y empieza a trabajar solo a una hora fija, aunque nadie le escriba. Eso es útil y también es un riesgo: lo que corre solo, corre aunque nadie lo mire.

**Piénsalo como:** una tarjeta de receta (la skill) y la alarma del despertador (la tarea programada).

**Palabras nuevas:** [skill](../../GLOSARIO.md), [cron o tarea programada](../../GLOSARIO.md).

**Hazlo sin programar (≈10 min):** Escribe la descripción de una skill para tu propio trabajo, en 2 o 3 frases: qué resuelve, para quién y con qué palabras pediría ayuda alguien (los errores, productos o situaciones que mencionaría). Compárala con la descripción de [soporte-nemoclaw](skills/soporte-nemoclaw/SKILL.md). Si tu laboratorio está encendido, en la [lección 03c](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/03c-always-on.html) presiona **▶ Ejecutar todo** en Paso 1 y **▶ Ejecutar** en Paso 2, y anota qué archivo apareció sin que nadie escribiera en el chat.

**Qué te llevas:** sabes escribir la descripción que hace que un agente encuentre su receta, y describir cualquier automatización con tres preguntas: qué recuerda, qué instrucciones sigue y qué la hace empezar.

**Tu crédito:** esta práctica usa ≈25 min de instancia encendida `[VERIFICAR EN LAB]`. Al terminar, detén la instancia (ver [LABORATORIO.md](../../LABORATORIO.md)).

## Lo que vas a lograr

- Instalar una skill (una carpeta con `SKILL.md`) en tu agente y comprobar que la usa, primero de forma explícita y luego de forma automática.
- Programar una tarea con el cron del gateway que escribe un archivo sin ningún mensaje de chat, y verificarla como operador.
- Describir cualquier mecanismo "siempre activo" con 3 controles: sesión, directiva y disparador.

## Antes de empezar

- Las clases 4.1 y 4.2 terminadas: instancia en `RUNNING`, **Probar conexión** en verde en la [lección 03a](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/03a-kickstart.html) y `SOUL.md` personalizado.
- `brev shell <instancia>` funcionando.
- En tu computadora, el repositorio del curso con:
  - la skill: [`clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/SKILL.md`](skills/soporte-nemoclaw/SKILL.md)
  - la FAQ del curso: `datos/faq/*.md`

## Los 3 controles

Toda ejecución del agente, la pidas tú o no, se describe con tres preguntas:

- **Sesión:** ¿qué contexto hereda la ejecución?
- **Directiva:** ¿de dónde salen sus instrucciones?
- **Disparador:** ¿qué hace que empiece?

| Mecanismo | Sesión | La directiva vive en | Disparador | En esta clase |
|---|---|---|---|---|
| Skill | Reutiliza la del que la invoca | `workspace/skills/<nombre>/SKILL.md` | Una petición en la conversación | La instalas y la usas |
| Heartbeat | Una sesión dedicada al heartbeat | `HEARTBEAT.md` | Temporizador del gateway, cada 30 min por defecto | Solo concepto |
| Cron | Aislada: una sesión nueva en cada disparo | `payload.message` de la tarea | Una hora programada | La programas y la verificas |
| Subagente | Nueva; el agente padre conserva la referencia | Las instrucciones que le da el padre | El agente padre decide a mitad de un turno | Solo concepto |

## Paso a paso

### Parte A · Mira cómo es una skill (página del curso)

1. **Abre la lección** [El agente siempre activo](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/03c-always-on.html). Revisa que la pastilla diga **OpenClaw ✓**.

2. **Ejecuta Paso 1 · Lee una habilidad y su guía operativa.** En el flujo **Instala una habilidad de práctica y léela explícitamente en una sesión nueva**, haz clic en **▶ Ejecutar todo**:
   - **Instala y verifica los archivos de práctica** crea `/sandbox/.openclaw/workspace/skills/course-triage-<id>/` con un `SKILL.md` y un `runbook.md`, y los lee de vuelta.
   - **Usa la habilidad instalada** abre una sesión nueva y le pide al agente leer ese `SKILL.md` y seguirlo para un incidente de práctica.

   Abre el código del primer nodo y mira la forma del `SKILL.md`:
   ```markdown
   ---
   name: course-triage-<id>
   description: Review a checkout-service incident using the bundled practice runbook; propose changes without executing them.
   ---
   Read runbook.md in this skill directory. Confirm service and time window. ...
   ```
   Deberías ver: la respuesta del agente con la referencia `BOOK-…` del runbook. La celda lo advierte: esto prueba el **uso explícito** (le diste la ruta), no que el agente descubra la skill solo.

### Parte B · Instala la skill soporte-nemoclaw (terminal)

3. **Lleva la skill y la FAQ a la máquina de Brev.** Elige una opción (detalle en el [cookbook](cookbook.md), receta 1):
   ```bash
   # En tu computadora, desde la raíz del repo del curso
   brev copy ./clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw <instancia>:/home/ubuntu/soporte-nemoclaw
   brev copy ./datos/faq <instancia>:/home/ubuntu/faq
   ```
   `[VERIFICAR EN LAB: que brev copy acepte carpetas y que el inicio sea /home/ubuntu]`. Si no, el cookbook trae la skill lista para pegar con un heredoc.

4. **Instálala en el sandbox.** En `brev shell <instancia>`:
   ```bash
   cd ~
   nemoclaw my-assistant skill install ./soporte-nemoclaw/
   nemoclaw my-assistant skill list
   ```
   NemoClaw valida que la carpeta tenga un `SKILL.md` con frontmatter y `name`, y luego llama al comando nativo de OpenClaw (`openclaw skills install … --agent main --force`).
   Deberías ver: `soporte-nemoclaw` en la lista. `[VERIFICAR EN LAB: salida de skill install y skill list]`

5. **Copia la FAQ al workspace:**
   ```bash
   nemoclaw my-assistant upload ./faq/ /sandbox/.openclaw/workspace/faq/
   nemoclaw my-assistant exec --workdir /sandbox/.openclaw/workspace -- ls -la faq
   ```
   Deberías ver: los archivos `.md` de la FAQ dentro de `faq/` (no en `faq/faq/`). `[VERIFICAR EN LAB: cómo anida upload una carpeta]`

### Parte C · Comprueba que el agente la usa

6. **Uso explícito.** En la página 03c, baja a **Prueba · activa una skill durante la conversación** y escribe (o usa la receta 4 del cookbook):
   > Lee /sandbox/.openclaw/workspace/skills/soporte-nemoclaw/SKILL.md y síguelo para esta duda de un estudiante: "brev shell me responde ssh: Could not resolve hostname".

   Deberías ver: una respuesta con **Categoría:** `brev`, pasos numerados y **Fuente:** `faq/<archivo>.md`. Revisa las filas `⚙️`: el agente corrió `ls`, `grep` o `cat` sobre `faq/`. `[VERIFICAR EN LAB: ruta donde quedó instalada la skill]`

7. **Uso automático.** Abre una conversación **nueva** y pregunta **sin** dar la ruta:
   > Un estudiante dice: "Mi notebook responde HTTP 401 cuando llamo al modelo". ¿Qué le respondes?

   Si el agente usa la skill sola, la respuesta trae el formato de la skill y cita la FAQ. Si no, la descripción no fue suficiente: eso es el reto de esta clase.

### Parte D · Observa una escritura programada (página del curso)

8. **Ejecuta Paso 2 · Examina el agente en ejecución.** En el flujo **Observa una escritura programada y elimina la tarea creada**, haz clic en **▶ Ejecutar** en el nodo **Programa, verifica y limpia**. La celda llama al gateway con:
   ```js
   state.call("cron.add", {
     name, schedule: {kind: "at", at: new Date(Date.now() + 15000).toISOString()}, deleteAfterRun: true,
     sessionTarget: "isolated", wakeMode: "now",
     delivery: {mode: "none"},
     payload: {kind: "agentTurn", message: "Write the file specified by the JSON object below. …", timeoutSeconds: 120}
   });
   ```
   Luego consulta `cron.runs` cada 5 segundos, hasta 3 minutos.

   **No escribas nada en el chat mientras espera.** Deja la pestaña abierta hasta que termine la limpieza.

   Deberías ver: `Ejecución programada: Ns transcurridos; ok` y el mensaje de que verificó una ejecución correcta y su archivo nuevo, sin enviar ningún mensaje de chat.

9. **Léelo tú, como operador.** En `brev shell <instancia>`:
   ```bash
   nemoclaw my-assistant exec -- bash -lc 'ls -la /sandbox/.openclaw/workspace/course-cron-*.txt; cat /sandbox/.openclaw/workspace/course-cron-*.txt'
   ```
   Deberías ver: un archivo `course-cron-<id>.txt` con un contenido `CRON-<id>`. Nadie escribió en el chat y el archivo existe: esa es la prueba.

### Parte E · Programa el resumen de Soporte NemoClaw

10. **Abre la lección 03a** y baja al flujo **Gateway · protocolo WebSocket paso a paso**.
    1. Ejecuta **Abre la conexión del gateway**.
    2. Abre el código del nodo **Llama a models.list y cron.list**, borra su contenido y pega esto:

    ```js
    // Tarea programada de Soporte NemoClaw: un resumen de la FAQ, sin mensajes de chat.
    if (!state.call) { helpers.log("Ejecuta primero el nodo Abre la conexión del gateway."); return; }

    const id = helpers.randomId();
    const archivo = "/sandbox/.openclaw/workspace/reportes/resumen-faq-" + id + ".md";
    const cuando = new Date(Date.now() + 60000).toISOString(); // dentro de 60 s, en UTC (termina en Z)

    const job = await state.call("cron.add", {
      name: "soporte-resumen-" + id,
      schedule: { kind: "at", at: cuando },
      deleteAfterRun: true,        // se borra sola después de correr
      sessionTarget: "isolated",   // una sesión nueva en cada disparo
      wakeMode: "now",
      delivery: { mode: "none" },  // no envía mensajes a ningún canal
      payload: {
        kind: "agentTurn",
        timeoutSeconds: 180,
        message: "Lee /sandbox/.openclaw/workspace/skills/soporte-nemoclaw/SKILL.md y sigue su sección Modo reporte. " +
          "Escribe el resumen de la FAQ en " + archivo + ". No modifiques otros archivos ni envíes mensajes."
      }
    });
    if (!job?.id) throw new Error("cron.add no devolvió un id; revisa cron.list");
    helpers.log({ jobId: job.id, programadaPara: cuando, archivo });

    // Revisa el historial cada 5 s, hasta 4 minutos
    const limite = Date.now() + 240000;
    while (Date.now() < limite) {
      const historial = await state.call("cron.runs", { id: job.id, limit: 20 });
      const corridas = historial?.entries || historial?.runs || [];
      helpers.log("estado: " + (corridas[0]?.status || "todavía no corre"));
      if (corridas.some(c => c.status === "ok")) { helpers.log("Listo. Ahora léelo como operador."); return { archivo }; }
      const mala = corridas.find(c => c.status === "error" || c.status === "skipped");
      if (mala) { helpers.log.details("corrida fallida", mala); throw new Error("La ejecución programada falló: " + (mala.error || mala.status)); }
      await helpers.delay(5000, helpers.signal);
    }
    throw new Error("No hubo una ejecución correcta en 4 minutos; revisa cron.list y la hora programada");
    ```

    3. Haz clic en **▶ Ejecutar** en ese nodo. No escribas en el chat.

    `[VERIFICAR EN LAB: este fragmento reutiliza los mismos parámetros de cron.add que la lección 03c; pruébalo antes de grabar]`

    Para volver al código original del nodo, usa **↺ Restablecer**. Ejecutarlo después te muestra `cron.list`: tu tarea ya no debería aparecer, porque `deleteAfterRun` la borra.

11. **Lee el resumen como operador:**
    ```bash
    nemoclaw my-assistant exec -- bash -lc 'ls -la /sandbox/.openclaw/workspace/reportes/ && cat /sandbox/.openclaw/workspace/reportes/resumen-faq-*.md'
    ```
    Deberías ver: un Markdown con una sección por categoría, preguntas con su archivo fuente y la línea "Generado por la skill soporte-nemoclaw".

### Parte F · Heartbeat y subagentes (solo concepto)

- **Heartbeat:** cada cierto tiempo (30 min por defecto en OpenClaw) el agente despierta en una sesión dedicada, revisa pendientes y lee `HEARTBEAT.md` si existe. NemoClaw configura esa sesión aislada para que tu actividad normal no lo sustituya. En el laboratorio no lo cambies; en una instalación propia se ajusta con `NEMOCLAW_AGENT_HEARTBEAT_EVERY` antes del onboarding o con `openclaw config set agents.defaults.heartbeat.every 2h` dentro del sandbox (`0m` lo apaga). Ningún paso de esta clase lo dispara: no lo esperes.
- **Subagentes:** el agente padre lanza un hijo con una sesión nueva y le pasa instrucciones de tarea, como los subagentes de la clase 3.3. La diferencia: aquí el hijo corre dentro del mismo sandbox, con la misma política.

**Atención:** una tarea programada corre aunque nadie la esté mirando. Una instrucción como "envía el reporte diario" se dispara igual. Cada disparo usa una sesión aislada, pero los archivos compartidos del workspace sí pueden influir en ejecuciones futuras. Nombra tus tareas, revisa `cron.list` y borra las que no reconozcas.

## Comprueba que funcionó

- [ ] El flujo de la skill de práctica de la 03c terminó con la referencia `BOOK-…`.
- [ ] `nemoclaw my-assistant skill list` muestra `soporte-nemoclaw`.
- [ ] `faq/` está en el workspace con los archivos de la FAQ.
- [ ] Una pregunta con la ruta de la skill devuelve **Categoría**, pasos y **Fuente: faq/…**.
- [ ] El cron de la 03c terminó en `ok` y leíste `course-cron-<id>.txt` como operador.
- [ ] Tu cron `soporte-resumen-…` dejó `reportes/resumen-faq-<id>.md` y lo leíste como operador.
- [ ] Puedes explicar skill, heartbeat, cron y subagente con sesión, directiva y disparador.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `No se observó ninguna ejecución programada correcta en tres minutos` (o tu fragmento agota los 4 min) | La hora `at` quedó en el pasado o muy lejos, el gateway se reinició, o la instancia se pausó. | Revisa `cron.list` (nodo original de la 03a). Usa siempre `new Date(Date.now() + 60000).toISOString()`. Vuelve a **Probar conexión** y reintenta. |
| El cron se disparó a otra hora | Escribiste la hora sin zona horaria. `toISOString()` siempre da UTC (termina en `Z`); la Ciudad de México está en UTC-6. | Escribe la hora con desfase explícito, por ejemplo `"2026-10-20T09:00:00-06:00"`, o calcula desde `Date.now()`. `[VERIFICAR EN LAB: cómo interpreta el gateway una hora sin desfase]` |
| `La ejecución programada del agente informó de un error: …` | El turno del agente falló (modelo, tiempo o permisos). | Lee el detalle del run. Sube `timeoutSeconds`. Corre la **Comprobación de estado** (flujo *Detectar y recuperar*). |
| La tarea "corrió" pero no hay archivo | El agente reportó éxito sin escribir, o escribió en otra ruta. | El cron no prueba nada por sí solo: lee el archivo como operador. Busca con `nemoclaw my-assistant exec -- bash -lc 'ls -la /sandbox/.openclaw/workspace/reportes/'`. |
| `Examina o elimina la tarea propia anterior antes de iniciar otra` | La página guardó el ID de una tarea anterior que no se limpió. | Ejecuta el nodo **Reintenta la eliminación de la tarea creada**. |
| `Limpieza incompleta; ejecuta Eliminar tarea creada. ID conservado: …` | Cerraste la pestaña o falló `cron.remove`. | Usa el ID con **Reintenta la eliminación de la tarea creada**. Con `deleteAfterRun`, algunas versiones de OpenClaw rechazan `cron.remove` porque la tarea ya se borró sola: confirma con `cron.list`. |
| El agente no usa la skill si no le das la ruta | La `description` del frontmatter es vaga ("skill de soporte") y no coincide con la pregunta. | Reescribe la `description`: qué hace, para quién y con qué palabras preguntaría el estudiante. Reinstala con `skill install` (reemplaza la del mismo nombre) y prueba en una sesión **nueva**. |
| `skill install` falla por el `SKILL.md` | Falta el frontmatter, falta `name`, o el nombre tiene caracteres no permitidos. | Frontmatter YAML entre `---` con `name` (solo letras, números, puntos, guiones y guiones bajos) y `description`. Los archivos que empiezan con `.` se omiten. |
| La skill responde "No encuentro la FAQ del curso en el workspace" | No copiaste la FAQ o quedó en `faq/faq/`. | `nemoclaw my-assistant exec --workdir /sandbox/.openclaw/workspace -- ls -R faq` y corrige con `upload`. |

## Reto

**Que el agente descubra la skill solo.** Reemplaza temporalmente la `description` de tu `SKILL.md` por `Skill de soporte.`, reinstálala y haz la pregunta del paso 7 en una sesión nueva. Luego restaura una descripción buena (la original o una mejor) y repite.

Criterio de éxito: con la descripción vaga el agente no sigue el formato de la skill; con la buena, en una sesión nueva y **sin darle la ruta**, responde con **Categoría**, pasos y **Fuente:** `faq/…`. Anota las dos respuestas.

## Avance del proyecto

**Soporte NemoClaw ya está desplegado en OpenClaw:**

- La skill `soporte-nemoclaw` instalada, con la FAQ del curso en `faq/` dentro del workspace.
- Una tarea programada que deja `reportes/resumen-faq-<id>.md` sin intervención.

Repite la pregunta de la línea base de 4.1 ("Mi notebook responde HTTP 401") y compara. Guarda la respuesta nueva en `proyecto/linea-base-4.1.md`, debajo de la anterior, y anota la diferencia: ¿ahora cita la FAQ? ¿Sigue las categorías del router de la clase 3.1? En el módulo 5 vas a revisar qué riesgos abrió todo esto: un agente con datos, herramientas y tareas que corren solas.

## Recursos

- [Lección 03c · El agente siempre activo (NVIDIA DLI, español)](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/03c-always-on.html)
- [NemoClaw · Referencia de comandos: `skill install`, `skill list`, `skill remove`, `upload`](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands.md)
- [NemoClaw · Configurar heartbeats del agente](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/configure-agents/configure-agent-heartbeats.md)
- [OpenClaw · Automatización: cron vs. heartbeat](https://docs.openclaw.ai/cron-vs-heartbeat)
- [Anthropic · Agent Skills](https://www.anthropic.com/news/skills) y [Voyager (arXiv 2305.16291)](https://arxiv.org/abs/2305.16291)
- `man 8 cron` para el cron clásico de Unix (la idea es la misma: una hora y un comando)
