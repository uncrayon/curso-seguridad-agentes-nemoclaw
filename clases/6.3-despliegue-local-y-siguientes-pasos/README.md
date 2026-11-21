# 6.3 · Cómo correr tu agente de Brev en local

Corre NemoClaw en tu Mac con Apple Silicon y Colima, cierra tu proyecto y elige por dónde seguir. El cookbook conserva las alternativas para Linux y Windows.

| | |
|---|---|
| **Duración del video** | ≈13 min |
| **Práctica** | Guiada en esta página + [cookbook opcional de instalación local](cookbook.md) (en tu propia computadora, fuera de Brev) |
| **Habilidad** | Planear un despliegue local y cerrar un proyecto de agente con criterios de calidad |
| **Material** | [Diapositivas](slides.html) · [FAQ del curso](../../FAQ.md) |

> Esta clase no usa el laboratorio de Brev.

## Lo esencial (sin tecnicismos)

**La idea:** Puedes seguir en Brev, llevar tu agente a tu propia computadora (con 16 GB de memoria y Docker) o a un servidor. Para producción, NVIDIA tiene piezas que mejoran el modelo, la búsqueda y los filtros de lo que entra y sale, pero ninguna reemplaza al sandbox. Y si no lo hiciste al final del laboratorio, guarda tu trabajo y borra tu instancia: detenida sigue cobrando el disco.

**Piénsalo como:** pasar de una [oficina rentada por horas](../../GLOSARIO.md) a montar la oficina en tu casa, y entregar la llave de la rentada al irte.

**Palabras nuevas:** despliegue local (tener el agente en tu propia máquina), Docker (un programa que empaqueta otros programas en cajas estándar, como contenedores de barco), proveedor de inferencia (quien te presta el modelo: la oficina a la que tu agente le manda las preguntas).

**Hazlo sin programar (≈10 min):** Responde sí o no a este checklist: *¿mi organización está lista para tener un agente?* 1) Sabemos qué tarea concreta hará y quién lo va a operar. 2) Hicimos su hoja de trifecta (clase 5.1): qué datos privados lee, qué contenido de desconocidos recibe y por dónde puede sacar información. 3) Va a correr dentro de un sandbox con reglas escritas, y alguien sabe leerlas. 4) Las claves de acceso quedan fuera del agente y sabemos cómo cambiarlas si se filtran. 5) Una persona aprueba las acciones riesgosas: enviar, pagar, borrar, instalar. 6) Revisamos sus skills y tareas programadas como revisamos un contrato. 7) Queda un registro de lo que hace y alguien lo mira. 8) Sabemos cuánto cuesta al mes y quién lo apaga. 9) Sabemos dónde viven los datos y si pueden salir de la empresa. 10) Tenemos un plan para cuando se equivoque. Si marcaste "no" en tres o más, empieza con una prueba pequeña, sin datos reales.

**Qué te llevas:** Sabes qué necesitas para tener tu propio agente y puedes decir, con una lista concreta, si tu organización está lista para usar uno.

## Lo que vas a lograr
- Saber si tu máquina puede correr NemoClaw, qué instalar y qué proveedor de inferencia usar.
- Ubicar las piezas de producción de NVIDIA (NIM, NeMo Guardrails, NeMo Retriever, DGX Spark) en tu propio proyecto.
- Entregar **Soporte NemoClaw** con un checklist y una rúbrica, y elegir tu siguiente paso.

## Antes de empezar
- Tu proyecto **Soporte NemoClaw** con lo hecho en las clases 2.1 a 5.3, y en la 6.1 y la 6.2 si las hiciste (notebooks, skills en [`skill-library/`](../../skill-library/README.md), análisis de seguridad de la 5.x).
- Tu laboratorio de Brev ya debería estar **borrado**: lo cerraste al final de la [5.3](../5.3-sandbox-y-politicas/README.md) o, si hiciste prácticas complementarias, de la última que hiciste ([6.1](../6.1-clis-de-agentes/README.md) o la parte de laboratorio de la [6.2](../6.2-biblioteca-de-skills/README.md)). Si no, el paso 7 te dice cómo.
- Opcional, solo si quieres instalar NemoClaw en tu propia máquina: Linux, macOS Apple Silicon o Windows con WSL2 (ver tabla del paso 2). No necesitas Brev para esto.

