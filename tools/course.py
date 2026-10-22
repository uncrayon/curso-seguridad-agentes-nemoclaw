"""Fuente única de verdad del curso: módulos, clases, slugs y textos de enlace entre clases.

La usan:
  - tools/build_slides.py   -> diapositivas de apertura ("La clase pasada aprendimos")
                               y de cierre ("En la próxima clase aprenderemos")
  - tools/build_home.py     -> la portada del curso (index.html)
  - tools/notebooks/*.py    -> encabezados de los notebooks

Si cambias un título o un aprendizaje aquí, vuelve a correr:  python3 tools/build_all.py
"""

COURSE = {
    "title": "Seguridad de agentes con OpenShell y NemoClaw",
    "subtitle": "De una sola llamada a un modelo hasta un agente siempre activo, con skills y dentro de un sandbox.",
    "partner": "Platzi × NVIDIA Deep Learning Institute",
    "instructor": "Ulises Rayón",
    "nvidia_repo": "https://github.com/NVDLI/NemoClawDLI",
    "nemoclaw_repo": "https://github.com/NVIDIA/NemoClaw",
    "nemoclaw_docs": "https://docs.nvidia.com/nemoclaw/latest/",
    "brev": "https://brev.nvidia.com/",
    "launchable": "https://brev.nvidia.com/launchable/deploy/now?launchableID=env-3Azt0aYgVNFEuz7opyx3gscmowS&ncid=ref-dli-759990",
    "build": "https://build.nvidia.com/?ncid=ref-dli-146986",
    # Repo público en GitHub ("org/nombre"). Cuando exista, ponlo aquí y vuelve a construir:
    # los notebooks ganan el botón "Abrir en Colab" y la portada enlaza al repo.
    "github": "uncrayon/curso-seguridad-agentes-nemoclaw",
    "sitio": "https://uncrayon.github.io/curso-seguridad-agentes-nemoclaw/",
}

MODULES = [
    {"n": 1, "title": "Prepara tu entorno de agentes",
     "outcome": "Entiendes el stack y dejas listo tu acceso a modelos de NVIDIA.", "where": "Navegador + notebook"},
    {"n": 2, "title": "Construye el loop básico del agente",
     "outcome": "Construyes un loop de agente desde cero, con ReAct y herramientas.", "where": "Notebooks"},
    {"n": 3, "title": "Coordina, fundamenta y planea",
     "outcome": "Diseñas sistemas con enrutamiento, RAG sobre tus fuentes y subagentes.", "where": "Notebooks"},
    {"n": 4, "title": "Lleva tu agente a NemoClaw",
     "outcome": "Despliegas un agente real en Brev y lo operas de forma continua.", "where": "Laboratorio en Brev"},
    {"n": 5, "title": "Asegura el agente con OpenShell",
     "outcome": "Contienes al agente con identidad, sandbox y políticas verificables.", "where": "Laboratorio en Brev + notebook"},
    {"n": 6, "title": "Amplía tu práctica con agentes",
     "outcome": "Comparas herramientas, construyes tu biblioteca de skills y sabes cómo seguir.", "where": "Laboratorio en Brev + notebook"},
]

