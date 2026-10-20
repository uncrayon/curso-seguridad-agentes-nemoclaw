# OpenClaw: gateway, dashboard, pairing, workspace y sesiones

## P: ¿Cómo abro el dashboard de OpenClaw?
El dashboard escucha en `http://127.0.0.1:18789/`.
Obtén la URL con token con `nemoclaw <sandbox> dashboard-url --quiet` y ábrela en el navegador.
Si el sandbox está en Brev o en un servidor remoto, abre antes un túnel desde tu computadora con `brev port-forward <instancia> -p 18789:18789` o `ssh -N -L 18789:127.0.0.1:18789 <instancia>`.
La URL con `#token=` es una contraseña.

## P: El navegador dice ERR_CONNECTION_REFUSED en localhost:18789
El port forward del dashboard se cayó o no abriste el túnel.
Revisa los forwards con `openshell forward list` y restáuralos con `nemoclaw <sandbox> recover`.
Si estás en Brev, confirma que tu `brev port-forward` o `ssh -L` siga activo.

## P: El dashboard dice "Pairing required", ¿cómo lo resuelvo?
OpenClaw exige emparejar cada navegador o CLI con el gateway, y desde OpenClaw 2026.9.1 no se puede desactivar.
Espera unos minutos y recarga, o usa Overview, Gateway Access, Connect.
Desde la terminal: `nemoclaw <sandbox> connect`, luego `openclaw devices list --json` y `openclaw devices approve <requestId>`, aprobando solo el requestId que corresponde.

## P: ¿Dónde están los archivos del workspace del agente?
Dentro del sandbox, en `/sandbox/.openclaw/workspace/`.
Ahí están `SOUL.md` (personalidad), `AGENTS.md` (instrucciones), `TOOLS.md`, `USER.md`, `HEARTBEAT.md`, `MEMORY.md` (memoria de largo plazo), la carpeta `memory/` con notas diarias y `skills/<nombre>/SKILL.md`.
Para verlos: `nemoclaw <sandbox> connect` y `ls -la /sandbox/.openclaw/workspace`.

## P: El agente olvidó lo que le dije, ¿por qué?
El historial vive en la sesión, identificada por su clave (`sessionKey`).
Si abres una sesión nueva o la reinicias, el historial no está; lo que sobrevive entre sesiones es lo que el agente escribe en `MEMORY.md` o en `memory/`.
Lista las sesiones con `nemoclaw <sandbox> sessions list` y reinicia una con `nemoclaw <sandbox> sessions reset main`.

## P: Me sale EACCES permission denied al cambiar openclaw.json
Desde NemoClaw v0.0.130, OpenClaw es dueño de `/sandbox/.openclaw/openclaw.json`, pero se cambia con sus comandos.
Entra con `nemoclaw <sandbox> connect` y usa `openclaw config set <clave> <valor>` o `openclaw config unset <clave>`.
Si tu versión es más vieja, actualiza NemoClaw.
No guardes keys en ese archivo: el agente puede leerlo.

## P: ¿Cómo instalo una skill y por qué el agente no la usa?
Una skill es una carpeta con un `SKILL.md` que tiene frontmatter YAML con el campo `name`.
Instálala con `nemoclaw <sandbox> skill install ./mi-skill/` y revísala con `nemoclaw <sandbox> skill list`.
Que esté instalada no garantiza que el agente la elija solo: pruébala en una sesión nueva mencionándola o dando la ruta de su `SKILL.md`.
