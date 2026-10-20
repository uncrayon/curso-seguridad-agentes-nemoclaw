"""Diagramas del Módulo 4. Se usan en slides.md con ":::diagrama <nombre>".

Usa las piezas de tools/diagramas.py (nodo, flecha, cuarto, chips, pie) y las clases CSS del kit
(assets/slides.css, sección "Diagramas"). Estilos nuevos solo en assets/diagramas-m4.css.
Cada texto visible va en T["es"] y T["en"].

Piezas propias de este módulo (CSS en assets/diagramas-m4.css):
  carta(...)    una tarjeta dg-card con título e ícono
  matriz(...)   una tabla dibujada (filas que aparecen con cada clic)
  .m4-h         nodo horizontal: ícono a la izquierda, texto a la derecha
  .m4-fork      un nodo que se abre en varias ramas (dg-fan)
  .m4-lane      un carril con etiqueta a la izquierda
"""
from diagramas import chips, cuarto, flecha, nodo, pie  # noqa: F401


def _p(p):
    return f' data-paso="{p}"' if p else ""


def carta(titulo, contenido, icono="", clase="", paso=None, sub=""):
    ic = f'<span class="dg-i">{icono}</span> ' if icono else ""
    s = f'<small class="dg-card-sub">{sub}</small>' if sub else ""
    return f'<div class="dg-card m4-card {clase}"{_p(paso)}><h3>{ic}{titulo}</h3>{s}{contenido}</div>'


def cita(texto):
    return f'<p class="m4-quote">{texto}</p>'


def llamada(texto, tipo="warn", paso=None):
    return f'<div class="call {tipo}"{_p(paso)}><p>{texto}</p></div>'


def matriz(columnas, filas, clase=""):
    """columnas: [(icono, texto)]; filas: [(paso, icono, nombre, [celdas], clase_fila)]."""
    cab = '<div class="m4-mx-h"></div>' + "".join(
        f'<div class="m4-mx-h m4-mx-c{j}"><span class="dg-i">{ic}</span>{tx}</div>'
        for j, (ic, tx) in enumerate(columnas, 1))
    cuerpo = ""
    for paso, ic, nombre, celdas, cf in filas:
        cuerpo += f'<div class="m4-mx-name {cf}"{_p(paso)}><span class="dg-ico">{ic}</span><b>{nombre}</b></div>'
        cuerpo += "".join(f'<div class="m4-mx-cell m4-mx-c{j} {cf}"{_p(paso)}>{c}</div>'
                          for j, c in enumerate(celdas, 1))
    return (f'<div class="dg m4-matrix {clase}" style="grid-template-columns:auto repeat({len(columnas)},1fr)">'
            f"{cab}{cuerpo}</div>")


def carril(etiqueta, contenido, paso=None, clase=""):
    return (f'<div class="m4-lane {clase}"{_p(paso)}><span class="m4-lane-lab">{etiqueta}</span>'
            f'<div class="dg-row">{contenido}</div></div>')


