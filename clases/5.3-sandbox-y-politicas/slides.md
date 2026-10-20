## No preguntes "¿es seguro?"

.lead Pregunta: ¿a qué puede llegar exactamente, y ya lo probé?

:::diagrama c53-ciclo

Notas:
Es el flujo de la página 04a: Predecir, Confirmar, Comparar. El ciclo se ilumina solo; un clic por paso en la lista: lee la política real, predice, prueba en el sandbox, compara y, si no coincide, investiga.

---

## La política real

:::diagrama c53-reglamento

Notas:
En la página 04a es la celda "Lee la política activa del launchable"; en la terminal, openshell policy get my-assistant --full. Un clic por sección, con su nombre técnico a la derecha: filesystem_policy (include_workdir, read_only, read_write), landlock (compatibility: best_effort), process (run_as_user: sandbox) y network_policies (nvidia, managed_inference, clawhub…). Clic 5: seccomp no aparece aquí porque OpenShell lo aplica siempre. Guárdala antes de cambiar nada.

---

## Un grupo de red

:::diagrama c53-grupo

Notas:
Clic 1: llega una petición de openclaw. Clic 2: el grupo openclaw_docs y sus cinco datos (host docs.openclaw.ai, port 443, method GET, path /**, binaries /usr/local/bin/openclaw). Clic 3: coinciden todos, pasa. Clic 4: si falta uno, se niega. protocol: rest activa la inspección L7: el proxy revisa cada petición, no solo el host.

---

## Archivos: qué lee y dónde escribe

:::diagrama c53-archivos

Notas:
Un clic por grupo: solo lectura (/usr, /etc, /proc), lectura y escritura (/tmp, /sandbox, /sandbox/.openclaw), ni lectura (/var/lib/apt, /root). La regla con el prefijo más largo gana. /var/lib/apt es legible para cualquier usuario de Linux; la niega Landlock. Clic 4: SOUL.md vive en /sandbox/.openclaw y la política no protege la persona.

---

## Predice, luego prueba

:::diagrama c53-predice

Notas:
Clic 1: aparecen las cinco peticiones con un "?": pide que los estudiantes digan su predicción. Clics 2 a 6, un veredicto por clic: inference.local pasa; example.com recibe 403 del proxy; integrate.api.nvidia.com con curl se bloquea porque el grupo es para el binario openclaw; /var/lib/apt da EACCES; escribir SOUL.md está permitido (la sorpresa). Notebook: 12 acciones con puntaje. Lab: recetas 3 y 4. Una coincidencia respalda solo esa acción.

---

## Lee un bloqueo

:::diagrama c53-bloqueo

Notas:
Clic 1: curl hacia example.com y el proxy responde curl: (56) CONNECT tunnel failed, response 403. Clic 2: queda en nemoclaw my-assistant logs --tail 50. Clic 3: openshell term (Enter → r → Enter → a / x). Clic 4: la aprobación dura lo que dure esa instancia del sandbox. Dos tipos de bloqueo: policy_denied (no coincidió, ¿lo apruebas?) y upstream_unreachable (coincidió, el host no respondió). Un 403 puede venir del proxy o del servidor: CONNECT tunnel failed es del proxy.

---

## Cambiar la política

:::diagrama c53-preset

Notas:
Clic 1: el preset github se engrapa al reglamento. Un clic por acción: policy add github --dry-run (ensayo), --yes (aplica en caliente), policy remove github --yes (quita). Clic 4: el error en vivo, el preset abre GitHub para /usr/bin/git, no para curl. Clic 5: en caliente cambian red e inferencia; archivos, Landlock y proceso piden recrear el sandbox. Las aprobaciones de openshell term duran lo que dure esa instancia; para que persistan, preset.

---

## El preset de Soporte NemoClaw

:::diagrama c53-preset-soporte

Notas:
Un clic por regla: method GET; host docs.nvidia.com, port 443, protocol rest, path /nemoclaw/**; binaries /usr/local/bin/openclaw. Lo validamos en el notebook con validar_preset() y lo aplicamos con policy add --from-file soporte-docs.yaml --dry-run primero.

---

## El sandbox es una capa

:::diagrama c53-una-capa

Notas:
Clic 1: los pasos del ataque de la 5.1 contra esta política, con su "?". Clics 2 a 5: leer la FAQ envenenada, permitido; leer MEMORY.md, permitido; curl al host del atacante, bloqueado; node → clawhub.ai con POST, permitido. Clic 6: un secreto impreso por un comando permitido ya se escapó. Una allowlist aprueba el destino, no el significado de los bytes. Arriba: procedencia, aprobación humana, secretos fuera del sandbox.

---

## Si prefieres la terminal

```bash
openshell policy get my-assistant --full > ~/politica-antes.txt   # guarda la política
nemoclaw my-assistant logs --tail 50                             # los bloqueos recientes
openshell term                                                   # panel en vivo: x rechaza, a aprueba
nemoclaw my-assistant policy add github --dry-run                # ensayo
nemoclaw my-assistant policy add github --yes                    # aplica en caliente
nemoclaw my-assistant policy add --from-file soporte-docs.yaml --dry-run
nemoclaw my-assistant policy remove github --yes                 # todo como estaba
```

.lead Es opcional: lo mismo que viste en la página de NVIDIA y en el notebook, escrito como instrucciones.

Notas:
La forma de operador, desde el host del lab con brev shell. No aprobar example.com en openshell term: usar siempre x.

---

## Errores comunes

| Síntoma | Causa |
|---|---|
| `CONNECT tunnel failed, response 403` | Política: host o programa |
| `code=403` sin CONNECT | Respondió el servidor |
| Preset aplicado, sigue bloqueado | Programa equivocado en el preset |
| La aprobación "desapareció" | Se recreó el sandbox |

Notas:
La tabla completa está en la página de la clase.
