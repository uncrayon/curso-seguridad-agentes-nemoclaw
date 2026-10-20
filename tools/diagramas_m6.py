"""Diagramas del Módulo 6. Se usan en slides.md con ":::diagrama <nombre>".

Usa las piezas de tools/diagramas.py (nodo, flecha, cuarto, chips, pie) y las clases CSS del kit
(assets/slides.css, sección "Diagramas"). Estilos nuevos solo en assets/diagramas-m6.css
(todo lo propio va bajo la clase .c6). Cada texto visible va en T["es"] y T["en"].
"""
from diagramas import chips, cuarto, flecha, nodo, pie  # noqa: F401

T = {
    "es": {
        # ---------------------------------------------------------------- 6.1
        "pz_carpeta": "Carpeta de trabajo", "pz_carpeta_s": "lo que puede leer y escribir",
        "pz_herr": "Herramientas", "pz_herr_s": "terminal, editar, buscar",
        "pz_mem": "Memoria", "pz_mem_s": "instrucciones y sesiones guardadas",
        "pz_solo": "Tareas sin nadie", "pz_solo_s": "programadas o muy largas",
        "pz_red": "Red", "pz_red_s": "con quién puede hablar",
        "pz_cambia": "Todos repiten el mismo ciclo. Lo que cambia es qué viene abierto de fábrica.",
        "eje": "Eje", "pregunta": "La pregunta", "asistente": "En el asistente",
        "e_arch": "Archivos", "e_arch_q": "¿Qué puede escribir?", "e_arch_a": "qué cajones abre",
        "e_red": "Red", "e_red_q": "¿Con quién puede hablar?", "e_red_a": "a quién llama",
        "e_id": "Identidad", "e_id_q": "¿Como quién corre?", "e_id_a": "con qué gafete entra",
        "e_pers": "Persistencia", "e_pers_q": "¿Qué recuerda al cerrar?", "e_pers_a": "qué queda en su libreta",
        "e_sb": "Sandbox", "e_sb_q": "¿Quién lo frena si se equivoca?", "e_sb_a": "quién cuida la puerta",
        "e_aviso": "Cada libertad que le das es una puerta más para un ataque.",
        "cli_claude_s": "instrucciones en CLAUDE.md", "cli_claude_k": "el modo de permisos decide",
        "cli_codex_s": "instrucciones en AGENTS.md", "cli_codex_k": "sandbox y reglas de aprobación",
        "cli_cursor_s": "instrucciones en .cursor/rules", "cli_cursor_k": "edita solo; la terminal pregunta",
        "cli_hermes_s": "skills y memoria", "cli_hermes_k": "modo de aprobación",
        "cli_deep_s": "skills y memoria", "cli_deep_k": "aprobación de herramientas",
        "cli_oc_s": "SOUL.md y AGENTS.md", "cli_oc_k": "dentro de OpenShell",
        "cli_escritorio": "Trabajan en tu escritorio", "cli_cuarto": "En un cuarto con cerradura",
        "cli_dilo": "Di siempre: «por defecto, según su documentación, en esta versión»",
        "ag_oc_s": "el de siempre, con dashboard", "ag_hermes_s": "memoria, skills y mensajería",
        "ag_deep_s": "solo terminal; candado estricto",
        "ag_tres": "Los tres:", "ag_user": "usuario sandbox", "ag_red": "red cerrada por defecto",
        "ag_key": "la key, afuera",
        "pl_app": "Plano de la app", "pl_app_s": "el protocolo de la oficina",
        "pl_aprob": "aprobaciones", "pl_modos": "modos",
        "pl_app_pie": "Lo puede cambiar un prompt o el propio agente",
        "pl_sis": "Plano del sistema", "pl_sis_s": "la cerradura, la reja y el guardia",
        "pl_arch": "archivos", "pl_acc": "acciones", "pl_red": "red",
        "pl_sis_pie": "Solo lo cambia el operador",
        "pl_aviso": "Una aprobación en la app <b>no es un candado</b>. El CLI pone el punto de partida; OpenShell decide hasta dónde llega.",
        "lado_tu": "Afuera: tu escritorio", "lado_tu_s": "tú, el operador",
        "lado_cuarto": "Adentro: el cuarto", "lado_oc_s": "corre como usuario sandbox",
        "lado_web_s": "403: la regla dice que no",
        "lado_aviso": "¿<code>openclaw: command not found</code>? Estás afuera: OpenClaw vive adentro. Pídeselo a NemoClaw.",
        "rg_menos": "menos riesgo", "rg_mas": "más riesgo",
        "rg_1": "Programar a tu lado", "rg_1s": "CLI con aprobaciones; tú revisas",
        "rg_2": "Trabajo largo sin nadie", "rg_2s": "un CLI dentro de OpenShell",
        "rg_3": "Asistente 24/7 por chat", "rg_3s": "OpenClaw o Hermes en NemoClaw",
        "rg_4": "Tarea programada con datos", "rg_4s": "sandbox y skill revisada",
        "rg_escritorio": "en tu escritorio", "rg_cerradura": "con cerradura",
        "rg_aviso": "Si la tarea junta la trifecta letal, el agente va en un sandbox.",
        "fi_fabrica": "De fábrica", "fi_cambia": "¿Se puede cambiar?", "fi_fuente": "Fuente (enlace)",
        "fi_pie": "¿No lo encuentras en su documentación? Escribe «no documentado»: ese es tu hallazgo.",
        # ---------------------------------------------------------------- 6.2
        "sc_sin": "Sin skills", "sc_s1": "Sesión 1 · pegas las reglas", "sc_s2": "Sesión 2 · las pegas otra vez",
        "sc_s3": "Sesión 3 · salen un poco distintas", "sc_sin_pie": "Cada sesión empieza de cero",
        "sc_con": "Con skills", "sc_tarjeta": "Tarjeta de receta", "sc_tarjeta_s": "un SKILL.md, escrito una vez",
        "sc_agente": "Tu agente", "sc_agente_s": "la saca cuando la necesita",
        "sc_con_pie": "La escribes una vez, en español normal",
        "an_desc": "description: Diagnostica errores 401, 429… Úsala cuando el usuario pegue un error de la API.",
        "an_pasos": "Pasos", "an_p1": "Extrae el código del error.", "an_p2": "Usa la herramienta <code>diagnosticar_http</code>.",
        "an_p3": "Responde: qué pasó, la causa y qué hacer.",
        "an_lim": "Límites", "an_lim1": "Nunca muestres la key completa.",
        "an_etq": "La etiqueta (frontmatter)", "an_etq_s": "nombre y descripción · el agente siempre la ve",
        "an_rec": "La receta", "an_rec_s": "pasos numerados · solo si la elige",
        "an_lims": "Los límites", "an_lims_s": "lo que nunca debe hacer",
        "mn_menu": "El menú", "mn_menu_s": "siempre a la vista",
        "mn_d1": "errores de la API", "mn_d2": "leer archivos con cuidado", "mn_d3": "el resumen del día",
        "mn_d4": "dudas del curso", "mn_tok_menu": "≈350 tokens",
        "mn_pides": "pides uno", "mn_receta": "La receta completa", "mn_receta_s": "solo la que pediste",
        "mn_receta_n": "pasos y límites completos",
        "mn_pie": "Todas las recetas, siempre: ≈1,800 tokens con 4 skills y más de 20,000 con 50.",
        "sl_exp": "Explícita", "sl_exp_s": "pides el platillo por su nombre", "sl_tu": "Tú",
        "sl_receta": "La receta", "sl_exp_pie": "Tú eliges",
        "sl_auto": "Automática", "sl_auto_s": "el mesero elige por ti", "sl_pedido": "«Me sale error 401»",
        "sl_menu": "El menú", "sl_menu_s": "compara descripciones", "sl_auto_pie": "El modelo elige",
        "sl_aviso": "Que funcione la explícita <b>no prueba</b> que funcione la automática.",
        "ds_vaga": "description: Herramienta útil.", "ds_nadie": "Nadie la elige", "ds_nadie_s": "no dice cuándo usarla",
        "ds_m1": "Diagnostica errores 401, 403…", "ds_m2": "Úsala cuando el usuario pegue un error",
        "ds_m3": "o diga «el modelo no responde».", "ds_sola": "La encuentra sola", "ds_sola_s": "el pedido coincide",
        "ds_l1": "Qué hace", "ds_l2": "Cuándo usarla", "ds_l3": "Las palabras del usuario",
        "ac_vagas": "Descripciones vagas", "ac_proy": "Descripciones del proyecto", "ac_turno": "Después de «Tu turno»",
        "ac_pie": "15 pedidos, cada uno con su skill esperada · modo de prueba (MOCK)",
        "lb_biblio": "Tu biblioteca", "lb_biblio_s": "skill-library, en el repo del curso",
        "lb_inst": "Tu instancia de Brev", "lb_inst_s": "la oficina rentada",
        "lb_sandbox": "Sandbox", "lb_oc_s": "ya tiene la skill",
        "lb_pie": "Abre una sesión nueva y pruébala: por su nombre y sin nombrarla",
        "er_yaml": "La etiqueta no se lee", "er_yaml_s": "mapping values are not allowed",
        "er_yaml_ok": "Descripción entre comillas", "er_yaml_ok_s": "o quita los dos puntos",
        "er_nombre": "Nombre rechazado", "er_nombre_s": "tiene espacios u otros signos",
        "er_nombre_ok": "Solo letras, números, . - _",
        "er_sola": "Instalada, pero no la usa sola", "er_sola_ok": "Mejora la descripción",
        "er_sola_ok_s": "y abre una sesión nueva",
        "er_otra": "Elige la skill equivocada", "er_otra_ok": "Di cuándo no usarla",
        "ps_biblio": "Tu biblioteca", "ps_mala": "skill envenenada",
        "ps_sesion": "Cada sesión nueva", "ps_sesion_s": "la orden envenenada vuelve",
        "ps_1": "Revísalas como un contrato: cambios, dueño, revisión",
        "ps_2": "El texto pide; la herramienta y el sandbox imponen",
        "ps_3": "Decide quién puede escribir en <code>skills/</code>",
        # ---------------------------------------------------------------- 6.3
        "dv_brev_s": "oficina rentada por horas", "dv_brev_c": "pagas por hora",
        "dv_pc": "Tu computadora", "dv_pc_s": "la oficina en tu casa", "dv_pc_c": "16 GB · Docker",
        "dv_srv": "Servidor o DGX Spark", "dv_srv_s": "tu propio edificio, 24/7", "dv_srv_c": "tus datos no salen",
        "dv_pie": "Elige por dónde están tus datos y quién lo va a operar",
        "rq_cpu": "Procesador", "rq_cpu_s": "4 núcleos",
        "rq_ram": "Memoria", "rq_ram_s": "mínimo 8 GB · mejor 16",
        "rq_disco": "Disco", "rq_disco_s": "mínimo 20 GB · mejor 40",
        "rq_docker_s": "cajas como contenedores de barco",
        "rq_linux": "Linux", "rq_mac": "Mac con chip de Apple", "rq_win": "Windows con WSL2",
        "rq_intel": "Mac con Intel: no",
        "rq_pie": "¿Cuánta memoria tienes? Mac: «Acerca de esta Mac» · Windows: Configuración → Sistema → Información",
        "in_desc": "Descarga", "in_inst": "Instala",
        "in_mal": "Instala «lkg»", "in_mal_s": "no la versión que pediste",
        "in_bien": "Instala tu versión", "in_bien_s": "repetible, igual cada vez",
        "in_pie": "Cada lado de la barra <code>|</code> lleva su propia mochila de ajustes. La versión va con <code>bash</code>.",
        "ob_revisa": "Revisa", "ob_revisa_s": "tu máquina y la recepción",
        "ob_elige": "Elige", "ob_elige_s": "agente, modelo y llave",
        "ob_confirma": "Confirma", "ob_confirma_s": "y pon las reglas",
        "ob_1": "1 Revisión previa", "ob_2": "2 Gateway", "ob_3": "3 Agente", "ob_4": "4 Proveedor", "ob_5": "5 Key",
        "ob_6": "6 Nombre", "ob_7": "7 Revisión", "ob_8": "8 Canales", "ob_9": "9 Política",
        "ob_aviso": "En la política, deja <b>Balanced</b>. <b>Personal</b> abre casi cualquier sitio sin preguntar.",
        "pv_agente": "Tu agente", "pv_sandbox": "Sandbox", "pv_gw": "Gateway", "pv_gw_s": "la recepción",
        "pv_key": "La key se queda aquí",
        "pv_nv_s": "probado · tu key nvapi-", "pv_ollama_s": "en tu máquina · con límites",
        "pv_vllm_s": "en tu máquina · con límites", "pv_nim": "NIM local", "pv_nim_s": "experimental · GPU de NVIDIA",
        "d1": "Día 1 · usar", "d1_status": "¿está sano?", "d1_launch": "abre el dashboard", "d1_logs": "lee el registro",
        "d1_skill": "instala tus skills",
        "d2": "Día 2 · después de reiniciar", "d2_upd": "Para actualizar:",
        "d_aviso": "Nunca actualices OpenShell ni OpenClaw por fuera: NemoClaw fija sus versiones.",
        "pp_nim_s": "un mejor modelo, en tu infraestructura", "pp_ret_s": "búsqueda grande para tu FAQ",
        "pp_guard_s": "filtra lo que entra y sale", "pp_spark_s": "tu agente 24/7, modelo incluido",
        "pp_cuarto": "Sandbox · OpenShell", "pp_agente": "Tu agente", "pp_agente_s": "sigue en su cuarto",
        "pp_aviso": "Rodean al sandbox; <b>ninguna lo reemplaza</b>. Guardrails y sandbox: quieres los dos.",
        "rb_1": "Funciona", "rb_1s": "Cita la FAQ y dice «no lo sé» si no hay fuente",
        "rb_2": "Herramientas y skills", "rb_2s": "Acierta el 90 % o más, medido",
        "rb_3": "Seguridad", "rb_3s": "Un bloqueo visto en el registro; ningún secreto publicado",
        "rb_4": "Operación", "rb_4s": "Tarea programada y plan tras un reinicio",
        "rb_5": "Documentación", "rb_5s": "Explica sus decisiones y sus límites",
        "rb_crit": "Criterio", "rb_dest": "Destacado",
        "rb_pie": "Califícate con honestidad y escribe qué mejorarías primero",
        "gb_1": "1 · Guarda tu trabajo", "gb_1s": "skills, SOUL.md y notas", "gb_pc": "tu computadora",
        "gb_2": "2 · Borra la instancia", "gb_2s": "consola de Brev → Delete",
        "gb_3": "Ya no cobra nada",
        "gb_aviso": "Detenida, <b>sigue cobrando el disco</b>. Borrada, lo de adentro se pierde: por eso, primero guarda.",
        "sg_con": "Conocimiento", "sg_con_s": "mejores búsquedas, respuestas fieles",
        "sg_con_c1": "fragmentos", "sg_con_c2": "fidelidad",
        "sg_sus": "Sustrato", "sg_sus_s": "estándares que conectan agentes", "sg_trazas": "trazas",
        "sg_flo": "Flotas", "sg_flo_s": "cada agente en su cuarto",
        "sg_pie": "Este curso es la lección 6 de la ruta de IA agéntica de NVIDIA",
    },
    "en": {
        # ---------------------------------------------------------------- 6.1
        "pz_carpeta": "Working folder", "pz_carpeta_s": "what it can read and write",
        "pz_herr": "Tools", "pz_herr_s": "terminal, editing, search",
        "pz_mem": "Memory", "pz_mem_s": "instructions and saved sessions",
        "pz_solo": "Unattended tasks", "pz_solo_s": "scheduled or very long",
        "pz_red": "Network", "pz_red_s": "who it can talk to",
        "pz_cambia": "They all repeat the same cycle. What changes is what comes open out of the box.",
        "eje": "Axis", "pregunta": "The question", "asistente": "For the assistant",
        "e_arch": "Files", "e_arch_q": "What can it write?", "e_arch_a": "which drawers it opens",
        "e_red": "Network", "e_red_q": "Who can it talk to?", "e_red_a": "who it calls",
        "e_id": "Identity", "e_id_q": "Who does it run as?", "e_id_a": "which badge it wears",
        "e_pers": "Persistence", "e_pers_q": "What does it remember after closing?", "e_pers_a": "what stays in its notebook",
        "e_sb": "Sandbox", "e_sb_q": "Who stops it if it gets it wrong?", "e_sb_a": "who guards the door",
        "e_aviso": "Every freedom you give it is one more door for an attack.",
        "cli_claude_s": "instructions in CLAUDE.md", "cli_claude_k": "permission mode decides",
        "cli_codex_s": "instructions in AGENTS.md", "cli_codex_k": "sandbox and approval rules",
        "cli_cursor_s": "instructions in .cursor/rules", "cli_cursor_k": "edits freely; terminal asks",
        "cli_hermes_s": "skills and memory", "cli_hermes_k": "approval mode",
        "cli_deep_s": "skills and memory", "cli_deep_k": "tool approval",
        "cli_oc_s": "SOUL.md and AGENTS.md", "cli_oc_k": "inside OpenShell",
        "cli_escritorio": "They work at your desk", "cli_cuarto": "In a locked room",
        "cli_dilo": "Always say: “by default, per its docs, in this version”",
        "ag_oc_s": "the usual one, with a dashboard", "ag_hermes_s": "memory, skills and messaging",
        "ag_deep_s": "terminal only; strict lock",
        "ag_tres": "All three:", "ag_user": "sandbox user", "ag_red": "network closed by default",
        "ag_key": "the key stays outside",
        "pl_app": "Application plane", "pl_app_s": "the office protocol",
        "pl_aprob": "approvals", "pl_modos": "modes",
        "pl_app_pie": "A prompt or the agent itself can change it",
        "pl_sis": "System plane", "pl_sis_s": "the lock, the bars and the guard",
        "pl_arch": "files", "pl_acc": "actions", "pl_red": "network",
        "pl_sis_pie": "Only the operator changes it",
        "pl_aviso": "An in-app approval <b>isn't a lock</b>. The CLI sets the starting point; OpenShell decides how far it goes.",
        "lado_tu": "Outside: your desk", "lado_tu_s": "you, the operator",
        "lado_cuarto": "Inside: the room", "lado_oc_s": "runs as the sandbox user",
        "lado_web_s": "403: the rule says no",
        "lado_aviso": "<code>openclaw: command not found</code>? You're outside: OpenClaw lives inside. Ask NemoClaw for it.",
        "rg_menos": "less risk", "rg_mas": "more risk",
        "rg_1": "Coding by your side", "rg_1s": "CLI with approvals; you review",
        "rg_2": "Long unattended job", "rg_2s": "a CLI inside OpenShell",
        "rg_3": "24/7 chat assistant", "rg_3s": "OpenClaw or Hermes in NemoClaw",
        "rg_4": "Scheduled task with data", "rg_4s": "sandbox and a reviewed skill",
        "rg_escritorio": "at your desk", "rg_cerradura": "locked in",
        "rg_aviso": "If the task brings the lethal trifecta together, the agent goes in a sandbox.",
        "fi_fabrica": "Out of the box", "fi_cambia": "Can you change it?", "fi_fuente": "Source (link)",
        "fi_pie": "Can't find it in the docs? Write “not documented”: that's your finding.",
        # ---------------------------------------------------------------- 6.2
        "sc_sin": "Without skills", "sc_s1": "Session 1 · you paste the rules", "sc_s2": "Session 2 · you paste them again",
        "sc_s3": "Session 3 · they come out a bit different", "sc_sin_pie": "Every session starts from scratch",
        "sc_con": "With skills", "sc_tarjeta": "Recipe card", "sc_tarjeta_s": "a SKILL.md, written once",
        "sc_agente": "Your agent", "sc_agente_s": "pulls it out when needed",
        "sc_con_pie": "You write it once, in plain language",
        "an_desc": "description: Diagnoses 401, 429… errors. Use it when the user pastes an API error.",
        "an_pasos": "Steps", "an_p1": "Pull out the error code.", "an_p2": "Use the <code>diagnosticar_http</code> tool.",
        "an_p3": "Answer: what happened, the cause, what to do.",
        "an_lim": "Limits", "an_lim1": "Never show the full key.",
        "an_etq": "The label (frontmatter)", "an_etq_s": "name and description · the agent always sees it",
        "an_rec": "The recipe", "an_rec_s": "numbered steps · only if it picks it",
        "an_lims": "The limits", "an_lims_s": "what it must never do",
        "mn_menu": "The menu", "mn_menu_s": "always in view",
        "mn_d1": "API errors", "mn_d2": "read files carefully", "mn_d3": "the daily summary",
        "mn_d4": "course questions", "mn_tok_menu": "≈350 tokens",
        "mn_pides": "you order one", "mn_receta": "The full recipe", "mn_receta_s": "only the one you ordered",
        "mn_receta_n": "full steps and limits",
        "mn_pie": "Every recipe, all the time: ≈1,800 tokens with 4 skills and over 20,000 with 50.",
        "sl_exp": "Explicit", "sl_exp_s": "you order the dish by name", "sl_tu": "You",
        "sl_receta": "The recipe", "sl_exp_pie": "You pick",
        "sl_auto": "Automatic", "sl_auto_s": "the waiter picks for you", "sl_pedido": "“I get a 401 error”",
        "sl_menu": "The menu", "sl_menu_s": "compares descriptions", "sl_auto_pie": "The model picks",
        "sl_aviso": "Explicit working <b>doesn't prove</b> automatic works.",
        "ds_vaga": "description: Useful tool.", "ds_nadie": "Nobody picks it", "ds_nadie_s": "doesn't say when to use it",
        "ds_m1": "Diagnoses 401, 403… errors.", "ds_m2": "Use it when the user pastes an error",
        "ds_m3": "or says “the model isn't responding”.", "ds_sola": "Found on its own", "ds_sola_s": "the request matches",
        "ds_l1": "What it does", "ds_l2": "When to use it", "ds_l3": "The user's words",
        "ac_vagas": "Vague descriptions", "ac_proy": "Project descriptions", "ac_turno": "After “Your turn”",
        "ac_pie": "15 requests, each with its expected skill · test mode (MOCK)",
        "lb_biblio": "Your library", "lb_biblio_s": "skill-library, in the course repo",
        "lb_inst": "Your Brev instance", "lb_inst_s": "the rented office",
        "lb_sandbox": "Sandbox", "lb_oc_s": "now has the skill",
        "lb_pie": "Open a new session and try it: by name and without naming it",
        "er_yaml": "The label can't be read", "er_yaml_s": "mapping values are not allowed",
        "er_yaml_ok": "Quote the description", "er_yaml_ok_s": "or drop the colon",
        "er_nombre": "Name rejected", "er_nombre_s": "has spaces or other symbols",
        "er_nombre_ok": "Only letters, numbers, . - _",
        "er_sola": "Installed, but never used alone", "er_sola_ok": "Improve the description",
        "er_sola_ok_s": "and open a new session",
        "er_otra": "Picks the wrong skill", "er_otra_ok": "Say when not to use it",
        "ps_biblio": "Your library", "ps_mala": "poisoned skill",
        "ps_sesion": "Every new session", "ps_sesion_s": "the poisoned order comes back",
        "ps_1": "Review them like a contract: changes, owner, review",
        "ps_2": "The text asks; the tool and the sandbox enforce",
        "ps_3": "Decide who can write to <code>skills/</code>",
        # ---------------------------------------------------------------- 6.3
        "dv_brev_s": "an office rented by the hour", "dv_brev_c": "pay per hour",
        "dv_pc": "Your computer", "dv_pc_s": "the office at home", "dv_pc_c": "16 GB · Docker",
        "dv_srv": "Server or DGX Spark", "dv_srv_s": "your own building, 24/7", "dv_srv_c": "your data stays put",
        "dv_pie": "Choose by where your data is and who will run it",
        "rq_cpu": "Processor", "rq_cpu_s": "4 cores",
        "rq_ram": "Memory", "rq_ram_s": "at least 8 GB · 16 is better",
        "rq_disco": "Disk", "rq_disco_s": "at least 20 GB · 40 is better",
        "rq_docker_s": "boxes like shipping containers",
        "rq_linux": "Linux", "rq_mac": "Mac with Apple chip", "rq_win": "Windows with WSL2",
        "rq_intel": "Intel Mac: no",
        "rq_pie": "How much memory do you have? Mac: “About This Mac” · Windows: Settings → System → About",
        "in_desc": "Downloads", "in_inst": "Installs",
        "in_mal": "Installs “lkg”", "in_mal_s": "not the version you asked for",
        "in_bien": "Installs your version", "in_bien_s": "repeatable, the same every time",
        "in_pie": "Each side of the <code>|</code> bar carries its own backpack of settings. The version goes with <code>bash</code>.",
        "ob_revisa": "Check", "ob_revisa_s": "your machine and the front desk",
        "ob_elige": "Choose", "ob_elige_s": "agent, model and key",
        "ob_confirma": "Confirm", "ob_confirma_s": "and set the rules",
        "ob_1": "1 Preflight", "ob_2": "2 Gateway", "ob_3": "3 Agent", "ob_4": "4 Provider", "ob_5": "5 Key",
        "ob_6": "6 Name", "ob_7": "7 Review", "ob_8": "8 Channels", "ob_9": "9 Policy",
        "ob_aviso": "For the policy, keep <b>Balanced</b>. <b>Personal</b> opens almost any site without asking.",
        "pv_agente": "Your agent", "pv_sandbox": "Sandbox", "pv_gw": "Gateway", "pv_gw_s": "the front desk",
        "pv_key": "The key stays here",
        "pv_nv_s": "tested · your nvapi- key", "pv_ollama_s": "on your machine · with limits",
        "pv_vllm_s": "on your machine · with limits", "pv_nim": "Local NIM", "pv_nim_s": "experimental · NVIDIA GPU",
        "d1": "Day 1 · use it", "d1_status": "is it healthy?", "d1_launch": "opens the dashboard", "d1_logs": "reads the log",
        "d1_skill": "installs your skills",
        "d2": "Day 2 · after a restart", "d2_upd": "To update:",
        "d_aviso": "Never update OpenShell or OpenClaw on the side: NemoClaw pins their versions.",
        "pp_nim_s": "a better model, on your infrastructure", "pp_ret_s": "big search for your FAQ",
        "pp_guard_s": "filters what goes in and out", "pp_spark_s": "your 24/7 agent, model included",
        "pp_cuarto": "Sandbox · OpenShell", "pp_agente": "Your agent", "pp_agente_s": "still in its room",
        "pp_aviso": "They surround the sandbox; <b>none replaces it</b>. Guardrails and sandbox: you want both.",
        "rb_1": "Works", "rb_1s": "Cites the FAQ and says “I don't know” without a source",
        "rb_2": "Tools and skills", "rb_2s": "Hits 90 % or more, measured",
        "rb_3": "Security", "rb_3s": "A block seen in the log; no secret published",
        "rb_4": "Operations", "rb_4s": "Scheduled task and a plan after a restart",
        "rb_5": "Documentation", "rb_5s": "Explains its decisions and its limits",
        "rb_crit": "Criterion", "rb_dest": "Outstanding",
        "rb_pie": "Grade yourself honestly and write what you'd improve first",
        "gb_1": "1 · Save your work", "gb_1s": "skills, SOUL.md and notes", "gb_pc": "your computer",
        "gb_2": "2 · Delete the instance", "gb_2s": "Brev console → Delete",
        "gb_3": "Nothing billed anymore",
        "gb_aviso": "Stopped, <b>the disk keeps billing</b>. Deleted, what's inside is lost: so save first.",
        "sg_con": "Knowledge", "sg_con_s": "better search, faithful answers",
        "sg_con_c1": "chunking", "sg_con_c2": "faithfulness",
        "sg_sus": "Substrate", "sg_sus_s": "standards that connect agents", "sg_trazas": "traces",
        "sg_flo": "Fleets", "sg_flo_s": "each agent in its room",
        "sg_pie": "This course is lesson 6 of NVIDIA's agentic AI learning path",
    },
}


