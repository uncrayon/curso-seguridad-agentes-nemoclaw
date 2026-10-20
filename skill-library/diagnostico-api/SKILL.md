---
name: diagnostico-api
description: Diagnostica errores al llamar a la API de modelos de NVIDIA (build.nvidia.com o integrate.api.nvidia.com) a partir del código HTTP o del mensaje de error, como 401, 403, 404, 410, 429 o 5xx, y propone la corrección. Úsala cuando el usuario pegue un error de la API o diga que el modelo no responde.
---

# diagnostico-api

## Propósito
Convertir un error de la API en tres cosas: qué pasó, por qué y qué hacer ahora.
Es el "FAQ en código" de la clase 1.3, empaquetado como skill.

## Pasos
1. Extrae el código HTTP del mensaje (por ejemplo, `401`). Si no hay código, busca pistas: `timeout`, `Connection`, `Could not resolve host`.
2. Herramienta: `diagnosticar_http` con `{"codigo": "<codigo>"}`.
3. Responde con este formato:
   - **Qué pasó:** una línea.
   - **Causa probable:** una línea.
   - **Qué hacer:** de 1 a 3 pasos con comandos exactos.
4. Si el error viene del laboratorio (sale en `nemoclaw <sandbox> status` como `unauthorized` o `unreachable`), di que es la credencial o la ruta del sandbox y sugiere `nemoclaw <sandbox> status` antes de cambiar nada.
5. Si el código no está en la tabla de la herramienta, dilo y pide el cuerpo completo del error.

## Errores que ya conoces
| Código | Significa |
|---|---|
| 401 | La key no es válida o está mal copiada |
| 403 | Key válida sin acceso a ese modelo o sin créditos |
| 404 | Modelo o ruta que no existe (revisa el ID y que la URL termine en `/v1`) |
| 410 | Modelo retirado del endpoint gratuito |
| 429 | Demasiadas solicitudes por minuto |
| 5xx | Falla del servidor o modelo arrancando |

## Límites
- Nunca muestres la key completa. Si necesitas verificarla, revisa solo que empiece con `nvapi-`.
- No recomiendes desactivar TLS ni usar `--insecure`.
- Un 403 dentro del sandbox con `CONNECT tunnel failed, response 403` no es un error de la API: es la política de red. En ese caso, usa `soporte-nemoclaw`.
