# Preguntas frecuentes y solución de problemas

Curso **Seguridad de agentes con OpenShell y NemoClaw** (Platzi × NVIDIA DLI).

Esta página reúne los problemas reales que vas a encontrar en el curso: la API key, los errores del modelo, los notebooks, Brev, la conexión con el laboratorio, OpenClaw, OpenShell y la instalación local de NemoClaw. Cada entrada tiene la **causa**, la **solución** con comandos exactos y, cuando existe, la **fuente** oficial.

> **Antes de seguir:** NemoClaw está en *alpha* y publica versiones cada 1 a 3 días. Si un comando no coincide con lo que ves, revisa tu versión con `nemoclaw --version` y la documentación oficial. Las entradas marcadas con `[VERIFICAR EN LAB]` todavía no se confirmaron en el laboratorio del curso.

En los comandos, `<sandbox>` es el nombre de tu sandbox (en el laboratorio suele ser `my-assistant`; confírmalo con `nemoclaw list`) e `<instancia>` es el nombre de tu instancia en Brev (confírmalo con `brev ls`).

## Índice

1. [Cuenta y API key de NVIDIA Build](#api-key)
2. [Errores de la API (401, 403, 404, 410, 422, 429, 5xx, timeouts, `finish_reason`)](#errores-api)
3. [Notebooks, Colab y Python](#notebooks)
4. [Brev y el launchable](#brev)
5. [Conexión del curso de NVIDIA con el laboratorio](#conexion-laboratorio)
6. [OpenClaw: gateway, dashboard, pairing, workspace y sesiones](#openclaw)
7. [OpenShell y políticas](#openshell)
8. [NemoClaw instalado en tu máquina](#instalacion-local)
9. [Seguridad](#seguridad)
10. [Observabilidad y trazas](#trazas)
11. [Hermes en NemoClaw](#hermes)
12. [Cómo pedir ayuda bien](#pedir-ayuda)

### Los 10 problemas que más vas a ver

| Síntoma | Ir a |
|---|---|
| `401 Unauthorized` al llamar al modelo | [401](#e401) |
| Respuesta vacía con `finish_reason: "length"` | [finish_reason](#elength) |
| `429 Too Many Requests` | [429](#e429) |
| El notebook dice `Modo: MOCK` aunque pusiste tu key | [MOCK](#emock) |
| No sabes si tu instancia de Brev te sigue cobrando | [Costos](#ecostos) |
| El curso de NVIDIA no conecta con tu launchable | [Access session](#ecookie) |
| `OpenClaw is starting. Retrying in N seconds` | [503 starting](#estarting) |
| El dashboard pide *Pairing required* | [Pairing](#epairing) |
| `CONNECT tunnel failed, response 403` | [Red bloqueada](#e403tunnel) |
| Filtraste tu API key | [Key filtrada](#efiltrada) |

---

<a id="api-key"></a>
## 1. Cuenta y API key de NVIDIA Build

### ¿Dónde creo mi API key de NVIDIA?

**Causa:** el curso usa los modelos alojados en NVIDIA Build (`https://integrate.api.nvidia.com/v1`) y todos piden una key personal.

**Solución:**
1. Entra a `https://build.nvidia.com/?ncid=ref-dli-146986` e inicia sesión (o crea tu cuenta).
2. Abre tu perfil → **API Keys** → **Generate API Key**.
3. Copia la key completa. Empieza con `nvapi-`.
4. Guárdala en un gestor de contraseñas. No la pegues en el código.

La interfaz de build.nvidia.com cambia seguido; si no ves el menú **API Keys**, busca el botón **Get API Key** en la página de cualquier modelo. `[VERIFICAR EN LAB]`

**Fuente:** clase 1.2; [guía anterior de NemoClaw en Brev](https://github.com/NVIDIA/NemoClaw/blob/b00e2f21fe/docs/deployment/brev-web-ui.mdx).

### No me llega el SMS o la verificación de teléfono falla al crear la key

**Causa:** la verificación de teléfono de build.nvidia.com falla con algunos números fuera de EE. UU. o con mensajes como "number has requested too many". No es un problema de NemoClaw ni del curso.

**Solución:**
1. Espera unos minutos antes de reintentar; no pidas el código muchas veces seguidas.
2. Si sigue fallando, escribe a `help@build.nvidia.com` con tu correo registrado, los números que probaste y capturas de pantalla. También puedes usar `https://developer.nvidia.com/support`.
3. Mientras tanto, avanza con los notebooks en modo MOCK (corren sin key).

**Fuente:** [NVIDIA/NemoClaw#201](https://github.com/NVIDIA/NemoClaw/issues/201), [#214](https://github.com/NVIDIA/NemoClaw/issues/214).

### `Key should start with nvapi-`

**Causa:** pegaste otra cosa (un ID, una key de otro proveedor o la key cortada). La página del curso de NVIDIA valida el prefijo cuando usas el endpoint por defecto.

**Solución:** vuelve a copiar la key completa desde build.nvidia.com, sin espacios ni comillas. En los notebooks del curso verás el aviso `⚠  Tu key no empieza con 'nvapi-'`. Si la perdiste, genera una nueva: NVIDIA no te la vuelve a mostrar. `[VERIFICAR EN LAB]`

**Fuente:** `web/nemoclaw/scripts/_keypanel.js` de [NVDLI/NemoClawDLI](https://github.com/NVDLI/NemoClawDLI); `tools/notebooks/comun.py` de este repo.

### ¿Dónde guardo mi API key? ¿Sirve la misma en todo el curso?

**Causa:** la key es un secreto y cada entorno la lee de un lugar distinto. Es la **misma** key `nvapi-` en todos lados; cambia solo el nombre de la variable.

**Solución:**
- **Google Colab:** icono de llave 🔑 (*Secrets*) → nuevo secreto `NVIDIA_API_KEY` → activa el acceso del notebook.
- **Tu máquina:** copia `.env.example` como `.env` en la raíz del repo y pon tu key en `NVIDIA_API_KEY`. `.env` ya está en `.gitignore`.
- **Terminal:** `export NVIDIA_API_KEY=nvapi-xxxxxxxx` (solo dura esa sesión).
- **Curso web de NVIDIA:** la página guarda la key solo en la pestaña (`sessionStorage`) y la descarta al cerrarla.
- **Launchable de Brev:** la pegas en el asistente de configuración, con **NVIDIA Cloud** seleccionado.
- **NemoClaw en tu máquina:** el instalador y `nemoclaw onboard` leen **`NVIDIA_INFERENCE_API_KEY`** y la registran en el gateway de OpenShell. (`NVIDIA_API_KEY` solo aparece documentada para el onboarding diferido; no cuentes con ella.)

Si rotas la key, actualízala en todos estos lugares.

**Fuente:** `.env.example` de este repo; [credential storage de NemoClaw](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/security/credential-storage); [commands](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands) ("Onboarding Configuration").

### ¿Cómo pruebo rápido si mi key funciona?

**Solución:** una sola llamada con `curl` desde tu terminal:

```bash
export NVIDIA_API_KEY=nvapi-xxxxxxxx
curl https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"nvidia/nemotron-3.5-lightning-30b-a3b","messages":[{"role":"user","content":"Di hola"}],"max_tokens":1024}'
```

Deberías ver un JSON con `choices[0].message.content`. Si ves `401` o `403`, revisa la sección de [errores de la API](#errores-api).

**Fuente:** clase 1.2; ruta y modelo por defecto en `web/nemoclaw/scripts/_shared.js` de NVDLI/NemoClawDLI.

### ¿Cuántos créditos o solicitudes por minuto me da la cuenta gratuita?

**Causa:** NVIDIA Build limita el uso por cuenta (créditos y solicitudes por minuto). Los números cambian y no están en la documentación que revisamos.

**Solución:** revisa el uso y el límite en tu cuenta de build.nvidia.com. Para no gastarlos: pon siempre un límite de pasos a tus loops de agente (clase 2.1) y no ejecutes celdas en ráfaga. Si recibes `429`, espera antes de reintentar. `[VERIFICAR EN LAB]`

**Fuente:** sección "If a model request fails" de `web/nemoclaw/index.html` en NVDLI/NemoClawDLI.

---

<a id="errores-api"></a>
## 2. Errores de la API

En los notebooks del curso, la función `diagnostico()` traduce cada error a "qué pasó + qué hacer". En el curso web de NVIDIA, el mensaje se ve así: `Model request failed: HTTP <status>. <motivo>`.

<a id="e401"></a>
### `401 Unauthorized` (o `Key rejected ✗` en el curso de NVIDIA)

**Causa:** la key no es válida: está incompleta, tiene espacios o comillas, la revocaste o la regeneraste (la vieja deja de servir). En el curso web, el mensaje es "The model credential was rejected or lacks access."

**Solución:**
1. Copia otra vez la key completa (`nvapi-…`) sin espacios.
2. Revisa qué variable lee tu código: `echo ${NVIDIA_API_KEY:0:6}` debe imprimir `nvapi-`.
3. En Colab, confirma que el secreto `NVIDIA_API_KEY` tiene activado el acceso del notebook.
4. Más esperas o más reintentos **no** arreglan una key inválida.

**Fuente:** `modelHttpFailure` en `web/nemoclaw/scripts/_shared.js` (NVDLI/NemoClawDLI).

### `403 Forbidden` al llamar a un modelo

**Causa:** la key es válida, pero no tiene acceso a ese modelo o la cuenta no tiene cuota.

**Solución:** prueba con el modelo del curso (`nvidia/nemotron-3.5-lightning-30b-a3b`). Revisa tu cuenta y tus créditos en build.nvidia.com. Si el error aparece **dentro del sandbox** como `CONNECT tunnel failed, response 403`, no es la API: es la política de red (ver [OpenShell](#e403tunnel)).

**Fuente:** `_shared.js` de NVDLI/NemoClawDLI; [troubleshooting de NemoClaw](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/troubleshooting).

### `404 Not Found`

**Causa:** el ID del modelo está mal escrito, el modelo no está disponible para tu cuenta o la ruta está mal (por ejemplo, `BASE_URL` sin `/v1` o con `/v1` duplicado).

**Solución:**
- `BASE_URL` debe ser exactamente `https://integrate.api.nvidia.com/v1`.
- Copia el ID exacto del catálogo de build.nvidia.com (por ejemplo `nvidia/nemotron-3-embed-1b` para embeddings).
- Si el modelo aparece en el catálogo pero da 404, elige otro: no todos los modelos están desplegados para todas las cuentas.

**Fuente:** `docs/inference/verify-inference-route.mdx` en [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw/blob/main/docs/inference/verify-inference-route.mdx).

### `410 Gone`

**Causa:** NVIDIA retiró ese modelo del endpoint gratuito. Le pasó al curso de NVIDIA con `nvidia/nemotron-3-nano-30b-a3b`. Los modelos por defecto cambian con el tiempo.

**Solución:** cambia `NVIDIA_MODEL` (o la variable `MODEL` del notebook) por un modelo vigente del catálogo. El de este curso es `nvidia/nemotron-3.5-lightning-30b-a3b`. Para embeddings, usa `nvidia/nemotron-3-embed-1b`.

**Fuente:** issue #106 de [NVDLI/NemoClawDLI](https://github.com/NVDLI/NemoClawDLI/issues/106).

### `422 Unprocessable Entity`

**Causa:** el servidor entendió la solicitud, pero algún argumento tiene un formato inválido: un esquema de tool mal formado o, en embeddings, falta `input_type`.

**Solución:** en embeddings, envía `input_type="query"` para preguntas y `"passage"` para documentos (la función `embed()` del curso ya lo hace). En tools, revisa que `parameters` sea un JSON Schema válido. Lee el cuerpo del error: casi siempre nombra el campo. `[VERIFICAR EN LAB]`

**Fuente:** `tools/notebooks/comun.py` de este repo; formato de embeddings en `web/nemoclaw/scripts/_rag.js` (NVDLI/NemoClawDLI).

<a id="e429"></a>
### `429 Too Many Requests`

**Causa:** mandaste demasiadas solicitudes por minuto. Pasa con loops sin límite, celdas que se ejecutan en ráfaga o varios notebooks a la vez.

**Solución:**
1. Espera unos segundos y reintenta una sola vez.
2. Respeta el encabezado `Retry-After` si viene.
3. Pon un límite de pasos al loop del agente y un `time.sleep()` entre llamadas en pruebas masivas.
4. En el curso de NVIDIA, **Request handling** permite hasta 5 reintentos automáticos (solo para errores de red, 429 y 5xx).

**Fuente:** `_shared.js` y sección "If a model request fails" de `web/nemoclaw/index.html` (NVDLI/NemoClawDLI).

### `500`, `502`, `503` o `504` del modelo

**Causa:** falla del lado del proveedor o del relay, o el modelo está arrancando. En el curso de NVIDIA, algunos 503/504 venían del relay del DLI, que corta si el modelo no empieza a responder en unos 10 segundos.

**Solución:** espera 30 a 60 segundos y reintenta una vez. Si persiste, prueba otro modelo o vuelve más tarde. Si el 502 sale al probar el laboratorio, ve a [Conexión del curso con el laboratorio](#conexion-laboratorio).

**Fuente:** `_shared.js` e issue #151 de [NVDLI/NemoClawDLI](https://github.com/NVDLI/NemoClawDLI/issues/151).

### Timeout: `Model stream stopped producing data for Ns` o `Network or endpoint failure after N attempt(s)`

**Causa:** no llegó respuesta (o el stream se detuvo) dentro del tiempo de espera configurado. Puede ser tu red, una VPN o proxy corporativo, o un modelo lento.

**Solución:**
- Revisa tu conexión y desactiva la VPN para probar.
- En el curso de NVIDIA, sube la espera en **Request handling** (de 5 a 300 s; por defecto 60 s).
- En los notebooks, el cliente usa `timeout=60`; baja `max_tokens` o reintenta.

**Fuente:** `_shared.js` de NVDLI/NemoClawDLI.

<a id="elength"></a>
### La respuesta llega vacía y `finish_reason` es `"length"`

**Causa:** el modelo del curso **razona antes de responder** y gasta tokens en ese razonamiento. Con un `max_tokens` pequeño se le acaban antes de escribir la respuesta: `content` queda vacío.

**Solución:** sube `max_tokens` (el curso de NVIDIA usa 8196 en las celdas y 1024 en la prueba de conexión; los notebooks usan 4096). El helper `chat()` del curso te avisa con `⚠  finish_reason=length sin contenido`.

**Fuente:** comentario sobre `chat()` en `web/nemoclaw/scripts/_shared.js` (NVDLI/NemoClawDLI).

### `Failed to fetch` o error de CORS en el curso web de NVIDIA

**Causa:** el navegador bloqueó la llamada directa al modelo porque el endpoint no permite el origen de la página. Para eso existe el relay del DLI.

**Solución:** en el panel de la API key, activa **Use the NVIDIA DLI browser relay**. El relay reenvía tu solicitud a NVIDIA; no te da una key ni acceso extra. Si abriste el curso como archivo local (`file:`), sírvelo con `python3 -m http.server -d web 8000` y abre `http://localhost:8000/nemoclaw/`.

**Fuente:** secciones 1.4 y 3.2 del análisis del curso; `_shared.js` de NVDLI/NemoClawDLI.

---

<a id="notebooks"></a>
## 3. Notebooks, Colab y Python

<a id="emock"></a>
### El notebook dice `Modo: MOCK` aunque configuré mi key

**Causa:** la celda de configuración no encontró `NVIDIA_API_KEY`. En Colab suele ser porque el secreto no tiene acceso al notebook o tiene otro nombre. En local, porque `.env` no está en la raíz del repo.

**Solución:**
- **Colab:** 🔑 *Secrets* → el nombre debe ser exactamente `NVIDIA_API_KEY` → activa el acceso del notebook → vuelve a ejecutar la primera celda.
- **Local:** el notebook busca `.env` en la carpeta actual y en `../../.env`. Ejecuta Jupyter desde la carpeta de la clase o pon `.env` en la raíz del repo.
- Después de cambiar la key, ejecuta otra vez **las dos primeras celdas** (configuración y cliente).

**Fuente:** celdas `SETUP` y `MOCK` en `tools/notebooks/comun.py` de este repo.

### `NameError: name 'chat' is not defined` (o `client`, `MODEL`)

**Causa:** ejecutaste una celda de la mitad sin correr antes las celdas de configuración. También pasa después de reiniciar el kernel.

**Solución:** ejecuta en orden la celda **Configuración** y la celda **Cliente** (o *Entorno de ejecución → Ejecutar todas las celdas anteriores*). Cada notebook está pensado para correr de arriba abajo.

**Fuente:** diseño de los notebooks en `tools/notebooks/comun.py`.

### `ModuleNotFoundError: No module named 'openai'` (o `dotenv`)

**Causa:** falta instalar dependencias en tu entorno local. En Colab, la primera celda las instala sola.

**Solución:**

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Luego reinicia el kernel y elige el intérprete de `.venv`.

**Fuente:** `requirements.txt` de este repo.

### El notebook no encuentra `datos/faq/` en Colab

**Causa:** Colab abre solo el notebook, no el repo completo.

**Solución:** no tienes que hacer nada: cada notebook trae una muestra de la FAQ incrustada y, si existe `../../datos/faq/`, carga el corpus completo. Si quieres el corpus completo en Colab, clona el repo en la primera celda con `!git clone <url-del-repo>`.

**Fuente:** brief del curso (sección notebooks).

### Mi agente se quedó en un loop y gastó muchas llamadas

**Causa:** un loop de agente sin condición de salida sigue llamando al modelo mientras el modelo pida tools.

**Solución:** detén la celda (botón ■ o *Interrumpir*). Agrega siempre un máximo de pasos (`for paso in range(MAX_PASOS):`) y sal cuando `finish_reason` sea `"stop"`. Lo construyes en la clase 2.1.

**Fuente:** clases 2.1 y 2.2 de este curso; lección 01b del curso de NVIDIA.

---

<a id="brev"></a>
## 4. Brev y el launchable

<a id="ecostos"></a>
### ¿Cuánto me cuesta el laboratorio en Brev?

**Causa:** Brev cobra por hora mientras la instancia está encendida. El launchable de NemoClaw usa una instancia **solo CPU** (sin GPU), `n2d-standard-4` (4 vCPU, 16 GiB) en GCP, que en las pruebas de NVIDIA aparece como **Free**.

**Solución:**
- Antes de desplegar, mira el costo por hora en la página de despliegue.
- Referencia pública de precios de CPU: 4 vCPU / 16 GB ≈ **USD 0.15/h**; el disco cuesta **USD 0.0001314 por GB-hora** mientras exista la instancia.
- El curso de NVIDIA anuncia un crédito de **USD 1.00** por usuario para los primeros 25 000 usuarios, suficiente para los 4 módulos (~4 h).

Confirma en la pantalla de despliegue si tu instancia es gratuita. `[VERIFICAR EN LAB]`

**Fuente:** [precios de launchables](https://www.nvidia.com/en-us/launchables/pricing); [NemoClaw#11536](https://github.com/NVIDIA/NemoClaw/issues/11536); `web/nemoclaw/index.html` de NVDLI/NemoClawDLI.

### ¿Qué me cobra Brev si la detengo y qué si la borro?

**Causa:** son tres estados distintos.

**Solución:**

| Estado | Cómputo | Disco | Datos |
|---|---|---|---|
| **Running** (encendida) | Se cobra | Se cobra | Se conservan |
| **Stopped** (detenida) | No se cobra | **Se sigue cobrando** | Se conservan (excepto `/tmp`) |
| **Deleted** (borrada) | No | No | **Se pierden para siempre** |

Al terminar cada clase: detén la instancia. Si no vas a volver en días, bórrala (después de guardar tu trabajo en git).

**Fuente:** [Brev: GPU Instances](https://docs.nvidia.com/brev/latest/concepts/gpu-instances); [Console Reference › Billing](https://docs.nvidia.com/brev/latest/guides/console-reference).

### ¿Cómo detengo o borro mi instancia?

**Solución:**
- **Consola:** brev.nvidia.com → **GPUs** → tu instancia → **Stop** (o **Delete**).
- **CLI:**

```bash
brev ls                     # nombre y estado
brev stop <instancia>       # detener
brev delete <instancia>     # borrar (irreversible)
brev ls                     # confirma STOPPED o que ya no aparece
```

Si `brev stop` responde `instance "<instancia>" does not support stop.`, ese tipo de instancia no se puede detener: la única forma de dejar de pagar es `brev delete`. No sabemos aún si la instancia gratuita del launchable se puede detener. `[VERIFICAR EN LAB]`

**Fuente:** `pkg/cmd/stop/stop.go` de [brevdev/brev-cli](https://github.com/brevdev/brev-cli); [guía anterior de NemoClaw en Brev](https://github.com/NVIDIA/NemoClaw/blob/b00e2f21fe/docs/deployment/brev-web-ui.mdx).

### ¿Qué pasa si se me acaban los créditos? ¿Cómo cargo un código?

**Causa:** los créditos de Brev son prepagados y se comparten en toda la organización. Cuando se agotan, Brev actúa sobre tus recursos.

**Solución:** Brev te avisa por correo, **pausa** las instancias que se pueden detener y **borra** las que no. Si a las 24 horas sigues sin saldo, borra todos los recursos y los datos no se recuperan.
- Revisa tu saldo en **Billing** y deja la recarga automática apagada si usas créditos prepagados.
- Para canjear un código: **Billing → Credits → Redeem a credit code**, o desde la CLI `brev redeem <código>`. Antes, confirma que estás en la organización correcta.

**Fuente:** [Console Reference › Billing](https://docs.nvidia.com/brev/latest/guides/console-reference); `pkg/cmd/redeem` de [brevdev/brev-cli](https://github.com/brevdev/brev-cli).

### `You have run out of credits` pero sí tengo créditos

**Causa:** tienes activa otra organización de Brev. Los créditos son por organización.

**Solución:**

```bash
brev ls orgs           # lista tus organizaciones
brev set <org>         # activa la que tiene los créditos
```

En la consola, cambia de organización en el selector superior.

**Fuente:** [brevdev/brev-cli#390](https://github.com/brevdev/brev-cli/issues/390); `pkg/cmd/set/set.go` de brev-cli.

### Mi instancia se queda en **Deploying** o **Waiting**, no hay capacidad o no vuelve a arrancar

**Causa:** el proveedor tarda en asignar la máquina, falló el despliegue (`context deadline exceeded`) o no hay capacidad. Al reiniciar una instancia detenida, Brev intenta el mismo tipo, proveedor y región; si no hay capacidad, el arranque falla y tus datos quedan inaccesibles hasta que vuelva.

**Solución:**
1. Ten paciencia: el despliegue completo del launchable de NemoClaw tarda unos 5 a 15 minutos (la configuración del agente sola, unos 5).
2. Revisa `brev ls` y la pestaña **Activity Logs** de la instancia.
3. Si sigue atascada, bórrala, espera 30 segundos y créala de nuevo (con otro nombre, región o proveedor; `brev search cpu --sort price` lista opciones).
4. Antes de reintentar, confirma con `brev ls` que no quedó una instancia duplicada cobrando.
5. Si persiste, escribe a `brev-support@nvidia.com` con tu ID de organización, la instancia y la hora.

El launchable de NemoClaw es solo CPU, así que los problemas de capacidad son menos frecuentes que con GPU.

**Fuente:** [Instance Stuck in Waiting](https://docs.nvidia.com/brev/latest/troubleshooting/instances-gpus/instance-stuck-in-waiting-state); [Brev: GPU Instances](https://docs.nvidia.com/brev/latest/concepts/gpu-instances); [brev-cli#382](https://github.com/brevdev/brev-cli/issues/382).

### La página del launchable se queda en 0 %, muestra un **RETRY** rojo, pierde el progreso o da `503 ... no_healthy_upstream`

**Causa:** son errores conocidos del asistente de configuración del launchable. El `503 ... no_healthy_upstream` (aunque Brev diga HEALTHY) aparece cuando el proxy de la instancia todavía no ve el servicio; es intermitente.

**Solución:**
- No refresques la pestaña durante la configuración.
- **No hagas clic en RETRY** si el registro de actividad muestra que el paso terminó: RETRY reconstruye todo el sandbox.
- Sigue el registro de actividad hasta ver "AGENT CREATED SUCCESSFULLY".
- Con el 503, espera un minuto y recarga. Si sigue igual varios minutos, despliega una instancia nueva.

**Fuente:** [NemoClaw#11536](https://github.com/NVIDIA/NemoClaw/issues/11536), [#8101](https://github.com/NVIDIA/NemoClaw/issues/8101), [#11167](https://github.com/NVIDIA/NemoClaw/issues/11167), [#11535](https://github.com/NVIDIA/NemoClaw/issues/11535).

### `brev shell <instancia> --host` se queda esperando (timeout)

**Causa:** desde la versión 0.6.331 de la CLI de Brev cambió la ruta `--host`, y en el launchable de NemoClaw (modo VM) no responde.

**Solución:** usa el comando sin `--host`:

```bash
brev shell <instancia>
```

**Fuente:** [NemoClaw#11534](https://github.com/NVIDIA/NemoClaw/issues/11534).

### `ssh: Could not resolve hostname <instancia>` o la instancia no aparece en la CLI

**Causa:** la CLI no sincronizó la lista de instancias (por ejemplo, la creaste en la consola), la IP cambió al reiniciar o la línea `Include` que Brev agrega a `~/.ssh/config` quedó **dentro** de un bloque `Host` ajeno y SSH no la lee.

**Solución:**
1. `brev ls` (¿está RUNNING?) y luego `brev refresh` (sincroniza y reescribe `~/.brev/ssh_config`).
2. Si sigue fallando, haz una copia: `cp ~/.ssh/config ~/.ssh/config.bak`.
3. Mueve la línea `Include` de Brev al **inicio** de `~/.ssh/config`, antes del primer `Host` o `Match`.
4. Prueba `brev shell <instancia>`.

**Fuente:** [Brev: Common Issues](https://docs.nvidia.com/brev/latest/troubleshooting/common-issues); [NemoClaw#13090](https://github.com/NVIDIA/NemoClaw/issues/13090).

### `brev login` no termina o SSH responde `Permission denied (publickey)`

**Causa:** el navegador no abrió la URL de login, las cookies de brev.nvidia.com están viejas o la llave `~/.brev/brev.pem` está dañada.

**Solución:**
- `brev login --skip-browser` imprime la URL para abrirla a mano.
- Si el login falla o la sesión venció: `brev logout && brev login`, o borra las cookies de brev.nvidia.com.
- Con `Permission denied (publickey)`: respalda la llave, ejecuta `chmod 600 ~/.brev/brev.pem` y entra con el token de **Settings → CLI**: `brev login --token "<TOKEN>"`.
- No instales la CLI con `sudo`.

**Fuente:** [Brev: Common Issues](https://docs.nvidia.com/brev/latest/troubleshooting/common-issues); [macOS SSH auth](https://docs.nvidia.com/brev/latest/troubleshooting/cli-installation/cli-ssh-authentication-macos); `pkg/cmd/login/login.go` de brev-cli.

### Después de detener y volver a encender la instancia, el agente no responde

**Causa:** tras un reinicio de la VM, Docker, el gateway de OpenShell, el sandbox y los túneles pueden no arrancar solos.

**Solución:** entra con `brev shell <instancia>` y ejecuta:

```bash
sudo systemctl start docker && docker info
nemoclaw <sandbox> status          # también arranca el gateway
nemoclaw <sandbox> start           # si el sandbox quedó detenido
nemoclaw <sandbox> recover         # si el gateway o el forward no responden
nemoclaw <sandbox> connect --probe-only
```

**Fuente:** [Deploy NemoClaw to a Headless Server](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/deployment/deploy-to-headless-server); troubleshooting "Reconnect after a host reboot".

---

<a id="conexion-laboratorio"></a>
## 5. Conexión del curso de NVIDIA con el laboratorio

Esto aplica a la lección 3a del curso web de NVIDIA (**Connect NemoClaw**) y a las clases 4.x de este curso.

### ¿Qué pongo en **Base URL**? (o `A NemoClaw launchable is not a model API`)

**Causa:** el curso solo acepta la URL de la app NemoClaw de tu launchable, y la reduce al origen (quita rutas como `/onboard`). Es distinta de la ruta del modelo: si pegas el launchable en **Chat API base URL**, verás `A NemoClaw launchable is not a model API`.

**Solución:** deja la ruta del modelo en `https://integrate.api.nvidia.com/v1` y copia la URL de la app desde Brev en el campo **Base URL** de "Connect NemoClaw" (lección 3a). Tiene una de estas formas:
- `https://nemoclaw-<id>.brevlab.com` (Cloudflare Access)
- `https://nemoclaw-<id>.apps.run.brev.nvidia.com` (Pomerium)
- `https://nemoclaw-<id>.gobrev.dev` (Brev Skybridge, launchables nuevos)

Sin `/v1` al final. Si ves `Use the NemoClaw App URL: https://nemoclaw-<id>.brevlab.com or https://nemoclaw-<id>.apps.run.brev.nvidia.com`, pegaste otra URL de Brev (la de Jupyter, la de la consola, etc.).

**Fuente:** `isOpenClawLaunchableHost` en `web/nemoclaw/scripts/_connection.js` y `normalizeModelApiBaseUrl` en `_shared.js` (NVDLI/NemoClawDLI).

<a id="ecookie"></a>
### ¿Qué es **Access session** y de dónde saco la cookie?

**Causa:** tu launchable está detrás de un login (Cloudflare Access o Pomerium). Cuando la página del curso está alojada en otro dominio, no puede ver tu sesión del navegador y necesita el valor de la cookie.

**Solución:**
1. Abre tu launchable en el mismo navegador e inicia sesión.
2. Abre DevTools:
   - Chrome, Edge o Brave: **Application → Storage → Cookies** → el origen del launchable.
   - Firefox: **Storage → Cookies**.
   - Safari: activa las funciones de desarrollador (**Settings → Advanced**) → Web Inspector → **Storage → Cookies**.
3. Busca la cookie según tu host:

| Host | Cookie |
|---|---|
| `*.brevlab.com` | `CF_Authorization` |
| `*.apps.run.brev.nvidia.com` | `_pomerium` |
| `*.gobrev.dev` | `__Host-skybridge-brev-prd` |

4. Copia **solo el Value completo**, no todo el encabezado `Cookie`.
5. Pégalo en **Access session** y pulsa **Test connection**.

El valor queda solo en esa pestaña. **Es una credencial:** no la compartas ni la pegues en capturas.

**Fuente:** lección 03a del curso de NVIDIA; `_connection.js` y `_openclaw.js` de NVDLI/NemoClawDLI.

### ¿Qué revisa cada una de las 4 rutas del **Test connection**?

**Solución:** las revisa en orden. Si una falla, abre su evidencia ("Redacted request and response"):

| # | Ruta | Qué confirma | Si falla |
|---|---|---|---|
| 1 | `GET /api/agent` | Que tu sesión de acceso funciona, y obtiene el token del gateway | Cookie vencida o equivocada, o el runtime está arrancando |
| 2 | WebSocket `/cli/gateway` | Que el gateway responde al desafío y acepta el token | Sesión vencida o transporte bloqueado |
| 3 | WebSocket `/ws/terminal` | Que puedes abrir una terminal en la VM (imprime `__NEMOCLAW_CONNECTION_READY__`) | Sesión de acceso inválida o la ruta de terminal no corre |
| 4 | `GET /healthz` | La salud general del launchable | El servicio no está sano |

Las cuatro en verde = "Connection ready. Metadata, gateway, terminal, and health checks passed."

**Fuente:** `runOpenClawConnectionAudit` en `web/nemoclaw/scripts/_openclaw.js` (NVDLI/NemoClawDLI).

<a id="estarting"></a>
### `OpenClaw is starting. Retrying in N seconds. Use Stop to cancel.` (503 `{"status":"starting"}`)

**Causa:** el launchable responde, pero OpenClaw todavía está arrancando.

**Solución:** no hagas nada: el curso reintenta solo (respeta `Retry-After` o cada 15 s) hasta 30 minutos. Si pasan más de 15 minutos, revisa en Brev que la instancia esté RUNNING y mira los registros de arranque.

**Fuente:** `openclawBootstrapRequest` en `_openclaw.js` (NVDLI/NemoClawDLI).

### `OpenClaw ⚠`: `session expired or unreachable`, `no challenge arrived within 30s` o `Expected JSON but received an HTML page`

**Causa:** tu sesión de acceso (la cookie) venció o el launchable se detuvo. Cuando la cookie ya no sirve, en vez de JSON llega la página de inicio de sesión de Cloudflare o Pomerium, y el curso dice `The launchable needs a fresh <cookie> browser session`. El curso revisa la sesión al cargar cada página y al volver a la pestaña.

**Solución:**
1. Confirma en Brev que la instancia está RUNNING.
2. Abre el launchable en una pestaña e inicia sesión otra vez.
3. Copia un valor **nuevo** de la cookie y pégalo en **Access session** (lección 3a). Con Pomerium, si aparece `Pomerium did not accept the access session`, usa un `_pomerium` recién copiado.
4. Pulsa **Test connection** de nuevo.

**Fuente:** `updateClawPill` y `GW_CONNECT` en `web/nemoclaw/scripts/_openclaw.js` (NVDLI/NemoClawDLI).

### La conexión al launchable `gobrev.dev` no funciona

**Causa:** los launchables nuevos usan el host `nemoclaw-<id>.gobrev.dev` con la cookie `__Host-skybridge-brev-prd`. El curso de NVIDIA lo soporta desde octubre de 2026, pero los relays que opera NVIDIA también deben actualizarse.

**Solución:** recarga el curso para tener la última versión, usa la cookie `__Host-skybridge-brev-prd` y vuelve a probar. Si falla solo en este tipo de host, repórtalo en el issue #165 del curso de NVIDIA. `[VERIFICAR EN LAB]`

**Fuente:** [NVDLI/NemoClawDLI#165](https://github.com/NVDLI/NemoClawDLI/issues/165).

### La comprobación agota el tiempo o devuelve `502`

**Causa:** un timeout o un 502 por sí solos no dicen la causa. Puede ser el gateway, el sandbox o el modelo.

**Solución:**
1. Abre la ruta que falló y lee su evidencia.
2. Ejecuta la celda 🩺 **Health check**.
3. Si marca `✗ DEGRADED`, ejecuta 🛠 **Recover**. Si no basta, pon `DO_RESTART = true`, espera unos 40 s y vuelve a conectar.
4. Si sigue fallando, el sandbox está trabado por debajo del gateway: relanza el launchable desde Brev.
5. Un 502 en `/v1/chat/completions` indica que el backend del modelo no responde: revisa que la key de NVIDIA esté bien cargada en el launchable.

**Fuente:** `mountGwRecover` en `_openclaw.js`; lección 03a del curso de NVIDIA.

### `Another turn is active on this gateway connection.`

**Causa:** mandaste un mensaje mientras el agente todavía procesa el anterior.

**Solución:** espera a que termine el turno o pulsa ■ **Stop** y vuelve a enviar. Si el turno se quedó colgado, revisa con 🩺 **Health check**: un comando esperando aprobación se ve igual que un cuelgue.

**Fuente:** `courseTurn` en `_openclaw.js` (NVDLI/NemoClawDLI).

### Veo `cannot create /proc/self/oom_score_adj: Permission denied` en la salida del agente

**Causa:** es ruido del sistema dentro del sandbox, no un error de tu ejercicio.

**Solución:** ignóralo. El curso de NVIDIA ya filtra la variante `/bin/sh`, y hay un issue abierto para la variante `/usr/bin/sh`.

**Fuente:** [NVDLI/NemoClawDLI#100](https://github.com/NVDLI/NemoClawDLI/issues/100).

### `Cleanup incomplete; run Remove owned job` en el ejercicio de cron

**Causa:** el trabajo programado se creó, pero no se pudo borrar al final (por ejemplo, cerraste la página o se cortó la conexión).

**Solución:** vuelve a conectar al **mismo** launchable y ejecuta la celda **Retry removal of the owned job**. Guarda el ID que imprime el mensaje. Un cron que se queda vivo sigue ejecutándose sin supervisión.

**Fuente:** lección 03c del curso de NVIDIA (`03c-always-on.html`).

---

<a id="openclaw"></a>
## 6. OpenClaw: gateway, dashboard, pairing, workspace y sesiones

### ¿Cómo abro el dashboard de OpenClaw (también desde Brev)?

**Solución:** el dashboard escucha en `http://127.0.0.1:18789/` (si el puerto está ocupado, NemoClaw usa el siguiente libre hasta 18799). Necesita un token:

```bash
nemoclaw <sandbox> dashboard-url --quiet
```

La URL incluye el token en el fragmento `#token=`: trátala como una contraseña. Si el sandbox está en un servidor remoto o en Brev, abre antes un túnel desde tu computadora:

```bash
brev port-forward <instancia> -p 18789:18789
# o con SSH:  ssh -N -L 18789:127.0.0.1:18789 <instancia>
```

Nunca abras el puerto 8080 (gateway) a internet ni uses `brev ports open ... --public` para el dashboard.

**Fuente:** [quickstart de NemoClaw](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/get-started/quickstart); [headless guide](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/deployment/deploy-to-headless-server); `pkg/cmd/portforward/portforward.go` de brev-cli.

### `ERR_CONNECTION_REFUSED` en `localhost:18789`

**Causa:** el *port forward* del dashboard se cayó (o no abriste el túnel desde tu máquina).

**Solución:**

```bash
openshell forward list            # ¿existe el forward del 18789?
nemoclaw <sandbox> recover        # restaura el gateway y los forwards administrados
```

Si estás en Brev, revisa también que siga activo tu `brev port-forward` o `ssh -L`.

**Fuente:** [NemoClaw#1088](https://github.com/NVIDIA/NemoClaw/issues/1088); [CLI selection guide](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/cli-selection-guide).

<a id="epairing"></a>
### *Pairing required*, *Device pairing required* o `scope upgrade pending approval`

**Causa:** OpenClaw exige que cada navegador o CLI se empareje con el gateway. Desde OpenClaw 2026.9.1 el emparejamiento es obligatorio: `NEMOCLAW_DISABLE_DEVICE_AUTH=1` ya **no** lo desactiva. NemoClaw aprueba solo clientes conocidos (`cli`, `openclaw-cli`, `openclaw-control-ui`) con permisos de lectura, escritura y emparejamiento. Si un comando pide más (por ejemplo `operator.admin`), verás `gateway connect failed: GatewayClientRequestError: scope upgrade pending approval (requestId: ...)`.

**Solución:**
1. Espera unos minutos y recarga: el aprobador automático suele resolverlo. Si fue un comando, vuelve a ejecutarlo sin cambios.
2. En el dashboard: **Overview → Gateway Access → Connect**.
3. Desde la terminal:

```bash
nemoclaw <sandbox> connect
openclaw devices list --json          # busca el requestId pendiente
openclaw devices approve <requestId>  # aprueba SOLO ese requestId
```

Revisa el cliente y los permisos antes de aprobar. Para acceso remoto, usa un túnel a `127.0.0.1:18789` en vez de exponer el dashboard.

**Fuente:** [gateway authentication controls](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/security/gateway-authentication-controls); troubleshooting "`scope upgrade pending approval`" y "`NEMOCLAW_DISABLE_DEVICE_AUTH=1` does not disable pairing"; [NemoClaw#13092](https://github.com/NVIDIA/NemoClaw/issues/13092).

### ¿Dónde está el workspace del agente y qué archivos tiene?

**Solución:** dentro del sandbox, en `/sandbox/.openclaw/workspace/`:

| Archivo | Para qué sirve |
|---|---|
| `SOUL.md` | Personalidad y reglas del agente |
| `AGENTS.md` | Instrucciones de operación |
| `TOOLS.md` | Notas de uso de cada tool |
| `USER.md` | Datos sobre ti (empieza vacío) |
| `HEARTBEAT.md` | Instrucciones del heartbeat (~cada 30 min) |
| `memory/AAAA-MM-DD.md` | Notas diarias que el agente va agregando |
| `MEMORY.md` | Memoria de largo plazo, curada |
| `skills/<nombre>/SKILL.md` | Skills instaladas |

Para verlo: `nemoclaw <sandbox> connect` y luego `ls -la /sandbox/.openclaw/workspace`.

**Fuente:** lección 03b del curso de NVIDIA.

### El agente "olvidó" lo que le dije

**Causa:** OpenClaw tiene dos memorias. El historial de la conversación vive en la **sesión** (identificada por su `sessionKey`). Lo que sobrevive entre sesiones es lo que el agente escribe en archivos (`MEMORY.md`, `memory/`). Si abres una sesión nueva o la reinicias, el historial anterior no está.

**Solución:**
- Usa la misma clave de sesión para continuar una conversación.
- Pídele que guarde lo importante en `MEMORY.md`.
- Para ver o reiniciar sesiones:

```bash
nemoclaw <sandbox> sessions list
nemoclaw <sandbox> sessions reset main     # archiva y empieza de cero
```

**Fuente:** lecciones 03a y 03b del curso de NVIDIA; [commands](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands) (`sessions`).

### `EACCES: permission denied` al cambiar `/sandbox/.openclaw/openclaw.json`

**Causa:** en versiones viejas el archivo era de solo lectura. Desde la v0.0.130, OpenClaw es dueño de `openclaw.json` después del primer arranque, pero hay que cambiarlo con sus propios comandos.

**Solución:**

```bash
nemoclaw <sandbox> connect
openclaw config set <ruta.de.la.clave> <valor>
openclaw config unset <ruta.de.la.clave>
```

No guardes keys de proveedores en `openclaw.json`: dentro del sandbox se pueden leer. Si tu versión es anterior a la v0.0.130, actualiza (ver [Actualizar NemoClaw](#instalacion-local)).

**Fuente:** [NemoClaw#719](https://github.com/NVIDIA/NemoClaw/issues/719); troubleshooting "Change OpenClaw Configuration Inside the Sandbox".

### ¿Cómo hablo con el agente desde la terminal?

**Solución:**

```bash
nemoclaw launch <sandbox>                      # verifica y abre la TUI
# o bien
nemoclaw <sandbox> connect                     # shell dentro del sandbox
openclaw tui
# un solo turno, sin interfaz:
nemoclaw <sandbox> agent -m "Hola, ¿qué skills tienes?"
```

**Fuente:** [quickstart de NemoClaw](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/get-started/quickstart).

### ¿Cómo instalo una skill y por qué el agente no la usa?

**Causa:** una skill es una carpeta con un `SKILL.md` (con *frontmatter* YAML y un campo `name`). Que esté instalada no garantiza que el agente la elija solo.

**Solución:**

```bash
nemoclaw <sandbox> skill install ./mi-skill/
nemoclaw <sandbox> skill list
```

Para probarla, abre una sesión nueva y menciónala o da la ruta de su `SKILL.md`. La selección automática es otra prueba aparte. El nombre solo admite letras, números, puntos, guiones y guiones bajos.

**Fuente:** [commands](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands) (`skill install`); lección 03c del curso de NVIDIA.

---

<a id="openshell"></a>
## 7. OpenShell y políticas

<a id="e403tunnel"></a>
### `curl: (56) CONNECT tunnel failed, response 403`

**Causa:** **no** es un problema de certificados ni de la herramienta. La red de salida del sandbox está bloqueada por defecto y el proxy de OpenShell rechazó la conexión. Para que pase, deben coincidir **el host y el binario** que hace la llamada.

**Solución:**

```bash
nemoclaw <sandbox> logs --tail 50     # muestra la línea DENIED (host y binario)
nemoclaw <sandbox> policy list        # presets aplicados
nemoclaw <sandbox> policy add <preset>
```

Para una prueba puntual, apruébalo en vivo con `openshell term`. Si usas `nemoclaw <sandbox> exec -- <comando>`, NemoClaw te imprime una pista con el host bloqueado; para silenciarla: `export NEMOCLAW_NO_POLICY_HINT=1`. Un error HTTP puede venir del proxy o de la aplicación destino: identifica la fuente antes de culpar a la política.

**Fuente:** troubleshooting "A request inside the sandbox fails with `CONNECT tunnel failed, response 403`"; lección 04a del curso de NVIDIA.

### ¿Cómo apruebo en vivo un acceso de red bloqueado con `openshell term`?

**Solución:** usa la TUI de OpenShell en el host (en Brev, dentro de `brev shell <instancia>`):

```bash
openshell term
```

1. Elige el sandbox con `j`/`k` y `Enter`.
2. Pulsa `r` para ir a **Network Rules**.
3. Elige la solicitud pendiente (`Enter` muestra detalles, incluida la ruta del binario).
4. `a` aprueba, `x` rechaza, `A` aprueba todas (confirma con `y`).

Ojo: estas aprobaciones duran solo mientras exista esa instancia del sandbox. Al recrearlo se pierden y no se escriben en la política base; si lo necesitas siempre, usa un preset (`nemoclaw <sandbox> policy add`).

En la TUI, `policy_denied` significa que ninguna regla coincidió, y `upstream_unreachable` que la política lo permitió pero el host no respondió (DNS, red o servicio caído). Las teclas vienen de la documentación de NemoClaw; confírmalas con OpenShell 0.0.116. `[VERIFICAR EN LAB]`

**Fuente:** [Approve network requests](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/network-policy/approve-network-requests); [network policies](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/network-policies).

### ¿Cómo veo la política activa y cómo agrego o quito un preset (`pypi`, `github`…)?

**Solución:**

```bash
nemoclaw <sandbox> policy list               # presets aplicados y de dónde vienen
nemoclaw <sandbox> policy get                # política base
openshell policy get --full <sandbox>        # política efectiva completa

nemoclaw <sandbox> policy add pypi --dry-run # prueba sin aplicar
nemoclaw <sandbox> policy add pypi --yes
nemoclaw <sandbox> policy remove pypi --yes
nemoclaw <sandbox> policy add                # selector interactivo
```

La política activa vive en OpenShell; NemoClaw no guarda otra copia aparte. GitHub y las plataformas de mensajería **no** están en la política base: hay que agregarlas a propósito. Los cambios de red se aplican en caliente, sin reiniciar.

**Fuente:** [network policies](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/network-policies); [CLI selection guide](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/cli-selection-guide).

### Permití el host y sigue saliendo 403 (`binary '...' not allowed in policy`)

**Causa:** OpenShell exige **dos** coincidencias: el host y el programa que hace la llamada. Por ejemplo, `npm` corre como `/usr/local/bin/node`; si el preset no lista ese binario, la llamada se rechaza. El log lo muestra así: `DENIED /usr/local/bin/node -> registry.npmjs.org:443 reason: binary '/usr/local/bin/node' not allowed in policy 'npm_registry'`.

**Solución:** lee la línea `DENIED` en `nemoclaw <sandbox> logs --tail 50` (o el detalle en `openshell term`), copia la ruta exacta del binario y agrégala a la sección `binaries:` de tu preset propio.

**Fuente:** [NemoClaw#481](https://github.com/NVIDIA/NemoClaw/issues/481), [#993](https://github.com/NVIDIA/NemoClaw/issues/993); [create custom policy presets](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/network-policy/create-custom-policy-presets).

### `pip install` sigue fallando aunque permití PyPI

**Causa:** algunas instalaciones necesitan llegar a IPs privadas o a varios hosts, y el sandbox lo impide (protección SSRF).

**Solución:** instala las dependencias al **construir** la imagen, no en tiempo de ejecución: `nemoclaw onboard --from <Dockerfile>`. El Dockerfile debe partir de la imagen administrada completa, no de `sandbox-base`.

**Fuente:** `docs/network-policy/customize-network-policy.mdx`; [Discussion #6108](https://github.com/NVIDIA/NemoClaw/discussions/6108).

### Cambié la política de archivos y no tuvo efecto

**Causa:** solo la política de **red** y de **inferencia** se recargan en caliente. La política de sistema de archivos (Landlock) y la de procesos quedan fijas al crear el sandbox.

**Solución:** edita la política base y vuelve a crear el sandbox con `nemoclaw onboard` (o `nemoclaw <sandbox> rebuild`).

**Fuente:** `docs/about/how-it-works.mdx` en NVIDIA/NemoClaw; [network policies](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/network-policies) ("Static Changes").

### `⚠ Landlock: Docker VM kernel <v> does not support Landlock (requires ≥5.13).`

**Causa:** el kernel (o la VM de Docker en macOS) no soporta Landlock, la capa del kernel que limita qué archivos puede tocar el sandbox.

**Solución:** es un aviso, no bloquea. El sandbox funciona en modo `best_effort`, sin restricciones de archivos a nivel kernel. Para la protección completa, usa Linux con kernel 5.13 o mayor (Ubuntu 22.04 en adelante).

**Fuente:** troubleshooting "Landlock filesystem restrictions silently degraded".

### ¿Qué nivel de política elijo: Restricted, Balanced, Open o Personal?

**Solución:**

| Nivel | Qué permite |
|---|---|
| Restricted | Solo la política base |
| **Balanced** (por defecto) | Base + `npm`, `pypi`, `huggingface`, `brew-balanced`, `brave` |
| Open | Agrega mensajería, `jira`, `outlook`, `weather` y más |
| Personal | Cualquier host en 80/443, **sin pedir aprobación** |

Para el curso usa **Balanced**. Usa Personal solo con cargas de trabajo en las que confías por completo.

**Fuente:** `nemoclaw-blueprint/policies/tiers.yaml`; [network policies](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/network-policies) ("Policy Tiers").

---

<a id="instalacion-local"></a>
## 8. NemoClaw instalado en tu máquina

Esto aplica a la clase 6.3 o si quieres seguir después del curso fuera de Brev.

### ¿Qué necesito para instalar NemoClaw?

**Solución:**

| Recurso | Mínimo | Recomendado |
|---|---|---|
| CPU | 4 vCPU | 4+ vCPU |
| RAM | 8 GB | 16 GB |
| Disco libre | 20 GB | 40 GB |

- Node.js **22.19 o mayor** y npm 10 o mayor.
- Docker (Docker Engine, Docker Desktop o Colima) funcionando **antes** de instalar.
- Plataformas: Ubuntu 24.04 (la principal), macOS con Apple Silicon y Windows con WSL2. **Mac con Intel no está soportado.** Distribuciones sin `apt-get` tampoco.
- Revisa tu máquina antes de instalar: `nemoclaw host probe`.

Instalación: `curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash`.

**Fuente:** [prerequisites](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/get-started/prerequisites); [platform support](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/platform-support).

### `nemoclaw: command not found` o Node.js "muy viejo" después de instalar

**Causa:** la terminal actual no tiene el `PATH` actualizado, o sigue usando el Node anterior. NemoClaw pide Node **22.19 o mayor**; el instalador puede instalarlo con nvm, pero tu shell abierta no se entera.

**Solución:**

```bash
source ~/.bashrc                   # o ~/.zshrc, o abre una terminal nueva
nvm install 22 && nvm use 22       # si node --version sigue en v20
node --version
nemoclaw --version
```

Si instalaste desde el código fuente, agrega `~/.local/bin` a tu `PATH`. Luego vuelve a ejecutar el instalador si se quedó a medias.

**Fuente:** troubleshooting "`nemoclaw` not found after install" y "Node.js version is too old"; [NemoClaw#2178](https://github.com/NVIDIA/NemoClaw/issues/2178).

### `Docker is not running` (aunque Docker sí está corriendo) o `permission denied` en el socket

**Causa:** tu usuario no está en el grupo `docker`, así que no puede hablar con el daemon.

**Solución:**

```bash
sudo systemctl start docker                       # si de verdad está apagado
sudo usermod -aG docker $USER && newgrp docker
docker ps                                         # debe funcionar sin sudo
```

Si el gateway corre como servicio de usuario, cierra sesión por completo (o reinicia) para que tome el grupo nuevo. Ojo: estar en el grupo `docker` equivale casi a ser root; hazlo solo en tu máquina.

**Fuente:** troubleshooting "Docker permission denied on Linux"; [NemoClaw#50](https://github.com/NVIDIA/NemoClaw/issues/50); [OpenShell#1377](https://github.com/NVIDIA/OpenShell/issues/1377).

### macOS: falla la primera instalación o no encuentra Docker con Colima

**Causa:** faltan las Command Line Tools de Xcode, el runtime de contenedores no arrancó o Colima tiene muy pocos recursos.

**Solución:**

```bash
xcode-select --install
brew install colima docker
colima start --cpu 4 --memory 8
docker info
```

Si la construcción se queda lenta: `colima stop; colima start --cpu 6 --memory 12 --disk 100`. Si aparece `Socket not found: /var/run/docker.sock` con Colima (problema abierto), exporta `export DOCKER_HOST=unix://$HOME/.colima/default/docker.sock` y reintenta.

**Fuente:** troubleshooting "macOS first-run failures" y "Colima socket not detected"; [NemoClaw#12367](https://github.com/NVIDIA/NemoClaw/issues/12367).

### WSL2: `docker info` falla dentro de WSL (`Cannot connect to the Docker daemon`)

**Causa:** Docker Desktop no está abierto o no tiene activada la integración con tu distribución de WSL.

**Solución:** abre Docker Desktop → **Settings → Resources → WSL integration** → activa Ubuntu. Luego, en PowerShell, `wsl --shutdown`, abre Ubuntu de nuevo y prueba `docker info`. Ejecuta NemoClaw **dentro** de Ubuntu, no en PowerShell.

**Fuente:** troubleshooting "`docker info` fails inside WSL"; [windows preparation](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/get-started/windows-preparation).

### La creación del sandbox muere por memoria (exit 137, OOM)

**Causa:** la imagen del sandbox pesa unos 2.4 GB comprimida. Con 8 GB de RAM o menos, el *OOM killer* puede matar la subida.

**Solución:** agrega swap (o usa una máquina de 16 GB):

```bash
sudo dd if=/dev/zero of=/swapfile bs=1M count=4096
sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile
```

El onboarding también ofrece crear 4 GB de swap automáticamente.

**Fuente:** troubleshooting "Sandbox creation killed by OOM (exit 137)"; [NemoClaw#444](https://github.com/NVIDIA/NemoClaw/issues/444).

### El puerto 18789 o el 8080 ya está en uso (o `Port 18789 is not available. Blocked by: ssh`)

**Causa:** otro programa, un onboarding anterior o un túnel SSH viejo ocupa el puerto del dashboard (18789) o del gateway (8080).

**Solución:**

```bash
sudo lsof -i :18789 -sTCP:LISTEN -P -n            # ¿quién lo ocupa?
nemoclaw onboard --control-ui-port 19000          # dashboard en otro puerto
NEMOCLAW_GATEWAY_PORT=8990 nemoclaw onboard       # gateway en otro puerto
```

Si es tu propio `ssh` viejo, termina ese PID (las versiones recientes lo cierran solas). Si usas un puerto de gateway distinto, mantén la misma variable en los comandos siguientes. Solo detén un proceso si sabes que es tuyo.

**Fuente:** troubleshooting "Port already in use" y "Re-onboard fails because port 18789 is held by SSH"; [NemoClaw#684](https://github.com/NVIDIA/NemoClaw/issues/684).

### `Cannot allocate dashboard port: The OpenShell forward operation timed out.`

**Causa:** una regresión de las versiones v0.0.126 a v0.0.129 (macOS, WSL2 y Brev x86). Hay una variante con `could not prove OpenShell forward ownership` todavía abierta en algunos equipos.

**Solución:** actualiza con `nemoclaw update`. Mientras tanto, el arreglo temporal de la comunidad es usar otro puerto de gateway: `NEMOCLAW_GATEWAY_PORT=8990 nemoclaw onboard --fresh` (y deja esa variable puesta para los demás comandos).

**Fuente:** [NemoClaw#11963](https://github.com/NVIDIA/NemoClaw/issues/11963), [#11979](https://github.com/NVIDIA/NemoClaw/issues/11979).

### `Sandbox '<sandbox>' was created but did not become ready within 180s.`

**Causa:** la máquina tardó más de lo esperado (por ejemplo, una VM en la nube recién encendida).

**Solución:**

```bash
nemoclaw <sandbox> destroy            # limpia el sandbox que quedó a medias
export NEMOCLAW_SANDBOX_READY_TIMEOUT=600
nemoclaw onboard
```

No reintentes con el mismo nombre sin destruir antes.

**Fuente:** troubleshooting "Sandbox onboard times out with 'did not become ready within Ns'".

### El onboarding se interrumpió a la mitad

**Causa:** cerraste la terminal, se cortó SSH o algún paso falló. NemoClaw guarda el avance en `~/.nemoclaw/onboard-session.json`.

**Solución:**

```bash
nemoclaw onboard --resume      # continúa donde se quedó
nemoclaw onboard --fresh       # descarta la sesión y empieza de cero
```

En servidores remotos, corre el onboarding dentro de `tmux new-session -s nemoclaw-onboard` para que sobreviva a una desconexión.

**Fuente:** troubleshooting "Previous onboarding session failed"; [headless guide](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/deployment/deploy-to-headless-server).

### Puse las variables antes de `curl` y el instalador las ignoró

**Causa:** en `curl ... | bash`, las variables deben ir del lado de `bash`, no del lado de `curl`.

**Solución:**

```bash
# Mal:  NEMOCLAW_ACCEPT_THIRD_PARTY_SOFTWARE=1 curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash
# Bien:
curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_ACCEPT_THIRD_PARTY_SOFTWARE=1 bash
```

**Fuente:** [quickstart](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/get-started/quickstart) ("Automate an installation").

### ¿Cómo actualizo NemoClaw (y OpenClaw) sin romper mis sandboxes?

**Causa:** NemoClaw fija una versión exacta de OpenShell y empaqueta su propia versión de OpenClaw. Actualizar piezas por separado deja los sandboxes en un estado inconsistente: por ejemplo, `openclaw update` dentro del sandbox se cuelga.

**Solución:**

```bash
nemoclaw backup-all                        # respaldo de todos los sandboxes
nemoclaw update --check
nemoclaw update
nemoclaw upgrade-sandboxes --check
nemoclaw upgrade-sandboxes --auto          # o: nemoclaw <sandbox> rebuild
```

Si `nemoclaw <sandbox> status` dice que el agente está desactualizado, ejecuta `nemoclaw <sandbox> rebuild`. Hay reportes abiertos de políticas personalizadas perdidas tras actualizar: anota tus presets (`policy list`) antes.

**Fuente:** [commands](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands) (`update`, `upgrade-sandboxes`, `backup-all`); troubleshooting "`openclaw update` hangs or times out inside the sandbox"; [NemoClaw#7420](https://github.com/NVIDIA/NemoClaw/issues/7420).

### ¿Cómo cambio el modelo o roto mi API key en NemoClaw?

**Solución:**
- **Ver el modelo actual:** `nemoclaw inference get`.
- **Cambiar de modelo:** `nemoclaw inference set --provider nvidia-prod --model <modelo> --sandbox <sandbox>`.
- **Rotar la key** (lee la key sin que quede en el historial):

```bash
printf 'Nueva NVIDIA API key: ' >&2
IFS= read -r -s NVIDIA_INFERENCE_API_KEY; printf '\n' >&2
export NVIDIA_INFERENCE_API_KEY
nemoclaw onboard --name <sandbox> --non-interactive --yes --yes-i-accept-third-party-software
unset NVIDIA_INFERENCE_API_KEY
```

Si `nemoclaw <sandbox> status` muestra `unauthorized` en la fila de inferencia, el problema es la key, no la ruta. El nombre del proveedor puede variar: confírmalo con `nemoclaw credentials list`.

**Fuente:** [credential rotation](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/security/credential-rotation); [CLI selection guide](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/cli-selection-guide).

### ¿Puedo actualizar OpenShell por mi cuenta con `openshell self-update`?

**Causa:** cada versión de NemoClaw fija una versión exacta de OpenShell (la v0.0.134 fija la **0.0.116**, mínima y máxima). OpenShell ya va en la 0.1.x, que cambió el formato de configuración del gateway y es incompatible.

**Solución:** **no.** Nunca ejecutes `openshell self-update`, `npm update -g openshell` ni el `install.sh` de OpenShell por separado. Deja que el instalador de NemoClaw lo maneje: `nemoclaw update`. Si ya lo hiciste y ves `✗ openshell <version> is above the maximum supported by this NemoClaw release.`, vuelve a ejecutar el instalador oficial de NemoClaw.

**Fuente:** [prerequisites](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/get-started/prerequisites); troubleshooting "OpenShell version above maximum"; [NemoClaw#1261](https://github.com/NVIDIA/NemoClaw/issues/1261), [#12456](https://github.com/NVIDIA/NemoClaw/issues/12456).

### Después de reiniciar la máquina: `handshake verification failed`, `sandbox not found` o el dashboard no abre

**Causa:** tras reiniciar el host, Docker, el gateway de OpenShell y el sandbox pueden no arrancar solos. En versiones viejas (OpenShell anterior a 0.0.24) el sandbox además se perdía porque el gateway regeneraba sus secretos.

**Solución:**

```bash
sudo systemctl start docker                  # macOS: abre Docker Desktop o `colima start`
systemctl --user status openshell-gateway    # Linux (paquete); si está caído:
systemctl --user restart openshell-gateway
nemoclaw <sandbox> status
nemoclaw <sandbox> start                     # si quedó detenido
nemoclaw <sandbox> recover                   # si el gateway o los forwards no responden
nemoclaw <sandbox> connect
```

Logs del gateway en Linux: `journalctl --user --unit openshell-gateway --no-pager --lines=200`. Si el sandbox se creó con OpenShell anterior a 0.0.24, recréalo con `nemoclaw onboard`. Antes de reiniciar algo importante, respalda con `nemoclaw backup-all`.

Si encuentras guías que usan `docker exec openshell-cluster-nemoclaw kubectl ...`, ignóralas: son de la arquitectura vieja con k3s, que ya no existe.

**Fuente:** troubleshooting "Reconnect after a host reboot" y "Sandbox lost after gateway restart"; [NemoClaw#768](https://github.com/NVIDIA/NemoClaw/issues/768), [#7404](https://github.com/NVIDIA/NemoClaw/issues/7404), [#2481](https://github.com/NVIDIA/NemoClaw/issues/2481).

### Ollama local: `Sandbox containers cannot reach the Ollama auth proxy at host.openshell.internal:11435`

**Causa:** NemoClaw deja Ollama en `127.0.0.1:11434` y abre un **proxy con token en el puerto 11435** para que el sandbox llegue a él sin exponer Ollama a tu red. Un firewall del host (por ejemplo `ufw`) puede bloquear ese tráfico.

**Solución:**

```bash
SUBNET=$(docker network inspect openshell-docker --format '{{(index .IPAM.Config 0).Subnet}}')
sudo ufw allow from "$SUBNET" to any port 11435 proto tcp
nemoclaw onboard
```

No pongas `OLLAMA_HOST=0.0.0.0` (era el arreglo viejo y en WSL2 causa timeouts): deja Ollama en `127.0.0.1:11434`. Si el proxy no arranca, revisa quién ocupa el puerto con `sudo lsof -i :11435`.

**Fuente:** troubleshooting "Ollama auth proxy is unreachable from the sandbox" y "Ollama auth proxy did not start"; [NemoClaw#709](https://github.com/NVIDIA/NemoClaw/issues/709), [#1472](https://github.com/NVIDIA/NemoClaw/issues/1472).

### `openshell: command not found` (exit 127)

**Causa:** instalaste NemoClaw por npm o desde el código sin la CLI de OpenShell. NemoClaw **no** se publica en npm.

**Solución:** usa el instalador oficial, que instala OpenShell si falta: `curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash`.

**Fuente:** [NemoClaw#410](https://github.com/NVIDIA/NemoClaw/issues/410), [#2481](https://github.com/NVIDIA/NemoClaw/issues/2481).

---

<a id="seguridad"></a>
## 9. Seguridad

### ¿Qué datos nunca debo compartir?

**Solución:** trata todo esto como una contraseña. No lo pegues en foros, issues, capturas de pantalla, notebooks compartidos ni commits:
- Tu API key `nvapi-…` (y cualquier key de otro proveedor).
- Las cookies del laboratorio: `CF_Authorization`, `_pomerium`, `__Host-skybridge-brev-prd`.
- La URL del dashboard con `#token=` y la salida de `nemoclaw <sandbox> gateway-token`.
- Tus archivos `.env`, `~/.brev/credentials.json`, `~/.brev/brev.pem` y `~/.nemoclaw/credentials.json`.
- Exportaciones de sesiones (`sessions export`): pueden contener secretos que pegaste en el chat.

**Fuente:** [headless guide](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/deployment/deploy-to-headless-server); [commands](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands) (`sessions export`); lección 03a del curso de NVIDIA.

<a id="efiltrada"></a>
### Filtré mi API key (la subí a GitHub, salió en un video o en una captura)

**Causa:** cualquiera que la vea puede gastar tus créditos. Borrar el archivo o hacer otro commit **no** basta: la key sigue en el historial de git y en las copias que alguien haya hecho.

**Solución:**
1. **Revócala ya** en build.nvidia.com → **API Keys** (bórrala o desactívala). `[VERIFICAR EN LAB]`
2. Genera una key nueva.
3. Actualízala donde la uses: secreto de Colab, `.env`, y NemoClaw (ver [rotar la key](#instalacion-local)).
4. Revisa tu uso en build.nvidia.com por si hubo consumo extraño.
5. Quita la key del repo y agrega `.env` a `.gitignore`. Asume que la key vieja ya es pública aunque limpies el historial.

**Fuente:** [credential rotation](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/security/credential-rotation); notas de producción de la clase 1.2.

### Compartí sin querer una cookie del laboratorio o la URL del dashboard

**Causa:** con esa cookie o ese token, otra persona podría entrar a tu launchable o a tu gateway mientras la sesión siga activa.

**Solución:**
1. Detén la instancia en Brev (consola → **GPUs** → **Stop**) o bórrala si no tiene nada que conservar.
2. Cierra sesión en el launchable y vuelve a entrar para obtener una cookie nueva.
3. No sabemos si cerrar sesión invalida la cookie anterior al instante; por eso detener la instancia es lo más seguro. `[VERIFICAR EN LAB]`

**Fuente:** lección 03a del curso de NVIDIA (las credenciales de acceso viven solo en la pestaña); [Brev: Console Reference](https://docs.nvidia.com/brev/latest/guides/console-reference).

### ¿Es seguro abrir el dashboard o el gateway a internet?

**Causa:** el gateway (8080) controla el agente y el dashboard (18789) da acceso a él.

**Solución:** no. Usa un túnel (`brev port-forward <instancia> -p 18789:18789` o `ssh -L`), que mantiene el origen en `127.0.0.1`. Nunca abras el 8080 y no uses `--public` en `brev ports open` para el dashboard. Si necesitas exponerlo, hazlo detrás de HTTPS y con el pairing activo.

**Fuente:** [gateway authentication controls](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/security/gateway-authentication-controls); [headless guide](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/deployment/deploy-to-headless-server).

### ¿Dónde guarda NemoClaw mis keys? ¿Las ve el agente?

**Solución:** NemoClaw registra las keys de proveedores en el gateway de OpenShell, del lado del host. Desde la v0.0.132–0.0.133, los sandboxes nuevos usan proveedores adjuntos al sandbox y las credenciales se quedan en el host. Por eso **no** debes poner keys dentro de `openclaw.json` ni en archivos del workspace: lo que está dentro del sandbox, el agente lo puede leer.

**Fuente:** [credential storage](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/security/credential-storage); troubleshooting "Change OpenClaw Configuration Inside the Sandbox"; changelog v0.0.132 y v0.0.133.

---

<a id="trazas"></a>
## 10. Observabilidad y trazas

### ¿Qué herramienta de observabilidad uso? ¿NVIDIA tiene una propia?

**Respuesta:** en el curso usamos **OpenTelemetry** (el estándar abierto) con convenciones **OpenInference** y **Arize Phoenix** (código abierto) como interfaz. NVIDIA tiene dos piezas: el **NeMo Agent Toolkit** (`nvidia-nat`), que instrumenta flujos de agentes y exporta a Phoenix, Langfuse, LangSmith, Weave u OTel con YAML; y en **NemoClaw**, `logs`, `sessions export` y `openshell term` para el sandbox, más exportación OTLP para Deep Agents (`--observability`). Todo habla OTel, así que puedes mezclarlas.

**Fuente:** clase 3.4; [NeMo Agent Toolkit · Observar flujos](https://docs.nvidia.com/nemo/agent-toolkit/latest/run-workflows/observe/observe.html).

### El notebook dice `Phoenix: no detectado` aunque lo tengo corriendo

**Causa:** ejecutaste la celda del tracer antes de levantar Phoenix, o Phoenix escucha en otro host o puerto.

**Solución:** con `phoenix serve` corriendo (o `docker run -p 6006:6006 arizephoenix/phoenix:latest`), vuelve a ejecutar la celda del tracer. Si usas otro puerto o un Phoenix remoto: `export PHOENIX_COLLECTOR_ENDPOINT=http://<host>:<puerto>` antes de abrir el notebook. En Colab no hace falta Phoenix: `ver_traza` dibuja la traza en texto.

**Fuente:** clase 3.4.

### `pip install arize-phoenix` falla con un error de versión de Python

**Causa:** Phoenix requiere Python 3.11 o mayor.

**Solución:** usa Docker (`arizephoenix/phoenix`) o un entorno con Python 3.11+. El notebook de la 3.4 funciona igual sin Phoenix: solo usa OpenTelemetry, que corre en 3.10.

**Fuente:** [arize-phoenix en PyPI](https://pypi.org/project/arize-phoenix/).

### Mi key (o mi cookie) apareció en una traza

**Causa:** las trazas guardan prompts completos y salidas de herramientas. Si alguien pegó una key en el chat, la traza la guardó.

**Solución:** revoca la key en build.nvidia.com y genera otra. Borra la traza (en Phoenix, el proyecto o las trazas afectadas). En tu código, pasa **todo** atributo por una función de redacción, como `poner()`/`redactar()` de la clase 3.4, y no publiques un Phoenix sin autenticación.

**Fuente:** clases 1.2 y 3.4.

### ¿Puedo ver en Phoenix lo que hace el agente dentro del sandbox?

**Respuesta:** no directamente. Desde el host trazas las **llamadas** al agente (por ejemplo, la API de Hermes con `hermes_trazado.py`), pero no las herramientas que el agente ejecuta dentro del sandbox. Esas están en el historial de sesiones: `nemoclaw <sandbox> sessions export` (OpenClaw) o `nemohermes <sandbox> sessions export` (Hermes). NemoClaw solo exporta trazas OTLP desde dentro del sandbox para Deep Agents, con el preset de red `observability-otlp-local`.

**Fuente:** clase 4.4; [NemoClaw · Exportar trazas de Deep Agents](https://docs.nvidia.com/nemoclaw/latest/user-guide/deepagents/monitoring/set-up-deepagents-trace-export).

---

<a id="hermes"></a>
## 11. Hermes en NemoClaw

### ¿Hermes reemplaza a NemoClaw?

**Respuesta:** no. NemoClaw es el sandbox de OpenShell, las políticas, la inferencia administrada y el ciclo de vida. Hermes (de Nous Research) es **un agente** que vive dentro, como OpenClaw o LangChain Deep Agents. Cambias el agente con `nemohermes onboard` (o `NEMOCLAW_AGENT=hermes`) y la seguridad se queda igual.

**Fuente:** clase 4.4; [NemoClaw · Ecosistema](https://docs.nvidia.com/nemoclaw/latest/user-guide/hermes/about/ecosystem).

### `nemohermes: command not found`

**Causa:** tu versión del CLI de NemoClaw es anterior a los alias por agente, o el `PATH` no incluye el CLI.

**Solución:** `NEMOCLAW_AGENT=hermes nemoclaw onboard` hace lo mismo. Para actualizar: `nemoclaw update`. Revisa tu versión con `nemoclaw --version`. `[VERIFICAR EN LAB]`

**Fuente:** [NemoClaw · Comandos de nemohermes](https://docs.nvidia.com/nemoclaw/latest/user-guide/hermes/reference/commands).

### ¿Dónde están SOUL.md, la memoria y las skills de Hermes?

**Respuesta:** la personalidad en `/sandbox/SOUL.md`. Todo lo demás en `/sandbox/.hermes/`: `config.yaml` (lo genera NemoClaw; no lo edites a mano porque `rebuild` lo regenera), `memories/MEMORY.md` y `USER.md`, `skills/`, `state.db` (sesiones en SQLite) y `logs/`. `destroy` borra todo; `rebuild` y las actualizaciones lo conservan.

**Fuente:** [NemoClaw · Estado del sandbox de Hermes](https://docs.nvidia.com/nemoclaw/latest/user-guide/hermes/manage-sandboxes/state-and-backups/understand-sandbox-state).

### `curl: (7) Failed to connect to 127.0.0.1 port 8642` o `401` en la API de Hermes

**Causa:** la API tomó otro puerto (8642 a 8652 si hay otro sandbox), el forward se cayó tras un reinicio, o el token es incorrecto.

**Solución:** `openshell forward list` para ver el puerto real; si no aparece, `nemohermes <sandbox> recover`. Para el token: `TOKEN="$(nemohermes <sandbox> gateway-token --quiet)"` y envíalo como `Authorization: Bearer $TOKEN`. El token cambia si reconstruyes el sandbox.

**Fuente:** [NemoClaw · Quickstart con Hermes](https://docs.nvidia.com/nemoclaw/latest/user-guide/hermes/get-started/quickstart).

### Instalé una skill en Hermes y no la usa

**Causa:** Hermes carga las skills al iniciar la sesión, o la `description` del `SKILL.md` no coincide con cómo pregunta el estudiante.

**Solución:** confirma con `nemohermes <sandbox> skill list`, sal con `/exit` y abre una sesión nueva. Prueba la skill como comando (`/soporte-nemoclaw ...`). Si quieres reemplazarla, primero `skill remove`: sin comando nativo de Hermes, `skill install` no sobrescribe una carpeta con el mismo nombre.

**Fuente:** clase 4.4.

### Hermes guardó algo en su memoria que yo no quería

**Causa:** Hermes escribe en su memoria y crea skills por su cuenta. Sin aprobación, una instrucción (tuya o de un texto malicioso) queda guardada para sesiones futuras.

**Solución:** dentro de Hermes, `/memory approval on` y `/skills approval on`; revisa con `/memory pending` y rechaza con `/memory reject <id>`. Lee `/sandbox/.hermes/memories/MEMORY.md` como operador y limpia lo que no reconozcas. `[VERIFICAR EN LAB]` los comandos en la versión fijada.

**Fuente:** [Hermes Agent · Memoria](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory); clase 4.4 y Módulo 5.

---

<a id="pedir-ayuda"></a>
## 12. Cómo pedir ayuda bien

Una buena pregunta se responde en minutos; una vaga, en días. Antes de preguntar, busca tu mensaje de error exacto en esta página (Ctrl+F / Cmd+F).

### Qué incluir

1. **Qué intentabas hacer:** clase (por ejemplo, 4.2), paso y comando exacto que ejecutaste.
2. **Qué esperabas y qué pasó:** el mensaje de error **completo y literal** (copiado como texto, no como foto).
3. **Dónde:** notebook en Colab, notebook local, curso web de NVIDIA, launchable de Brev o NemoClaw en tu máquina. Sistema operativo.
4. **Versiones y estado** (si usas NemoClaw):

```bash
nemoclaw --version
openshell --version
nemoclaw status
nemoclaw <sandbox> status
nemoclaw <sandbox> logs --tail 50
```

5. **Diagnóstico para un bug** (solo si te lo piden o vas a abrir un issue):

```bash
nemoclaw debug --quick
nemoclaw debug --sandbox <sandbox> --output /tmp/nemoclaw-debug.tar.gz
```

Revisa el contenido antes de compartirlo.

6. **Qué ya probaste** de esta FAQ.

### Qué NO pegar nunca

- Tu API key (`nvapi-…`) ni ninguna otra key o token.
- Cookies del laboratorio (`CF_Authorization`, `_pomerium`, `__Host-skybridge-brev-prd`).
- La URL del dashboard con `#token=` ni la salida de `gateway-token`.
- Tu `.env`, `credentials.json` o archivos `.pem`.

Si un log o una captura incluye alguno de estos valores, reemplázalo por `nvapi-xxxxxxxx` o `<REDACTADO>`. Si ya lo pegaste, sigue los pasos de [key filtrada](#efiltrada).

### Dónde preguntar

| Tipo de problema | Dónde |
|---|---|
| Dudas del curso, notebooks, ejercicios | Comunidad de Platzi, en la sección de comentarios de la clase |
| Cuenta de NVIDIA Build, verificación de teléfono | `help@build.nvidia.com` o `https://developer.nvidia.com/support` |
| Brev: facturación, instancias trabadas, límites de la organización | `brev-support@nvidia.com` |
| Curso web de NVIDIA (páginas, conexión con el launchable) | Issues de [NVDLI/NemoClawDLI](https://github.com/NVDLI/NemoClawDLI/issues) |
| Bugs de NemoClaw | Issues de [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw/issues) (busca primero si ya existe) |
| Preguntas generales sobre NemoClaw | [Discussions de NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw/discussions) |
| Bugs de OpenShell | Issues de [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell/issues) |

---

*Basada en la documentación pública de NVIDIA NemoClaw (Apache-2.0), en el curso de NVIDIA DLI "Securing Agents with OpenShell and NemoClaw" ([NVDLI/NemoClawDLI](https://github.com/NVDLI/NemoClawDLI), Apache-2.0), en la documentación de NVIDIA Brev y en issues públicos de GitHub revisados el 14 de octubre de 2026. Versión de referencia: NemoClaw v0.0.134, OpenShell 0.0.116.*