# Cada clase:
#   aprendimos: 3-4 frases cortas con lo que el estudiante YA sabe hacer al terminar la clase.
#               Se muestran al inicio de la clase siguiente ("La clase pasada aprendimos").
#   promesa:    3 frases con lo que la clase va a enseñar.
#               Se muestran al final de la clase anterior ("En la próxima clase aprenderemos").
#   practica:   "notebook" | "lab" (cookbook en Brev) | "slides" | "navegador"
#   nvidia:     archivo de la lección de NVIDIA DLI en la que se basa la clase (solo para el crédito en texto;
#               no se enlaza a las páginas de NVIDIA), o None si la clase no tiene lección equivalente;
#               en ese caso "ref" = (etiqueta, url) apunta a la documentación de referencia.
CLASSES = [
    # ------------------------------------------------------------------ Módulo 1
    {"id": "1.1", "module": 1, "slug": "1.1-que-son-nemoclaw-openclaw-openshell",
     "title": "Qué son NemoClaw, OpenClaw y OpenShell", "minutes": 6, "practica": "navegador",
     "nvidia": "index.html", "skill": None,
     "promesa": ["Qué es un agente de IA, sin tecnicismos",
                 "Qué hace cada pieza: OpenClaw, OpenShell y NemoClaw",
                 "Qué vas a construir en el curso y qué necesitas"],
     "aprendimos": ["Un agente es un modelo dentro de un loop, con herramientas y memoria",
                    "OpenClaw es el agente; OpenShell, el sandbox; NemoClaw, el blueprint que los une",
                    "El curso va de un loop en Python a un agente real dentro de un sandbox en Brev"]},
    {"id": "1.2", "module": 1, "slug": "1.2-cuenta-y-api-key-nvidia-build",
     "title": "Crea tu cuenta y tu API key en NVIDIA Build", "minutes": 6, "practica": "navegador",
     "nvidia": "index.html", "skill": "Administrar el consumo de API en NVIDIA Build",
     "promesa": ["Crear tu cuenta gratuita en build.nvidia.com",
                 "Generar tu API key nvapi- y guardarla sin exponerla",
                 "Hacer tu primera llamada a un modelo y cuidar tus créditos"],
     "aprendimos": ["Tienes una cuenta en NVIDIA Build y una API key nvapi-",
                    "La key vive en una variable de entorno o un .env, nunca en el código",
                    "Hiciste tu primera llamada con curl y conoces los límites de la cuenta gratuita"]},
    {"id": "1.3", "module": 1, "slug": "1.3-rutas-de-modelo-y-errores",
     "title": "Configura rutas de modelo y diagnostica errores", "minutes": 7, "practica": "notebook",
     "nvidia": "index.html", "skill": "Configurar rutas de modelo; diagnosticar errores 401, 403, 404, 429 y 5xx",
     "promesa": ["Configurar las rutas de chat y embeddings que usa todo el curso",
                 "Usar el panel del curso de NVIDIA y el notebook de verificación",
                 "Leer y resolver los errores 401, 403, 404, 410, 429 y 5xx"],
     "aprendimos": ["Configuraste las rutas de chat y de embeddings",
                    "Tu notebook de verificación pasa en verde (o sabes por qué no)",
                    "Sabes qué significa cada error de la API y qué hacer con él"]},
    # ------------------------------------------------------------------ Módulo 2
    {"id": "2.1", "module": 2, "slug": "2.1-loop-de-agente",
     "title": "De una sola llamada al loop de agente", "minutes": 9, "practica": "notebook",
     "nvidia": "01a-loop.html", "skill": "Construir un loop básico de agente",
     "promesa": ["Qué separa una llamada a un modelo de un agente",
                 "El ciclo observar → decidir → actuar y su condición de parada",
                 "Por qué el modelo no tiene memoria y cómo se la damos"],
     "aprendimos": ["Un agente es un loop: observar → decidir → actuar → ¿parar?",
                    "La función de decisión puede ser código, búsqueda o un LLM; el loop no cambia",
                    "La memoria es la lista messages que reenvías en cada llamada"]},
    {"id": "2.2", "module": 2, "slug": "2.2-patron-react",
     "title": "Razonamiento con el patrón ReAct", "minutes": 9, "practica": "notebook",
     "nvidia": "01b-react.html", "skill": "Implementar el patrón ReAct",
     "promesa": ["El patrón ReAct: razonar, actuar, observar y repetir",
                 "Cómo finish_reason le dice al loop qué hacer",
                 "Construir un loop ReAct desde cero con una herramienta"],
     "aprendimos": ["ReAct alterna razonamiento y acciones hasta tener una respuesta",
                    "finish_reason decide: stop, tool_calls o length",
                    "Cada tool_call se valida, se ejecuta y su resultado vuelve como mensaje tool"]},
    {"id": "2.3", "module": 2, "slug": "2.3-funciones-a-herramientas",
     "title": "Convierte funciones en herramientas", "minutes": 9, "practica": "notebook",
     "nvidia": "01c-tools.html", "skill": "Convertir funciones en herramientas de agente",
     "promesa": ["El contrato entre el modelo y una herramienta",
                 "Cómo escribir descripciones que el modelo entiende",
                 "Validar argumentos y devolver errores como observaciones"],
     "aprendimos": ["Una herramienta es un contrato: nombre, descripción, esquema y resultado en texto",
                    "La descripción decide cuándo el modelo la usa",
                    "Los argumentos se validan antes de ejecutar y los errores vuelven al modelo"]},
    # ------------------------------------------------------------------ Módulo 3
    {"id": "3.1", "module": 3, "slug": "3.1-enrutamiento-y-workflows",
     "title": "Enruta trabajo entre varias llamadas", "minutes": 9, "practica": "notebook",
     "nvidia": "02a-routing.html", "skill": "Enrutar subtareas entre llamadas a modelos",
     "promesa": ["Cuándo un solo loop no alcanza",
                 "Un router de triage con un enum fijo",
                 "ReWOO y fan-out: planear, ejecutar en paralelo y unir"],
     "aprendimos": ["Un router clasifica con un enum cerrado y nunca adivina",
                    "ReWOO planea primero y ejecuta los pasos en paralelo",
                    "Cada rama necesita un plan para cuando falla"]},
    {"id": "3.2", "module": 3, "slug": "3.2-rag",
     "title": "RAG para fundamentar en tus fuentes", "minutes": 9, "practica": "notebook",
     "nvidia": "02b-rag.html", "skill": "Implementar RAG con tus propias fuentes",
     "promesa": ["Indexar documentos con embeddings",
                 "Recuperar los fragmentos relevantes y citarlos",
                 "Convertir la búsqueda en una herramienta del agente"],
     "aprendimos": ["RAG = indexar, recuperar y generar con los fragmentos citados",
                    "Los embeddings se piden con input_type query o passage",
                    "La recuperación es una herramienta más que el agente decide usar"]},
    {"id": "3.3", "module": 3, "slug": "3.3-agentes-profundos",
     "title": "Agentes profundos que crean subagentes", "minutes": 9, "practica": "notebook",
     "nvidia": "02c-deep.html", "skill": "Coordinar subagentes con un planificador",
     "promesa": ["Planificadores que dividen una tarea grande",
                 "Subagentes con contexto aislado que escriben en archivos",
                 "La diferencia entre aislar contexto y aislar el sistema operativo"],
     "aprendimos": ["Un planificador divide la tarea y lanza subagentes",
                    "Cada subagente tiene su propio contexto y deja su trabajo en archivos",
                    "Aislar contexto no es lo mismo que un sandbox: eso llega con OpenShell"]},
    # ------------------------------------------------------------------ Módulo 4
    {"id": "4.1", "module": 4, "slug": "4.1-laboratorio-nemoclaw-en-brev",
     "title": "Levanta el laboratorio NemoClaw en Brev", "minutes": 9, "practica": "lab",
     "nvidia": "03a-kickstart.html", "skill": "Desplegar NemoClaw en Brev",
     "promesa": ["Lanzar el launchable de NemoClaw en Brev con tu cupón",
                 "Configurar tu agente desde el navegador y abrir su tablero",
                 "Cuidar tu crédito: cuánto cuesta y cuándo usar Stop o Delete"],
     "aprendimos": ["Tu laboratorio NemoClaw corre en Brev y lo abres con el botón NemoClaw",
                    "Configuraste tu agente en el navegador y conoces los 4 botones del tablero",
                    "Sabes cuánto cuesta (≈0.25 USD/h) y cuándo usar Stop o Delete"]},
    {"id": "4.2", "module": 4, "slug": "4.2-gateway-y-workspace-openclaw",
     "title": "Explora el gateway y el workspace de OpenClaw", "minutes": 8, "practica": "lab",
     "nvidia": "03b-openclaw.html", "skill": None,
     "promesa": ["Las piezas de OpenClaw: gateway, sesiones y workspace",
                 "Los archivos que definen al agente: SOUL.md, AGENTS.md, MEMORY.md",
                 "Verificar como operador lo que el agente dice que hizo"],
     "aprendimos": ["El gateway recibe los turnos y guarda las sesiones",
                    "El workspace es el contexto del agente: SOUL.md, AGENTS.md, MEMORY.md, skills/",
                    "Como operador, siempre verificas lo que el agente afirma"]},
    {"id": "4.3", "module": 4, "slug": "4.3-agentes-siempre-activos",
     "title": "Agentes en operación continua y programada", "minutes": 8, "practica": "lab",
     "nvidia": "03c-always-on.html", "skill": "Operar agentes en modo continuo",
     "promesa": ["Instalar una skill y hacer que el agente la use",
                 "Programar una tarea que corre sin que nadie escriba en el chat",
                 "Los 3 controles: sesión, directiva y disparador"],
     "aprendimos": ["Instalaste una skill (SKILL.md) y el agente la usó",
                    "Programaste una automatización que escribió un archivo sin que nadie usara el chat",
                    "Un agente siempre activo = sesión + directiva + disparador"]},
    {"id": "4.4", "module": 4, "slug": "4.4-hermes-en-nemoclaw", "opcional": True,
     "title": "Cambia OpenClaw por Hermes en NemoClaw", "minutes": 9, "practica": "lab",
     "nvidia": None,
     "ref": ("NemoClaw · Hermes", "https://docs.nvidia.com/nemoclaw/latest/user-guide/hermes/get-started/quickstart"),
     "skill": "Desplegar y operar Hermes Agent en NemoClaw",
     "promesa": ["Crear un sandbox con Hermes Agent en lugar de OpenClaw",
                 "Dónde viven su personalidad, memoria, skills y sesiones",
                 "Llevar tu skill soporte-nemoclaw a Hermes y llamarlo por su API compatible con OpenAI"],
     "aprendimos": ["NemoClaw es el mismo sandbox para OpenClaw o Hermes: cambia el agente, no la seguridad",
                    "Hermes guarda todo en /sandbox/.hermes: config, memoria, skills y sesiones en state.db",
                    "Tu skill funciona en los dos agentes y llamas a Hermes desde un programa con su API compatible con OpenAI"]},
    # ------------------------------------------------------------------ Módulo 5
    {"id": "5.1", "module": 5, "slug": "5.1-trifecta-letal",
     "title": "La trifecta letal y la superficie de riesgo", "minutes": 8, "practica": "slides",
     "nvidia": "04a-safety.html", "skill": None,
     "promesa": ["Por qué un agente autónomo es riesgoso por diseño",
                 "La trifecta letal: datos privados, contenido no confiable y salida al exterior",
                 "Las 3 capas de defensa: prompt, harness y sandbox"],
     "aprendimos": ["Trifecta letal = datos privados + contenido no confiable + comunicación externa",
                    "Una instrucción inyectada puede desviar a un agente con herramientas",
                    "Defensa en capas: prompt → harness → sandbox"]},
    {"id": "5.2", "module": 5, "slug": "5.2-identidades-openshell",
     "title": "Identidades y límites con OpenShell", "minutes": 9, "practica": "lab",
     "nvidia": "04a-safety.html", "skill": "Configurar identidades de agente en OpenShell",
     "promesa": ["Quién es el agente dentro del sandbox",
                 "Cómo OpenShell decide permisos por binario e identidad",
                 "Mínimo privilegio en la práctica: usuario no-root y syscalls bloqueadas"],
     "aprendimos": ["El agente corre como un usuario sin privilegios dentro del sandbox",
                    "OpenShell otorga permisos por binario e identidad, no por nombre",
                    "Las credenciales reales nunca entran al sandbox"]},
    {"id": "5.3", "module": 5, "slug": "5.3-sandbox-y-politicas",
     "title": "Restringe herramientas, archivos y red", "minutes": 9, "practica": "lab",
     "nvidia": "04a-safety.html", "skill": "Definir y verificar un sandbox en OpenShell",
     "promesa": ["Leer la política real de tu sandbox",
                 "Predecir y comprobar qué se permite y qué se bloquea",
                 "Por qué el aislamiento es una capa y no la solución completa"],
     "aprendimos": ["Leíste la política real del sandbox y la entendiste",
                    "Predijiste y comprobaste bloqueos de red y archivos",
                    "Un comando permitido todavía puede filtrar un secreto: el sandbox es una capa"]},
    # ------------------------------------------------------------------ Módulo 6
    {"id": "6.1", "module": 6, "slug": "6.1-clis-de-agentes", "opcional": True,
     "title": "Compara CLIs de agentes modernos", "minutes": 8, "practica": "lab",
     "nvidia": "04b-modern-clis.html", "skill": None,
     "promesa": ["Claude Code, Codex, Cursor, Hermes, Deep Agents y OpenClaw lado a lado",
                 "Los ejes que importan: archivos, red, identidad y persistencia",
                 "Cómo elegir según la tarea y el riesgo"],
     "aprendimos": ["Los agentes de CLI comparten el mismo loop con distintos defaults",
                    "Se comparan por archivos, red, identidad y persistencia",
                    "Elegir herramienta es elegir qué riesgo aceptas"]},
    {"id": "6.2", "module": 6, "slug": "6.2-biblioteca-de-skills", "opcional": True,
     "title": "Construye tu biblioteca de skills", "minutes": 9, "practica": "notebook",
     "nvidia": "03c-always-on.html", "skill": "Crear skills de agente reutilizables",
     "promesa": ["Anatomía de una skill: SKILL.md con frontmatter y runbook",
                 "Selección explícita vs. automática",
                 "Empezar tu propia biblioteca y llevarla al laboratorio"],
     "aprendimos": ["Una skill es una carpeta con SKILL.md: nombre, descripción y runbook",
                    "La descripción decide si el agente la descubre solo",
                    "Tu biblioteca de skills viaja contigo entre sesiones y agentes"]},
    {"id": "6.3", "module": 6, "slug": "6.3-despliegue-local-y-siguientes-pasos", "opcional": True,
     "title": "Próximos pasos y despliegue local", "minutes": 8, "practica": "slides",
     "nvidia": "04c-going-further.html", "skill": None,
     "promesa": ["Qué necesitas para correr NemoClaw en tu propia máquina",
                 "Rutas de producción: NIM, NeMo Guardrails, NeMo Retriever",
                 "Cómo seguir aprendiendo y cerrar tu proyecto"],
     "aprendimos": ["Sabes qué requisitos tiene un despliegue local",
                    "Conoces las piezas de producción de NVIDIA",
                    "Tienes un proyecto terminado y un camino para seguir"]},
]


def by_id(cid):
    return next(c for c in CLASSES if c["id"] == cid)


def neighbors(cid):
    i = [c["id"] for c in CLASSES].index(cid)
    prev = CLASSES[i - 1] if i > 0 else None
    nxt = CLASSES[i + 1] if i + 1 < len(CLASSES) else None
    return prev, nxt


def module(n):
    return MODULES[n - 1]
