# Cookbook 5.3 · Leer, probar y cambiar la política del sandbox

Recetas para el laboratorio NemoClaw en Brev, todas desde el navegador: leer la política real, predecir y probar bloqueos, diagnosticar una negación y agregar o quitar permisos con los comandos reales de NemoClaw.

**Convenciones**
- `my-assistant` es el nombre del sandbox (compruébalo con `openshell sandbox list`).
- Los comandos van en la **VM TERMINAL** del tablero de tu laboratorio (la terminal de operador, usuario `ubuntu`). Haz clic dentro del área negra antes de escribir. `openshell sandbox exec` los corre dentro del sandbox. Si usas `|`, `&&` o `>` dentro del sandbox, envuélvelos en `sh -c '...'`.
- Todos los comandos `nemoclaw` imprimen `ExperimentalWarning: SQLite is an experimental feature`. Ignórala.
- Las recetas 1 a 5 solo leen. Las 6 y 7 **cambian** la política: cada una dice cómo deshacerlo.
- Las salidas "esperadas" vienen de una prueba real del laboratorio. Donde una prueba no se repitió, la receta te dice qué buscar en lugar de prometer el texto exacto.

---

## 1 · Lee la política real

```bash
openshell policy get my-assistant --full
```

Deberías ver un encabezado de estado, una línea `---` y después el YAML con cuatro secciones: `filesystem_policy`, `landlock`, `process` y `network_policies`. Es largo: para leerlo con calma, guárdalo y ábrelo con `less` (sales con **q**).

**Sin comandos:** en el tablero, **OPENSHELL TUI** → `my-assistant` → **Enter**. La vista del sandbox muestra las carpetas de solo lectura y de lectura y escritura, y las reglas de red.

Guárdala para compararla después:

```bash
openshell policy get my-assistant --full > ~/politica-antes.txt
less ~/politica-antes.txt
```

Otras vistas útiles:

```bash
nemoclaw my-assistant policy list       # presets activos y disponibles, con su origen: [user-added], [from openclaw agent]…
nemoclaw my-assistant policy explain    # resumen sin YAML, pensado para el agente
nemoclaw my-assistant status            # estado del sandbox y de la inferencia
```

Solo los nombres de los grupos de red:

```bash
openshell policy get my-assistant --full | sed -n '/^network_policies:/,$p' | grep -E '^  [a-z0-9_-]+:$'
```

En el laboratorio de prueba había 13 grupos (el tablero dice «13 network policies»): `_provider_nemoclaw_nvidia_prod_v1`, `brew-balanced`, `clawhub`, `huggingface`, `managed_inference`, `native_nvidia_inference`, `npm_registry`, `npm_yarn`, `nvidia`, `openclaw-pricing`, `openclaw_api`, `openclaw_docs` y `pypi`.

**Si falla**
- Error de sandbox no encontrado: copia el nombre exacto de `openshell sandbox list`.
- Ves grupos que no están en el YAML del notebook (por ejemplo `pypi`, `brew-balanced` o entradas con prefijo `_provider_`): vienen del tier, de los presets activos o del proveedor de inferencia. Es normal.
- El comando de los nombres no imprime nada: tu versión formatea distinto el archivo. Busca `network_policies:` dentro de `less` escribiendo `/network_policies` y **Enter**.

## 2 · Recorre el YAML con esta lista

Busca y anota en tu hoja:

| Dónde | Qué mirar | Pregunta que responde |
|---|---|---|
| `filesystem_policy.read_only` | Rutas que se leen pero no se escriben (`/usr`, `/etc`…) | ¿Qué archivos alcanza? |
| `filesystem_policy.read_write` + `include_workdir` | Rutas donde puede escribir (`/tmp`, `/sandbox/.openclaw`, `/sandbox`) | ¿Dónde puede dejar cambios? |
| `landlock.compatibility` | `best_effort` o estricto | ¿Qué pasa si el kernel no soporta Landlock? |
| `process.run_as_user` | `sandbox` | ¿Con qué autoridad empieza? |
| `network_policies.<grupo>.endpoints` | `host`, `port`, `protocol`, `rules` (método + ruta) | ¿A dónde, y con qué peticiones? |
| `network_policies.<grupo>.binaries` | Rutas de ejecutables | ¿Quién puede usar ese destino? |

## 3 · Predice, luego prueba: red

Primero escribe tu predicción (ALLOW/DENY) para cada línea. Después ejecútalas:

```bash
# 3a · La dirección interna del modelo (grupo managed_inference)
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://inference.local/v1/models

# 3b · Un host que no está en la política
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://example.com; echo "salida=$?"

# 3c · La dirección de metadata de la nube
openshell sandbox exec -n my-assistant -- curl -sS -m 6 -o /dev/null -w 'code=%{http_code}\n' http://169.254.169.254/latest/meta-data/

# 3d · La API de modelos de NVIDIA, con curl
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://integrate.api.nvidia.com/v1/models

# 3e · El índice de PyPI (tier Balanced)
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://pypi.org/simple/
```

Cómo leer el resultado:

| Ves | Significa |
|---|---|
| `code=200` (o cualquier código del servidor) | La política dejó pasar la conexión. Si el código es 4xx/5xx, lo respondió el **servidor**, no el sandbox |
| `curl: (56) CONNECT tunnel failed, response 403` | El **proxy de OpenShell** negó la conexión (HTTPS) |
| `code=403` en una dirección `http://` | En HTTP sin cifrar, el 403 del proxy llega como código. Revisa el registro para saber si fue el proxy |
| Tiempo agotado | Puede ser un bloqueo o un host caído. Revisa la receta 5 |

Lo que salió en el laboratorio de prueba:

| Línea | Resultado | Lectura |
|---|---|---|
| 3a `inference.local` | `code=503` | Pasa el proxy; la ruta interna responde 503 porque el lab usa la ruta nativa de NVIDIA |
| 3b `example.com` | `curl: (56) CONNECT tunnel failed, response 403`, `code=000`, `salida=56` | Bloqueado por el proxy |
| 3c `169.254.169.254` | `code=403` | Bloqueado (el 403 del proxy, visible porque es HTTP) |
| 3d `integrate.api.nvidia.com` | `code=200` | **Permitido para curl**: el perfil nativo de inferencia de NVIDIA lo abre (grupos `native_nvidia_inference` y `_provider_nemoclaw_nvidia_prod_v1`) |
| 3e `pypi.org` | `code=200` | Permitido por el tier Balanced (grupo `pypi`) |

3d es la sorpresa que vale la pena discutir. La política base publicada (y el notebook) dicen que el grupo `nvidia` es solo para `openclaw`; tu laboratorio tiene además el perfil del proveedor, que deja pasar a `curl`. No es una falla: es un canal de salida más que tienes que anotar en tu `trifecta.md`.

**Si falla**
- 3b responde `code=200`: tu sandbox tiene el tier **Personal** (`personal-open-internet`), que abre todo 80/443. Revísalo con `nemoclaw my-assistant policy list`.
- Todo da 403, incluso 3e: el proxy no está sano. `nemoclaw my-assistant status` y, si hace falta, `nemoclaw my-assistant recover`.

## 4 · Predice, luego prueba: archivos

```bash
# 4a · Permitido: /var/lib/dpkg está en read_only
openshell sandbox exec -n my-assistant -- sh -c 'ls /var/lib/dpkg | head -3'

# 4b · Bloqueado: /var/lib/apt no está en la política (aunque Linux lo deje leer a cualquiera)
openshell sandbox exec -n my-assistant -- ls /var/lib/apt/lists

# 4c · Bloqueado: /usr y /etc son solo lectura
openshell sandbox exec -n my-assistant -- touch /usr/prueba
openshell sandbox exec -n my-assistant -- touch /etc/prueba-curso

# 4d · Permitido: /tmp es lectura y escritura (y lo limpiamos)
openshell sandbox exec -n my-assistant -- sh -c 'touch /tmp/prueba-curso && ls -l /tmp/prueba-curso && rm /tmp/prueba-curso'
```

Esperado (así salió en el laboratorio de prueba): 4a lista `alternatives`, `arch-native` y `available`; 4b da `Permission denied`; 4c da `Permission denied` en los dos; 4d crea y borra el archivo. 4b es la prueba que aísla a Landlock: los permisos normales de Linux sí dejarían leer esa carpeta.

Y pídeselo al agente (su respuesta cambia de una vez a otra; compárala con lo que viste tú):

```bash
nemoclaw my-assistant agent -m "Dime qué usuario eres y luego intenta crear el archivo /etc/prueba-agente. Cuéntame exactamente qué error recibiste."
```

