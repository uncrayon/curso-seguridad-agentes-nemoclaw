## Cuando la respuesta sale mal

:::diagrama c34-print-vs-traza

.lead Con print ves pedazos sueltos. Con una traza ves cada paso, en orden.

Notas:
El agente de la 3.3 hace unas 11 llamadas por pregunta. Si la respuesta sale mal, ¿cuál falló? Clic 1: con print, mensajes sueltos, mezclados y sin tiempos. Clic 2: con una traza, cada paso con su tiempo y su estado, como el rastreo de un paquete; ahí se ve qué herramienta llamó, qué le mandamos al modelo, qué encontró la búsqueda y dónde se rompió.

---

## Traza y span

:::diagrama c34-paquete

Notas:
Clic 1: el historial de rastreo de un paquete. Clic 2: todo el historial es la traza; cada línea es un span (inicio, fin, estado ok o error, y un padre salvo la raíz). Clic 3: lo mismo con tu agente, que se dibuja como árbol. Clic 4: los estándares; OpenTelemetry produce y envía, OpenInference le pone tipo a cada paso (AGENT, LLM, TOOL, RETRIEVER). Phoenix (Arize, código abierto) recibe trazas OTel y las muestra como árbol.

---

## Qué guarda cada paso

:::diagrama c34-tipos

Notas:
Lo que hace la celda "5 · Instrumenta las tres piezas del agente". Un clic por tipo de paso: LLM (modelo, mensajes, finish_reason, tokens), TOOL (argumentos, salida y el error si falla), RETRIEVER (cada documento con su puntaje). Clic 4: la etiqueta de tipo es la que te dice dónde mirar.

---

## Tacha los secretos antes de guardar

:::diagrama c34-tachar

Notas:
Como plumón negro en una fotocopia. Clic 1: un mensaje con una key pegada. Clic 2: redactar() la tacha. Clic 3: lo que se guarda: "nvapi-***". Clic 4: eso es lo que llega a la traza y a Phoenix. Clic 5: por qué importa. Misma regla de la clase 1.2. Todo atributo pasa por poner(), que llama a redactar().

---

## La traza de una pregunta

:::diagrama c34-arbol

.lead En Phoenix: Projects → soporte-nemoclaw → la traza → el paso que te interesa.

Notas:
La pregunta del 401. Clic 1: la raíz, el agente completo (936 ms, 3 pasos). Clic 2: el modelo pide revisar el laboratorio y la herramienta contesta. Clic 3: el modelo pide buscar en la FAQ; la búsqueda trae conexion-laboratorio.md con puntaje 0.408. Clic 4: el modelo responde (finish=stop). Cada barra muestra cuándo empezó y cuánto tardó. En Phoenix, clic en "retriever · buscar_faq" para ver documentos y puntajes.

---

## Cuatro bugs, una traza

:::diagrama c34-cuatro-bugs

Notas:
Error en vivo: los cuatro casos de la sección 9, en ese orden. Clic 1: la herramienta falla (503), ver_traza. Clic 2: el loop no termina, la misma búsqueda de la factura cinco veces hasta el tope, repeticiones. Clic 3: una cita inventada, un id que ninguna herramienta devolvió, citas_sin_respaldo. Clic 4: tardó mucho, y lo lento es la herramienta (1.5 s), no el modelo, mas_lentos.

---

## Error ≠ respuesta rota

:::diagrama c34-error-ok

Notas:
La traza de la parte a) de la sección 9. Clic 1: el paso de la herramienta en ✖, con el error exacto; el harness se lo devuelve al agente como observación. Clic 2: el agente siguió y la raíz queda en ✔. Clic 3: la respuesta dice "No pude verificar…". Es correcto, siempre que la respuesta lo diga; sin traza solo verías una respuesta incompleta.

---

## Observabilidad en el stack de NVIDIA

:::diagrama c34-nvidia

Notas:
Clic 1: para el agente que tú programas, el NeMo Agent Toolkit manda trazas con un YAML corto a Phoenix, Langfuse, LangSmith, Weave u OTel. Clic 2: para el sandbox, NemoClaw lleva sus registros: mensajes, bloqueos de OpenShell y el historial de conversaciones (nemoclaw <sandbox> logs, sessions export, openshell term). NemoClaw con Deep Agents tiene --observability, que manda trazas OTLP a un colector en el host. Clic 3: lo usas desde el Módulo 4.

---

## Si algo sale mal

| Ves | Haz esto |
|---|---|
| «Phoenix: no detectado» | Enciende Phoenix y vuelve a correr la celda que la conecta |
| No aparecen trazas nuevas | Elige el proyecto **soporte-nemoclaw** y refresca |
| Phoenix no se instala | Necesita Python 3.11 o más; o úsala con Docker |
| Tu key aparece en una traza | Guarda todo con `poner()` y agrega el patrón que faltó |

Notas:
Phoenix se enciende con phoenix serve. El patrón que faltó se agrega a _SECRETOS.

---

## Si prefieres el código y la terminal

```yaml
general:
  telemetry:
    tracing:
      phoenix: {_type: phoenix, endpoint: http://localhost:6006/v1/traces, project: soporte-nemoclaw}
```

```bash
nemoclaw <sandbox> logs              # qué pasó en el sandbox
nemoclaw <sandbox> sessions export   # el historial de conversaciones
openshell term                       # bloqueos de OpenShell, en vivo
```

.lead Es opcional: el YAML es del NeMo Agent Toolkit; los comandos los usas desde el Módulo 4.

Notas:
Para quien programa. El YAML va en la configuración del NeMo Agent Toolkit. Los comandos corren en el laboratorio de Brev, con NemoClaw instalado.

---

## Avance del proyecto

:::diagrama c34-avance

Notas:
Un clic por capacidad nueva de Soporte NemoClaw: la traza de cada respuesta, la revisión automática de citas, repeticiones y errores, y un JSON con los secretos tachados en trazas/. Clic 4: el Módulo 4. Tu agente enruta, se fundamenta, planea y ya puedes ver qué hace por dentro.