def _i(icono):
    return f'<span class="dg-i">{icono}</span>'


def _call(clase, texto, paso):
    return f'<div class="call {clase}" data-paso="{paso}"><p>{texto}</p></div>'


def _fila(paso, icono, *celdas, clase=""):
    tds = "".join(f"<span>{c}</span>" for c in celdas)
    return f'<div class="c6-fila {clase}" data-paso="{paso}"><span class="dg-ico">{icono}</span>{tds}</div>'


def _cabecera(*celdas):
    return '<div class="c6-fila c6-cab"><span></span>' + "".join(f"<span>{c}</span>" for c in celdas) + "</div>"


# ======================================================================================== 6.1
def c61_cinco_piezas(lang):
    t = T[lang]
    piezas = [("folder_open", "pz_carpeta"), ("settings", "pz_herr"), ("edit_note", "pz_mem"),
              ("schedule", "pz_solo"), ("public", "pz_red")]
    fila = "".join(nodo(ic, t[k], t[k + "_s"], paso=i) for i, (ic, k) in enumerate(piezas, 1))
    return f'<div class="dg c6 dg-row">{fila}</div>' + pie(t["pz_cambia"], paso=6, icono="tune")


EJES = [("folder_open", "e_arch"), ("public", "e_red"), ("badge", "e_id"), ("edit_note", "e_pers"), ("lock", "e_sb")]


