# Errores de la API del modelo

## P: ¿Qué significa el error 401 Unauthorized?
Tu key no es válida: está incompleta, tiene espacios o comillas, o la revocaste o regeneraste.
Copia otra vez la key completa (`nvapi-…`) y confirma que tu código lee la variable correcta, por ejemplo con `echo ${NVIDIA_API_KEY:0:6}`, que debe imprimir `nvapi-`.
Reintentar o esperar más no arregla una key inválida.

## P: ¿Por qué me da 403 Forbidden si mi key es válida?
Un 403 de la API significa que tu key no tiene acceso a ese modelo o tu cuenta no tiene cuota.
Prueba con el modelo del curso, `nvidia/nemotron-3.5-lightning-30b-a3b`, y revisa tus créditos en build.nvidia.com.
Si el 403 aparece dentro del sandbox como `CONNECT tunnel failed, response 403`, no es la API: es la política de red de OpenShell.

## P: Me sale 404 Not Found al llamar al modelo, ¿qué reviso?
Revisa tres cosas: que el ID del modelo esté escrito exacto como en el catálogo, que la base URL sea `https://integrate.api.nvidia.com/v1` (con `/v1` una sola vez) y que el modelo esté disponible para tu cuenta.
Si aparece en el catálogo pero da 404, elige otro modelo.

## P: ¿Qué significa 410 Gone?
NVIDIA retiró ese modelo del endpoint gratuito; le pasó al curso de NVIDIA con `nvidia/nemotron-3-nano-30b-a3b`.
Cambia la variable `NVIDIA_MODEL` por un modelo vigente.
El de este curso es `nvidia/nemotron-3.5-lightning-30b-a3b` y el de embeddings es `nvidia/nemotron-3-embed-1b`.

## P: ¿Qué hago si recibo 429 Too Many Requests?
Mandaste demasiadas solicitudes por minuto.
Espera unos segundos y reintenta una sola vez, respetando el encabezado `Retry-After` si viene.
Pon un límite de pasos al loop del agente y agrega una pausa (`time.sleep()`) entre llamadas en pruebas masivas.

## P: El modelo devuelve 500, 502, 503 o 504, ¿es mi culpa?
Normalmente no: es una falla del proveedor o del relay, o el modelo está arrancando.
Espera 30 a 60 segundos y reintenta una vez.
Si persiste, prueba otro modelo o vuelve más tarde.

## P: La respuesta llega vacía y finish_reason es "length", ¿por qué?
El modelo del curso razona antes de responder y gasta tokens en ese razonamiento.
Si `max_tokens` es pequeño, se le acaban antes de escribir la respuesta y `content` queda vacío.
Sube `max_tokens` (los notebooks usan 4096 y el curso de NVIDIA 8196).

## P: La llamada se queda esperando hasta dar timeout, ¿qué hago?
No llegó respuesta dentro del tiempo de espera.
Revisa tu conexión y desactiva la VPN o proxy para probar.
En los notebooks el cliente espera 60 segundos: baja `max_tokens` o reintenta.
En el curso web de NVIDIA puedes subir la espera en **Request handling** hasta 300 segundos.
