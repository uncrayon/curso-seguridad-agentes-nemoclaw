# NemoClaw instalado en tu máquina

## P: ¿Qué necesito para instalar NemoClaw en mi computadora?
Mínimo 4 vCPU, 8 GB de RAM y 20 GB de disco libre (recomendado 16 GB y 40 GB).
Necesitas Node.js 22.19 o mayor y Docker funcionando antes de instalar.
Funciona en Ubuntu 24.04, macOS con Apple Silicon y Windows con WSL2; Mac con Intel no está soportado.
Revisa tu máquina con `nemoclaw host probe` e instala con `curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash`.

## P: Después de instalar me sale "nemoclaw: command not found"
Tu terminal no tiene el PATH actualizado.
Abre una terminal nueva o ejecuta `source ~/.bashrc` (o `source ~/.zshrc`).
Si `node --version` sigue mostrando v20, ejecuta `nvm install 22 && nvm use 22` y vuelve a correr el instalador.

## P: El instalador dice "Docker is not running" pero Docker sí está corriendo
Tu usuario no está en el grupo `docker`.
Ejecuta `sudo usermod -aG docker $USER && newgrp docker` y comprueba que `docker ps` funcione sin sudo; si el gateway corre como servicio, cierra sesión por completo o reinicia.
Ojo: estar en el grupo docker equivale casi a ser root, hazlo solo en tu máquina.

## P: En macOS con Colima no encuentra Docker ("Socket not found: /var/run/docker.sock")
Instala lo necesario con `xcode-select --install` y `brew install colima docker`, arranca Colima con `colima start --cpu 4 --memory 8` y comprueba con `docker info`.
Si aparece `Socket not found: /var/run/docker.sock`, es una regresión abierta: exporta `export DOCKER_HOST=unix://$HOME/.colima/default/docker.sock` y reintenta.

## P: La creación del sandbox muere con exit 137 por falta de memoria
La imagen del sandbox pesa unos 2.4 GB comprimida y con 8 GB de RAM o menos el sistema puede matar el proceso.
Agrega 4 GB de swap (el onboarding ofrece hacerlo) o usa una máquina de 16 GB.

## P: El puerto 18789 o el 18080 ya está en uso, ¿qué hago?
Mira quién lo ocupa con `sudo lsof -i :18789 -sTCP:LISTEN -P -n`.
Puedes mover el dashboard con `nemoclaw onboard --control-ui-port 19000` y el gateway con `NEMOCLAW_GATEWAY_PORT=8990 nemoclaw onboard`, manteniendo esa variable en los comandos siguientes.
Solo detén un proceso si sabes que es tuyo.

## P: El onboarding se interrumpió a la mitad, ¿tengo que empezar de cero?
No.
NemoClaw guarda el avance en `~/.nemoclaw/onboard-session.json`.
Continúa con `nemoclaw onboard --resume` o descarta todo con `nemoclaw onboard --fresh`.
En servidores remotos, corre el onboarding dentro de `tmux` para que sobreviva a una desconexión.

## P: ¿Cómo actualizo NemoClaw? ¿Puedo usar openshell self-update?
Nunca uses `openshell self-update`: cada versión de NemoClaw fija una versión exacta de OpenShell (la 0.0.116 en la v0.0.134).
Actualiza así: `nemoclaw backup-all`, `nemoclaw update`, `nemoclaw upgrade-sandboxes --check` y `nemoclaw upgrade-sandboxes --auto`.
Tampoco actualices OpenClaw dentro del sandbox: usa `nemoclaw update` y luego `nemoclaw <sandbox> rebuild`.

## P: Reinicié la máquina y el sandbox no responde o dice "sandbox not found"
Docker, el gateway y el sandbox pueden no arrancar solos.
Inicia Docker (`sudo systemctl start docker`, Docker Desktop o `colima start`), revisa el gateway en Linux con `systemctl --user restart openshell-gateway` y luego ejecuta `nemoclaw <sandbox> status`, `nemoclaw <sandbox> start` y `nemoclaw <sandbox> recover`.
No sigas guías que usan `docker exec openshell-cluster-nemoclaw kubectl`: son de una arquitectura vieja.

## P: Con Ollama local sale "cannot reach the Ollama auth proxy at host.openshell.internal:11435"
NemoClaw deja Ollama en `127.0.0.1:11434` y abre un proxy con token en el puerto 11435 para el sandbox.
Un firewall del host lo está bloqueando: permite la subred de la red `openshell-docker` hacia el puerto 11435 con `ufw` y vuelve a ejecutar `nemoclaw onboard`.
No uses `OLLAMA_HOST=0.0.0.0`.

## P: ¿Cómo cambio el modelo o roto mi API key en NemoClaw?
Mira el modelo actual con `nemoclaw inference get` y cámbialo con `nemoclaw inference set --provider nvidia-prod --model <modelo> --sandbox <sandbox>`.
Para rotar la key, exporta la nueva en `NVIDIA_INFERENCE_API_KEY` y ejecuta `nemoclaw onboard --name <sandbox> --non-interactive --yes --yes-i-accept-third-party-software`; después haz `unset NVIDIA_INFERENCE_API_KEY`.
Confirma el nombre del proveedor con `nemoclaw credentials list`.
