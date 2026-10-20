# Brev y el launchable de NemoClaw

## P: ¿Cuánto me cuesta el laboratorio en Brev?
El launchable de NemoClaw usa una instancia solo CPU, `n2d-standard-4` (4 vCPU y 16 GiB), que en las pruebas de NVIDIA aparece como "Free".
Como referencia pública, una instancia de 4 vCPU y 16 GB cuesta unos USD 0.15 por hora, más USD 0.0001314 por GB-hora de disco.
El curso de NVIDIA anuncia un crédito de USD 1.00 para los primeros 25 000 usuarios.
Confirma el precio en la pantalla de despliegue. [VERIFICAR EN LAB]

## P: ¿Me cobran si detengo la instancia? ¿Y si la borro?
Encendida (Running), Brev cobra cómputo y disco.
Detenida (Stopped), no cobra cómputo pero sí sigue cobrando el disco, y tus datos se conservan (excepto `/tmp`).
Borrada (Deleted), no cobra nada, pero los datos se pierden para siempre.
Al terminar cada clase, detén la instancia; si no vas a volver en días, bórrala después de guardar tu trabajo en git.

## P: ¿Cómo detengo o borro mi instancia de Brev?
En la consola: brev.nvidia.com, sección GPUs, tu instancia, botón Stop o Delete.
En la CLI: `brev ls` para ver el nombre, `brev stop <instancia>` para detenerla o `brev delete <instancia>` para borrarla, y otra vez `brev ls` para confirmar.
Si `brev stop` responde `does not support stop`, esa instancia solo se puede borrar.

## P: ¿Qué pasa si se me acaban los créditos de Brev?
Brev te avisa por correo, pausa las instancias que se pueden detener y borra las que no.
Si a las 24 horas sigues sin saldo, borra todos los recursos y los datos no se recuperan.
Para canjear un código, ve a Billing, Credits, "Redeem a credit code", o usa `brev redeem <código>`.

## P: Brev dice "You have run out of credits" pero sí tengo créditos, ¿por qué?
Tienes activa otra organización; los créditos son por organización.
Lista tus organizaciones con `brev ls orgs` y activa la correcta con `brev set <org>`.
En la consola, cambia de organización en el selector superior.

## P: Mi instancia se queda en Deploying o Waiting, ¿qué hago?
El despliegue completo del launchable tarda unos 5 a 15 minutos.
Revisa `brev ls` y la pestaña Activity Logs.
Si sigue atascada, bórrala, espera 30 segundos y créala de nuevo, quizá en otra región.
Antes de reintentar, confirma con `brev ls` que no quedó una instancia duplicada cobrando.
Si persiste, escribe a brev-support@nvidia.com.

## P: La página del launchable se queda en 0 % o muestra un RETRY rojo, ¿lo pulso?
No.
Son errores visuales conocidos del asistente: RETRY reconstruye todo el sandbox.
No refresques la pestaña durante la configuración y sigue el registro de actividad hasta ver "AGENT CREATED SUCCESSFULLY".
Si ves `503 no_healthy_upstream`, espera un minuto y recarga; si no se arregla, despliega una instancia nueva.

## P: Me sale "ssh: Could not resolve hostname" o la instancia no aparece en la CLI
Primero ejecuta `brev ls` y `brev refresh`, que sincroniza la lista y reescribe `~/.brev/ssh_config`.
Si sigue fallando, la línea `Include` de Brev en `~/.ssh/config` quedó dentro de otro bloque `Host`: haz una copia del archivo y mueve esa línea al inicio, antes del primer `Host`.
Si SSH dice `Permission denied (publickey)`, vuelve a entrar con `brev logout && brev login`.

## P: Detuve y volví a encender la instancia y el agente no responde
Tras reiniciar la VM, Docker, el gateway de OpenShell y el sandbox pueden no arrancar solos.
Entra con `brev shell <instancia>` y ejecuta `sudo systemctl start docker`, luego `nemoclaw <sandbox> status`, `nemoclaw <sandbox> start` si quedó detenido y `nemoclaw <sandbox> recover` si el gateway no responde.
