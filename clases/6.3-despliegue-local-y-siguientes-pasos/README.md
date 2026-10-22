# 6.3 · Próximos pasos y despliegue local

Cierra tu proyecto, aprende qué necesitas para correr NemoClaw en tu máquina y elige por dónde seguir.

| | |
|---|---|
| **Duración del video** | ≈8 min |
| **Práctica** | Guiada en esta página + [cookbook opcional de instalación local](cookbook.md) (en tu propia computadora, fuera de Brev) |
| **Habilidad** | Planear un despliegue local y cerrar un proyecto de agente con criterios de calidad |
| **Material** | [Diapositivas](slides.html) · [FAQ del curso](../../FAQ.md) |

> **El Módulo 6 es opcional.** Esta clase no usa el laboratorio de Brev.

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
- Tu laboratorio de Brev ya debería estar **borrado**: lo cerraste al final de la [5.3](../5.3-sandbox-y-politicas/README.md) o, si hiciste prácticas opcionales, de la última que hiciste ([6.1](../6.1-clis-de-agentes/README.md) o la parte de laboratorio de la [6.2](../6.2-biblioteca-de-skills/README.md)). Si no, el paso 7 te dice cómo.
- Opcional, solo si quieres instalar NemoClaw en tu propia máquina: Linux, macOS Apple Silicon o Windows con WSL2 (ver tabla del paso 2). No necesitas Brev para esto.

## Paso a paso

### 1. Decide dónde vive tu agente
| Opción | Cuándo conviene | Costo | Qué cuidas tú |
|---|---|---|---|
| **Seguir en Brev** (un despliegue nuevo del launchable de NemoClaw) | Quieres el mismo entorno del curso, sin instalar nada | ≈USD 0.25/h encendida; detenida, el disco sigue cobrando ≈USD 1.20 al día | Borrarla (**Delete**) al terminar |
| **Tu máquina** | Tienes 16 GB de RAM y quieres el agente cerca de tus archivos | Luz y disco | Docker, actualizaciones, reinicios |
| **Un servidor propio o DGX Spark** | Agente 24/7, inferencia local, datos que no salen | Hardware | Acceso remoto seguro (`ssh -L`), respaldos |

Para un despliegue separado con modelos alojados: endpoint `https://integrate.api.nvidia.com/v1` y tu key de NVIDIA. Verifica el acceso y la cuota vigentes de tu cuenta.

### 2. Revisa tu máquina en 2 minutos
| Recurso | Mínimo | Recomendado |
|---|---|---|
| CPU | 4 vCPU | 4+ vCPU |
| RAM | 8 GB | **16 GB** (con 8 GB, la imagen del sandbox puede quedarse sin memoria) |
| Disco libre | 20 GB | 40 GB |
| Software | Docker, Node.js 22.19+, npm 10+ | |
| Plataformas | Linux (Ubuntu 24.04 validado), macOS Apple Silicon, Windows WSL2, DGX Spark | Mac Intel **no** está soportado |

```bash
nproc; free -h; df -h ~        # en macOS: sysctl -n hw.ncpu; sysctl -n hw.memsize; df -h ~
docker info >/dev/null && echo "Docker OK"
node --version                 # v22.19.0 o mayor
```
Deberías ver: 4 o más CPUs, 8 GB o más de RAM, 20 GB o más libres, `Docker OK` y Node 22.19+. Si algo falta, el [cookbook](cookbook.md) (Recetas 0 y 1) dice cómo arreglarlo.

### 3. (Opcional) Instala NemoClaw en local
Solo si quieres tener NemoClaw en tu propia máquina. Todo esto pasa en tu computadora, no en Brev. Sigue el [cookbook](cookbook.md). El camino corto:
```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_REF= NEMOCLAW_INSTALL_TAG=vX.Y.Z bash
```
- Las variables van **del lado de `bash`** del pipe.
- En el onboarding, la key se lee de `NVIDIA_INFERENCE_API_KEY` (no de `NVIDIA_API_KEY`).
- Proveedores: **NVIDIA Endpoints** (sin GPU), **Ollama** local, **vLLM** local, **NIM** local (experimental, requiere GPU NVIDIA).
- Igual que en el laboratorio, el chat de OpenClaw queda en `http://127.0.0.1:18789/` y el gateway de OpenShell en el puerto 18080. `openshell status` te dice si está `Connected`.

