# Preguntas frecuentes y solución de problemas

Curso **Seguridad de agentes con OpenShell y NemoClaw** (Platzi × NVIDIA DLI).

Esta página reúne los problemas reales que vas a encontrar en el curso: la API key, los errores del modelo, los notebooks, Brev, la conexión con el laboratorio, OpenClaw, OpenShell y la instalación local de NemoClaw. Cada entrada tiene la **causa**, la **solución** con comandos exactos y, cuando existe, la **fuente** oficial.

> **Antes de seguir:** NemoClaw está en *alpha* y publica versiones cada 1 a 3 días. Si un comando no coincide con lo que ves, revisa tu versión con `nemoclaw --version` y la documentación oficial. Las entradas del laboratorio se probaron con NemoClaw v0.0.135 y OpenShell 0.0.116.

En los comandos, `<sandbox>` es el nombre de tu sandbox (en el laboratorio es `my-assistant`; confírmalo con `nemoclaw list`). En el laboratorio, los comandos `nemoclaw` y `openshell` se pegan en la **terminal de operador**: el botón **VM TERMINAL** de tu tablero (ver [LABORATORIO.md](LABORATORIO.md)).

## Índice

1. [Cuenta y API key de NVIDIA Build](#api-key)
2. [Errores de la API (401, 403, 404, 410, 422, 429, 5xx, timeouts, `finish_reason`)](#errores-api)
3. [Notebooks, Colab y Python](#notebooks)
4. [Brev y el launchable](#brev)
5. [Conexión con tu laboratorio (tablero, chat y terminal)](#conexion-laboratorio)
6. [OpenClaw: gateway, dashboard, pairing, workspace y sesiones](#openclaw)
7. [OpenShell y políticas](#openshell)
8. [NemoClaw instalado en tu máquina](#instalacion-local)
9. [Seguridad](#seguridad)
10. [Hermes en NemoClaw](#hermes)
11. [Cómo pedir ayuda bien](#pedir-ayuda)

### Los 10 problemas que más vas a ver

| Síntoma | Ir a |
|---|---|
| `401 Unauthorized` al llamar al modelo | [401](#e401) |
| Respuesta vacía con `finish_reason: "length"` | [finish_reason](#elength) |
| `429 Too Many Requests` | [429](#e429) |
| El notebook dice `Modo: MOCK` aunque pusiste tu key | [MOCK](#emock) |
| No sabes si tu instancia de Brev te sigue cobrando | [Costos](#ecostos) |
| Escribes en la terminal del laboratorio y no pasa nada | [Terminal sin foco](#eterminal) |
| El agente dice que abrió una página, pero el log dice `DENIED` | [Respuesta sin acceso](#edenied) |
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

La interfaz de build.nvidia.com cambia seguido; si no ves el menú **API Keys**, busca el botón **Get API Key** en la página de cualquier modelo.

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

**Solución:** vuelve a copiar la key completa desde build.nvidia.com, sin espacios ni comillas. En los notebooks del curso verás el aviso `⚠  Tu key no empieza con 'nvapi-'`. Si la perdiste, genera una nueva: NVIDIA no te la vuelve a mostrar.

**Fuente:** `web/nemoclaw/scripts/_keypanel.js` de [NVDLI/NemoClawDLI](https://github.com/NVDLI/NemoClawDLI); `tools/notebooks/comun.py` de este repo.

### ¿Dónde guardo mi API key? ¿Sirve la misma en todo el curso?

**Causa:** la key es un secreto y cada entorno la lee de un lugar distinto. Es la **misma** key `nvapi-` en todos lados; cambia solo el nombre de la variable.

**Solución:**
- **Google Colab:** icono de llave 🔑 (*Secrets*) → nuevo secreto `NVIDIA_API_KEY` → activa el acceso del notebook.
- **Tu máquina:** copia `.env.example` como `.env` en la raíz del repo y pon tu key en `NVIDIA_API_KEY`. `.env` ya está en `.gitignore`.
- **Terminal:** `export NVIDIA_API_KEY=nvapi-xxxxxxxx` (solo dura esa sesión).
- **Curso web de NVIDIA:** la página guarda la key solo en la pestaña (`sessionStorage`) y la descarta al cerrarla.
- **Laboratorio en Brev:** la pegas una vez, en el paso **Connect to AI** de la configuración, con el proveedor **NVIDIA CLOUD** seleccionado (campo **NVIDIA CLOUD API KEY**).
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

**Solución:** revisa el uso y el límite en tu cuenta de build.nvidia.com. Para no gastarlos: pon siempre un límite de pasos a tus loops de agente (clase 2.1) y no ejecutes celdas en ráfaga. Si recibes `429`, espera antes de reintentar. En el laboratorio, las automatizaciones también gastan estos créditos: una sola ejecución de prueba usó ≈112 000 tokens.

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

**Solución:** en embeddings, envía `input_type="query"` para preguntas y `"passage"` para documentos (la función `embed()` del curso ya lo hace). En tools, revisa que `parameters` sea un JSON Schema válido. Lee el cuerpo del error: casi siempre nombra el campo.

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

**Solución:** espera 30 a 60 segundos y reintenta una vez. Si persiste, prueba otro modelo o vuelve más tarde. Si el error sale en el chat de tu laboratorio, ve a [Conexión con tu laboratorio](#conexion-laboratorio).

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

**Causa:** Brev cobra por hora mientras la instancia existe. El launchable de NemoClaw usa una instancia **solo CPU** (4 CPUs, 16 GiB, en GCP). El modelo corre en la nube de NVIDIA, no en tu instancia.

**Solución:**
- **Encendida (Running):** ≈**USD 0.25 por hora** (cómputo ≈0.20 + disco ≈0.05). La página de la instancia muestra ≈$0.26/hr.
- **Detenida (Stopped):** el disco sigue cobrando ≈USD 0.05 por hora, unos **USD 1.20 al día**. En un día gasta más que el cupón de 1 USD.
- Con 1 USD tienes unas **4 horas** encendida. El plan del curso usa ≈3 horas en **una sola sentada** y termina con **Delete** (ver [LABORATORIO.md](LABORATORIO.md)).
- Lo que le preguntas al modelo no gasta crédito de Brev: gasta los créditos de tu cuenta de build.nvidia.com.

**Fuente:** prueba del laboratorio del curso (20 de octubre de 2026); [precios de launchables](https://www.nvidia.com/en-us/launchables/pricing).

### ¿Qué me cobra Brev si la detengo y qué si la borro?

**Causa:** son tres estados distintos.

**Solución:**

| Estado | Cómputo | Disco | Costo aprox. | Datos |
|---|---|---|---|---|
| **Running** (encendida) | Se cobra | Se cobra | ≈USD 0.25/h | Se conservan |
| **Stopped** (detenida) | No se cobra | **Se sigue cobrando** | ≈USD 1.20/día | Se conservan (excepto `/tmp`) |
| **Deleted** (borrada) | No | No | USD 0 | **Se pierden para siempre** |

Usa **Stop** solo para pausas cortas: vuelve el mismo día o el siguiente. Al terminar la última práctica (clase 6.1), guarda lo que quieras conservar y usa **Delete**.

**Fuente:** prueba del laboratorio del curso; [Brev: GPU Instances](https://docs.nvidia.com/brev/latest/concepts/gpu-instances); [Console Reference › Billing](https://docs.nvidia.com/brev/latest/guides/console-reference).

### ¿Cómo detengo o borro mi instancia?

**Solución:** en la consola de Brev (brev.nvidia.com) → **Compute** → tu instancia (se llama algo como `nemoclaw-xxxxxx`) → **Stop** para detenerla o **Delete** para borrarla. Confirma que el estado cambie. **Delete** no se puede deshacer.

No necesitas instalar nada: todo el curso usa la consola de Brev en el navegador.

**Fuente:** prueba del laboratorio del curso; [Brev: Console Reference](https://docs.nvidia.com/brev/latest/guides/console-reference).

### ¿Necesito instalar la CLI de Brev o usar SSH?

**Respuesta:** no. Todo el laboratorio se hace en el navegador: la consola de Brev para encender, detener y borrar, y el tablero de tu laboratorio (botón verde **NemoClaw**) para el chat, las terminales y el panel de OpenShell. Los comandos de las guías se pegan en la **VM TERMINAL** del tablero. La pantalla de configuración también ofrece **SET UP OVER SSH**, pero el curso no la usa.

**Fuente:** [LABORATORIO.md](LABORATORIO.md).

### ¿Qué pasa si se me acaban los créditos? ¿Cómo cargo un código?

**Causa:** los créditos de Brev son prepagados y se comparten en toda la organización. Cuando se agotan, Brev actúa sobre tus recursos.

**Solución:** Brev te avisa por correo, **pausa** las instancias que se pueden detener y **borra** las que no. Si a las 24 horas sigues sin saldo, borra todos los recursos y los datos no se recuperan.
- Revisa tu saldo en la pastilla de saldo de la barra de arriba y en **Billing**. Deja la recarga automática apagada.
- Para canjear un código: **Billing → Credits → Redeem Code**. Antes, confirma en el selector de organización (arriba a la derecha) que estás en la organización correcta.

**Fuente:** [Console Reference › Billing](https://docs.nvidia.com/brev/latest/guides/console-reference); prueba del laboratorio del curso.

### `You have run out of credits` pero sí tengo créditos

**Causa:** tienes activa otra organización de Brev. Los créditos son por organización.

**Solución:** en la consola de Brev, abre el **selector de organización** (arriba a la derecha) y elige la organización donde canjeaste el cupón. Revisa que la pastilla de saldo muestre tu crédito y vuelve a desplegar desde ahí.

**Fuente:** [brevdev/brev-cli#390](https://github.com/brevdev/brev-cli/issues/390); [Console Reference](https://docs.nvidia.com/brev/latest/guides/console-reference).

### Mi instancia se queda en **Deploying** o **Waiting**, no hay capacidad o no vuelve a arrancar

**Causa:** el proveedor tarda en asignar la máquina, falló el despliegue (`context deadline exceeded`) o no hay capacidad. Al reiniciar una instancia detenida, Brev intenta el mismo tipo, proveedor y región; si no hay capacidad, el arranque falla y tus datos quedan inaccesibles hasta que vuelva.

**Solución:**
1. Ten paciencia: en la prueba del curso, la instancia pasó a **Running** en ≈1 minuto y la configuración del agente (**Building your agent**) tardó ≈3 minutos. Puede tardar más si hay mucha demanda.
2. En **Compute**, abre tu instancia y revisa la pestaña **Logs**.
3. Si sigue atascada más de 15 minutos, bórrala (**Delete**), espera 30 segundos y créala de nuevo desde el enlace del launchable.
4. Antes de reintentar, revisa en **Compute** que no quedó una instancia duplicada cobrando.
5. Si persiste, escribe a `brev-support@nvidia.com` con tu ID de organización, la instancia y la hora.

El launchable de NemoClaw es solo CPU, así que los problemas de capacidad son menos frecuentes que con GPU.

**Fuente:** [Instance Stuck in Waiting](https://docs.nvidia.com/brev/latest/troubleshooting/instances-gpus/instance-stuck-in-waiting-state); [Brev: GPU Instances](https://docs.nvidia.com/brev/latest/concepts/gpu-instances); [brev-cli#382](https://github.com/brevdev/brev-cli/issues/382).

### La configuración del agente se queda en **Building your agent**, muestra un **RETRY** rojo, pierde el progreso o da `503 ... no_healthy_upstream`

**Causa:** son errores conocidos de la configuración en el navegador. El `503 ... no_healthy_upstream` aparece cuando el proxy de la instancia todavía no ve el servicio; es intermitente.

**Solución:**
- No recargues la pestaña mientras dice **Building your agent**. Los pasos son: Preflight checks, OpenShell gateway, Configure inference, Set inference route y Create sandbox.
- **No hagas clic en RETRY** si el paso ya terminó: RETRY reconstruye todo el sandbox.
- Espera hasta ver **YOUR AGENT IS LIVE**.
- Con el 503, espera un minuto y recarga. Si sigue igual varios minutos, borra la instancia y despliega una nueva.

**Fuente:** [NemoClaw#11536](https://github.com/NVIDIA/NemoClaw/issues/11536), [#8101](https://github.com/NVIDIA/NemoClaw/issues/8101), [#11167](https://github.com/NVIDIA/NemoClaw/issues/11167), [#11535](https://github.com/NVIDIA/NemoClaw/issues/11535).

### Después de detener y volver a encender la instancia, el agente no responde

**Causa:** tras un reinicio de la VM, el gateway de OpenShell y el sandbox pueden tardar en arrancar o no arrancar solos.

**Solución:**
1. Espera un par de minutos y revisa el panel de registros del tablero (filtros **VM**, **Gateway** y **Agent**).
2. Si sigue sin responder, abre la **VM TERMINAL** y pregúntale al laboratorio si está sano:

```bash
nemoclaw my-assistant status       # debe decir Inference healthy y Phase Ready
```

3. Si el sandbox quedó detenido, o el gateway no responde, prueba en este orden:

```bash
nemoclaw my-assistant start        # si el sandbox quedó detenido
nemoclaw my-assistant recover      # si el gateway no responde
openshell gateway info             # el gateway debe aparecer como healthy
```

Si nada de esto funciona, guarda lo que necesites y crea una instancia nueva.

**Fuente:** [Deploy NemoClaw to a Headless Server](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/deployment/deploy-to-headless-server); troubleshooting "Reconnect after a host reboot".

---

<a id="conexion-laboratorio"></a>
## 5. Conexión con tu laboratorio (tablero, chat y terminal)

Esto aplica a las clases 4.1 a 6.1. Tu laboratorio se abre con el botón verde **NemoClaw** de tu instancia en Brev, en una dirección como `https://nemoclaw-<tu-id>.gobrev.dev`.

### Cerré la pestaña del tablero: ¿cómo vuelvo?

**Solución:** cerrar la pestaña no apaga nada. Entra a brev.nvidia.com → **Compute** → tu instancia → botón verde **NemoClaw**. Si la instancia está **Stopped**, enciéndela primero y espera a que diga **Running**.

**Fuente:** [LABORATORIO.md](LABORATORIO.md).

### Me pide iniciar sesión con NVIDIA otra vez

**Causa:** tu laboratorio está protegido por tu inicio de sesión de NVIDIA. Cuando la sesión del navegador vence, o abres el laboratorio desde otro navegador, te lo vuelve a pedir.

**Solución:** es normal. Inicia sesión con la misma cuenta de NVIDIA con la que entras a Brev. No tienes que copiar nada a ningún lado.

### No veo el botón verde **NemoClaw** en mi instancia

**Causa:** la instancia todavía no está lista, está detenida o estás viendo otra organización.

**Solución:**
1. Revisa que el estado diga **Running**. Si dice **Stopped**, enciéndela.
2. Revisa el selector de organización (arriba a la derecha): debe ser la organización donde la creaste.
3. Si acabas de desplegarla, espera un minuto y recarga la página de Brev.

### Me equivoqué de proveedor en **Connect to AI** y el agente no responde

**Causa:** el proveedor viene en **OpenRouter** por defecto. Con tu key `nvapi-` el proveedor debe ser **NVIDIA CLOUD**.

**Solución:** si todavía estás en la configuración, cambia el proveedor a **NVIDIA CLOUD**, pega tu key en **NVIDIA CLOUD API KEY** y haz clic en **CREATE AGENT**. Si el agente ya se creó con otro proveedor, lo más sencillo es borrar la instancia y crear una nueva. Para revisar qué proveedor usa, pega en la **VM TERMINAL**:

```bash
nemoclaw list          # la columna del proveedor debe decir nvidia-prod
```

**Fuente:** prueba del laboratorio del curso.

### ¿Qué es la terminal de operador (VM Terminal)?

**Respuesta:** es la terminal de la computadora que rodea al cuarto del agente (usuario `ubuntu`, carpeta `/home/ubuntu`). La abres con el botón **VM TERMINAL** del tablero. Desde ahí eres el **operador**: revisas al agente, instalas skills, cambias políticas y lees los registros. Es distinta de la **SANDBOX TERMINAL**, que abre una terminal **dentro** del cuarto (usuario `sandbox`, carpeta `/sandbox`), con los mismos límites que el agente.

Para traer los archivos del curso a tu laboratorio, pega esto una vez en la **VM TERMINAL**:

```bash
git clone --depth 1 https://github.com/uncrayon/curso-seguridad-agentes-nemoclaw ~/curso
```

**Fuente:** prueba del laboratorio del curso; [LABORATORIO.md](LABORATORIO.md).

<a id="eterminal"></a>
### Escribí y se abrieron pestañas / no pasa nada en la terminal

**Causa:** la terminal se abre como una ventana encima del tablero. Si escribes sin hacer clic dentro, las teclas van al tablero y activan sus atajos de teclado: pueden abrir pestañas o no hacer nada.

**Solución:**
1. Haz clic dentro del área negra de la terminal.
2. Vuelve a pegar el comando con **Ctrl + V** (en Mac, **Cmd + V**) y presiona **Enter**.
3. Si cerraste la terminal sin querer: **Shift + Esc** la cierra junto con lo que estaba corriendo. Ábrela otra vez con el botón **VM TERMINAL**. La tecla Esc sola se envía a la terminal y no la cierra.

**Fuente:** prueba del laboratorio del curso.

### Todos los comandos `nemoclaw` imprimen `ExperimentalWarning: SQLite is an experimental feature`

**Causa:** es un aviso de Node.js, el programa sobre el que corre la CLI de NemoClaw.

**Solución:** ignóralo. No es un error y no afecta el resultado del comando.

<a id="edenied"></a>
### El agente me dice que abrió una página pero el log dice DENIED

**Causa:** el agente no siempre sabe, o no siempre dice, que su acceso fue bloqueado. En la prueba del curso, al pedirle que abriera `https://docs.openclaw.ai`, el agente intentó con `curl` y con `node`; OpenShell bloqueó los dos y aun así el agente respondió con una frase convincente sobre OpenClaw, sacada de lo que ya sabía. Una respuesta no prueba que hubo acceso.

**Solución:** verifica como operador. En la **VM TERMINAL**:

```bash
nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4
```

Si ves una línea así, la conexión **no** salió del sandbox:

```text
[OCSF ] [ocsf] NET:OPEN [MED] DENIED /usr/bin/curl(11932) -> docs.openclaw.ai:443 [policy:- engine:opa] [reason:binary '/usr/bin/curl' not allowed in policy 'openclaw_docs' ...]
```

Lo mismo vale para lo que el agente dice de sí mismo: en la prueba dijo ser el usuario `gateway-owner`, pero el comando `nemoclaw my-assistant exec -- whoami` responde `sandbox`. Lo que cuenta es lo que ves como operador.

**Fuente:** prueba del laboratorio del curso (clase 5.2).

### El chat se queda pensando o no responde

**Causa:** el modelo tarda, la inferencia no está sana o el gateway se detuvo.

**Solución:**
1. Espera un minuto. El modelo del laboratorio razona antes de responder.
2. Revisa el panel de registros del tablero con el filtro **Agent** o **Gateway**.
3. En la **VM TERMINAL**, pregúntale al laboratorio si está sano:

```bash
nemoclaw my-assistant status       # Inference healthy y Phase Ready
openshell status                   # Status Connected
```

4. Si la inferencia no está sana, revisa tu key y tus créditos en build.nvidia.com (ver [errores de la API](#errores-api)).

**Fuente:** prueba del laboratorio del curso.

### Veo `cannot create /proc/self/oom_score_adj: Permission denied` en la salida del agente

**Causa:** es ruido del sistema dentro del sandbox, no un error de tu ejercicio.

**Solución:** ignóralo.

**Fuente:** [NVDLI/NemoClawDLI#100](https://github.com/NVDLI/NemoClawDLI/issues/100).

### Mi automatización sigue en la lista o se repite y gasta créditos

**Causa:** una automatización con **Repeat** en **Interval** o **Cron** se ejecuta sola una y otra vez, y cada ejecución gasta créditos del modelo (una ejecución de prueba usó ≈112 000 tokens). Las de **Once** con **Delete after run** activado desaparecen solas después de correr.

**Solución:**
1. En el chat, ve a **Automations** y revisa las pestañas **All**, **Active** y **Run history**.
2. Abre la automatización que creaste y desactívala o bórrala.
3. Confirma como operador en la **VM TERMINAL**:

```bash
nemoclaw my-assistant exec -- openclaw cron list
```

Las tareas que vienen con el laboratorio (`heartbeat`, `memory-core…`, `skill-collection-review`) son normales. Que el heartbeat diga `Skipped · heartbeat skipped: no-route` también es normal en el laboratorio.

**Fuente:** prueba del laboratorio del curso (clase 4.3).

---

<a id="openclaw"></a>
## 6. OpenClaw: gateway, dashboard, pairing, workspace y sesiones

### ¿Cómo abro el dashboard (el chat) de OpenClaw?

**Solución en el laboratorio:** en tu tablero, haz clic en **CHAT WITH AGENT**. Se abre el chat de OpenClaw en una pestaña nueva, ya emparejado, con el menú **Home**, **Dashboards**, **Automations**, **Plugins** y **Sessions**. No necesitas tokens ni túneles.

**Solución con NemoClaw en tu máquina:** el dashboard escucha en `http://127.0.0.1:18789/` (si el puerto está ocupado, NemoClaw usa el siguiente libre hasta 18799). Necesita un token:

```bash
nemoclaw <sandbox> dashboard-url --quiet
```

La URL incluye el token en el fragmento `#token=`: trátala como una contraseña. Si el sandbox está en un servidor remoto, abre antes un túnel desde tu computadora:

```bash
ssh -N -L 18789:127.0.0.1:18789 <servidor>
```

Nunca abras a internet el puerto del gateway (18080 en la versión del curso) ni el del dashboard.

**Fuente:** prueba del laboratorio del curso; [quickstart de NemoClaw](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/get-started/quickstart); [headless guide](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/deployment/deploy-to-headless-server).

### `ERR_CONNECTION_REFUSED` en `localhost:18789`

**Causa:** el *port forward* del dashboard se cayó (o no abriste el túnel desde tu máquina). Esto pasa con NemoClaw en tu máquina; en el laboratorio usa el botón **CHAT WITH AGENT** del tablero.

**Solución:**

```bash
openshell forward list            # ¿existe el forward del 18789?
nemoclaw <sandbox> recover        # restaura el gateway y los forwards administrados
```

Si el sandbox está en un servidor remoto, revisa también que siga activo tu túnel `ssh -L`.

**Fuente:** [NemoClaw#1088](https://github.com/NVIDIA/NemoClaw/issues/1088); [CLI selection guide](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/cli-selection-guide).

<a id="epairing"></a>
### *Pairing required*, *Device pairing required* o `scope upgrade pending approval`

**Causa:** OpenClaw exige que cada navegador o CLI se empareje con el gateway. En el laboratorio, el chat que abre **CHAT WITH AGENT** ya viene emparejado; esta entrada aplica sobre todo a NemoClaw en tu máquina. Desde OpenClaw 2026.9.1 el emparejamiento es obligatorio: `NEMOCLAW_DISABLE_DEVICE_AUTH=1` ya **no** lo desactiva. NemoClaw aprueba solo clientes conocidos (`cli`, `openclaw-cli`, `openclaw-control-ui`) con permisos de lectura, escritura y emparejamiento. Si un comando pide más (por ejemplo `operator.admin`), verás `gateway connect failed: GatewayClientRequestError: scope upgrade pending approval (requestId: ...)`.

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
| `IDENTITY.md` | Quién es el agente (nombre y presentación) |
| `POLICY.md` | Notas sobre sus límites |
| `TOOLS.md` | Notas de uso de cada tool |
| `USER.md` | Datos sobre ti (empieza vacío) |
| `HEARTBEAT.md` | Instrucciones del heartbeat (~cada 30 min) |
| `memory/AAAA-MM-DD.md` | Notas diarias que el agente va agregando |
| `MEMORY.md` | Memoria de largo plazo, curada |
| `skills/<nombre>/SKILL.md` | Skills instaladas |

En un laboratorio recién creado solo están los siete archivos `.md` de arriba (de `SOUL.md` a `HEARTBEAT.md`): `MEMORY.md`, `memory/` y `skills/` aparecen cuando el agente o tú los crean.

Para verlo como operador, en la **VM TERMINAL**:

```bash
nemoclaw my-assistant exec -- ls -la /sandbox/.openclaw/workspace
```

**Fuente:** prueba del laboratorio del curso; basado en la lección 03b del curso NVIDIA DLI «NemoClaw» (Apache-2.0).

### El agente "olvidó" lo que le dije

**Causa:** OpenClaw tiene dos memorias. El historial de la conversación vive en la **sesión** (identificada por su `sessionKey`). Lo que sobrevive entre sesiones es lo que el agente escribe en archivos (`MEMORY.md`, `memory/`). Si abres una sesión nueva o la reinicias, el historial anterior no está.

**Solución:**
- Usa la misma clave de sesión para continuar una conversación.
- Pídele que guarde lo importante en `MEMORY.md`.
- Para ver o reiniciar sesiones:

```bash
nemoclaw <sandbox> sessions list --json          # más fácil de leer que la tabla
nemoclaw <sandbox> sessions reset <clave>        # archiva y empieza de cero
```

En el laboratorio puedes comprobarlo con una clave de sesión de prueba:

```bash
nemoclaw my-assistant agent --session-key memo-41 -m 'Recuerda este codigo: CODE-7Q4. No lo escribas en ningun archivo. Responde solo OK.'
nemoclaw my-assistant agent --session-key memo-41 -m 'Cual era el codigo que te di? Responde solo el codigo.'
nemoclaw my-assistant sessions reset memo-41
nemoclaw my-assistant agent --session-key memo-41 -m 'Cual era el codigo que te di? Si no lo sabes, responde: no lo se.'
```

Antes del `reset` responde `CODE-7Q4`; después, `no lo se`.

**Fuente:** prueba del laboratorio del curso; basado en las lecciones 03a y 03b del curso NVIDIA DLI «NemoClaw» (Apache-2.0); [commands](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands) (`sessions`).

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

**Solución:** en el laboratorio, lo más sencillo es el chat (**CHAT WITH AGENT**). Desde la **VM TERMINAL**, un turno sin interfaz:

```bash
nemoclaw my-assistant agent --session-key prueba -m 'Hola, ¿qué skills tienes?'
```

Con NemoClaw en tu máquina también puedes abrir la interfaz de texto:

```bash
nemoclaw launch <sandbox>                      # verifica y abre la TUI
# o bien
nemoclaw <sandbox> connect                     # shell dentro del sandbox
openclaw tui
```

**Fuente:** prueba del laboratorio del curso; [quickstart de NemoClaw](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/get-started/quickstart).

### ¿Cómo instalo una skill y por qué el agente no la usa?

**Causa:** una skill es una carpeta con un `SKILL.md` (con *frontmatter* YAML y un campo `name`). Que esté instalada no garantiza que el agente la elija solo.

**Solución:**

```bash
nemoclaw <sandbox> skill install ./mi-skill/
nemoclaw <sandbox> skill list
```

En el laboratorio, con los archivos del curso en `~/curso`, la skill de la clase 4.3 se instala así y responde `✓ Validated SKILL.md`:

```bash
nemoclaw my-assistant skill install ~/curso/clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/
```

Para probarla, abre una sesión nueva y menciónala o da la ruta de su `SKILL.md`. La selección automática es otra prueba aparte. El nombre solo admite letras, números, puntos, guiones y guiones bajos.

**Fuente:** [commands](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands) (`skill install`); prueba del laboratorio del curso; basado en la lección 03c del curso NVIDIA DLI «NemoClaw» (Apache-2.0).

---

<a id="openshell"></a>
## 7. OpenShell y políticas

<a id="e403tunnel"></a>
### `curl: (56) CONNECT tunnel failed, response 403`

**Causa:** **no** es un problema de certificados ni de la herramienta. La red de salida del sandbox está bloqueada por defecto y el proxy de OpenShell rechazó la conexión. Para que pase, deben coincidir **el host y el binario** que hace la llamada.

**Solución:**

```bash
nemoclaw <sandbox> logs --tail 300 | grep DENIED | tail -4   # la línea DENIED (host y binario)
nemoclaw <sandbox> policy list                               # presets aplicados
nemoclaw <sandbox> policy add <preset>
```

En el laboratorio, `https://example.com` desde el sandbox da este error, mientras que `https://pypi.org` (nivel Balanced) y la API de modelos de NVIDIA responden `200`. Para una prueba puntual, apruébalo en vivo con el botón **OPENSHELL TUI** del tablero (o `openshell term`). Si usas `nemoclaw <sandbox> exec -- <comando>`, NemoClaw te imprime una pista con el host bloqueado; para silenciarla: `export NEMOCLAW_NO_POLICY_HINT=1`. Un error HTTP puede venir del proxy o de la aplicación destino: identifica la fuente antes de culpar a la política.

**Fuente:** troubleshooting "A request inside the sandbox fails with `CONNECT tunnel failed, response 403`"; prueba del laboratorio del curso; basado en la lección 04a del curso NVIDIA DLI «NemoClaw» (Apache-2.0).

### ¿Cómo apruebo en vivo un acceso de red bloqueado con `openshell term`?

**Solución:** usa la TUI de OpenShell en el host. En el laboratorio, haz clic en **OPENSHELL TUI** en tu tablero. Con NemoClaw en tu máquina, ejecuta:

```bash
openshell term
```

1. Elige el sandbox con `j`/`k` y `Enter`. (`Tab` cambia de panel y `q` sale.)
2. Pulsa `r` para ir a las reglas. Ahí aparecen las solicitudes pendientes, por ejemplo `openclaw_docs` vía `curl`.
3. Elige la solicitud pendiente (`Enter` muestra detalles, incluida la ruta del binario).
4. `a` aprueba, `x` rechaza, `A` aprueba todas. `p` muestra la política.

Ojo: estas aprobaciones duran solo mientras exista esa instancia del sandbox. Al recrearlo se pierden y no se escriben en la política base; si lo necesitas siempre, usa un preset (`nemoclaw <sandbox> policy add`).

Según la documentación, en la TUI `policy_denied` significa que ninguna regla coincidió, y `upstream_unreachable` que la política lo permitió pero el host no respondió (DNS, red o servicio caído). Las teclas de arriba son las de OpenShell 0.0.116, la versión del laboratorio.

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

En el laboratorio lo verás con `docs.openclaw.ai`: el grupo `openclaw_docs` existe, pero no permite ni `/usr/bin/curl` ni `/usr/local/bin/node`, así que el agente no llega a esa página.

**Solución:** lee la línea `DENIED` en `nemoclaw <sandbox> logs --tail 300 | grep DENIED` (o el detalle en la OpenShell TUI), copia la ruta exacta del binario y agrégala a la sección `binaries:` de tu preset propio.

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

### El puerto 18789 o el del gateway ya está en uso (o `Port 18789 is not available. Blocked by: ssh`)

**Causa:** otro programa, un onboarding anterior o un túnel SSH viejo ocupa el puerto del dashboard (18789) o del gateway (18080 en la versión del curso; versiones anteriores usaban 8080). `openshell gateway info` te dice qué puerto usa el tuyo.

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

**Causa:** cada versión de NemoClaw fija una versión exacta de OpenShell (la v0.0.135 del laboratorio fija la **0.0.116**, mínima y máxima). OpenShell ya va en la 0.1.x, que cambió el formato de configuración del gateway y es incompatible.

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
- Las cookies de sesión de tu navegador para Brev y tu laboratorio (por ejemplo `__Host-skybridge-brev-prd`). El curso nunca te pide copiarlas.
- El valor de `OPENCLAW_GATEWAY_TOKEN` que aparece si listas las variables de entorno dentro del sandbox.
- La URL del dashboard con `#token=` y la salida de `nemoclaw <sandbox> gateway-token`.
- Tus archivos `.env` y `~/.nemoclaw/credentials.json`.
- Exportaciones de sesiones (`sessions export`): pueden contener secretos que pegaste en el chat.

**Fuente:** [headless guide](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/deployment/deploy-to-headless-server); [commands](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/commands) (`sessions export`); lección 03a del curso de NVIDIA.

<a id="efiltrada"></a>
### Filtré mi API key (la subí a GitHub, salió en un video o en una captura)

**Causa:** cualquiera que la vea puede gastar tus créditos. Borrar el archivo o hacer otro commit **no** basta: la key sigue en el historial de git y en las copias que alguien haya hecho.

**Solución:**
1. **Revócala ya** en build.nvidia.com → **API Keys** (bórrala o desactívala). Si no ves ese menú, búscalo en tu perfil: la interfaz cambia seguido.
2. Genera una key nueva.
3. Actualízala donde la uses: secreto de Colab, `.env`, y NemoClaw (ver [rotar la key](#instalacion-local)).
4. Revisa tu uso en build.nvidia.com por si hubo consumo extraño.
5. Quita la key del repo y agrega `.env` a `.gitignore`. Asume que la key vieja ya es pública aunque limpies el historial.

**Fuente:** [credential rotation](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/security/credential-rotation); notas de producción de la clase 1.2.

### Compartí sin querer un token, una cookie o una captura con datos de mi laboratorio

**Causa:** la dirección de tu laboratorio (`nemoclaw-<tu-id>.gobrev.dev`) pide iniciar sesión con NVIDIA, pero un token del gateway, una URL con `#token=` o una cookie de sesión podrían dejar entrar a otra persona mientras sigan vigentes.

**Solución:**
1. Si ya no necesitas el laboratorio, bórralo: brev.nvidia.com → **Compute** → tu instancia → **Delete**. Es lo más seguro.
2. Si todavía estás a mitad de la práctica, detenlo con **Stop**, cierra sesión en Brev y vuelve a entrar.
3. Si en la captura salía tu API key, revócala también (ver [key filtrada](#efiltrada)).

**Fuente:** [Brev: Console Reference](https://docs.nvidia.com/brev/latest/guides/console-reference); [gateway authentication controls](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/security/gateway-authentication-controls).

### ¿Es seguro abrir el dashboard o el gateway a internet?

**Causa:** el gateway (puerto 18080 en la versión del curso) controla el agente y el dashboard (18789) da acceso a él.

**Solución:** no. En el laboratorio no tienes que abrir nada: el tablero y el chat ya están detrás de tu inicio de sesión de NVIDIA. Con NemoClaw en un servidor propio, usa un túnel (`ssh -L 18789:127.0.0.1:18789`), que mantiene el origen en `127.0.0.1`. Nunca abras el puerto del gateway. Si necesitas exponer el dashboard, hazlo detrás de HTTPS y con el pairing activo.

**Fuente:** [gateway authentication controls](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/security/gateway-authentication-controls); [headless guide](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/deployment/deploy-to-headless-server).

### ¿Dónde guarda NemoClaw mis keys? ¿Las ve el agente?

**Solución:** NemoClaw registra las keys de proveedores en el gateway de OpenShell, del lado del host. Desde la v0.0.132–0.0.133, los sandboxes nuevos usan proveedores adjuntos al sandbox y las credenciales se quedan en el host. Por eso **no** debes poner keys dentro de `openclaw.json` ni en archivos del workspace: lo que está dentro del sandbox, el agente lo puede leer.

**Fuente:** [credential storage](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/security/credential-storage); troubleshooting "Change OpenClaw Configuration Inside the Sandbox"; changelog v0.0.132 y v0.0.133.

---

<a id="hermes"></a>
## 10. Hermes en NemoClaw

### ¿Hermes reemplaza a NemoClaw?

**Respuesta:** no. NemoClaw es el sandbox de OpenShell, las políticas, la inferencia administrada y el ciclo de vida. Hermes (de Nous Research) es **un agente** que vive dentro, como OpenClaw o LangChain Deep Agents. Cambias el agente con `nemohermes onboard` (o `NEMOCLAW_AGENT=hermes`) y la seguridad se queda igual.

**Fuente:** clase 4.4; [NemoClaw · Ecosistema](https://docs.nvidia.com/nemoclaw/latest/user-guide/hermes/about/ecosystem).

### `nemohermes: command not found`

**Causa:** tu versión del CLI de NemoClaw es anterior a los alias por agente, o el `PATH` no incluye el CLI.

**Solución:** `NEMOCLAW_AGENT=hermes nemoclaw onboard` hace lo mismo. Para actualizar: `nemoclaw update`. Revisa tu versión con `nemoclaw --version`. En el laboratorio del curso, `nemohermes` ya viene instalado (v0.0.135, en `/usr/bin/nemohermes`).

**Fuente:** [NemoClaw · Comandos de nemohermes](https://docs.nvidia.com/nemoclaw/latest/user-guide/hermes/reference/commands).

### ¿Dónde están SOUL.md, la memoria y las skills de Hermes?

**Respuesta:** la personalidad en `/sandbox/SOUL.md`. Todo lo demás en `/sandbox/.hermes/`: `config.yaml` (lo genera NemoClaw; no lo edites a mano porque `rebuild` lo regenera), `memories/MEMORY.md` y `USER.md`, `skills/`, `state.db` (sesiones en SQLite) y `logs/`. `destroy` borra todo; `rebuild` y las actualizaciones lo conservan.

**Fuente:** [NemoClaw · Estado del sandbox de Hermes](https://docs.nvidia.com/nemoclaw/latest/user-guide/hermes/manage-sandboxes/state-and-backups/understand-sandbox-state).

### `curl: (7) Failed to connect to 127.0.0.1 port 8642` o `401` en la API de Hermes

**Causa:** la API tomó otro puerto (8642 a 8652 si hay otro sandbox), el forward se cayó tras un reinicio, o el token es incorrecto.

**Solución:** `openshell forward list` para ver el puerto real; si no aparece, `nemohermes <sandbox> recover`. Para el token: `TOKEN="$(nemohermes <sandbox> gateway-token --quiet)"` y envíalo como `Authorization: Bearer $TOKEN`. El token cambia si reconstruyes el sandbox.

**Fuente:** [NemoClaw · Quickstart con Hermes](https://docs.nvidia.com/nemoclaw/latest/user-guide/hermes/get-started/quickstart).

### ¿Puedo ver desde mi programa lo que Hermes hace dentro del sandbox?

**Respuesta:** no. Desde el host, un programa como `hermes_api.py` solo ve la pregunta y la respuesta. Las herramientas que Hermes ejecuta dentro del sandbox (sus `grep` o `cat`) están en su historial de sesiones: `nemohermes <sandbox> sessions export`. Con OpenClaw es igual: `nemoclaw <sandbox> sessions export`. El archivo exportado contiene prompts y salidas de herramientas: trátalo como dato sensible.

**Fuente:** clase 4.4.

### Instalé una skill en Hermes y no la usa

**Causa:** Hermes carga las skills al iniciar la sesión, o la `description` del `SKILL.md` no coincide con cómo pregunta el estudiante.

**Solución:** confirma con `nemohermes <sandbox> skill list`, sal con `/exit` y abre una sesión nueva. Prueba la skill como comando (`/soporte-nemoclaw ...`). Si quieres reemplazarla, primero `skill remove`: sin comando nativo de Hermes, `skill install` no sobrescribe una carpeta con el mismo nombre.

**Fuente:** clase 4.4.

### Hermes guardó algo en su memoria que yo no quería

**Causa:** Hermes escribe en su memoria y crea skills por su cuenta. Sin aprobación, una instrucción (tuya o de un texto malicioso) queda guardada para sesiones futuras.

**Solución:** según la documentación de Hermes, dentro de Hermes puedes usar `/memory approval on` y `/skills approval on`; revisar con `/memory pending` y rechazar con `/memory reject <id>`. Si tu versión muestra otros nombres, revisa su ayuda dentro de Hermes. Lee `/sandbox/.hermes/memories/MEMORY.md` como operador y limpia lo que no reconozcas.

**Fuente:** [Hermes Agent · Memoria](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory); clase 4.4 y Módulo 5.

---

<a id="pedir-ayuda"></a>
## 11. Cómo pedir ayuda bien

Una buena pregunta se responde en minutos; una vaga, en días. Antes de preguntar, busca tu mensaje de error exacto en esta página (Ctrl+F / Cmd+F).

### Qué incluir

1. **Qué intentabas hacer:** clase (por ejemplo, 4.2), paso y comando exacto que ejecutaste.
2. **Qué esperabas y qué pasó:** el mensaje de error **completo y literal** (copiado como texto, no como foto).
3. **Dónde:** notebook en Colab, notebook local, curso web de NVIDIA, laboratorio de Brev (tablero, chat, **VM TERMINAL** u **OPENSHELL TUI**) o NemoClaw en tu máquina. Sistema operativo.
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
- Cookies de sesión del navegador (por ejemplo `__Host-skybridge-brev-prd`) ni el valor de `OPENCLAW_GATEWAY_TOKEN`.
- La URL del dashboard con `#token=` ni la salida de `gateway-token`.
- Tu `.env`, `credentials.json` o archivos `.pem`.

Si un log o una captura incluye alguno de estos valores, reemplázalo por `nvapi-xxxxxxxx` o `<REDACTADO>`. Si ya lo pegaste, sigue los pasos de [key filtrada](#efiltrada).

### Dónde preguntar

| Tipo de problema | Dónde |
|---|---|
| Dudas del curso, notebooks, ejercicios | Comunidad de Platzi, en la sección de comentarios de la clase |
| Cuenta de NVIDIA Build, verificación de teléfono | `help@build.nvidia.com` o `https://developer.nvidia.com/support` |
| Brev: facturación, instancias trabadas, límites de la organización | `brev-support@nvidia.com` |
| Curso web de NVIDIA (páginas y panel de la API key de los Módulos 1 a 3) | Issues de [NVDLI/NemoClawDLI](https://github.com/NVDLI/NemoClawDLI/issues) |
| Bugs de NemoClaw | Issues de [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw/issues) (busca primero si ya existe) |
| Preguntas generales sobre NemoClaw | [Discussions de NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw/discussions) |
| Bugs de OpenShell | Issues de [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell/issues) |

---

*Basada en la documentación pública de NVIDIA NemoClaw (Apache-2.0), en el curso de NVIDIA DLI "Securing Agents with OpenShell and NemoClaw" ([NVDLI/NemoClawDLI](https://github.com/NVDLI/NemoClawDLI), Apache-2.0), en la documentación de NVIDIA Brev y en issues públicos de GitHub revisados el 14 de octubre de 2026, y en una prueba completa del laboratorio del curso el 20 de octubre de 2026. Versión de referencia: NemoClaw v0.0.135, OpenShell 0.0.116, OpenClaw v2026.9.2.*
