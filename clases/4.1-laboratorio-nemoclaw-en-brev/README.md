# 4.1 · Levanta el laboratorio NemoClaw en Brev

Despliega el launchable de NemoClaw en Brev, conéctate por navegador y por terminal, verifica las 4 rutas y aprende a pausarlo sin gastar créditos de más.

| | |
|---|---|
| Duración del video | ≈9 min |
| Práctica | Laboratorio en Brev: página del curso de NVIDIA + terminal ([cookbook.md](cookbook.md)) |
| Habilidad | Desplegar NemoClaw en Brev |

Material: [diapositivas](slides.html) · [recetario de terminal](cookbook.md) · [preguntas frecuentes del curso](../../FAQ.md)

> Basado en la lección 03a-kickstart del curso de NVIDIA DLI (Apache-2.0).

## Lo esencial (sin tecnicismos)

**La idea:** Vas a rentar una computadora en la nube con Brev, el servicio de NVIDIA que presta computadoras por horas, y a sentar ahí a tu agente dentro de su cuarto con cerradura. Todo se puede hacer con clics: desplegar, conectar la página del curso y apagar la máquina al terminar.

**Piénsalo como:** rentar una oficina por horas que ya trae muebles, internet y llaves. Con la luz encendida cobra; con la luz apagada cobra solo el disco.

**Palabras nuevas:** [launchable](../../GLOSARIO.md), [instancia](../../GLOSARIO.md), [cookie de sesión](../../GLOSARIO.md).

**Hazlo sin programar (≈10 min):** Con tu laboratorio desplegado (pasos 1 a 7, todo en la consola de Brev), abre la [lección 03a](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/03a-kickstart.html), conecta la página con tu cookie (pasos 8 a 12) y presiona **Chat breve** (Paso 1) y **▶ Ejecutar todo** (Paso 3). Anota en dos líneas qué recordó el agente antes y después de reiniciar la conversación. Termina con **Stop** en la consola de Brev.

**Qué te llevas:** sabes encender, usar y apagar tu propio laboratorio en la nube sin gastar crédito de más.

**Tu crédito:** esta práctica usa ≈30 min de instancia encendida, incluida la espera del despliegue `[VERIFICAR EN LAB]`. Al terminar, detén la instancia (ver [LABORATORIO.md](../../LABORATORIO.md)).

## Lo que vas a lograr

- Tener tu propio laboratorio NemoClaw corriendo en Brev: OpenClaw (el agente) dentro de OpenShell (el sandbox).
- Conectarte de dos formas: desde la página del curso de NVIDIA (navegador) y desde tu terminal con la CLI `brev`.
- Detener y reanudar la instancia sabiendo cuánto cuesta cada estado.

## Antes de empezar

- Tu API key `nvapi-` de la clase 1.2, guardada en el panel de la página del curso de NVIDIA (la usamos para el paso de control).
- Un navegador de escritorio con herramientas de desarrollador: Chrome, Edge, Brave, Firefox o Safari. Desde el celular no se puede.
- Una cuenta de NVIDIA (la misma de build.nvidia.com) para entrar a Brev.
- Para la ruta de terminal: macOS, Linux o Windows con WSL (Ubuntu 22.04 o superior). La CLI `brev` no corre en Windows nativo.
- 20 minutos sin prisa: el despliegue tarda entre 5 y 15 minutos.

Las piezas que vas a levantar, en una frase cada una:

| Pieza | Qué hace |
|---|---|
| Endpoint del modelo | Convierte un prompt en texto. No recuerda nada entre llamadas. |
| OpenClaw | El agente (el *harness*): guarda el historial de la sesión, un workspace de archivos y las herramientas. |
| OpenShell | El sandbox: limita a qué archivos, red y procesos llega el agente. |
| NemoClaw | El blueprint que configura OpenClaw dentro de OpenShell. |

## Paso a paso

### Parte A · Despliega el launchable

