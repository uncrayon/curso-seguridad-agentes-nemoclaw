# 5.2 · Identidades y límites con OpenShell

Comprueba con evidencia quién es tu agente dentro del sandbox, qué binarios pueden salir a la red y dónde está (y dónde no) tu API key.

| | |
|---|---|
| Duración del video | ≈9 min |
| Práctica | Laboratorio en Brev ([`cookbook.md`](cookbook.md)) |
| Habilidad | Configurar identidades de agente en OpenShell |

Material: [diapositivas](slides.html) · [cookbook del lab](cookbook.md) · [FAQ del curso](../../FAQ.md)

## Lo esencial (sin tecnicismos)

**La idea:** Dentro del sandbox, el agente trabaja como un usuario sin poderes de administrador, y cada programa tiene sus propios permisos para salir a internet: no basta con decir "soy el agente". Tu API key nunca entra al sandbox; adentro solo hay un vale sin valor. Así, aunque alguien engañe al agente, lo que puede lograr es poco.

**Piénsalo como:** darle al asistente la llave de su oficina, no la llave maestra del edificio.

**Palabras nuevas:** [mínimo privilegio](../../GLOSARIO.md), [Landlock, seccomp y aislamiento de red](../../GLOSARIO.md) (los candados del cuarto).

**Hazlo sin programar (≈10 min):** Con tu instancia encendida, abre la [lección 04a de NVIDIA](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/04a-safety.html) y presiona ▶ en **🩺 Health check**, en **Pregunta cualquier cosa al entorno, en código** y en **Lee la política activa del launchable**. En el mapa, cambia el programa que llama de `curl` a `openclaw`. Anota tres cosas: qué usuario es el agente, qué mensajes salen cuando intenta pedir más poder y qué destinos cambian según el programa.

**Qué te llevas:** Puedes comprobar por ti mismo, sin creerle al agente, qué tan poco poder tiene y que tu key no está a su alcance.

**Tu crédito:** esta práctica usa ≈20 min de instancia encendida `[VERIFICAR EN LAB]`. Al terminar, detén la instancia (ver [LABORATORIO.md](../../LABORATORIO.md)).

## Lo que vas a lograr

- Demostrar que el agente corre como el usuario `sandbox`, sin root, con seccomp activo y sin poder escalar.
- Explicar por qué OpenShell da permisos de red **por binario** (ruta real + hash) y por qué falsificar `argv[0]` no sirve.
- Mostrar que la API key real nunca entra al sandbox: adentro solo hay un placeholder.

## Antes de empezar

- Tu laboratorio NemoClaw en Brev está encendido y la verificación de la clase 4.1 está en verde.
- Sabes entrar al host con `brev shell <tu-instancia>` (clase 4.1).
- Tu sandbox se llama `my-assistant` (o anotaste el nombre que muestra `openshell sandbox list`).
- Hiciste tu hoja `trifecta.md` en la clase 5.1.

## Paso a paso

### 1. Tres identidades distintas

Antes de teclear, ten claro de quién hablamos:

| Identidad | Quién es | Qué poder tiene |
|---|---|---|
| **El proceso del agente** | El usuario `sandbox` dentro del contenedor | Lo que permitan Landlock, seccomp y la política de red |
| **El binario** | La ruta real del ejecutable que abre la conexión (`/usr/local/bin/openclaw`, `/usr/bin/curl`) | Los destinos que su grupo de la política le permita |
| **El operador** | Tú, en la terminal del host, con `nemoclaw` y `openshell` | Cambiar políticas, aprobar egress, leer el token del gateway |

### 2. ¿Quién es el agente?

En el host del lab:

```bash
openshell sandbox exec -n my-assistant -- whoami
openshell sandbox exec -n my-assistant -- id
openshell sandbox exec -n my-assistant -- pwd
```

Deberías ver `sandbox`, un `uid` distinto de 0 y `/sandbox`. Después pregúntale al agente lo mismo:

```bash
nemoclaw my-assistant agent -m "Usa tu herramienta exec para ejecutar whoami y pwd, y dime en una frase qué usuario eres y dónde estás."
```

