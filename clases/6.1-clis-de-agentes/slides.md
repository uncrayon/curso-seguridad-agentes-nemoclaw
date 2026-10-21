## El mismo loop, distintos defaults

:::diagrama c61-cinco-piezas

Notas:
Abre con la idea fuerte: no vamos a memorizar productos, vamos a aprender a compararlos. Cinco clics, una pieza cada uno: carpeta de trabajo, herramientas (terminal, edición, búsqueda, MCP), memoria, tareas sin nadie (cron, tareas largas, colas) y red. Clic 6: lo que cambia es qué viene abierto por defecto. El loop es el que ya conoces.

---

## Cinco preguntas para cualquier agente

:::diagrama c61-cinco-preguntas

Notas:
Un clic por eje: archivos, red, identidad, persistencia y sandbox por defecto, cada uno con su versión «en el asistente» para quien no programa. Clic 6: los grados de libertad son la superficie de ataque. Estas cinco preguntas sobreviven al próximo lanzamiento de producto. Pídeles que las anoten.

---

## Los CLIs tal como los instalas

:::diagrama c61-asistentes

.lead Asistentes distintos: cambia la llave que les das el primer día.

Notas:
Fuente: lección 04b de NVIDIA. Clic 1: Claude Code, Codex CLI y Cursor (Cursor: `.cursor/rules/*.mdc`; edita sin aprobar, la terminal pide aprobación). Clic 2: Hermes y Deep Agents (la aprobación de herramientas de Deep Agents fuera de NemoClaw no viene en 04b: no la afirmes). Clic 3: OpenClaw, el único que aquí vive en el cuarto (gateway y cron dentro de OpenShell). Clic 4: la frase que hay que decir siempre. Los defaults cambian con cada release. Deja la diapositiva 20 segundos en pantalla.

---

## NemoClaw no es solo OpenClaw

:::diagrama c61-tres-agentes

Notas:
Clic 1: OpenClaw (`nemoclaw`), el de siempre, con gateway y dashboard; Landlock `best_effort`. Clic 2: Hermes (`nemohermes`); red hacia NVIDIA, Nous y PyPI. Clic 3: Deep Agents (`nemo-deepagents`, binario `dcode`); Landlock `strict`: si no puede poner el candado, no arranca. Clic 4: lo que comparten los tres. Dato del repo de NemoClaw; los tres comandos vienen instalados en la VM del laboratorio. Detalle fino: OpenShell ve a dcode como Python, así que un permiso de red aplica a todo Python del sandbox.

---

## La CLI fija el default; el sandbox fija el límite

:::diagrama c61-dos-planos

Notas:
Clic 1: el plano de la app (CLAUDE.md, AGENTS.md, aprobaciones, modos): lo puede cambiar el agente o un prompt. Clic 2: el plano del sistema (Landlock, seccomp, netns, proxy de red): solo lo cambia el operador. Clic 3: una aprobación no es un límite del kernel. NVIDIA documenta OpenShell también para Codex, Cursor y OpenCode. Conecta con lo que viste de seguridad: prompt, harness, sandbox.

---

## ¿De qué lado de la puerta?

:::diagrama c61-de-que-lado

Notas:
Clic 1: afuera, tú en la VM TERMINAL del tablero (`id` responde `uid=1000(ubuntu)`, con grupos `sudo` y `docker`). Clic 2: `nemoclaw my-assistant exec` entra al cuarto: adentro, el agente es el usuario sandbox (`uid=998`). Clic 3: el agente intenta salir a example.com y la regla responde 403 (`CONNECT tunnel failed, response 403`): es el error en vivo de la clase. Clic 4: el error más común del foro, `openclaw: command not found`, porque estás afuera. Demo del cookbook, recetas 5 a 7, toda en la VM TERMINAL.

---

## Si prefieres la terminal

```bash
# en la VM TERMINAL del tablero de NemoClaw
id                                     # afuera: tú, el operador
nemoclaw my-assistant exec -- id       # adentro: usuario sandbox
nemoclaw my-assistant skill list       # no "openclaw ...": vive adentro
nemoclaw my-assistant exec -- curl -sS https://example.com
# curl: (56) CONNECT tunnel failed, response 403
nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4
```

.lead Es opcional: lo mismo del dibujo anterior, escrito como instrucciones.

Notas:
Otros errores comunes: escribir sin hacer clic en el área negra (se activan atajos del tablero); la línea `ExperimentalWarning: SQLite` (se ignora); `openshell gateway status` no existe (usa `openshell status` o `openshell gateway info`); `openshell logs --tail` no termina (en openshell `--tail` sigue: usa `-n 20`); inferencia `unauthorized` en `status` (revisa la key); 403 por política de red (OPENSHELL TUI → [r] → [a], o `policy add`). La confusión host/sandbox es la pregunta número uno en el foro.

---

## Cómo elegir según la tarea y el riesgo

:::diagrama c61-elegir

Notas:
Un clic por tarea, de menos a más riesgo. Clic 1: programar contigo al lado: Claude Code, Codex o Cursor con aprobaciones. Clic 2: refactor desatendido: Deep Agents o un CLI dentro de OpenShell. Clic 3: asistente 24/7 por chat: OpenClaw o Hermes en NemoClaw. Clic 4: cron que lee datos y reporta: sandbox y skill revisada. Clic 5: la trifecta letal manda al sandbox. El criterio no es "cuál es mejor", es "quién mira, qué toca, con quién habla, qué sobrevive".

---

## Tu ficha de cinco ejes

:::diagrama c61-ficha

Notas:
Es el reto de la clase. Que lo hagan con el agente que usan en su trabajo, leyendo su documentación oficial en el navegador, con un enlace por fila. Clic 1: la ficha vacía. Clic 2: si no está documentado, ese es el hallazgo. Cierra con el recordatorio: si van a hacer la parte opcional de laboratorio sobre la biblioteca de skills, dejan la instancia encendida y siguen; si no, guardan lo que quieran y borran la instancia en la consola de Brev con Delete (detenida, el disco sigue cobrando ≈USD 1.20 al día). Luego, revisa Billing.