1. **Entra a Brev.** Abre https://brev.nvidia.com e inicia sesión con tu cuenta de NVIDIA.
   Deberías ver: la consola de Brev con secciones como **GPUs**, **Launchables** y **Billing**.

2. **Revisa tu organización.** En Brev los créditos y las instancias pertenecen a una *organización*, no a tu usuario. Si te invitaron a varias (por ejemplo, la de tu empresa y la personal), revisa cuál está activa antes de desplegar. `[VERIFICAR EN LAB: dónde está el selector de organización en la consola y si una cuenta nueva recibe una organización personal automáticamente]`

3. **Revisa tus créditos.** Ve a **Billing**. Ahí ves el saldo y puedes canjear un código en **Credits → Redeem a credit code**. La página del curso de NVIDIA anuncia que NVIDIA cubre el costo de Brev por tiempo limitado con un crédito de 1 USD para los primeros 25 000 usuarios (uno por persona), suficiente para los 4 módulos. `[VERIFICAR EN LAB: si el crédito sigue vigente y si se aplica solo o hay que canjearlo]`

   **Atención:** No actives la recarga automática (*auto-recharge*) si trabajas con créditos prepagados.

4. **Abre el launchable de NemoClaw:**
   https://brev.nvidia.com/launchable/deploy/now?launchableID=env-3Azt0aYgVNFEuz7opyx3gscmowS&ncid=ref-dli-759990

   Deberías ver: la página de despliegue con el tipo de instancia, el proveedor y el costo por hora. Según los reportes públicos de NVIDIA (septiembre-octubre de 2026), es una instancia **solo CPU** `n2d-standard-4` (4 vCPU, 16 GiB de RAM) en Google Cloud, marcada como **Free**. No necesitas GPU: el modelo corre en la nube de NVIDIA. `[VERIFICAR EN LAB: tipo de instancia, precio, tamaño de disco y si aparece como Free]`

5. **Despliega.** Haz clic en el botón de despliegue (en la versión anterior se llamaba **Deploy NemoClaw**). Deja la pestaña abierta. `[VERIFICAR EN LAB: texto exacto del botón]`
   Deberías ver: un panel lateral con el progreso. La instancia pasa por los estados `DEPLOYING` → `STARTING` → `RUNNING`. Calcula entre 5 y 15 minutos: Brev crea la máquina en 1-2 minutos y la configuración del agente toma unos 5 más.

6. **Configura el agente si te lo pide.** La interfaz del launchable cambia seguido. Vas a ver una de estas dos cosas:
   - **Un asistente con tres opciones** (SET UP IN THIS BROWSER, SET UP OVER SSH, SET UP WITH MY CODING AGENT). Elige **SET UP IN THIS BROWSER**, deja **OpenClaw** como agente y **NVIDIA Cloud** como proveedor, pega tu key `nvapi-` y crea el agente. Termina con un mensaje tipo "AGENT CREATED SUCCESSFULLY".
   - **Un dashboard** con una tarjeta **my-assistant** ya corriendo. Haz clic en **Chat with Agent**.

   `[VERIFICAR EN LAB: cuál de los dos flujos muestra el launchable el día de la grabación]`

   **Atención:** Durante la configuración **no recargues la pestaña** y **no hagas clic en RETRY** aunque veas una tarjeta roja: si el registro de actividad avanza, el paso sí funcionó, y RETRY reconstruye todo el sandbox.

7. **Copia la URL de tu launchable.** Es la dirección de la app de NemoClaw y tiene esta forma (cambia el dominio según el proveedor de acceso):
   - `https://nemoclaw-<id>.brevlab.com`
   - `https://nemoclaw-<id>.apps.run.brev.nvidia.com`
   - `https://nemoclaw-<id>.gobrev.dev`

   Captura: la barra de direcciones de la pestaña de NemoClaw con el host `nemoclaw-…` resaltado. `[VERIFICAR EN LAB: en qué parte de la consola de Brev aparece esta URL]`

