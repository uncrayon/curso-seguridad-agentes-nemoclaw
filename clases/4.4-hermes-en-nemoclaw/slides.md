## Cambia el agente, no la seguridad

:::diagrama c44-mismo-cuarto

Notas:
Mismo cuarto con cerradura, otro asistente. Clic 1: OpenClaw, el de las clases 4.1 a 4.3. Clic 2: lo cambias por Hermes (Nous Research, licencia MIT). Clic 3: lo que se queda igual: el sandbox de OpenShell, las políticas de red, la inferencia administrada con la key en el host. Clic 4: lo nuevo, Hermes guarda memoria entre sesiones y crea sus propias skills. NemoClaw ≠ OpenClaw: es la pregunta de la clase 1.1, ahora comprobada en el laboratorio. También puede llevar LangChain Deep Agents.

---

## Crea el sandbox

:::diagrama c44-crear

Notas:
Un clic por paso. 1: nemoclaw my-assistant stop (se detiene, no se borra). 2: la key con read -rsp, no aparece en pantalla ni en el historial. 3: NEMOCLAW_SANDBOX_NAME=mi-hermes nemohermes onboard; nemohermes es el CLI de NemoClaw con Hermes por defecto; proveedor NVIDIA Endpoints, búsqueda web none, reglas sugeridas. 4: nemohermes mi-hermes status. 5: la puerta nueva en el puerto 8642 (openshell forward list, curl /health). Clic 6: el crédito; ≈35 min de la sesión de laboratorio, y al final se vuelve a encender my-assistant. Todo en la VM TERMINAL del tablero, no en la SANDBOX TERMINAL. Alternativa: un laboratorio nuevo puede elegir Hermes en la configuración del navegador.

---

## La forma de operador, en la terminal

```bash
nemoclaw my-assistant stop                        # pausa OpenClaw, no lo borra
read -rsp "NVIDIA API key: " NVIDIA_INFERENCE_API_KEY; echo
export NVIDIA_INFERENCE_API_KEY
NEMOCLAW_SANDBOX_NAME=mi-hermes nemohermes onboard
nemohermes mi-hermes status                       # ¿está sano?
curl -sf http://127.0.0.1:8642/health             # ¿la puerta nueva contesta?
```

.lead En esta clase la VM TERMINAL es el camino: antes de cada línea, dices para qué sirve.

Notas:
Las preguntas del onboarding pueden variar un poco según la versión; elegir NVIDIA Endpoints, el modelo que propone, búsqueda web none y las reglas sugeridas. El onboarding tarda varios minutos la primera vez: cortar en edición. No presionar Shift+Escape mientras corre: cierra la terminal y sus procesos.

---

## OpenClaw vs. Hermes

:::diagrama c44-comparar

Notas:
Dónde guarda cada cosa. Un clic por fila: personalidad, memoria (el diario, con límite de caracteres), skills (Hermes también crea las suyas), conversaciones (SQLite en state.db; sessions export las saca como JSONL) y la puerta para programas (API compatible con OpenAI en el 8642, con token Bearer). Clic 6: lo que no cambia. La búsqueda web también cambia: Brave en OpenClaw, Tavily en Hermes. config.yaml lo escribe NemoClaw: no se edita a mano. Para verlo como operador: nemohermes mi-hermes exec -- bash -lc 'ls -la /sandbox; ls -la /sandbox/.hermes'.

---

## La misma skill, otro agente

:::diagrama c44-misma-skill

.lead SKILL.md es un formato abierto: lo entienden los dos agentes.

Notas:
Clic 1: la skill soporte-nemoclaw de la clase 4.3. Clic 2: en OpenClaw vive en skills/ del escritorio. Clic 3: en Hermes solo cambian dos rutas (la FAQ en /sandbox/faq). Clic 4: el resultado, sin darle la ruta. Comandos: nemohermes mi-hermes skill install ~/curso/clases/4.4-hermes-en-nemoclaw/skills/soporte-nemoclaw/, nemohermes mi-hermes upload ~/curso/datos/faq/ /sandbox/ (el destino es la carpeta padre, como en la 4.3), nemohermes launch mi-hermes. Cada skill también es un comando del chat: /soporte-nemoclaw. Estándar: agentskills.io.

---

## Un agente que aprende solo

:::diagrama c44-aprobacion

Notas:
Error en vivo. Clic 1: sin aprobación, "recuerda X" se guarda en MEMORY.md sin preguntarte (léelo como operador). Clic 2: si quien lo pide es un texto malicioso, también se guarda y queda para todas las conversaciones futuras. Clic 3: con /memory approval on, cada nota espera tu sí; /memory pending las muestra y /memory reject las rechaza. Clic 4: lo mismo con las skills que crea. Si la versión del día ya trae la aprobación activada, mostrar /memory pending directamente y decirlo.

---

## La API compatible con OpenAI

:::diagrama c44-dos-capas

Notas:
Clic 1: tu programa en Python habla con Hermes por la puerta nueva (base_url http://127.0.0.1:8642/v1), con el token del gateway: TOKEN="$(nemohermes mi-hermes gateway-token --quiet)", nunca en pantalla. Clic 2: capa 1, tu programa recibe la respuesta: con el cliente normal de OpenAI (pip install openai), sin nada más. Clic 3: capa 2, lo que Hermes hizo adentro (sus grep y cat) no aparece en tu programa: está en su historial, nemohermes mi-hermes sessions export. Clic 4: dos capas distintas. Script: hermes_api.py.

---

## Errores comunes

| Ves | Haz esto |
|---|---|
| `nemohermes: command not found` | Usa la VM TERMINAL, no la SANDBOX TERMINAL |
| `Port 18789 is not available` | Usa el siguiente puerto libre (míralo en `openshell forward list`) |
| `401` al hablarle por la puerta nueva | Pide el token otra vez y guárdalo en una variable, sin mostrarlo |
| La skill no aparece en el chat | Sal con `/exit` y abre una conversación nueva |
| `skill install` no reemplaza la anterior | Quítala con `skill remove` e instálala otra vez |
| `my-assistant` no responde después | Enciéndelo: `nemoclaw my-assistant start` |

Notas:
El token: TOKEN="$(nemohermes mi-hermes gateway-token --quiet)". Nunca muestres la salida de gateway-token en cámara.

---

## Avance del proyecto

:::diagrama c44-avance

.lead Apaga el cuarto de Hermes y vuelve a encender my-assistant.

Notas:
Clic 1: Soporte NemoClaw corre en dos agentes, con la misma skill y la misma personalidad, dentro del mismo tipo de cuarto, y un cliente en Python que le habla por su API. Clic 2: lo que abrimos para el Módulo 5: memoria que se escribe sola, skills que el agente crea y una API con token. Para apagar: nemohermes mi-hermes stop, y volver a encender OpenClaw con nemoclaw my-assistant start (los módulos 5 y 6 lo usan). Si paras por hoy: Stop en la consola de Brev y vuelve pronto.
