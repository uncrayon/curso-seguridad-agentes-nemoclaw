# 2.3 · Convierte funciones en herramientas

Objetivo: convertir funciones de Python en herramientas que el modelo usa bien, con argumentos validados y errores que el agente puede corregir.

| | |
|---|---|
| **Duración del video** | ≈9 min |
| **Práctica** | Notebook (≈50 min), funciona sin key en modo MOCK |
| **Habilidad** | Convertir funciones en herramientas de agente |
| **Material** | [Diapositivas](slides.html) · [Notebook](2.3-funciones-a-herramientas.ipynb) · [Preguntas frecuentes](../../FAQ.md) |

## Lo esencial (sin tecnicismos)

**La idea:** el modelo elige qué herramienta usar leyendo solo su ficha: nombre, descripción y datos que pide. Si la descripción es mala, elige mal. Y como el modelo a veces pide cosas incorrectas o peligrosas, tu programa revisa cada pedido y solo ejecuta las herramientas que tú permitiste.

**Piénsalo como:** la ventanilla de un trámite, con un letrero que dice cómo se llama, para qué sirve, qué papeles pide y qué te entregan. Un subagente es como un jefe de proyecto que reparte encargos a su equipo, y MCP es una tienda de apps de otra empresa: tú decides cuáles instalas.

**Palabras nuevas:** contrato de una herramienta (su ficha: nombre, descripción, datos que pide y resultado en texto), [subagente](../../GLOSARIO.md), MCP (un estándar para descubrir herramientas que viven en otro servidor).