### Parte B · Conéctate desde el navegador (página del curso de NVIDIA)

La página del curso vive en `nvdli.github.io`, un dominio distinto al de tu launchable. Por eso necesita dos cosas: la **URL base** y tu **sesión de acceso** (una cookie del navegador).

8. **Abre la lección** [Conecta NemoClaw](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/03a-kickstart.html) y baja a **Inicia el launchable → Inspecciona las cuatro rutas de conexión**. Vas a ver el panel **Conectar NemoClaw** con dos campos: **URL base** y **Sesión de acceso**.

9. **Pega la URL base** del paso 7. La página se queda solo con el origen (borra rutas como `/onboard`).

10. **Lee esto antes de copiar la cookie.**

    > **Una cookie de sesión es una contraseña.** Quien la tenga puede actuar como tú en ese launchable hasta que expire.
    > 1. Pégala **solo** en el campo **Sesión de acceso** de la página del curso. Nunca en un chat, un issue, una captura ni un video.
    > 2. La página la guarda solo en esa pestaña (`sessionStorage`) y la borra al cerrarla.
    > 3. Al terminar, cierra sesión en Brev y detén la instancia.
    > 4. Si grabas tu pantalla, difumina el valor.

11. **Copia la cookie correcta.** En la pestaña del launchable (con la sesión iniciada), abre las herramientas de desarrollador y busca la cookie según el dominio de tu URL:

    | Tu URL contiene | Cookie que copias |
    |---|---|
    | `brevlab.com` | `CF_Authorization` |
    | `apps.run.brev.nvidia.com` | `_pomerium` |
    | `gobrev.dev` | `__Host-skybridge-brev-prd` |

    - **Chrome, Edge o Brave:** `F12` (o `Cmd+Opt+I` en Mac) → pestaña **Application** → **Storage → Cookies** → elige el origen del launchable → busca la cookie → doble clic en la celda **Value** → copia.
    - **Firefox:** `F12` → pestaña **Storage** (Almacenamiento) → **Cookies** → origen del launchable → selecciona la fila → doble clic en el valor → copia.
    - **Safari:** primero activa **Ajustes → Avanzado → Mostrar funciones para desarrolladores web**. Luego `Cmd+Opt+I` → pestaña **Storage** → **Cookies** → origen del launchable → copia el valor.

    Copia **solo el Value completo**. No copies el encabezado `Cookie` entero ni el nombre de la cookie.

12. **Pega el valor en Sesión de acceso y haz clic en Probar conexión.** La página corre 4 pruebas en orden:

    | Ruta | Qué comprueba |
    |---|---|
    | Metadatos del agente (`GET /api/agent`) | Que tu sesión es válida. De aquí la página saca el **token del gateway** (no lo escribas tú). |
    | Gateway (WebSocket `/cli/gateway`) | Que el gateway de OpenClaw responde y acepta el token. |
    | Terminal (WebSocket `/ws/terminal`) | Que hay una terminal de operador en la máquina. |
    | Health (`GET /healthz`) | Que el runtime está sano. |

    Deberías ver: `Conexión lista. Las pruebas de metadatos, gateway, terminal y estado se aprobaron.` y la pastilla de arriba en **OpenClaw ✓**.
    Si ves `OpenClaw is starting. Retrying in N seconds.`, espera: la página reintenta sola hasta 30 minutos.

13. **Haz el control: una llamada directa al modelo, sin agente.** En **Paso 1 · Establece el control directo del modelo**, usa **Probar el endpoint activo del modelo** y luego **Chat breve**.
    Deberías ver: una respuesta normal del modelo `nvidia/nemotron-3.5-lightning-30b-a3b`. Sin herramientas ni memoria. Esta es tu línea base.

