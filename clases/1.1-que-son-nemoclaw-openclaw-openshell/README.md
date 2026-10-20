# 1.1 · Qué son NemoClaw, OpenClaw y OpenShell

Objetivo: entender qué es un agente y qué hace cada pieza del stack antes de tocar código.

| | |
|---|---|
| **Duración del video** | ≈6 min |
| **Práctica** | Guiada en el navegador (sin código, ≈20 min) |
| **Habilidad** | Ubicar cada pieza del stack: OpenClaw, OpenShell y NemoClaw |
| **Lección de NVIDIA** | [Inicio del curso](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/index.html) |
| **Material** | [Diapositivas](slides.html) · [Preguntas frecuentes](../../FAQ.md) |

## Lo esencial (sin tecnicismos)

**La idea:** un agente es un asistente de inteligencia artificial que no solo contesta: también hace cosas por ti, paso a paso, hasta terminar una tarea. Por eso hay que cuidarlo. OpenClaw es el asistente, OpenShell es el cuarto cerrado donde trabaja y NemoClaw es el kit que arma todo.

**Piénsalo como:** contratar a un asistente y sentarlo en un cuarto con cerradura, ventanas con rejas y un guardia que revisa lo que entra y sale.

**Palabras nuevas:** [modelo](../../GLOSARIO.md), [agente](../../GLOSARIO.md), [sandbox](../../GLOSARIO.md).

**Hazlo sin programar (≈10 min):** clasifica estos cinco ejemplos como **agente** o **solo modelo** (un modelo contesta; un agente además actúa y repite pasos):

1. Le preguntas a un chat cuál es la capital de Perú y te responde.
2. Un asistente revisa tu correo cada hora, encuentra las facturas y las guarda en una carpeta.
3. Pides que te resuman un texto que pegaste.
4. Un asistente busca vuelos, compara precios y te escribe cuál conviene, sin que le digas cada paso.
5. Un asistente lee una página web y, si encuentra un error en tu agenda, lo corrige solo.

Después, completa en una hoja estas tres frases con tus palabras: "OpenClaw es ___", "OpenShell es ___", "NemoClaw es ___". Por último, abre la [portada del curso de NVIDIA en español](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/index.html) y busca, solo leyendo, la sección "Dónde se ejecuta el curso". Respuestas: 2, 4 y 5 son agentes; 1 y 3, solo modelo.

**Qué te llevas:** puedes explicarle a cualquiera qué es un agente, por qué hay que encerrarlo y qué papel tiene cada pieza.

## Lo que vas a lograr

- Explicar con tus palabras qué es un agente de IA: un modelo dentro de un loop, con herramientas y memoria.
- Distinguir OpenClaw (el agente), OpenShell (el sandbox y el gateway) y NemoClaw (el blueprint y la CLI que los une).
- Saber qué vas a construir en las 20 clases y qué necesitas para cada módulo.

## Antes de empezar

- Un navegador de escritorio (Chrome, Edge o Firefox). Desde el Módulo 4 lo vas a necesitar con herramientas de desarrollador, así que no uses el celular para este curso.
- Nada más. No hace falta cuenta, GPU ni instalar nada en esta clase.

## Las ideas clave

### Qué es un agente

Un **modelo de lenguaje** (LLM) por sí solo recibe texto y devuelve texto. Un **agente** es ese modelo puesto dentro de un **loop** (un ciclo que se repite):

1. **Observa**: lee la petición y lo que ha pasado hasta ahora (su memoria).
2. **Decide**: el modelo elige el siguiente paso: responder o usar una herramienta (una *tool*, una función que tu código ejecuta por él).
3. **Actúa**: tu código ejecuta la herramienta y le devuelve el resultado.
4. **¿Para?**: si ya terminó, responde; si no, vuelve al paso 1.

El problema: un agente con herramientas puede leer archivos, ejecutar comandos y conectarse a internet. Si alguien lo engaña con una instrucción escondida en un documento, puede hacer daño real. Por eso este curso trata de **seguridad de agentes**.

### Las tres piezas

