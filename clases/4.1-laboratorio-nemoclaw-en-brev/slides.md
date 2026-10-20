## Lo que vas a levantar hoy

:::diagrama brev-laboratorio

.lead Tu oficina rentada ya trae todo: el agente, el cuarto con cerradura y el kit. El modelo corre en la nube de NVIDIA.

Notas:
Clic 1: la consola de Brev. Clic 2: tu instancia con el launchable. Clic 3: la página del curso de NVIDIA, desde donde haremos casi todo. La instancia es solo CPU porque el modelo corre afuera.

---

## Brev desde cero

:::diagrama brev-pasos

Notas:
Un clic por paso. Instancia esperada: n2d-standard-4, 4 vCPU / 16 GiB, marcada Free o ≈USD 0.15/h. VERIFICAR EN LAB. RETRY reconstruye todo el sandbox; la tarjeta roja suele ser un error visual.

---

## La cookie de sesión, con calma

:::diagrama cookie-segura

| Tu dirección contiene | Busca la cookie |
|---|---|
| `brevlab.com` | `CF_Authorization` |
| `apps.run.brev.nvidia.com` | `_pomerium` |
| `gobrev.dev` | `__Host-skybridge-brev-prd` |

Notas:
La pulsera del evento. Chrome/Edge: F12 → Application → Storage → Cookies → la dirección del launchable → doble clic en Value. Firefox: Storage → Cookies. Safari: activar funciones de desarrollador. Difuminar el valor al grabar.

---

## Las 4 pruebas

:::diagrama cuatro-rutas

.lead Si alguna sale en rojo, abre esa prueba: te dice qué hacer.

Notas:
Tu sesión = metadatos (/api/agent, entrega el token del gateway). Recepción = gateway (/cli/gateway). Terminal = /ws/terminal. Salud = /healthz. El token del gateway es una segunda credencial; lo retomamos en el Módulo 5.

---

## Control, agente y memoria

:::cols
**1 · Control**
El modelo solo
Contesta, sin herramientas
|||
**2 · Agente**
Usa una herramienta
Las filas ⚙️ y ✓ son sus acciones
|||
**3 · Memoria**
Recuerda un código
Reinicias la conversación y lo olvida
:::

.lead La conversación la guarda la recepción (el gateway), no tu navegador.

Notas:
Los archivos del workspace sobreviven al reinicio: eso es la clase 4.2.

---

## Si prefieres la terminal

```bash
brev ls                         # tus instancias y su estado
brev shell <instancia>          # entra a la máquina
nemoclaw list                   # el sandbox de tu agente
nemoclaw my-assistant status    # ¿el agente está sano?
```

.lead Es opcional: lo mismo que hiciste con clics, escrito como instrucciones.

Notas:
brev shell sin --host (issue #11534). La URL del dashboard lleva el token después de #token=: trátala como contraseña.

---

## Cuánto cuesta cada estado

:::diagrama estados-instancia

:::tip
Al terminar por hoy: consola de Brev → tu instancia → **Stop**. Al reanudar, copia una cookie nueva.
:::

Notas:
Disco: 0.0001314 USD por GB-hora mientras exista la instancia. Si no hay capacidad, Start falla y los datos quedan inaccesibles hasta que vuelva. Sin créditos, Brev pausa las instancias que se pueden detener.

---

## Si algo sale mal

| Ves | Haz esto |
|---|---|
| `OpenClaw is starting…` | Espera: reintenta solo |
| **OpenClaw ⚠** o sesión expirada | Copia una cookie nueva y prueba otra vez |
| "out of credits" con saldo | Cambia a la organización correcta en Brev |
| Tarjeta roja **RETRY** | No la toques: mira si el registro avanza |

Notas:
nemoclaw deploy ya no existe (eliminado en v0.0.117). Si un tutorial viejo lo menciona, ignorarlo. "Could not resolve hostname": receta 12 del recetario.

---

## Avance del proyecto

.lead Soporte NemoClaw ya tiene casa. Mide cómo responde hoy.

- Pregúntale: *"Un estudiante dice: 'Mi notebook responde HTTP 401'. ¿Qué le respondes?"*
- Copia la respuesta en tus notas del proyecto
- En la clase 4.3 le das la FAQ y comparas

Notas:
La línea base sin skill es la que vamos a mejorar con la FAQ del curso.