# ------------------------------------------------------------------------------------------
# Textos por idioma
# ------------------------------------------------------------------------------------------
T = {
    "es": {
        # 4.2 · edificio
        "tu": "Tú", "tu_sub": "escribes un mensaje",
        "gw": "Gateway", "gw_sub": "la recepción del edificio",
        "gw_c1": "Recibe cada turno", "gw_c2": "Guarda el historial",
        "cuarto": "Sandbox · cuarto con cerradura",
        "oc_sub": "el asistente",
        "ws": "Workspace", "ws_sub": "su escritorio, con sus papeles",
        "ws_nota": "Tu agente es lo que dicen los papeles de su escritorio",
        # 4.2 · escritorio
        "esc": "El escritorio del asistente",
        "soul_sub": "el puesto y sus reglas", "agents_sub": "cómo trabaja",
        "user_sub": "quién eres tú", "tools_sub": "notas de sus herramientas",
        "hb_sub": "tareas periódicas", "skills_sub": "sus tarjetas de receta",
        "memdir_sub": "notas del día", "mem_sub": "lo importante, a largo plazo",
        "relee": "Lo relee cada vez que empieza una conversación nueva",
        # 4.2 · memoria
        "conv": "La conversación", "conv_sub": "la guarda la recepción (gateway)",
        "hist": "Historial del chat", "hist_sub": "dura lo que dura la sesión",
        "se_pierde": "Se pierde al reiniciar la sesión",
        "arch": "Los archivos", "arch_sub": "en su escritorio (workspace)",
        "lo_imp": "lo importante",
        "sobrevive": "Sobreviven al reinicio de la sesión y del cuarto",
        # 4.2 · planos
        "operador": "Operador", "operador_sub": "tú, afuera del cuarto",
        "terminal_maq": "En la terminal",
        "lee_arch": "lee el archivo",
        "agente": "Agente", "agente_sub": "adentro, con reglas más estrictas",
        "ya_lo_hice": "«Ya lo hice»",
        "los_arch": "Los archivos", "los_arch_sub": "lo que de verdad hay",
        "evidencia": "Lo que el agente dice no es evidencia. El archivo sí.",
        # 4.2 · dice vs archivo
        "dice": "Lo que dice el agente",
        "dice_cita": "«Mi escritorio tiene SOUL.md, AGENTS.md y MEMORY.md…»",
        "relato": "Un relato: puede ser correcto o no",
        "muestra": "Lo que muestra el archivo",
        "lista_real": "La lista real, leída por el operador",
        "compara": "Compara las dos listas. Si no coinciden, gana el archivo.",
        # 4.2 · dos sesiones
        "conv_a": "Conversación A", "conv_a_sub": "pide guardar una preferencia",
        "op_lee": "Operador", "op_lee_sub": "lee MEMORY.md y la busca",
        "conv_b": "Conversación B", "conv_b_sub": "nueva: la encuentra en disco",
        "guardado": "«Guardado» no es prueba. Léelo de vuelta.",
        # 4.2 · SOUL.md
        "seccion": "Tu sección", "seccion_sub": "en español normal",
        "s_c1": "A quién ayuda", "s_c2": "Idioma y tono", "s_c3": "Lo que nunca hace",
        "agregala": "agrégala al final", "soul_esc": "en el escritorio del agente",
        "conv_nueva": "conversación nueva",
        "soporte": "Soporte NemoClaw", "soporte_sub": "ya conoce su puesto",
        "abre_nueva": "Una conversación ya abierta no cambia: abre una nueva",
        # 4.2 · tilde
        "pides": "Le pides", "pides_sub": "«agrégalo a ~/SOUL.md»",
        "tilde": "~ = /sandbox", "suelto": "SOUL.md suelto", "suelto_sub": "en /sandbox · nadie lo lee",
        "ruta": "ruta completa", "del_esc": "SOUL.md del escritorio", "del_esc_sub": ".openclaw/workspace/ · el que lee",
        "tilde_nota": "Dentro del cuarto, ~ es la entrada, no el escritorio. Pide la ruta completa y léelo de vuelta.",
        # 4.3 · receta y despertador
        "skill": "Skill", "skill_sub": "una tarjeta de receta",
        "pides_algo": "Pides algo", "lee_receta": "Lee la receta", "lee_receta_sub": "solo cuando la necesita",
        "responde": "Responde",
        "cron": "Tarea programada", "cron_sub": "la alarma del despertador",
        "suena": "Suena la alarma", "trabaja_solo": "Trabaja solo", "deja_arch": "Deja un archivo",
        "corre_solo": "Lo que corre solo, corre aunque nadie lo mire.",
        # 4.3 · controles
        "sesion": "Sesión", "sesion_sub": "¿qué conversación recuerda?",
        "directiva": "Directiva", "directiva_sub": "¿qué instrucciones sigue?",
        "disparador": "Disparador", "disparador_sub": "¿qué la hace empezar?",
        "siempre": "Agente siempre activo",
        "cualquier": "Sirven para describir cualquier automatización, de cualquier herramienta",
        # 4.3 · mecanismos
        "m_skill_s": "tu misma conversación", "m_skill_d": "su tarjeta: SKILL.md", "m_skill_t": "cuando la pides",
        "m_cron_s": "una nueva y vacía cada vez", "m_cron_d": "el mensaje que dejaste", "m_cron_t": "a una hora fija",
        "m_hb_s": "una propia", "m_hb_d": "HEARTBEAT.md", "m_hb_t": "cada 30 minutos",
        "subagente": "Subagente", "m_sub_s": "una nueva", "m_sub_d": "lo que pide quien lo crea",
        "m_sub_t": "el agente que lo crea",
        "hoy": "Hoy corremos skill y cron. Heartbeat y subagente: solo como idea.",
        # 4.3 · anatomía
        "etiqueta": "La etiqueta", "etiqueta_sub": "así la encuentra el agente",
        "desc_txt": "«Responde dudas de estudiantes del curso con la FAQ. Úsala cuando pregunten por 401, Brev, cookies u OpenShell…»",
        "pasos": "Los pasos", "pasos_sub": "lo que hace, en orden",
        "paso1": "Clasifica la duda", "paso2": "Busca en la FAQ", "paso3": "Responde con pasos y cita la fuente",
        "reglas": "Las reglas", "reglas_sub": "lo que nunca hace",
        "nunca_keys": "Nunca pide API keys", "nunca_inventa": "Nunca inventa comandos",
        "desc_decide": "La descripción decide si el agente la encuentra solo: escribe las palabras con que alguien pediría ayuda.",
        # 4.3 · instalar
        "sk_nombre": "Skill soporte-nemoclaw", "sk_nombre_sub": "el procedimiento",
        "faq": "FAQ del curso", "faq_sub": "el conocimiento",
        "instalas": "la instalas", "subes": "la subes",
        "escritorio": "Escritorio del agente",
        "rota": "Error en vivo: una copia sin <b>name</b> en la etiqueta. NemoClaw la rechaza y te dice qué falta.",
        # 4.3 · explícita / automática
        "explicita": "Explícita", "explicita_sub": "le das la ruta de la receta",
        "explicita_cita": "«Lee skills/soporte-nemoclaw/SKILL.md y síguelo para esta duda…»",
        "puede": "Prueba que <b>puede</b> seguirla",
        "automatica": "Automática", "automatica_sub": "solo describes el problema",
        "automatica_cita": "«Un estudiante dice: “Mi notebook responde HTTP 401”. ¿Qué le respondes?»",
        "elige": "Prueba que <b>la elige</b> solo",
        "mejora": "Si no la elige solo, mejora la descripción. Pruébalo siempre en una conversación nueva.",
        # 4.3 · cron
        "c1": "Pones la alarma", "c1s": "para dentro de 2 minutos",
        "c2": "Suena", "c2s": "nadie escribe en el chat",
        "c3": "Conversación nueva", "c3s": "vacía, sin historial",
        "c4": "Sigue tu mensaje", "c4s": "lee su skill y la FAQ",
        "c5": "Deja un archivo", "c5s": "un resumen de la FAQ",
        "zona": "«Run at» usa la hora local de tu navegador; la fecha dentro del archivo va en hora universal (UTC).",
        # 4.3 · la prueba
        "registro": "El registro dice «ok»", "registro_sub": "no basta",
        "tu_op": "Tú, como operador", "tu_op_sub": "lees el archivo",
        "existe": "El archivo existe", "existe_sub": "esa es la evidencia",
        "nadie": "Nadie escribió en el chat y el archivo está ahí",
        # 4.3 · nadie mira
        "tarea": "Tu tarea programada", "tarea_sub": "suena a su hora",
        "sola": "Se dispara sola", "sola_sub": "aunque no estés",
        "comparte": "Comparte el escritorio", "comparte_sub": "lo que escribe afecta lo que sigue",
        "gasta": "Gasta crédito", "gasta_sub": "en cada disparo",
        "nombra": "Ponle nombre a tus tareas, revisa la lista y borra las que no reconozcas.",
        # 4.4 · mismo cuarto
        "cuarto_os": "OpenShell · cuarto con cerradura",
        "oc_41": "clases 4.1 a 4.3", "cambias": "cambias",
        "hermes_sub": "lleva un diario",
        "igual": "Se queda igual", "igual_sub": "el cuarto, las reglas de red y la key afuera",
        "cambia": "Cambia", "cambia_sub": "el asistente que trabaja adentro",
        "nuevo": "Lo nuevo de Hermes", "nuevo_sub": "guarda notas y escribe sus propias recetas",
        # 4.4 · crear
        "h1": "Pausa OpenClaw", "h1s": "no lo borres: libera memoria",
        "h2": "Tu key, oculta", "h2s": "no se ve ni queda guardada",
        "h3": "Crea el cuarto", "h3s": "mi-hermes, con nemohermes",
        "h4": "¿Está sano?", "h4s": "estado y prueba de salud",
        "h5": "Una puerta nueva", "h5s": "para que otros programas le hablen",
        "credito": "Usa ≈30 min de tu sesión de laboratorio y crea un segundo cuarto. Al terminar, enciende otra vez my-assistant.",
        # 4.4 · comparar
        "personalidad": "Personalidad", "memoria": "Memoria", "skills": "Skills",
        "conversaciones": "Conversaciones", "puerta": "Puerta para programas",
        "oc_soul": "SOUL.md en su escritorio", "he_soul": "/sandbox/SOUL.md",
        "oc_mem": "MEMORY.md en su escritorio", "he_mem": ".hermes/memories/ · con límite",
        "oc_sk": "skills/ en su escritorio", "he_sk": ".hermes/skills/ · también crea las suyas",
        "oc_conv": "archivos de texto", "he_conv": "una base de datos: state.db",
        "oc_api": "gateway (WebSocket)", "he_api": "compatible con OpenAI · 8642",
        "igual_dos": "Igual en los dos: el cuarto, la key afuera, las reglas de red y <b>skill install</b>",
        # 4.4 · misma skill
        "receta_43": "la receta de la clase 4.3",
        "oc_rutas": "skills/ del escritorio", "dos_rutas": "cambian 2 rutas",
        "he_rutas": "la FAQ en /sandbox/faq",
        "resultado": "Responde con categoría, pasos y Fuente: faq/errores-api.md, sin darle la ruta",
        # 4.4 · aprobación
        "sin_ap": "Sin aprobación", "con_ap": "Con aprobación",
        "recuerda": "«Recuerda esto»", "malicioso": "…o un texto malicioso",
        "diario": "Su diario", "diario_sin": "guardado sin preguntarte",
        "espera": "Espera tu sí", "diario_con": "solo lo que apruebas",
        "recetas_ap": "Lo mismo con sus recetas: <b>/skills approval on</b>. Lo verás a fondo en el Módulo 5.",
        # 4.4 · dos capas
        "programa": "Tu programa en Python", "programa_sub": "habla por la puerta nueva",
        "con_token": "con token", "cuarto_he": "Sandbox de Hermes",
        "he_busca": "busca en la FAQ adentro",
        "capa1": "Capa 1 · tu programa", "capa1_sub": "la pregunta y la respuesta",
        "capa2": "Capa 2 · su historial", "capa2_sub": "lo que hizo adentro",
        "capas": "Desde fuera ves la pregunta y la respuesta; lo de adentro queda en el historial del agente",
        # 4.4 · avance
        "dos_agentes": "Soporte NemoClaw en dos agentes",
        "a1": "Misma skill", "a2": "Misma personalidad", "a3": "Un cliente en Python",
        "mod5": "Para el Módulo 5", "r1": "Memoria que se escribe sola",
        "r2": "Recetas que crea el agente", "r3": "Una puerta con token",
        "riesgo": "Más poder, más superficie de riesgo",
    },
    "en": {
        "tu": "You", "tu_sub": "you send a message",
        "gw": "Gateway", "gw_sub": "the building's front desk",
        "gw_c1": "Takes every turn", "gw_c2": "Keeps the history",
        "cuarto": "Sandbox · locked room",
        "oc_sub": "the assistant",
        "ws": "Workspace", "ws_sub": "its desk, with its papers",
        "ws_nota": "Your agent is whatever the papers on its desk say",
        "esc": "The assistant's desk",
        "soul_sub": "the job and its rules", "agents_sub": "how it works",
        "user_sub": "who you are", "tools_sub": "notes on its tools",
        "hb_sub": "periodic tasks", "skills_sub": "its recipe cards",
        "memdir_sub": "daily notes", "mem_sub": "what matters, long term",
        "relee": "It rereads it every time a new conversation starts",
        "conv": "The conversation", "conv_sub": "kept by the front desk (gateway)",
        "hist": "Chat history", "hist_sub": "lasts as long as the session",
        "se_pierde": "Lost when the session resets",
        "arch": "The files", "arch_sub": "on its desk (workspace)",
        "lo_imp": "what matters",
        "sobrevive": "They survive a session reset and a room restart",
        "operador": "Operator", "operador_sub": "you, outside the room",
        "terminal_maq": "At the terminal",
        "lee_arch": "reads the file",
        "agente": "Agent", "agente_sub": "inside, with stricter rules",
        "ya_lo_hice": "“Done!”",
        "los_arch": "The files", "los_arch_sub": "what's really there",
        "evidencia": "What the agent says isn't evidence. The file is.",
        "dice": "What the agent says",
        "dice_cita": "“My desk has SOUL.md, AGENTS.md and MEMORY.md…”",
        "relato": "A story: it may or may not be right",
        "muestra": "What the file shows",
        "lista_real": "The real list, read by the operator",
        "compara": "Compare both lists. If they don't match, the file wins.",
        "conv_a": "Conversation A", "conv_a_sub": "asks to save a preference",
        "op_lee": "Operator", "op_lee_sub": "reads MEMORY.md, looks for it",
        "conv_b": "Conversation B", "conv_b_sub": "new: finds it on disk",
        "guardado": "“Saved” isn't proof. Read it back.",
        "seccion": "Your section", "seccion_sub": "in plain language",
        "s_c1": "Who it helps", "s_c2": "Language and tone", "s_c3": "What it never does",
        "agregala": "append it", "soul_esc": "on the agent's desk",
        "conv_nueva": "new conversation",
        "soporte": "Soporte NemoClaw", "soporte_sub": "now knows its job",
        "abre_nueva": "A conversation that's already open doesn't change: start a new one",
        "pides": "You ask", "pides_sub": "“append it to ~/SOUL.md”",
        "tilde": "~ = /sandbox", "suelto": "Stray SOUL.md", "suelto_sub": "in /sandbox · nobody reads it",
        "ruta": "full path", "del_esc": "The desk's SOUL.md", "del_esc_sub": ".openclaw/workspace/ · the one it reads",
        "tilde_nota": "Inside the room, ~ is the entrance, not the desk. Ask for the full path and read it back.",
        "skill": "Skill", "skill_sub": "a recipe card",
        "pides_algo": "You ask", "lee_receta": "Reads the recipe", "lee_receta_sub": "only when it needs it",
        "responde": "Answers",
        "cron": "Scheduled task", "cron_sub": "the alarm clock",
        "suena": "The alarm rings", "trabaja_solo": "Works alone", "deja_arch": "Leaves a file",
        "corre_solo": "What runs on its own runs even when nobody's watching.",
        "sesion": "Session", "sesion_sub": "what conversation does it remember?",
        "directiva": "Directive", "directiva_sub": "what instructions does it follow?",
        "disparador": "Trigger", "disparador_sub": "what makes it start?",
        "siempre": "Always-on agent",
        "cualquier": "They describe any automation, from any tool",
        "m_skill_s": "your same conversation", "m_skill_d": "its card: SKILL.md", "m_skill_t": "when you ask",
        "m_cron_s": "a new, empty one each time", "m_cron_d": "the message you left", "m_cron_t": "at a set time",
        "m_hb_s": "its own", "m_hb_d": "HEARTBEAT.md", "m_hb_t": "every 30 minutes",
        "subagente": "Subagent", "m_sub_s": "a new one", "m_sub_d": "what its creator asks",
        "m_sub_t": "the agent that creates it",
        "hoy": "Today we run skill and cron. Heartbeat and subagent: just the idea.",
        "etiqueta": "The label", "etiqueta_sub": "how the agent finds it",
        "desc_txt": "“Answers course students' questions with the FAQ. Use it when they ask about 401, Brev, cookies or OpenShell…”",
        "pasos": "The steps", "pasos_sub": "what it does, in order",
        "paso1": "Classify the question", "paso2": "Search the FAQ", "paso3": "Answer with steps and cite the source",
        "reglas": "The rules", "reglas_sub": "what it never does",
        "nunca_keys": "Never asks for API keys", "nunca_inventa": "Never makes up commands",
        "desc_decide": "The description decides whether the agent finds it on its own: write the words someone would use to ask for help.",
        "sk_nombre": "soporte-nemoclaw skill", "sk_nombre_sub": "the procedure",
        "faq": "Course FAQ", "faq_sub": "the knowledge",
        "instalas": "you install it", "subes": "you upload it",
        "escritorio": "The agent's desk",
        "rota": "Live error: a copy with no <b>name</b> on its label. NemoClaw rejects it and tells you what's missing.",
        "explicita": "Explicit", "explicita_sub": "you give it the recipe's path",
        "explicita_cita": "“Read skills/soporte-nemoclaw/SKILL.md and follow it for this question…”",
        "puede": "Proves it <b>can</b> follow it",
        "automatica": "Automatic", "automatica_sub": "you only describe the problem",
        "automatica_cita": "“A student says: ‘My notebook returns HTTP 401’. What do you tell them?”",
        "elige": "Proves it <b>picks it</b> on its own",
        "mejora": "If it doesn't pick it, improve the description. Always test in a new conversation.",
        "c1": "You set the alarm", "c1s": "for 2 minutes from now",
        "c2": "It rings", "c2s": "nobody types in the chat",
        "c3": "New conversation", "c3s": "empty, no history",
        "c4": "Follows your message", "c4s": "reads its skill and the FAQ",
        "c5": "Leaves a file", "c5s": "a summary of the FAQ",
        "zona": "“Run at” uses your browser's local time; the date inside the file is in universal time (UTC).",
        "registro": "The log says “ok”", "registro_sub": "not enough",
        "tu_op": "You, as the operator", "tu_op_sub": "you read the file",
        "existe": "The file exists", "existe_sub": "that's the evidence",
        "nadie": "Nobody typed in the chat and the file is there",
        "tarea": "Your scheduled task", "tarea_sub": "rings on time",
        "sola": "Fires on its own", "sola_sub": "even when you're away",
        "comparte": "Shares the desk", "comparte_sub": "what it writes affects what's next",
        "gasta": "Spends credit", "gasta_sub": "every time it fires",
        "nombra": "Name your tasks, review the list and delete the ones you don't recognize.",
        "cuarto_os": "OpenShell · locked room",
        "oc_41": "classes 4.1 to 4.3", "cambias": "you swap",
        "hermes_sub": "keeps a diary",
        "igual": "Stays the same", "igual_sub": "the room, the network rules and the key outside",
        "cambia": "Changes", "cambia_sub": "the assistant working inside",
        "nuevo": "What's new in Hermes", "nuevo_sub": "takes notes and writes its own recipes",
        "h1": "Pause OpenClaw", "h1s": "don't delete it: frees memory",
        "h2": "Your key, hidden", "h2s": "not shown, not saved",
        "h3": "Create the room", "h3s": "mi-hermes, with nemohermes",
        "h4": "Is it healthy?", "h4s": "status and health check",
        "h5": "A new door", "h5s": "so other programs can talk to it",
        "credito": "Uses ≈30 min of your lab sitting and creates a second room. When you finish, turn my-assistant back on.",
        "personalidad": "Personality", "memoria": "Memory", "skills": "Skills",
        "conversaciones": "Conversations", "puerta": "Door for programs",
        "oc_soul": "SOUL.md on its desk", "he_soul": "/sandbox/SOUL.md",
        "oc_mem": "MEMORY.md on its desk", "he_mem": ".hermes/memories/ · with a limit",
        "oc_sk": "skills/ on its desk", "he_sk": ".hermes/skills/ · also writes its own",
        "oc_conv": "text files", "he_conv": "a database: state.db",
        "oc_api": "gateway (WebSocket)", "he_api": "OpenAI-compatible · 8642",
        "igual_dos": "Same in both: the room, the key outside, the network rules and <b>skill install</b>",
        "receta_43": "the recipe from class 4.3",
        "oc_rutas": "skills/ on the desk", "dos_rutas": "2 paths change",
        "he_rutas": "the FAQ in /sandbox/faq",
        "resultado": "Answers with category, steps and Fuente: faq/errores-api.md, without being given the path",
        "sin_ap": "Without approval", "con_ap": "With approval",
        "recuerda": "“Remember this”", "malicioso": "…or a malicious text",
        "diario": "Its diary", "diario_sin": "saved without asking you",
        "espera": "Asks you first", "diario_con": "only what you approve",
        "recetas_ap": "Same for its recipes: <b>/skills approval on</b>. You'll dig into this in Module 5.",
        "programa": "Your Python program", "programa_sub": "talks through the new door",
        "con_token": "with a token", "cuarto_he": "Hermes's sandbox",
        "he_busca": "searches the FAQ inside",
        "capa1": "Layer 1 · your program", "capa1_sub": "the question and the answer",
        "capa2": "Layer 2 · its history", "capa2_sub": "what it did inside",
        "capas": "From outside you see the question and the answer; what happens inside stays in the agent's history",
        "dos_agentes": "Soporte NemoClaw on two agents",
        "a1": "Same skill", "a2": "Same personality", "a3": "A Python client",
        "mod5": "For Module 5", "r1": "Memory that writes itself",
        "r2": "Recipes the agent creates", "r3": "A door with a token",
        "riesgo": "More power, more risk surface",
    },
}


