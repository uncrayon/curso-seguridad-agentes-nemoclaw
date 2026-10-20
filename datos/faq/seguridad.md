# Seguridad de keys, cookies y accesos

## P: ¿Qué datos nunca debo compartir en foros, issues o capturas?
Tu API key `nvapi-`, el valor de `OPENCLAW_GATEWAY_TOKEN` que ves dentro del sandbox, la URL del dashboard con `#token=`, la salida de `nemoclaw <sandbox> gateway-token`, las cookies de sesión de tu navegador y archivos como `.env`, `~/.brev/credentials.json` o `~/.brev/brev.pem`.
Tampoco compartas exportaciones de sesiones sin revisarlas: pueden incluir secretos que pegaste en el chat.
Si un log o una captura los incluye, reemplázalos por `<REDACTADO>`.

## P: Filtré mi API key (la subí a GitHub o salió en un video), ¿qué hago?
Revócala de inmediato en build.nvidia.com, en API Keys, y genera una nueva.
Actualízala en Colab, en tu `.env` y en NemoClaw: en el laboratorio, lo más simple es borrar la instancia y crear tu agente otra vez con la key nueva; en tu máquina, usa `nemoclaw onboard --name <sandbox>` con la nueva `NVIDIA_INFERENCE_API_KEY`.
Borrar el archivo o hacer otro commit no basta: la key sigue en el historial de git.
Revisa el consumo de tu cuenta en build.nvidia.com por si hubo uso extraño.

## P: Compartí sin querer una cookie del laboratorio o la URL del dashboard
Con una cookie de sesión, una URL con token o el token del gateway, otra persona podría entrar a tu laboratorio o a tu agente.
Si la instancia no tiene nada que conservar, bórrala en Brev con Delete; si necesitas pensarlo, detenla con Stop mientras decides.
Una instancia nueva tiene su propia dirección y sus propios tokens.
Cierra también la sesión de tu cuenta de NVIDIA en ese navegador si lo usaste en una computadora compartida.

## P: ¿Es seguro exponer el dashboard o el gateway a internet?
No.
El gateway de OpenShell (puerto 18080) controla el agente y el dashboard de OpenClaw (puerto 18789) da acceso a él; en el laboratorio los dos escuchan solo en `127.0.0.1` de la máquina.
Al laboratorio entras por la página del botón verde NemoClaw, que pide iniciar sesión con tu cuenta de NVIDIA.
Nunca abras esos puertos al público, por ejemplo con `brev ports open` y `--public`.

## P: ¿Dónde guarda NemoClaw mis keys? ¿El agente puede verlas?
NemoClaw registra las keys de los proveedores en el gateway de OpenShell, del lado del host, y los sandboxes nuevos usan proveedores adjuntos que dejan la credencial en el host.
Dentro del sandbox, `NVIDIA_INFERENCE_API_KEY` solo contiene un marcador que empieza con `openshell:resolve:env:`, no la key real.
Por eso no pongas keys en `openclaw.json` ni en archivos del workspace: lo que está dentro del sandbox, el agente lo puede leer.