## Paso a paso

### 1. Decide dónde vive tu agente
| Opción | Cuándo conviene | Costo | Qué cuidas tú |
|---|---|---|---|
| **Seguir en Brev** (un despliegue nuevo del launchable de NemoClaw) | Quieres el mismo entorno del curso, sin instalar nada | ≈USD 0.25/h encendida; detenida, el disco sigue cobrando ≈USD 1.20 al día | Borrarla (**Delete**) al terminar |
| **Tu máquina** | Tienes 16 GB de RAM y quieres el agente cerca de tus archivos | Luz y disco | Docker, actualizaciones, reinicios |
| **Un servidor propio o DGX Spark** | Agente 24/7, inferencia local, datos que no salen | Hardware | Acceso remoto seguro (`ssh -L`), respaldos |

Para un despliegue separado con modelos alojados: endpoint `https://integrate.api.nvidia.com/v1` y tu key de NVIDIA. Verifica el acceso y la cuota vigentes de tu cuenta.

### 2. Prepara tu Mac con Colima

Esta práctica usa **Colima con Docker y NVIDIA Endpoints**. El agente corre en tu computadora; las solicitudes al modelo van a la API alojada de NVIDIA. No necesitas una GPU NVIDIA local.

Docker ejecuta los contenedores. El comando `docker` es su cliente; Colima proporciona la máquina virtual Linux que ejecuta el motor en macOS. Docker Desktop es otra opción que incluye su propia VM. Aquí elegimos Colima, aunque NemoClaw no lo exige.

| Recurso | Mínimo | Recomendado |
|---|---|---|
| CPU | 4 vCPU | 4+ vCPU |
| RAM | 8 GB | **16 GB** (con 8 GB, la imagen del sandbox puede quedarse sin memoria) |
| Disco libre | 20 GB | 40 GB |
| Software | Colima + Docker CLI en este Mac, Node.js 22.19+, npm 10+ | Homebrew para los comandos siguientes |
| Plataformas | Linux (Ubuntu 24.04 validado), macOS Apple Silicon, Windows WSL2, DGX Spark | Mac Intel **no** está soportado |

Primero revisa los recursos del Mac. `hw.memsize` muestra bytes:

```bash
sysctl -n hw.ncpu
sysctl -n hw.memsize
df -h ~
```