# ------------------------------------------------------------------------------------------
# 4.2 · Gateway y workspace
# ------------------------------------------------------------------------------------------
def c42_edificio(lang):
    t = T[lang]
    adentro = ('<div class="dg-row tight">'
               + nodo("assistant", "OpenClaw", t["oc_sub"], clase="is-primary")
               + nodo("folder_open", t["ws"], t["ws_sub"], clase="ok", paso=4) + "</div>")
    return ('<div class="dg dg-row">'
            + nodo("person", t["tu"], t["tu_sub"], paso=1)
            + flecha("h", paso=2)
            + nodo("domain", t["gw"], t["gw_sub"], paso=2, extra=chips([t["gw_c1"], t["gw_c2"]]))
            + flecha("h", paso=3)
            + cuarto(t["cuarto"], adentro, paso=3)
            + "</div>" + pie(t["ws_nota"], paso=5, icono="description"))


def c42_escritorio(lang):
    t = T[lang]
    tiles = [(1, "contract", "SOUL.md", t["soul_sub"], "is-primary"),
             (2, "list", "AGENTS.md", t["agents_sub"], ""), (2, "person", "USER.md", t["user_sub"], ""),
             (2, "settings", "TOOLS.md", t["tools_sub"], ""), (3, "schedule", "HEARTBEAT.md", t["hb_sub"], ""),
             (3, "menu_book", "skills/", t["skills_sub"], ""), (4, "edit_note", "memory/", t["memdir_sub"], ""),
             (4, "bookmark", "MEMORY.md", t["mem_sub"], "ok")]
    grid = "".join(nodo(ic, a, b, clase=f"mini {c}", paso=p) for p, ic, a, b, c in tiles)
    return ('<div class="dg m4-desk">'
            + carta(t["esc"], f'<div class="dg-grid">{grid}</div>', icono="folder_open", clase="is-primary",
                    sub="/sandbox/.openclaw/workspace/")
            + "</div>" + pie(t["relee"], paso=5, icono="replay"))


