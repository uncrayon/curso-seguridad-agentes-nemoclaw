# API key de NVIDIA Build

## P: ¿Dónde consigo mi API key de NVIDIA para el curso?
Entra a https://build.nvidia.com e inicia sesión o crea tu cuenta.
Abre tu perfil, ve a **API Keys** y pulsa **Generate API Key**.
Copia la key completa: empieza con `nvapi-`.
Guárdala en un gestor de contraseñas y nunca la pegues en el código.

## P: No me llega el SMS de verificación al crear la key, ¿qué hago?
La verificación de teléfono de build.nvidia.com falla con algunos números fuera de EE. UU. o cuando pides el código muchas veces.
No es un problema de NemoClaw ni del curso.
Espera unos minutos y reintenta una sola vez; si sigue fallando, escribe a help@build.nvidia.com con tu correo, los números que probaste y capturas.
Mientras tanto, los notebooks del curso corren en modo MOCK sin key.

## P: ¿Dónde guardo mi key y con qué nombre de variable?
Es la misma key `nvapi-` en todo el curso.
En Colab, guárdala en Secrets (icono de llave) como `NVIDIA_API_KEY` y activa el acceso del notebook.
En tu máquina, ponla en el archivo `.env` de la raíz del repo como `NVIDIA_API_KEY` (ese archivo ya está en `.gitignore`).
Para NemoClaw instalado en tu máquina, usa la variable `NVIDIA_INFERENCE_API_KEY`.

## P: ¿Cómo pruebo rápido si mi key funciona?
Exporta la key con `export NVIDIA_API_KEY=nvapi-xxxxxxxx` y haz una llamada con curl a `https://integrate.api.nvidia.com/v1/chat/completions` con el encabezado `Authorization: Bearer $NVIDIA_API_KEY`, el modelo `nvidia/nemotron-3.5-lightning-30b-a3b` y `max_tokens` de 1024.
Si responde un JSON con `choices`, la key sirve.
Si ves 401 o 403, revisa que la key esté completa y sin espacios.

## P: ¿Cuántos créditos o solicitudes por minuto tengo gratis?
NVIDIA Build limita el uso por cuenta, pero los números cambian y no están documentados en las fuentes del curso.
Revisa tu uso en tu cuenta de build.nvidia.com.
Para no gastarlos, pon un límite de pasos a tus loops de agente y no ejecutes celdas en ráfaga. [VERIFICAR EN LAB]