def c61_cinco_preguntas(lang):
    t = T[lang]
    filas = "".join(_fila(i, ic, f"<b>{t[k]}</b>", t[k + "_q"], f"<em>{t[k + '_a']}</em>")
                    for i, (ic, k) in enumerate(EJES, 1))
    return (f'<div class="dg c6"><div class="c6-ficha">{_cabecera(t["eje"], t["pregunta"], t["asistente"])}{filas}</div></div>'
            + _call("warn", t["e_aviso"], 6))


def c61_asistentes(lang):
    t = T[lang]

    def tarjeta(ic, nombre, k, paso, clase=""):
        llave = f'<span class="c6-llave">{_i("key")}{t[k + "_k"]}</span>'
        return nodo(ic, nombre, t[k + "_s"], clase=clase, paso=paso, extra=llave)
    escritorio = (tarjeta("terminal", "Claude Code", "cli_claude", 1) + tarjeta("code", "Codex CLI", "cli_codex", 1)
                  + tarjeta("edit", "Cursor", "cli_cursor", 1) + tarjeta("book", "Hermes", "cli_hermes", 2)
                  + tarjeta("stack", "Deep Agents", "cli_deep", 2))
    oc = tarjeta("assistant", "OpenClaw", "cli_oc", 3, clase="is-primary")
    return ('<div class="dg c6 c6-cli">'
            + f'<div class="c6-grupo"><span class="c6-grupo-t">{_i("person")}{t["cli_escritorio"]}</span>'
            + f'<div class="c6-grid5">{escritorio}</div></div>'
            + cuarto(t["cli_cuarto"], oc, paso=3)
            + "</div>" + pie(t["cli_dilo"], paso=4, icono="record_voice_over"))


