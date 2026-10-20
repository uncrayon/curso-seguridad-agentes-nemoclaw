## Dilo una vez, guárdalo para siempre

:::diagrama c62-sin-con

Notas:
Clic 1: sin skills, cada sesión empieza de cero y pegas las mismas reglas; cada vez salen un poco distintas. Clic 2: con skills, una carpeta con `SKILL.md` que el agente carga cuando la necesita: la tarjeta de receta. Idea de Voyager (2023): lo que funcionó se guarda como receta reutilizable.

---

## Anatomía de un SKILL.md

:::diagrama c62-tarjeta

Notas:
Clic 1: la etiqueta (frontmatter, entre dos líneas `---`): nombre y descripción; es lo que el harness ve siempre. Clic 2: la receta (runbook): pasos numerados, con la herramienta exacta. Clic 3: los límites; el texto los pide, ya veremos quién los impone. El cuerpo lo ve el modelo solo si elige la skill. Muéstrala 20 segundos: es la que capturan.

---

## Progressive disclosure

:::diagrama c62-menu

.lead Menú barato; la receta, solo cuando hace falta.

Notas:
Clic 1: el menú (`nombre: descripción`), siempre en el prompt: ~350 tokens para 4 skills. Clic 2: la receta completa, solo la que se pide. Clic 3: cargar todo serían ~1,800 tokens con 4 y más de 20 mil con 50 skills, en cada llamada. Dato del notebook, sección 3.

---

## Explícita vs. automática

:::diagrama c62-dos-selecciones

Notas:
Clic 1: explícita, tú la nombras (`/diagnostico-api ...`); casi nunca falla. En el laboratorio es cuando le das la ruta del `SKILL.md`. Clic 2: automática, el modelo compara tu pedido con las descripciones; falla si la descripción no dice cuándo usarla. En el laboratorio es cuando omites la ruta. Clic 3: NVIDIA lo advierte en su lección 03c: el ejercicio con la ruta "no demuestra la selección automática".

---

## La description es el disparador

:::diagrama c62-disparador

Notas:
Clic 1: una descripción vaga ("Herramienta útil") no dice cuándo usarla: nadie la elige. Clic 2: la útil, con sus tres partes marcadas. Clic 3: qué hace + cuándo usarla + las palabras del usuario. Una description no es un título: es una regla de enrutamiento.

---

## Mide: tasa de acierto

:::diagrama c62-acierto

:::tip
Arregla la **descripción**, no la receta. Y evalúa con el modelo que vas a usar.
:::

Notas:
Un clic por barra: descripciones vagas 13 %, del proyecto 80 %, después de ✏️ Tu turno ≥ 90 % (modo MOCK). 15 pedidos con la skill esperada. Los tres fallos enseñan algo: usar las palabras del usuario, descriptions vecinas que compiten y palabras de relleno que atraen pedidos.

---

## Llévala al laboratorio

:::diagrama c62-al-lab

.lead Sin terminal, tu biblioteca ya funciona en el notebook. Este es el camino de operador.

Notas:
Clic 1: la carpeta skill-library, que ya viene en el repo del curso. Clic 2: en la VM TERMINAL del tablero, el curso ya está clonado en `~/curso` desde la 4.3 (si no, `git clone --depth 1 https://github.com/uncrayon/curso-seguridad-agentes-nemoclaw ~/curso`). Clic 3: `nemoclaw my-assistant skill install ~/curso/skill-library/diagnostico-api/`; responde `✓ Validated SKILL.md` e `Installed diagnostico-api from path -> …`; confirma con `nemoclaw my-assistant skill list`. Clic 4: sesión nueva y prueba las dos selecciones: `nemoclaw my-assistant agent --session-key prueba-62a -m '…'` o el botón CHAT WITH AGENT. Es opcional y va justo después de la práctica de la 6.1. Al terminar, cierra el laboratorio: guarda lo que quieras, Delete en la consola de Brev y revisa Billing. OpenClaw la deja en /sandbox/.openclaw/workspace/skills/<nombre>. Hermes en /sandbox/.hermes/skills; Deep Agents en /sandbox/.deepagents/agent/skills.

---

## Errores comunes

:::diagrama c62-errores

Notas:
Un clic por error. 1: `mapping values are not allowed here` = hay `: ` dentro de la description; usa comillas (el error de YAML es el número uno; lo provocamos en vivo). 2: el nombre solo acepta letras, números, `.` `-` `_`. 3: instalada pero no se usa sola: mejora la description y abre sesión nueva. 4: elige la skill equivocada: di cuándo **no** usarla.

---

## Una skill es persistencia

:::diagrama c62-persistencia

Notas:
Clic 1: tu biblioteca, con una skill envenenada escondida. Clic 2: una skill envenenada es una directiva envenenada que sobrevive entre sesiones. Clics 3 a 5: revísalas como código (diff, dueño, pull request); el texto pide, la herramienta y el sandbox imponen; decide quién puede escribir en `skills/`. Conecta con 5.1: la persistencia hace que una inyección dure más que una conversación.
