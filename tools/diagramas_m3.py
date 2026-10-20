"""Diagramas del Módulo 3. Se usan en slides.md con ":::diagrama <nombre>".

Usa las piezas de tools/diagramas.py (nodo, flecha, cuarto, chips, pie) y las clases CSS del kit
(assets/slides.css, sección "Diagramas"). Estilos nuevos solo en assets/diagramas-m3.css (prefijo c3-).
Cada texto visible va en T["es"] y T["en"].
"""
from diagramas import chips, cuarto, flecha, nodo, pie  # noqa: F401

# ------------------------------------------------------------------------------------------
# Textos por idioma
# ------------------------------------------------------------------------------------------
T = {
    "es": {
        # comunes
        "modelo": "Modelo", "llamada": "1 llamada", "avance": "Soporte NemoClaw",
        # 3.1 · loop vs flujo
        "c31_ticket": "«Me sale 401 en el laboratorio después de reanudar Brev»",
        "c31_loop": "Loop: el modelo decide", "c31_loop_pie": "Ideal si el paso 2 depende del 1",
        "c31_paso1": "Paso 1", "c31_paso1_sub": "mira el resultado", "c31_ahora": "¿Y ahora?",
        "c31_flujo": "Flujo: tu código decide", "c31_flujo_pie": "Ideal si ya sabes qué revisar",
        "c31_key": "Key", "c31_inst": "Instancia", "c31_sesion": "Sesión",
        # 3.1 · cuatro patrones
        "c31_react_sub": "el modelo decide cada paso", "c31_react_chip": "ya lo conoces",
        "c31_router_sub": "cada petición, a una ventanilla", "c31_router_chip": "decide tu código",
        "c31_rewoo_sub": "la lista del súper primero", "c31_rewoo_chip": "planea una vez",
        "c31_fan_sub": "varios a la vez, juntas notas", "c31_fan_chip": "decide tu código",
        "c31_hoy": "Hoy construimos los tres de la derecha, para Soporte NemoClaw",
        # 3.1 · router
        "c31_ticket_corto": "Ticket del estudiante", "c31_ticket_sub": "«me sale 401…»",
        "c31_recep": "Router", "c31_recep_sub": "la recepcionista: elige UNA etiqueta",
        "c31_v_inst": "instalación", "c31_v_seg": "seguridad", "c31_v_otro": "otro · lo revisa una persona",
        "c31_router_pie": "El modelo solo elige la etiqueta. Tu código manda el ticket a su ventanilla.",
        # 3.1 · etiqueta inventada
        "c31_dice": "El modelo dice", "c31_revisa": "Tu código revisa", "c31_revisa_sub": "¿está en la lista?",
        "c31_no": "no está", "c31_reintento": "Un reintento", "c31_reintento_sub": "le muestras su error",
        "c31_otro_sub": "si insiste · lo revisa una persona",
        "c31_adivinar": "Nunca adivines a mano: «facturacion» no es «brev». Lo que dice el modelo se revisa, igual que lo que escribe un usuario.",
        # 3.1 · ReWOO
        "c31_plan": "Planificador", "c31_plan_sub": "escribe la lista completa", "c31_tope": "máximo 4",
        "c31_ejec": "Ejecutor · sin modelo", "c31_ejec_sub": "todas las búsquedas a la vez",
        "c31_b1": "error 401", "c31_b2": "reanudar Brev", "c31_b3": "cookie vencida", "c31_b4": "servicios de la instancia",
        "c31_b5": "búsqueda 5 · fuera por el tope",
        "c31_sint": "Sintetizador", "c31_sint_sub": "responde con las citas",
        "c31_dos": "2 llamadas al modelo, sin importar cuántas búsquedas",
        # 3.1 · fan-out
        "c31_rep": "Reporte del 401", "c31_rep_sub": "lo reciben tres a la vez",
        "c31_e_key": "Key y cuenta", "c31_e_key_sub": "revisa tu key",
        "c31_e_brev": "Brev", "c31_e_brev_sub": "revisa la instancia",
        "c31_e_seg": "Seguridad", "c31_e_seg_sub": "no contestó",
        "c31_union": "Unión", "c31_union_sub": "junta las notas y dice qué faltó",
        "c31_falta": "Falta la revisión de seguridad",
        "c31_fan_pie": "Como repartir la lista entre tres y juntarse en la caja: si uno no llega, se dice",
        # 3.1 · tiempo
        "c31_t_plan": "Planificador (modelo)", "c31_t_serie": "Búsquedas una tras otra",
        "c31_t_par": "Búsquedas a la vez", "c31_t_sint": "Sintetizador (modelo)",
        "c31_t_vivo": "en vivo: segundos",
        "c31_t_tip": "Si el modelo tarda más que todo lo demás, buscar a la vez casi no se nota. Mide antes de presumir.",
        # 3.1 · dividir
        "c31_una": "Una sola llamada", "c31_gen": "Generalista", "c31_gen_sub": "responde todo de una vez",
        "c31_cuatro": "Dividido en cuatro", "c31_cuatro_sub": "4 llamadas al modelo",
        "c31_mas_espera": "más espera", "c31_mas_costo": "más costo", "c31_mas_fallas": "más lugares donde fallar",
        "c31_si": "Divide si las partes son independientes y mides que ganas",
        "c31_nodiv": "No dividas si el paso 2 depende del 1",
        # 3.1 · avance
        "c31_a1": "Clasifica", "c31_a1s": "cada ticket, con lista cerrada",
        "c31_a2": "Lo envía", "c31_a2s": "al especialista correcto",
        "c31_a3": "Si es urgente", "c31_a3s": "pregunta a varios a la vez",
        "c31_reto": "<strong>Tu reto:</strong> agrega la ventanilla «costos». Tres tickets llegan bien y el reembolso sigue en «otro».",
        # 3.2 · libro abierto
        "c32_pregunta": "«Session expired»: ¿qué hago?",
        "c32_memoria": "De memoria", "c32_mal": "Responde muy seguro… y a veces mal",
        "c32_libro": "A libro abierto (RAG)", "c32_apuntes": "Tus apuntes", "c32_apuntes_sub": "la FAQ del curso",
        "c32_bien": "Responde con su nota al pie", "c32_nose": "o dice «no sé»",
        # 3.2 · pipeline
        "c32_vez": "Una sola vez", "c32_cada": "En cada pregunta",
        "c32_faq": "FAQ", "c32_faq_sub": "un documento por tema",
        "c32_tarjetas": "Tarjetas", "c32_tarjetas_sub": "una por pregunta",
        "c32_coord": "Coordenadas", "c32_coord_sub": "cada tarjeta en el mapa",
        "c32_indice": "Índice", "c32_indice_sub": "guardado para buscar",
        "c32_preg": "Pregunta", "c32_preg_sub": "la escribe el estudiante",
        "c32_coord_q": "Coordenadas", "c32_coord_q_sub": "la pregunta en el mapa",
        "c32_cerca": "Las más cercanas", "c32_cerca_sub": "las 3 tarjetas vecinas",
        "c32_resp": "Respuesta", "c32_resp_sub": "con nota al pie",
        "c32_mapa_pie": "Un embedding son coordenadas: los textos parecidos quedan cerca, como lugares en un mapa",
        # 3.2 · tarjetas
        "c32_doc_sub": "un documento por tema", "c32_parte": "se parte",
        "c32_tema": "Conexión con el laboratorio",
        "c32_f1": "P: ¿De dónde saco la cookie?", "c32_f2": "P: Me sale «session expired»",
        "c32_f3": "P: La conexión da timeout o 502",
        "c32_tarj_pie": "El nombre de cada tarjeta es lo que el agente cita",
        # 3.2 · mapa
        "c32_m_passage": "<code>passage</code> · cada tarjeta, al guardarla",
        "c32_m_query": "<code>query</code> · cada pregunta, al buscar",
        "c32_m_umbral": "Puntaje mínimo · si nada queda cerca, «no sé»",
        "c32_m_q": "«session expired»", "c32_m_peru": "«¿capital de Perú?»",
        "c32_m_warn": "Si inviertes las etiquetas no hay error: solo peores resultados.",
        # 3.2 · reglas
        "c32_r1": "Solo tus apuntes", "c32_r1s": "usa solo lo que te paso",
        "c32_r2": "Nota al pie", "c32_r2s": "cita cada afirmación",
        "c32_r3": "«No sé»", "c32_r3s": "si no hay evidencia",
        "c32_r4": "Datos, no órdenes", "c32_r4s": "lo que lee no manda",
        "c32_r_tip": "Si ninguna tarjeta pasa el puntaje mínimo, ni llamas al modelo. Y tu código revisa que cada cita exista.",
        # 3.2 · medir
        "c32_es": "En español", "c32_en": "En inglés",
        "c32_l_ok": "la correcta quedó primera", "c32_l_baja": "quedó más abajo",
        "c32_h_es": "Hit@1 0.88 · Hit@3 1.00", "c32_h_en": "Hit@1 0.50",
        # 3.2 · herramienta
        "c32_c1": "«Hola»", "c32_c2": "«Session expired»", "c32_c3": "«¿Capital de Perú?»",
        "c32_agente": "Agente", "c32_busca": "busca",
        "c32_o1": "Responde directo, sin buscar", "c32_o2": "Responde con su cita",
        "c32_o3": "Sin evidencia: «no sé»",
        # 3.2 · avance
        "c32_a1": "Responde", "c32_a1s": "con la FAQ del curso",
        "c32_a2": "Cita", "c32_a2s": "cada dato, con su nota al pie",
        "c32_a3": "Dice «no sé»", "c32_a3s": "si no hay evidencia",
        "c32_falta": "<strong>Lo que falta:</strong> «401 después de reanudar Brev» está repartido en varias tarjetas. Juntar piezas de varias fuentes: eso hacen los subagentes.",
        # 3.3 · escritorio
        "c33_escr": "Un solo escritorio",
        "c33_p_inst": "Instrucciones", "c33_p_rep": "Reporte del 401", "c33_p_b1": "Búsqueda: key",
        "c33_p_r1": "Resultado: key", "c33_p_b2": "Búsqueda: instancia", "c33_p_r2": "Resultado: instancia",
        "c33_p_b3": "Búsqueda: cookie", "c33_p_r3": "Resultado: cookie",
        "c33_f1": "Ya no cabe", "c33_f1s": "el escritorio se desborda",
        "c33_f2": "Lo de en medio se pierde", "c33_f2s": "cabe, pero el modelo lo atiende poco",
        "c33_f3": "Un tema ensucia al otro", "c33_f3s": "lo de la key confunde lo de la cookie",
        # 3.3 · flujo
        "c33_plan": "Planificador", "c33_plan_sub": "divide en 2 a 4 partes",
        "c33_s1": "¿qué significa el 401?", "c33_s2": "¿qué cambia al reanudar?", "c33_s3": "¿cómo renuevo la sesión?",
        "c33_sub": "Subagente",
        "c33_sint": "Sintetizador", "c33_sint_sub": "lee los archivos y escribe el reporte",
        "c33_flujo_pie": "Como un jefe de proyecto: cada quien en su escritorio, y deja su nota en una carpeta",
        # 3.3 · escritorios
        "c33_recibe": "Recibe", "c33_reporte": "el reporte", "c33_su_parte": "su parte",
        "c33_herr": "Herramientas", "c33_buscar": "buscar en la FAQ", "c33_escribir": "escribir su borrador",
        "c33_solo": "solo escribe en", "c33_aisla_pie": "Ninguno vio la parte de otro, y el notebook lo comprueba",
        # 3.3 · reporte
        "c33_doc": "Reporte de diagnóstico",
        "c33_d_causa": "<b>Causa más probable:</b> la cookie de acceso venció al reanudar",
        "c33_d_pasos": "<b>Pasos:</b> revisa la key, arranca los servicios de la instancia, copia una cookie nueva",
        "c33_d_falta": "<b>No pudimos verificar:</b> lo que faltó, si un subagente se cayó",
        "c33_check": "Tu código revisa cada cita", "c33_check_sub": "¿está en un borrador y en la FAQ?",
        # 3.3 · topes
        "c33_t1": "Pide 9 subagentes", "c33_t1p": "Máximo 4",
        "c33_t2": "Busca sin parar", "c33_t2p": "Máximo 5 pasos",
        "c33_t3": "Escribe fuera de su archivo", "c33_t3p": "«Permiso denegado»",
        "c33_t4": "Un subagente se cae", "c33_t4p": "El reporte dice qué faltó",
        "c33_t5": "Inventa una cita", "c33_t5p": "Tu código revisa las citas",
        # 3.3 · no es sandbox
        "c33_hoy": "Escritorios separados (hoy)", "c33_programa": "tu programa",
        "c33_ve_key": "ve tu API key", "c33_ve_disco": "ve tu disco",
        "c33_piensa": "Separa lo que el agente <b>piensa</b>",
        "c33_cuarto": "Cuarto con cerradura (OpenShell)", "c33_agente": "Tu agente",
        "c33_archivos": "archivos", "c33_internet": "internet", "c33_programas": "programas",
        "c33_toca": "Limita lo que el agente <b>toca</b>",
        "c33_dos": "Necesitas las dos. El «permiso denegado» de hoy lo puso tu código; el cuarto lo pone OpenShell.",
        # 3.3 · costo
        "c33_rag": "Agente con búsqueda (3.2)", "c33_rag_n": "2 a 3 llamadas",
        "c33_prof": "Agente con 3 subagentes", "c33_prof_n": "≈ 11 llamadas",
        # 3.3 · avance
        "c33_a1": "Planea", "c33_a1s": "divide el reporte en partes",
        "c33_a2": "Reparte", "c33_a2s": "subagentes con escritorio propio",
        "c33_a3": "Guarda notas", "c33_a3s": "un borrador por subagente",
        "c33_a4": "Revisa citas", "c33_a4s": "reporte de diagnóstico confiable",
        "c33_mod4": "<strong>Módulo 4:</strong> lo llevas a NemoClaw en Brev, con la FAQ en su carpeta de trabajo y dentro de un sandbox.",
        # 3.4 · print vs traza
        "c34_print": "Con print", "c34_print_pie": "Pedazos sueltos, sin orden ni tiempos",
        "c34_j1": "buscando…", "c34_j2": "ok", "c34_j3": "paso 2", "c34_j4": "respuesta: …",
        "c34_j5": "llamando al modelo", "c34_j6": "¿error?",
        "c34_traza": "Con una traza", "c34_traza_pie": "Cada paso en orden, con su tiempo y su estado",
        "c34_r1": "Pregunta recibida", "c34_r2": "Modelo · paso 1", "c34_r3": "Herramienta · estado de Brev",
        "c34_r4": "Respuesta enviada",
        # 3.4 · paquete
        "c34_paquete": "Tu paquete", "c34_pq1": "Salió del almacén", "c34_pq2": "Llegó a tu ciudad",
        "c34_pq3": "Retraso en la aduana", "c34_pq4": "Entregado",
        "c34_tag_traza": "traza = todo el historial", "c34_tag_span": "span = una línea",
        "c34_tu_agente": "Tu agente",
        "c34_paquete_pie": "OpenTelemetry es el formato de la guía de envío. Phoenix es el mapa donde ves el recorrido.",
        # 3.4 · tipos de paso
        "k_agente": "Agente", "k_modelo": "Modelo", "k_herr": "Herramienta", "k_busq": "Búsqueda",
        "c34_m_sub": "LLM · cada pregunta al modelo", "c34_h_sub": "TOOL · cada herramienta que usa",
        "c34_b_sub": "RETRIEVER · cada búsqueda en la FAQ",
        "c34_mensajes": "mensajes", "c34_tokens": "texto usado", "c34_paro": "por qué paró",
        "c34_args": "con qué datos", "c34_salida": "qué devolvió", "c34_error": "el error",
        "c34_docs": "qué documentos", "c34_puntaje": "con qué puntaje",
        "c34_tipos_pie": "Cada paso lleva su etiqueta: así sabes si falló el modelo, la herramienta o la búsqueda",
        # 3.4 · tachar
        "c34_llega": "Lo que llega", "c34_texto": "mi key es nvapi-AbCd…",
        "c34_redactar": "redactar()", "c34_redactar_sub": "plumón negro antes de guardar",
        "c34_guarda": "Lo que se guarda", "c34_guardado": "mi key es nvapi-",
        "c34_destino": "Traza y Phoenix", "c34_destino_sub": "sin secretos",
        "c34_tachar_pie": "Una traza guarda los mensajes completos: si alguien pega su key, ahí se queda",
        # 3.4 · árbol
        "c34_t_paso": "Paso", "c34_t_tiempo": "Cuándo y cuánto tardó", "c34_t_ms": "ms",
        # 3.4 · cuatro bugs
        "c34_bug1": "La herramienta falla", "c34_bug1_v": "un paso con ✖ y el error exacto",
        "c34_bug2": "El loop no termina", "c34_bug2_v": "la misma búsqueda en cada paso",
        "c34_bug3": "Una cita inventada", "c34_bug3_v": "ninguna búsqueda devolvió ese documento",
        "c34_bug4": "Tardó mucho", "c34_bug4_v": "lo lento es la herramienta, no el modelo",
        "c34_factura": "buscar_faq «factura de Brev»",
        # 3.4 · error no es respuesta rota
        "c34_e1": "La herramienta falló", "c34_e1s": "el error le llega al agente como un dato más",
        "c34_e2": "El agente siguió", "c34_e2s": "la raíz queda en ✔",
        "c34_e3": "«No pude verificar tu instancia…»", "c34_e3s": "la respuesta lo dice: eso es lo correcto",
        # 3.4 · NVIDIA
        "c34_capa1": "Tu código de agente", "c34_capa2": "El sandbox",
        "c34_nat_sub": "la caja de herramientas de NVIDIA", "c34_trazas": "trazas",
        "c34_phoenix_sub": "el mapa del recorrido", "c34_otras": "u otras: Langfuse, LangSmith, Weave",
        "c34_sandbox": "NemoClaw · sandbox", "c34_agente": "Tu agente",
        "c34_regs": "Registros de NemoClaw", "c34_regs_sub": "lo que pasó en el cuarto",
        "c34_msgs": "mensajes", "c34_bloq": "bloqueos de OpenShell", "c34_conv": "conversaciones",
        "c34_nv_pie": "Hablan el mismo idioma que lo de hoy. Las dos capas las usas desde el Módulo 4.",
        # 3.4 · avance
        "c34_a1": "Su traza", "c34_a1s": "en cada respuesta",
        "c34_a2": "Revisión automática", "c34_a2s": "citas, repeticiones y errores",
        "c34_a3": "Secretos tachados", "c34_a3s": "un archivo listo para reportar",
        "c34_mod4": "<strong>Módulo 4:</strong> dos capas. Trazas para tu agente y registros para el sandbox. En la 4.4 trazas las llamadas a Hermes.",
    },
    "en": {
        "modelo": "Model", "llamada": "1 call", "avance": "Soporte NemoClaw",
        "c31_ticket": "“I get a 401 in the lab after resuming Brev”",
        "c31_loop": "Loop: the model decides", "c31_loop_pie": "Great when step 2 depends on step 1",
        "c31_paso1": "Step 1", "c31_paso1_sub": "looks at the result", "c31_ahora": "Now what?",
        "c31_flujo": "Workflow: your code decides", "c31_flujo_pie": "Great when you know what to check",
        "c31_key": "Key", "c31_inst": "Instance", "c31_sesion": "Session",
        "c31_react_sub": "the model decides each step", "c31_react_chip": "you know it",
        "c31_router_sub": "each request, to one window", "c31_router_chip": "your code decides",
        "c31_rewoo_sub": "the shopping list first", "c31_rewoo_chip": "plans once",
        "c31_fan_sub": "several at once, merge notes", "c31_fan_chip": "your code decides",
        "c31_hoy": "Today we build the three on the right, for Soporte NemoClaw",
        "c31_ticket_corto": "Student ticket", "c31_ticket_sub": "“I get a 401…”",
        "c31_recep": "Router", "c31_recep_sub": "the receptionist: picks ONE label",
        "c31_v_inst": "instalacion", "c31_v_seg": "seguridad", "c31_v_otro": "otro · a person reviews it",
        "c31_router_pie": "The model only picks the label. Your code sends the ticket to its window.",
        "c31_dice": "The model says", "c31_revisa": "Your code checks", "c31_revisa_sub": "is it on the list?",
        "c31_no": "not there", "c31_reintento": "One retry", "c31_reintento_sub": "you show it its error",
        "c31_otro_sub": "if it insists · a person reviews it",
        "c31_adivinar": "Never guess by hand: “facturacion” is not “brev”. What the model says gets checked, just like what a user types.",
        "c31_plan": "Planner", "c31_plan_sub": "writes the whole list", "c31_tope": "max 4",
        "c31_ejec": "Executor · no model", "c31_ejec_sub": "every search at once",
        "c31_b1": "401 error", "c31_b2": "resuming Brev", "c31_b3": "expired cookie", "c31_b4": "instance services",
        "c31_b5": "search 5 · cut by the cap",
        "c31_sint": "Synthesizer", "c31_sint_sub": "answers with citations",
        "c31_dos": "2 model calls, no matter how many searches",
        "c31_rep": "The 401 report", "c31_rep_sub": "three get it at once",
        "c31_e_key": "Key and account", "c31_e_key_sub": "checks your key",
        "c31_e_brev": "Brev", "c31_e_brev_sub": "checks the instance",
        "c31_e_seg": "Security", "c31_e_seg_sub": "didn't answer",
        "c31_union": "Join", "c31_union_sub": "merges the notes, says what's missing",
        "c31_falta": "The security review is missing",
        "c31_fan_pie": "Like splitting the list among three and meeting at the checkout: if one doesn't show, you say so",
        "c31_t_plan": "Planner (model)", "c31_t_serie": "Searches one after another",
        "c31_t_par": "Searches at once", "c31_t_sint": "Synthesizer (model)",
        "c31_t_vivo": "live: seconds",
        "c31_t_tip": "If the model takes longer than everything else, searching at once barely shows. Measure before you brag.",
        "c31_una": "A single call", "c31_gen": "Generalist", "c31_gen_sub": "answers it all at once",
        "c31_cuatro": "Split in four", "c31_cuatro_sub": "4 model calls",
        "c31_mas_espera": "more waiting", "c31_mas_costo": "more cost", "c31_mas_fallas": "more places to fail",
        "c31_si": "Split if the parts are independent and you measure a gain",
        "c31_nodiv": "Don't split if step 2 depends on step 1",
        "c31_a1": "Classifies", "c31_a1s": "each ticket, with a closed list",
        "c31_a2": "Sends it", "c31_a2s": "to the right specialist",
        "c31_a3": "If it's urgent", "c31_a3s": "asks several at once",
        "c31_reto": "<strong>Your challenge:</strong> add the “costos” window. Three tickets land correctly and the refund still goes to “otro”.",
        "c32_pregunta": "“Session expired”: what do I do?",
        "c32_memoria": "From memory", "c32_mal": "Answers very confidently… and sometimes wrong",
        "c32_libro": "Open book (RAG)", "c32_apuntes": "Your notes", "c32_apuntes_sub": "the course FAQ",
        "c32_bien": "Answers with its footnote", "c32_nose": "or says “I don't know”",
        "c32_vez": "Just once", "c32_cada": "On every question",
        "c32_faq": "FAQ", "c32_faq_sub": "one document per topic",
        "c32_tarjetas": "Cards", "c32_tarjetas_sub": "one per question",
        "c32_coord": "Coordinates", "c32_coord_sub": "each card on the map",
        "c32_indice": "Index", "c32_indice_sub": "saved for searching",
        "c32_preg": "Question", "c32_preg_sub": "the student writes it",
        "c32_coord_q": "Coordinates", "c32_coord_q_sub": "the question on the map",
        "c32_cerca": "The closest", "c32_cerca_sub": "the 3 neighboring cards",
        "c32_resp": "Answer", "c32_resp_sub": "with a footnote",
        "c32_mapa_pie": "An embedding is a set of coordinates: similar texts end up close, like places on a map",
        "c32_doc_sub": "one document per topic", "c32_parte": "gets cut",
        "c32_tema": "Connecting to the lab",
        "c32_f1": "Q: Where do I get the cookie?", "c32_f2": "Q: I get “session expired”",
        "c32_f3": "Q: The connection times out or 502s",
        "c32_tarj_pie": "Each card's name is what the agent cites",
        "c32_m_passage": "<code>passage</code> · each card, when you save it",
        "c32_m_query": "<code>query</code> · each question, when you search",
        "c32_m_umbral": "Minimum score · if nothing is close, “I don't know”",
        "c32_m_q": "“session expired”", "c32_m_peru": "“capital of Peru?”",
        "c32_m_warn": "If you swap the labels there's no error: just worse results.",
        "c32_r1": "Only your notes", "c32_r1s": "use only what I give you",
        "c32_r2": "Footnote", "c32_r2s": "cite every claim",
        "c32_r3": "“I don't know”", "c32_r3s": "if there's no evidence",
        "c32_r4": "Data, not orders", "c32_r4s": "what it reads doesn't command",
        "c32_r_tip": "If no card passes the minimum score, don't even call the model. And your code checks that every citation exists.",
        "c32_es": "In Spanish", "c32_en": "In English",
        "c32_l_ok": "the right one came first", "c32_l_baja": "it came further down",
        "c32_h_es": "Hit@1 0.88 · Hit@3 1.00", "c32_h_en": "Hit@1 0.50",
        "c32_c1": "“Hi”", "c32_c2": "“Session expired”", "c32_c3": "“Capital of Peru?”",
        "c32_agente": "Agent", "c32_busca": "searches",
        "c32_o1": "Answers directly, no search", "c32_o2": "Answers with its citation",
        "c32_o3": "No evidence: “I don't know”",
        "c32_a1": "Answers", "c32_a1s": "from the course FAQ",
        "c32_a2": "Cites", "c32_a2s": "every fact, with its footnote",
        "c32_a3": "Says “I don't know”", "c32_a3s": "when there's no evidence",
        "c32_falta": "<strong>What's missing:</strong> “401 after resuming Brev” is spread across several cards. Pulling pieces from several sources together: that's what subagents do.",
        "c33_escr": "A single desk",
        "c33_p_inst": "Instructions", "c33_p_rep": "The 401 report", "c33_p_b1": "Search: key",
        "c33_p_r1": "Result: key", "c33_p_b2": "Search: instance", "c33_p_r2": "Result: instance",
        "c33_p_b3": "Search: cookie", "c33_p_r3": "Result: cookie",
        "c33_f1": "It no longer fits", "c33_f1s": "the desk overflows",
        "c33_f2": "The middle gets lost", "c33_f2s": "it fits, but the model barely notices it",
        "c33_f3": "One topic muddies another", "c33_f3s": "the key stuff confuses the cookie stuff",
        "c33_plan": "Planner", "c33_plan_sub": "splits into 2 to 4 parts",
        "c33_s1": "what does the 401 mean?", "c33_s2": "what changes on resume?", "c33_s3": "how do I renew the session?",
        "c33_sub": "Subagent",
        "c33_sint": "Synthesizer", "c33_sint_sub": "reads the files and writes the report",
        "c33_flujo_pie": "Like a project lead: everyone at their own desk, leaving their note in a folder",
        "c33_recibe": "Gets", "c33_reporte": "the report", "c33_su_parte": "its part",
        "c33_herr": "Tools", "c33_buscar": "search the FAQ", "c33_escribir": "write its draft",
        "c33_solo": "only writes to", "c33_aisla_pie": "None saw another's part, and the notebook checks it",
        "c33_doc": "Diagnostic report",
        "c33_d_causa": "<b>Most likely cause:</b> the access cookie expired on resume",
        "c33_d_pasos": "<b>Steps:</b> check the key, start the instance services, copy a fresh cookie",
        "c33_d_falta": "<b>We couldn't verify:</b> what's missing, if a subagent failed",
        "c33_check": "Your code checks every citation", "c33_check_sub": "is it in a draft and in the FAQ?",
        "c33_t1": "Asks for 9 subagents", "c33_t1p": "Max 4",
        "c33_t2": "Searches nonstop", "c33_t2p": "Max 5 steps",
        "c33_t3": "Writes outside its file", "c33_t3p": "“Permission denied”",
        "c33_t4": "A subagent fails", "c33_t4p": "The report says what's missing",
        "c33_t5": "Makes up a citation", "c33_t5p": "Your code checks citations",
        "c33_hoy": "Separate desks (today)", "c33_programa": "your program",
        "c33_ve_key": "sees your API key", "c33_ve_disco": "sees your disk",
        "c33_piensa": "Separates what the agent <b>thinks</b>",
        "c33_cuarto": "Locked room (OpenShell)", "c33_agente": "Your agent",
        "c33_archivos": "files", "c33_internet": "internet", "c33_programas": "programs",
        "c33_toca": "Limits what the agent <b>touches</b>",
        "c33_dos": "You need both. Today's “permission denied” came from your code; OpenShell provides the room.",
        "c33_rag": "Agent with search (3.2)", "c33_rag_n": "2 to 3 calls",
        "c33_prof": "Agent with 3 subagents", "c33_prof_n": "≈ 11 calls",
        "c33_a1": "Plans", "c33_a1s": "splits the report into parts",
        "c33_a2": "Delegates", "c33_a2s": "subagents with their own desk",
        "c33_a3": "Keeps notes", "c33_a3s": "one draft per subagent",
        "c33_a4": "Checks citations", "c33_a4s": "a trustworthy diagnostic report",
        "c33_mod4": "<strong>Module 4:</strong> you take it to NemoClaw on Brev, with the FAQ in its working folder and inside a sandbox.",
        "c34_print": "With print", "c34_print_pie": "Loose fragments, no order or timing",
        "c34_j1": "searching…", "c34_j2": "ok", "c34_j3": "step 2", "c34_j4": "answer: …",
        "c34_j5": "calling the model", "c34_j6": "error?",
        "c34_traza": "With a trace", "c34_traza_pie": "Every step in order, with its time and status",
        "c34_r1": "Question received", "c34_r2": "Model · step 1", "c34_r3": "Tool · Brev status",
        "c34_r4": "Answer sent",
        "c34_paquete": "Your parcel", "c34_pq1": "Left the warehouse", "c34_pq2": "Arrived in your city",
        "c34_pq3": "Held at customs", "c34_pq4": "Delivered",
        "c34_tag_traza": "trace = the whole history", "c34_tag_span": "span = one line",
        "c34_tu_agente": "Your agent",
        "c34_paquete_pie": "OpenTelemetry is the shipping-label format. Phoenix is the map where you see the route.",
        "k_agente": "Agent", "k_modelo": "Model", "k_herr": "Tool", "k_busq": "Search",
        "c34_m_sub": "LLM · each question to the model", "c34_h_sub": "TOOL · each tool it uses",
        "c34_b_sub": "RETRIEVER · each FAQ search",
        "c34_mensajes": "messages", "c34_tokens": "text used", "c34_paro": "why it stopped",
        "c34_args": "with what data", "c34_salida": "what it returned", "c34_error": "the error",
        "c34_docs": "which documents", "c34_puntaje": "with what score",
        "c34_tipos_pie": "Every step carries its label: that's how you know if the model, the tool or the search failed",
        "c34_llega": "What comes in", "c34_texto": "my key is nvapi-AbCd…",
        "c34_redactar": "redactar()", "c34_redactar_sub": "black marker before saving",
        "c34_guarda": "What gets saved", "c34_guardado": "my key is nvapi-",
        "c34_destino": "Trace and Phoenix", "c34_destino_sub": "no secrets",
        "c34_tachar_pie": "A trace stores full messages: if someone pastes their key, there it stays",
        "c34_t_paso": "Step", "c34_t_tiempo": "When, and how long it took", "c34_t_ms": "ms",
        "c34_bug1": "The tool fails", "c34_bug1_v": "a step with ✖ and the exact error",
        "c34_bug2": "The loop never ends", "c34_bug2_v": "the same search at every step",
        "c34_bug3": "An invented citation", "c34_bug3_v": "no search ever returned that document",
        "c34_bug4": "It took too long", "c34_bug4_v": "the tool is slow, not the model",
        "c34_factura": "buscar_faq “Brev invoice”",
        "c34_e1": "The tool failed", "c34_e1s": "the agent gets the error as one more piece of data",
        "c34_e2": "The agent kept going", "c34_e2s": "the root stays ✔",
        "c34_e3": "“I couldn't verify your instance…”", "c34_e3s": "the answer says so: that's correct",
        "c34_capa1": "Your agent code", "c34_capa2": "The sandbox",
        "c34_nat_sub": "NVIDIA's toolbox", "c34_trazas": "traces",
        "c34_phoenix_sub": "the map of the route", "c34_otras": "or others: Langfuse, LangSmith, Weave",
        "c34_sandbox": "NemoClaw · sandbox", "c34_agente": "Your agent",
        "c34_regs": "NemoClaw logs", "c34_regs_sub": "what happened in the room",
        "c34_msgs": "messages", "c34_bloq": "OpenShell blocks", "c34_conv": "conversations",
        "c34_nv_pie": "They speak the same language as today's work. You use both layers from Module 4.",
        "c34_a1": "Its trace", "c34_a1s": "with every answer",
        "c34_a2": "Automatic review", "c34_a2s": "citations, repeats and errors",
        "c34_a3": "Redacted secrets", "c34_a3s": "a file ready to report",
        "c34_mod4": "<strong>Module 4:</strong> two layers. Traces for your agent and logs for the sandbox. In 4.4 you trace the calls to Hermes.",
    },
}


