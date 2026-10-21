## ¿Cuándo un loop no alcanza?

:::diagrama c31-loop-vs-flujo

Notas:
Clic 1: el ticket del proyecto. Clic 2: el loop ReAct que construiste antes, donde el modelo descubre qué revisar un paso a la vez. Clic 3: el flujo de trabajo, donde tu código ya sabe que toca revisar key, instancia y sesión. La pregunta de la clase: ¿quién decide la forma del trabajo, el modelo o tu código?

---

## Cuatro patrones

:::diagrama c31-patrones

Notas:
Un clic por patrón: ReAct (ya lo conoces), router, ReWOO y fan-out. Clic 5: hoy construimos los tres de la derecha, aplicados a Soporte NemoClaw.

---

## El router: ventanillas fijas

:::diagrama c31-router

Notas:
La recepcionista de la clínica. Clic 1: llega el ticket. Clic 2: el router; el modelo solo elige UNA etiqueta y contesta en una ficha con campos fijos (JSON estricto con enum, temperatura 0). Clic 3: la lista cerrada de ventanillas. Clic 4: el 401 cae en api_key. Clic 5: tu código hace el envío. Cada especialista es el mismo código con otras instrucciones (la fábrica crear_especialista, el "specialist factory" de la lección de NVIDIA).

---

## ¿Y si el modelo inventa una etiqueta?

:::diagrama c31-etiqueta

Notas:
Error en vivo de la clase. Clic 1: el modelo contesta "facturacion", que no existe; usada tal cual, el programa se cae (KeyError). Clic 2: tu código la revisa contra la lista. Clic 3: un solo reintento, mostrándole su error. Clic 4: si insiste, "otro" y lo revisa una persona. Clic 5: nunca mapees sinónimos a mano. La salida del modelo es una entrada no confiable, igual que la del usuario.

---

## ReWOO: planea una vez

:::diagrama c31-rewoo

Notas:
La lista del súper antes de salir. Clic 1: el planificador escribe el plan completo en una llamada; tu código lo recorta a 4. Clic 2: el ejecutor, sin modelo, hace todas las búsquedas a la vez (la quinta queda fuera por el tope). Clic 3: el sintetizador responde con citas. Clic 4: dos llamadas al modelo, sin importar cuántas búsquedas. Xu et al., 2023. Si el paso 2 necesita la respuesta del paso 1, ReWOO no sirve: vuelve al loop.

---

## Fan-out / fan-in

:::diagrama c31-fanout

Notas:
Clic 1: el reporte del 401. Clic 2: dos especialistas lo revisan a la vez. Clic 3: el de seguridad no contesta (lo provocamos a propósito). Clic 4: la unión junta lo que llegó y dice qué faltó. Clic 5: la analogía de la caja del súper. Una rama caída no tumba el resultado: lo contrario de Promise.all. Reintento con espera solo para 429, dentro de la rama; un 401 no se reintenta.

---

## Mide el tiempo, no lo adivines

:::diagrama c31-tiempo

Notas:
Cifras del modo sin key (simulado). Clic 1: las búsquedas una tras otra contra todas a la vez. Clic 2: las dos llamadas al modelo; en vivo tardan segundos cada una. Clic 3: si el modelo domina el total, paralelizar casi no se nota. Las cifras en vivo dependen del modelo y la carga: llenar con los números de la prueba previa.

---

## Cuándo NO dividir

:::diagrama c31-dividir

Notas:
Clic 1: una sola llamada (el generalista del notebook). Clic 2: la misma pregunta dividida en cuatro llamadas, con su costo. Clic 3: cuándo sí dividir. Clic 4: cuándo no. Cada frontera es una llamada más, más espera y otro lugar donde fallar. Si leer la traza importa más que la velocidad, tampoco dividas.

---

## Si algo sale mal

| Ves | Haz esto |
|---|---|
| La etiqueta «facturacion» no está en la lista | Es lo esperado: un reintento y luego «otro» |
| La respuesta llega cortada o sin ficha | Dale más espacio a la respuesta (`max_tokens`) |
| Error 400 al pedir la ficha con campos fijos | Sigue sin la ficha, pero revisa igual |
| Error 429 en una rama | Menos ramas a la vez y reintento con espera |
| El programa se cae buscando la ventanilla | Revisa la etiqueta antes de enviar el ticket |

Notas:
Mensajes técnicos tal como salen en el notebook: "categoria inválida: 'facturacion'", "JSON ilegible" / finish_reason=length, 400 con response_format, 429, KeyError en ESPECIALISTAS.

---

## Si prefieres el código

```python
CATEGORIAS = ["instalacion", "api_key", "brev", "seguridad", "otro"]
t = clasificar(ticket)                              # el modelo elige UNA etiqueta
respuesta = ESPECIALISTAS[t["categoria"]](ticket)   # el router: un diccionario

with ThreadPoolExecutor(max_workers=3) as pool:     # fan-out: todas las ramas a la vez
    futuros = {pool.submit(rama, n, reporte): n for n in RAMAS}
```

.lead Es opcional: todo esto está, listo para ▶, en el notebook de la clase.

Notas:
Para quien programa. response_format con json_schema y enum; temperatura 0. En el fan-out, cada f.result() va dentro de try/except: la rama cae y las demás siguen.

---

## Avance del proyecto

:::diagrama c31-avance

Notas:
Un clic por capacidad nueva de Soporte NemoClaw y, al final, el reto. Siguiente paso, muy pronto: que los especialistas dejen de responder de memoria.