**Si falla**
- 4b sí lista archivos: Landlock está en `best_effort` y el kernel quizá no lo soporta. Corre `openshell sandbox exec -n my-assistant -- uname -r` (Landlock necesita 5.13 o más) y busca en los logs `⚠ Landlock: … does not support Landlock`.
- 4c funciona: anótalo y repórtalo. No debería.

## 5 · Lee un bloqueo

```bash
nemoclaw my-assistant logs --tail 300 | grep DENIED | tail -4
```

Busca las negaciones de las recetas 3 y 4. Una línea de negación de red se ve así (ejemplo real de la clase 5.2, recortado):

```text
[sandbox] [OCSF ] [ocsf] NET:OPEN [MED] DENIED /usr/bin/curl(11932) -> docs.openclaw.ai:443 [policy:- engine:opa] [reason:binary '/usr/bin/curl' not allowed in policy 'openclaw_docs' (ancestors: [/usr/bin/bash -> /usr/local/bin/node -> /usr/bin/bash], cmdline: …
```

Te dice **quién** (programa y número de proceso), **quién lo lanzó** (`ancestors`), **a dónde** (host:puerto) y **por qué** (sin regla, programa no permitido o regla L7). Para `example.com` el motivo será otro, porque ningún grupo nombra ese host.

**Si falla**
- No aparecen negaciones: aumenta `--tail` o repite la receta 3b y vuelve a buscar. También puedes verlas en la OPENSHELL TUI (receta 6).

## 6 · Aprueba o rechaza en vivo (OPENSHELL TUI)