def c61_tres_agentes(lang):
    t = T[lang]

    def cmd(c):
        return f'<span class="c6-cmd">{c}</span>'
    fila = (nodo("assistant", "OpenClaw", t["ag_oc_s"], clase="is-primary", paso=1, extra=cmd("nemoclaw"))
            + nodo("book", "Hermes", t["ag_hermes_s"], paso=2, extra=cmd("nemohermes"))
            + nodo("stack", "Deep Agents", t["ag_deep_s"], paso=3, extra=cmd("nemo-deepagents")))
    kit = ('<div class="dg-kit"><span class="dg-label"><span class="dg-i">category</span>NemoClaw</span>'
           + cuarto("OpenShell", f'<div class="dg-row">{fila}</div>') + "</div>")
    comun = (f'<div class="c6-comun" data-paso="4"><b>{t["ag_tres"]}</b>'
             + chips([_i("badge") + t["ag_user"], _i("block") + t["ag_red"], _i("key") + t["ag_key"]]) + "</div>")
    return f'<div class="dg c6 c6-centro">{kit}{comun}</div>'


def c61_dos_planos(lang):
    t = T[lang]
    app = (f'<div class="dg-card" data-paso="1"><h3>{_i("description")}{t["pl_app"]}</h3>'
           f'<small class="dg-card-sub">{t["pl_app_s"]}</small>'
           + chips(["CLAUDE.md", "AGENTS.md", t["pl_aprob"], t["pl_modos"]])
           + pie(t["pl_app_pie"], icono="edit") + "</div>")
    sis = (f'<div class="dg-card is-primary" data-paso="2"><h3>{_i("lock")}{t["pl_sis"]}</h3>'
           f'<small class="dg-card-sub">{t["pl_sis_s"]}</small>'
           + chips([_i("folder_open") + t["pl_arch"], _i("bolt") + t["pl_acc"], _i("public") + t["pl_red"]])
           + pie(t["pl_sis_pie"], icono="key") + "</div>")
    return f'<div class="dg c6 c6-mitades">{app}{sis}</div>' + _call("warn", t["pl_aviso"], 3)


