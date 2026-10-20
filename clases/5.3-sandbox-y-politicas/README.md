# 5.3 · Restringe herramientas, archivos y red

Lee la política real de tu sandbox, predice qué permite y qué bloquea, compruébalo en vivo y cámbiala con los comandos de NemoClaw.

| | |
|---|---|
| Duración del video | ≈9 min |
| Práctica | Laboratorio en Brev ([`cookbook.md`](cookbook.md)) + [notebook](5.3-sandbox-y-politicas.ipynb) |
| Habilidad | Definir y verificar un sandbox en OpenShell |
| Lección de NVIDIA | [04a · El sandbox de OpenShell](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/04a-safety.html) (política activa, mapa y "Veredicto estático frente al sandbox activo") |

Material: [diapositivas](slides.html) · [cookbook del lab](cookbook.md) · [notebook](5.3-sandbox-y-politicas.ipynb) · [FAQ del curso](../../FAQ.md)

## Lo esencial (sin tecnicismos)

**La idea:** El sandbox obedece una lista de reglas escritas: qué carpetas puede leer, dónde puede escribir y a qué sitios puede salir cada programa. Puedes leer esa lista, adivinar qué va a pasar y comprobarlo. Y aun con buenas reglas, un secreto que el agente lee con permiso puede escaparse: el sandbox es una capa, no la solución completa.

**Piénsalo como:** el reglamento del guardia en la puerta.

**Palabras nuevas:** [política](../../GLOSARIO.md), preset (un paquete de reglas ya escrito que se agrega a la política, como una hoja extra que engrapas al reglamento).

**Hazlo sin programar (≈10 min):** Antes de ver resultados, escribe "permitido" o "bloqueado" junto a cada petición: 1) el agente (programa `openclaw`) abre `docs.openclaw.ai`; 2) el programa `curl` abre la misma página; 3) `curl` abre `example.com`; 4) el agente crea un archivo en la carpeta temporal `/tmp`; 5) el agente crea un archivo en la carpeta del sistema `/etc`; 6) el agente cambia su propia personalidad (`SOUL.md`); 7) el agente lee un archivo con un secreto y te dice qué contiene. Después compara con la [lección 04a](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/04a-safety.html) (elige un escenario y presiona **Predecir** y luego **Confirmar**) o con el [notebook](5.3-sandbox-y-politicas.ipynb) en Colab, presionando ▶. (Respuestas: permitidos 1, 4, 6 y 7; bloqueados 2, 3 y 5. El 6 y el 7 son la sorpresa: por eso el sandbox es solo una capa.)

**Qué te llevas:** Puedes leer las reglas de un agente y decir, antes de probarlo, qué puede y qué no puede hacer, y qué riesgo queda aunque las reglas estén bien.

**Tu crédito:** esta práctica usa ≈25 min de instancia encendida `[VERIFICAR EN LAB]`. Al terminar, detén la instancia (ver [LABORATORIO.md](../../LABORATORIO.md)).

## Lo que vas a lograr

- Leer el YAML real de OpenShell (`filesystem_policy`, `landlock`, `process`, `network_policies`) y explicar cada sección.
- Predecir y comprobar bloqueos de red y de archivos, y leer un bloqueo en el log o en `openshell term`.
- Agregar y quitar un preset en caliente, escribir el preset de *Soporte NemoClaw* y explicar por qué el sandbox es solo una capa.

## Antes de empezar

- Laboratorio de Brev encendido y sano (`nemoclaw my-assistant status` en verde).
- Hiciste la clase 5.2: sabes usar `openshell sandbox exec -n my-assistant -- …`.
- Tienes tu hoja `trifecta.md` (5.1) con la sección "Identidad" (5.2).
- Para el notebook: Python 3.10+ o Colab. No necesita API key ni PyPI extra: si tienes PyYAML lo usa, si no, usa un dict equivalente.

## Paso a paso

### 1. Lee la política real

En el host del lab:

```bash
openshell policy get my-assistant --full
```

Deberías ver un encabezado de estado, `---` y el YAML. Este es un extracto de la política base de OpenClaw en NemoClaw (`nemoclaw-blueprint/policies/openclaw-sandbox.yaml`):