def c42_memoria(lang):
    t = T[lang]
    izq = carta(t["conv"], nodo("chat", t["hist"], t["hist_sub"], clase="warn")
                + pie(t["se_pierde"], icono="delete"), icono="forum", paso=1, sub=t["conv_sub"])
    der = carta(t["arch"], '<div class="dg-row">'
                + nodo("edit_note", "memory/", t["memdir_sub"], clase="mini", paso=2)
                + flecha("h", t["lo_imp"], paso=3)
                + nodo("bookmark", "MEMORY.md", t["mem_sub"], clase="mini ok", paso=3) + "</div>"
                + pie(t["sobrevive"], paso=4, icono="verified"),
                icono="folder_open", clase="is-primary", paso=2, sub=t["arch_sub"])
    return f'<div class="dg dg-two m4-two-eq">{izq}{der}</div>'


def c42_planos(lang):
    t = T[lang]
    dice = chips([f'<span class="dg-i">chat</span>{t["ya_lo_hice"]}'])
    adentro = ('<div class="dg-row tight">'
               + nodo("assistant", t["agente"], t["agente_sub"], extra=dice)
               + nodo("description", t["los_arch"], t["los_arch_sub"], clase="ok", paso=3) + "</div>")
    return ('<div class="dg dg-row">'
            + nodo("person", t["operador"], t["operador_sub"], clase="is-primary", paso=2,
                   extra=chips([f'<span class="dg-i">terminal</span>{t["terminal_maq"]}']))
            + flecha("h", t["lee_arch"], paso=3)
            + cuarto(t["cuarto"], adentro, paso=1)
            + "</div>" + pie(t["evidencia"], paso=4, icono="verified"))


