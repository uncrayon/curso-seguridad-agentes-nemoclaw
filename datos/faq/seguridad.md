# Seguridad de keys, cookies y accesos

## P: ¿Qué datos nunca debo compartir en foros, issues o capturas?
Tu API key `nvapi-`, las cookies del laboratorio (`CF_Authorization`, `_pomerium`, `__Host-skybridge-brev-prd`), la URL del dashboard con `#token=`, la salida de `nemoclaw <sandbox> gateway-token` y archivos como `.env`, `~/.brev/credentials.json` o `~/.brev/brev.pem`.
Tampoco compartas exportaciones de sesiones sin revisarlas: pueden incluir secretos que pegaste en el chat.
Si un log los incluye, reemplázalos por `<REDACTADO>`.

## P: Filtré mi API key (la subí a GitHub o salió en un video), ¿qué hago?
Revócala de inmediato en build.nvidia.com, en API Keys, y genera una nueva.
Actualízala en Colab, en tu `.env` y en NemoClaw (con `nemoclaw onboard --name <sandbox>` y la nueva `NVIDIA_INFERENCE_API_KEY`).
Borrar el archivo o hacer otro commit no basta: la key sigue en el historial de git.
Revisa tu uso por si hubo consumo extraño. [VERIFICAR EN LAB]

## P: Compartí sin querer una cookie del laboratorio o la URL del dashboard
Con esa cookie o ese token otra persona podría entrar a tu launchable o a tu gateway.
Detén la instancia en Brev (o bórrala si no tiene nada que conservar), cierra sesión en el launchable y vuelve a entrar para obtener una cookie nueva.
Detener la instancia es lo más seguro mientras no sepamos si cerrar sesión invalida la cookie al instante. [VERIFICAR EN LAB]

## P: ¿Es seguro exponer el dashboard o el gateway a internet?
No.
El gateway (puerto 8080) controla el agente y el dashboard (puerto 18789) da acceso a él.
Usa un túnel con `brev port-forward <instancia> -p 18789:18789` o `ssh -L`, que mantiene el acceso en `127.0.0.1`.
Nunca abras el 8080 ni uses `brev ports open` con `--public` para el dashboard.

## P: ¿Dónde guarda NemoClaw mis keys? ¿El agente puede verlas?
NemoClaw registra las keys de los proveedores en el gateway de OpenShell, del lado del host, y los sandboxes nuevos usan proveedores adjuntos que dejan la credencial en el host.
Por eso no pongas keys en `openclaw.json` ni en archivos del workspace: lo que está dentro del sandbox, el agente lo puede leer.
