# OpenClaw: gateway, dashboard, pairing, workspace y sesiones

## P: ¿Cómo abro el dashboard de OpenClaw?
En el laboratorio, abre el tablero con el botón verde NemoClaw de tu instancia en Brev y pulsa CHAT WITH AGENT: el chat de OpenClaw se abre en otra pestaña, listo para usar.
En una instalación propia, el dashboard escucha en `http://127.0.0.1:18789/`; obtén la URL con token con `nemoclaw <sandbox> dashboard-url --quiet` y ábrela en el navegador.
La URL con `#token=` es una contraseña.

## P: El navegador dice ERR_CONNECTION_REFUSED en localhost:18789
En el laboratorio no uses localhost: entra al chat con el botón CHAT WITH AGENT del tablero.
En una instalación propia, el port forward del dashboard se cayó o no abriste el túnel.
Revisa los forwards con `openshell forward list` y restáuralos con `nemoclaw <sandbox> recover`.

## P: El dashboard dice "Pairing required", ¿cómo lo resuelvo?
En el laboratorio, el chat que abre CHAT WITH AGENT ya viene emparejado: no necesitas hacer nada.
En una instalación propia, OpenClaw exige emparejar cada navegador o CLI con el gateway, y desde OpenClaw 2026.9.1 no se puede desactivar.
Espera unos minutos y recarga, o usa Overview, Gateway Access, Connect.
Desde la terminal: `nemoclaw <sandbox> connect`, luego `openclaw devices list --json` y `openclaw devices approve <requestId>`, aprobando solo el requestId que corresponde.

## P: ¿Dónde están los archivos del workspace del agente?
Dentro del sandbox, en `/sandbox/.openclaw/workspace/`.
Al principio ahí están `AGENTS.md` (instrucciones), `SOUL.md` (personalidad), `IDENTITY.md`, `POLICY.md`, `TOOLS.md`, `USER.md` y `HEARTBEAT.md`.
Con el uso aparecen `MEMORY.md` (memoria de largo plazo), la carpeta `memory/` con notas diarias y `skills/<nombre>/SKILL.md` cuando instalas una skill.
Para verlos en el laboratorio, abre VM TERMINAL y ejecuta `nemoclaw my-assistant exec -- ls -la /sandbox/.openclaw/workspace`.

## P: El agente olvidó lo que le dije, ¿por qué?
El historial vive en la sesión, identificada por su clave (`sessionKey`).
Si abres una sesión nueva o la reinicias, el historial no está; lo que sobrevive entre sesiones es lo que el agente escribe en `MEMORY.md` o en `memory/`.
Lista las sesiones con `nemoclaw <sandbox> sessions list --json` (la tabla sin `--json` es muy ancha) y reinicia una con `nemoclaw <sandbox> sessions reset <clave>`, por ejemplo `nemoclaw my-assistant sessions reset memo-41`.

## P: Me sale EACCES permission denied al cambiar openclaw.json
Desde NemoClaw v0.0.130, OpenClaw es dueño de `/sandbox/.openclaw/openclaw.json`, pero se cambia con sus comandos.
Entra al sandbox (en el laboratorio, con SANDBOX TERMINAL; en tu máquina, con `nemoclaw <sandbox> connect`) y usa `openclaw config set <clave> <valor>` o `openclaw config unset <clave>`.
Si tu versión es más vieja, actualiza NemoClaw.
No guardes keys en ese archivo: el agente puede leerlo.

## P: ¿Cómo instalo una skill y por qué el agente no la usa?
Una skill es una carpeta con un `SKILL.md` que tiene frontmatter YAML con el campo `name`.
Instálala con `nemoclaw <sandbox> skill install ./mi-skill/` y revísala con `nemoclaw <sandbox> skill list`.
En el laboratorio, desde VM TERMINAL: `nemoclaw my-assistant skill install ~/curso/clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/`; debe decir `Validated SKILL.md`.
Que esté instalada no garantiza que el agente la elija solo: pruébala en una sesión nueva mencionándola o dando la ruta de su `SKILL.md`.
