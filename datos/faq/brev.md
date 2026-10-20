# Brev y el launchable de NemoClaw

## P: ¿Cuánto me cuesta el laboratorio en Brev?
El launchable de NemoClaw usa una instancia solo CPU de 4 CPU y 16 GiB.
Encendida cuesta unos USD 0.25 por hora (0.20 de cómputo y 0.05 de disco); la página de la instancia muestra un precio parecido, por ejemplo $0.26/hr.
Con el cupón de 1 USD te alcanza para unas 4 horas encendida.
Las llamadas al modelo no gastan crédito de Brev: gastan los créditos de tu cuenta de build.nvidia.com.
El plan del curso: ve primero los videos de los Módulos 4 a 6, haz todas las prácticas en una sola sesión de 2.5 a 3 horas y borra la instancia al terminar.

## P: ¿Me cobran si detengo la instancia? ¿Y si la borro?
Encendida (Running), Brev cobra cómputo y disco: unos USD 0.25 por hora.
Detenida (Stopped), no cobra cómputo, pero el disco sigue cobrando unos USD 0.05 por hora, unos USD 1.20 al día: más que tu cupón en un solo día.
Borrada (Deleted), no cobra nada, pero los datos se pierden para siempre.
Si tienes que pausar, pulsa Stop y vuelve el mismo día o al siguiente; nunca la dejes detenida varios días.
Al terminar el laboratorio (después de la clase 6.1), pulsa Delete.

## P: ¿Cómo detengo o borro mi instancia de Brev?
En la consola de brev.nvidia.com entra a Compute y abre tu instancia (se llama algo como nemoclaw-xxxxxx).
Pulsa Stop para detenerla o Delete para borrarla, y confirma que el estado cambie.
En este curso no necesitas la CLI de Brev: todo se hace desde el navegador.

## P: ¿Cómo canjeo mi cupón y dónde veo mi saldo?
En la consola de brev.nvidia.com entra a Billing, luego a Credits, y pulsa Redeem Code.
Escribe el código del cupón y confirma.
Tu saldo aparece en la barra superior de la consola.

## P: ¿Qué pasa si se me acaban los créditos de Brev?
Brev te avisa por correo, pausa las instancias que se pueden detener y borra las que no.
Si a las 24 horas sigues sin saldo, borra todos los recursos y los datos no se recuperan.
Para canjear un código, ve a Billing, Credits y pulsa Redeem Code.

## P: Brev dice "You have run out of credits" pero sí tengo créditos, ¿por qué?
Tienes activa otra organización; los créditos son por organización.
En la consola, cambia de organización con el selector de arriba a la derecha y revisa el saldo de la barra superior.
Despliega el laboratorio en la organización donde canjeaste el cupón.

## P: Mi instancia se queda en Deploying o Waiting, ¿qué hago?
Normalmente la instancia pasa a Running en un par de minutos, y crear el agente (la pantalla Building your agent) tarda unos 3 minutos más.
Revisa la pestaña Logs de tu instancia en Compute.
Si sigue atascada después de 15 minutos, bórrala con Delete, espera 30 segundos y créala de nuevo desde el enlace del launchable.
Antes de reintentar, confirma en Compute que no quedó una instancia duplicada cobrando.
Si persiste, escribe a brev-support@nvidia.com.

## P: La página del launchable se queda en 0 % o muestra un RETRY rojo, ¿lo pulso?
No mientras los pasos sigan avanzando: reintentar reconstruye todo el sandbox.
No refresques la pestaña durante Building your agent y espera hasta ver YOUR AGENT IS LIVE.
Los pasos son Preflight checks, OpenShell gateway, Configure inference, Set inference route y Create sandbox.
Si un paso se queda detenido más de 15 minutos o ves `503 no_healthy_upstream` por más de unos minutos, recarga una vez; si no se arregla, borra la instancia y despliega una nueva.

## P: Me sale "ssh: Could not resolve hostname" o la instancia no aparece en la CLI
En este curso no necesitas SSH ni la CLI de Brev: abre tu instancia, pulsa el botón verde NemoClaw y usa VM TERMINAL en el tablero.
Si de todos modos usas la CLI en tu computadora, ejecuta `brev ls` y `brev refresh`, que sincroniza la lista y reescribe `~/.brev/ssh_config`.
Si SSH dice `Permission denied (publickey)`, vuelve a entrar con `brev logout && brev login`.

## P: Detuve y volví a encender la instancia y el agente no responde
Tras reiniciar la máquina, los servicios pueden tardar unos minutos en arrancar.
Abre el tablero con el botón verde NemoClaw y mira el panel de logs: cuando todo está bien, los servicios aparecen como 7/7 OK.
Si no responde, abre VM TERMINAL y ejecuta `nemoclaw my-assistant status`; debe decir Inference healthy y Phase Ready.
Si el sandbox quedó detenido, ejecuta `nemoclaw my-assistant start`; si el gateway no responde, `nemoclaw my-assistant recover`.