def c61_de_que_lado(lang):
    t = T[lang]
    return ('<div class="dg c6 dg-row">'
            + nodo("person", t["lado_tu"], t["lado_tu_s"], paso=1, extra='<span class="c6-cmd">id → ubuntu</span>')
            + flecha("h", "nemoclaw … exec", paso=2)
            + cuarto(t["lado_cuarto"], nodo("assistant", "OpenClaw", t["lado_oc_s"], clase="is-primary",
                                            extra='<span class="c6-cmd">id → sandbox</span>'), paso=2)
            + flecha("h", clase="bad", paso=3)
            + nodo("public", "example.com", t["lado_web_s"], clase="bad", paso=3)
            + "</div>" + _call("tip", t["lado_aviso"], 4))


def c61_elegir(lang):
    t = T[lang]

    def marca(icono, k):
        return f'<span class="c6-marca">{_i(icono)}{t[k]}</span>'
    nodos = (nodo("person", t["rg_1"], t["rg_1s"], paso=1, extra=marca("computer", "rg_escritorio"))
             + nodo("schedule", t["rg_2"], t["rg_2s"], clase="ok", paso=2, extra=marca("lock", "rg_cerradura"))
             + nodo("forum", t["rg_3"], t["rg_3s"], clase="ok", paso=3, extra=marca("lock", "rg_cerradura"))
             + nodo("event", t["rg_4"], t["rg_4s"], clase="ok", paso=4, extra=marca("lock", "rg_cerradura")))
    barra = (f'<div class="c6-riesgo"><span>{t["rg_menos"]}</span><i></i><span>{t["rg_mas"]}</span></div>')
    return (f'<div class="dg c6 c6-pila">{barra}<div class="c6-grid4">{nodos}</div></div>'
            + _call("tip", t["rg_aviso"], 5))


