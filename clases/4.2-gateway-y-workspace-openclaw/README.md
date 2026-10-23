# 4.2 · Explora el gateway y el workspace de OpenClaw

Abre la carpeta que define a tu agente, compara lo que el agente dice de sí mismo con lo que hay en disco y personalízalo para el proyecto Soporte NemoClaw.

| | |
|---|---|
| Duración del video | ≈8 min |
| Práctica | Laboratorio en Brev: tablero de NemoClaw + terminal del navegador ([cookbook.md](cookbook.md)) |
| Habilidad | Orientación (sin habilidad evaluada) |

Material: [diapositivas](slides.html) · [recetario de terminal](cookbook.md) · [preguntas frecuentes del curso](../../FAQ.md)

> Basado en la lección 03b-openclaw del curso NVIDIA DLI «NemoClaw» (Apache-2.0).

## Lo esencial (sin tecnicismos)

**La idea:** Tu agente es lo que dicen unos archivos de texto en su carpeta de trabajo: su personalidad, sus reglas y su memoria. Hoy los abres, comparas lo que el agente dice de sí mismo con lo que de verdad está escrito y le das el puesto de Soporte NemoClaw.

**Piénsalo como:** un edificio de oficinas. La recepción recibe los mensajes (el gateway), el asistente trabaja en su escritorio (el workspace) y sobre el escritorio están el reglamento y la descripción del puesto (SOUL.md).

**Palabras nuevas:** [gateway](../../GLOSARIO.md), [workspace](../../GLOSARIO.md), [SOUL.md](../../GLOSARIO.md).

**Hazlo sin programar (≈10 min):** Escribe en español normal la sección «Proyecto: Soporte NemoClaw» de tu `SOUL.md`: a quién ayuda tu agente, en qué idioma y con qué tono responde, y tres cosas que nunca hace. Si tu laboratorio está encendido, abre **CHAT WITH AGENT** y pídele: «Enumera los archivos de tu workspace». Compara su lista con la lista real de la Parte B de esta guía y anota las diferencias.

**Qué te llevas:** puedes definir por escrito la personalidad y los límites de un agente, y sabes que lo que el agente dice se comprueba en el archivo.

**Tu crédito:** esta práctica usa ≈20 min de instancia encendida, dentro de tu sentada única de laboratorio (ver [LABORATORIO.md](../../LABORATORIO.md)). Si paras por hoy, haz **Stop** y vuelve pronto. Al final del laboratorio (después de la 5.3, o de la última práctica complementaria que hagas), haz **Delete**.

## Lo que vas a lograr

- Nombrar las piezas de OpenClaw (gateway, sesiones, workspace) y qué archivo del workspace moldea cada parte del comportamiento.
- Verificar como operador, con `ls` y `cat`, lo que el agente afirma sobre sus archivos y su memoria.
- Personalizar `SOUL.md` para que tu agente se comporte como **Soporte NemoClaw**, y probarlo en una sesión nueva.
- Listar y reiniciar sesiones, y comprobar que lo escrito en archivos sobrevive a una sesión nueva.

## Antes de empezar

- La clase 4.1 terminada: instancia en **Running**, tu agente `my-assistant` vivo y el tablero abierto.
- Si cerraste la pestaña: consola de Brev → **Compute** → tu instancia → botón verde **NemoClaw**. Puede que te pida iniciar sesión con NVIDIA otra vez; es normal.
- Recuerda cómo usar la **VM TERMINAL**: haz clic dentro del área negra antes de escribir, y ignora la línea `ExperimentalWarning: SQLite is an experimental feature`.

## Las piezas, en una tabla

| Pieza | Dónde vive | Qué hace |
|---|---|---|
| Gateway de OpenClaw | Dentro del sandbox, puerto 18789 | Recibe cada turno, corre el loop del agente y sirve el chat que abres con **CHAT WITH AGENT**. |
| Gateway de OpenShell | En la máquina (el host), puerto 18080, solo local | Maneja el ciclo de vida del sandbox y la ruta al modelo. Lo ves con `openshell gateway info`. |
| Sesiones | En el gateway de OpenClaw | El historial de cada conversación, identificado por su clave de sesión. |
| Workspace | `/sandbox/.openclaw/workspace/` | Archivos Markdown que el agente lee **al inicio de cada sesión**. Es su configuración. |

El workspace, archivo por archivo:

| Archivo | Qué define |
|---|---|
| `SOUL.md` | Personalidad, límites, tono y valores. |
| `AGENTS.md` | Instrucciones de operación y reglas: memoria, seguridad, flujo de cada sesión. |
| `IDENTITY.md` | Tarjeta corta: nombre, idioma, emoji. |
| `USER.md` | Quién es la persona a la que ayuda y sus preferencias. |
| `TOOLS.md` | Notas de uso de cada herramienta. |
| `HEARTBEAT.md` | Lista de tareas periódicas (lo vemos en 4.3). |
| `POLICY.md` | Resumen de la política de red, escrito por NemoClaw. |
| `memory/` | Notas diarias `AAAA-MM-DD.md` que el agente agrega mientras trabaja. Se crea la primera vez que el agente guarda una nota. |
| `MEMORY.md` | Memoria de largo plazo, depurada. Se crea la primera vez que el agente la usa. |
| `skills/` | Una carpeta por skill, con su `SKILL.md`. Aparece cuando instalas la primera skill (clase 4.3). |

Un detalle que causa muchos errores: dentro del sandbox, `~` es `/sandbox`, **no** el workspace. `~/SOUL.md` apunta a `/sandbox/SOUL.md`, que el agente no lee como su personalidad. Usa siempre la ruta completa `/sandbox/.openclaw/workspace/SOUL.md`.

## Paso a paso

### Parte A · Pide al agente que se describa (chat)

1. **Abre el chat.** En el tablero, tarjeta **MY-ASSISTANT**, haz clic en **CHAT WITH AGENT**. Se abre OpenClaw en una pestaña nueva.

   ![Chat de OpenClaw: 1 marca el menú de la izquierda con Sessions y 2 marca el cuadro donde escribes el mensaje](../../assets/lab/22-chat-openclaw.jpg)

2. **Pídele que describa su escritorio.** Escribe:
   > Enumera brevemente los archivos de tu workspace y explica cada uno en una viñeta, sin volcar su contenido.

   Deberías ver: una lista de archivos con una explicación por viñeta. **Anótala**: es lo que el agente *dice*.

### Parte B · Verifica como operador

3. **Abre la terminal de operador.** Vuelve a la pestaña del tablero y haz clic en **VM TERMINAL**.

4. **Lista el workspace real.** Este comando le pide al sandbox la lista de archivos del escritorio del agente:
   ```bash
   nemoclaw my-assistant exec -- ls -la /sandbox/.openclaw/workspace
   ```
   Deberías ver, en un laboratorio recién creado: `AGENTS.md`, `HEARTBEAT.md`, `IDENTITY.md`, `POLICY.md`, `SOUL.md`, `TOOLS.md` y `USER.md`. Todavía **no** hay `MEMORY.md`, `memory/` ni `skills/`, y es normal.

5. **Lee su personalidad y sus reglas.** Estos comandos muestran el contenido de `SOUL.md` y el principio de `AGENTS.md`:
   ```bash
   nemoclaw my-assistant exec -- cat /sandbox/.openclaw/workspace/SOUL.md
   nemoclaw my-assistant exec -- head -n 30 /sandbox/.openclaw/workspace/AGENTS.md
   ```

6. **Compara.** ¿El agente mencionó un archivo que no existe, como `MEMORY.md`? ¿Se le olvidó alguno, como `POLICY.md`? Esa diferencia es el punto de la clase: **lo que el agente dice no es evidencia; el archivo sí**.

   Por qué funciona así: el laboratorio tiene dos planos de autoridad. La **VM TERMINAL** es el operador y corre **fuera** del sandbox. El agente corre **dentro**, con una política más estrecha.

7. **(Opcional) Mira el escritorio desde adentro.** En el tablero, haz clic en **SANDBOX TERMINAL**. Esa terminal está dentro del cuarto, como el agente. Escribe:
   ```bash
   whoami; echo "$HOME"
   ls /sandbox/.openclaw/workspace
   ```
   Deberías ver: `sandbox`, `/sandbox` y la misma lista de archivos. Fíjate: aquí `~` es `/sandbox`, no el workspace.

### Parte C · Personaliza SOUL.md para Soporte NemoClaw

Vas a escribir tu sección en un archivo de la máquina, subirlo al sandbox y agregarlo al final de `SOUL.md`. Todo en la **VM TERMINAL**.

8. **Escribe tu sección en un archivo.** Este comando crea `~/soul-extra.md` en la máquina con el texto que va entre las dos líneas `EOF`. Cambia el texto por el que escribiste en «Hazlo sin programar», o usa este:
   ```bash
   cat > ~/soul-extra.md <<'EOF'

   ## Proyecto: Soporte NemoClaw
   - Ayudas a estudiantes del curso "Agentes Seguros con NemoClaw".
   - Respondes en español neutro, con frases cortas y pasos numerados.
   - Antes de responder, clasificas la duda en una categoría: instalacion, api_key, brev, seguridad u otro.
   - Si usas la FAQ del curso, citas el archivo de donde sale la respuesta.
   - Nunca pides, repites ni guardas API keys, tokens o cookies. Si alguien pega una, le pides que la revoque.
   - Si no sabes algo, lo dices y sugieres preguntar en el foro del curso.
   EOF
   ```
   Si prefieres un editor, usa `nano ~/soul-extra.md`, pega el texto, guarda con **Ctrl + O**, **Enter**, y sal con **Ctrl + X**.