def c42_dice_vs_archivo(lang):
    t = T[lang]
    izq = carta(t["dice"], cita(t["dice_cita"]) + pie(t["relato"], icono="info"), icono="chat", clase="m4-warn", paso=1)
    reales = chips(["SOUL.md", "AGENTS.md", "USER.md", "TOOLS.md", "IDENTITY.md", "HEARTBEAT.md", "POLICY.md"], "m4-files")
    der = carta(t["muestra"], reales + pie(t["lista_real"], icono="verified"), icono="terminal", clase="is-primary", paso=2)
    return f'<div class="dg dg-two m4-two-eq">{izq}{der}</div>' + llamada(t["compara"], "tip", paso=3)


def c42_dos_sesiones(lang):
    t = T[lang]
    return ('<div class="dg dg-row">'
            + nodo("forum", t["conv_a"], t["conv_a_sub"], paso=1)
            + flecha("h", paso=2)
            + nodo("visibility", t["op_lee"], t["op_lee_sub"], clase="is-primary", paso=2)
            + flecha("h", paso=3)
            + nodo("forum", t["conv_b"], t["conv_b_sub"], clase="ok", paso=3)
            + "</div>" + llamada(t["guardado"], "warn", paso=4))


def c42_soul(lang):
    t = T[lang]
    return ('<div class="dg dg-row">'
            + nodo("edit_note", t["seccion"], t["seccion_sub"], paso=1,
                   extra=chips([t["s_c1"], t["s_c2"], t["s_c3"]]))
            + flecha("h", t["agregala"], paso=2)
            + nodo("contract", "SOUL.md", t["soul_esc"], clase="is-primary", paso=2)
            + flecha("h", t["conv_nueva"], paso=3)
            + nodo("assistant", t["soporte"], t["soporte_sub"], clase="ok", paso=3)
            + "</div>" + pie(t["abre_nueva"], paso=4, icono="replay"))