```yaml
filesystem_policy:
  include_workdir: true
  read_only: [/usr, /lib, /proc, /dev/urandom, /app, /etc, /var/log, /var/lib/dpkg]
  read_write: [/tmp, /dev/null, /dev/pts, /sandbox/.openclaw, /sandbox/.nemoclaw, /home/linuxbrew]
landlock:
  compatibility: best_effort
process:
  run_as_user: sandbox
  run_as_group: sandbox
network_policies:
  openclaw_docs:
    name: openclaw_docs
    endpoints:
      - host: docs.openclaw.ai
        port: 443
        protocol: rest          # el proxy inspecciona cada petición HTTP
        enforcement: enforce
        rules:
          - allow: { method: GET, path: "/**" }
    binaries:
      - { path: /usr/local/bin/openclaw }
```

Léelo así:
- **Red**: todo está cerrado salvo los grupos de `network_policies`. Cada grupo une **destinos** (host, puerto, método, ruta) con **binarios**.
- **Archivos**: Landlock deja leer `read_only`, leer y escribir `read_write` y `/sandbox`. Todo lo demás se niega.
- **Proceso**: corre como `sandbox`. seccomp no aparece en este YAML: lo aplica OpenShell siempre.

En la página 04a, lo mismo es la celda **"Lee la política activa del launchable"** (`helpers.policyGet()`), que además dibuja el mapa.

### 2. Practica en el notebook: predecir → evaluar → puntuar

Abre [`5.3-sandbox-y-politicas.ipynb`](5.3-sandbox-y-politicas.ipynb). Usa la política real en su formato de OpenShell y un evaluador en Python (versión simplificada del que usa la página de NVIDIA). Escribe tus predicciones para 12 acciones y ejecuta:

```text
✗ d curl → API de NVIDIA (binario equivocado)  predijiste ALLOW → DENY  | el binario '/usr/bin/curl' no está permitido en 'nvidia'
✗ i ESCRIBIR SOUL.md (la persona)              predijiste DENY  → ALLOW | … está bajo read_write /sandbox/.openclaw
Puntaje: 7/12
```

Las filas ✗ son la lección: el permiso va **atado al binario**, las reglas L7 frenan métodos y la política **no** protege `SOUL.md`.

### 3. Compruébalo en el sandbox

El simulador predice; el sandbox decide. Corre las recetas 3 y 4 del [cookbook](cookbook.md):

```bash
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://inference.local/v1/models
openshell sandbox exec -n my-assistant -- curl -sS -m 8 -o /dev/null -w 'code=%{http_code}\n' https://example.com
openshell sandbox exec -n my-assistant -- ls /var/lib/apt/lists
```

Deberías ver: la primera sin `CONNECT tunnel failed`; la segunda con `curl: (56) CONNECT tunnel failed, response 403`; la tercera con `Permission denied`.

Si una predicción no coincide, revisa tres cosas antes de concluir: la política **activa** (no la del notebook), el **binario** real y **quién** respondió (¿el proxy o el servidor?).

### 4. Lee un bloqueo

```bash
nemoclaw my-assistant logs --tail 50
```

Busca la denegación: binario, host:puerto y motivo. Para verla en vivo y decidir, abre `openshell term` en otra terminal (receta 6): `Enter` en tu sandbox, `r` para **Network Rules**, `Enter` para ver el detalle, `x` para rechazar.

### 5. Cambia la política en caliente

```bash
nemoclaw my-assistant policy add github --dry-run
nemoclaw my-assistant policy add github --yes
openshell sandbox exec -n my-assistant -- sh -c 'git ls-remote https://github.com/NVIDIA/NemoClaw | head -1'
nemoclaw my-assistant policy remove github --yes
```

La red y la inferencia cambian **en caliente**. El filesystem y el proceso se fijan al crear el sandbox: para cambiarlos hay que editar la política base y recrearlo.

### 6. El cierre: el sandbox es una capa

En el notebook (sección 9) la FAQ envenenada de la 5.1 ataca a *Soporte NemoClaw* con la política real: el `curl` al host del atacante se bloquea, pero el envío desde el runtime del agente a `clawhub.ai` (un host permitido que acepta `POST`) **pasa**. Y la receta 8 del cookbook lo muestra en vivo con un secreto falso: un secreto impreso por un comando permitido ya se escapó.

## Comprueba que funcionó

