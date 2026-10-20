# 1.2 · Crea tu cuenta y tu API key en NVIDIA Build

Objetivo: tener una API key `nvapi-` guardada de forma segura y una primera llamada a un modelo que responde.

| | |
|---|---|
| **Duración del video** | ≈6 min |
| **Práctica** | Guiada en el navegador y la terminal (≈20 min) |
| **Habilidad** | Administrar el consumo de API en NVIDIA Build |
| **Material** | [Diapositivas](slides.html) · [Preguntas frecuentes](../../FAQ.md) |

## Lo esencial (sin tecnicismos)

**La idea:** para que un programa hable con los modelos de NVIDIA necesitas una cuenta gratuita y una contraseña especial, la API key. Hoy la creas, la guardas en un lugar seguro y pruebas el modelo. Cada respuesta gasta un poco de tu saldo gratuito.

**Piénsalo como:** la tarjeta de acceso de un edificio: quien la tenga entra a tu nombre. Y el saldo es como el prepago del celular.

**Palabras nuevas:** [API key](../../GLOSARIO.md), [crédito](../../GLOSARIO.md), [token](../../GLOSARIO.md).

**Hazlo sin programar (≈10 min):**

1. Entra a [build.nvidia.com](https://build.nvidia.com/?ncid=ref-dli-146986), crea tu cuenta y confirma tu correo.
2. En el menú de tu cuenta, abre **API Keys**, genera una key y guárdala en tu gestor de contraseñas (o en una nota privada). Si usarás Colab, guárdala también en el panel de la llave 🔑 con el nombre `NVIDIA_API_KEY`.
3. Abre la ficha del modelo Nemotron en el catálogo y, en el cuadro de prueba de la página, escribe tres preguntas: una pregunta de cultura general, "Resume en una frase qué es un agente de IA" y la misma pregunta otra vez. Anota si las dos respuestas iguales salieron idénticas.
4. Busca en tu cuenta dónde se ve tu consumo o tu saldo.

**Qué te llevas:** tienes tu llave a los modelos guardada sin exponerla, sabes probar un modelo en el navegador y sabes qué hacer si tu key se filtra: revocarla y generar otra.

## Lo que vas a lograr

- Crear tu cuenta gratuita en build.nvidia.com y generar tu API key `nvapi-`.
- Guardar la key en tres lugares correctos (`.env`, variable de entorno y Secrets de Colab) sin que acabe en GitHub.
- Hacer tu primera llamada con `curl` a `/v1/models` y a `/v1/chat/completions`, y saber qué hacer si filtras la key.

## Antes de empezar

- Un correo electrónico al que tengas acceso y un teléfono para la verificación por SMS (lee el primer error común si estás fuera de EE. UU.).
- Una terminal: Terminal en macOS, una terminal de Linux, o en Windows **Git Bash** o **WSL**. Si solo tienes PowerShell, hay una variante abajo.
- `curl` y `python3` instalados (`curl --version` y `python3 --version`).
- Para guardar la key en `.env`: haber clonado el repo del curso.

> **Consejo:** crea tu cuenta y tu key **antes** de empezar el curso. Si la verificación por teléfono falla, la solución puede tardar unos días.

## Paso a paso

### 1. Crea tu cuenta en NVIDIA Build

1. Abre <https://build.nvidia.com/?ncid=ref-dli-146986>.
2. Haz clic en el botón para iniciar sesión y crea una cuenta de NVIDIA con tu correo (o entra con la que ya tengas).
3. Confirma tu correo con el enlace que te llega.
4. Si en algún momento te pide verificar tu teléfono (puede ser al crear la cuenta o al generar la key), escribe tu número con el código de país y luego el código del SMS.

Deberías ver: el catálogo de modelos de build.nvidia.com con tu sesión iniciada (tu avatar arriba a la derecha).

### 2. Genera tu API key

1. Abre el menú de tu cuenta y entra a la página de **API Keys**. También puedes entrar a la ficha de un modelo, por ejemplo Nemotron, y usar el botón para generar tu API key (puede decir *Generate API Key* o *Get API Key*).
2. Genera una key nueva. Si te deja ponerle nombre, usa algo como `curso-platzi-nemoclaw`. Si te deja elegir vencimiento, elige uno corto: vas a regenerarla al terminar el curso. Si no ves esas opciones, sigue con el siguiente paso.
3. Copia la key **en ese momento**. Empieza con `nvapi-` y es larga.

Deberías ver: un texto como `nvapi-xxxxxxxx…`. Trátalo como una contraseña.

> ⚠️ Nunca pegues tu key en un notebook que vas a compartir, en un mensaje de chat, en una captura de pantalla ni en un commit.

### 3. Guárdala bien (elige según dónde trabajes)

#### Opción A · Archivo `.env` (para tu máquina)

El repo trae un archivo `.env.example` en la raíz con las cuatro variables del curso:

| Variable | Para qué | Valor por defecto |
|---|---|---|
| `NVIDIA_API_KEY` | Tu key | (la tuya) |
| `NVIDIA_BASE_URL` | El endpoint | `https://integrate.api.nvidia.com/v1` |
| `NVIDIA_MODEL` | El modelo de chat | `nvidia/nemotron-3.5-lightning-30b-a3b` |
| `NVIDIA_EMBED_MODEL` | El modelo de embeddings | `nvidia/nemotron-3-embed-1b` |

```bash
# desde la raíz del repo del curso
cp .env.example .env
# abre .env con tu editor y reemplaza nvapi-xxxxxxxx… por tu key real
git check-ignore .env      # debe imprimir ".env": significa que git lo ignora
```

Deberías ver: `.env` impreso por `git check-ignore`. Si no imprime nada, **no hagas commit** y revisa que `.gitignore` tenga la línea `.env`.

#### Opción B · Variable de entorno (para la terminal)

Para no dejar la key en el historial de la terminal, léela sin mostrarla:

```bash
read -rs NVIDIA_API_KEY && export NVIDIA_API_KEY   # pega la key y presiona Enter (no se ve)
echo "${NVIDIA_API_KEY:0:6}…"                      # debe imprimir nvapi-…
```

La variable solo existe en **esa** terminal. Si abres otra pestaña, tienes que repetirlo.

#### Opción C · Secrets de Google Colab

1. En Colab, abre el panel izquierdo y haz clic en el icono de llave 🔑 (**Secrets**).
2. Agrega un secreto con el nombre exacto `NVIDIA_API_KEY` y pega tu key como valor.
3. Activa el interruptor de **acceso del notebook**.

Los notebooks del curso lo leen solos con `userdata.get("NVIDIA_API_KEY")`.

#### ¿Y en la página del curso de NVIDIA?

Ahí pegas la key en el panel de configuración de la portada. La página la guarda en `sessionStorage`: **se borra al cerrar la pestaña**. Por eso, cada vez que abres el curso en una pestaña nueva, te la vuelve a pedir. La URL y el modelo sí se recuerdan.

#### Un nombre distinto para NemoClaw

En los notebooks del curso la variable se llama `NVIDIA_API_KEY`. El instalador de NemoClaw, que usarás si lo corres en tu máquina (clase 6.3), usa otro nombre: `NVIDIA_INFERENCE_API_KEY`. Es la misma key, en otra variable.

### 4. Primera llamada: lista los modelos

`/v1/models` no gasta tokens. Es la forma más barata de comprobar que llegas al endpoint.

```bash
curl -s https://integrate.api.nvidia.com/v1/models \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  | python3 -c "import sys, json; ids = [m['id'] for m in json.load(sys.stdin)['data']]; print(len(ids), 'modelos'); print('nvidia/nemotron-3.5-lightning-30b-a3b' in ids)"
```

Deberías ver: un número de modelos y `True` (el modelo del curso está en el catálogo).

### 5. Primera llamada al modelo de chat

```bash
curl -s https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
    "messages": [{"role": "user", "content": "Saluda en una frase a un estudiante de Platzi."}],
    "max_tokens": 1024
  }' | python3 -m json.tool
```

Deberías ver un JSON con, entre otras cosas:

- `choices[0].message.content`: el saludo.
- `choices[0].finish_reason`: `"stop"` (terminó bien).
- `usage`: `prompt_tokens`, `completion_tokens` y `total_tokens`. Es lo que gastaste.

¿Por qué `max_tokens: 1024` para una frase? El modelo del curso **razona antes de responder** y ese razonamiento también gasta tokens. Con un límite muy bajo, la respuesta puede llegar vacía con `finish_reason: "length"`. Lo vas a provocar a propósito en la clase 1.3.

**Variante para PowerShell (Windows):**

```powershell
$env:NVIDIA_API_KEY = Read-Host "Pega tu key"
$body = @{ model = "nvidia/nemotron-3.5-lightning-30b-a3b"; max_tokens = 1024;
           messages = @(@{ role = "user"; content = "Saluda en una frase." }) } | ConvertTo-Json -Depth 5
Invoke-RestMethod -Uri "https://integrate.api.nvidia.com/v1/chat/completions" -Method Post `
  -Headers @{ Authorization = "Bearer $env:NVIDIA_API_KEY" } -ContentType "application/json" -Body $body
```

### 6. Cuida tus créditos y tus límites

- La cuenta gratuita de NVIDIA Build da acceso a los modelos alojados con **límites de uso**: créditos o solicitudes por minuto. Las cifras cambian con el tiempo: revisa tu consumo y tus créditos en tu cuenta de build.nvidia.com.
- Cuando superas el límite por minuto, la API responde **429**. Espera y reintenta (en la 1.3 escribes un reintento con backoff).
- Lo que más gasta: loops sin límite de pasos, ejecutar celdas en ráfaga y `max_tokens` enormes. En el Módulo 2 tu loop siempre tendrá un máximo de pasos.
- Los modelos gratuitos **cambian**. Un modelo retirado responde **410**. Le pasó al curso de NVIDIA con `nvidia/nemotron-3-nano-30b-a3b`. Por eso el modelo vive en una variable (`NVIDIA_MODEL`) y no escrito en el código.

### 7. Si filtras tu key

Si tu key apareció en un commit, en una captura, en un notebook compartido o en un chat:

1. Entra a **API Keys** en build.nvidia.com y **revoca** (elimina) esa key. El botón puede decir *Revoke*, *Delete* o mostrarse como un icono de bote de basura.
2. Genera una nueva.
3. Actualízala en todos lados: `.env`, tus variables de entorno, los Secrets de Colab y, si ya la usaste, en NemoClaw (clase 6.3).
4. Si la subiste a GitHub, borrar el archivo **no basta**: la key queda en el historial. Lo que te protege es revocarla.

## Comprueba que funcionó

- [ ] Tengo una key que empieza con `nvapi-`.
- [ ] `git check-ignore .env` imprime `.env` (o uso Colab Secrets).
- [ ] `/v1/models` devolvió una lista y `True`.
- [ ] La llamada de chat respondió con `finish_reason: "stop"` y vi el bloque `usage`.
- [ ] Sé dónde revocar mi key si la filtro.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| La verificación por teléfono falla con tu número de LATAM, o aparece "number has requested too many" | Problema conocido de verificación por SMS con números fuera de EE. UU. (issues [#201](https://github.com/NVIDIA/NemoClaw/issues/201) y #214 de NemoClaw). No es un error de NemoClaw ni tuyo | Escribe a help@build.nvidia.com con tu correo registrado, los números que probaste y capturas, o usa developer.nvidia.com/support. Hazlo con días de anticipación |
| `curl` responde **401** | La variable está vacía en esta terminal (abriste otra pestaña) o la key tiene comillas o espacios | `echo "${NVIDIA_API_KEY:0:6}"` debe imprimir `nvapi-`. Si sale vacío, vuelve a hacer el paso 3B |
| `curl` responde **404** | El ID del modelo tiene un error o la URL no termina en `/v1/...` | Copia el ID de la lista de `/v1/models`. Revisa la URL completa |
| `"content": null` o vacío y `"finish_reason": "length"` | `max_tokens` muy bajo: el modelo gastó todo razonando | Sube `max_tokens` a 1024 o más |
| La API responde **429** | Superaste el límite de solicitudes por minuto | Espera unos segundos y vuelve a intentar. No ejecutes en ráfaga |
| La página del curso de NVIDIA me pide la key otra vez | La key se guarda en `sessionStorage` y se borra al cerrar la pestaña | Es por seguridad. Vuelve a pegarla en el panel de la portada |
| En PowerShell, `curl -H ...` falla con un error de parámetros | En Windows PowerShell, `curl` es un alias de `Invoke-WebRequest` | Usa la variante con `Invoke-RestMethod`, o `curl.exe`, o Git Bash |
| `KeyError: 'data'` al listar modelos | La respuesta fue un error (por ejemplo 401) y no una lista | Quita la parte de `python3 -c` y mira el JSON del error |

## Reto

Haz que la llamada de chat responda en **menos de 15 palabras** y gaste **menos tokens de salida** que tu primera llamada, sin que llegue vacía.

**Criterio de éxito:** `finish_reason` es `"stop"`, el contenido no está vacío y `usage.completion_tokens` es menor que en tu primera llamada. Pista: cambia el prompt, no solo `max_tokens`.

## Avance del proyecto

Soporte NemoClaw ya tiene **credenciales**. Tu `.env` (o tus Secrets de Colab) con las cuatro variables es lo que leerán todos los notebooks del proyecto, de la clase 1.3 a la 6.2. Y ya tienes la primera respuesta que el agente sabrá dar: "¿qué hago si me filtraron la key?". La vas a encontrar en la FAQ del curso.

## Recursos

- [NVIDIA Build](https://build.nvidia.com/?ncid=ref-dli-146986): catálogo de modelos y tus API keys
- Página de inicio del curso de NVIDIA DLI en español, sección "Cómo introducir tu clave de API". Esta clase está basada en ella (Apache-2.0).
- [Issue #201 de NemoClaw: verificación por teléfono](https://github.com/NVIDIA/NemoClaw/issues/201)
- [Rotación de credenciales en NemoClaw](https://docs.nvidia.com/nemoclaw/latest/) (página *Credential Rotation*, para cuando uses NemoClaw local)
- [Preguntas frecuentes del curso](../../FAQ.md)

---
*Basado en la página de inicio del curso de NVIDIA DLI "Securing Agents with OpenShell and NemoClaw" (Apache-2.0).*
