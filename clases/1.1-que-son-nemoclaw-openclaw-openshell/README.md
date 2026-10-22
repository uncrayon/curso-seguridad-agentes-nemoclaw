# 1.1 · Qué son NemoClaw, OpenClaw y OpenShell

Objetivo: entender qué es un agente y qué hace cada pieza del stack antes de tocar código.

| | |
|---|---|
| **Duración del video** | ≈6 min |
| **Práctica** | Guiada en el navegador (sin código, ≈20 min) |
| **Habilidad** | Ubicar cada pieza del stack: OpenClaw, OpenShell y NemoClaw |
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

Después, completa en una hoja estas tres frases con tus palabras: "OpenClaw es ___", "OpenShell es ___", "NemoClaw es ___". Por último, abre la [portada del curso](../../index.html) (el enlace que está debajo del video) y busca, solo leyendo, la sección "Clase por clase". Respuestas: 2, 4 y 5 son agentes; 1 y 3, solo modelo.

**Qué te llevas:** puedes explicarle a cualquiera qué es un agente, por qué hay que encerrarlo y qué papel tiene cada pieza.

## Lo que vas a lograr

- Explicar con tus palabras qué es un agente de IA: un modelo dentro de un loop, con herramientas y memoria.
- Distinguir OpenClaw (el agente), OpenShell (el sandbox y el gateway) y NemoClaw (el blueprint y la CLI que los une).
- Saber qué vas a construir en las 19 clases y qué necesitas para cada módulo.

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

### El mapa de las 19 clases

| Módulo | Clase | Práctica |
|---|---|---|
| **1 · Prepara tu entorno** | 1.1 Qué son NemoClaw, OpenClaw y OpenShell | Navegador |
| | 1.2 Crea tu cuenta y tu API key en NVIDIA Build | Navegador |
| | 1.3 Configura rutas de modelo y diagnostica errores | Notebook |
| **2 · El loop básico** | 2.1 De una sola llamada al loop de agente | Notebook |
| | 2.2 Razonamiento con el patrón ReAct | Notebook |
| | 2.3 Convierte funciones en herramientas | Notebook |
| **3 · Coordina, fundamenta y planea** | 3.1 Enruta trabajo entre varias llamadas | Notebook |
| | 3.2 RAG para fundamentar en tus fuentes | Notebook |
| | 3.3 Agentes profundos que crean subagentes | Notebook |
| **4 · Lleva tu agente a NemoClaw** | 4.1 Levanta el laboratorio NemoClaw en Brev | Laboratorio |
| | 4.2 Explora el gateway y el workspace de OpenClaw | Laboratorio |
| | 4.3 Agentes en operación continua y programada | Laboratorio |
| | 4.4 Cambia OpenClaw por Hermes en NemoClaw *(opcional)* | Laboratorio |
| **5 · Asegura el agente con OpenShell** | 5.1 La trifecta letal y la superficie de riesgo | Diapositivas |
| | 5.2 Identidades y límites con OpenShell | Laboratorio |
| | 5.3 Restringe herramientas, archivos y red | Laboratorio |
| **6 · Amplía tu práctica** *(opcional)* | 6.1 Compara CLIs de agentes modernos *(opcional)* | Laboratorio |
| | 6.2 Construye tu biblioteca de skills *(opcional)* | Notebook |
| | 6.3 Próximos pasos y despliegue local *(opcional)* | Diapositivas |

Qué necesitas en cada etapa:

- **Módulos 1 a 3**: una API key gratuita de NVIDIA Build y Python (Colab o tu máquina). No necesitas GPU.
- **Módulos 4 a 6**: una cuenta de [Brev](https://brev.nvidia.com/) para levantar el laboratorio (una máquina en la nube con NemoClaw ya instalado) y un navegador de escritorio.

## Paso a paso (práctica guiada en el navegador)

### 1. Recorre la portada del curso

1. Abre la [portada del curso](../../index.html): es el enlace que está debajo del video. Desde ahí llegas a todo el material.
2. Lee **"¿No programas? Este curso también es para ti"**. Son tres ideas: cada clase empieza con «Lo esencial» (la idea en palabras simples y una actividad sin programar), los notebooks se corren con un botón en Colab aunque todavía no tengas API key, y el laboratorio se hace desde el navegador, sin instalar nada.
3. Baja a **"Cómo funciona el curso"** y ubica las tres etapas: tu acceso a modelos (una API key `nvapi-` gratuita, lo único que necesitas en los módulos 1 a 3), los notebooks en Colab o en tu máquina, y el laboratorio real en Brev desde el Módulo 4.
4. Mira **"El stack en un vistazo"**: una tarjeta por pieza (OpenClaw, el agente; OpenShell, el sandbox; NemoClaw, el blueprint) y un diagrama que muestra que tu API key se queda fuera del sandbox. Compáralo con la tabla de "Las tres piezas" de arriba.
5. Lee **"Proyecto del curso: «Soporte NemoClaw»"**: ahí ves cómo crece el agente del Módulo 2 al 6.
6. Baja a **"Clase por clase"**: 6 módulos y 19 clases. Cada tarjeta trae la duración, lo que vas a aprender y sus enlaces: **Guía** (la página de la clase, como esta), **Diapositivas** y, según la clase, **Colab** (el notebook, que se abre en tu navegador) o **Recetario** (las recetas de comandos del laboratorio). Compara con la tabla de arriba y ubica la clase 1.3: es la primera con botón de Colab.
7. Lee **"Los errores que más vas a ver"**. Ahí está la regla de oro: ante un 401 o 403, revisa tu key y tu cuenta; ante un 404 o 410, revisa el nombre del modelo; ante un 429, espera unos segundos y reintenta.
8. Ubica las páginas de apoyo: el **Glosario** (botón de arriba), **Tu laboratorio en Brev** (el enlace «plan del laboratorio», en la primera sección: cuánto cuesta y cómo hacer que te alcance el crédito) y las **Preguntas frecuentes**, con más de 50 casos resueltos. Guarda la portada en tus marcadores.

Deberías ver: arriba, el título del curso con los botones "Empieza con la clase 1.1", "Consigue tu API key", "Laboratorio en Brev", "Preguntas frecuentes" y "Glosario", y la línea "6 módulos · 19 clases".

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
- [ ] Encontré en la portada del curso la sección "Clase por clase" y sé qué enlaces trae cada tarjeta.
- [ ] Encontré `blueprint.yaml` en el repo de NemoClaw.
- [ ] Sé qué módulos necesitan Brev y cuáles solo una API key.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Busco "NemoClaw" como modelo en build.nvidia.com y no lo puedo llamar por API | NemoClaw no es un modelo: es un blueprint y una CLI. En build.nvidia.com hay una **ficha del blueprint**, no un endpoint de chat | Para llamar a un modelo usa un Nemotron (clase 1.2). NemoClaw se usa en el laboratorio |
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

- [Portada del curso](../../index.html), [glosario](../../GLOSARIO.md) y [tu laboratorio en Brev](../../LABORATORIO.md)
- Página de inicio del curso de NVIDIA DLI en español. Esta clase está basada en ella (Apache-2.0).
- [Repositorio del curso de NVIDIA: NVDLI/NemoClawDLI](https://github.com/NVDLI/NemoClawDLI)
- [Repositorio de NemoClaw](https://github.com/NVIDIA/NemoClaw) y su [documentación](https://docs.nvidia.com/nemoclaw/latest/)
- [Repositorio de OpenShell](https://github.com/NVIDIA/OpenShell)
- [OpenClaw](https://openclaw.ai)
- [Preguntas frecuentes del curso](../../FAQ.md)

---
*Basado en la página de inicio del curso de NVIDIA DLI "Securing Agents with OpenShell and NemoClaw" (Apache-2.0) y en la documentación de NemoClaw.*