- [ ] Guardaste tu política con `openshell policy get my-assistant --full > ~/politica-antes.txt`.
- [ ] Puedes señalar en el YAML dónde está cada una de las cuatro preguntas (red, archivos, proceso; seccomp va aparte).
- [ ] Tu puntaje en el notebook subió después de leer las filas ✗.
- [ ] Viste en vivo un `CONNECT tunnel failed, response 403` y un `Permission denied`, y los encontraste en el log.
- [ ] Agregaste y quitaste el preset `github` sin reiniciar nada.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `curl: (56) CONNECT tunnel failed, response 403` | El proxy de OpenShell negó la conexión: host fuera de la política o binario no permitido | No es TLS ni DNS. `nemoclaw my-assistant logs --tail 50` y revisa el grupo con `openshell policy get my-assistant --full` |
| `code=403` **sin** "CONNECT tunnel failed" | La conexión pasó y respondió el servidor (o una regla L7) | Identifica la fuente antes de culpar al sandbox. Mira el log |
| Agregaste el preset y el agente sigue bloqueado | El preset no incluye el binario que realmente abre la conexión (p. ej. `node` y no `openclaw`) | Copia la ruta exacta del binario desde `openshell term` o del log a tu preset |
| `DENIED /usr/local/bin/node -> registry.npmjs.org:443 reason: binary '/usr/local/bin/node' not allowed in policy 'npm_registry'` | El grupo base `npm_registry` solo permite a `openclaw` | Si de verdad lo necesitas: `nemoclaw my-assistant policy add npm --dry-run`, revísalo y aplícalo |
| `ls /var/lib/apt/lists` sí funciona | Landlock en `best_effort` sobre un kernel sin soporte (aviso `⚠ Landlock: … does not support Landlock (requires ≥5.13)`) | Revisa `uname -r` dentro del sandbox. La red y seccomp siguen activos |
| En `openshell term` ves `upstream_unreachable` | La política coincidió, pero el host no respondió | No abras más la política: revisa el host, DNS o el proxy corporativo |
| Agregaste un endpoint con `openshell term` y "desapareció" | Las aprobaciones viven solo en esa instancia del sandbox; al recrearlo vuelve la política base | Para que dure, usa un preset (`policy add`) |
| El notebook dice "Sin PyYAML" | No tienes PyYAML instalado | No pasa nada: usa el dict equivalente. Es el mismo contenido |

## Reto

En el notebook (sección 🏁), completa `PRESET_RETO` para que *Soporte NemoClaw* pueda leer `docs.nvidia.com/nemoclaw/**` y la portada de `build.nvidia.com` solo con `GET`, sin abrir nada a `curl`. **Criterio de éxito:** `probar_reto(PRESET_RETO)` da **6/6** y `nemoclaw my-assistant policy add --from-file … --dry-run` lo acepta en el lab.

## Avance del proyecto

Cierra el módulo con la política de *Soporte NemoClaw*:

1. Guarda `soporte-docs.yaml` (receta 7e) junto a la skill `soporte-nemoclaw` en tu repo.
2. Agrega a tu `trifecta.md` una sección **"Política (clase 5.3)"**: qué grupos usa el proyecto, qué preset propio agregaste y qué canal de salida **sigue abierto** (el proveedor de inferencia y `clawhub.ai`).
3. Corre `nemoclaw my-assistant policy explain --write` para que el agente conozca su política y pueda explicar a un estudiante por qué no puede abrir un sitio.

En la clase 6.2 vas a empaquetar esto como parte de tu biblioteca de skills.

## Recursos

- NVIDIA DLI · [04a · El sandbox de OpenShell](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/04a-safety.html) (Apache-2.0).
- NemoClaw · política base [`openclaw-sandbox.yaml`](https://github.com/NVIDIA/NemoClaw/blob/main/nemoclaw-blueprint/policies/openclaw-sandbox.yaml), [presets](https://github.com/NVIDIA/NemoClaw/tree/main/nemoclaw-blueprint/policies/presets) y [tiers](https://github.com/NVIDIA/NemoClaw/blob/main/nemoclaw-blueprint/policies/tiers.yaml).
- NemoClaw · [Referencia de comandos](https://docs.nvidia.com/nemoclaw/latest/) → `policy add`, `policy list`, `policy remove`, `policy explain`, `logs`.
- NemoClaw · *Approve or Deny Network Requests* (`openshell term`) y *Create Custom Policy Presets*.
- OpenShell · [Esquema de políticas](https://docs.nvidia.com/openshell/latest/reference/policy-schema.html).
- [FAQ del curso](../../FAQ.md).

---
Basado en la lección 04a-safety del curso de NVIDIA DLI (Apache-2.0) y en `nemoclaw-blueprint/policies/` de NVIDIA/NemoClaw (Apache-2.0).
