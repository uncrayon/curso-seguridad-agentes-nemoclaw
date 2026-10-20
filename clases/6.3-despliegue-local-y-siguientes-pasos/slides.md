## ¿Dónde vive tu agente?

:::diagrama c63-tres-caminos

Notas:
Como mudarse de una oficina rentada a una propia. Clic 1: Brev, el launchable del curso; pagas por hora encendida y el disco mientras exista. Clic 2: tu computadora (16 GB de RAM, Docker, Node 22.19+), cerca de tus archivos. Clic 3: un servidor o una DGX Spark: 24/7 e inferencia local, tus datos no salen. Clic 4: el criterio. El laboratorio termina; tu proyecto no. Esta clase es un mapa, no un tutorial de instalación: el paso a paso está en el cookbook opcional.

---

## Requisitos para correrlo en local

:::diagrama c63-requisitos

Notas:
Clic 1: mínimo 4 vCPU, 8 GB de RAM y 20 GB de disco; recomendado 16 GB y 40 GB. Docker y Node 22.19+. Clic 2: probado en Linux (Ubuntu 24.04), DGX Spark, macOS Apple Silicon y WSL2; Mac Intel no está soportado (el instalador lo rechaza). Clic 3: cómo ver tu memoria sin terminal. Con 8 GB, la imagen del sandbox (~2.4 GB comprimida) puede disparar el OOM killer. La GPU es opcional si usas NVIDIA Endpoints. Muéstrala 20 segundos.

---

## Instalar en una línea (y fijar la versión)

:::diagrama c63-instalar

.lead Es la forma de operador: una línea instala OpenShell y NemoClaw, y lanza el asistente de configuración.

Notas:
El comando: `curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_REF= NEMOCLAW_INSTALL_TAG=vX.Y.Z bash`. Clic 1: la variable del lado de `curl` (el error en vivo): el instalador anuncia "lkg". Clic 2: la variable del lado de `bash`: instala tu versión. Clic 3: la mochila de cada lado de la barra. Sin la etiqueta, sigue "lkg" (last-known-good). NemoClaw saca versiones cada 1 a 3 días: fijarla hace que tu instalación sea repetible. La key en local: `NVIDIA_INFERENCE_API_KEY=nvapi-...`.

---

## El onboarding en 9 pasos

:::diagrama c63-onboarding

Notas:
Pásala rápido. Clic 1: revisión previa (preflight) y gateway de OpenShell. Clic 2: agente (OpenClaw, Hermes o Deep Agents), proveedor y modelo, credencial, nombre del sandbox (`my-assistant`). Clic 3: revisión (Apply / Edit / Exit), canales y búsqueda web (opcional), política. Clic 4: Balanced por defecto. El tier Personal abre cualquier host en 80/443 sin aprobaciones: no lo uses para un agente que lee mensajes de desconocidos.

---

## Proveedores de inferencia

:::diagrama c63-proveedores

.lead El proveedor de inferencia te presta el modelo: la oficina a la que tu agente llama para consultar.

Notas:
Clic 1: el agente en su cuarto. Clic 2: la recepción (gateway) guarda la key: nunca entra al sandbox. Clic 3: NVIDIA Endpoints, probado, con tu key `nvapi-`. Clic 4: locales: Ollama (con un modelo validado) y vLLM (servidor en `:8000`) con limitaciones; NIM local, experimental (GPU NVIDIA + NGC). Modelos validados en Ollama: qwen3.6:35b, nemotron-3-nano:30b, qwen3.5:9b. Si las tool calls salen como texto, el servidor no devuelve tool_calls estructurados.

---

## Día 1 y día 2

:::diagrama c63-dias

Notas:
Clic 1: día 1, `nemoclaw my-assistant status` · `launch` · `logs --follow`, y `skill install ./skill-library/<skill>/`. Clic 2: día 2, tras reiniciar: `status` → `start` → `recover`; para actualizar: `backup-all` → `update` → `upgrade-sandboxes --auto`. Clic 3: nunca `openshell self-update`, `openclaw update` en el sandbox ni `nemoclaw start/stop` globales. NemoClaw fija una versión exacta de OpenShell: actualizarla por fuera rompe la compatibilidad.

---

## Si prefieres la terminal: errores al instalar

| Síntoma | Solución |
|---|---|
| `nemoclaw: command not found` | Terminal nueva o `source ~/.bashrc` |
| `Docker is not running` | `usermod -aG docker $USER && newgrp docker` |
| Exit 137 (OOM) | 16 GB o 4–8 GB de swap |
| `did not become ready within 180s` | `NEMOCLAW_SANDBOX_READY_TIMEOUT=600` |
| `Port 18789 is not available` | `--control-ui-port 19000` |

.lead Es opcional: cada uno tiene su receta en la página de la clase.

Notas:
Todos tienen receta en el cookbook opcional de la clase.

---

## Piezas de producción de NVIDIA

:::diagrama c63-piezas

Notas:
El sandbox queda en el centro. Clic 1: NIM, el modelo empaquetado con un servidor compatible con OpenAI en tu infraestructura; verifica tool calls y salida estructurada antes de cambiar. Clic 2: NeMo Retriever, búsqueda híbrida, reranker y chunking: la versión de producción del RAG en memoria de la 3.2. Clic 3: NeMo Guardrails, filtros de entrada y salida en la app. Clic 4: DGX Spark, agente 24/7 con inferencia local. Clic 5: Guardrails complementa al sandbox; quieres los dos.

---

## Cierra tu proyecto

:::diagrama c63-rubrica

.lead El checklist y la rúbrica completos están en la página de la clase.

Notas:
Un clic por criterio, con su nivel "Destacado": funciona, herramientas y skills (≥ 90 % de acierto medido), seguridad (bloqueo comprobado en logs, sin secretos en git), operación (cron + recuperación tras reinicio documentada), documentación (README con decisiones y límites). Clic 6: pide que publiquen su puntaje y qué mejorarían primero. Es el entregable final del curso. Muéstrala 20 segundos.

---

## Guarda tu trabajo y borra tu instancia

:::diagrama c63-guarda-borra

Notas:
Clic 1: guarda tus skills, tu SOUL.md y tus notas en tu computadora o en GitHub (forma de operador: `brev copy`). Clic 2: consola de Brev → GPUs → tu instancia → Delete (forma de operador: `brev delete`). No borres en cámara la instancia de grabación. Clic 3: borrada ya no cobra. Clic 4: detenida sigue cobrando el disco; borrada, lo de adentro se pierde.

---

## Por dónde seguir

:::diagrama c63-seguir

Notas:
Clic 1: conocimiento (chunking, recuperación y fidelidad). Clic 2: sustrato (MCP, Responses API, OTel GenAI, A2A). Clic 3: flotas y contención (N agentes acotados con Landlock, seccomp y netns). Clic 4: este curso es la lección 6 de la ruta de IA agéntica de NVIDIA. Elige el eje con el que tu proyecto tropieza más. Antes de producción: prueba los controles de la app y los del runtime por separado.