9. **Guarda una copia del original.** Este comando copia `SOUL.md` a la carpeta `/tmp` del sandbox, por si quieres volver atrás:
   ```bash
   nemoclaw my-assistant exec -- cp /sandbox/.openclaw/workspace/SOUL.md /tmp/SOUL.md.original
   ```

10. **Sube tu sección al sandbox.** Este comando copia el archivo de la máquina a la carpeta `/tmp` del sandbox, y el segundo comprueba que llegó:
    ```bash
    nemoclaw my-assistant upload ~/soul-extra.md /tmp/
    nemoclaw my-assistant exec -- ls -la /tmp/soul-extra.md
    ```
    Deberías ver: el archivo `soul-extra.md`, con dueño `sandbox`.

11. **Agrégala al final de SOUL.md y léelo de vuelta.** El primer comando pega tu sección al final del archivo, dentro del sandbox. El segundo muestra las últimas líneas:
    ```bash
    nemoclaw my-assistant exec -- sh -c 'cat /tmp/soul-extra.md >> /sandbox/.openclaw/workspace/SOUL.md'
    nemoclaw my-assistant exec -- tail -n 9 /sandbox/.openclaw/workspace/SOUL.md
    ```
    Deberías ver: la sección «Proyecto: Soporte NemoClaw» al final.

    Usa `>>` (dos signos), no `>`: con uno solo, borras todo lo que había en `SOUL.md`.

    Para volver al original: `nemoclaw my-assistant exec -- cp /tmp/SOUL.md.original /sandbox/.openclaw/workspace/SOUL.md`. La copia en `/tmp` se borra si detienes la instancia.

### Parte D · Pruébalo en una sesión nueva

El agente lee el workspace al **inicio** de cada sesión. Una conversación que ya estaba abierta no cambia.

12. **Pregúntale en una sesión nueva.** En la **VM TERMINAL**:
    ```bash
    nemoclaw my-assistant agent --session-key soul-42 -m '¿Quien eres, a quien ayudas y que nunca haces?'
    ```
    O en **CHAT WITH AGENT**: en el menú **Sessions**, abre una conversación nueva y haz la misma pregunta.

    Deberías ver: menciona el curso, el español neutro y que nunca pide API keys.

### Parte E · Sesiones y memoria en archivos

13. **Lista tus sesiones.** Este comando muestra las conversaciones que guarda el gateway, en un formato fácil de leer:
    ```bash
    nemoclaw my-assistant sessions list --json
    ```
    Deberías ver: un JSON con tus sesiones y campos como `"agentId": "main"` y `"kind": "direct"`. Busca las claves que usaste (`memo-41`, `soul-42`). Sin `--json`, la tabla es muy ancha para la terminal del navegador.

14. **Pídele al agente que guarde una preferencia en un archivo.** Esto es memoria en disco, no en la conversación:
    ```bash
    nemoclaw my-assistant agent --session-key memoria-a -m 'Agrega esta linea al final de /sandbox/.openclaw/workspace/MEMORY.md sin borrar nada: "soporte-pref-01: responde en español neutro y cita el archivo de la FAQ que usaste. Referencia REF-4821." Despues leelo de vuelta y cita la linea.'
    ```
    Deberías ver: que el agente dice que la guardó. Todavía no le creas.

15. **Compruébalo como operador.** Este comando busca la referencia dentro del archivo:
    ```bash
    nemoclaw my-assistant exec -- grep -n "REF-4821" /sandbox/.openclaw/workspace/MEMORY.md
    ```
    Deberías ver: la línea con `REF-4821`. Si no aparece, el agente no la escribió ahí, aunque haya dicho que sí.

16. **Reinicia la sesión y pregunta desde otra.** Reiniciar borra la conversación, no los archivos:
    ```bash
    nemoclaw my-assistant sessions reset memoria-a
    nemoclaw my-assistant agent --session-key memoria-b -m 'Lee /sandbox/.openclaw/workspace/MEMORY.md e indica la preferencia y la referencia de soporte-pref-01.'
    ```
    Deberías ver: `REF-4821` en la respuesta de la sesión nueva. La conversación se fue; el archivo se quedó.

## Comprueba que funcionó

