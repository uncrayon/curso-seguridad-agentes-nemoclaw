## Casi todos los problemas no son de agentes

:::diagrama c13-causas

Notas:
Clics 1 a 3: las tres causas de casi todo (key mal copiada, ID de modelo con un error, límite de uso). Clic 4: NVIDIA responde con un aviso con número, como un cajero automático. Clic 5: hoy los provocamos a propósito y dejamos el entorno verificado antes del Módulo 2. El objetivo es que nadie vuelva a entrar en pánico con un 401.

---

## Una ruta de modelo

:::diagrama c13-ruta-postal

Notas:
La ruta es la dirección postal de una oficina. Clic 1: la dirección (URL base, https://integrate.api.nvidia.com/v1). Clic 2: el destinatario (ID del modelo). Clic 3: tu firma (la key). Clic 4: las dos rutas del curso; la de embeddings usa nvidia/nemotron-3-embed-1b con la misma dirección. Clic 5: si un dato está mal, la carta regresa. En Python: NVIDIA_BASE_URL, NVIDIA_MODEL, NVIDIA_EMBED_MODEL, NVIDIA_API_KEY.

---

## El panel del curso de NVIDIA

:::diagrama c13-panel

Notas:
Clic 1: los tres datos de la ruta (dirección y modelo ya vienen llenos; la key se guarda en sessionStorage). Clic 2: la casilla del relay de CORS; no da key ni acceso, solo reenvía (en Python no hace falta). Clic 3: los desplegables Ruta de embeddings y Gestión de la solicitud (espera de 60 s, reintentos de 0 a 5; subir a 2). Clic 4: Guardar y verificar hace una prueba real. Clic 5: la key se borra al cerrar la pestaña. Los textos del panel en español son traducción y pueden cambiar: lee lo que veas. Este panel es opcional; el notebook hace la misma verificación.

---

## El doctor del curso

:::diagrama c13-doctor

Notas:
Clic 1: el notebook y sus celdas de configuración. Clic 2: EN VIVO si encontró la key; MOCK si no (respuestas simuladas, con errores simulados). Clics 3 a 7: las cinco pruebas (forma de la key, GET /v1/models, chat con latencia y usage, tool buscar_faq, vector de embeddings). Clic 8: el veredicto, "✅ entorno listo" o instrucciones precisas.

---

## Rompe tu entorno a propósito

:::diagrama c13-rompe

Notas:
Una fila por clic: key falsa → 401; modelo inexistente → 404; max_tokens=8 → finish_reason="length" y contenido vacío. El tercero no es una excepción: es una respuesta 200 incompleta. Clic 4: diagnostico(e) traduce cada error a "qué pasó + qué hacer". Si en vivo sale 403 en lugar de 401, o 400/422 en lugar de 404, dilo así: el diagnóstico es el mismo.

---

## La tabla de errores

:::diagrama c13-avisos

Notas:
Los avisos del cajero. Clics 1 a 4: los que se corrigen (401, 403, 404, 410): reintentar no sirve. Clics 5 y 6: los que se arreglan esperando (429 y 5xx). Clic 7: más espera o más reintentos nunca arreglan un 401.

---

## Reintento con backoff

:::diagrama c13-backoff

Notas:
Clics 1 a 3: dos 429 y éxito al tercer intento, esperando cada vez el doble. Clic 4: siempre con límite de intentos. Clic 5: con un 401 no se reintenta. Solo se reintentan 429, 5xx y fallas de red; si llega Retry-After, se respeta. El cliente openai ya reintenta 2 veces (max_retries=2); el código está en la sección 8 del notebook.

---

## Errores comunes

| Ves | Haz esto |
|---|---|
| `Modo: MOCK` aunque guardaste tu key | Revisa el secreto `NVIDIA_API_KEY` y el acceso del notebook |
| "La clave debe comenzar por nvapi-" | Copia la key completa, sin espacios |
| Respuesta vacía y `length` | Dale más espacio: sube `max_tokens` |
| "Connection failed" en el panel | Lee el número: 401/403 tu key · 429 espera · 5xx NVIDIA |

Notas:
Si trabajas en tu máquina y sale MOCK con .env creado: el .env va en la raíz del repo y hay que reiniciar el kernel.

---

## Avance del proyecto

:::diagrama c13-reporte

.lead Soporte NemoClaw gana su primera pieza: `reporte_entorno()`

Notas:
Clic 1: el doctor. Clic 2: el reporte sin secretos (Python, modo, rutas, pruebas, latencia). Clic 3: el estudiante lo pega al pedir ayuda; en la 3.3 los subagentes lo leen para diagnosticar. Clic 4: el assert del notebook garantiza que la key nunca aparece en el reporte.
