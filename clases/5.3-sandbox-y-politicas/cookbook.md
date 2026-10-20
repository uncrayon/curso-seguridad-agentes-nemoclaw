# Cookbook 5.3 · Leer, probar y cambiar la política del sandbox

Recetas de terminal para el laboratorio NemoClaw en Brev: leer la política real, predecir y probar bloqueos, diagnosticar una denegación y agregar o quitar permisos con los comandos reales de NemoClaw.

**Convenciones**
- `my-assistant` es el nombre del sandbox (compruébalo con `openshell sandbox list`).
- Los comandos van en el **host** del lab (`brev shell <tu-instancia>`). `openshell sandbox exec` los corre dentro del sandbox. Si usas `|`, `&&` o `>`, envuélvelos en `sh -c '...'`.
- Las recetas 1 a 5 solo leen. Las 6 y 7 **cambian** la política: cada una dice cómo deshacerlo.
- Lo marcado `[VERIFICAR EN LAB]` se confirma en la prueba previa.

---

## 1 · Lee la política real

```bash
openshell policy get my-assistant --full
```

Deberías ver un encabezado de estado, una línea `---` y después el YAML con cuatro secciones: `filesystem_policy`, `landlock`, `process` y `network_policies`. Es el mismo comando que corre `helpers.policyGet()` en la página 04a.

Guárdala para compararla después:

```bash
openshell policy get my-assistant --full > ~/politica-antes.txt
```

Otras vistas útiles:

```bash
nemoclaw my-assistant policy list       # presets activos, con su origen: [from balanced tier], [user-added]…
nemoclaw my-assistant policy explain    # resumen sin YAML, pensado para el agente
nemoclaw my-assistant status            # incluye una sección Policy con la política activa
```

Solo los nombres de los grupos de red:

```bash
openshell policy get my-assistant --full | sed -n '/^network_policies:/,$p' | grep -E '^  [a-z0-9_-]+:$'
```

**Si falla**
- Error de sandbox no encontrado: copia el nombre exacto de `openshell sandbox list`.
- En la página 04a: "Mantén el launchable abierto en otra pestaña, vuelve a ejecutar y comprueba el nombre con: openshell sandbox list". Reconéctate en 03a.
- Ves grupos que no están en el YAML del notebook (por ejemplo `pypi`, `brave` o entradas con prefijo `_provider_`): vienen del tier del launchable o del proveedor de inferencia. Es normal. `[VERIFICAR EN LAB]` cuáles trae el launchable.

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
# 3a · Permitido para curl en la política base (grupo managed_inference)
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://inference.local/v1/models

# 3b · Bloqueado: un host que no está en la política
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://example.com

# 3c · Bloqueado siempre: la dirección de metadata de la nube
openshell sandbox exec -n my-assistant -- curl -sS -m 6 -o /dev/null -w 'code=%{http_code}\n' http://169.254.169.254/latest/meta-data/

# 3d · Host permitido, binario equivocado (el grupo nvidia es para openclaw)
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://integrate.api.nvidia.com/v1/models
```

Cómo leer el resultado:

| Ves | Significa |
|---|---|
| `code=200` (o cualquier código del servidor) | La política dejó pasar la conexión. Si el código es 4xx/5xx, lo respondió el **servidor**, no el sandbox |
| `curl: (56) CONNECT tunnel failed, response 403` | El **proxy de OpenShell** negó la conexión |
| Tiempo agotado | Puede ser un bloqueo o un host caído. Revisa la receta 5 |

Esperado con la política base: 3a pasa; 3b, 3c y 3d se bloquean. `[VERIFICAR EN LAB]` 3a (qué código devuelve `inference.local` cuando el proveedor usa la ruta nativa) y 3d (el perfil nativo de NVIDIA podría permitir `curl` para su verificación).

Si tu tier es **Balanced** (el predeterminado), también deberías poder bajar índices de PyPI con curl:

```bash
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://pypi.org/simple/
```

**Si falla**
- 3b responde `code=200`: tu sandbox tiene el tier **Personal** (`personal-open-internet`), que abre todo 80/443. Revísalo con `nemoclaw my-assistant policy list`.
- Todo da 403, incluso 3a: el proxy no está sano. `nemoclaw my-assistant status` y, si hace falta, `nemoclaw my-assistant recover`.

## 4 · Predice, luego prueba: archivos

```bash
# 4a · Permitido: /var/lib/dpkg está en read_only
openshell sandbox exec -n my-assistant -- sh -c 'ls /var/lib/dpkg | head -3'

# 4b · Bloqueado: /var/lib/apt no está en la política (aunque Linux lo deje leer a cualquiera)
openshell sandbox exec -n my-assistant -- ls /var/lib/apt/lists

# 4c · Bloqueado: /etc es solo lectura
openshell sandbox exec -n my-assistant -- touch /etc/prueba-curso