Compara su respuesta con lo que viste tú. Como operador, **verificas** lo que el agente dice.

### 3. Lee su autoridad en `/proc/self/status`

```bash
openshell sandbox exec -n my-assistant -- grep -E '^(Uid|Gid|NoNewPrivs|Seccomp|Seccomp_filters|CapEff|CapBnd)' /proc/self/status
```

Deberías ver `NoNewPrivs: 1`, `Seccomp: 2` y `CapEff: 0000000000000000`: sin privilegios nuevos, con filtro seccomp y sin capacidades de root. Es una prueba segura: solo lee un archivo.

### 4. Intenta escalar (y lee bien el error)

Corre las pruebas de NVIDIA de la [receta 3](cookbook.md#3--pedir-más-autoridad-catálogo-de-nvidia-04a) y las de seccomp de la [receta 4](cookbook.md#4--seccomp-ptrace-mount-y-setuid-sin-romper-nada):

```bash
openshell sandbox exec -n my-assistant -- sudo id
openshell sandbox exec -n my-assistant -- python3 -c 'import os; os.setuid(0)'
```

Deberías ver fallas. Distingue el mensaje:
- `command not found`: la herramienta no existe en la imagen. No prueba ningún límite.
- `Permission denied` (`EACCES`): permisos de archivo o Landlock.
- `Operation not permitted` (`EPERM`): el kernel negó la operación (falta de capacidades o seccomp).

Un fallo por sí solo no identifica el mecanismo. Por eso el paso 3 lee el estado del proceso.

### 5. El permiso de red va atado al binario

En la política base, `docs.openclaw.ai` solo se permite para `/usr/local/bin/openclaw`. Pruébalo con `curl` y luego intenta engañar a OpenShell:

```bash
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://docs.openclaw.ai
openshell sandbox exec -n my-assistant -- bash -c 'exec -a /usr/local/bin/openclaw curl -sS -m 8 -o /dev/null -w "code=%{http_code}\n" https://docs.openclaw.ai'
```

Deberías ver dos veces `curl: (56) CONNECT tunnel failed, response 403`. OpenShell identifica al binario por `/proc/<pid>/exe` (la ruta que el kernel garantiza), recorre los procesos padre y guarda un hash SHA256 de cada binario la primera vez que lo ve (*trust-on-first-use*). `argv[0]` se puede falsificar; por eso no cuenta. Las variantes "copiar curl como openclaw" y "reemplazar el binario" están en la [receta 5](cookbook.md#5--permisos-por-binario-el-host-está-permitido-el-binario-no).

Luego pídeselo al agente, que sí usa el binario permitido:

```bash
nemoclaw my-assistant agent -m "Abre https://docs.openclaw.ai y dime en una línea de qué trata la página."
```

### 6. Busca tu API key dentro del sandbox

```bash
openshell sandbox exec -n my-assistant -- sh -c 'env | grep -iE "key|token" | sed -E "s/=(openshell:resolve:env:).*/=\1…/; t; s/=.*/=<oculto>/"'
openshell sandbox exec -n my-assistant -- sh -c 'grep -rIl "nvapi-" /sandbox 2>/dev/null | wc -l'
```

Deberías ver algo como `NVIDIA_INFERENCE_API_KEY=openshell:resolve:env:…` y un `0`. La key real vive en el gateway de OpenShell, en el host. El proxy L7 cambia el placeholder por la key **solo** cuando la petición sale por la ruta permitida. Si el agente imprime esa variable o la manda a otro lado, lo que filtra es un texto sin valor.

En el host, mira dónde está la key de verdad (los valores nunca se muestran):

```bash
nemoclaw credentials list
```

### 7. Lo mismo, desde la página 04a de NVIDIA

Si prefieres el navegador, abre la [lección 04a](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/04a-safety.html) con tu launchable conectado y sigue la [receta 7](cookbook.md#7--en-la-página-04a-de-nvidia): agrega `["¿Quién soy?", ["whoami", "id", "pwd"]]` a la celda "Pregunta cualquier cosa al entorno, en código" y cambia el binario en el mapa de la política.

## Comprueba que funcionó

- [ ] `whoami` dice `sandbox` y `id` muestra un `uid` distinto de 0.
- [ ] `/proc/self/status` muestra `NoNewPrivs: 1` y `Seccomp: 2`.
- [ ] `sudo id` y `os.setuid(0)` fallan, y sabes qué significa cada mensaje.
- [ ] `curl` a `docs.openclaw.ai` da 403 aunque falsifiques `argv[0]`.
- [ ] Dentro del sandbox no hay ninguna `nvapi-`: solo un placeholder `openshell:resolve:env:…`.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `curl: (56) CONNECT tunnel failed, response 403` | La política negó la conexión (host o binario no permitidos). Es lo esperado en el paso 5 | No es un problema de TLS. Revisa `nemoclaw my-assistant logs --tail 30` para ver binario y motivo |
| `nemoclaw: recent network policy denial detected for docs.openclaw.ai:443 …` | Pista informativa de `nemoclaw … exec` tras una denegación | Léela y sigue. Se silencia con `NEMOCLAW_NO_POLICY_HINT=1` |
| `whoami` dice `root` | Usaste `docker exec` sobre el contenedor (corre como root, `HOME=/root`) | Usa `openshell sandbox exec -n …` o `nemoclaw my-assistant exec -- …` |
| Un comando con tubería (`grep … \| wc`) se ejecuta en el host | `openshell sandbox exec` recibe argumentos, no una línea de shell | Envuelve el comando completo en `-- sh -c '…'` |
| No aparece ninguna variable `…KEY` en el paso 6 | Sandbox creado antes de NemoClaw v0.0.132: usa la ruta `inference.local` y no recibe ni el placeholder | Es normal. La key tampoco está adentro |
| La página 04a dice "Mantén el launchable abierto en otra pestaña, vuelve a ejecutar y comprueba el nombre con: openshell sandbox list" | La página perdió la sesión con tu launchable | Reabre el launchable, reconéctate en 03a y ejecuta 🩺 Health check |
| `python3: command not found` | La imagen cambió | Usa la celda de la página 04a o salta la receta 4 |

## Reto

Encuentra **un host que tu política permita para `curl`** y otro que solo permita para `openclaw`, usando solo comandos de lectura (`openshell policy get my-assistant --full` te ayuda; lo verás a fondo en la 5.3). Criterio de éxito: dos comandos `curl` desde el sandbox, uno con `code=200` (o el código del servidor) y otro con `CONNECT tunnel failed, response 403`, y una frase que explique la diferencia.

## Avance del proyecto

Agrega a tu `trifecta.md` de *Soporte NemoClaw* una sección **"Identidad"** con lo que comprobaste:

```markdown
## Identidad (clase 5.2)
- Corre como: sandbox (uid …), NoNewPrivs 1, Seccomp 2
- Binarios que salen a la red: /usr/local/bin/openclaw, /usr/local/bin/node
- Dónde vive la API key: gateway de OpenShell (host). En el sandbox: openshell:resolve:env:…
- Riesgo que queda: el token del gateway de OpenClaw sí es legible dentro del sandbox
```

En la clase 5.3 vas a leer la política completa y a escribir el preset del proyecto.

## Recursos

- NVIDIA DLI · [04a · El sandbox de OpenShell](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/04a-safety.html) (Apache-2.0).
- NemoClaw · [Security Best Practices](https://docs.nvidia.com/nemoclaw/latest/) → "Binary-Scoped Endpoint Rules" (identificación por `/proc/<pid>/exe` y hash SHA256).
- NemoClaw · Credential Storage (`docs/security/credential-storage.mdx`): placeholders `openshell:resolve:env:<KEY>`.
- NemoClaw · Process Controls (`docs/security/process-controls.mdx`): `no-new-privileges`, capacidades, `ulimit -u 512`.
- Kernel de Linux · [seccomp filter](https://docs.kernel.org/userspace-api/seccomp_filter.html) · man7 · [capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html).
- [FAQ del curso](../../FAQ.md).

---
Basado en la lección 04a-safety del curso de NVIDIA DLI (Apache-2.0).