14. **Haz un turno de agente a través del gateway.** En **Paso 2**, abre el flujo **Gateway · protocolo WebSocket paso a paso**:
    1. Ejecuta el nodo **Abre la conexión del gateway** (botón **▶ Ejecutar**).
    2. Ejecuta **Llama a models.list y cron.list**. Deberías ver la lista de modelos y `cron jobs: (none)`.
    3. Abre el código de **Envía un mensaje de chat por streaming**. La **última** línea `message = …` sin comentar es la que se envía. Déjala así o cámbiala por:
       ```js
       message = "Usa tu herramienta exec para ejecutar `whoami` y `pwd` en tu sandbox y dime en una frase qué usuario eres y dónde estás.";
       ```
    4. Ejecuta el nodo.

    Deberías ver: filas `⚙️` (cada una es una llamada a herramienta con sus argumentos) y filas `✓` (el resultado). La respuesta menciona el usuario `sandbox` y la carpeta `/sandbox`. `[VERIFICAR EN LAB: salida exacta de whoami y pwd]`

15. **Prueba que la memoria vive en la `sessionKey`.** En **Paso 3 · Compara el historial de la conversación**, haz clic en **▶ Ejecutar todo** del flujo **Compara el historial antes y después del restablecimiento**:
    - **Introduce un dato nuevo:** le da al agente un código `CODE-…` y le pide no escribirlo en archivos.
    - **Recupera el dato sin volver a introducirlo:** el agente lo recuerda.
    - **Restablece la sesión y vuelve a preguntar:** llama a `sessions.reset` y el agente ya no lo sabe.
    - **Elimina solo las sesiones de este flujo:** limpia lo que creó.

    Deberías ver: `recalled` con el código antes del reset y "unknown" (o equivalente) después. Lo único que el cliente envía es la clave de sesión: el gateway reconstruye la conversación del lado del servidor.

### Parte C · Conéctate desde tu terminal

Los comandos completos, con su salida esperada y qué hacer si fallan, están en el [cookbook](cookbook.md). El resumen:

16. **Instala la CLI de Brev e inicia sesión:**
    ```bash
    # macOS
    brew install brevdev/homebrew-brev/brev
    # Linux o WSL (sin sudo)
    bash -c "$(curl -fsSL https://raw.githubusercontent.com/brevdev/brev-cli/main/bin/install-latest.sh)"

    brev --version
    brev login
    ```

17. **Busca tu instancia y entra:**
    ```bash
    brev ls
    brev shell <instancia>      # sin --host
    ```
    Deberías ver: tu instancia en estado `RUNNING` y, tras `brev shell`, un prompt dentro de la máquina de Brev.

    **Atención:** No uses `brev shell <instancia> --host` con este launchable: se queda esperando hasta agotar el tiempo (issue conocido de NemoClaw con la CLI ≥ v0.6.331).

18. **Revisa el stack desde dentro de la máquina:**
    ```bash
    nemoclaw list
    nemoclaw status
    openshell sandbox list
    nemoclaw my-assistant status
    ```
    Deberías ver: tu sandbox (normalmente `my-assistant`) en estado `Ready` y la ruta de inferencia `healthy`. Si tu sandbox tiene otro nombre, usa el que muestra `nemoclaw list` en todos los comandos. `[VERIFICAR EN LAB: nombre del sandbox en el launchable]`

19. **Abre el dashboard de OpenClaw en tu computadora** (opcional). En una terminal local, deja corriendo el túnel:
    ```bash
    brev port-forward <instancia> -p 18789:18789
    ```
    En la terminal de `brev shell`, pide la URL autenticada:
    ```bash
    nemoclaw my-assistant dashboard-url --quiet
    ```
    Abre esa URL en tu navegador. Contiene el token del gateway después de `#token=`: trátala como una contraseña.

### Parte D · Pausa, reanuda y no gastes de más