# ------------------------------------------------------------------------------------------
# Piezas propias del módulo
# ------------------------------------------------------------------------------------------
def _p(paso):
    return f' data-paso="{paso}"' if paso else ""


def _call(tipo, texto, paso=None):
    return f'<div class="call {tipo}"{_p(paso)}><p>{texto}</p></div>'


def _card(titulo, contenido, paso=None, clase="", icono=None):
    ico = f'<span class="dg-i">{icono}</span>' if icono else ""
    return f'<div class="dg-card {clase}"{_p(paso)}><h3>{ico}{titulo}</h3>{contenido}</div>'


def _pill(icono, texto, clase="", paso=None, extra=""):
    return f'<span class="c3-pill {clase}"{_p(paso)}><span class="dg-i">{icono}</span>{texto}{extra}</span>'


def _fila(*piezas, clase=""):
    return f'<div class="dg-row {clase}">' + "".join(piezas) + "</div>"


def _abanico(origen, ramas, destino="", clase=""):
    """origen → varias filas en paralelo → destino. ramas: lista de (paso, html)."""
    filas = "".join(f'<div class="dg-fan-row"{_p(p)}>{h}</div>' for p, h in ramas)
    return f'<div class="dg c3-abanico {clase}">{origen}<div class="dg-fan">{filas}</div>{destino}</div>'