Día 1 y día 2 en una tabla:

| Momento | Comandos |
|---|---|
| Día 1 · usar | `nemoclaw my-assistant status` · `dashboard-url --quiet` · `nemoclaw launch my-assistant` · `logs --follow` |
| Día 1 · tu proyecto | `nemoclaw my-assistant skill install ./skill-library/<skill>/` · `skill list` |
| Día 2 · reinicio | `nemoclaw my-assistant status` → `start` → `recover` |
| Día 2 · actualizar | `nemoclaw backup-all` → `nemoclaw update` → `nemoclaw upgrade-sandboxes --auto` |
| Nunca | `openshell self-update` · `openclaw update` dentro del sandbox · `nemoclaw start/stop` globales (obsoletos) |

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
Lo normal es que ya hayas borrado tu instancia al final de tu última práctica de laboratorio ([5.3](../5.3-sandbox-y-politicas/README.md), o la última práctica opcional que hiciste). Compruébalo en el navegador:
1. En la consola de Brev (brev.nvidia.com), abre **Compute**. Tu instancia (`nemoclaw-…`) ya no debe aparecer.
2. Si sigue ahí, guarda lo que quieras (muéstralo en la **VM TERMINAL** y copia el texto a tus notas), y luego abre la instancia y presiona **Delete**. Confirma en el aviso que aparece.
3. Abre **Billing** en el menú de arriba y revisa tu saldo.

Encendida, la instancia cuesta ≈USD 0.25/h. Detenida (**Stop**), el disco sigue cobrando ≈USD 0.05/h, unos USD 1.20 al día. Borrada (**Delete**), ya no cobra nada, pero pierdes lo que había adentro. Detalles en [LABORATORIO.md](../../LABORATORIO.md).

## Comprueba que funcionó
- [ ] Sabes si tu máquina cumple los requisitos (o qué le falta).
- [ ] Escribiste una línea por pieza de producción para tu proyecto.
- [ ] Marcaste el checklist de entrega y tienes tu puntaje de la rúbrica.
- [ ] Tu instancia de Brev está borrada y revisaste tu saldo.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| El instalador rechaza tu Mac | Mac Intel (x86_64) no está soportado | Usa Brev, un Linux o un Mac con Apple Silicon |
| Exit 137 / OOM al crear el sandbox | 8 GB de RAM o menos | 16 GB, o agrega 4–8 GB de swap (cookbook, Receta 0) |
| `NEMOCLAW_INSTALL_TAG` "no hace nada" | La variable quedó del lado de `curl` | `curl ... \| NEMOCLAW_INSTALL_REF= NEMOCLAW_INSTALL_TAG=vX.Y.Z bash` |
| `nemoclaw: command not found` al terminar | El `PATH` de tu shell no se actualizó | Terminal nueva o `source ~/.bashrc` |
| `Docker is not running` aunque Docker corre | Tu usuario no está en el grupo `docker` | `sudo usermod -aG docker $USER && newgrp docker` |
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
- NemoClaw · [Documentación](https://docs.nvidia.com/nemoclaw/latest/) · [Requisitos](https://docs.nvidia.com/nemoclaw/latest/get-started/prerequisites) · [Repo e issues](https://github.com/NVIDIA/NemoClaw)
- NVIDIA · [NIM](https://docs.nvidia.com/nim/) · [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) · [NeMo Curator](https://github.com/NVIDIA/NeMo-Curator) · [AI-Q Blueprint](https://build.nvidia.com/nvidia/aiq)
- NVIDIA · [Playbooks de NemoClaw para DGX Spark](https://build.nvidia.com/spark/nemoclaw-applications) · [NemoClaw en DGX Spark](https://build.nvidia.com/spark/nemoclaw/instructions)
- NVIDIA · [Agentic AI Learning Path](https://developer.nvidia.com/topics/ai/agentic-ai-learning-path) · [Blog de IA generativa](https://developer.nvidia.com/blog/category/generative-ai/)
- NVIDIA Blog · [Un agente local siempre activo y seguro con NemoClaw y OpenClaw](https://developer.nvidia.com/blog/build-a-secure-always-on-local-ai-agent-with-nvidia-nemoclaw-and-openclaw/)
