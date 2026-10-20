# OpenShell y políticas del sandbox

## P: ¿Qué significa "CONNECT tunnel failed, response 403" dentro del sandbox?
No es un problema de certificados: la red de salida del sandbox está bloqueada por defecto y el proxy de OpenShell rechazó la conexión porque ninguna política la permite.
Mira la línea DENIED con `nemoclaw <sandbox> logs --tail 50`, revisa los presets con `nemoclaw <sandbox> policy list` y agrega el que falte con `nemoclaw <sandbox> policy add <preset>`.

## P: Ya permití el host y sigue saliendo 403, ¿por qué?
OpenShell exige que coincidan el host y el binario que hace la llamada.
Por ejemplo, npm corre como `/usr/local/bin/node`, y si el preset no lista ese binario la llamada se rechaza.
Lee la línea DENIED en `nemoclaw <sandbox> logs --tail 50`, copia la ruta exacta del binario y agrégala a la sección `binaries:` de tu preset.

## P: ¿Cómo apruebo en vivo una conexión bloqueada?
En el host ejecuta `openshell term`.
Elige el sandbox con `j`/`k` y Enter, pulsa `r` para ir a Network Rules, selecciona la solicitud pendiente y pulsa `a` para aprobar o `x` para rechazar.
Estas aprobaciones duran solo mientras exista esa instancia del sandbox; para que sean permanentes, usa un preset.

## P: ¿Cómo veo la política activa y agrego un preset como pypi o github?
Ve los presets con `nemoclaw <sandbox> policy list` y la política efectiva completa con `openshell policy get --full <sandbox>`.
Prueba un preset con `nemoclaw <sandbox> policy add pypi --dry-run` y aplícalo con `--yes`; quítalo con `nemoclaw <sandbox> policy remove pypi --yes`.
GitHub no está en la política base: agrégalo a propósito.
Los cambios de red se aplican sin reiniciar.

## P: Cambié la política de archivos y no tuvo efecto, ¿por qué?
Solo la política de red y la de inferencia se recargan en caliente.
La de sistema de archivos (Landlock) y la de procesos quedan fijas al crear el sandbox.
Edita la política base y vuelve a crear el sandbox con `nemoclaw onboard` o `nemoclaw <sandbox> rebuild`.

## P: Me aparece el aviso "Landlock: Docker VM kernel does not support Landlock", ¿es grave?
Es un aviso, no bloquea.
Tu kernel (o la VM de Docker en macOS) no soporta Landlock, así que el sandbox funciona en modo `best_effort`, sin restricciones de archivos a nivel kernel.
Para la protección completa, usa Linux con kernel 5.13 o mayor, como Ubuntu 22.04 o posterior.

## P: ¿Qué nivel de política elijo: Restricted, Balanced, Open o Personal?
Para el curso usa Balanced, el nivel por defecto: incluye la política base más `npm`, `pypi`, `huggingface`, `brew-balanced` y `brave`.
Restricted deja solo la base.
Open agrega mensajería y otros servicios.
Personal permite cualquier host en los puertos 80 y 443 sin pedir aprobación; úsalo solo con cargas de trabajo en las que confías por completo.
