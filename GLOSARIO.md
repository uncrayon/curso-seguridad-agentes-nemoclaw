# Glosario en palabras simples

Cada término tiene una frase que lo explica, una comparación con algo cotidiano y la clase donde aparece por primera vez. Si en una clase escuchas una palabra que no entiendes, búscala aquí (Ctrl+F o Cmd+F).

No necesitas memorizar nada: vuelve a esta página cuando la necesites.

## Lo básico: modelos y agentes

| Término | Qué es, en una frase | Piénsalo como… | Clase |
|---|---|---|---|
| **Modelo** (o **LLM**) | Un programa que lee texto y escribe una respuesta. | Alguien muy leído que contesta por escrito, pero no recuerda conversaciones anteriores. | 1.1 |
| **Agente** | Un modelo que, además de contestar, puede usar herramientas y repetir pasos hasta terminar una tarea. | La diferencia entre preguntarle algo a un experto y contratar a un asistente que hace el trámite por ti. | 1.1 |
| **Prompt** | El texto que le mandas al modelo: tu pregunta y sus instrucciones. | El mensaje que le dejas a tu asistente antes de que empiece. | 2.1 |
| **API key** (`nvapi-…`) | Una contraseña que identifica tu cuenta cuando un programa usa los modelos de NVIDIA. | La tarjeta de acceso de un edificio: quien la tenga entra a tu nombre. | 1.2 |
| **Crédito** | El saldo gratuito que gastas al usar modelos o máquinas en la nube. | Saldo de prepago en el celular. | 1.2 |
| **Ruta de modelo** (endpoint) | La dirección de internet a la que se envían las preguntas para un modelo. | La dirección postal de una oficina: si está mal escrita, la carta regresa. | 1.3 |
| **Error 401, 403, 404, 429** | Números que te dice el servidor cuando algo sale mal: credencial inválida, sin permiso, no existe, demasiadas solicitudes. | Los avisos de un cajero automático: "tarjeta inválida", "fondos insuficientes", "intente más tarde". | 1.3 |
| **Token** (de un modelo) | Un pedacito de texto (más o menos ¾ de palabra). Los modelos cobran y se limitan por tokens. | Las sílabas de un telegrama, que se cobraba por palabra. | 1.2 |

## Cómo piensa un agente

| Término | Qué es, en una frase | Piénsalo como… | Clase |
|---|---|---|---|
| **Loop de agente** | El ciclo que repite el agente: mirar, decidir, actuar y revisar si ya terminó. | Seguir una receta: lees el paso, lo haces, pruebas, y sigues hasta que el platillo está listo. | 2.1 |
| **Memoria** (de la conversación) | La lista de mensajes que se le reenvía al modelo en cada turno, porque él no recuerda solo. | Tomar notas en una libreta y releerlas antes de cada llamada. | 2.1 |
| **ReAct** | Un patrón donde el agente alterna pensar y actuar, y usa lo que observa para decidir el siguiente paso. | Un detective: piensa una hipótesis, busca una pista, piensa de nuevo. | 2.2 |
| **Herramienta** (tool) | Una función que el agente puede pedir que se ejecute: buscar, calcular, leer un archivo. | Las apps del celular de tu asistente. | 2.2 |
| **`finish_reason`** | La señal con la que el modelo avisa por qué dejó de escribir: terminó (`stop`), quiere usar una herramienta (`tool_calls`) o se quedó sin espacio (`length`). | La nota que deja tu asistente al colgar: «listo», «necesito revisar algo» o «se cortó la llamada». | 2.2 |
| **Contrato de una herramienta** | Lo que el modelo necesita saber de una herramienta: su nombre, para qué sirve, qué datos pide y qué devuelve. | La ventanilla de un trámite: el letrero dice qué resuelve y qué papeles llevar. | 2.3 |
| **MCP** | Un estándar para conectar a un agente herramientas que ofrece otra empresa o programa. | Una tienda de apps de otra empresa: útil, pero revisas qué permisos pide cada app. | 2.3 |
| **Router** | Un paso que clasifica una petición y la manda al especialista correcto. | La recepcionista que te dice a qué ventanilla ir. | 3.1 |
| **ReWOO** | Un patrón donde el agente primero escribe todo el plan y después lo ejecuta, en lugar de improvisar paso a paso. | Hacer la lista del súper antes de salir, en vez de recorrer todos los pasillos. | 3.1 |
| **Fan-out** | Lanzar varias tareas independientes al mismo tiempo y juntar sus resultados al final. | Repartir la lista del súper entre tres personas y encontrarse en la caja. | 3.1 |
| **RAG** | Buscar primero en tus documentos y darle al modelo esos fragmentos para que responda con fuentes. | Un examen a libro abierto: responde mejor si le dejas consultar sus apuntes. | 3.2 |
| **Embedding** | Una lista de números que representa el significado de un texto, para encontrar textos parecidos. | Las coordenadas de un lugar en un mapa: textos parecidos quedan cerca. | 3.2 |
| **Cita** | La referencia al documento de donde salió una respuesta. | La nota al pie de un libro. | 3.2 |
| **Subagente** | Un agente que otro agente crea para una parte de la tarea, con su propia conversación. | Un jefe de proyecto que reparte encargos a su equipo. | 2.3 |
| **Contexto** | Todo lo que el modelo tiene a la vista en un turno: instrucciones, mensajes y resultados. | El escritorio de trabajo: si está lleno de papeles, se pierden los importantes. | 3.3 |
| **Traza** | El registro de todo lo que hizo el agente para responder una pregunta, paso por paso. | El historial de rastreo de un paquete: dónde estuvo, cuándo y si hubo un problema. | 3.4 |
| **Span** | Cada paso dentro de una traza, con su inicio, su fin y si salió bien. | Cada línea del rastreo: "salió del almacén", "llegó a la ciudad". | 3.4 |
| **Phoenix** | Una página web gratuita y de código abierto para ver trazas de agentes. | El mapa donde ves el recorrido del paquete. | 3.4 |