def _carril(etiqueta, icono, contenido, paso=None):
    return (f'<div class="c3-carril"{_p(paso)}><span class="c3-carril-lab"><span class="dg-i">{icono}</span>{etiqueta}</span>'
            f'<div class="dg-row">{contenido}</div></div>')


def _resp(texto, clase="", paso=None, icono="chat"):
    return f'<div class="c3-resp {clase}"{_p(paso)}><span class="dg-i">{icono}</span>{texto}</div>'


def _avance(t, version, items, nota, tipo="tip"):
    fila = "".join(nodo(ic, a, b, paso=i + 1) for i, (ic, a, b) in enumerate(items))
    return ('<div class="dg dg-flow">'
            + _card(f'{t["avance"]} {version}', f'<div class="dg-row">{fila}</div>', clase="is-primary", icono="forum")
            + "</div>" + _call(tipo, nota, paso=len(items) + 1))


# Árbol de una traza: cada fila (nivel, tipo, etiqueta, nombre, inicio_ms, ms, ok, paso, detalle)
_TIPOS = {"agente": ("k_agente", "assistant"), "modelo": ("k_modelo", "auto_awesome"),
          "herr": ("k_herr", "settings"), "busq": ("k_busq", "search")}


def _arbol(t, filas, total=None, cabecera=True, clase=""):
    niveles = [f[0] for f in filas]
    html_filas = []
    for i, (n, tipo, nombre, inicio, ms, ok, paso, detalle) in enumerate(filas):
        resto = niveles[i + 1:]

        def sigue(k):                         # ¿hay otro hermano de nivel k más abajo, antes de subir?
            for m in resto:
                if m < k:
                    return False
                if m == k:
                    return True
            return False
        guias = "".join(f'<i class="c3-guia" style="--g:{k}"></i>' for k in range(1, n) if sigue(k))
        if n > 0:
            guias += f'<i class="c3-codo" style="--g:{n}"></i>'
            if sigue(n):
                guias += f'<i class="c3-guia" style="--g:{n}"></i>'
        clave, ico = _TIPOS[tipo]
        det = f'<small class="c3-det">{detalle}</small>' if detalle else ""
        nombre_html = (f'<div class="c3-nombre" style="--n:{n}">{guias}'
                       f'<span class="c3-kind k-{tipo}"><span class="dg-i">{ico}</span>{t[clave]}</span>'
                       f'<code>{nombre}</code>{det}</div>')
        barra = ""
        if total:
            izq, ancho = 100 * inicio / total, 100 * ms / total
            barra = (f'<div class="c3-pista"><span class="c3-barra k-{tipo}" '
                     f'style="left:{izq:.1f}%;width:max({ancho:.1f}%,4px)"></span></div>')
        estado = ('<span class="dg-i c3-ok">check_circle</span>' if ok else '<span class="dg-i c3-mal">cancel</span>')
        html_filas.append(f'<div class="c3-span{" mal" if not ok else ""}"{_p(paso)}>{nombre_html}{barra}'
                          f'<span class="c3-ms">{ms}</span>{estado}</div>')
    cab = ""
    if cabecera:
        cab = (f'<div class="c3-span c3-cab"><span>{t["c34_t_paso"]}</span>'
               + (f'<span>{t["c34_t_tiempo"]} · 0 → {total} ms</span>' if total else "")
               + f'<span class="c3-ms">{t["c34_t_ms"]}</span><span></span></div>')
    return f'<div class="c3-arbol {clase}{" con-barras" if total else ""}">{cab}{"".join(html_filas)}</div>'


