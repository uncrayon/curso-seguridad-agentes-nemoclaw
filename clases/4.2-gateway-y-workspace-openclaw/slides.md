## Las tres piezas de OpenClaw

:::diagrama c42-edificio

Notas:
El edificio de oficinas. Clic 1: tú escribes. Clic 2: la recepción (gateway) recibe cada turno y guarda las conversaciones. Clic 3: el cuarto con cerradura y el asistente adentro. Clic 4: su escritorio (workspace). Clic 5: la idea de la clase, el directorio es la configuración. Hay dos gateways: el de OpenShell en el host (puerto 18080, solo local, ciclo de vida del sandbox; se ve con openshell gateway info) y el de OpenClaw dentro del sandbox (18789, el agente y su chat). Hoy hablamos del de OpenClaw.

---

## El workspace, archivo por archivo

:::diagrama c42-escritorio

Notas:
Clic 1: SOUL.md, el reglamento y la descripción del puesto. Clic 2: AGENTS.md, USER.md y TOOLS.md. Clic 3: HEARTBEAT.md y la carpeta skills (clase 4.3). Clic 4: la memoria en dos niveles, memory/ y MEMORY.md. Clic 5: lo relee al empezar cada conversación. También están IDENTITY.md (nombre, emoji) y POLICY.md (resumen de la política, lo escribe NemoClaw). En un laboratorio nuevo todavía no existen MEMORY.md, memory/ ni skills/: aparecen cuando hacen falta.

---

## Memoria en dos niveles

:::diagrama c42-memoria

Notas:
Clic 1: la conversación vive en la recepción y se pierde al reiniciar la sesión (nemoclaw my-assistant sessions reset <clave>). Clic 2: los archivos, notas del día en memory/AAAA-MM-DD.md. Clic 3: lo importante pasa a MEMORY.md. Clic 4: los archivos sobreviven al reinicio. Que algo no esté en el contexto no impide leerlo del archivo. Inspirado en MemGPT.

---

## Dos planos de autoridad

:::diagrama c42-planos

Notas:
Clic 1: el cuarto, con el agente adentro (usuario sandbox, política más estrecha); solo puede contar lo que hizo. Clic 2: el operador, afuera, con la VM TERMINAL del tablero. Clic 3: el operador lee los archivos directamente (nemoclaw my-assistant exec -- ls / cat). Clic 4: la regla. Esta separación es la base del Módulo 5: un agente que reescribe su propio workspace puede influir en sus ejecuciones futuras.

---

## Verifica como operador

:::diagrama c42-dice-vs-archivo

Notas:
Clic 1: lo que el agente dice de sí mismo, en CHAT WITH AGENT («Enumera brevemente los archivos de tu workspace…»). Clic 2: lo que muestra la VM TERMINAL con nemoclaw my-assistant exec -- ls -la /sandbox/.openclaw/workspace. Clic 3: compara. En un laboratorio nuevo la lista real es AGENTS.md, HEARTBEAT.md, IDENTITY.md, POLICY.md, SOUL.md, TOOLS.md y USER.md; si el agente menciona MEMORY.md, todavía no existe.

---

## El agente edita su memoria

:::diagrama c42-dos-sesiones

Notas:
Clic 1: la sesión memoria-a pide agregar una preferencia (REF-4821) a MEMORY.md sin borrar lo demás. Clic 2: el operador no le cree y busca la línea con grep en la VM TERMINAL. Clic 3: después de reiniciar memoria-a, una sesión nueva (memoria-b) la encuentra en el disco. Clic 4: la regla. Comandos en la Parte E del README y en la receta 8.

---

## Personaliza SOUL.md

:::diagrama c42-soul

Notas:
Clic 1: la sección "Proyecto: Soporte NemoClaw", escrita en español normal (es la actividad sin programar). Clic 2: se agrega al final de SOUL.md: la escribes en ~/soul-extra.md en la máquina, la subes a /tmp del sandbox con upload y la pegas con sh -c 'cat … >> …'. Clic 3: en una sesión nueva (soul-42), el agente ya conoce su puesto. Clic 4: el workspace se lee al inicio de cada conversación; una ya abierta no cambia.

---

## Cuidado con la tilde

:::diagrama c42-tilde

Notas:
El error en vivo. Clic 1: agregas la sección a ~/SOUL.md, dentro del sandbox. Clic 2: dentro del cuarto, ~ es /sandbox: queda un archivo suelto que nadie lee. Clic 3: con la ruta completa (/sandbox/.openclaw/workspace/SOUL.md) llega al reglamento de verdad. Clic 4: usa siempre la ruta completa y verifica como operador con tail. Borra el archivo suelto: nemoclaw my-assistant exec -- rm /sandbox/SOUL.md.

---

## Comandos de operador

```bash
# Mira el escritorio del agente
nemoclaw my-assistant exec -- ls -la /sandbox/.openclaw/workspace

# Agrega tu sección a SOUL.md sin depender del agente
nemoclaw my-assistant upload ~/soul-extra.md /tmp/
nemoclaw my-assistant exec -- sh -c 'cat /tmp/soul-extra.md >> /sandbox/.openclaw/workspace/SOUL.md'

# Pruébalo en una sesión nueva
nemoclaw my-assistant agent --session-key soul-42 -m '¿Quien eres?'
```

.lead Se pegan en la VM TERMINAL del tablero.

Notas:
Receta 5 del cookbook: ~/soul-extra.md con cat > … <<'EOF', copia de seguridad en /tmp/SOUL.md.original, upload, cat >> y tail. Dos signos >>: con uno solo se borra SOUL.md. Para ver sesiones: sessions list --json (receta 7).

---

## Errores comunes

| Ves | Haz esto |
|---|---|
| El agente dice «lo guardé» y no está | Léelo como operador y pide la ruta completa |
| Escribiste `~/SOUL.md` y nada cambió | Usa el escritorio: `/sandbox/.openclaw/workspace/` |
| Una conversación abierta no cambia | Usa una sesión nueva |
| `SOUL.md` quedó solo con tu sección | Usaste `>`: restaura la copia y usa `>>` |
| `openclaw update` se queda colgado | No lo uses: la versión viene fija |

Notas:
El chat del laboratorio ya viene emparejado: si apareciera "Pairing required", cerrar la pestaña y abrir de nuevo CHAT WITH AGENT desde el tablero. En una instalación propia, actualizar es nemoclaw update y luego nemoclaw <nombre> rebuild. En el laboratorio, no tocar versiones.

---

## Avance del proyecto

.lead Tu agente ya es Soporte NemoClaw.

- En `SOUL.md`: a quién ayuda, en qué idioma responde y qué nunca hace
- En `MEMORY.md`: una preferencia, comprobada en el archivo
- Repite la pregunta del 401 de la clase 4.1 y anota qué cambió

Le falta conocimiento: en la clase 4.3 llega la skill con la FAQ.

Notas:
Copiar la sección de SOUL.md en las notas del proyecto. La preferencia de memoria del proyecto es soporte-pref-01: citar el archivo de la FAQ. La pregunta del 401 se repite con una sesión nueva (linea-base-42).
