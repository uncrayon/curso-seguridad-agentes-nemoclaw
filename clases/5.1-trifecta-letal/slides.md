## Un chatbot dice. Un agente hace.

:::diagrama c51-dice-hace

Notas:
Clic 1: el chatbot (texto entra, texto sale; el peor caso es una respuesta equivocada). Clic 2: el agente, con archivos, programas, internet, memoria y tareas que corren solas; el peor caso es una acción equivocada sin nadie mirando. Clic 3: el detalle clave, toma como orden cualquier texto que lee. Antes dejamos al agente trabajando solo: hoy, ¿qué es lo peor que puede hacer con el acceso que ya tiene?

---

## La trifecta letal

:::diagrama c51-trifecta

Notas:
Un clic por pata, con la comparación del glosario: clic 1, datos privados (las llaves de tu casa); clic 2, contenido no confiable (el correo de cualquiera); clic 3, comunicación externa (un teléfono). Clic 4: las tres juntas se conectan en rojo, ese es el ataque. Clic 5: quitamos una pata (aquí, la salida) y el camino se rompe. Idea de Simon Willison, la usa NVIDIA en 04a. Insistir: la salida incluye al servicio del modelo y a la respuesta del chat.

---

## El ataque: una FAQ envenenada

:::diagrama c51-faq-envenenada

Notas:
Clic 1: alguien propone un cambio "útil" a la FAQ del curso. Clic 2: la entrada se ve normal. Clic 3: el comentario escondido, que la página no muestra. Clic 4: el agente lo lee como una orden. Clic 5: el nombre, inyección de prompt (indirecta: la orden no la escribe el usuario, viene dentro de un dato que el agente lee). El estudiante solo preguntó dónde guardar su key.

---

## Lo que pasó, paso a paso

:::diagrama c51-ataque-pasos

Notas:
Un clic por paso: la pregunta; buscar_faq trae la entrada envenenada; el modelo lee el comentario como orden; enviar_http manda el token interno (tok-soporte-…) afuera; la respuesta al estudiante sale perfecta. Clic 6: ningún paso fue ilegal. Demo en el notebook opcional. En vivo el modelo real a veces cae y a veces no. "A veces" no es una defensa.

---

## Tres capas de defensa

:::diagrama c51-capas

Notas:
De adentro hacia afuera, un clic por capa: el prompt (¿qué quiere hacer?; al modelo se le engaña), el harness de OpenClaw (¿la llamada es válida?; solo revisa lo que programaste) y el sandbox de OpenShell (¿qué logra aunque lo engañen?; no entiende el contenido). Clic 4: la política se aplica por debajo del modelo. Mínimo privilegio (Saltzer y Schroeder, 1975). No intentes demostrar la intención del modelo: mide los límites.

---

## Cuatro mecanismos de OpenShell

:::diagrama c51-mecanismos

Notas:
Un clic por pregunta, cada una con su nombre técnico en la etiqueta: ¿a dónde se conecta? (espacio de red aislado + proxy CONNECT + OPA); ¿qué archivos alcanza? (Landlock); ¿qué acciones pide al sistema? (seccomp: sin ptrace, mount, setuid); ¿con qué poder empieza? (usuario sandbox, sin root). Clic 5: pronto pruebas usuario y seccomp; después, red y archivos. No leas los nombres técnicos en voz alta.

---

## Lo que el sandbox no ve

:::diagrama c51-no-ve

Notas:
Clic 1: una respuesta sale hacia un sitio permitido; el guardia revisa el destino y la deja pasar. Clic 2: por el mismo camino sale tu contraseña escondida en el mensaje; el guardia también la deja pasar. Clic 3: la allowlist aprueba el destino, no el significado de los bytes. Clic 4: lo que falta arriba. Tabla de NVIDIA 04a (alineada con el OWASP Top 10 for Agentic Applications): inyección de prompt → procedencia y aprobación humana; mal uso de tools → validar argumentos; abuso de identidad → tokens con alcance mínimo; memoria envenenada → historial revisable.

---

## Tu hoja de trifecta

:::diagrama c51-hoja

.lead Llénala para tu agente: la vas a usar en una clase futura.

Notas:
El ejemplo de Soporte NemoClaw, un clic por pata: datos privados (MEMORY.md, resúmenes del cron, el token del gateway), no confiable (la FAQ, las preguntas), salida (el modelo, clawhub.ai, el chat). Clic 4: la pata que quitamos, no guardar datos personales. La tabla completa y cinco casos para practicar están en la página de la clase; pide que la guarden como trifecta.md.

---

## Errores comunes

:::bad
"Mi agente no sale a internet" → el modelo y el chat también son salidas.
:::

:::bad
"Lo arreglo en el prompt" → es la capa más débil.
:::

:::bad
"El sandbox me protege de todo" → lo desmentimos con datos más adelante.
:::

Notas:
Cierra con la idea fuerza: quitar una pata rompe el ataque.
