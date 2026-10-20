# Tu laboratorio en Brev: crédito, sesiones y cookie

Los Módulos 4, 5 y 6 se hacen en un **laboratorio**: una computadora en la nube con NemoClaw ya instalado. Esta página te explica cuánto cuesta, cómo planear tus sesiones para que te alcance el crédito de **1 USD** y cómo conectarte sin miedo.

No necesitas instalar nada en tu computadora. Todo se hace desde el navegador.

> **Piénsalo como** rentar una oficina por horas: pagas mientras la luz está encendida, pagas un poco por guardar tus cosas aunque la luz esté apagada, y si la entregas, pierdes lo que dejaste adentro.

## Lo que necesitas

- Una cuenta de NVIDIA para entrar a [Brev](https://brev.nvidia.com/).
- Tu cupón de **1 USD** de crédito.
- Tu API key `nvapi-` de la clase 1.2.
- Una computadora con navegador de escritorio (Chrome, Edge, Firefox o Safari). El celular no sirve para el laboratorio.

## 1 · Tu crédito de 1 USD

### Qué cuesta y qué no

| Estado de tu instancia | ¿Cobra la computadora? | ¿Cobra el disco? | ¿Se conserva tu trabajo? |
|---|---|---|---|
| **Running** (encendida) | Sí | Sí | Sí |
| **Stopped** (detenida) | No | **Sí, poquito** | Sí |
| **Deleted** (borrada) | No | No | **No, se pierde** |

- La instancia del curso es **solo CPU** (sin tarjeta gráfica): unos **USD 0.15 por hora** encendida. El modelo de IA corre en la nube de NVIDIA, no en tu instancia. `[VERIFICAR EN LAB: precio en la página de despliegue; puede aparecer como Free]`
- El disco cobra **mientras exista la instancia**, aunque esté detenida. Por eso conviene hacer el laboratorio en pocos días y borrarla al final. `[VERIFICAR EN LAB: tamaño del disco]`
- Usar la **página del curso de NVIDIA**, los **notebooks** en Colab y tu **API key** no gasta crédito de Brev.

### El plan: tres sesiones en pocos días

| Sesión | Clases | Tiempo encendida (aprox.) | Costo aprox. |
|---|---|---|---|
| **1** | 4.1, 4.2 y 4.3 | ≈75 min | ≈USD 0.19 |
| **2** (si te alcanza) | 4.4 · Hermes | ≈35 min | ≈USD 0.09 |
| **3** | 5.2, 5.3 y 6.1 | ≈65 min | ≈USD 0.16 |
| **Total** | | **≈3 h** | **≈USD 0.45 + disco** |

`[VERIFICAR EN LAB: tiempos reales y costo del disco por día]`

Cinco reglas para que te alcance:

1. **Mira primero el video de la clase.** Así, cuando enciendas la instancia, ya sabes qué vas a hacer.
2. **Detén la instancia al terminar cada sesión:** consola de Brev → **GPUs** → tu instancia → **Stop**. Confirma que diga `STOPPED`.
3. **Haz las tres sesiones en 2 o 3 días seguidos.** El disco cobra cada día que la instancia exista.
4. **Al terminar el Módulo 6, guarda tu trabajo y borra la instancia:** **Delete**. Es la única forma de que deje de cobrar del todo.
5. **No actives la recarga automática** (*auto-recharge*) en **Billing**.

### Cómo canjear el cupón y revisar tu saldo

1. Entra a https://brev.nvidia.com.
2. Ve a **Billing** → **Credits** → **Redeem a credit code** y pega tu cupón.
3. Revisa que el saldo diga 1.00 USD **en la organización correcta**. En Brev el crédito es de la *organización*, no de tu usuario; si tienes varias (la de tu empresa y la personal), elige la tuya antes de desplegar.

`[VERIFICAR EN LAB: nombres exactos de los menús y si el cupón se aplica solo]`

**Si se te acaba el crédito:** tu instancia se detiene. No pierdes la cuenta. Revisa [¿Qué pasa si se me acaban los créditos?](FAQ.md#brev) y pide ayuda en el foro del curso.

## 2 · Todo desde el navegador

En el laboratorio vas a usar cuatro páginas web. Ninguna requiere instalar programas:

| Página | Para qué |
|---|---|
| **Consola de Brev** (brev.nvidia.com) | Encender, detener y borrar tu instancia; ver tu crédito. |
| **La página de tu launchable** (`nemoclaw-<id>…`) | Configurar tu agente con el botón **SET UP IN THIS BROWSER** y conversar con él. |
| **Las lecciones del curso de NVIDIA** ([03a](https://nvdli.github.io/NemoClawDLI/es/nemoclaw/03a-kickstart.html), 03b, 03c, 04a, 04b) | Ejecutar los pasos del laboratorio con botones ▶, sin escribir comandos. |
| **El dashboard de tu agente** | Conversar con él y ver su estado. |

Algunas clases muestran también **comandos de terminal**. Son la forma «de operador»: la misma tarea, escrita como instrucción. Cada guía dice primero cómo hacerlo con clics y después el comando, para quien quiera usarlo. Si una clase te pide un comando y no quieres instalar nada, puedes pegarlo en la **terminal web** de tu launchable. `[VERIFICAR EN LAB: dónde abre el launchable su terminal en el navegador]`

## 3 · La cookie de sesión, con calma

La página del curso de NVIDIA vive en otro sitio web que tu laboratorio. Para que pueda hablar con tu laboratorio, le das una prueba de que eres tú: tu **cookie de sesión**.

> **Piénsalo como** la pulsera de un evento: mientras la traigas, entras sin mostrar el boleto. Si alguien te la quita, entra como tú. Por eso la cuidas.

### Antes de copiarla

- Pégala **solo** en el campo **Sesión de acceso** de la página del curso de NVIDIA.
- **Nunca** en un chat, un correo, un foro, una captura de pantalla ni un video.
- La página la guarda solo mientras tengas esa pestaña abierta.
- Caduca sola. Al terminar, cierra sesión en Brev y detén tu instancia.

### Paso a paso (Chrome o Edge)

1. Abre la pestaña de **tu launchable** (la dirección empieza con `nemoclaw-`) con tu sesión iniciada.
2. Presiona **F12** (en Mac: **Cmd + Opción + I**). Se abre un panel de herramientas a un lado. No vas a cambiar nada ahí, solo copiar un valor.
3. Arriba de ese panel, haz clic en la pestaña **Application**. Si no la ves, haz clic en **»** para ver más pestañas.
4. A la izquierda: **Storage** → **Cookies** → haz clic en la dirección de tu launchable.
5. En la lista, busca el nombre según tu dirección:

   | Tu dirección contiene | Busca la cookie |
   |---|---|
   | `brevlab.com` | `CF_Authorization` |
   | `apps.run.brev.nvidia.com` | `_pomerium` |
   | `gobrev.dev` | `__Host-skybridge-brev-prd` |

6. Haz doble clic en la columna **Value** de esa fila, selecciona todo y copia (**Ctrl + C** o **Cmd + C**).
7. Ve a la lección de NVIDIA, pégalo en **Sesión de acceso** y haz clic en **Probar conexión**.

Deberías ver: `Conexión lista` y la pastilla de arriba en **OpenClaw ✓**.

En Firefox y Safari los pasos son casi iguales; están en la [guía de la clase 4.1](clases/4.1-laboratorio-nemoclaw-en-brev/README.md) (paso 11). `[VERIFICAR EN LAB: capturas de cada paso]`

### Cuando caduca (es normal)

Cada vez que detienes y vuelves a encender la instancia, la cookie anterior deja de servir. Verás **OpenClaw ⚠** o un mensaje como `fresh browser session`. No es un error tuyo:

1. Abre otra vez la pestaña de tu launchable e inicia sesión.
2. Repite los pasos 2 a 7 y copia la cookie nueva.

## 4 · Al terminar el curso

1. Guarda lo que quieras conservar: tu `SOUL.md`, tu skill y tus notas del proyecto (cada guía te dice cómo).
2. En la consola de Brev: tu instancia → **Delete**.
3. Revisa en **Billing** que no quede nada encendido.

## Si algo sale mal

- [Preguntas frecuentes: Brev y el launchable](FAQ.md#brev)
- [Preguntas frecuentes: conexión con la página de NVIDIA](FAQ.md#conexion-laboratorio)
- [Glosario en palabras simples](GLOSARIO.md)
