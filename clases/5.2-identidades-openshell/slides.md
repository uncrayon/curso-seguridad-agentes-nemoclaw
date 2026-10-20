## ¿Quién está actuando?

:::diagrama c52-quien

Notas:
Tres respuestas, tres niveles de poder. Clic 1: el usuario con el que corre el agente (sandbox, sin root). Clic 2: cada programa que abre una conexión (/usr/local/bin/openclaw, /usr/bin/curl…), con sus propios permisos. Clic 3: tú, el operador, en el host con nemoclaw y openshell. Clic 4: mínimo privilegio, la llave de su oficina y no la llave maestra. Si la respuesta fuera "root con un token que puede todo", ninguna política abajo te salva.

---

## Pedir más autoridad

:::diagrama c52-pedir-mas

Notas:
Es el bloque "¿Qué ocurre cuando estos comandos solicitan más permisos?" de la página 04a. Las pruebas: sudo id, nsenter -t 1 -m -- id, docker ps, y con Python os.setuid(0), ptrace y mount. Un clic por mensaje: command not found (no existe, no prueba nada), Permission denied (archivos / Landlock), Operation not permitted (kernel / seccomp). Clic 4: un EPERM no te dice si fue seccomp o la falta de capacidades. Las pruebas de seccomp usan Python con ctypes, no tienen efectos y están en la receta 4.

---

## El permiso de red va atado al programa

:::diagrama c52-por-programa

Notas:
Es el mapa de la página 04a con el selector "binario que llama". Clic 1: openclaw pasa a docs.openclaw.ai. Clic 2: curl, al mismo destino, recibe CONNECT tunnel failed, response 403. Clic 3: mismo destino, otro programa, otra respuesta. En la política base, openclaw_docs solo lista /usr/local/bin/openclaw.

---

## Pregúntale al sandbox

:::diagrama c52-verifica

Notas:
Clic 1: primero el operador le pregunta al sistema (openshell sandbox exec … whoami, id, pwd): sandbox, uid distinto de 0, /sandbox. Clic 2: luego se lo preguntas al agente con nemoclaw my-assistant agent -m. Clic 3: si no coinciden, gana la terminal. Los comandos están en la diapositiva "Si prefieres la terminal".

---

## Su autoridad, en un archivo

:::diagrama c52-ficha

Notas:
grep -E '^(NoNewPrivs|Seccomp|CapEff)' /proc/self/status dentro del sandbox. Prueba segura: solo lee. Un clic por línea: NoNewPrivs 1 (sin escalar con setuid), Seccomp 2 (filtro de syscalls activo), CapEff en ceros (sin capacidades de root). Valores a confirmar en la prueba previa.

---

## ¿Y si engaño a OpenShell?

:::diagrama c52-enganar

Notas:
Un clic por truco: falsificar argv[0] (exec -a /usr/local/bin/openclaw curl …) → 403; copiar el binario (cp curl /tmp/openclaw) → 403; reemplazar el real → /usr es solo lectura, EACCES. Clic 4: OpenShell lee /proc/<pid>/exe, recorre los procesos padre y guarda un hash SHA256 la primera vez (trust-on-first-use). Si el binario cambia mientras corre el sandbox, el hash no coincide y se niega.

---

## Tu API key no está adentro

:::diagrama c52-key-afuera

Notas:
Clic 1: dentro del sandbox el agente solo tiene un placeholder: NVIDIA_INFERENCE_API_KEY=openshell:resolve:env:…. Clic 2: el proxy L7 (la recepción) lo cambia por la key real. Clic 3: solo en la ruta permitida a integrate.api.nvidia.com. Clic 4: si el agente filtra esa variable, filtra un texto sin valor. Quita la pata de datos privados para la key, no para todo: el token del gateway de OpenClaw sí está en el sandbox. Usar siempre el env filtrado de la receta 6.

---

## El operador está por encima

:::diagrama c52-operador

Notas:
Clic 1: tu terminal cambia políticas y aprueba salidas. Clic 2: el token del gateway (operator.admin) lee persona, cron y sesiones. Clic 3: las reglas de egress no ven esta autoridad. Clic 4: tokens con alcance mínimo, vida corta y rotación. Celda "¿Qué puede ver un token operator.admin?" de la página 04a: solo lecturas.

---

## Si prefieres la terminal

```bash
openshell sandbox list                                      # el nombre exacto del sandbox
openshell sandbox exec -n my-assistant -- whoami            # sandbox
openshell sandbox exec -n my-assistant -- grep -E '^(NoNewPrivs|Seccomp|CapEff)' /proc/self/status
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://docs.openclaw.ai
nemoclaw credentials list                                   # la key vive afuera
```

.lead Es opcional: lo mismo que viste en la página de NVIDIA, escrito como instrucciones.

Notas:
La forma de operador, desde el host del lab con brev shell. Nunca env sin filtro ni una tubería sin sh -c '…': correría en el host. Los comandos largos (exec -a, env filtrado, seccomp) están en el cookbook.

---

## Errores comunes

| Síntoma | Causa |
|---|---|
| `whoami` → `root` | Usaste `docker exec` |
| La tubería corre en el host | Falta `sh -c '…'` |
| No hay variable `…KEY` | Sandbox anterior a v0.0.132 |
| "recent network policy denial detected" | Pista informativa |

Notas:
La tabla completa está en la página de la clase.