20. **Entiende los tres estados:**

    | Estado | Cómputo | Disco | Tus datos |
    |---|---|---|---|
    | Corriendo (`RUNNING`) | Se cobra por hora | Se cobra | Ahí están |
    | Detenida (`STOPPED`) | No se cobra | **Se sigue cobrando** | Se conservan (menos `/tmp`) |
    | Eliminada | Nada | Nada | **Se pierden para siempre** |

    El disco cuesta 0.0001314 USD por GB-hora. Con un disco de 100 GB, una semana detenida cuesta unos 2.2 USD. `[VERIFICAR EN LAB: tamaño real del disco del launchable]`

21. **Detén la instancia al terminar cada sesión de estudio.** En la consola: **GPUs** → tu instancia → **Stop**. O desde tu terminal:
    ```bash
    brev stop <instancia>
    brev ls
    ```
    Si ves `instance "<nombre>" does not support stop.`, ese tipo de instancia no se puede pausar: respalda tu workspace (receta 11 del cookbook) y elimínala con `brev delete <instancia>`. `[VERIFICAR EN LAB: si la instancia del launchable es stoppable]`

22. **Reanuda y vuelve a verificar:**
    ```bash
    brev start <instancia>
    brev refresh
    brev shell <instancia>
    nemoclaw my-assistant status
    ```
    Después vuelve a la página del curso: tu cookie probablemente expiró, así que copia una nueva (paso 11) y repite **Probar conexión**.

    Ojo: si el proveedor no tiene capacidad, `brev start` falla y tus datos quedan inaccesibles hasta que vuelva la capacidad. Con una instancia de CPU es poco común, pero pasa.

## Comprueba que funcionó

- [ ] `brev ls` muestra tu instancia en `RUNNING`.
- [ ] **Probar conexión** muestra `Conexión lista` con las 4 rutas en verde.
- [ ] El control directo al modelo responde sin herramientas.
- [ ] El turno por el gateway muestra una fila `⚙️` de `exec` y su resultado `✓`.
- [ ] El código plantado se recuerda antes del reset y se olvida después.
- [ ] Desde `brev shell`, `openshell sandbox list` muestra tu sandbox en `Ready`.
- [ ] Sabes detener tu instancia y la dejaste en `STOPPED` al terminar.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `OpenClaw is starting. Retrying in N seconds. Use Stop to cancel.` | El runtime todavía arranca (`/api/agent` responde 503 `starting`). | Espera. La página reintenta sola hasta 30 min. Si pasan más de 15 min, revisa la consola de Brev. |
| La URL de puerto 80 muestra `503 … no_healthy_upstream` aunque Brev dice HEALTHY | Falla intermitente del proxy del launchable. | Espera un par de minutos y recarga. Si sigue, despliega una instancia nueva. |
| La prueba de NemoClaw da 502 o agota el tiempo | Un 502 solo no dice la causa. | Abre la prueba que falló y lee su evidencia. Luego usa **Comprobación de estado** (flujo *Detectar y recuperar*). Usa **Recuperar** solo si la comprobación muestra un problema de configuración o de sesión. |
| Pastilla **OpenClaw ⚠** o `no challenge arrived within 30s. Open the launchable, then retry with a fresh matching access session` | Tu cookie de sesión expiró o es de otro launchable. | Abre el launchable, inicia sesión, copia el **Value** nuevo de la cookie correcta y vuelve a **Probar conexión**. |
| `The launchable needs a fresh <cookie> browser session.` | Pegaste el encabezado completo, otra cookie o nada. | Copia solo el **Value** de la cookie que corresponde a tu dominio (tabla del paso 11). |
| `You have run out of credits ...` aunque sí tienes créditos | Tienes activa otra organización de Brev. | `brev ls orgs` y luego `brev set <org>`. En la consola, cambia de organización. |
| `ssh: Could not resolve hostname <instancia>` aunque corriste `brev refresh` | La línea `Include` de Brev quedó dentro de un bloque `Host` de tu `~/.ssh/config`. | Respalda `~/.ssh/config` y mueve la línea `Include … .brev/ssh_config` hasta arriba, antes del primer `Host`. Receta 12 del cookbook. |
| `brev shell <instancia> --host` se queda esperando | Problema conocido de la ruta `--host` con este launchable. | Usa `brev shell <instancia>` sin `--host`. |
| Tarjeta roja con **RETRY** o progreso en 0 % durante la configuración | Error visual de la interfaz del launchable. | Mira el registro de actividad. Si avanza, no hagas nada. No hagas clic en **RETRY**: reconstruye el sandbox. |
| El chat se queda sin respuesta y agota el tiempo; nunca aparece `exec` | `toolSearch` activado: el modelo da vueltas con `tool_search_code`. | **Comprobación de estado** lee el valor real. Si dice `toolSearch activado`, **Recuperar** lo apaga con `config.patch`. |
| `brev start` falla después de una pausa | El proveedor no tiene capacidad para ese tipo de instancia. | Espera y reintenta. Si urge, elimina y despliega de nuevo (pierdes los datos que no respaldaste). |
| Un tutorial te dice que uses `nemoclaw deploy` | Ese comando se eliminó en NemoClaw v0.0.117. | No lo uses. En este curso desplegamos con el launchable de Brev. |