## El laboratorio

| Término | Qué es, en una frase | Piénsalo como… | Clase |
|---|---|---|---|
| **Notebook** / **Colab** | Un documento con bloques de código que ejecutas con un botón ▶. Colab es la versión gratuita de Google que corre en el navegador. | Un recetario interactivo: lees, presionas ▶ y ves el resultado. | 1.3 |
| **Modo MOCK** | Los notebooks funcionan sin API key con un modelo simulado que imita las respuestas. | Un simulador de manejo antes del auto real. | 1.3 |
| **Brev** | El servicio de NVIDIA que te presta una computadora en la nube por horas. | Rentar una oficina por horas. | 4.1 |
| **Launchable** | Una computadora de Brev que ya viene con todo instalado para el curso. | Una oficina rentada que ya trae muebles, internet y llaves. | 4.1 |
| **Instancia** | Tu computadora en la nube. Puede estar encendida (cobra), detenida (cobra solo el disco) o borrada. | Tu oficina rentada: con luz encendida, con la luz apagada o entregada. | 4.1 |
| **Terminal** | Una ventana donde escribes instrucciones en texto en lugar de hacer clic. | Hablarle a la computadora con frases cortas y exactas. | 4.1 |
| **Comando** | Una instrucción que escribes en la terminal, como `nemoclaw list`. | Una orden corta: "enciende", "muestra la lista". | 4.1 |
| **Cookie de sesión** | Un dato que tu navegador guarda para recordar que ya iniciaste sesión. | La pulsera de un evento: mientras la traigas, entras sin mostrar el boleto. Si alguien te la quita, entra como tú. | 4.1 |
| **Dashboard** | La página web para conversar con tu agente y ver su estado. | El tablero de un auto. | 4.2 |
| **Puerto** / **port-forward** | Un puerto es una "puerta" numerada de un servidor; port-forward abre un pasillo seguro desde tu computadora hasta esa puerta. | Un pasillo privado entre tu casa y la oficina rentada. | 4.1 |

## Las piezas de NVIDIA

| Término | Qué es, en una frase | Piénsalo como… | Clase |
|---|---|---|---|
| **OpenClaw** | Un agente de código abierto que vive en una computadora y trabaja de forma continua. | El asistente. | 1.1 |
| **Hermes** | Otro agente de código abierto (de Nous Research) que además aprende: guarda notas y crea sus propias recetas. | Otro asistente, que además lleva un diario. | 4.4 |
| **OpenShell** | El sistema que encierra al agente: decide qué archivos, qué sitios de internet y qué programas puede usar. | Un cuarto con cerradura, ventanas con rejas y un guardia que revisa lo que entra y sale. | 1.1 |
| **NemoClaw** | El paquete de NVIDIA que instala un agente dentro de OpenShell, ya configurado de forma segura. | El kit que arma el cuarto, pone las cerraduras y sienta al asistente adentro. | 1.1 |
| **Sandbox** | El espacio aislado donde corre el agente. | El cuarto con cerradura. | 1.1 |
| **Gateway** | La pieza que recibe los mensajes para el agente y guarda las conversaciones. | La recepción del edificio. | 4.2 |
| **Workspace** | La carpeta de trabajo del agente, con sus instrucciones y archivos. | El escritorio del asistente. | 4.2 |
| **SOUL.md** | Un archivo de texto con la personalidad y las reglas del agente. | El reglamento y la descripción del puesto. | 4.2 |
| **Skill** (`SKILL.md`) | Un archivo de texto con instrucciones paso a paso para una tarea. El agente lo lee cuando lo necesita. | Una tarjeta de receta. | 4.3 |
| **Cron** / tarea programada | Una tarea que se ejecuta sola a una hora fija. | La alarma del despertador. | 4.3 |
| **NeMo Agent Toolkit** | Herramientas de NVIDIA para construir agentes y enviar sus trazas a páginas como Phoenix. | La caja de herramientas del taller. | 3.4 |