def c42_tilde(lang):
    t = T[lang]
    ramas = (f'<div class="dg-fan-row" data-paso="2">{flecha("h", t["tilde"], clase="warn")}'
             f'{nodo("draft", t["suelto"], t["suelto_sub"], clase="bad m4-h")}</div>'
             f'<div class="dg-fan-row" data-paso="3">{flecha("h", t["ruta"])}'
             f'{nodo("contract", t["del_esc"], t["del_esc_sub"], clase="ok m4-h")}</div>')
    return ('<div class="dg m4-fork">'
            + nodo("chat", t["pides"], t["pides_sub"], clase="is-primary", paso=1)
            + f'<div class="dg-fan">{ramas}</div></div>'
            + pie(t["tilde_nota"], paso=4, icono="info"))


# ------------------------------------------------------------------------------------------
# 4.3 · Agentes siempre activos
# ------------------------------------------------------------------------------------------
def c43_receta_alarma(lang):
    t = T[lang]
    izq = carta(t["skill"], '<div class="dg-row">'
                + nodo("person", t["pides_algo"], clase="mini")
                + flecha("h")
                + nodo("menu_book", t["lee_receta"], t["lee_receta_sub"], clase="mini is-primary")
                + flecha("h")
                + nodo("check_circle", t["responde"], clase="mini ok") + "</div>",
                icono="menu_book", paso=1, sub=t["skill_sub"])
    der = carta(t["cron"], '<div class="dg-row">'
                + nodo("notifications", t["suena"], clase="mini")
                + flecha("h")
                + nodo("assistant", t["trabaja_solo"], clase="mini is-primary")
                + flecha("h")
                + nodo("description", t["deja_arch"], clase="mini ok") + "</div>",
                icono="timer", paso=2, sub=t["cron_sub"])
    return f'<div class="dg dg-two m4-two-eq">{izq}{der}</div>' + llamada(t["corre_solo"], "warn", paso=3)


def c43_controles(lang):
    t = T[lang]
    return ('<div class="dg dg-row">'
            + nodo("forum", t["sesion"], t["sesion_sub"], paso=1)
            + '<span class="m4-op" data-paso="2">+</span>'
            + nodo("description", t["directiva"], t["directiva_sub"], paso=2)
            + '<span class="m4-op" data-paso="3">+</span>'
            + nodo("bolt", t["disparador"], t["disparador_sub"], paso=3)
            + '<span class="m4-op" data-paso="4">=</span>'
            + nodo("update", t["siempre"], clase="is-primary big", paso=4)
            + "</div>" + pie(t["cualquier"], paso=5, icono="info"))


def c43_mecanismos(lang):
    t = T[lang]
    cols = [("forum", t["sesion"]), ("description", t["directiva"]), ("bolt", t["disparador"])]
    filas = [(1, "menu_book", "Skill", [t["m_skill_s"], t["m_skill_d"], t["m_skill_t"]], ""),
             (2, "timer", "Cron", [t["m_cron_s"], t["m_cron_d"], t["m_cron_t"]], ""),
             (3, "favorite", "Heartbeat", [t["m_hb_s"], t["m_hb_d"], t["m_hb_t"]], "m4-dim"),
             (3, "group", t["subagente"], [t["m_sub_s"], t["m_sub_d"], t["m_sub_t"]], "m4-dim")]
    return matriz(cols, filas) + pie(t["hoy"], paso=4, icono="info")