# ------------------------------------------------------------------------------------------
# 3.1 · Enrutamiento y workflows
# ------------------------------------------------------------------------------------------
def c31_loop_vs_flujo(lang):
    t = T[lang]
    izq = _card(t["c31_loop"], _fila(nodo("visibility", t["c31_paso1"], t["c31_paso1_sub"], clase="mini"),
                                     flecha("h"), nodo("quiz", t["c31_ahora"], clase="mini warn"),
                                     flecha("h"), nodo("quiz", t["c31_ahora"], clase="mini warn"))
                + pie(t["c31_loop_pie"], icono="replay"), paso=2, icono="replay")
    der = _card(t["c31_flujo"], _fila(nodo("key", t["c31_key"], clase="mini ok"), flecha("h"),
                                      nodo("computer", t["c31_inst"], clase="mini ok"), flecha("h"),
                                      nodo("cookie", t["c31_sesion"], clase="mini ok"))
                + pie(t["c31_flujo_pie"], icono="check_circle"),
                paso=3, clase="is-primary", icono="code")
    return (f'<div class="c3-ticket" data-paso="1"><span class="dg-i">confirmation_number</span>{t["c31_ticket"]}</div>'
            f'<div class="dg c3-two">{izq}{der}</div>')


def c31_patrones(lang):
    t = T[lang]
    datos = [("replay", "ReAct", t["c31_react_sub"], t["c31_react_chip"], "c3-dim"),
             ("route", "Router", t["c31_router_sub"], t["c31_router_chip"], "is-primary"),
             ("edit_note", "ReWOO", t["c31_rewoo_sub"], t["c31_rewoo_chip"], "is-primary"),
             ("groups", "Fan-out", t["c31_fan_sub"], t["c31_fan_chip"], "is-primary")]
    fila = "".join(nodo(ic, n, s, clase=c, paso=i + 1, extra=chips([ch]))
                   for i, (ic, n, s, ch, c) in enumerate(datos))
    return f'<div class="dg c3-cuatro">{fila}</div>' + pie(t["c31_hoy"], paso=5, icono="forum")


