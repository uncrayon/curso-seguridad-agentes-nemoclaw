## El contrato de una herramienta

:::diagrama c23-ventanilla

Notas:
Basado en la lección 01c de NVIDIA: "el contrato de llamada a herramientas permanece fijo". Un clic por parte de la ficha: nombre (una capacidad), descripción (cuándo usarla y cuándo no), datos que pide (el esquema: argumentos, tipos y límites) y lo que entrega (siempre texto). Clic 5: contrato fijo = puedes cambiar todo lo de adentro.

---

## De función a herramienta

:::diagrama c23-de-funcion

Notas:
Clics 1 y 2: la función y su comentario (el docstring). Clic 3: la etiqueta @herramienta (el decorador) los lee y escribe la ficha. Clic 4: el modelo elige leyendo solo la ficha. Clic 5: firma + docstring → esquema, una sola fuente de verdad. Mostrar el JSON generado: type number, minimum, additionalProperties false.

---

## Las descripciones deciden

:::diagrama c23-descripciones

Notas:
Demo: sabotear la descripción de buscar_faq ("Herramienta 1.") y repetir las tres preguntas. Clic 1: con una buena descripción, cada pregunta va a su herramienta. Clic 2: con una mala, el modelo adivina. Clic 3: la descripción es la principal superficie de prompt engineering.

---

## Valida antes de ejecutar

:::diagrama c23-filtro

Notas:
Clic 1: el pedido del modelo. Clic 2: ¿la herramienta existe y está permitida? Clic 3: ¿los argumentos son JSON válido? Clic 4: ¿cumplen el esquema? (required, type, enum, minimum, additionalProperties). Clic 5: se ejecuta dentro de try. Clic 6: todo error vuelve como texto al modelo. Clic 7: el esquema pide, el harness hace cumplir. Son 30 líneas sin dependencias; en producción, la librería jsonschema.

---

## Un error es una pista

:::diagrama c23-tres-dias

Notas:
Error en vivo de la clase. Clic 1: el modelo manda "tres días" donde va un número. Clic 2: "ERROR de validación: 'horas' debe ser number, llegó str ('tres días'). Corrige y vuelve a llamar." Clic 3: corrige a 72. Clic 4: 72 h × $0.15/h ≈ $10.80 USD de cómputo. Clic 5: el modelo lee el error y sigue; tu código no explota.

---

## Tu lista decide qué se ejecuta

:::diagrama c23-tu-lista

Notas:
Una herramienta es una puerta entre el texto del modelo y tu computadora. Clic 1: el modelo puede pedir lo que sea. Clic 2: lo que está en el registro se ejecuta. Clic 3: borrar_instancia no está: vuelve un error y no se ejecuta nada. Otros errores comunes: responde de memoria → la descripción no dice cuándo usar la herramienta; "'horas' debe ser number" en loop → pon un ejemplo en la descripción del parámetro; "Sin resultados en la FAQ" → dilo, nunca adivines; celdas fuera de orden → TOOLS vacío, re-ejecuta el decorador.

---

## Mismo contrato, otra búsqueda

:::diagrama c23-otra-busqueda

Notas:
Adelanto de RAG (clase 3.2). Clic 1: el modelo y la ficha de buscar_faq. Clic 2: antes buscaba por palabras clave. Clic 3: ahora por significado, con embeddings (nemotron-3-embed-1b): REGISTRO["buscar_faq"] = buscar_faq_semantica, y el modelo no se entera. Clic 4: si el backend nuevo es peor, el esquema no te avisa.

---

## Un subagente detrás de una herramienta

:::diagrama c23-subagente

Notas:
Clic 1: el principal solo ve consultar_experto_brev(pregunta). Clic 2: el subagente tiene su propio prompt y solo estimar_costo_brev. Clic 3: regresa solo la respuesta; sus pasos no ensucian el historial principal (separa contexto). Clic 4: no es control de acceso. Lo escalamos en la clase 3.3 con un planificador.

---

## MCP: herramientas de otro servidor

:::diagrama c23-mcp

Notas:
tools/list → nombres, descripciones y esquemas; tools/call → resultado. Clic 1: la lista que da el servidor (simulado en el notebook). Clic 2: la descripción sospechosa de sincronizar_notas. Clic 3: tu lista blanca (PERMITIDAS_MCP). Clic 4: faq_curso entra, sincronizar_notas se rechaza. Clic 5: tools/list es una entrada no confiable; mínimo alcance. Antes de un MCP remoto: verifica identidad, alcance, a qué servidor van las credenciales y a qué destinos de red sale. Módulo 5.

---

## Proyecto: Soporte NemoClaw v3

:::diagrama c23-soporte-v3

Notas:
Clic 1: buscar_faq (responde con la FAQ y cita tema y pregunta) y estimar_costo_brev (horas × tarifa). Clic 2: Soporte NemoClaw v3. Clic 3: el harness (argumentos validados, errores que se corrigen solos, solo ve las herramientas que necesita). Clic 4: reto, tarifa_instancia(tipo) con enum → dos llamadas en orden y el costo correcto. En 3.1: router de triage con instalacion | api_key | brev | seguridad | otro.

---

## Tu práctica

:::diagrama c23-practica

Notas:
Un clic por paso. Preguntas de "Lo esencial": qué herramienta eligió el modelo para cada pregunta (sección 4), qué pasó con borrar_instancia (sección 5), qué herramienta rechazó la lista de permitidas y qué frase sospechosa tenía (sección 9). Extra sin programar: escribir la descripción de una herramienta diciendo cuándo usarla y cuándo no. Si programas: el notebook completo y el reto de tarifa_instancia con enum.