1. En la VM TERMINAL, provoca un bloqueo: repite la receta 3b (`example.com`).
2. Vuelve al tablero y haz clic en **OPENSHELL TUI**.
3. Pantalla principal: con **j**/**k** elige `my-assistant` y presiona **Enter**. (**Tab** cambia de panel, **q** sale.)
4. En la vista del sandbox, presiona **r** (Rules).
5. Selecciona la petición pendiente (por ejemplo la de `example.com`, o la de `openclaw_docs` con `curl` de la clase 5.2).
6. Presiona **x** (Reject) para **rechazarla**. **a** (Approve) la aprueba; **A** (Approve All) aprueba todas; **p** (Policy) muestra la política.

En el curso practica con **x**. Una aprobación en la TUI es **temporal**: vale para este sandbox y no se guarda en la política base; si recreas el sandbox, desaparece. Para un permiso que dure, que puedas revisar y quitar, usa un preset (receta 7).

Según la documentación de NemoClaw, un bloqueo puede ser de dos tipos:
- `policy_denied`: la política no coincidió. Decide si apruebas o no.
- `upstream_unreachable`: la política **sí** coincidió, pero el host no respondió. Abrir más la política no lo arregla.

**Si falla**
- El panel se ve cortado: agranda la ventana del navegador.
- No presiones **d** en la vista del sandbox: borra el sandbox.
- Aprobaste algo por error: queda activo en este sandbox. Anótalo y pide ayuda en el foro antes de tocar la política a mano.

## 7 · Presets: agrega y quita permisos (en caliente)

Los cambios de **red** se aplican sin reiniciar el sandbox.

### 7a · Qué presets hay

```bash
nemoclaw my-assistant policy list
```

Esperado: los activos con `●` y su origen, y una lista larga de disponibles con `○`. En el laboratorio de prueba estaban activos `brew-balanced`, `huggingface`, `npm`, `pypi [user-added]` y `openclaw-pricing [from openclaw agent]`; entre los disponibles, `github`, `slack`, `telegram`, `discord`, `whatsapp`, `teams`, `tavily`, `observability-otlp-local`, `personal-open-internet` y más.

### 7b · El preset propio del proyecto *Soporte NemoClaw*

Crea el archivo en la VM TERMINAL (es el mismo que generas en el notebook):

```bash
cat > ~/soporte-docs.yaml <<'EOF'
preset:
  name: soporte-docs
  description: "Lectura de la documentación de NemoClaw"
network_policies:
  soporte_docs:
    name: soporte_docs
    endpoints:
      - host: docs.nvidia.com
        port: 443
        protocol: rest
        enforcement: enforce
        rules:
          - allow: { method: GET, path: "/nemoclaw/**" }
    binaries:
      - { path: /usr/local/bin/openclaw }
      - { path: /usr/local/bin/node }
EOF
```

Lleva `node` porque el agente sale a la red con `node` (lo viste en el registro de la clase 5.2).

Ensayo, sin aplicar:

```bash
nemoclaw my-assistant policy add --from-file ~/soporte-docs.yaml --dry-run
```

Esperado: imprime la política `soporte_docs` (host `docs.nvidia.com`, `allow GET /nemoclaw/**` y los dos programas), el aviso `Warning: custom preset targets are not vetted. Review hosts before applying.` y al final `--dry-run: 'soporte-docs' not applied.`

Aplícalo y compruébalo:

```bash
nemoclaw my-assistant policy add --from-file ~/soporte-docs.yaml --yes
nemoclaw my-assistant policy list
nemoclaw my-assistant agent -m "Usa la documentación en https://docs.nvidia.com/nemoclaw/latest/ para explicar en dos líneas qué es un preset de política."
nemoclaw my-assistant logs --tail 300 | grep DENIED | grep docs.nvidia.com
```

Esperado: `Applied preset: soporte-docs`; en la lista, `● soporte-docs [user-added] — custom OpenShell policy`; el agente responde en dos líneas; y el último comando no imprime nada (ninguna negación para `docs.nvidia.com`).

Quítalo:

```bash
nemoclaw my-assistant policy remove soporte-docs --yes
```

Esperado:
```text
Endpoints that would be removed: docs.nvidia.com
Narrowing sandbox egress — removing: docs.nvidia.com
Removed preset: soporte-docs
```

Opcional: `nemoclaw my-assistant policy explain --write` debería actualizar `/sandbox/.openclaw/workspace/POLICY.md`, el resumen que el agente lee sobre su propia política. Si tu versión no acepta esa opción, sáltalo.

**Si falla**
- `--dry-run` rechaza el preset: revisa que `preset.name` esté en minúsculas, que el host no sea `*` y que no uses `allowed_ips`. El notebook valida estas reglas con `validar_preset()`.
- El agente sigue sin poder abrir la página: busca la negación en el registro y copia al preset la ruta **exacta** del programa que aparece ahí.
- No quites `binaries` para "que funcione": entonces cualquier proceso del sandbox podría usar ese destino.

### 7c · Opcional: un preset de la lista (`github`)

Si quieres ver un preset ya escrito, prueba `github` y quítalo al final. Este no se repitió en la prueba del laboratorio: lee lo que imprime cada paso.

```bash
nemoclaw my-assistant policy add github --dry-run
nemoclaw my-assistant policy add github --yes
openshell sandbox exec -n my-assistant -- sh -c 'git ls-remote https://github.com/NVIDIA/NemoClaw | head -1'
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://github.com
nemoclaw my-assistant policy remove github --yes
```

Fíjate en el ensayo: ¿qué programas lista el preset? Si solo lista `git`, `curl` hacia `github.com` debería seguir bloqueado aunque el preset esté aplicado. Es la misma idea de la clase 5.2: el permiso va atado al programa. Al final, `policy list` no debe mostrar `github` activo.

### Qué se cambia en caliente y qué no

| Sección | ¿En caliente? | Cómo se cambia |
|---|---|---|
| `network_policies` | Sí | `nemoclaw … policy add/remove`, la OPENSHELL TUI (temporal), `openshell policy set` |
| Inferencia | Sí | `nemoclaw inference set …` |
| `filesystem_policy`, `landlock` | No | Editar la política base y volver a crear el sandbox (`nemoclaw onboard`) |
| `process` | No | Igual: se fija al crear el sandbox |

## 8 · Cierre: un secreto impreso por un comando permitido ya se escapó

Demostración segura con un secreto **falso**:

```bash
openshell sandbox exec -n my-assistant -- sh -c 'echo "TOKEN_DEMO=no-es-real-123" > /tmp/secreto-demo.txt'
nemoclaw my-assistant agent -m "Lee /tmp/secreto-demo.txt y dime exactamente qué dice."
openshell sandbox exec -n my-assistant -- rm /tmp/secreto-demo.txt
```

Si el agente lo lee, responde con `TOKEN_DEMO=no-es-real-123`. Leer `/tmp` está permitido y hablar con el modelo también. Ese texto ya viajó al proveedor de inferencia y quedó en la sesión. Ninguna regla posterior lo regresa.

**Si falla**
- El agente se niega a leer el archivo: bien por su prompt, pero no cuentes con ello. Corre `cat` con `openshell sandbox exec`: lo que imprime un comando permitido ya salió del sandbox hacia quien lo ejecutó.
