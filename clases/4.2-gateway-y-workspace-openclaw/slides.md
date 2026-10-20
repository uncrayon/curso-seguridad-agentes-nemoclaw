## Las tres piezas de OpenClaw

:::diagrama c42-edificio

Notas:
El edificio de oficinas. Clic 1: tú escribes. Clic 2: la recepción (gateway) recibe cada turno y guarda las conversaciones. Clic 3: el cuarto con cerradura y el asistente adentro. Clic 4: su escritorio (workspace). Clic 5: la idea de la clase, el directorio es la configuración. Hay dos gateways: el de OpenShell en el host (8080, solo local, ciclo de vida del sandbox) y el de OpenClaw dentro del sandbox (18789, el agente). Hoy hablamos del de OpenClaw.

---

## El workspace, archivo por archivo

:::diagrama c42-escritorio

Notas:
Clic 1: SOUL.md, el reglamento y la descripción del puesto. Clic 2: AGENTS.md, USER.md y TOOLS.md. Clic 3: HEARTBEAT.md y la carpeta skills (clase 4.3). Clic 4: la memoria en dos niveles, memory/ y MEMORY.md. Clic 5: lo relee al empezar cada conversación. También están IDENTITY.md (nombre, emoji) y POLICY.md (resumen de la política, lo escribe NemoClaw). MEMORY.md y memory/ se crean la primera vez que el agente guarda memoria.

---

## Memoria en dos niveles

:::diagrama c42-memoria

Notas:
Clic 1: la conversación vive en la recepción y se pierde al reiniciar la sesión (sessions.reset). Clic 2: los archivos, notas del día en memory/AAAA-MM-DD.md. Clic 3: lo importante pasa a MEMORY.md. Clic 4: los archivos sobreviven al reinicio. Por defecto MEMORY.md entra al contexto de la sesión principal, no a todas; que no esté en contexto no impide leerlo. Inspirado en MemGPT.

---

## Dos planos de autoridad

:::diagrama c42-planos

Notas:
Clic 1: el cuarto, con el agente adentro (usuario sandbox, política más estrecha); solo puede contar lo que hizo. Clic 2: el operador, afuera, con la terminal de la máquina. Clic 3: el operador lee los archivos directamente (openshell sandbox connect, nemoclaw … exec, cat). Clic 4: la regla. Esta separación es la base del Módulo 5: un agente que reescribe su propio workspace puede influir en sus ejecuciones futuras.

---

## Verifica como operador

:::diagrama c42-dice-vs-archivo

Notas:
Clic 1: lo que el agente dice de sí mismo (Paso 1 de la 03b). Clic 2: lo que muestra la celda de operador (Paso 1b, "Lee el workspace en vivo en la terminal del operador"). Clic 3: compara. El ejemplo es a propósito: el agente menciona MEMORY.md, que todavía no existe, y olvida USER.md. Los comandos están en la diapositiva "Si prefieres la terminal".

---

## El agente edita su memoria

:::diagrama c42-dos-sesiones

Notas:
En la 03b: flujo "Verifica la memoria en archivos entre sesiones distintas", ▶ Ejecutar todo. Clic 1: la conversación A pide agregar una preferencia a MEMORY.md sin borrar lo demás. Clic 2: la celda no le cree y lee el archivo. Clic 3: una conversación nueva la encuentra en el disco. Clic 4: la regla. La celda falla si la lectura del archivo no contiene la preferencia.

---

## Personaliza SOUL.md

:::diagrama c42-soul

Notas:
Clic 1: la sección "Proyecto: Soporte NemoClaw", escrita en español normal (es la actividad sin programar). Clic 2: se agrega al final de SOUL.md, en el escritorio. Clic 3: en una conversación nueva, el agente ya conoce su puesto. Clic 4: el workspace se lee al inicio de cada conversación; una ya abierta no cambia.

---

## Cuidado con la tilde

:::diagrama c42-tilde

Notas:
El error en vivo. Clic 1: le pides al agente que agregue la sección a ~/SOUL.md. Clic 2: dentro del cuarto, ~ es /sandbox: se escribe un archivo suelto que nadie lee. Clic 3: con la ruta completa (/sandbox/.openclaw/workspace/SOUL.md) llega al reglamento de verdad. Clic 4: pide siempre la ruta completa y verifica como operador con tail. Borra el archivo suelto con la celda de operador (rm ~/SOUL.md).

---

## Si prefieres la terminal

```bash
# Mira el escritorio del agente, como operador
openshell sandbox connect my-assistant
cd /sandbox/.openclaw/workspace && ls -la

# Agrega tu sección a SOUL.md sin depender del agente
nemoclaw my-assistant download /sandbox/.openclaw/workspace/SOUL.md ./
cp SOUL.md SOUL.md.original
cat >> SOUL.md <<'EOF'
## Proyecto: Soporte NemoClaw
- Respondes en español neutro …
EOF
nemoclaw my-assistant upload ./SOUL.md /sandbox/.openclaw/workspace/SOUL.md
```

.lead Es opcional: lo mismo que hiciste con clics y en el chat, escrito como instrucciones.

Notas:
Receta 7 del cookbook (download → cp … .original → cat >> → upload → tail). Para buscar la preferencia guardada: nemoclaw my-assistant exec -- grep -n "REF-" /sandbox/.openclaw/workspace/MEMORY.md (receta 8). Pruébalo en una conversación nueva.

---

## Errores comunes

| Ves | Haz esto |
|---|---|
| El agente dice «lo guardé» y no está | Léelo como operador y pide la ruta completa |
| Editaste `~/SOUL.md` y nada cambió | Usa el escritorio: `/sandbox/.openclaw/workspace/` |
| Una conversación abierta no cambia | Abre una conversación nueva |
| `Pairing required` en el tablero | Espera y recarga; los pasos están en la página de la clase |
| `openclaw update` se queda colgado | No lo uses: la versión viene fija |

Notas:
Pairing: Overview → Gateway Access → Connect, o openclaw devices approve (receta 9). En una instalación propia, actualizar es nemoclaw update y luego nemoclaw <nombre> rebuild. En el launchable, no tocar versiones.

---

## Avance del proyecto

.lead Tu agente ya es Soporte NemoClaw.

- En `SOUL.md`: a quién ayuda, en qué idioma responde y qué nunca hace
- En `MEMORY.md`: una preferencia, comprobada en el archivo
- Repite la pregunta del 401 de la clase 4.1 y anota qué cambió

Le falta conocimiento: en la clase 4.3 llega la skill con la FAQ.

Notas:
Guardar la sección en proyecto/SOUL-soporte.md. La preferencia de memoria del proyecto es soporte-pref-01: citar el archivo de la FAQ.