**Hazlo sin programar (≈10 min):** descarga el notebook de esta clase, súbelo a [Colab](https://colab.research.google.com/) con **Archivo → Subir notebook** y presiona ▶ en cada celda, en orden, sin leer el código (o usa **Entorno de ejecución → Ejecutar todo**) (sin key funciona con respuestas simuladas). Luego responde:

1. En la sección 4, ¿qué herramienta eligió el modelo para cada una de las tres preguntas?
2. En la sección 5, ¿qué pasó cuando el modelo pidió `borrar_instancia`, una herramienta que no está en la lista?
3. En la sección 9, ¿qué herramienta rechazó la lista de permitidas y qué frase sospechosa tenía su descripción?

Extra: escribe en español normal la descripción de una herramienta que te gustaría darle a un asistente, diciendo cuándo usarla y cuándo no.

**Qué te llevas:** sabes que una buena descripción guía al agente y que la lista de herramientas permitidas la decides tú, no el modelo ni un servidor ajeno.

## Lo que vas a lograr

- Generar el contrato de una herramienta (nombre, descripción, esquema) desde la firma y el docstring de una función.
- Validar argumentos con JSON Schema escrito a mano y devolver cada error como una observación que el modelo puede corregir.
- Darle a Soporte NemoClaw sus primeras herramientas reales, `buscar_faq` y `estimar_costo_brev`, y saber cuándo usar un subagente o un servidor MCP (y qué riesgo trae).

## Antes de empezar

- Haber terminado la clase 2.2: tienes un loop ReAct con validación y tope de pasos.
- Python 3.10+ o Colab, y tu key `nvapi-` (opcional: sin key corre en MOCK).
- Si corres el notebook desde el repo, carga la FAQ completa de `datos/faq/`. En Colab usa una muestra incrustada de 9 preguntas; las dos opciones sirven.

## Paso a paso

### 1. Abre el notebook y ejecuta la configuración

```bash
source .venv/bin/activate
jupyter lab clases/2.3-funciones-a-herramientas/2.3-funciones-a-herramientas.ipynb
```

Ejecuta las dos primeras celdas y la del simulador.

### 2. Carga la FAQ (sección 2)

Ejecuta la celda de `cargar_faq`. Deberías ver una de estas dos líneas:

```text
FAQ completa: 61 entradas de 9 archivos en datos/faq/
FAQ de muestra incrustada: 9 entradas (no encontré datos/faq/)
```

(El número exacto de entradas depende de la versión del repo). El formato de cada archivo es `# Tema`, luego `## P: pregunta` y la respuesta debajo.

### 3. Convierte funciones en herramientas (sección 3)

Lee el decorador `@herramienta` y las dos funciones del proyecto. Ejecuta la celda.

Deberías ver la entrada de la FAQ sobre el error 401, el cálculo `72 h × $0.15/h ≈ $10.80 USD de cómputo...` y el JSON del esquema de `estimar_costo_brev`, con `"type": "number"`, `"minimum": 0.1` y `"additionalProperties": false`. Ese JSON es lo único que ve el modelo.

### 4. Mira cómo elige el modelo (sección 4)

Ejecuta la celda de `PREGUNTAS`. Deberías ver:

```text
👤 ¿Qué hago si me sale error 401?
   → [('buscar_faq', '{"consulta": "..."}')]
👤 ¿Cuánto me cuesta dejar Brev prendido 10 horas a 0.15 la hora?
   → [('estimar_costo_brev', '{"horas": 10.0, "tarifa_hora": 0.15}')]
👤 Hola, ¿cómo estás?
   → (responde sin herramienta)
```

Con tu key, haz el **✏️ Tu turno**: cambia la descripción de `buscar_faq` por `"Herramienta 1."`, vuelve a ejecutar `PREGUNTAS` y compara. Luego restaura la descripción ejecutando otra vez la celda de la sección 3.

### 5. Valida argumentos y rompe cosas a propósito (sección 5)

Ejecuta `validar_args` y `ejecutar`, y después la celda de `casos`. Deberías ver seis errores en texto, por ejemplo:

```text
estimar_costo_brev({"horas": "tres días", "tarifa_hora": 0.15})
   → ERROR de validación: 'horas' debe ser number, llegó str ('tres días'). Corrige los argumentos y vuelve a llamar.
borrar_instancia({"nombre": "mi-lab"})
   → ERROR: la herramienta 'borrar_instancia' no existe o no está permitida. Usa una de: [...]
```

Ninguno lanza una excepción. Y fíjate en `borrar_instancia`: el modelo puede pedir cualquier nombre, pero solo se ejecuta lo que está en tu registro.

### 6. Corre Soporte NemoClaw con herramientas reales (sección 6)

Ejecuta la celda de `agente` con las tres preguntas. En la de "tres días" deberías ver la recuperación:

```text
🔧 estimar_costo_brev({"horas": "tres días", ...}) → ERROR de validación: 'horas' debe ser number...
🔧 estimar_costo_brev({"horas": 72, "tarifa_hora": 0.15}) → 72 h × $0.15/h ≈ $10.80 USD...
```

El modelo leyó el error y corrigió. En vivo, muchos modelos mandan `72` a la primera; el harness te protege para cuando no.

### 7. Cambia el backend sin tocar el loop (sección 7)

Ejecuta la celda de `buscar_faq_semantica`. Cambia el registro a la versión con embeddings (`nvidia/nemotron-3-embed-1b`), corre el agente y regresa al backend original. El esquema no cambió y el modelo no se entera.

Con tu key, prueba preguntas con sinónimos ("mi llave", "no la acepta") y compara los dos backends.

### 8. Esconde un subagente detrás de una herramienta (sección 8)

Ejecuta la celda de `consultar_experto_brev`. Deberías ver `↳ principal → subagente: ...` y `↳ subagente → principal: ...`: el agente principal solo ve una herramienta; el subagente tiene su propio prompt y solo `estimar_costo_brev`.

### 9. Descubre herramientas con MCP y fíltralas (sección 9)

Ejecuta las dos celdas del `ServidorMCPSimulado`. Deberías ver:

```text
✅ faq_curso: aceptada
🚫 sincronizar_notas: rechazada · fuera de la lista blanca=True · alertas=['api key', 'antes de responder', 'historial completo']
```

`tools/list` devolvió una herramienta con una instrucción escondida en la descripción. Tu lista blanca la rechazó antes de que el modelo la leyera.

## Comprueba que funcionó

- [ ] `json.dumps(TOOLS[1])` muestra el esquema de `estimar_costo_brev` con tipos, límites y descripciones.
- [ ] Los seis `casos` devuelven un `ERROR ...` en texto, sin excepción.
- [ ] Soporte NemoClaw cita la FAQ (tema y pregunta) y se recupera del error de "tres días".
- [ ] Cambiaste el backend de `buscar_faq` sin tocar `agente` ni el esquema.
- [ ] Puedes explicar por qué `tools/list` es una entrada no confiable.

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `FAQ de muestra incrustada: 9 entradas (no encontré datos/faq/)` y esperabas la FAQ completa | Abriste el notebook en Colab o desde otra carpeta | Es normal en Colab. En tu máquina, abre el notebook desde `clases/2.3-funciones-a-herramientas/`. Ver [FAQ: notebooks](../../FAQ.md#notebooks) |
| El modelo responde de memoria y nunca llama a `buscar_faq` | La descripción no dice cuándo usarla o el system prompt no prohíbe adivinar | Escribe en la descripción **cuándo** usarla ("para cualquier duda sobre…") y en el system prompt "nunca inventes datos" |
| `ERROR de validación: 'horas' debe ser number, llegó str ('tres días')` una y otra vez | El modelo no entiende el formato | Pon un ejemplo en la descripción del parámetro ("72 para 3 días"); el tope de pasos evita el loop infinito |
| `Sin resultados en la FAQ para '...'` | La búsqueda por palabras no encontró coincidencias (sinónimos, errores de dedo) | Prueba otras palabras o el backend semántico de la sección 7. El agente debe decir que no lo encontró, no adivinar |
| `KeyError: 'buscar_faq'` o `StopIteration` en `ejecutar` | Ejecutaste las celdas fuera de orden y `TOOLS` o `REGISTRO` quedaron vacíos | Vuelve a ejecutar la celda de la sección 3 (el decorador reinicia `TOOLS` y `REGISTRO`) |
| `RuntimeError: 422 · Argumentos con formato incorrecto ...` en embeddings | Llamaste a `client.embeddings.create` sin `input_type` | Usa el helper `embed(textos, input_type="query" o "passage")`, que ya lo agrega |
| `RuntimeError: 400 · Solicitud inválida: ...` al enviar las tools | Un esquema mal formado (por ejemplo, un tipo que no existe) | Imprime `json.dumps(TOOLS, indent=2)` y revisa tipos (`string`, `number`, `integer`, `boolean`) y `required` |

## Reto: una herramienta con `enum`

Agrega `tarifa_instancia(tipo: str)` con un `enum` de tres tipos (`"2 vCPU / 4 GB"`, `"4 vCPU / 16 GB"`, `"8 vCPU / 32 GB"`) que devuelva una tarifa de referencia por hora. Toma los valores de la [página de precios de launchables de NVIDIA](https://www.nvidia.com/en-us/launchables/pricing) y anota la fecha en que los consultaste.

**Criterio de éxito** (en vivo): con `tools_de("buscar_faq", "estimar_costo_brev", "tarifa_instancia")`, la pregunta "¿Cuánto me cuesta usar 8 horas una instancia de 4 vCPU / 16 GB?" produce **dos** llamadas en orden (`tarifa_instancia` y luego `estimar_costo_brev`) y un número final correcto. Además, `tarifa_instancia` con un tipo fuera del `enum` devuelve un `ERROR de validación`, no una excepción.

## Avance del proyecto

**Soporte NemoClaw v3: herramientas reales.** Ahora responde con la FAQ del curso (`buscar_faq`, con cita de tema y pregunta) y calcula costos de Brev (`estimar_costo_brev`), con argumentos validados y errores que se corrigen solos. También sabes delegar en un subagente (`consultar_experto_brev`) y filtrar herramientas descubiertas por MCP.

Agrega a tu `soporte_nemoclaw.py` el decorador `herramienta`, `validar_args`, `ejecutar`, `agente` y las dos herramientas. En la clase 3.1 le pones un router de triage con las categorías `instalacion | api_key | brev | seguridad | otro`.

## Recursos

- Lección 01c · Herramientas a escala, curso de NVIDIA DLI en español. Esta clase está basada en ella (Apache-2.0).
- [Especificación de MCP (Model Context Protocol)](https://modelcontextprotocol.io/specification) y su guía de [buenas prácticas de seguridad](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices).
- [Especificación de JSON Schema](https://json-schema.org/specification).
- Schick et al. (2023), [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761).
- [Precios de los launchables de NVIDIA](https://www.nvidia.com/en-us/launchables/pricing) (para `estimar_costo_brev`) y la [FAQ de Brev del curso](../../FAQ.md#brev).