def c31_router(lang):
    t = T[lang]
    origen = _fila(nodo("confirmation_number", t["c31_ticket_corto"], t["c31_ticket_sub"], paso=1),
                   flecha("h", paso=2),
                   nodo("route", t["c31_recep"], t["c31_recep_sub"], clase="is-primary", paso=2))
    marca = '<span class="c3-badge" data-paso="4"><span class="dg-i">check</span>401</span>'
    ventanillas = [("download", t["c31_v_inst"], "", ""), ("key", "api_key", "ok", marca),
                   ("computer", "brev", "", ""), ("lock", t["c31_v_seg"], "", ""),
                   ("person", t["c31_v_otro"], "", "")]
    ramas = [(3, flecha("h") + _pill(ic, tx, clase=c, extra=ex)) for ic, tx, c, ex in ventanillas]
    return _abanico(origen, ramas) + pie(t["c31_router_pie"], paso=5, icono="info")


def c31_etiqueta(lang):
    t = T[lang]
    return (_fila(nodo("auto_awesome", t["c31_dice"], "«facturacion»" if lang == "es" else "“facturacion”", clase="bad", paso=1),
                  flecha("h", paso=2),
                  nodo("verified", t["c31_revisa"], t["c31_revisa_sub"], paso=2),
                  flecha("h", t["c31_no"], clase="warn", paso=3),
                  nodo("replay", t["c31_reintento"], t["c31_reintento_sub"], clase="warn", paso=3),
                  flecha("h", paso=4),
                  nodo("person", "otro", t["c31_otro_sub"], clase="ok", paso=4), clase="dg")
            + _call("warn", t["c31_adivinar"], paso=5))


def c31_rewoo(lang):
    t = T[lang]
    busquedas = "".join(_pill("search", t[k]) for k in ("c31_b1", "c31_b2", "c31_b3", "c31_b4"))
    busquedas += _pill("block", t["c31_b5"], clase="bad")
    ejec = (f'<div class="dg-card c3-ejec" data-paso="2"><h3><span class="dg-i">bolt</span>{t["c31_ejec"]}</h3>'
            f'<div class="c3-pilas">{busquedas}</div><small class="dg-card-sub">{t["c31_ejec_sub"]}</small></div>')
    return (_fila(nodo("edit_note", t["c31_plan"], t["c31_plan_sub"], paso=1, extra=chips([t["llamada"], t["c31_tope"]])),
                  flecha("h", paso=2), ejec, flecha("h", paso=3),
                  nodo("article", t["c31_sint"], t["c31_sint_sub"], clase="is-primary", paso=3, extra=chips([t["llamada"]])),
                  clase="dg")
            + pie(t["c31_dos"], paso=4, icono="auto_awesome"))


def c31_fanout(lang):
    t = T[lang]
    origen = nodo("confirmation_number", t["c31_rep"], t["c31_rep_sub"], paso=1)
    ramas = [(2, flecha("h") + nodo("key", t["c31_e_key"], t["c31_e_key_sub"], clase="mini ok") + flecha("h")),
             (2, flecha("h") + nodo("computer", t["c31_e_brev"], t["c31_e_brev_sub"], clase="mini ok") + flecha("h")),
             (3, flecha("h") + nodo("lock", t["c31_e_seg"], t["c31_e_seg_sub"], clase="mini bad") + '<span class="c3-hueco"></span>')]
    destino = nodo("done_all", t["c31_union"], t["c31_union_sub"], clase="is-primary", paso=4,
                   extra=f'<span class="c3-falta"><span class="dg-i">warning</span>{t["c31_falta"]}</span>')
    return _abanico(origen, ramas, destino) + pie(t["c31_fan_pie"], paso=5, icono="groups")


def _barras(filas):
    """filas: (etiqueta, segundos, máximo, clase, paso, chip)."""
    out = []
    for et, seg, mx, clase, paso, chip in filas:
        ch = f'<span class="c3-chip-vivo">{chip}</span>' if chip else ""
        out.append(f'<div class="c3-bar-fila {clase}"{_p(paso)}><span class="c3-bar-lab">{et}</span>'
                   f'<div class="c3-bar-pista"><span class="c3-bar" style="width:{70 * seg / mx:.0f}%"></span>'
                   f'<b>{seg:.1f} s</b>{ch}</div></div>')
    return '<div class="dg c3-barras">' + "".join(out) + "</div>"


def c31_tiempo(lang):
    t = T[lang]
    filas = [(t["c31_t_plan"], 0.3, 2.0, "modelo", 2, t["c31_t_vivo"]),
             (t["c31_t_serie"], 2.0, 2.0, "lento", 1, ""),
             (t["c31_t_par"], 0.5, 2.0, "rapido", 1, ""),
             (t["c31_t_sint"], 0.3, 2.0, "modelo", 2, t["c31_t_vivo"])]
    return _barras(filas) + _call("tip", t["c31_t_tip"], paso=3)


def c31_dividir(lang):
    t = T[lang]
    izq = _card(t["c31_una"], nodo("auto_awesome", t["c31_gen"], t["c31_gen_sub"], clase="ok")
                + chips([t["llamada"]]), paso=1, icono="check_circle")
    puntos = "".join('<span class="c3-punto"><span class="dg-i">auto_awesome</span></span>' for _ in range(4))
    der = _card(t["c31_cuatro"], f'<div class="c3-puntos">{puntos}</div><small class="dg-card-sub">{t["c31_cuatro_sub"]}</small>'
                + chips([f'<span class="dg-i">schedule</span>{t["c31_mas_espera"]}',
                         f'<span class="dg-i">paid</span>{t["c31_mas_costo"]}',
                         f'<span class="dg-i">warning</span>{t["c31_mas_fallas"]}']), paso=2, icono="grid_view")
    return (f'<div class="dg c3-two">{izq}{der}</div>'
            + '<div class="dg-row tight">' + pie(t["c31_si"], paso=3, icono="check_circle")
            + pie(t["c31_nodiv"], paso=4, icono="block") + "</div>")


