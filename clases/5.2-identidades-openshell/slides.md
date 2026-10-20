## ¿Quién está actuando?

:::diagrama c52-quien

Notas:
Tres respuestas, tres niveles de poder. Clic 1: el usuario con el que corre el agente (sandbox, sin root). Clic 2: cada programa que abre una conexión (/usr/local/bin/openclaw, /usr/bin/curl…), con sus propios permisos. Clic 3: tú, el operador, en el host con nemoclaw y openshell. Clic 4: mínimo privilegio, la llave de su oficina y no la llave maestra. Si la respuesta fuera "root con un token que puede todo", ninguna política abajo te salva.

---

## Pedir más autoridad

:::diagrama c52-pedir-mas

Notas:
Desde la VM TERMINAL con openshell sandbox exec (recetas 3 y 4). En el lab: sudo id → command not found; os.setuid(0) → PermissionError [Errno 1] Operation not permitted; touch /usr/local/bin/… → Permission denied. Un clic por mensaje: command not found (no existe, no prueba nada), Permission denied (archivos / Landlock), Operation not permitted (kernel / seccomp). nsenter, docker ps y ptrace/mount están en el cookbook para clasificar con la misma tabla. Clic 4: un EPERM no te dice si fue seccomp o la falta de capacidades. Las pruebas de seccomp usan Python con ctypes, no tienen efectos y están en la receta 4.

---

## El permiso de red va atado al programa

:::diagrama c52-por-programa

Notas:
La regla nombra programas, no "al agente". Clic 1: el programa que la regla openclaw_docs lista pasa. Clic 2: curl, al mismo destino, recibe CONNECT tunnel failed, response 403 (verificado en el lab, salida 56). Clic 3: mismo destino, otro programa, otra respuesta. Ojo con lo que vimos en el lab: cuando el agente lo intentó, salió por curl y por node, y el guardia negó los dos. Las reglas se ven en la OPENSHELL TUI (Enter en my-assistant).

---

## Pregúntale al sandbox

:::diagrama c52-verifica

Notas:
Clic 1: primero el operador le pregunta al sistema (SANDBOX TERMINAL, o openshell sandbox exec … id desde la VM TERMINAL): sandbox, uid=998, /sandbox. Clic 2: luego se lo preguntas al agente en el chat. Clic 3: si no coinciden, gana la terminal. Caso real del lab: el agente dijo ser "gateway-owner"; el usuario real es sandbox. Comparar con la VM TERMINAL: ubuntu, con sudo y docker.

---

## Su autoridad, en un archivo

:::diagrama c52-ficha

Notas:
grep -E '^(NoNewPrivs|Seccomp|CapEff)' /proc/self/status dentro del sandbox. Prueba segura: solo lee. Un clic por línea: NoNewPrivs 1 (sin escalar con setuid), Seccomp 2 (filtro de syscalls activo), CapEff en ceros (sin capacidades de root). Son los valores que vimos en el lab.

---

## ¿Y si engaño a OpenShell?

:::diagrama c52-enganar

Notas:
Un clic por truco, según la documentación de NemoClaw: falsificar argv[0] (exec -a /usr/local/bin/openclaw curl …) no cambia el programa real; copiar el binario (cp curl /tmp/openclaw) deja otra ruta; reemplazar el real no se puede: touch en /usr/local/bin da Permission denied (visto en el lab). Clic 4: OpenShell lee /proc/<pid>/exe, recorre los procesos padre y guarda un hash SHA256 la primera vez (trust-on-first-use). Los dos primeros trucos están en la receta 5 para que los estudiantes los prueben y anoten el resultado.

---

## Una respuesta no es una prueba

```text
DENIED /usr/bin/curl(11932) -> docs.openclaw.ai:443
  reason: binary '/usr/bin/curl' not allowed in policy 'openclaw_docs'
  (ancestors: /usr/bin/bash -> /usr/local/bin/node -> /usr/bin/bash)
DENIED /usr/local/bin/node(11950) -> docs.openclaw.ai:443
  reason: binary '/usr/local/bin/node' not allowed in policy 'openclaw_docs'
```

.lead El agente respondió igual, de memoria. Lo que prueba el acceso es el registro.

Notas:
Lo que pasó en el lab: le pedimos al agente que abriera docs.openclaw.ai. Intentó con curl y luego con node; el guardia negó los dos. Aun así respondió con una frase creíble sobre OpenClaw. Comando: nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4. Leer la línea: quién (binario y PID), sus procesos padre (ancestors: el agente corre sobre node), a dónde (host:puerto) y por qué (la política openclaw_docs no lista ese binario). La misma petición aparece pendiente en la OPENSHELL TUI, tecla r (Rules).

---

## Tu API key no está adentro

:::diagrama c52-key-afuera

Notas:
Clic 1: dentro del sandbox el agente solo tiene un placeholder: NVIDIA_INFERENCE_API_KEY=openshell:resolve:env:… (visto en el lab). Clic 2: el proxy L7 (la recepción) lo cambia por la key real. Clic 3: solo en la ruta permitida hacia NVIDIA. Clic 4: si el agente filtra esa variable, filtra un texto sin valor. Quita la pata de datos privados para la key, no para todo: el token del gateway de OpenClaw sí está en el sandbox (OPENCLAW_GATEWAY_TOKEN). Usar siempre el env filtrado de la receta 6.

---

## El operador está por encima

:::diagrama c52-operador

Notas:
Clic 1: tu terminal cambia políticas y aprueba salidas. Clic 2: el token del gateway (operator.admin) lee persona, cron y sesiones. Clic 3: las reglas de egress no ven esta autoridad. Clic 4: tokens con alcance mínimo, vida corta y rotación. Recordar: en el lab, el operador es ubuntu con sudo y docker.

---

## Si prefieres la terminal

```bash
openshell sandbox list                                      # el nombre exacto del sandbox
openshell sandbox exec -n my-assistant -- whoami            # sandbox
openshell sandbox exec -n my-assistant -- grep -E '^(NoNewPrivs|Seccomp|CapEff)' /proc/self/status
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://docs.openclaw.ai
nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4   # quién fue negado y por qué
```

.lead Se pegan en la VM TERMINAL del tablero. El chat y la OPENSHELL TUI muestran lo mismo con clics.

Notas:
La forma de operador: VM TERMINAL del tablero (usuario ubuntu). Clic en el área negra antes de escribir. Nunca env sin filtro ni una tubería sin sh -c '…': correría en el host. Los comandos largos (env filtrado, seccomp, exec -a) están en el cookbook.

---

## Errores comunes

| Síntoma | Causa |
|---|---|
| `whoami` → `root` | Usaste `docker exec` |
| La tubería corre en el host | Falta `sh -c '…'` |
| No hay variable `…KEY` | Sandbox anterior a v0.0.132 |
| "recent network policy denial detected" | Pista informativa |
| El agente "abrió" la página | Mira el registro: puede ser memoria |

Notas:
La tabla completa está en la página de la clase.
