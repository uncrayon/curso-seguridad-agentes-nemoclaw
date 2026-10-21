## Por qué un solo contexto se rompe

:::diagrama c33-escritorio

.lead La salida no es un modelo más grande: es dejar de apilar.

Notas:
El contexto es el escritorio de trabajo. Un solo loop que investiga key, instancia y cookie apila todo en el mismo escritorio. Un clic por falla (lección 02c de NVIDIA). Clic 1: desbordamiento, ya no cabe en la ventana de contexto. Clic 2: context rot, cabe pero lo de en medio pesa poco (Lost in the Middle, 2023). Clic 3: interferencia, razonar sobre A ensucia a B.

---

## Planear, investigar, preservar, sintetizar

:::diagrama c33-flujo

Notas:
El jefe de proyecto. Clic 1: planear; el planificador divide el reporte en 2 a 4 partes, con tope. Clic 2: investigar; un subagente por parte, en paralelo y con el escritorio limpio. Clic 3: preservar; cada uno deja su borrador en un archivo (/borradores/s1.md). Clic 4: sintetizar; el sintetizador lee archivos, no conversaciones, y escribe el reporte con citas. Es la idea de librerías como deepagents o LangGraph, aquí en Python puro.

---

## Cada subagente, su propio contexto

:::diagrama c33-escritorios

Notas:
Un clic por subagente. Cada uno empieza con el escritorio vacío: sus instrucciones, el reporte y su parte; nada de la historia de sus hermanos. Herramientas: buscar_faq (el RAG que construiste antes) y escribir_archivo. El permiso del harness solo lo deja escribir en /borradores/<su id>.md. Clic 4: no lo supongas, compruébalo: la celda "Comprueba el aislamiento".

---

## El reporte de diagnóstico

:::diagrama c33-reporte

Notas:
El reporte para "Me sale 401 en el laboratorio después de reanudar Brev". Clic 1: el reporte. Clic 2: la causa más probable, con su cita a la FAQ. Clic 3: los pasos. Clic 4: lo que no se pudo verificar, si un subagente cayó. Clic 5: tu código revisa cada cita: debe estar en un borrador y existir en la FAQ (revisar_citas).

---

## Topes y fallas

:::diagrama c33-topes

Notas:
Un clic por riesgo y su protección: MAX_SUBAGENTES = 4; max_pasos = 5; "permiso denegado" devuelto como observación; el reporte dice qué faltó; revisar_citas. Error en vivo: el subagente s9 intenta escribir en /reporte_diagnostico.md.

---

## Contexto aislado ≠ sandbox

:::diagrama c33-no-es-sandbox

Notas:
Clic 1: los escritorios separados de hoy; separan lo que el agente piensa y los aplica tu código. Clic 2: pero corren en tu programa: ven tu NVIDIA_API_KEY y tu disco (celda de os.environ). Clic 3: el cuarto con cerradura, que ya conoces; limita lo que el agente toca y lo aplican el sistema operativo y la política. Clic 4: necesitas las dos.

---

## Cuánto cuesta

:::diagrama c33-costo

.lead Úsalo solo cuando el problema no cabe en una conversación o necesitas varias investigaciones independientes.

Notas:
Cada círculo es una llamada al modelo. Clic 1: el agente con búsqueda que hiciste antes, 2 a 3 llamadas. Clic 2: el agente profundo con 3 subagentes, unas 11.

---

## Si algo sale mal

| Ves | Haz esto |
|---|---|
| «El planificador no devolvió subtareas válidas» | Mira lo que contestó y pide el formato más claro |
| «Terminó sin guardar su borrador» | Recuérdale guardar y revisa el tope de pasos |
| Error 429 con varios subagentes | Menos subagentes a la vez y reintento con espera |
| «no_existen_en_faq» en la revisión | El reporte no es confiable: revísalo |

Notas:
Para el 429: bajar max_workers y reintentar con espera. "Terminó sin guardar": reforzar el paso 2 de SISTEMA_SUBAGENTE y revisar max_pasos.

---

## Si prefieres el código

```python
mensajes = [
  {"role": "system", "content": SISTEMA_SUBAGENTE},
  {"role": "user", "content": f"Reporte: {reporte}\nTu subtarea: {st['objetivo']}"},
]   # nada de la historia de sus hermanos
```

.lead Es opcional: todo esto está, listo para ▶, en el notebook de la clase.

Notas:
Para quien programa: ejecutar_subagente crea esta lista desde cero para cada subagente; escribir_archivo rechaza cualquier ruta fuera de /borradores/<id>.md.

---

## Avance del proyecto

:::diagrama c33-avance

Notas:
Un clic por capacidad nueva de Soporte NemoClaw. Clic 5: lo que sigue, donde lo llevas a NemoClaw en Brev; la FAQ va en el workspace y la skill soporte-nemoclaw corre en un sandbox. Tu agente enruta, se fundamenta y planea; ahora necesita un lugar seguro donde vivir.