def c31_avance(lang):
    t = T[lang]
    return _avance(t, "v3.1", [("route", t["c31_a1"], t["c31_a1s"]), ("person", t["c31_a2"], t["c31_a2s"]),
                               ("groups", t["c31_a3"], t["c31_a3s"])], t["c31_reto"])


# ------------------------------------------------------------------------------------------
# 3.2 · RAG
# ------------------------------------------------------------------------------------------
def c32_libro_abierto(lang):
    t = T[lang]
    q = f'<span class="c3-q-chip"><span class="dg-i">chat</span>{t["c32_pregunta"]}</span>'
    izq = _card(t["c32_memoria"], '<div class="dg-col">' + q + flecha("v")
                + nodo("auto_awesome", t["modelo"], clase="mini") + flecha("v")
                + _resp(t["c32_mal"], clase="bad", icono="error") + "</div>", paso=1, icono="history")
    der = _card(t["c32_libro"], '<div class="dg-col">' + q + flecha("v")
                + _fila(nodo("menu_book", t["c32_apuntes"], t["c32_apuntes_sub"], clase="mini"), flecha("h"),
                        nodo("auto_awesome", t["modelo"], clase="mini is-primary"))
                + flecha("v") + _resp(t["c32_bien"] + ' <span class="c3-nota-pie">¹</span>', clase="ok", icono="check_circle")
                + chips([t["c32_nose"]]) + "</div>", paso=2, clase="is-primary", icono="menu_book")
    return f'<div class="dg c3-two">{izq}{der}</div>'


def c32_pipeline(lang):
    t = T[lang]
    vez = (nodo("description", t["c32_faq"], t["c32_faq_sub"], clase="mini") + flecha("h")
           + nodo("cards", t["c32_tarjetas"], t["c32_tarjetas_sub"], clase="mini") + flecha("h", "passage")
           + nodo("my_location", t["c32_coord"], t["c32_coord_sub"], clase="mini") + flecha("h")
           + nodo("dataset", t["c32_indice"], t["c32_indice_sub"], clase="mini"))
    cada = (nodo("chat", t["c32_preg"], t["c32_preg_sub"], clase="mini") + flecha("h", "query")
            + nodo("my_location", t["c32_coord_q"], t["c32_coord_q_sub"], clase="mini") + flecha("h")
            + nodo("radar", t["c32_cerca"], t["c32_cerca_sub"], clase="mini") + flecha("h")
            + nodo("article", t["c32_resp"], t["c32_resp_sub"], clase="mini is-primary"))
    return ('<div class="dg c3-carriles">' + _carril(t["c32_vez"], "event", vez, paso=1)
            + _carril(t["c32_cada"], "replay", cada, paso=2) + "</div>" + pie(t["c32_mapa_pie"], paso=3, icono="my_location"))


def c32_tarjetas(lang):
    t = T[lang]
    fichas = [("c32_f1", "que-es-la-access-session"), ("c32_f2", "me-sale-session-expired"), ("c32_f3", "timeout-o-502")]
    html_f = "".join(f'<div class="c3-ficha"><small>{t["c32_tema"]}</small><b>{t[k]}</b>'
                     f'<code>conexion-laboratorio.md#{i}…</code></div>' for k, i in fichas)
    return (_fila(nodo("description", "conexion-laboratorio.md", t["c32_doc_sub"], paso=1),
                  flecha("h", t["c32_parte"], paso=2),
                  f'<div class="c3-fichas" data-paso="2">{html_f}</div>', clase="dg")
            + pie(t["c32_tarj_pie"], paso=3, icono="bookmark"))


def c32_mapa(lang):
    t = T[lang]
    puntos = [(14, 22), (30, 30), (42, 16), (55, 86), (78, 16), (88, 62), (44, 36), (91, 34), (40, 76), (8, 42)]
    cerca = [(54, 54), (71, 52), (62, 66)]
    dots = "".join(f'<span class="c3-dot" style="left:{x}%;top:{y}%"></span>' for x, y in puntos)
    dots_c = "".join(f'<span class="c3-dot cerca" style="left:{x}%;top:{y}%"></span>' for x, y in cerca)
    mapa = (f'<div class="c3-mapa">'
            f'<div class="c3-capa" data-paso="1">{dots}{dots_c}</div>'
            f'<div class="c3-capa" data-paso="2"><span class="c3-radio" style="left:62%;top:46%"></span>'
            f'<span class="c3-pin" style="left:62%;top:46%"><span class="dg-i">chat</span></span>'
            f'<span class="c3-pin-lab" style="left:62%;top:46%">{t["c32_m_q"]}</span></div>'
            f'<div class="c3-capa" data-paso="3"><span class="c3-radio vacio" style="left:20%;top:74%"></span>'
            f'<span class="c3-pin otro" style="left:20%;top:74%"><span class="dg-i">chat</span></span>'
            f'<span class="c3-pin-lab" style="left:20%;top:74%">{t["c32_m_peru"]}</span></div></div>')
    filas = [(1, "circle", t["c32_m_passage"], "c3-l-dot"), (2, "chat", t["c32_m_query"], "is-primary"),
             (3, "radio_button_unchecked", t["c32_m_umbral"], "c3-l-umbral")]
    leyenda = "".join(f'<div class="dg-legend-row {c}" data-paso="{p}"><span class="dg-ico">{ic}</span><div><b>{tx}</b></div></div>'
                      for p, ic, tx, c in filas)
    return (f'<div class="dg c3-split">{mapa}<div class="dg-legend">{leyenda}</div></div>'
            + _call("warn", t["c32_m_warn"], paso=4))


def c32_reglas(lang):
    t = T[lang]
    reglas = [("menu_book", "c32_r1"), ("bookmark", "c32_r2"), ("front_hand", "c32_r3"), ("lock", "c32_r4")]
    fila = "".join(nodo(ic, t[k], t[k + "s"], paso=i + 1) for i, (ic, k) in enumerate(reglas))
    return f'<div class="dg dg-row">{fila}</div>' + _call("tip", t["c32_r_tip"], paso=5)


def c32_medir(lang):
    t = T[lang]

    def fila(etq, estados, chip, paso):
        cajas = "".join(f'<span class="c3-q {"ok" if e else "baja"}"><span class="dg-i">{"check" if e else "remove"}</span></span>'
                        for e in estados)
        return (f'<div class="c3-medida"{_p(paso)}><span class="c3-medida-lab">{etq}</span>'
                f'<div class="c3-qs">{cajas}</div><span class="dg-chip">{chip}</span></div>')
    es = [1, 1, 1, 1, 0, 1, 1, 1]
    en = [1, 0, 1, 0, 0, 1, 1, 0]
    leyenda = ('<div class="dg-row tight c3-medida-ley">'
               f'<span class="c3-q ok"><span class="dg-i">check</span></span>{t["c32_l_ok"]}'
               f'<span class="c3-q baja"><span class="dg-i">remove</span></span>{t["c32_l_baja"]}</div>')
    return ('<div class="dg c3-medidas">' + fila(t["c32_es"], es, t["c32_h_es"], 1)
            + fila(t["c32_en"], en, t["c32_h_en"], 2) + "</div>" + leyenda)


def c32_herramienta(lang):
    t = T[lang]
    agente = _pill("assistant", t["c32_agente"], clase="is-primary")
    casos = [(1, t["c32_c1"], flecha("h"), _resp(t["c32_o1"], icono="chat")),
             (2, t["c32_c2"], flecha("h", t["c32_busca"]), _resp(t["c32_o2"] + ' <span class="c3-nota-pie">¹</span>', clase="ok", icono="check_circle")),
             (3, t["c32_c3"], flecha("h", t["c32_busca"], clase="warn"), _resp(t["c32_o3"], clase="warn", icono="front_hand"))]
    filas = "".join(f'<div class="c3-caso"{_p(p)}><span class="c3-q-chip"><span class="dg-i">chat</span>{q}</span>'
                    f'{flecha("h")}{agente}{fl}{r}</div>' for p, q, fl, r in casos)
    return f'<div class="dg c3-casos">{filas}</div>'


def c32_avance(lang):
    t = T[lang]
    return _avance(t, "v3.2", [("menu_book", t["c32_a1"], t["c32_a1s"]), ("bookmark", t["c32_a2"], t["c32_a2s"]),
                               ("front_hand", t["c32_a3"], t["c32_a3s"])], t["c32_falta"], tipo="warn")