def c61_ficha(lang):
    t = T[lang]
    vacio = '<i class="c6-hueco"></i>'
    filas = "".join(_fila(1, ic, f"<b>{t[k]}</b>", vacio, vacio, vacio) for ic, k in EJES)
    return (f'<div class="dg c6"><div class="c6-ficha c6-vacia">'
            f'{_cabecera(t["eje"], t["fi_fabrica"], t["fi_cambia"], t["fi_fuente"])}{filas}</div></div>'
            + pie(t["fi_pie"], paso=2, icono="search"))


# ======================================================================================== 6.2
def c62_sin_con(lang):
    t = T[lang]
    sin = (f'<div class="dg-card" data-paso="1"><h3>{_i("content_copy")}{t["sc_sin"]}</h3><div class="c6-sesiones">'
           f'<span class="dg-chip">{_i("chat")}{t["sc_s1"]}</span>'
           f'<span class="dg-chip">{_i("chat")}{t["sc_s2"]}</span>'
           f'<span class="dg-chip c6-chip-warn">{_i("chat")}{t["sc_s3"]}</span></div>'
           + pie(t["sc_sin_pie"], icono="replay") + "</div>")
    con = (f'<div class="dg-card is-primary" data-paso="2"><h3>{_i("menu_book")}{t["sc_con"]}</h3><div class="dg-row tight">'
           + nodo("menu_book", t["sc_tarjeta"], t["sc_tarjeta_s"], clase="mini")
           + flecha("h")
           + nodo("assistant", t["sc_agente"], t["sc_agente_s"], clase="is-primary mini")
           + "</div>" + pie(t["sc_con_pie"], icono="edit_note") + "</div>")
    return f'<div class="dg c6 c6-mitades">{sin}{con}</div>'


def _receta_html(t):
    return ('<div class="c6-receta">'
            '<span class="c6-ruta">skill-library/diagnostico-api/SKILL.md</span>'
            '<div class="c6-etiqueta" data-paso="1"><span class="c6-tab">frontmatter</span>'
            f'<code>name: diagnostico-api</code><code>{t["an_desc"]}</code></div>'
            f'<div class="c6-cuerpo" data-paso="2"><b>{t["an_pasos"]}</b><ol>'
            f'<li>{t["an_p1"]}</li><li>{t["an_p2"]}</li><li>{t["an_p3"]}</li></ol></div>'
            f'<div class="c6-limites" data-paso="3"><b>{t["an_lim"]}</b><p>{t["an_lim1"]}</p></div>'
            "</div>")


def c62_tarjeta(lang):
    t = T[lang]
    filas = [(1, "label", t["an_etq"], t["an_etq_s"], "is-primary"), (2, "list", t["an_rec"], t["an_rec_s"], "room"),
             (3, "block", t["an_lims"], t["an_lims_s"], "kit")]
    leyenda = "".join(f'<div class="dg-legend-row {c}" data-paso="{p}"><span class="dg-ico">{ic}</span>'
                      f'<div><b>{n}</b><small>{s}</small></div></div>' for p, ic, n, s, c in filas)
    return f'<div class="dg c6 c6-anatomia">{_receta_html(t)}<div class="dg-legend">{leyenda}</div></div>'


def c62_menu(lang):
    t = T[lang]
    platos = [("diagnostico-api", "mn_d1"), ("lector-seguro-archivos", "mn_d2"), ("resumen-diario", "mn_d3"),
              ("soporte-nemoclaw", "mn_d4")]
    lista = "".join(f'<li><code>{n}</code><small>{t[k]}</small></li>' for n, k in platos)
    menu = (f'<div class="dg-card c6-carta" data-paso="1"><h3>{_i("menu_book")}{t["mn_menu"]}</h3>'
            f'<small class="dg-card-sub">{t["mn_menu_s"]}</small><ul>{lista}</ul>'
            + chips([t["mn_tok_menu"]]) + "</div>")
    receta = (f'<div class="dg-card is-primary" data-paso="2"><h3>{_i("description")}{t["mn_receta"]}</h3>'
              f'<small class="dg-card-sub">{t["mn_receta_s"]}</small>'
              + nodo("description", "diagnostico-api", t["mn_receta_n"], clase="is-primary mini") + "</div>")
    return (f'<div class="dg c6 dg-row">{menu}{flecha("h", t["mn_pides"], paso=2)}{receta}</div>'
            + pie(t["mn_pie"], paso=3, icono="paid"))


def c62_dos_selecciones(lang):
    t = T[lang]
    exp = (f'<div class="dg-card" data-paso="1"><h3>{_i("person")}{t["sl_exp"]}</h3>'
           f'<small class="dg-card-sub">{t["sl_exp_s"]}</small><div class="dg-row tight c6-nowrap">'
           + nodo("person", t["sl_tu"], '<code>/diagnostico-api …</code>', clase="mini")
           + flecha("h")
           + nodo("description", t["sl_receta"], clase="ok mini")
           + "</div>" + pie(t["sl_exp_pie"], icono="person") + "</div>")
    auto = (f'<div class="dg-card is-primary" data-paso="2"><h3>{_i("auto_awesome")}{t["sl_auto"]}</h3>'
            f'<small class="dg-card-sub">{t["sl_auto_s"]}</small><div class="dg-row tight c6-nowrap">'
            + nodo("chat", t["sl_pedido"], clase="mini")
            + flecha("h")
            + nodo("menu_book", t["sl_menu"], t["sl_menu_s"], clase="mini")
            + flecha("h")
            + nodo("description", t["sl_receta"], clase="ok mini")
            + "</div>" + pie(t["sl_auto_pie"], icono="auto_awesome") + "</div>")
    return f'<div class="dg c6 c6-sel">{exp}{auto}</div>' + _call("warn", t["sl_aviso"], 3)


