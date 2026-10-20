## Tu llave a los modelos

:::diagrama c12-tarjeta

Notas:
La API key es la tarjeta de acceso de un edificio. Clic 1: tú, con tu cuenta gratuita. Clic 2: la key (empieza con nvapi-). Clic 3: build.nvidia.com, el catálogo de modelos alojados por NVIDIA (API compatible con OpenAI, dirección https://integrate.api.nvidia.com/v1). Clic 4: Nemotron, el modelo del curso. Clic 5: trátala como contraseña. Los Módulos 1 a 3 usan esta dirección; no hace falta tarjeta gráfica propia.

---

## Crea la cuenta y la key

:::diagrama c12-pasos-cuenta

Notas:
Un clic por paso: entrar, confirmar el correo, generar la key en API Keys, copiarla en ese momento y probar el modelo en el cuadro de prueba de su ficha. Clic 6: el aviso para LATAM (issues #201 y #214 de NemoClaw; soporte en help@build.nvidia.com con correo, números probados y capturas). [VERIFICAR EN LAB] nombres exactos de menú y botón, y si la ficha de Nemotron tiene cuadro de prueba.

---

## Dónde guardarla

:::diagrama c12-donde-guardar

Notas:
Clic 1: lugares seguros (gestor de contraseñas, Secrets de Colab con el nombre NVIDIA_API_KEY, archivo .env, panel del curso de NVIDIA, que la guarda en sessionStorage y la borra al cerrar la pestaña). Clic 2: dónde nunca. Clic 3: los pasos de Colab. NemoClaw local (6.3) usa otro nombre de variable: NVIDIA_INFERENCE_API_KEY. Misma key.

---

## Si prefieres la terminal

```bash
cp .env.example .env              # archivo privado: pega ahí tu key
read -rs NVIDIA_API_KEY && export NVIDIA_API_KEY   # o solo en esta terminal
git check-ignore .env             # debe imprimir .env
curl -s https://integrate.api.nvidia.com/v1/models \
  -H "Authorization: Bearer $NVIDIA_API_KEY"       # ¿llego? no gasta tokens
```

.lead Es opcional. Ojo: una terminal nueva no recuerda tu key; vuelve a cargarla.

Notas:
Error en vivo: 401 en una pestaña nueva de terminal. Revisar con echo "${NVIDIA_API_KEY:0:6}" que empiece con nvapi-, exportar de nuevo y repetir. Pedir la lista de modelos no gasta tokens y dice si el ID exacto existe. El curl de chat completo está en la página de la clase.

---

## Primera llamada al modelo

:::diagrama c12-primera-llamada

Notas:
Clic 1: tu pregunta viaja con tu key. Clic 2: Nemotron piensa antes de responder (por eso max_tokens va en 1024). Clics 3 a 5: los tres campos de la respuesta: content, finish_reason (stop = terminó bien) y usage (tokens de entrada y salida). Clic 6: qué es un token. El curl de /v1/chat/completions está en la página de la clase.

---

## Cuida tus créditos

:::diagrama c12-creditos

Notas:
Clic 1: tus créditos, como el saldo de prepago del celular. Clic 2: cada pregunta gasta tokens; si te pasas del límite, NVIDIA responde 429. Clic 3: espera y reintenta. Clic 4: lo que más gasta. Clic 5: los modelos gratuitos cambian; uno retirado da 410, por eso el modelo vive en NVIDIA_MODEL y no escrito en el código. [VERIFICAR EN LAB] cifras vigentes de créditos o solicitudes por minuto y la página donde se ve el consumo. No dar números sin confirmar.

---

## Errores comunes

| Ves | Haz esto |
|---|---|
| **401** en una terminal nueva | Vuelve a cargar tu key en esa terminal |
| **404** | Copia el nombre exacto del modelo |
| Respuesta vacía y `length` | Dale más espacio: sube `max_tokens` |
| El curso de NVIDIA te pide la key otra vez | Normal: se borra al cerrar la pestaña |
| El SMS no llega (LATAM) | Escribe a help@build.nvidia.com |

Notas:
El nombre exacto del modelo sale de la lista /v1/models. La página del curso guarda la key en sessionStorage.

---

## Si filtras tu key

:::diagrama c12-filtrada

Notas:
Un clic por paso: se filtró, revócala en API Keys, genera otra y actualízala en todos lados (.env, terminal, Colab y NemoClaw). Clic 5: borrar el archivo del repo no basta porque la key queda en el historial de git. Revocar es lo único que protege. Hazlo en cuanto te des cuenta.
