## Lo que vas a levantar hoy

:::diagrama brev-laboratorio

.lead Tu oficina rentada ya trae todo: el agente, el cuarto con cerradura y el kit. El modelo corre en la nube de NVIDIA.

Notas:
Clic 1: la consola de Brev. Clic 2: tu instancia con el launchable. Clic 3: el tablero de NemoClaw, desde donde haremos todo: chat y terminal en el navegador. La instancia es solo CPU (4 CPUs, 16 GiB) porque el modelo corre afuera.

---

## Brev desde cero

:::diagrama brev-pasos

Notas:
Un clic por paso. Menú de arriba: Compute, Agents, Launchables, Team, Billing, Docs. Cupón: Billing → Credits → Redeem Code. Selector de organización arriba a la derecha. Botón Deploy NemoClaw. En Compute, la instancia pasa a Running en ≈1 min y muestra $0.26/hr. RETRY reconstruye todo el sandbox; la tarjeta roja suele ser un error visual.

---

## Configura tu agente en el navegador

1. Botón verde **NemoClaw** → pestaña nueva → inicia sesión con NVIDIA
2. **SET UP IN THIS BROWSER** → **OPEN BROWSER SETUP →**
3. Agente **OpenClaw** · proveedor: de OpenRouter a **NVIDIA CLOUD**
4. Pega tu key `nvapi-` → **CREATE AGENT**
5. **Building your agent** (≈3 min) → **YOUR AGENT IS LIVE**

:::tip
Tu key se pega solo en ese campo. Nunca en el chat, en una captura ni en un video.
:::

Notas:
El inicio de sesión lo hace cada estudiante con su propia cuenta. Mientras se construye: no recargar la pestaña; si sale RETRY y el registro avanza, no tocarlo. Al final: agente my-assistant, modelo nvidia/nemotron-3.5-super-vl-120b-a12b. Back to overview lleva al tablero.

---

## Tu tablero: 4 botones

| Botón | Qué abre |
|---|---|
| **CHAT WITH AGENT** | El chat de OpenClaw, para conversar con tu agente |
| **SANDBOX TERMINAL** | Una terminal dentro del cuarto (usuario `sandbox`) |
| **VM TERMINAL** | La terminal de operador, afuera del cuarto (usuario `ubuntu`) |
| **OPENSHELL TUI** | El panel del guardia: política y accesos pendientes |

.lead La terminal de operador es donde pegas los comandos de las guías.

Notas:
Arriba del tablero: procesador, memoria, disco y el estado de seguridad (20 allowed sites, 13 network policies). Abajo, registros con filtros All / VM / Gateway / Agent. En la VM TERMINAL: clic dentro del área negra antes de escribir; Shift+Esc la cierra. La línea ExperimentalWarning de SQLite se ignora.

---

## Verifica como operador

:::cols
**Lo que dice el agente**
«Trabajo en /sandbox/.openclaw/workspace»
Puede decir que es `gateway-owner`
|||
**Lo que muestra el sistema**
`nemoclaw my-assistant exec -- whoami`
→ `sandbox`
:::

.lead Lo que el agente dice de sí mismo no es evidencia. El sistema sí.

Notas:
En el chat: «¿Quién eres y en qué carpeta trabajas?». En la VM TERMINAL: nemoclaw list, nemoclaw my-assistant status (inferencia healthy, fase Ready) y exec -- whoami / pwd (sandbox, /sandbox). Esta idea vuelve en 4.2 y en el Módulo 5.

---

## La memoria vive en la sesión

:::cols
**1 · Planta un dato**
Sesión `memo-41`
«Recuerda CODE-7Q4» → OK
|||
**2 · Pregunta**
Misma sesión
→ CODE-7Q4
|||
**3 · Reinicia y pregunta**
`sessions reset memo-41`
→ «no lo se»
:::

.lead La conversación la guarda la recepción (el gateway), no el modelo.

Notas:
Los cuatro comandos están en la Parte D del README y en la receta 7. En el chat se ve igual: en Sessions, una conversación nueva no conoce el código. Los archivos del workspace sobreviven al reinicio: eso es la clase 4.2.

---

## Comandos de operador

```bash
nemoclaw list                         # el sandbox de tu agente
nemoclaw my-assistant status          # ¿el agente está sano?
nemoclaw my-assistant exec -- whoami  # ¿quién es, de verdad?
git clone --depth 1 https://github.com/uncrayon/curso-seguridad-agentes-nemoclaw ~/curso
```

.lead Se pegan en la VM TERMINAL del tablero. No instalas nada en tu computadora.

Notas:
El git clone deja los archivos del curso en ~/curso; la clase 4.3 los usa (FAQ y skill). El gateway de OpenShell escucha en 18080 (openshell gateway info); el chat de OpenClaw, en 18789.

---

## Cuánto cuesta cada estado

:::diagrama estados-instancia

:::tip
Haz todo el laboratorio en una sola sentada. Si paras, **Stop** y vuelve pronto. Al terminar la clase 6.1, **Delete**.
:::

Notas:
Encendida ≈USD 0.25/h (la página muestra $0.26/hr). Detenida, el disco cobra ≈USD 0.05/h, ≈USD 1.20 al día: más que el cupón. Las preguntas al modelo se pagan con los créditos de build.nvidia.com, no con Brev.

---

## Si algo sale mal

| Ves | Haz esto |
|---|---|
| Te pide iniciar sesión otra vez | Normal: entra con la misma cuenta |
| Tarjeta roja **RETRY** | No la toques: mira si el registro avanza |
| "out of credits" con saldo | Cambia a la organización correcta en Brev |
| Escribes y la terminal no reacciona | Haz clic dentro del área negra |
| `503 … no_healthy_upstream` | Espera un par de minutos y recarga |

Notas:
nemoclaw deploy ya no existe (eliminado en v0.0.117). La línea ExperimentalWarning de SQLite no es un error. Shift+Esc cierra la terminal.

---

## Avance del proyecto

.lead Soporte NemoClaw ya tiene casa. Mide cómo responde hoy.

- Pregúntale: *"Un estudiante dice: 'Mi notebook responde HTTP 401'. ¿Qué le respondes?"*
- Copia la respuesta en tus notas del proyecto
- En la clase 4.3 le das la FAQ y comparas

Notas:
Se puede preguntar en el chat o con nemoclaw my-assistant agent --session-key linea-base -m '…'. La línea base sin skill es la que vamos a mejorar con la FAQ del curso.
