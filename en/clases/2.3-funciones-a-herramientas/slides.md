## A tool's contract

:::diagrama c23-ventanilla

Notes:
Based on NVIDIA's lesson 01c: "the tool-calling contract stays fixed". One click per part of the card: name (a capability), description (when to use it and when not), inputs it needs (the schema: arguments, types and limits) and what it returns (always text). Click 5: fixed contract = you can change everything inside.

---

## From function to tool

:::diagrama c23-de-funcion

Notes:
Clicks 1 and 2: the function and its comment (the docstring). Click 3: the @herramienta tag (the decorator) reads them and writes the card. Click 4: the model chooses by reading only the card. Click 5: signature + docstring → schema, a single source of truth. Show the generated JSON: type number, minimum, additionalProperties false.

---

## Descriptions decide

:::diagrama c23-descripciones

Notes:
Demo: sabotage buscar_faq's description ("Herramienta 1.") and repeat the three questions. Click 1: with a good description, each question goes to its tool. Click 2: with a bad one, the model guesses. Click 3: the description is the main prompt-engineering surface.

---

## Validate before running

:::diagrama c23-filtro

Notes:
Click 1: the model's request. Click 2: does the tool exist and is it allowed? Click 3: are the arguments valid JSON? Click 4: do they match the schema? (required, type, enum, minimum, additionalProperties). Click 5: it runs inside try. Click 6: every error goes back to the model as text. Click 7: the schema asks, the harness enforces. It's 30 lines with no dependencies; in production, the jsonschema library.

---

## An error is a clue

:::diagrama c23-tres-dias

Notes:
The live error in this class. Click 1: the model sends "tres días" (three days) where a number goes. Click 2: "ERROR de validación: 'horas' debe ser number, llegó str ('tres días'). Corrige y vuelve a llamar." Click 3: it corrects to 72. Click 4: 72 h × $0.15/h ≈ $10.80 USD of compute. Click 5: the model reads the error and moves on; your code doesn't blow up.

---

## Your list decides what runs

:::diagrama c23-tu-lista

Notes:
A tool is a door between the model's text and your computer. Click 1: the model can ask for anything. Click 2: what's in the registry runs. Click 3: borrar_instancia isn't there: an error comes back and nothing runs. Other common errors: answers from memory → the description doesn't say when to use the tool; "'horas' debe ser number" in a loop → put an example in the parameter description; "Sin resultados en la FAQ" → say so, never guess; cells out of order → empty TOOLS, rerun the decorator.

---

## Same contract, a different search

:::diagrama c23-otra-busqueda

Notes:
A preview of RAG, which comes later. Click 1: the model and buscar_faq's card. Click 2: before, it searched by keywords. Click 3: now by meaning, with embeddings (nemotron-3-embed-1b): REGISTRO["buscar_faq"] = buscar_faq_semantica, and the model doesn't notice. Click 4: if the new backend is worse, the schema won't warn you.

---

## A subagent behind a tool

:::diagrama c23-subagente

Notes:
Click 1: the main agent only sees consultar_experto_brev(pregunta). Click 2: the subagent has its own prompt and only estimar_costo_brev. Click 3: only the answer comes back; its steps don't clutter the main history (it separates context). Click 4: it's not access control. Later we scale it up with a planner.

---

## MCP: tools from another server

:::diagrama c23-mcp

Notes:
tools/list → names, descriptions and schemas; tools/call → result. Click 1: the list the server hands over (simulated in the notebook). Click 2: sincronizar_notas' suspicious description. Click 3: your allow list (PERMITIDAS_MCP). Click 4: faq_curso gets in, sincronizar_notas is rejected. Click 5: tools/list is untrusted input; minimum scope. Before a remote MCP: verify identity, scope, which server the credentials go to and which network destinations it reaches. We dig into this later, when we cover security.

---

## Project: Soporte NemoClaw v3

:::diagrama c23-soporte-v3

Notes:
Click 1: buscar_faq (answers from the FAQ and cites topic and question) and estimar_costo_brev (hours × rate). Click 2: Soporte NemoClaw v3. Click 3: the harness (validated arguments, errors it fixes on its own, it only sees the tools it needs). Click 4: challenge, tarifa_instancia(tipo) with an enum → two calls in order and the right cost. Coming up: a triage router with instalacion | api_key | brev | seguridad | otro.

---

## Your practice

:::diagrama c23-practica

Notes:
One click per step. Questions on the class page: which tool the model chose for each question (section 4), what happened with borrar_instancia (section 5), which tool the allow list rejected and what suspicious sentence it had (section 9). Extra, no coding: write a tool description saying when to use it and when not. If you code: the whole notebook and the tarifa_instancia enum challenge.