def c62_disparador(lang):
    t = T[lang]
    vaga = (f'<div class="c6-desc">{_i("label")}<code>{t["ds_vaga"]}</code></div>')
    util = (f'<div class="c6-desc">{_i("label")}<code>description: '
            f'<mark class="c6-m1">{t["ds_m1"]}</mark> <mark class="c6-m2">{t["ds_m2"]}</mark> '
            f'<mark class="c6-m3">{t["ds_m3"]}</mark></code></div>')
    fila1 = (f'<div class="dg-row c6-izq" data-paso="1">{vaga}{flecha("h", clase="bad")}'
             + nodo("search", t["ds_nadie"], t["ds_nadie_s"], clase="bad mini") + "</div>")
    fila2 = (f'<div class="dg-row c6-izq" data-paso="2">{util}{flecha("h")}'
             + nodo("check_circle", t["ds_sola"], t["ds_sola_s"], clase="ok mini") + "</div>")
    leyenda = (f'<div class="c6-claves" data-paso="3"><span class="c6-m1">{t["ds_l1"]}</span>+'
               f'<span class="c6-m2">{t["ds_l2"]}</span>+<span class="c6-m3">{t["ds_l3"]}</span></div>')
    return f'<div class="dg c6 c6-pila">{fila1}{fila2}{leyenda}</div>'


def c62_acierto(lang):
    t = T[lang]
    barras = [(1, t["ac_vagas"], 13, "13 %", "bad"), (2, t["ac_proy"], 80, "80 %", ""), (3, t["ac_turno"], 90, "≥ 90 %", "ok")]
    filas = "".join(f'<div class="c6-barra {c}" data-paso="{p}"><span class="c6-barra-t">{n}</span>'
                    f'<span class="c6-barra-v"><i style="width:{w}%"></i></span><b>{v}</b></div>'
                    for p, n, w, v, c in barras)
    return f'<div class="dg c6"><div class="c6-barras">{filas}</div></div>' + pie(t["ac_pie"], paso=3, icono="quiz")


def c62_al_lab(lang):
    t = T[lang]
    return ('<div class="dg c6 dg-row">'
            + nodo("folder_open", t["lb_biblio"], t["lb_biblio_s"], paso=1)
            + flecha("h", "git clone", paso=2)
            + nodo("computer", t["lb_inst"], t["lb_inst_s"], paso=2)
            + flecha("h", "skill install", paso=3)
            + cuarto(t["lb_sandbox"], nodo("assistant", "OpenClaw", t["lb_oc_s"], clase="is-primary",
                                           extra=chips([_i("menu_book") + "diagnostico-api"])), paso=3)
            + "</div>" + pie(t["lb_pie"], paso=4, icono="chat"))


def _par(paso, mal, mal_s, bien, bien_s="", clase="bad"):
    return (f'<div class="c6-par" data-paso="{paso}">' + nodo("error", mal, mal_s, clase=f"{clase} mini")
            + flecha("h") + nodo("check_circle", bien, bien_s, clase="ok mini") + "</div>")


def c62_errores(lang):
    t = T[lang]
    return ('<div class="dg c6 c6-pares">'
            + _par(1, t["er_yaml"], f'<code>{t["er_yaml_s"]}</code>', t["er_yaml_ok"], t["er_yaml_ok_s"])
            + _par(2, t["er_nombre"], t["er_nombre_s"], t["er_nombre_ok"])
            + _par(3, t["er_sola"], "", t["er_sola_ok"], t["er_sola_ok_s"], clase="warn")
            + _par(4, t["er_otra"], "", t["er_otra_ok"], clase="warn")
            + "</div>")


def c62_persistencia(lang):
    t = T[lang]
    biblio = (f'<div class="dg-card c6-biblio" data-paso="1"><h3>{_i("menu_book")}{t["ps_biblio"]}</h3>'
              '<div class="c6-estante">'
              + "".join(f'<span class="dg-chip">{_i("description")}{n}</span>'
                        for n in ("diagnostico-api", "resumen-diario", "soporte-nemoclaw"))
              + f'<span class="dg-chip c6-chip-bad">{_i("warning")}{t["ps_mala"]}</span></div></div>')
    fila = (f'<div class="dg-row">{biblio}{flecha("h", clase="warn", paso=2)}'
            + nodo("replay", t["ps_sesion"], t["ps_sesion_s"], clase="warn", paso=2) + "</div>")
    pies = ('<div class="c6-tres">' + pie(t["ps_1"], paso=3, icono="contract") + pie(t["ps_2"], paso=4, icono="lock")
            + pie(t["ps_3"], paso=5, icono="key") + "</div>")
    return f'<div class="dg c6 c6-pila">{fila}{pies}</div>'


# ======================================================================================== 6.3
def c63_tres_caminos(lang):
    t = T[lang]
    return ('<div class="dg c6 dg-row">'
            + nodo("business", "Brev", t["dv_brev_s"], clase="ok", paso=1, extra=chips([t["dv_brev_c"]]))
            + flecha("h", paso=2)
            + nodo("home", t["dv_pc"], t["dv_pc_s"], paso=2, extra=chips([t["dv_pc_c"]]))
            + flecha("h", paso=3)
            + nodo("storage", t["dv_srv"], t["dv_srv_s"], paso=3, extra=chips([t["dv_srv_c"]]))
            + "</div>" + pie(t["dv_pie"], paso=4, icono="route"))


def c63_requisitos(lang):
    t = T[lang]
    fila = (nodo("bolt", t["rq_cpu"], t["rq_cpu_s"], paso=1)
            + nodo("speed", t["rq_ram"], t["rq_ram_s"], clase="is-primary", paso=1)
            + nodo("storage", t["rq_disco"], t["rq_disco_s"], paso=1)
            + nodo("box", "Docker", t["rq_docker_s"], paso=1, extra=chips(["+ Node 22.19+"])))
    sistemas = (f'<div class="dg-chips c6-sistemas" data-paso="2">'
                + "".join(f'<span class="dg-chip">{_i("check_circle")}{x}</span>'
                          for x in (t["rq_linux"], t["rq_mac"], t["rq_win"], "DGX Spark"))
                + f'<span class="dg-chip c6-chip-bad">{_i("block")}{t["rq_intel"]}</span></div>')
    return f'<div class="dg c6 c6-pila"><div class="dg-row">{fila}</div>{sistemas}</div>' + pie(t["rq_pie"], paso=3, icono="search")


def c63_instalar(lang):
    t = T[lang]

    def fila(paso, tag_clase, fin):
        tag = f'<span class="c6-cmd {tag_clase}">TAG=vX.Y.Z</span>'
        izq = tag if tag_clase == "mal" else ""
        der = tag if tag_clase == "bien" else ""
        return (f'<div class="dg-row" data-paso="{paso}">'
                + nodo("download", "curl", t["in_desc"], clase="mini", extra=izq)
                + flecha("h", "|")
                + nodo("terminal", "bash", t["in_inst"], clase="mini", extra=der)
                + flecha("h", clase="bad" if tag_clase == "mal" else "")
                + fin + "</div>")
    return ('<div class="dg c6 c6-pila">'
            + fila(1, "mal", nodo("cancel", t["in_mal"], t["in_mal_s"], clase="bad mini"))
            + fila(2, "bien", nodo("check_circle", t["in_bien"], t["in_bien_s"], clase="ok mini"))
            + "</div>" + pie(t["in_pie"], paso=3, icono="info"))