Instala [Homebrew](https://brew.sh/) si te falta. Si faltan las herramientas de línea de comandos de Xcode, ejecuta `xcode-select --install` y termina el diálogo antes de continuar.

```bash
brew install colima docker
colima start --cpu 4 --memory 12 --disk 100
```

El ejemplo asigna a la VM 4 CPUs, 12 GiB de RAM y un disco virtual de 100 GiB. Es un punto de partida para el Mac de 18 GiB usado en esta práctica, no una garantía para cualquier carga. Deja memoria para macOS y tus otras aplicaciones. El límite del disco virtual no crea espacio libre en el Mac; las descargas y los builds necesitan espacio real. Si Colima ya corre y quieres cambiar sus recursos, ejecuta `colima stop` antes del nuevo comando `colima start`. Esto detiene todas las cargas de esa VM.

Selecciona el perfil predeterminado de Colima y revisa el motor:

```bash
unset DOCKER_HOST DOCKER_CONTEXT
docker context use colima
colima status
docker info --format 'CPUs={{.NCPU}} MemoryBytes={{.MemTotal}}'
```

Debes ver Colima en ejecución y **4 CPUs** en la salida de Docker. La memoria disponible puede quedar ligeramente por debajo de 12 GiB. Los contenedores usan la capacidad del motor, no todos los recursos del Mac.

Si `docker info` funciona pero NemoClaw u OpenShell todavía no encuentran Docker, indica el socket en la terminal donde los vas a ejecutar:

```bash
unset DOCKER_CONTEXT
export DOCKER_HOST="unix://${HOME}/.colima/default/docker.sock"
docker info
```

`DOCKER_HOST` le dice al cliente dónde conectarse. Es una solución para seleccionar el socket, no una señal de que Docker esté mal instalado. La ruta anterior corresponde al perfil predeterminado de Colima; para otro perfil, consulta su socket con `colima status`. El `export` dura en esta sesión de terminal. Repítelo en una terminal nueva si hace falta. Antes de cambiar de runtime, elimina esa variable con `unset DOCKER_HOST` y selecciona el contexto que quieras. Consulta la [FAQ del socket de Colima](https://colima.run/docs/faq/#where-is-the-docker-socket-located) y los [contextos de Docker](https://docs.docker.com/engine/manage-resources/contexts/).

### 3. Instala, usa y pausa NemoClaw

#### Instala con límites que quepan en la VM

Para la VM anterior de 4 CPUs y 12 GiB, limita el sandbox a **3 CPUs y 8 GiB**. Así queda capacidad para la VM, Docker y los procesos de apoyo. Son límites dentro de Colima, no recursos adicionales. El límite de CPU tampoco reserva núcleos físicos de forma permanente.

En NemoClaw v0.0.145 observamos que el perfil developer calculaba su 75 % sobre un Mac de 12 CPUs y 18 GiB. Pedía 9 CPUs y 13Gi a una VM más pequeña, y Docker rechazaba la solicitud de CPU. Los valores explícitos siguientes evitan ese error. El [issue #14743](https://github.com/NVIDIA/NemoClaw/issues/14743) contiene la propuesta de corrección y las pruebas de regresión; que exista un parche en un fork no significa que tu versión instalada ya lo incluya.

Si todavía no tienes NemoClaw, ejecuta:

```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | \
  NEMOCLAW_AGENT=openclaw NEMOCLAW_CPU=3 NEMOCLAW_RAM=8Gi bash
```

Las variables van **del lado de `bash`** del pipe para que las reciban el instalador y el onboarding. El instalador revisa Node.js y npm; verifica que `node --version` sea al menos 22.19 y `npm --version`, al menos 10. Para fijar una versión, usa la Receta 3 del [cookbook](cookbook.md).

Si NemoClaw ya está instalado y vas a crear un sandbox, ejecuta:

```bash
NEMOCLAW_CPU=3 NEMOCLAW_RAM=8Gi nemoclaw onboard --name my-assistant
```

Elige **OpenClaw**, **NVIDIA Endpoints** y la política **Balanced**. Introduce tu key de NVIDIA cuando la pida el asistente. Si usas una variable, usa `NVIDIA_INFERENCE_API_KEY` y evita que su valor real quede en el historial o en archivos compartidos. El onboarding debe mostrar los límites de CPU y RAM y terminar con `NemoClaw is ready`.

Si un intento anterior falló, lee `nemoclaw debug --quick` antes de elegir cómo recuperarlo. Un timeout por sí solo no identifica la causa. Después de resolver una desconexión temporal, usa `nemoclaw onboard --resume`. Para el error de recursos, empieza otro intento con un nombre nuevo:

```bash
NEMOCLAW_CPU=3 NEMOCLAW_RAM=8Gi \
  nemoclaw onboard --fresh --name my-assistant-fixed
```

`--fresh` descarta el checkpoint del onboarding; no cambia los límites de un sandbox existente ni libera su nombre. Conserva el sandbox fallido hasta saber si contiene datos que necesitas. Si elegiste el nombre nuevo, úsalo en los comandos siguientes. No necesitas borrar Colima ni reinstalar Docker para corregir este límite de CPU.

#### Comprueba que responde y úsalo

```bash
nemoclaw my-assistant status
nemoclaw my-assistant dashboard-url --quiet
nemoclaw launch my-assistant
```

Abre la URL que muestra tu instalación, normalmente en `127.0.0.1:18789`. Trata una URL que incluya un token como una contraseña. El puerto 18080 suele pertenecer al gateway de OpenShell. Para revisar un fallo, ejecuta `nemoclaw my-assistant logs --follow`; sal de los logs con **Ctrl+C**. Instala las skills del curso con la Receta 8 del cookbook.

#### Apaga por hoy y vuelve después

Para detener solo este sandbox y dejar Colima disponible para otras tareas:

```bash
nemoclaw my-assistant stop
```

Para detener toda la VM de Colima y todos sus contenedores:

```bash
colima stop
colima status
```

Colima debe indicar que no está corriendo. La VM y sus contenedores dejan de usar CPU y RAM; sus datos siguen en disco. Pueden quedar procesos en el Mac: un servicio del gateway de OpenShell, un servidor Ollama local o un túnel de terminal corren fuera de la VM. Revisa el Monitor de Actividad y `brew services list`; detén esos servicios con el gestor que los inició. Evita comandos que maten todos los procesos por nombre.

Para volver, reutiliza la configuración guardada de la VM:

```bash
colima start
docker info
nemoclaw my-assistant status
```

Antes, restaura `DOCKER_HOST` si esta terminal necesita la solución del socket. Si el sandbox está detenido, ejecuta `nemoclaw my-assistant start`. Si sigue sin estar sano, revisa su estado y ejecuta `nemoclaw my-assistant recover`. Los comandos de estado y recuperación pueden iniciar servicios de apoyo; usa `colima status` para comprobar que la VM siga apagada.

`colima stop` es el apagado cotidiano. `colima delete`, `destroy` y la desinstalación son operaciones de limpieza. Para actualizar, sigue `nemoclaw backup-all`, `nemoclaw update` y `nemoclaw upgrade-sandboxes --auto`. Deja que NemoClaw gestione su versión compatible de OpenShell; no ejecutes `openshell self-update` por separado.

### 4. Ubica las piezas de producción en tu proyecto
| Pieza | Qué es | Qué mejora en Soporte NemoClaw |
|---|---|---|
| **NIM** | Modelo + tokenizer + servidor compatible con OpenAI en un contenedor, en tu infraestructura | Cambias `BASE_URL` y el modelo corre en tu red. Antes, prueba que soporte tool calls y salida estructurada |
| **NeMo Retriever** | Búsqueda híbrida (dispersa + densa), reranker y chunking, con embeddings NIM | Reemplaza el RAG en memoria de la 3.2 cuando la FAQ crezca |
| **NeMo Guardrails** | Filtros programables de entrada y salida en la capa de aplicación | Bloquea que el agente pida o muestre keys, o que hable de temas fuera del curso. **Complementa** al sandbox; no lo reemplaza |
| **DGX Spark** | Equipo de escritorio con GPU NVIDIA; plataforma probada de NemoClaw con inferencia local | Agente 24/7 con datos que no salen de tu oficina. Revisa la galería de [playbooks de NemoClaw para Spark](https://build.nvidia.com/spark/nemoclaw-applications) |

Para cada una, escribe una línea en tu proyecto: "la usaría para ___ cuando ___".

### 5. Cierra tu proyecto: checklist de entrega
- [ ] **Loop y herramientas** (2.x): el agente responde con `buscar_faq` y `estimar_costo_brev`, y valida argumentos.
- [ ] **Triage** (3.1): clasifica en `instalacion | api_key | brev | seguridad | otro`.
- [ ] **RAG con citas** (3.2): cada respuesta trae `Fuente:` de `datos/faq/`.
- [ ] **Reporte de diagnóstico** (3.3): los subagentes dejan su trabajo en archivos.
- [ ] **Despliegue** (4.x): la skill `soporte-nemoclaw` corre en OpenClaw y la tarea cron deja el resumen.
- [ ] **Seguridad** (5.x): análisis de trifecta y política del sandbox documentados; ningún secreto en el repo (`git grep nvapi-` no devuelve keys reales).
- [ ] **Skills** (6.2): 4 skills en `skill-library/`, validadas, con tasa de acierto ≥ 90 % y la tabla en `docs/evaluacion-skills.md`.
- [ ] **Elección de agente** (6.1): `docs/eleccion-de-agente.md`.
- [ ] **README del proyecto**: qué hace, cómo correrlo, límites conocidos y una captura (con el token difuminado).
- [ ] **Brev**: instancia borrada (ya no aparece en **Compute**) y saldo revisado en **Billing**.

### 6. Autoevalúate con la rúbrica
| Criterio | Inicial (1) | Competente (2) | Destacado (3) |
|---|---|---|---|
| **Funciona** | Responde algunas preguntas | Responde la FAQ con citas correctas | Además dice "no lo sé" cuando no hay fuente y escala |
| **Herramientas y skills** | Herramientas sin validar | Herramientas validadas, 4 skills válidas | Tasa de acierto ≥ 90 % medida y documentada; una quinta skill |
| **Seguridad** | Sin análisis | Trifecta identificada y política del sandbox leída | Mitigación probada (bloqueo comprobado en logs) y sin secretos en el historial de git |
| **Operación** | Corre solo a mano | Cron que deja el resumen diario | Sabe recuperarlo tras un reinicio y lo documenta (status → start → recover) |
| **Documentación** | Sin README | README con pasos para correrlo | README + decisiones (agente, proveedor, piezas de producción) y límites conocidos |

Suma tus puntos: **5–8** sigue iterando · **9–12** listo para mostrar · **13–15** publícalo y compártelo.

### 7. Confirma que el laboratorio está borrado
Lo normal es que ya hayas borrado tu instancia al final de tu última práctica de laboratorio ([5.3](../5.3-sandbox-y-politicas/README.md), o la última práctica complementaria que hiciste). Compruébalo en el navegador:
1. En la consola de Brev (brev.nvidia.com), abre **Compute**. Tu instancia (`nemoclaw-…`) ya no debe aparecer.
2. Si sigue ahí, guarda lo que quieras: copia el texto desde la **VM TERMINAL** o baja todo en un zip con la [receta previa del cookbook](cookbook.md#receta-previa--respalda-tu-laboratorio-en-un-zip), y luego abre la instancia y presiona **Delete**. Confirma en el aviso que aparece.
3. Abre **Billing** en el menú de arriba y revisa tu saldo.

Encendida, la instancia cuesta ≈USD 0.25/h. Detenida (**Stop**), el disco sigue cobrando ≈USD 0.05/h, unos USD 1.20 al día. Borrada (**Delete**), ya no cobra nada, pero pierdes lo que había adentro. Detalles en [LABORATORIO.md](../../LABORATORIO.md).

## Comprueba que funcionó
- [ ] Sabes si tu máquina cumple los requisitos (o qué le falta).
- [ ] Si instalaste en local, Docker muestra la capacidad de la VM, el agente responde y puedes detener y reanudar Colima sin borrar datos.
- [ ] Escribiste una línea por pieza de producción para tu proyecto.
- [ ] Marcaste el checklist de entrega y tienes tu puntaje de la rúbrica.
- [ ] Tu instancia de Brev está borrada y revisaste tu saldo.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| El instalador rechaza tu Mac | Mac Intel (x86_64) no está soportado | Usa Brev, un Linux o un Mac con Apple Silicon |
| Exit 137 / OOM al crear el sandbox | La VM o el host se quedaron sin memoria | Revisa ambos límites. Sube la memoria de Colima solo si el Mac tiene margen; el swap de la Receta 0 es para Linux |
| `NEMOCLAW_INSTALL_TAG` "no hace nada" | La variable quedó del lado de `curl` | `curl ... \| NEMOCLAW_INSTALL_REF= NEMOCLAW_INSTALL_TAG=vX.Y.Z bash` |
| `nemoclaw: command not found` al terminar | El `PATH` de tu shell no se actualizó | Abre una terminal nueva; en macOS con zsh, revisa `~/.zshrc` y `~/.local/bin` |
| `docker: command not found` tras instalar Colima | Falta el cliente de Docker | `brew install docker` |
| Falla la conexión a Docker en macOS | Colima está detenido o el cliente eligió otro socket | Sigue el paso 2: `colima status`, contexto de Docker y `DOCKER_HOST` si hace falta |
| Falla la conexión a Docker en Linux | El motor está detenido o tu usuario no tiene acceso al socket | Sigue la Receta 1; los comandos del grupo `docker` de Linux no aplican a macOS |
| Docker rechaza la cantidad de CPUs y luego aparece un timeout | El perfil porcentual usó la capacidad del host | Compara `docker info` con la solicitud; usa los límites explícitos del paso 3 y otro nombre de sandbox |
| `✗ openshell <versión> is above the maximum supported by this NemoClaw release.` | Actualizaste OpenShell por fuera | No uses `openshell self-update`; reinstala la versión soportada |
| Tu saldo de Brev sigue bajando aunque ya no usas el laboratorio | La instancia está detenida (**Stop**), no borrada: el disco cobra | Consola de Brev → **Compute** → tu instancia → **Delete** |
| `Port 18080 is not available` al instalar en local | Otro proceso usa el puerto del gateway de OpenShell | Cierra ese proceso o revisa la Receta 5 del cookbook |

## Reto
Elige **una** pieza de producción y haz un plan de una página para agregarla a Soporte NemoClaw: qué cambia en el código, qué riesgo reduce, cómo medirías la mejora y qué **no** resuelve.
**Criterio de éxito:** el plan nombra una métrica (p. ej. tasa de respuestas con cita correcta, o intentos de pedir una key bloqueados) y una prueba que la mida.

## Avance del proyecto · Cierre
Tu proyecto termina aquí. Publícalo en tu GitHub con:
1. El checklist del paso 5 completo en el README.
2. Tu puntaje de la rúbrica y qué mejorarías primero.
3. Tu decisión de despliegue: Brev, local o servidor, y con qué proveedor de inferencia.

## Siguientes pasos
- **Ruta de aprendizaje de IA agéntica de NVIDIA**: este curso corresponde a la lección 6, *agentes autónomos más seguros con OpenClaw*. Las lecciones previas cubren construir agentes, RAG agéntico, evaluación, personalización y agentes profundos.
- **Elige un eje para profundizar** (lección 04c):
  - **La capa de conocimiento**: chunking, recuperación, fidelidad de las respuestas.
  - **El sustrato**: MCP, Responses API, convenciones OTel GenAI, A2A.
  - **Flotas y contención**: qué cambia con N agentes y cómo Landlock, seccomp y los namespaces de red acotan a cada uno.
- **Antes de llevarlo a producción**: prueba los controles de la aplicación **y** los permisos del runtime por separado; y verifica la autoridad administrativa aparte: poder leer no prueba que controlas al agente.

## Recursos
- NVIDIA DLI · Cómo profundizar en el tema (04c). Esta clase está basada en la lección 04c del curso de NVIDIA DLI (Apache-2.0).
- NemoClaw · [Requisitos](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/get-started/prerequisites) · [Quickstart de OpenClaw](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/get-started/quickstart) · [Error de capacidad de Docker y propuesta de corrección](https://github.com/NVIDIA/NemoClaw/issues/14743)
- Colima · [Primeros pasos](https://colima.run/docs/getting-started/) · [Configuración](https://colima.run/docs/configuration/) · [Comandos](https://colima.run/docs/commands/)
- NVIDIA · [NIM](https://docs.nvidia.com/nim/) · [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) · [NeMo Curator](https://github.com/NVIDIA/NeMo-Curator) · [AI-Q Blueprint](https://build.nvidia.com/nvidia/aiq)
- NVIDIA · [Playbooks de NemoClaw para DGX Spark](https://build.nvidia.com/spark/nemoclaw-applications) · [NemoClaw en DGX Spark](https://build.nvidia.com/spark/nemoclaw/instructions)
- NVIDIA · [Agentic AI Learning Path](https://developer.nvidia.com/topics/ai/agentic-ai-learning-path) · [Blog de IA generativa](https://developer.nvidia.com/blog/category/generative-ai/)
- NVIDIA Blog · [Un agente local siempre activo y seguro con NemoClaw y OpenClaw](https://developer.nvidia.com/blog/build-a-secure-always-on-local-ai-agent-with-nvidia-nemoclaw-and-openclaw/)