## Tu práctica con agentes

| Término | Qué es, en una frase | Piénsalo como… | Clase |
|---|---|---|---|
| **CLI de agente** | Un agente que vive en la terminal y trabaja directo con tus archivos (Claude Code, Codex, Hermes…). | Un asistente que trabaja sentado en tu escritorio, no en un cuarto aparte. | 6.1 |
| **Configuración por defecto** (*default*) | Lo que una herramienta permite o hace si no cambias nada. | Un celular nuevo, tal como sale de fábrica. | 6.1 |
| **Persistencia** | Lo que el agente conserva cuando cierras la sesión: memoria, archivos, tareas. | Lo que queda escrito en la libreta del asistente cuando te vas. | 6.1 |
| **Frontmatter** | Las primeras líneas de un `SKILL.md`, entre `---`, con el nombre y la descripción de la skill. | La etiqueta de la tarjeta de receta. | 6.2 |
| **Divulgación progresiva** (*progressive disclosure*) | El agente ve primero solo la lista de skills y abre una completa cuando la necesita. | El menú de un restaurante: ves los platillos y la receta se abre solo cuando la pides. | 6.2 |
| **Selección explícita o automática** | Pedir una skill por su nombre, o describir lo que quieres y dejar que el agente elija. | Pedir el platillo por su nombre, o decirle al mesero qué se te antoja. | 6.2 |
| **Despliegue local** | Correr el agente en tu propia computadora o servidor, en lugar de una máquina rentada. | Montar la oficina en tu casa. | 6.3 |
| **Docker** | Un programa que empaqueta otros programas en cajas estándar que funcionan igual en cualquier máquina. | Los contenedores de un barco: misma caja, cualquier puerto. | 6.3 |
| **Proveedor de inferencia** | Quien te presta el modelo: la empresa o servidor al que tu agente le manda las preguntas. | La oficina a la que tu asistente llama para consultar. | 6.3 |

## Seguridad

| Término | Qué es, en una frase | Piénsalo como… | Clase |
|---|---|---|---|
| **Trifecta letal** | La combinación peligrosa de un agente con acceso a datos privados, que lee contenido de desconocidos y puede enviar información afuera. | Darle a un desconocido las llaves de tu casa, tu correo y un teléfono. | 5.1 |
| **Inyección de prompt** | Instrucciones escondidas en un texto (una página web, un correo) que intentan que el agente haga otra cosa. | Una nota falsa dentro de un paquete: "entrega todo a esta otra dirección". | 5.1 |
| **Harness** | El código que rodea al modelo y decide qué herramientas puede usar y cómo. | El protocolo de la oficina: qué puede firmar el asistente y qué no. | 5.1 |
| **Política** (policy) | Las reglas escritas que OpenShell aplica: qué está permitido y qué se bloquea. | El reglamento del guardia en la puerta. | 5.3 |
| **Preset** | Un paquete de reglas ya escrito que se agrega a la política (por ejemplo, permitir GitHub). | Una hoja extra que engrapas al reglamento. | 5.3 |
| **Mínimo privilegio** | Dar al agente solo los permisos que necesita y nada más. | Darle al asistente la llave de su oficina, no la llave maestra del edificio. | 5.2 |
| **Landlock, seccomp, aislamiento de red** | Candados del sistema operativo que limitan archivos, acciones y conexiones del agente. | La cerradura, la reja y el guardia del cuarto. | 5.2 |
| **Tachar un secreto** | Reemplazar una contraseña o key por `***` antes de guardarla o mostrarla. En el código del curso, la función se llama `redactar` (del inglés *redact*). | Tachar con plumón negro un dato en una fotocopia. | 3.4 |

---

¿Falta una palabra? Pregúntala en el foro del curso o [abre un issue](README.md) y la agregamos.