- [ ] Tienes anotada la lista de archivos que dio el agente y la lista real de `ls`, y sabes si coinciden.
- [ ] Leíste `SOUL.md` y `AGENTS.md` como operador.
- [ ] `tail` muestra la sección «Proyecto: Soporte NemoClaw» al final de `SOUL.md`.
- [ ] Una sesión nueva (`soul-42`) responde con la identidad de Soporte NemoClaw.
- [ ] `sessions list --json` muestra tus claves de sesión.
- [ ] `REF-4821` está en `MEMORY.md` y la sesión `memoria-b` la recupera.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| El agente dice «listo, lo guardé» pero el archivo no cambió | El modelo reporta una acción que no hizo, o escribió en otra ruta. | Verifica siempre con `cat` o `grep` como operador. Pídele de nuevo con la ruta completa y que lea el archivo de vuelta. |
| Escribiste en `~/SOUL.md` y el agente no cambió | Dentro del sandbox, `~` es `/sandbox`, no el workspace. Escribiste `/sandbox/SOUL.md`. | Usa `/sandbox/.openclaw/workspace/SOUL.md`. Borra el archivo suelto: `nemoclaw my-assistant exec -- rm /sandbox/SOUL.md`. |
| Cambiaste `SOUL.md` y la conversación abierta sigue igual | El workspace se lee al iniciar cada sesión. | Prueba con una clave de sesión nueva o una conversación nueva en **Sessions**. |
| `SOUL.md` quedó solo con tu sección | Usaste `>` en vez de `>>`. | Restaura la copia: `nemoclaw my-assistant exec -- cp /tmp/SOUL.md.original /sandbox/.openclaw/workspace/SOUL.md` y repite con `>>`. |
| Al pegar el bloque `cat > … <<'EOF'` la terminal muestra `>` y espera | Falta la línea final `EOF`, o tiene espacios antes. | Escribe `EOF` solo, al inicio de la línea, y presiona **Enter**. |
| `MEMORY.md`, `memory/` o `skills/` no existen | El agente aún no ha guardado memoria ni tiene skills instaladas. | Es normal. Se crean la primera vez que hacen falta. |
| `ls: cannot access '/tmp/soul-extra.md'` | El archivo no llegó al sandbox, o quedó en otra ruta. | Repite el `upload` y revisa con `nemoclaw my-assistant exec -- ls -la /tmp/`. |
| `Pairing required` en el chat | El chat del laboratorio ya viene emparejado; este aviso no debería salir. | Cierra la pestaña y vuelve a abrir el chat desde **CHAT WITH AGENT** en el tablero. |
| Corriste `openclaw update` dentro del sandbox y se colgó | OpenClaw viene fijado en la imagen del sandbox. No se actualiza en el lugar. | No lo hagas. Cancela con `Ctrl+C`. En el laboratorio del curso, no toques versiones. |

## Reto

**Haz que el agente demuestre lo que guarda.** Agrega esta regla al final de `AGENTS.md`, con el mismo método de la Parte C (archivo en la máquina, `upload` a `/tmp` y `cat >>`):

```text
- Cada vez que digas que guardaste algo en un archivo, léelo de vuelta y cita la línea exacta que quedó escrita.
```

Criterio de éxito: en una sesión nueva le pides guardar una preferencia en `MEMORY.md`, su respuesta incluye la línea leída de vuelta y `grep` como operador confirma que esa línea existe.

## Avance del proyecto

Tu agente ya tiene la identidad de **Soporte NemoClaw**:

- `SOUL.md` con la sección del proyecto (idioma, categorías de triage, regla de no pedir keys).
- `MEMORY.md` con la preferencia `soporte-pref-01` (citar el archivo de la FAQ).

Copia en tus notas la sección que agregaste a `SOUL.md`. Luego repite la pregunta de la línea base de 4.1 en una sesión nueva:

```bash
nemoclaw my-assistant agent --session-key linea-base-42 -m 'Un estudiante dice: "Mi notebook responde HTTP 401 cuando llamo al modelo". ¿Que le respondes? Responde en español y en 5 lineas como maximo.'
```

Anota en tus notas, debajo de la línea base, qué cambió. Todavía no conoce la FAQ: eso llega en 4.3 con la skill `soporte-nemoclaw`.

## Recursos

- [NemoClaw · Estado del sandbox y archivos del workspace](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/manage-sandboxes/workspace-files.md)
- [NemoClaw · Referencia de comandos](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands.md) (`exec`, `agent`, `sessions`, `upload`)
- [NemoClaw · Troubleshooting](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/troubleshooting.md)
- [OpenClaw · Documentación](https://docs.openclaw.ai)
- [Tu laboratorio en Brev: crédito, plan y tablero](../../LABORATORIO.md)
- [MemGPT: memoria por niveles para LLMs (arXiv 2310.08560)](https://arxiv.org/abs/2310.08560)
