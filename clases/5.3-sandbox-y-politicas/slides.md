## No preguntes "¿es seguro?"

.lead Pregunta: ¿a qué puede llegar exactamente, y ya lo probé?

:::diagrama c53-ciclo

Notas:
Es el flujo de toda la clase. El ciclo se ilumina solo; un clic por paso en la lista: lee la política real, predice, prueba en el sandbox, compara y, si no coincide, investiga.

---

## La política real

:::diagrama c53-reglamento

Notas:
En el tablero: OPENSHELL TUI → my-assistant → Enter (carpetas y reglas de red); en la VM TERMINAL: openshell policy get my-assistant --full. Un clic por sección, con su nombre técnico a la derecha: filesystem_policy (include_workdir, read_only, read_write), landlock (compatibility: best_effort), process (run_as_user: sandbox) y network_policies (en el lab, 13 grupos: nvidia, managed_inference, native_nvidia_inference, clawhub, openclaw_docs, pypi…). Clic 5: seccomp no aparece aquí porque OpenShell lo aplica siempre. Guárdala antes de cambiar nada.

---

## Un grupo de red

:::diagrama c53-grupo

Notas:
Clic 1: llega una petición de openclaw. Clic 2: el grupo openclaw_docs y sus cinco datos (host docs.openclaw.ai, port 443, method GET, path /**, binaries /usr/local/bin/openclaw). Clic 3: coinciden todos, pasa. Clic 4: si falta uno, se niega. protocol: rest activa la inspección L7: el proxy revisa cada petición, no solo el host. Recordar la 5.2: en el lab, cuando el agente pidió docs.openclaw.ai salió por curl y por node, y este grupo negó a los dos.

---

## Archivos: qué lee y dónde escribe

:::diagrama c53-archivos

Notas:
Un clic por grupo: solo lectura (/usr, /etc, /proc), lectura y escritura (/tmp, /sandbox, /sandbox/.openclaw), ni lectura (/var/lib/apt, /root). La regla con el prefijo más largo gana. En el lab: ls /var/lib/dpkg funciona; ls /var/lib/apt/lists da Permission denied (legible para cualquier usuario de Linux; la niega Landlock); touch en /usr y /etc, Permission denied; /tmp se puede escribir. Clic 4: SOUL.md vive en /sandbox/.openclaw y la política no protege la persona.

---

## Predice, luego prueba

:::diagrama c53-predice

Notas:
Clic 1: aparecen las cinco peticiones con un "?": pide que los estudiantes digan su predicción. Clics 2 a 6, un veredicto por clic: inference.local pasa el proxy (code=503: responde la ruta interna, que el lab no usa); example.com recibe CONNECT tunnel failed, 403 del proxy; integrate.api.nvidia.com con curl PASA (code=200): el perfil nativo de inferencia de NVIDIA lo abre, aunque el notebook (política base) diga DENY. Es un hallazgo real, no una falla; /var/lib/apt da Permission denied; escribir SOUL.md está permitido (la otra sorpresa). Notebook: 12 acciones con puntaje. Lab: recetas 3 y 4. Una coincidencia respalda solo esa acción.

---

## Lee un bloqueo

:::diagrama c53-bloqueo

Notas:
Clic 1: curl hacia example.com y el proxy responde curl: (56) CONNECT tunnel failed, response 403. Clic 2: con nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4. Clic 3: OPENSHELL TUI → my-assistant → Enter → r (Rules) → seleccionar → x rechaza, a aprueba. Clic 4: aprobar ahí es temporal, vale para ese sandbox; para algo que dure, un preset. Dos tipos de bloqueo: policy_denied (no coincidió, ¿lo apruebas?) y upstream_unreachable (coincidió, el host no respondió). Un 403 puede venir del proxy o del servidor: CONNECT tunnel failed es del proxy.

---

## Cambiar la política

:::diagrama c53-preset

Notas:
Clic 1: un preset de la lista (github, uno de los muchos que muestra policy list) se engrapa al reglamento. Un clic por acción: --dry-run (ensayo), --yes (aplica en caliente), policy remove … --yes (quita). Clic 4: un preset también va atado a programas: el de github nombra a git, no a curl. Clic 5: en caliente cambian red e inferencia; archivos, Landlock y proceso piden recrear el sandbox. En el video el ciclo completo se hace con soporte-docs (siguiente diapositiva); github queda como receta opcional 7c. Las aprobaciones de la OPENSHELL TUI son temporales; para que persistan, preset.

---

## El preset de Soporte NemoClaw

:::diagrama c53-preset-soporte

Notas:
Un clic por regla: method GET; host docs.nvidia.com, port 443, protocol rest, path /nemoclaw/**; binaries /usr/local/bin/openclaw y /usr/local/bin/node (el agente sale a la red con node). Lo validamos en el notebook con validar_preset(). En el lab: --dry-run imprime la política, el aviso "custom preset targets are not vetted" y "not applied"; --yes → "Applied preset: soporte-docs"; policy list lo marca [user-added]; el agente respondió en dos líneas sin negaciones; policy remove soporte-docs --yes → "Removed preset: soporte-docs".

---

## El sandbox es una capa

:::diagrama c53-una-capa

Notas:
Clic 1: los pasos del ataque de la 5.1 contra esta política, con su "?". Clics 2 a 5: leer la FAQ envenenada, permitido; leer MEMORY.md, permitido; curl al host del atacante, bloqueado; node → clawhub.ai con POST, permitido. Clic 6: un secreto impreso por un comando permitido ya se escapó. Y otro canal real del lab: curl llega a integrate.api.nvidia.com. Una allowlist aprueba el destino, no el significado de los bytes. Arriba: procedencia, aprobación humana, secretos fuera del sandbox.

---

## Si prefieres la terminal

```bash
openshell policy get my-assistant --full > ~/politica-antes.txt   # guarda la política
nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4   # los bloqueos recientes
nemoclaw my-assistant policy list                                # presets activos y disponibles
nemoclaw my-assistant policy add --from-file ~/soporte-docs.yaml --dry-run   # ensayo
nemoclaw my-assistant policy add --from-file ~/soporte-docs.yaml --yes       # aplica en caliente
nemoclaw my-assistant policy remove soporte-docs --yes           # todo como estaba
```

.lead Se pegan en la VM TERMINAL del tablero. La OPENSHELL TUI muestra la política y las peticiones pendientes con teclas.

Notas:
La forma de operador: VM TERMINAL del tablero (usuario ubuntu). En la OPENSHELL TUI: r (Rules), seleccionar, x rechaza. No aprobar example.com: usar siempre x. Nunca d en la vista del sandbox.

---

## Errores comunes

| Síntoma | Causa |
|---|---|
| `CONNECT tunnel failed, response 403` | Política: host o programa |
| `code=403` sin CONNECT | Respondió el servidor |
| Preset aplicado, sigue bloqueado | Programa equivocado en el preset |
| La aprobación "desapareció" | Se recreó el sandbox |
| curl → API de NVIDIA da 200 | Perfil nativo de NVIDIA |

Notas:
La tabla completa está en la página de la clase.