def c43_anatomia(lang):
    t = T[lang]

    def seccion(paso, icono, titulo, sub, contenido):
        return (f'<div class="m4-rc-sec"{_p(paso)}><div class="m4-rc-lab"><span class="dg-i">{icono}</span>'
                f'<b>{titulo}</b><small>{sub}</small></div><div class="m4-rc-body">{contenido}</div></div>')

    etiqueta = f'<p><code>name:</code> soporte-nemoclaw</p><p><code>description:</code> {t["desc_txt"]}</p>'
    pasos = f'<ol><li>{t["paso1"]}</li><li>{t["paso2"]}</li><li>{t["paso3"]}</li></ol>'
    reglas = chips([f'<span class="dg-i">block</span>{t["nunca_keys"]}',
                    f'<span class="dg-i">block</span>{t["nunca_inventa"]}'])
    return ('<div class="dg m4-recipe">'
            + seccion(1, "label", t["etiqueta"], t["etiqueta_sub"], etiqueta)
            + seccion(2, "list", t["pasos"], t["pasos_sub"], pasos)
            + seccion(3, "block", t["reglas"], t["reglas_sub"], reglas)
            + "</div>" + llamada(t["desc_decide"], "tip", paso=4))


def c43_instalar(lang):
    t = T[lang]
    adentro = ('<div class="dg-row tight">'
               + nodo("menu_book", "skills/", clase="mini ok", paso=3)
               + nodo("folder_open", "faq/", clase="mini ok", paso=4) + "</div>")
    return ('<div class="dg m4-merge">'
            + nodo("menu_book", t["sk_nombre"], t["sk_nombre_sub"], clase="is-primary m4-h", paso=1)
            + flecha("h", t["instalas"], paso=3)
            + cuarto(t["escritorio"], adentro, paso=3, clase="m4-merge-room")
            + nodo("folder", t["faq"], t["faq_sub"], clase="m4-h", paso=4)
            + flecha("h", t["subes"], paso=4)
            + "</div>" + llamada(t["rota"], "bad", paso=2))


def c43_explicita(lang):
    t = T[lang]
    izq = carta(t["explicita"], cita(t["explicita_cita"]) + pie(f'<span>{t["puede"]}</span>', icono="check_circle"),
                icono="route", paso=1, sub=t["explicita_sub"])
    der = carta(t["automatica"], cita(t["automatica_cita"]) + pie(f'<span>{t["elige"]}</span>', icono="auto_awesome"),
                icono="auto_awesome", clase="is-primary", paso=2, sub=t["automatica_sub"])
    return f'<div class="dg dg-two m4-two-eq">{izq}{der}</div>' + llamada(t["mejora"], "tip", paso=3)


def c43_cron(lang):
    t = T[lang]
    etapas = [("timer", t["c1"], t["c1s"]), ("notifications", t["c2"], t["c2s"]), ("forum", t["c3"], t["c3s"]),
              ("menu_book", t["c4"], t["c4s"]), ("description", t["c5"], t["c5s"])]
    pasos = "".join(f'<div class="dg-stage" data-paso="{i + 1}"><span class="dg-ico">{ic}</span>'
                    f'<b>{a}</b><small>{b}</small></div>' for i, (ic, a, b) in enumerate(etapas))
    return (f'<div class="dg dg-timeline"><div class="dg-track"></div>{pasos}</div>'
            + llamada(t["zona"], "warn", paso=6))


def c43_prueba(lang):
    t = T[lang]
    return ('<div class="dg dg-row">'
            + nodo("list", t["registro"], t["registro_sub"], clase="warn", paso=1)
            + flecha("h", paso=2)
            + nodo("visibility", t["tu_op"], t["tu_op_sub"], clase="is-primary", paso=2)
            + flecha("h", paso=3)
            + nodo("description", t["existe"], t["existe_sub"], clase="ok", paso=3)
            + "</div>" + pie(t["nadie"], paso=4, icono="verified"))


def c43_nadie_mira(lang):
    t = T[lang]
    ramas = "".join(f'<div class="dg-fan-row" data-paso="{p}">{flecha("h", clase="warn")}'
                    f'{nodo(ic, a, b, clase="warn m4-h")}</div>'
                    for p, ic, a, b in [(1, "send", t["sola"], t["sola_sub"]),
                                        (2, "folder_open", t["comparte"], t["comparte_sub"]),
                                        (3, "paid", t["gasta"], t["gasta_sub"])])
    return ('<div class="dg m4-fork">'
            + nodo("timer", t["tarea"], t["tarea_sub"], clase="is-primary big")
            + f'<div class="dg-fan">{ramas}</div></div>'
            + llamada(t["nombra"], "tip", paso=4))


# ------------------------------------------------------------------------------------------
# 4.4 · Hermes en NemoClaw
# ------------------------------------------------------------------------------------------
def c44_mismo_cuarto(lang):
    t = T[lang]
    adentro = ('<div class="dg-row">'
               + nodo("assistant", "OpenClaw", t["oc_41"], clase="mini m4-off", paso=1)
               + flecha("h", t["cambias"], paso=2)
               + nodo("assistant", "Hermes", t["hermes_sub"], clase="is-primary", paso=2) + "</div>")
    grafico = ('<div class="dg-kit"><span class="dg-label"><span class="dg-i">category</span>NemoClaw</span>'
               + cuarto(t["cuarto_os"], adentro) + "</div>")
    filas = [(3, "lock", t["igual"], t["igual_sub"], "room"),
             (2, "assistant", t["cambia"], t["cambia_sub"], "is-primary"),
             (4, "edit_note", t["nuevo"], t["nuevo_sub"], "kit")]
    leyenda = "".join(f'<div class="dg-legend-row {c}" data-paso="{p}"><span class="dg-ico">{ic}</span>'
                      f'<div><b>{n}</b><small>{sub}</small></div></div>' for p, ic, n, sub, c in filas)
    return f'<div class="dg dg-pieces m4-swap">{grafico}<div class="dg-legend">{leyenda}</div></div>'


