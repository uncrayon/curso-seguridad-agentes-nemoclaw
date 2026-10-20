## Una receta y un despertador

:::diagrama c43-receta-alarma

Notas:
Las dos palabras nuevas. Clic 1: la skill, una tarjeta de receta que el agente lee cuando la necesita. Clic 2: la tarea programada (cron), la alarma del despertador: a la hora fijada, el agente trabaja solo. Clic 3: ese es todo el punto y todo el riesgo.

---

## Los 3 controles

:::diagrama c43-controles

Notas:
Un clic por pregunta: sesión (¿qué conversación recuerda?), directiva (¿qué instrucciones sigue?), disparador (¿qué la hace empezar?). Clic 4: juntas describen un agente siempre activo. Clic 5: sirven para cualquier automatización, de OpenClaw o de otra herramienta. En el Módulo 6 se usan para comparar CLIs.

---

## Cuatro mecanismos, mismas preguntas

:::diagrama c43-mecanismos

Notas:
Clic 1: la skill usa tu misma conversación, sigue su SKILL.md y empieza cuando la pides. Clic 2: el cron empieza a una hora, en una conversación nueva y vacía (Isolated session), con el Prompt de la automatización. Clic 3: heartbeat y subagente, punteados porque hoy son solo concepto. El heartbeat aparece en Automations como heartbeat-main, cada 30 min; en el laboratorio su historial dice Skipped · no-route, y es normal. Clic 4: lo que corremos hoy.

---

## Anatomía de una skill

:::diagrama c43-anatomia

Notas:
La tarjeta de receta de soporte-nemoclaw, por partes. Clic 1: la etiqueta (el frontmatter), con name y description. Clic 2: los pasos. Clic 3: las reglas. Clic 4: la descripción decide si el agente la descubre solo. El name solo admite letras, números, puntos, guiones y guiones bajos. La skill completa está en la página de la clase.

---

## Instalar: procedimiento + conocimiento

:::diagrama c43-instalar

.lead La skill es el procedimiento. La FAQ es el conocimiento.

Notas:
Clic 1: la skill soporte-nemoclaw. Clic 2: el error en vivo, una copia sin name: NemoClaw revisa la etiqueta antes de subirla. Clic 3: la copia buena llega a skills/ del escritorio: "✓ Validated SKILL.md" e "Installed soporte-nemoclaw from path -> /sandbox/.openclaw/workspace/skills/soporte-nemoclaw". Clic 4: la FAQ llega a faq/. Ojo con upload: el destino es workspace/, no faq/, o queda faq/faq.

---

## La forma de operador, en la terminal

```bash
# Instala la skill
nemoclaw my-assistant skill install ~/curso/clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/

# Sube la FAQ al escritorio del agente (el destino es workspace/)
nemoclaw my-assistant upload ~/curso/datos/faq/ /sandbox/.openclaw/workspace/

# Compruébalo desde dentro del cuarto
nemoclaw my-assistant exec -- ls /sandbox/.openclaw/workspace/skills/ /sandbox/.openclaw/workspace/faq/
```

.lead Instalar va por la VM TERMINAL. Programar la tarea, con clics en Automations.

Notas:
En el tablero de NemoClaw, VM TERMINAL; clic dentro del área negra antes de escribir. Antes de cada línea, decir para qué sirve. La línea ExperimentalWarning de SQLite es inofensiva. Error en vivo: nemoclaw my-assistant skill install ~/soporte-rota/ (copia sin la línea name:).

---

## Explícita vs. automática

:::diagrama c43-explicita

Notas:
Clic 1: explícita, le das la ruta en el chat (CHAT WITH AGENT): prueba que puede seguirla. Clic 2: automática, solo describes el problema: prueba que la elige solo. En la VM TERMINAL: nemoclaw my-assistant agent --session-key prueba-43 -m 'Mi API key de NVIDIA me da 401, ¿qué hago?' respondió Categoría api_key, pasos y Fuente: faq/errores-api.md, faq/api-key.md. Clic 3: siempre en sesión nueva. Seguir la ruta que le diste no prueba que la elija solo.

---

## Cron: trabajo sin chat

:::diagrama c43-cron

Notas:
Un clic por etapa: la alarma (Automations → New automation, Repeat Once, Run at dentro de 2 minutos), suena, conversación nueva y vacía (Runs in: Isolated session), sigue el Prompt con la skill, deja el archivo reportes/resumen-faq.md. Clic 6: Run at usa la hora local de tu navegador; la fecha dentro del archivo va en UTC. Name soporte-resumen-faq, Delivery None, Advanced → Delete after run encendido. La lista dice in 2m, luego Running, y Run history dice OK con ≈112 mil tokens.

---

## La prueba la haces tú

:::diagrama c43-prueba

Notas:
Clic 1: un OK en Run history no basta. Clic 2: lo lees tú, como operador, en la VM TERMINAL: nemoclaw my-assistant exec -- bash -lc 'ls -la /sandbox/.openclaw/workspace/reportes/; cat /sandbox/.openclaw/workspace/reportes/resumen-faq.md'. Clic 3: el archivo existe, con dueño sandbox y la línea "Generado por la skill soporte-nemoclaw.". Clic 4: nadie escribió en el chat. Y nemoclaw my-assistant exec -- openclaw cron list confirma que la tarea se borró sola.

---

## Corre aunque nadie mire

:::diagrama c43-nadie-mira

Notas:
Clic 1: "Envía el reporte diario" se dispara aunque no estés. Clic 2: cada disparo es una sesión aislada, pero el workspace se comparte y afecta lo que viene. Clic 3: cada disparo consume créditos del modelo: nuestra tarea usó ≈112 mil tokens. Nunca dejes un Interval de pocos minutos encendido. Clic 4: nombra tus tareas, revisa Automations y pausa o borra con el menú ⋯ lo que no reconozcas. Puente al Módulo 5: un agente con datos, herramientas y tareas autónomas es el escenario de la trifecta letal.

---

## Errores comunes

| Ves | Haz esto |
|---|---|
| **NEXT RUN** no dice `in 2m` | **Run at** usa la hora de tu navegador: pon tu hora + 2 min |
| Se queda en **Running** mucho rato | Espera y mira **Run history**; revisa que la inferencia esté sana |
| Dice **OK**, pero no ves el archivo | Léelo como operador y búscalo por nombre |
| El agente no elige la skill solo | Mejora la descripción, reinstálala y abre una conversación nueva |
| `skill install` falla | Revisa que la etiqueta tenga `name` |
| «No encuentro la FAQ» | Súbela a `workspace/faq/` (sin que quede `faq/faq/`) |

Notas:
La hora del archivo va en UTC (la Ciudad de México está 6 horas atrás). heartbeat-main en Skipped · no-route es normal en el laboratorio. Búsqueda por nombre: grep -rl "Generado por la skill soporte-nemoclaw". Estado de la inferencia: nemoclaw my-assistant status.

---

## Avance del proyecto

.lead Soporte NemoClaw ya vive en OpenClaw.

- La skill `soporte-nemoclaw` y la FAQ en su escritorio
- Una tarea en Automations que dejó un resumen de la FAQ
- Repite la pregunta del 401 y compárala con la de la clase 4.1

¿Qué riesgos abrimos? Lo vemos en el Módulo 5.

Notas:
Guardar la respuesta nueva debajo de la anterior en proyecto/linea-base-4.1.md. Si paras por hoy: Stop en la consola de Brev y vuelve pronto.
