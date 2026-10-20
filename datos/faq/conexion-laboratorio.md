# Conexión con el laboratorio: el tablero de NemoClaw

## P: ¿Cómo entro a mi laboratorio?
En brev.nvidia.com entra a Compute y abre tu instancia: debe decir Running.
Pulsa el botón verde NemoClaw; se abre una pestaña nueva con una dirección como `https://nemoclaw-<id>.gobrev.dev`.
Inicia sesión con tu cuenta de NVIDIA, la misma de build.nvidia.com.
La primera vez eliges SET UP IN THIS BROWSER y pulsas OPEN BROWSER SETUP para crear tu agente; después llegas directo al tablero.

## P: ¿Qué URL pongo en el campo Base URL para conectar el laboratorio?
En este curso no conectas el laboratorio a ninguna otra página: no hay campo Base URL que llenar.
Tu laboratorio vive en la dirección que abre el botón verde NemoClaw, con la forma `https://nemoclaw-<id>.gobrev.dev`.
Si un notebook te pide la ruta del modelo, esa sigue siendo `https://integrate.api.nvidia.com/v1`.

## P: ¿Qué es la "Access session" y de dónde saco la cookie?
En este curso no necesitas copiar ninguna cookie: entras al laboratorio con el botón verde NemoClaw e inicias sesión con tu cuenta de NVIDIA.
La casilla Access session es de las lecciones interactivas del curso web de NVIDIA DLI, que este curso ya no usa.
Si alguna vez copias una cookie de sesión, trátala como una contraseña: no la compartas.

## P: ¿Cómo abro la terminal del laboratorio y para qué sirve cada botón del tablero?
En el tablero, la tarjeta de tu agente (MY-ASSISTANT) tiene cuatro botones.
CHAT WITH AGENT abre el chat de OpenClaw en otra pestaña, con el menú Home, Dashboards, Automations, Plugins y Sessions.
VM TERMINAL abre la terminal de operador: la máquina, con el usuario `ubuntu`, donde copias y pegas los comandos del curso.
SANDBOX TERMINAL abre una terminal dentro del sandbox, donde vive el agente, con el usuario `sandbox`.
OPENSHELL TUI abre el monitor de OpenShell: ahí ves las políticas y apruebas o rechazas conexiones pendientes.
Haz clic dentro del área negra antes de escribir; Shift+Escape cierra la terminal.

## P: ¿Cómo llevo los archivos del curso al laboratorio?
Abre VM TERMINAL y clona el repo del curso con `git clone --depth 1 https://github.com/uncrayon/curso-seguridad-agentes-nemoclaw ~/curso`.
Los archivos quedan en `~/curso/`, por ejemplo la FAQ en `~/curso/datos/faq/` y la skill en `~/curso/clases/4.3-agentes-siempre-activos/skills/soporte-nemoclaw/`.
Para pasar una carpeta al workspace del agente usa `nemoclaw my-assistant upload ~/curso/datos/faq/ /sandbox/.openclaw/workspace/`.
Cada comando `nemoclaw` imprime un aviso `ExperimentalWarning: SQLite is an experimental feature`: ignóralo.

## P: Me sale "OpenClaw is starting. Retrying in N seconds", ¿hago algo?
No.
Si el chat o el tablero dicen que el agente está arrancando, espera unos minutos sin recargar.
En el panel de logs del tablero puedes ver cuándo los servicios quedan en 7/7 OK.
Si pasan más de 15 minutos, revisa en Brev que la instancia esté Running.

## P: Me sale "session expired or unreachable" o "no challenge arrived within 30s"
Esos mensajes eran de las lecciones del curso web de NVIDIA, que este curso ya no usa.
Si la página del laboratorio te pide iniciar sesión otra vez o deja de responder, confirma en Brev que la instancia está Running.
Vuelve a pulsar el botón verde NemoClaw e inicia sesión con tu cuenta de NVIDIA.

## P: La página del laboratorio da timeout o 502, ¿qué hago?
Un timeout o un 502 solos no dicen la causa.
Confirma en Brev que la instancia está Running, espera un minuto y recarga la página.
Si el tablero abre, pulsa VM TERMINAL y ejecuta `nemoclaw my-assistant status`: debe decir Inference healthy y Phase Ready.
Si no, ejecuta `nemoclaw my-assistant recover` y vuelve a probar.
Si sigue fallando, borra la instancia y despliega una nueva desde el enlace del launchable.
