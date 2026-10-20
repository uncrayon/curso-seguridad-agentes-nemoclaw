## ReAct: razonar, actuar, observar

:::diagrama c22-detective

.lead ReAct viene del inglés *Reasoning + Acting*: razonar y actuar.

Notas:
Patrón de Yao et al., 2022; está detrás de LangChain, OpenClaw y casi todos los agentes modernos. Clic 1: la pregunta. Clic 2: el ciclo razonar → actuar → observar (se ilumina solo, paso por paso). Clic 3: cuando ya puede, responde. Clic 4: la comparación del detective.

---

## Herramienta y tool call

:::diagrama c22-pide

Notas:
Clic 1: el modelo solo ve la ficha de la herramienta (nombre, descripción, datos que pide = el esquema). Clic 2: manda un pedido (tool_call) y tu código lo revisa. Clic 3: tu código ejecuta la herramienta. Clic 4: el resultado vuelve como texto. Clic 5: el modelo no ejecuta nada. Insistir: quien ejecuta es el harness. Eso será clave para la seguridad en el Módulo 5.

---

## `finish_reason`: la nota al colgar

:::diagrama c22-finish

Notas:
Demo: misma pregunta sin tools (stop) y con tools (tool_calls). Clic 1: el modelo deja de escribir y deja una nota. Clics 2 a 4: stop, tool_calls y length, y qué hace el loop con cada una. Clic 5: si un agente se porta raro, mira finish_reason primero. Existe un cuarto valor, content_filter (filtro de seguridad): el loop avisa al usuario.

---

## El loop ReAct, vuelta por vuelta

:::diagrama c22-vueltas

Notas:
"¿Qué hora es en UTC?". Clic 1: vuelta 1, tool_calls, se ejecuta el reloj y se anotan el pedido y el resultado con el mismo id (tool_call_id). Clic 2: vuelta 2, stop y la respuesta. Clic 3: el tope de pasos (max_pasos). Los tres detalles de la función react del notebook: misma etiqueta, validar antes de ejecutar, tope.

---

## Así crece la libreta

:::diagrama c22-libreta

Notas:
Es el disclosure de la lección 01b: inspecciona el orden de messages. Un clic por mensaje: system, user, assistant (pide get_current_time), tool (el resultado) y assistant (la respuesta). Clic 6: el mensaje tool es la prueba de que se ejecutó.

---

## Errores comunes

:::diagrama c22-errores

Notas:
Error en vivo: SISTEMA_TERCO llega al tope de 4 pasos. Clic 1: el agente terco; sin max_pasos seguiría llamando al modelo (y gastando créditos) para siempre. Clic 2: el pedido roto (celda tc_falso): JSON roto en arguments, herramienta inventada (get_time) o datos que no acepta; cada uno vuelve como "ERROR: ..." con la lista de disponibles, sin lanzar excepción. Clic 3: ninguno rompe el loop. Otros: finish_reason="length" → sube max_tokens, nunca la trates como respuesta final; 400 tras una tool → falta el turno assistant o el tool_call_id no coincide.

---

## Context rot

:::diagrama c22-context-rot

.lead *Context rot*: una conversación que se echa a perder de tan larga.

Notas:
Mostrar la celda de tokens_aprox: de cientos a miles de tokens por llamada. Clic 1: cada paso reenvía todo, la libreta crece. Clics 2 a 4: más costo, más espera y el modelo atiende peor lo que queda en medio (Liu et al., 2023). Clic 5: mitigaciones del Módulo 3 (planear primero, recuperar lo justo, delegar a subagentes).

---

## Proyecto: Soporte NemoClaw v2

:::diagrama c22-soporte-v2

Notas:
Pregunta de demo: "Soy de Bogotá. ¿Qué hora es allá?". Un clic por pieza: el estudiante, Soporte NemoClaw v2 (loop ReAct con tope y validación de cada tool_call), la herramienta hora_local(ciudad) y la respuesta. Clic 5: la función react no cambió; solo agregas el esquema a TOOLS y la función al REGISTRO. En 2.3: buscar_faq y estimar_costo_brev.

---

## Tu práctica

:::diagrama c22-practica

Notas:
Un clic por paso. Preguntas de "Lo esencial": el finish_reason sin y con reloj (sección 2), en cuántos pasos se detiene el agente terco (sección 5), de qué ciudad pidió la hora Soporte NemoClaw (sección 7). Si programas: provoca las tres fallas; "✏️ Tu turno" (sin pista en la pregunta, la capital de Francia, los minutos hasta las 17:00); reto: minutos_hasta(hora_utc) con una sola llamada a herramienta; opcional: la lección 01b de NVIDIA.