## Reto

**Pausa y vuelve en menos de 10 minutos.** Detén tu instancia, reanúdala y deja todo en verde otra vez.

Criterio de éxito: `brev ls` mostró `STOPPED` y luego `RUNNING`, `nemoclaw my-assistant status` reporta la inferencia `healthy` y **Probar conexión** vuelve a mostrar `Conexión lista`. Anota cuánto tardó cada paso y qué tuviste que repetir (pista: la cookie).

## Avance del proyecto

Tu agente **Soporte NemoClaw** ya tiene casa. Antes de enseñarle nada, mide cómo responde "de fábrica":

1. En el turno por el gateway (paso 14), envía esta duda de estudiante:
   ```js
   message = "Un estudiante dice: 'Mi notebook responde HTTP 401 cuando llamo al modelo'. ¿Qué le respondes? Responde en español y en 5 líneas como máximo.";
   ```
2. Guarda la respuesta en tu repo como `proyecto/linea-base-4.1.md`, junto con el nombre de tu instancia, el nombre del sandbox y el costo por hora que viste en Brev.

En la clase 4.3 instalarás la skill `soporte-nemoclaw` con la FAQ del curso y compararás contra esta línea base.

## Recursos

- [Lección 03a · Conecta NemoClaw (NVIDIA DLI, español)](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/03a-kickstart.html)
- [Launchable de NemoClaw en Brev](https://brev.nvidia.com/launchable/deploy/now?launchableID=env-3Azt0aYgVNFEuz7opyx3gscmowS&ncid=ref-dli-759990)
- [Brev · Quickstart](https://docs.nvidia.com/brev/latest/getting-started/quickstart.md) y [CLI: conectividad](https://docs.nvidia.com/brev/latest/cli/connectivity.md)
- [Brev · Instancias: estados y cobro](https://docs.nvidia.com/brev/latest/concepts/gpu-instances.md) y [Precios de launchables](https://www.nvidia.com/en-us/launchables/pricing)
- [NemoClaw · Desplegar en un servidor headless (incluye Brev)](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/deployment/deploy-to-headless-server.md)
- [NemoClaw · Troubleshooting](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/troubleshooting.md)
- Issues de referencia: [NemoClaw #13090](https://github.com/NVIDIA/NemoClaw/issues/13090) (hostname), [#11534](https://github.com/NVIDIA/NemoClaw/issues/11534) (`--host`), [#11535](https://github.com/NVIDIA/NemoClaw/issues/11535) (503), [#11536](https://github.com/NVIDIA/NemoClaw/issues/11536) (RETRY), [brev-cli #390](https://github.com/brevdev/brev-cli/issues/390) (organización)