# 4d · Permitido: /tmp es lectura y escritura (y lo limpiamos)
openshell sandbox exec -n my-assistant -- sh -c 'touch /tmp/prueba-curso && ls -l /tmp/prueba-curso && rm /tmp/prueba-curso'
```

Esperado: 4a lista archivos, 4b y 4c dan `Permission denied`, 4d crea y borra el archivo. `[VERIFICAR EN LAB]` 4b: es la prueba que aísla a Landlock, porque los permisos normales de Linux sí dejarían leer esa carpeta.

Y pídeselo al agente:

```bash
nemoclaw my-assistant agent -m "Dime qué usuario eres y luego intenta crear el archivo /etc/prueba-agente. Cuéntame exactamente qué error recibiste."
```

**Si falla**
- 4b sí lista archivos: Landlock está en `best_effort` y el kernel quizá no lo soporta. Corre `openshell sandbox exec -n my-assistant -- uname -r` (Landlock necesita 5.13 o más) y busca en los logs `⚠ Landlock: … does not support Landlock`.
- 4c funciona: anótalo y repórtalo. No debería.

## 5 · Lee un bloqueo

```bash
nemoclaw my-assistant logs --tail 50
```

Busca las denegaciones de las recetas 3 y 4. Una línea de denegación de red se ve parecida a esta (formato `[VERIFICAR EN LAB]`):

```text
DENIED /usr/bin/curl -> example.com:443 reason: …
```

Te dice **quién** (binario), **a dónde** (host:puerto) y **por qué** (sin endpoint, binario no permitido o regla L7).

Equivalente directo de OpenShell (ojo: aquí `-n` es el número de líneas y `--tail` **sigue** el log en vivo):

```bash
openshell logs my-assistant -n 20
```

**Si falla**
- No aparecen denegaciones: NemoClaw avisa si no pudo activar los logs de auditoría de OpenShell. Usa la receta 6 (`openshell term`), que muestra cada bloqueo en vivo.

## 6 · Aprueba o rechaza egress en vivo (`openshell term`)

Abre una **segunda** terminal en el host (`brev shell <tu-instancia>`) y lanza la TUI:

```bash
openshell term
```

1. Elige tu sandbox con `j`/`k` y pulsa `Enter`.
2. En la primera terminal, provoca un bloqueo: repite la receta 3b (`example.com`).
3. En la TUI, pulsa `r` para ir a **Network Rules**.
4. Selecciona la solicitud pendiente con `j`/`k` y pulsa `Enter` para ver host, puerto y **binario**.
5. Pulsa `x` para **rechazarla**. (`a` aprueba esa regla; `A` aprueba todas, con confirmación `y`).

En el curso practica con `x`. Una aprobación queda en la política del sandbox hasta que lo destruyas y lo vuelvas a crear; no se guarda en la política base.

En la TUI verás dos estados distintos:
- `policy_denied`: la política no coincidió. Decide si apruebas o no.
- `upstream_unreachable`: la política **sí** coincidió, pero el host no respondió. Abrir más la política no lo arregla.

**Si falla**
- `openshell term` no dibuja bien: agranda la ventana de la terminal o usa la receta 5. `[VERIFICAR EN LAB]` que la TUI funcione dentro de `brev shell`.
- Aprobaste algo por error: queda activo en esta instancia del sandbox. Anótalo y, si importa, recrea el sandbox (clase 4.1) o pide ayuda en el foro antes de tocar la política a mano.

## 7 · Agrega y quita un preset (en caliente)

Los cambios de **red** se aplican sin reiniciar el sandbox.

```bash
# 7a · Qué hay y qué abriría GitHub
nemoclaw my-assistant policy list
nemoclaw my-assistant policy add github --dry-run

# 7b · Aplícalo y pruébalo con el binario permitido (git)
nemoclaw my-assistant policy add github --yes
openshell sandbox exec -n my-assistant -- sh -c 'git ls-remote https://github.com/NVIDIA/NemoClaw | head -1'

# 7c · El mismo host con curl sigue bloqueado: el preset solo lista /usr/bin/git
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://github.com

# 7d · Deshazlo
nemoclaw my-assistant policy remove github --yes
nemoclaw my-assistant policy list
```

Esperado: después de 7b, `git ls-remote` imprime un hash y `HEAD`; 7c sigue con `CONNECT tunnel failed, response 403`; tras 7d, `github` ya no aparece.

### 7e · El preset propio del proyecto *Soporte NemoClaw*

Crea el archivo en el host (es el que generaste en el notebook):

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

nemoclaw my-assistant policy add --from-file ~/soporte-docs.yaml --dry-run
nemoclaw my-assistant policy add --from-file ~/soporte-docs.yaml --yes
nemoclaw my-assistant policy list            # aparece como [user-added]
nemoclaw my-assistant agent -m "Usa la documentación en https://docs.nvidia.com/nemoclaw/latest/ para explicar en dos líneas qué es un preset de política."
```

Para quitarlo:

```bash
nemoclaw my-assistant policy remove soporte-docs --yes
```

Opcional: actualiza el resumen que el agente lee sobre su propia política (`/sandbox/.openclaw/workspace/POLICY.md`):

```bash
nemoclaw my-assistant policy explain --write
```

**Si falla**
- `--dry-run` rechaza el preset: revisa que `preset.name` esté en minúsculas, que el host no sea `*` y que no uses `allowed_ips`. El notebook valida estas reglas con `validar_preset()`.
- El agente sigue sin poder abrir la página: mira `openshell term` o `nemoclaw my-assistant logs --tail 50` y usa la ruta **exacta** del binario que aparece ahí. `[VERIFICAR EN LAB]` si la herramienta de navegación de OpenClaw sale como `openclaw` o como `node`.
- No quites `binaries` para "que funcione": entonces cualquier proceso del sandbox podría usar ese destino.

### Qué se cambia en caliente y qué no

| Sección | ¿En caliente? | Cómo se cambia |
|---|---|---|
| `network_policies` | Sí | `nemoclaw … policy add/remove`, `openshell term`, `openshell policy set` |
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

El agente responde con `TOKEN_DEMO=no-es-real-123`. Leer `/tmp` está permitido y hablar con el modelo también. Ese texto ya viajó al proveedor de inferencia y quedó en la sesión. Ninguna regla posterior lo regresa.

**Si falla**
- El agente se niega a leer el archivo: bien por su prompt, pero no cuentes con ello. Corre `cat` con `openshell sandbox exec`: lo que imprime un comando permitido ya salió del sandbox hacia quien lo ejecutó.