# ------------------------------------------------------------------------------------------
# 3.3 · Agentes profundos
# ------------------------------------------------------------------------------------------
def c33_escritorio(lang):
    t = T[lang]
    papeles = [("c33_p_inst", ""), ("c33_p_rep", ""), ("c33_p_b1", "tenue"), ("c33_p_r1", "tenue"),
               ("c33_p_b2", "tenue"), ("c33_p_r2", "tenue"), ("c33_p_b3", ""), ("c33_p_r3", "")]
    pila = "".join(f'<span class="c3-papel {c}">{t[k]}</span>' for k, c in papeles)
    escritorio = (f'<div class="dg-card c3-escritorio"><h3><span class="dg-i">table</span>{t["c33_escr"]}</h3>'
                  + f'<div class="c3-pila">{pila}<span class="c3-papel desborde">+ …</span></div></div>')
    filas = [(1, "height", "c33_f1"), (2, "visibility_off", "c33_f2"), (3, "swap_vert", "c33_f3")]
    leyenda = "".join(f'<div class="dg-legend-row c3-l-mal" data-paso="{p}"><span class="dg-ico">{ic}</span>'
                      f'<div><b>{t[k]}</b><small>{t[k + "s"]}</small></div></div>' for p, ic, k in filas)
    return f'<div class="dg c3-split">{escritorio}<div class="dg-legend">{leyenda}</div></div>'


def c33_flujo(lang):
    t = T[lang]
    origen = nodo("edit_note", t["c33_plan"], t["c33_plan_sub"], paso=1)
    ramas = []
    for i, k in enumerate(("c33_s1", "c33_s2", "c33_s3"), 1):
        archivo = f'<div class="c3-grupo" data-paso="3">{flecha("h")}{_pill("description", f"s{i}.md")}{flecha("h")}</div>'
        ramas.append((2, flecha("h") + nodo("person", f'{t["c33_sub"]} s{i}', t[k], clase="mini") + archivo))
    destino = nodo("article", t["c33_sint"], t["c33_sint_sub"], clase="is-primary", paso=4)
    return _abanico(origen, ramas, destino) + pie(t["c33_flujo_pie"], paso=5, icono="folder_open")


def c33_escritorios(lang):
    t = T[lang]
    tareas = ("c33_s1", "c33_s2", "c33_s3")
    mesas = ""
    for i, k in enumerate(tareas, 1):
        mesas += (f'<div class="dg-card c3-mesa" data-paso="{i}"><h3><span class="dg-i">person</span>{t["c33_sub"]} s{i}</h3>'
                  f'<small class="dg-card-sub">{t[k]}</small>'
                  f'<span class="c3-mini-lab">{t["c33_recibe"]}</span>'
                  + chips([f'<span class="dg-i">description</span>{t["c33_reporte"]}', f'<span class="dg-i">target</span>{t["c33_su_parte"]}'])
                  + f'<span class="c3-mini-lab">{t["c33_herr"]}</span>'
                  + chips([f'<span class="dg-i">search</span>{t["c33_buscar"]}', f'<span class="dg-i">edit</span>{t["c33_escribir"]}'])
                  + _pill("lock", f'{t["c33_solo"]} <code>s{i}.md</code>', clase="c3-pill-lock") + "</div>")
    return f'<div class="dg c3-mesas">{mesas}</div>' + pie(t["c33_aisla_pie"], paso=4, icono="verified")


def c33_reporte(lang):
    t = T[lang]
    doc = (f'<div class="c3-doc"><h3 data-paso="1"><span class="dg-i">article</span>{t["c33_doc"]}</h3>'
           f'<p class="c3-doc-q" data-paso="1">{t["c31_ticket"]}</p>'
           f'<p data-paso="2">{t["c33_d_causa"]} <span class="c3-nota-pie">¹</span></p>'
           f'<p data-paso="3">{t["c33_d_pasos"]} <span class="c3-nota-pie">²</span></p>'
           f'<p data-paso="4">{t["c33_d_falta"]}</p>'
           f'<p class="c3-doc-notas" data-paso="2">¹ ² <code>conexion-laboratorio.md#…</code></p></div>')
    return _fila(doc, flecha("h", paso=5), nodo("verified", t["c33_check"], t["c33_check_sub"], clase="ok", paso=5), clase="dg")


def c33_topes(lang):
    t = T[lang]
    pares = [("groups", "c33_t1", "block"), ("replay", "c33_t2", "timer"), ("edit", "c33_t3", "lock"),
             ("cancel", "c33_t4", "report"), ("bookmark", "c33_t5", "verified")]
    cols = "".join(f'<div class="dg-col"{_p(i + 1)}>' + nodo(r, t[k], clase="mini warn") + flecha("v")
                   + nodo(p, t[k + "p"], clase="mini ok") + "</div>" for i, (r, k, p) in enumerate(pares))
    return f'<div class="dg c3-topes">{cols}</div>'


def c33_no_es_sandbox(lang):
    t = T[lang]
    mesas = "".join(_pill("person", f"s{i}") for i in (1, 2, 3))
    izq = _card(t["c33_hoy"], f'<div class="c3-proceso"><span class="c3-proceso-lab"><span class="dg-i">terminal</span>{t["c33_programa"]}</span>'
                f'<div class="dg-row tight">{mesas}</div>'
                f'<div class="dg-row tight c3-expuesto" data-paso="2">'
                + _pill("key", t["c33_ve_key"], clase="warn") + _pill("folder_open", t["c33_ve_disco"], clase="warn")
                + "</div></div>" + pie(t["c33_piensa"], icono="insights"),
                paso=1, icono="table")
    bloqueos = "".join(_pill(ic, t[k], clase="bad") for ic, k in
                       (("folder_open", "c33_archivos"), ("public", "c33_internet"), ("terminal", "c33_programas")))
    der = _card(t["c33_cuarto"], cuarto("OpenShell", nodo("assistant", t["c33_agente"], clase="mini is-primary"))
                + f'<div class="dg-row tight">{bloqueos}</div>' + pie(t["c33_toca"], icono="lock"),
                paso=3, clase="is-primary", icono="lock")
    return f'<div class="dg c3-two">{izq}{der}</div>' + _call("tip", t["c33_dos"], paso=4)


def c33_costo(lang):
    t = T[lang]

    def fila(etq, n, extra, cant, paso, clase=""):
        puntos = "".join('<span class="c3-punto"><span class="dg-i">auto_awesome</span></span>' for _ in range(n))
        puntos += "".join('<span class="c3-punto tal-vez"><span class="dg-i">auto_awesome</span></span>' for _ in range(extra))
        return (f'<div class="c3-costo {clase}"{_p(paso)}><span class="c3-medida-lab">{etq}</span>'
                f'<div class="c3-puntos">{puntos}</div><span class="dg-chip">{cant}</span></div>')
    return ('<div class="dg c3-medidas">' + fila(t["c33_rag"], 2, 1, t["c33_rag_n"], 1)
            + fila(t["c33_prof"], 11, 0, t["c33_prof_n"], 2, "caro") + "</div>")


def c33_avance(lang):
    t = T[lang]
    return _avance(t, "v3.3", [("edit_note", t["c33_a1"], t["c33_a1s"]), ("groups", t["c33_a2"], t["c33_a2s"]),
                               ("description", t["c33_a3"], t["c33_a3s"]), ("verified", t["c33_a4"], t["c33_a4s"])],
                   t["c33_mod4"])


# ------------------------------------------------------------------------------------------
# 3.4 · Observabilidad y trazas
# ------------------------------------------------------------------------------------------
def _rastreo(filas, clase=""):
    """Lista tipo «rastreo de paquete»: (ok, texto, tiempo, extra)."""
    out = "".join(f'<li class="{"ok" if ok else "mal"}"><span class="dg-i">{"check_circle" if ok else "cancel"}</span>'
                  f'<span>{tx}{ex}</span><small>{tm}</small></li>' for ok, tx, tm, ex in filas)
    return f'<ul class="c3-rastreo {clase}">{out}</ul>'


def c34_print_vs_traza(lang):
    t = T[lang]
    sueltos = "".join(f'<span class="c3-suelto s{i}">{t[k]}</span>'
                      for i, k in enumerate(("c34_j1", "c34_j2", "c34_j3", "c34_j4", "c34_j5", "c34_j6")))
    izq = _card(t["c34_print"], f'<div class="c3-revuelto">{sueltos}</div>' + pie(t["c34_print_pie"], icono="quiz"),
                paso=1, icono="terminal")
    der = _card(t["c34_traza"], _rastreo([(True, t["c34_r1"], "0 ms", ""), (True, t["c34_r2"], "310 ms", ""),
                                          (False, t["c34_r3"], "503", ""), (True, t["c34_r4"], "952 ms", "")])
                + pie(t["c34_traza_pie"], icono="timeline"), paso=2, clase="is-primary", icono="timeline")
    return f'<div class="dg c3-two">{izq}{der}</div>'


def c34_paquete(lang):
    t = T[lang]
    tag_span = f'<span class="c3-tag" data-paso="2">{t["c34_tag_span"]}</span>'
    paquete = (f'<div class="dg-card" data-paso="1"><h3><span class="dg-i">box</span>{t["c34_paquete"]}'
               f'<span class="c3-tag" data-paso="2">{t["c34_tag_traza"]}</span></h3>'
               + _rastreo([(True, t["c34_pq1"], "9:02", ""), (True, t["c34_pq2"], "14:30", tag_span),
                           (False, t["c34_pq3"], "16:10", ""), (True, t["c34_pq4"], "18:45", "")]) + "</div>")
    filas = [(0, "agente", "agente · soporte", 0, 936, True, None, ""),
             (1, "modelo", "llm · paso 1", 0, 310, True, None, ""),
             (1, "herr", "tool · buscar_faq", 0, 4, True, None, ""),
             (2, "busq", "retriever · buscar_faq", 0, 4, True, None, ""),
             (1, "modelo", "llm · paso 2", 0, 311, True, None, "")]
    agente = (f'<div class="dg-card is-primary" data-paso="3"><h3><span class="dg-i">assistant</span>{t["c34_tu_agente"]}</h3>'
              + _arbol(t, filas, cabecera=False, clase="compacto") + "</div>")
    return (f'<div class="dg c3-paquete">{paquete}<div class="dg-arrow h" data-paso="3"></div>{agente}</div>'
            + pie(t["c34_paquete_pie"], paso=4, icono="insights"))