def c44_crear(lang):
    t = T[lang]
    etapas = [("pause", t["h1"], t["h1s"]), ("key", t["h2"], t["h2s"]), ("rocket_launch", t["h3"], t["h3s"]),
              ("favorite", t["h4"], t["h4s"]), ("api", t["h5"], t["h5s"])]
    pasos = "".join(f'<div class="dg-stage" data-paso="{i + 1}"><span class="dg-ico">{ic}</span>'
                    f'<b>{a}</b><small>{b}</small></div>' for i, (ic, a, b) in enumerate(etapas))
    return (f'<div class="dg dg-timeline"><div class="dg-track"></div>{pasos}</div>'
            + llamada(t["credito"], "warn", paso=6))


def c44_comparar(lang):
    t = T[lang]
    cols = [("assistant", "OpenClaw"), ("assistant", "Hermes")]
    filas = [(1, "contract", t["personalidad"], [t["oc_soul"], t["he_soul"]], ""),
             (2, "edit_note", t["memoria"], [t["oc_mem"], t["he_mem"]], ""),
             (3, "menu_book", t["skills"], [t["oc_sk"], t["he_sk"]], ""),
             (4, "forum", t["conversaciones"], [t["oc_conv"], t["he_conv"]], ""),
             (5, "api", t["puerta"], [t["oc_api"], t["he_api"]], "")]
    return matriz(cols, filas, "m4-compare") + pie(f'<span>{t["igual_dos"]}</span>', paso=6, icono="lock")


def c44_misma_skill(lang):
    t = T[lang]
    ramas = (f'<div class="dg-fan-row" data-paso="2">{flecha("h")}'
             f'{nodo("assistant", "OpenClaw", t["oc_rutas"], clase="m4-h")}</div>'
             f'<div class="dg-fan-row" data-paso="3">{flecha("h", t["dos_rutas"])}'
             f'{nodo("assistant", "Hermes", t["he_rutas"], clase="ok m4-h")}</div>')
    return ('<div class="dg m4-fork">'
            + nodo("menu_book", "soporte-nemoclaw", t["receta_43"], clase="is-primary big m4-wide", paso=1)
            + f'<div class="dg-fan">{ramas}</div></div>'
            + pie(t["resultado"], paso=4, icono="verified"))


def c44_aprobacion(lang):
    t = T[lang]
    pide = ('<div class="dg-col m4-stack">' + nodo("chat", t["recuerda"], clase="mini m4-h")
            + f'<div data-paso="2">{nodo("description", t["malicioso"], clase="mini bad m4-h")}</div></div>')
    sin = (pide + flecha("h", clase="warn")
           + nodo("edit_note", t["diario"], t["diario_sin"], clase="warn m4-h"))
    con = (nodo("chat", t["recuerda"], clase="mini m4-h")
           + flecha("h")
           + nodo("approval", t["espera"], "/memory approval on", clase="is-primary m4-h")
           + flecha("h")
           + nodo("edit_note", t["diario"], t["diario_con"], clase="ok m4-h"))
    return ('<div class="dg m4-lanes">'
            + carril(t["sin_ap"], sin, paso=1, clase="warn")
            + carril(t["con_ap"], con, paso=3, clase="ok")
            + "</div>" + pie(f'<span>{t["recetas_ap"]}</span>', paso=4, icono="approval"))


def c44_dos_capas(lang):
    t = T[lang]
    return ('<div class="dg m4-layers">'
            + nodo("code", t["programa"], t["programa_sub"], paso=1)
            + flecha("h", t["con_token"], paso=1)
            + cuarto(t["cuarto_he"], nodo("assistant", "Hermes", t["he_busca"], clase="is-primary"), paso=1)
            + f'<div class="dg-branch m4-l1" data-paso="2">{flecha("v")}'
              f'{nodo("timeline", t["capa1"], t["capa1_sub"], clase="ok mini")}</div>'
            + f'<div class="dg-branch m4-l2" data-paso="3">{flecha("v")}'
              f'{nodo("forum", t["capa2"], t["capa2_sub"], clase="mini")}</div>'
            + "</div>" + pie(t["capas"], paso=4, icono="visibility"))


def c44_avance(lang):
    t = T[lang]
    izq = carta(t["dos_agentes"], '<div class="dg-row tight">'
                + nodo("assistant", "OpenClaw", clase="mini") + nodo("assistant", "Hermes", clase="mini ok") + "</div>"
                + chips([t["a1"], t["a2"], t["a3"]]), icono="verified", clase="is-primary", paso=1)
    riesgos = "".join(nodo(ic, tx, clase="mini warn m4-h") for ic, tx in
                      [("edit_note", t["r1"]), ("menu_book", t["r2"]), ("key", t["r3"])])
    der = carta(t["mod5"], f'<div class="dg-col">{riesgos}</div>' + pie(t["riesgo"], icono="warning"),
                icono="lock", clase="m4-warn", paso=2)
    return f'<div class="dg dg-two m4-two-eq">{izq}{der}</div>'


DIAGRAMAS = {
    "c42-edificio": c42_edificio,
    "c42-escritorio": c42_escritorio,
    "c42-memoria": c42_memoria,
    "c42-planos": c42_planos,
    "c42-dice-vs-archivo": c42_dice_vs_archivo,
    "c42-dos-sesiones": c42_dos_sesiones,
    "c42-soul": c42_soul,
    "c42-tilde": c42_tilde,
    "c43-receta-alarma": c43_receta_alarma,
    "c43-controles": c43_controles,
    "c43-mecanismos": c43_mecanismos,
    "c43-anatomia": c43_anatomia,
    "c43-instalar": c43_instalar,
    "c43-explicita": c43_explicita,
    "c43-cron": c43_cron,
    "c43-prueba": c43_prueba,
    "c43-nadie-mira": c43_nadie_mira,
    "c44-mismo-cuarto": c44_mismo_cuarto,
    "c44-crear": c44_crear,
    "c44-comparar": c44_comparar,
    "c44-misma-skill": c44_misma_skill,
    "c44-aprobacion": c44_aprobacion,
    "c44-dos-capas": c44_dos_capas,
    "c44-avance": c44_avance,
}
