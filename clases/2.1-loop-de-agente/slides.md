## Un modelo no es un agente

:::diagrama modelo-vs-agente

.lead La diferencia no es el modelo: es el código que lo rodea.

Notas:
Abrir con la pregunta: ¿qué le falta a ChatGPT para ser un agente? La respuesta es el loop. Clic 1: el modelo solo (texto entra, texto sale, una vez). Clic 2: el mismo modelo dentro de un ciclo que se repite, con herramientas y memoria.

---

## El loop

:::diagrama c21-loop

Notas:
La receta: lees el paso, lo haces, pruebas, y sigues. Clics 1 a 4: observar, decidir, actuar y ¿terminé? (con la flecha "no: otra vuelta"). Clic 5: sí, listo. Clic 6: el tope de pasos. Es casi literal la función correr_agente del notebook (for paso in range(max_pasos)); no dice "laberinto" ni "LLM".

---

## Una llamada no tiene estado

:::diagrama c21-sin-estado

Notas:
Demo: preguntar "¿Qué te pregunté hace un momento?". Clic 1: una llamada normal. Clic 2: la segunda llamada no sabe nada de la primera. Clic 3: cada llamada empieza de cero. Clic 4: lo que trae cada respuesta (en el notebook: content, finish_reason y usage; algunos modelos también devuelven reasoning_content).

---

## La decisión es reemplazable

:::diagrama c21-cerebros

Notas:
Es la idea central de la lección 01a de NVIDIA: observar y actuar no dependen de quién decide. Clic 1: el loop con un hueco donde va "decidir". Clics 2 a 4: tres cerebros (regla fija, búsqueda en anchura BFS, LLM). Clic 5: el loop no cambia.

---

## Cuando decide un LLM

:::diagrama c21-decide-llm

Notas:
Clic 1: el prompt describe el mapa en texto (posición, meta, movimientos legales) y pide una sola palabra. Clic 2: el modelo responde. Clic 3: extraemos el movimiento. Clic 4: validamos contra los movimientos legales. Clic 5: solo entonces actuamos. Clic 6: si no es legal, se lo decimos y reintenta. Clic 7: el esquema y el prompt piden; el harness hace cumplir. SIN_RAZONAR apaga el razonamiento largo de Nemotron: es el perfil "direct" del curso de NVIDIA.

---

## Errores comunes

:::diagrama c21-confianza

Notas:
Error en vivo de la clase: prompt flojo + confiar en el texto → 💥 Movimiento inválido. Clic 1: el carril que falla. Clic 2: el que funciona (extraer + validar). Clic 3: la regla de oro. Otros errores: "⛔ Se acabó el presupuesto de pasos" = le quitaste contexto al modelo (mapa, estrategia); finish_reason=length sin contenido = el modelo razonó de más, sube max_tokens; "Modo: MOCK" con key = reinicia el kernel.

---

## La memoria es una libreta

:::diagrama c21-libreta

.lead En el código, la libreta se llama `messages`.

Notas:
Clic 1: turno 1. Clic 2: en el turno 2 se reenvía todo y responde "Te llamas Ada". Clic 3: sin libreta, no lo sabe. Clic 4: cada turno cuesta más que el anterior. Toda la memoria, el contexto y el costo de los agentes salen de este hecho.

---

## Proyecto: Soporte NemoClaw v1

:::diagrama c21-soporte-v1

Notas:
Clic 1: lo que tiene (system prompt con rol y reglas, historial, nunca pide ni repite una API key, max_turnos por sesión). Clics 2 y 3: la ventana max_mensajes; con 4 olvida el nombre, con 20 lo recuerda. Clic 4: memoria contra costo. Pronto le damos ReAct y una herramienta.

---

## Tu práctica

:::diagrama c21-practica

Notas:
Un clic por paso. Preguntas de "Lo esencial": pasos de "siempre a la derecha" y de la búsqueda (sección 3), la frase del prompt flojo (sección 5), con cuántos mensajes olvida tu nombre (sección 7). Si programas: los experimentos de "✏️ Tu turno" (sin mapa, sin estrategia, temperatura 1.0), el reto de memoria de hechos con ventana de 4 y, opcional, la lección 01a de NVIDIA (includeHistory:false, perfiles direct, reasoning, omni).
