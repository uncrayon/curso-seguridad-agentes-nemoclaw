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
Clic 1: la skill usa tu misma conversación, sigue su SKILL.md y empieza cuando la pides. Clic 2: el cron empieza a una hora, en una conversación nueva y vacía (sesión aislada), con el mensaje programado (payload.message). Clic 3: heartbeat y subagente, punteados porque hoy son solo concepto: ninguna celda de la 03c los dispara. El heartbeat lo configura NemoClaw en una sesión aislada. Clic 4: lo que corremos hoy.

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
Clic 1: la skill soporte-nemoclaw. Clic 2: el error en vivo, una copia sin name: NemoClaw revisa la etiqueta antes de subirla. Clic 3: la copia buena llega a skills/ del escritorio. Clic 4: la FAQ llega a faq/. skill install valida el frontmatter y llama a openclaw skills install --agent main --force; reinstalar reemplaza la del mismo nombre.

---

## La forma de operador, en la terminal

```bash
# Instala la skill y comprueba que está
nemoclaw my-assistant skill install ./soporte-nemoclaw/
nemoclaw my-assistant skill list

# Sube la FAQ al escritorio del agente y compruébalo
nemoclaw my-assistant upload ./faq/ /sandbox/.openclaw/workspace/faq/
nemoclaw my-assistant exec --workdir /sandbox/.openclaw/workspace -- ls faq
```

.lead Instalar la skill es el único paso de hoy que va por la terminal. Lo demás, con clics.

Notas:
Antes de cada línea, decir para qué sirve. Error en vivo: nemoclaw my-assistant skill install ./soporte-rota/ (copia sin la línea name:).

---

## Explícita vs. automática

:::diagrama c43-explicita

Notas:
Clic 1: explícita, le das la ruta: prueba que puede seguirla (Paso 1 de la 03c). Clic 2: automática, solo describes el problema: prueba que la elige solo (panel "Prueba · activa una skill durante la conversación"). Clic 3: siempre en sesión nueva. La celda de la 03c lo dice: obtener la referencia del runbook no prueba la selección automática.

---

## Cron: trabajo sin chat

:::diagrama c43-cron

Notas:
Un clic por etapa: la alarma (cron.add con schedule.kind "at"), suena, conversación nueva y vacía (sessionTarget "isolated"), sigue el mensaje, deja el archivo reportes/resumen-faq-<id>.md. Clic 6: toISOString() da la hora en UTC (termina en Z). El fragmento completo está en la página de la clase, paso 10: se pega en el nodo "Llama a models.list y cron.list" de la 03a, después de "Abre la conexión del gateway". Luego cron.runs hasta ver ok.

---

## La prueba la haces tú

:::diagrama c43-prueba

Notas:
Clic 1: un status ok en cron.runs no basta. Clic 2: lo lees tú, como operador (celda de Paso 1b de la 03b). Clic 3: el archivo existe. Clic 4: nadie escribió en el chat. Por terminal: nemoclaw my-assistant exec -- bash -lc 'cat /sandbox/.openclaw/workspace/course-cron-*.txt' (exec no usa shell: para * o &&, envuélvelo en bash -lc).

---

## Corre aunque nadie mire

:::diagrama c43-nadie-mira

Notas:
Clic 1: "Envía el reporte diario" se dispara aunque no estés. Clic 2: cada disparo es una sesión aislada, pero el workspace se comparte y afecta lo que viene. Clic 3: cada disparo consume créditos del modelo. Clic 4: nombra tus tareas, revisa cron.list y borra lo que no reconozcas. Puente al Módulo 5: un agente con datos, herramientas y tareas autónomas es el escenario de la trifecta letal.

---

## Errores comunes

| Ves | Haz esto |
|---|---|
| La tarea no dice `ok` en 3 minutos | Revisa la lista de tareas y que la instancia esté encendida |
| Corrió a otra hora | Agrega tu zona horaria: el agente usa la hora universal |
| Dice `ok`, pero no ves el archivo | Léelo como operador y búscalo por nombre |
| El agente no elige la skill solo | Mejora la descripción, reinstálala y abre una conversación nueva |
| `skill install` falla | Revisa que la etiqueta tenga `name` |
| «No encuentro la FAQ» | Súbela a `workspace/faq/` (sin que quede `faq/faq/`) |

Notas:
Zona horaria de la Ciudad de México: -06:00. Con deleteAfterRun, algunas versiones de OpenClaw rechazan cron.remove porque la tarea ya se borró sola: confirmar con cron.list. Búsqueda por nombre: grep -rl.

---

## Avance del proyecto

.lead Soporte NemoClaw ya vive en OpenClaw.

- La skill `soporte-nemoclaw` y la FAQ en su escritorio
- Una tarea programada que deja un resumen de la FAQ
- Repite la pregunta del 401 y compárala con la de la clase 4.1

¿Qué riesgos abrimos? Lo vemos en el Módulo 5.

Notas:
Guardar la respuesta nueva debajo de la anterior en proyecto/linea-base-4.1.md.
