# Conexión del curso de NVIDIA con el laboratorio

## P: ¿Qué URL pongo en el campo Base URL para conectar el laboratorio?
La URL de la app NemoClaw de tu launchable, solo el origen y sin `/v1`.
Tiene la forma `https://nemoclaw-<id>.brevlab.com`, `https://nemoclaw-<id>.apps.run.brev.nvidia.com` o `https://nemoclaw-<id>.gobrev.dev`.
No la pongas en el campo de la ruta del modelo: esa debe seguir en `https://integrate.api.nvidia.com/v1`.

## P: ¿Qué es la "Access session" y de dónde saco la cookie?
Es el valor de la cookie de inicio de sesión de tu launchable.
Abre el launchable en el mismo navegador e inicia sesión.
En DevTools ve a Application, Storage, Cookies, y copia solo el Value completo de la cookie que corresponde: `CF_Authorization` para `brevlab.com`, `_pomerium` para `apps.run.brev.nvidia.com` o `__Host-skybridge-brev-prd` para `gobrev.dev`.
Es una credencial: no la compartas.

## P: ¿Qué revisa cada una de las cuatro rutas del Test connection?
Primero `GET /api/agent`, que confirma tu sesión y obtiene el token del gateway.
Después el WebSocket `/cli/gateway`, que confirma que el gateway acepta el token.
Luego el WebSocket `/ws/terminal`, que abre una terminal en la VM.
Por último `GET /healthz`, la salud general.
Si una falla, abre su evidencia para ver la solicitud y la respuesta.

## P: Me sale "OpenClaw is starting. Retrying in N seconds", ¿hago algo?
No.
El launchable responde, pero OpenClaw todavía está arrancando (503 con `status: starting`).
El curso reintenta solo hasta 30 minutos.
Si pasan más de 15, revisa en Brev que la instancia esté RUNNING.

## P: Me sale "session expired or unreachable" o "no challenge arrived within 30s"
Tu cookie de acceso venció o el launchable se detuvo.
Confirma en Brev que la instancia está RUNNING, abre el launchable e inicia sesión otra vez, copia un valor nuevo de la cookie y pégalo en Access session.
Lo mismo aplica si ves "Expected JSON but received an HTML page" o "The launchable needs a fresh browser session".

## P: La comprobación de conexión da timeout o 502, ¿qué hago?
Un timeout o un 502 solos no dicen la causa.
Abre la ruta que falló, ejecuta la celda Health check y, si marca DEGRADED, la celda Recover.
Si no basta, activa `DO_RESTART = true`, espera unos 40 segundos y vuelve a conectar.
Si sigue fallando, relanza el launchable desde Brev.