Las definiciones vienen de la [documentación de NemoClaw](https://docs.nvidia.com/nemoclaw/latest/) (página *Ecosystem*):

| Pieza | Qué es | Analogía |
|---|---|---|
| **OpenClaw** | El agente: el asistente con su runtime, herramientas, memoria y comportamiento, dentro del contenedor. Es un proyecto de terceros ([openclaw.ai](https://openclaw.ai)). No define el sandbox. | El empleado |
| **OpenShell** | El entorno de ejecución de NVIDIA: crea y vigila el **sandbox** (un contenedor aislado), aplica las políticas de red, archivos y procesos, y enruta la inferencia (las llamadas al modelo). Tiene un **gateway** en el host y la CLI `openshell`. | La oficina con cerraduras y un guardia en la puerta |
| **NemoClaw** | La pila de referencia de NVIDIA: la CLI `nemoclaw`, un **blueprint versionado** (un paquete YAML con las versiones exactas, la imagen y las políticas) y un plugin para OpenClaw. Prepara y opera todo lo anterior. | El contratista que monta la oficina y contrata al empleado |

Tres cosas que se confunden seguido:

- **NemoClaw no es un modelo.** Los modelos (Nemotron, por ejemplo) viven en build.nvidia.com y se llaman por API.
- **OpenShell sirve sin NemoClaw.** NemoClaw agrega encima una política más estricta, una imagen endurecida y verificación del blueprint.
- **Tu API key nunca entra al sandbox.** OpenShell la guarda afuera y la inyecta en la salida hacia el modelo.

### El flujo, en texto

```text
Tú (operador)
  │  nemoclaw onboard · nemoclaw <nombre> connect · nemoclaw <nombre> status
  ▼
nemoclaw (CLI en el host) ──── lee el blueprint versionado (YAML con versiones fijas)
  │  llama a la CLI openshell
  ▼
Gateway de OpenShell (host) ── políticas · rutas de inferencia · credenciales
  │  crea y vigila
  ▼
Sandbox (contenedor, usuario "sandbox"; solo /sandbox y /tmp se pueden escribir)
  └── OpenClaw (el agente) + plugin de NemoClaw
        │ quiere hablar con el modelo        │ quiere salir a internet
        ▼                                     ▼
  ruta de inferencia → build.nvidia.com   política de red: todo bloqueado
  (la key se agrega afuera del sandbox)    salvo lo que esté en la lista
```

### Qué vas a construir: el proyecto "Soporte NemoClaw"

A lo largo del curso construyes **Soporte NemoClaw**, un agente que responde dudas de estudiantes sobre NemoClaw, Brev y el propio curso, usando la FAQ del curso como base de conocimiento. Crece clase a clase:

| Módulo | Qué le agregas |
|---|---|
| 2 | Un loop de chat con memoria, el patrón ReAct y herramientas reales (`buscar_faq`, `estimar_costo_brev`) |
| 3 | Un router de triage, RAG sobre la FAQ con citas y subagentes que arman un reporte de diagnóstico |
| 4 | Lo despliegas en OpenClaw como skill dentro del laboratorio en Brev, con una tarea programada |
| 5 | Analizas sus riesgos y escribes la política de su sandbox |
| 6 | Armas tu biblioteca de skills y ves cómo correrlo en tu máquina |

### El mapa de las 20 clases

| Módulo | Clase | Práctica | Lección de NVIDIA |
|---|---|---|---|
| **1 · Prepara tu entorno** | 1.1 Qué son NemoClaw, OpenClaw y OpenShell | Navegador | Inicio |
| | 1.2 Crea tu cuenta y tu API key en NVIDIA Build | Navegador | Inicio |
| | 1.3 Configura rutas de modelo y diagnostica errores | Notebook | Inicio |
| **2 · El loop básico** | 2.1 De una sola llamada al loop de agente | Notebook | 1a Bucle |
| | 2.2 Razonamiento con el patrón ReAct | Notebook | 1b ReAct |
| | 2.3 Convierte funciones en herramientas | Notebook | 1c Herramientas |
| **3 · Coordina, fundamenta y planea** | 3.1 Enruta trabajo entre varias llamadas | Notebook | 2a Flujos de trabajo |
| | 3.2 RAG para fundamentar en tus fuentes | Notebook | 2b RAG |
| | 3.3 Agentes profundos que crean subagentes | Notebook | 2c Agentes profundos |
| | 3.4 Observa y depura tu agente con trazas | Notebook | (nueva) |
| **4 · Lleva tu agente a NemoClaw** | 4.1 Levanta el laboratorio NemoClaw en Brev | Laboratorio | 3a Conexión inicial |
| | 4.2 Explora el gateway y el workspace de OpenClaw | Laboratorio | 3b OpenClaw |
| | 4.3 Agentes en operación continua y programada | Laboratorio | 3c Operación continua |
| | 4.4 Cambia OpenClaw por Hermes en NemoClaw | Laboratorio | (nueva) |
| **5 · Asegura el agente con OpenShell** | 5.1 La trifecta letal y la superficie de riesgo | Diapositivas | 4a OpenShell |
| | 5.2 Identidades y límites con OpenShell | Laboratorio | 4a OpenShell |
| | 5.3 Restringe herramientas, archivos y red | Laboratorio | 4a OpenShell |
| **6 · Amplía tu práctica** | 6.1 Compara CLIs de agentes modernos | Laboratorio | 4b CLI modernos |
| | 6.2 Construye tu biblioteca de skills | Notebook | 3c Operación continua |
| | 6.3 Próximos pasos y despliegue local | Diapositivas | 4c Siguientes pasos |

Qué necesitas en cada etapa:

- **Módulos 1 a 3**: una API key gratuita de NVIDIA Build y Python (Colab o tu máquina). No necesitas GPU.
- **Módulos 4 a 6**: una cuenta de [Brev](https://brev.nvidia.com/) para levantar el laboratorio (una máquina en la nube con NemoClaw ya instalado) y un navegador de escritorio.

## Paso a paso (práctica guiada en el navegador)

### 1. Recorre la portada del curso de NVIDIA en español

1. Abre <https://nvdli.github.io/NemoClawDLI/es/nemoclaw/index.html>.
2. Si la ves en inglés, usa el menú de idioma de la página y elige español.
3. Ubica la sección **"Dónde se ejecuta el curso"**. Deberías ver tres tarjetas:
   - **Modelos · build.nvidia.com**: los modelos Nemotron que llamas con tu key `nvapi-`.
   - **Stack de agentes · Launchable de NemoClaw en Brev**: el laboratorio de los módulos 4 a 6 de nuestro curso.
   - **Búsqueda · Catálogo de materiales**: el glosario y los artículos del curso.
4. Baja a las tarjetas de módulos. El curso de NVIDIA tiene **4 módulos de 3 páginas** (unas 4 horas). Nuestro curso los reorganiza en **6 módulos y 20 clases**: compara con la tabla de arriba.
5. Abre la sección **"Cómo introducir tu clave de API"**. No pegues nada todavía: solo ubica los campos. Los configuras en la clase 1.3.
6. Abre la sección **"Si falla una solicitud al modelo"** y léela. Ahí está la regla de oro: ante un 401 o 403, revisa credenciales; ante un 429, espera; ante un 5xx, puede ser el proveedor.

Deberías ver: una página con la mascota de NemoClaw sosteniendo el escudo de OpenShell, el resumen del curso y los objetivos de aprendizaje.

### 2. Recorre el repositorio de NemoClaw

1. Abre <https://github.com/NVIDIA/NemoClaw> y lee el inicio del README.
2. Busca la frase que define el proyecto. Deberías ver algo como: una pila de referencia open source para correr agentes de forma más segura dentro de sandboxes de OpenShell.
3. Fíjate en la etiqueta **alpha / early preview**. NemoClaw saca versiones cada 1 a 3 días. Por eso, en el laboratorio, siempre se usa una versión fijada.
4. Busca la carpeta `nemoclaw-blueprint/` y abre `blueprint.yaml`. No necesitas entenderlo todo. Ubica:
   - las versiones mínima y máxima de OpenShell,
   - la versión mínima de OpenClaw,
   - los perfiles de inferencia (`components.inference.profiles`), que apuntan a `https://integrate.api.nvidia.com/v1`.

### 3. Recorre la documentación

1. Abre <https://docs.nvidia.com/nemoclaw/latest/>.
2. Busca la página **Ecosystem** (sección *About*). Ahí está la tabla con el alcance de OpenClaw, OpenShell y NemoClaw que resumimos arriba.
3. Busca **How it works**. Ubica la tabla de **capas de protección**: red, sistema de archivos, procesos e inferencia. Anota cuáles se pueden cambiar en caliente (red e inferencia) y cuáles quedan fijas al crear el sandbox (archivos y procesos). Lo vas a usar en el Módulo 5.

### 4. Completa tu mapa

Copia esta tabla en tus notas y llénala con tus palabras:

| Pieza | Qué hace | Dónde la verás en el curso |
|---|---|---|
| Modelo (Nemotron) | | |
| OpenClaw | | |
| OpenShell | | |
| NemoClaw | | |
| Brev | | |

## Comprueba que funcionó

- [ ] Puedo explicar en una frase qué separa una llamada a un modelo de un agente.
- [ ] Sé cuál pieza es el agente, cuál el sandbox y cuál el blueprint.
- [ ] Encontré en la portada de NVIDIA la sección "Cómo introducir tu clave de API".
- [ ] Encontré `blueprint.yaml` en el repo de NemoClaw.
- [ ] Sé qué módulos necesitan Brev y cuáles solo una API key.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Busco "NemoClaw" como modelo en build.nvidia.com y no lo puedo llamar por API | NemoClaw no es un modelo: es un blueprint y una CLI. En build.nvidia.com hay una **ficha del blueprint**, no un endpoint de chat | Para llamar a un modelo usa un Nemotron (clase 1.2). NemoClaw se usa en el laboratorio |
| La portada del curso de NVIDIA aparece en inglés | Abriste la URL sin `/es/` o el navegador recordó otro idioma | Usa <https://nvdli.github.io/NemoClawDLI/es/nemoclaw/index.html> o el menú de idioma |
| "Los módulos 3 y 4 de NVIDIA me piden un launchable" y me confundo con la numeración | NVIDIA tiene 4 módulos; nosotros, 6. Su Módulo 3 es nuestro Módulo 4 | Usa la columna "Lección de NVIDIA" de la tabla de 20 clases |
| Pienso que necesito GPU para empezar | Los módulos 1 a 3 llaman a modelos alojados por NVIDIA por API | Solo necesitas la key gratuita. La GPU llega con Brev en el Módulo 4, y no es tuya: es de la nube |
| Instrucciones de un blog no coinciden con el repo de NemoClaw | NemoClaw está en alpha y cambia cada pocos días | Confía en el README y la documentación oficial, y en la versión fijada del laboratorio |

## Reto

Escribe un párrafo de máximo 5 líneas que le explique a un compañero qué pasa cuando OpenClaw quiere entrar a un sitio web que no está en la política.

**Criterio de éxito:** tu párrafo menciona las tres piezas con su papel correcto, dice que la conexión se bloquea por defecto y dice dónde vive la API key (fuera del sandbox).

## Avance del proyecto

Todavía no hay código. Tu avance es el **mapa de Soporte NemoClaw**: en tus notas, dibuja el diagrama de flujo de arriba y marca dónde vivirá cada parte del proyecto:

- El loop en Python (Módulos 2 y 3): fuera de todo sandbox, en tu notebook.
- La skill `soporte-nemoclaw` y la FAQ (Módulo 4): dentro del workspace de OpenClaw, en el sandbox.
- La política que lo contiene (Módulo 5): en OpenShell.

## Recursos

- [Curso de NVIDIA DLI en español: inicio](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/index.html) (NVIDIA, Apache-2.0)
- [Repositorio del curso de NVIDIA: NVDLI/NemoClawDLI](https://github.com/NVDLI/NemoClawDLI)
- [Repositorio de NemoClaw](https://github.com/NVIDIA/NemoClaw) y su [documentación](https://docs.nvidia.com/nemoclaw/latest/)
- [Repositorio de OpenShell](https://github.com/NVIDIA/OpenShell)
- [OpenClaw](https://openclaw.ai)
- [Preguntas frecuentes del curso](../../FAQ.md)

---
*Basado en la página de inicio del curso de NVIDIA DLI "Securing Agents with OpenShell and NemoClaw" (Apache-2.0) y en la documentación de NemoClaw.*