def c34_tipos(lang):
    t = T[lang]
    datos = [("auto_awesome", "k_modelo", "c34_m_sub", ("c34_mensajes", "c34_tokens", "c34_paro"), "k-modelo"),
             ("settings", "k_herr", "c34_h_sub", ("c34_args", "c34_salida", "c34_error"), "k-herr"),
             ("search", "k_busq", "c34_b_sub", ("c34_docs", "c34_puntaje"), "k-busq")]
    fila = "".join(nodo(ic, t[k], t[s], clase=f"c3-tipo {c}", paso=i + 1, extra=chips([t[x] for x in xs]))
                   for i, (ic, k, s, xs, c) in enumerate(datos))
    return f'<div class="dg dg-row">{fila}</div>' + pie(t["c34_tipos_pie"], paso=4, icono="label")


def c34_tachar(lang):
    t = T[lang]
    antes = f'<span class="c3-texto">{t["c34_texto"]}</span>'
    despues = f'<span class="c3-texto">{t["c34_guardado"]}<span class="c3-tachon">AbCd…</span></span>'
    return (_fila(nodo("chat", t["c34_llega"], extra=antes, clase="warn", paso=1), flecha("h", paso=2),
                  nodo("brush", t["c34_redactar"], t["c34_redactar_sub"], clase="is-primary", paso=2), flecha("h", paso=3),
                  nodo("check_circle", t["c34_guarda"], extra=despues, clase="ok", paso=3), flecha("h", paso=4),
                  nodo("storage", t["c34_destino"], t["c34_destino_sub"], paso=4), clase="dg c3-tachar")
            + pie(t["c34_tachar_pie"], paso=5, icono="warning"))


def c34_arbol(lang):
    t = T[lang]
    filas = [(0, "agente", "agente · soporte", 0, 936, True, 1, ""),
             (1, "modelo", "llm · paso 1", 0, 310, True, 2, ""),
             (1, "herr", "tool · estado_laboratorio", 310, 0, True, 2, ""),
             (1, "modelo", "llm · paso 2", 311, 311, True, 3, ""),
             (1, "herr", "tool · buscar_faq", 622, 4, True, 3, ""),
             (2, "busq", "retriever · buscar_faq", 622, 4, True, 3, "conexion-laboratorio.md · 0.408"),
             (1, "modelo", "llm · paso 3", 625, 311, True, 4, "")]
    return f'<div class="dg">{_arbol(t, filas, total=936)}</div>'


def c34_cuatro_bugs(lang):
    t = T[lang]
    v1 = ('<div class="c3-mini-span mal"><span class="dg-i">cancel</span><code>tool · estado_laboratorio</code></div>'
          '<code class="c3-err">503 Service Unavailable</code>')
    v2 = ('<div class="c3-repite">' + "".join(f'<code>{t["c34_factura"]}</code>' for _ in range(3))
          + '<span class="dg-chip">× 5</span></div>')
    v3 = '<code class="c3-err">[brev.md#la-gpu-es-gratis-para-siempre]</code>'
    v4 = ('<div class="c3-barras mini">'
          f'<div class="c3-bar-fila modelo"><span class="c3-bar-lab">{t["k_modelo"]}</span><div class="c3-bar-pista">'
          '<span class="c3-bar" style="width:14%"></span><b>0.3 s</b></div></div>'
          f'<div class="c3-bar-fila lento"><span class="c3-bar-lab">{t["k_herr"]}</span><div class="c3-bar-pista">'
          '<span class="c3-bar" style="width:70%"></span><b>1.5 s</b></div></div></div>')
    bugs = [("error", "c34_bug1", v1), ("replay", "c34_bug2", v2), ("bookmark", "c34_bug3", v3), ("timer", "c34_bug4", v4)]
    cards = "".join(f'<div class="dg-card c3-bug"{_p(i + 1)}><h3><span class="dg-i">{ic}</span>{t[k]}</h3>{v}'
                    f'<small class="c3-bug-v"><span class="dg-i">visibility</span>{t[k + "_v"]}</small></div>'
                    for i, (ic, k, v) in enumerate(bugs))
    return f'<div class="dg c3-bugs">{cards}</div>'


def c34_error_ok(lang):
    t = T[lang]
    filas = [(0, "agente", "agente · soporte", 0, 952, True, None, ""),
             (1, "modelo", "llm · paso 1", 0, 310, True, None, ""),
             (1, "herr", "tool · estado_laboratorio", 0, 1, False, None, "503 Service Unavailable"),
             (1, "modelo", "llm · paso 2", 0, 312, True, None, ""),
             (1, "herr", "tool · buscar_faq", 0, 4, True, None, ""),
             (2, "busq", "retriever · buscar_faq", 0, 4, True, None, ""),
             (1, "modelo", "llm · paso 3", 0, 318, True, None, "")]
    arbol = f'<div class="dg-card">{_arbol(t, filas, cabecera=False, clase="compacto")}</div>'
    leyenda = (f'<div class="dg-legend-row c3-l-mal" data-paso="1"><span class="dg-ico">cancel</span>'
               f'<div><b>{t["c34_e1"]}</b><small>{t["c34_e1s"]}</small></div></div>'
               f'<div class="dg-legend-row is-primary" data-paso="2"><span class="dg-ico">check_circle</span>'
               f'<div><b>{t["c34_e2"]}</b><small>{t["c34_e2s"]}</small></div></div>'
               f'<div class="dg-legend-row is-primary" data-paso="3"><span class="dg-ico">chat</span>'
               f'<div><b>{t["c34_e3"]}</b><small>{t["c34_e3s"]}</small></div></div>')
    return f'<div class="dg c3-split">{arbol}<div class="dg-legend">{leyenda}</div></div>'


def c34_nvidia(lang):
    t = T[lang]
    capa1 = (nodo("tune", "NeMo Agent Toolkit", t["c34_nat_sub"], clase="is-primary") + flecha("h", t["c34_trazas"])
             + nodo("insights", "Phoenix", t["c34_phoenix_sub"], clase="ok", extra=chips([t["c34_otras"]])))
    capa2 = (cuarto(t["c34_sandbox"], nodo("assistant", t["c34_agente"], clase="mini")) + flecha("h")
             + nodo("history", t["c34_regs"], t["c34_regs_sub"],
                    extra=chips([t["c34_msgs"], t["c34_bloq"], t["c34_conv"]])))
    return ('<div class="dg c3-carriles libre">' + _carril(t["c34_capa1"], "code", capa1, paso=1)
            + _carril(t["c34_capa2"], "lock", capa2, paso=2) + "</div>" + pie(t["c34_nv_pie"], paso=3, icono="verified"))


def c34_avance(lang):
    t = T[lang]
    return _avance(t, "v3.4", [("timeline", t["c34_a1"], t["c34_a1s"]), ("verified", t["c34_a2"], t["c34_a2s"]),
                               ("brush", t["c34_a3"], t["c34_a3s"])], t["c34_mod4"])


DIAGRAMAS = {
    # 3.1
    "c31-loop-vs-flujo": c31_loop_vs_flujo,
    "c31-patrones": c31_patrones,
    "c31-router": c31_router,
    "c31-etiqueta": c31_etiqueta,
    "c31-rewoo": c31_rewoo,
    "c31-fanout": c31_fanout,
    "c31-tiempo": c31_tiempo,
    "c31-dividir": c31_dividir,
    "c31-avance": c31_avance,
    # 3.2
    "c32-libro-abierto": c32_libro_abierto,
    "c32-pipeline": c32_pipeline,
    "c32-tarjetas": c32_tarjetas,
    "c32-mapa": c32_mapa,
    "c32-reglas": c32_reglas,
    "c32-medir": c32_medir,
    "c32-herramienta": c32_herramienta,
    "c32-avance": c32_avance,
    # 3.3
    "c33-escritorio": c33_escritorio,
    "c33-flujo": c33_flujo,
    "c33-escritorios": c33_escritorios,
    "c33-reporte": c33_reporte,
    "c33-topes": c33_topes,
    "c33-no-es-sandbox": c33_no_es_sandbox,
    "c33-costo": c33_costo,
    "c33-avance": c33_avance,
    # 3.4
    "c34-print-vs-traza": c34_print_vs_traza,
    "c34-paquete": c34_paquete,
    "c34-tipos": c34_tipos,
    "c34-tachar": c34_tachar,
    "c34-arbol": c34_arbol,
    "c34-cuatro-bugs": c34_cuatro_bugs,
    "c34-error-ok": c34_error_ok,
    "c34-nvidia": c34_nvidia,
    "c34-avance": c34_avance,
}