def c63_onboarding(lang):
    t = T[lang]
    fases = [(1, "search", "ob_revisa", ["ob_1", "ob_2"]), (2, "tune", "ob_elige", ["ob_3", "ob_4", "ob_5", "ob_6"]),
             (3, "check_circle", "ob_confirma", ["ob_7", "ob_8", "ob_9"])]
    fila = ""
    for paso, ic, k, subs in fases:
        if paso > 1:
            fila += flecha("h", paso=paso)
        fila += nodo(ic, t[k], t[k + "_s"], paso=paso, clase="c6-fase", extra=chips([t[s] for s in subs]))
    return f'<div class="dg c6 dg-row">{fila}</div>' + _call("warn", t["ob_aviso"], 4)


def c63_proveedores(lang):
    t = T[lang]
    filas = [(3, "auto_awesome", "NVIDIA Endpoints", t["pv_nv_s"], "ok"), (4, "computer", "Ollama", t["pv_ollama_s"], "warn"),
             (4, "computer", "vLLM", t["pv_vllm_s"], "warn"), (4, "box", t["pv_nim"], t["pv_nim_s"], "warn")]
    fan = "".join(f'<div class="dg-fan-row" data-paso="{p}">{flecha("h")}{nodo(ic, n, s, clase=c + " mini c6-ancho")}</div>'
                  for p, ic, n, s, c in filas)
    gw = nodo("domain", t["pv_gw"], t["pv_gw_s"], paso=2,
              extra=f'<span class="c6-llave">{_i("key")}{t["pv_key"]}</span>')
    return ('<div class="dg c6 dg-star">'
            + cuarto(t["pv_sandbox"], nodo("assistant", t["pv_agente"], clase="is-primary mini"), paso=1)
            + flecha("h", paso=2) + gw + f'<div class="dg-fan">{fan}</div></div>')


def c63_dias(lang):
    t = T[lang]
    cmds = [("status", "d1_status"), ("launch", "d1_launch"), ("logs", "d1_logs"), ("skill install", "d1_skill")]
    lista = "".join(f'<li><code>{c}</code><span>{t[k]}</span></li>' for c, k in cmds)
    d1 = (f'<div class="dg-card" data-paso="1"><h3>{_i("today")}{t["d1"]}</h3><ul class="c6-cmds">{lista}</ul></div>')
    pasos = ""
    for i, c in enumerate(("status", "start", "recover")):
        if i:
            pasos += flecha("h")
        pasos += nodo(["favorite", "play_arrow", "restore"][i], c, clase="mini")
    d2 = (f'<div class="dg-card is-primary" data-paso="2"><h3>{_i("refresh")}{t["d2"]}</h3>'
          f'<div class="dg-row tight c6-nowrap">{pasos}</div>'
          + f'<div class="c6-upd">{_i("update")}<span>{t["d2_upd"]}</span><code>backup-all</code>→<code>update</code>'
            '→<code>upgrade-sandboxes</code></div>'
          + "</div>")
    return f'<div class="dg c6 c6-mitades">{d1}{d2}</div>' + _call("bad", t["d_aviso"], 3)


def c63_piezas(lang):
    t = T[lang]
    centro = cuarto(t["pp_cuarto"], nodo("assistant", t["pp_agente"], t["pp_agente_s"], clase="is-primary big"),
                    clase="c6-centro-cuarto")
    return ('<div class="dg c6 c6-orbita">'
            + nodo("box", "NIM", t["pp_nim_s"], paso=1, clase="c6-o1")
            + nodo("search", "NeMo Retriever", t["pp_ret_s"], paso=2, clase="c6-o2")
            + centro
            + nodo("filter_list", "NeMo Guardrails", t["pp_guard_s"], paso=3, clase="c6-o3")
            + nodo("computer", "DGX Spark", t["pp_spark_s"], paso=4, clase="c6-o4")
            + "</div>" + _call("tip", t["pp_aviso"], 5))


def c63_rubrica(lang):
    t = T[lang]
    filas = "".join(_fila(i, "check_circle", f'<b>{t[f"rb_{i}"]}</b>', t[f"rb_{i}s"]) for i in range(1, 6))
    return (f'<div class="dg c6"><div class="c6-ficha c6-rubrica">{_cabecera(t["rb_crit"], t["rb_dest"])}{filas}</div></div>'
            + pie(t["rb_pie"], paso=6, icono="emoji_events"))


def c63_guarda_borra(lang):
    t = T[lang]
    return ('<div class="dg c6 dg-row">'
            + nodo("save", t["gb_1"], t["gb_1s"], paso=1, extra=chips([t["gb_pc"], "GitHub"]))
            + flecha("h", paso=2)
            + nodo("delete", t["gb_2"], t["gb_2s"], clase="is-primary", paso=2)
            + flecha("h", paso=3)
            + nodo("check_circle", t["gb_3"], clase="ok", paso=3)
            + "</div>" + _call("warn", t["gb_aviso"], 4))


def c63_seguir(lang):
    t = T[lang]
    cuartos = '<span class="c6-mini-cuartos">' + _i("lock") * 3 + "</span>"
    return ('<div class="dg c6 dg-row c6-seguir">'
            + nodo("menu_book", t["sg_con"], t["sg_con_s"], paso=1, extra=chips([t["sg_con_c1"], t["sg_con_c2"]]))
            + nodo("conversion_path", t["sg_sus"], t["sg_sus_s"], paso=2, extra=chips(["MCP", "A2A", t["sg_trazas"]]))
            + nodo("groups", t["sg_flo"], t["sg_flo_s"], paso=3, extra=cuartos)
            + "</div>" + pie(t["sg_pie"], paso=4, icono="school"))


DIAGRAMAS = {
    "c61-cinco-piezas": c61_cinco_piezas,
    "c61-cinco-preguntas": c61_cinco_preguntas,
    "c61-asistentes": c61_asistentes,
    "c61-tres-agentes": c61_tres_agentes,
    "c61-dos-planos": c61_dos_planos,
    "c61-de-que-lado": c61_de_que_lado,
    "c61-elegir": c61_elegir,
    "c61-ficha": c61_ficha,
    "c62-sin-con": c62_sin_con,
    "c62-tarjeta": c62_tarjeta,
    "c62-menu": c62_menu,
    "c62-dos-selecciones": c62_dos_selecciones,
    "c62-disparador": c62_disparador,
    "c62-acierto": c62_acierto,
    "c62-al-lab": c62_al_lab,
    "c62-errores": c62_errores,
    "c62-persistencia": c62_persistencia,
    "c63-tres-caminos": c63_tres_caminos,
    "c63-requisitos": c63_requisitos,
    "c63-instalar": c63_instalar,
    "c63-onboarding": c63_onboarding,
    "c63-proveedores": c63_proveedores,
    "c63-dias": c63_dias,
    "c63-piezas": c63_piezas,
    "c63-rubrica": c63_rubrica,
    "c63-guarda-borra": c63_guarda_borra,
    "c63-seguir": c63_seguir,
}
