# Guía de estilo accesible (para quien escribe el curso)

El curso es para **cualquier persona**, no solo para quien programa. Quien ya programa sigue teniendo todo el detalle técnico en las guías, notebooks y cookbooks. Esta guía define cómo escribimos los guiones y la sección «Lo esencial» para que nadie se quede fuera.

## Reglas para los guiones (`clases/<slug>/guion.md`)

1. **No toques la apertura ni el cierre generados.** «La clase pasada aprendimos…» y «En la próxima clase vamos a aprender…» repiten los textos de `tools/course.py` (los de las diapositivas). Si cambias su contenido, se desincronizan.
2. **La idea antes que la herramienta.** Justo después de la apertura: la idea de la clase en una frase y una comparación cotidiana. Usa la comparación de [`GLOSARIO.md`](../GLOSARIO.md) para que todo el curso diga lo mismo.
3. **Máximo 3 palabras nuevas por clase.** Cada una se define la primera vez que se dice, en voz alta, con su comparación del glosario. Todo lo demás se dice con palabras comunes o se omite en el video (queda en la guía escrita).
4. **Navegador antes que terminal.** Si un paso se puede hacer en una página web (consola de Brev, el tablero del laboratorio con su chat, Automations y OpenShell TUI, Colab), se muestra primero ahí. La terminal aparece después, como «la forma de operador»: en el laboratorio es la **VM Terminal** del tablero, con comandos para copiar y pegar.
5. **Antes de cada comando, una frase de para qué sirve.** No «ejecutamos `nemoclaw my-assistant status`», sino «le preguntamos al laboratorio si está sano: ese es el comando `nemoclaw my-assistant status`».
6. **Cada clic se dice en voz alta.** En las clases de laboratorio, los `[HACER]` nombran el botón como aparece en pantalla y dónde está: «el botón **Deploy**, arriba a la derecha».
7. **Los errores se cuentan con calma.** Un error en vivo es normal y tiene arreglo: «esto le va a pasar a mucha gente; mira qué dice y qué hacemos». Nunca «obviamente» ni «es trivial».
8. **Crédito de Brev al final de cada laboratorio.** Antes del cierre: «Si paras por hoy, pulsa **Stop** en la consola de Brev y vuelve pronto: detenida, el disco sigue cobrando». Al final del laboratorio (después de la 6.1): «Ahora sí, **Delete**».
9. **Misma duración.** No agregues más de 30 segundos por clase. Para hacer espacio, mueve detalle técnico a «Notas de producción → Cortes posibles».
10. **Lenguaje.** Tuteo, español neutro, frases cortas. Nada de «simplemente», «obviamente», «trivial», «básicamente». Los nombres de producto (NemoClaw, OpenShell, Brev) se quedan; las siglas se explican o se evitan (di «la dirección del modelo», no «el endpoint»).
11. **Conserva** las demos y el «error en vivo» de cada clase. Ya no usamos marcas `[VERIFICAR EN LAB]`: si algo no está comprobado en el laboratorio, escríbelo sin prometer una salida exacta («deberías ver algo parecido a…», «si tu versión muestra otro texto, sigue con el siguiente paso») y anótalo en la lista privada de pendientes.

## La sección «Lo esencial» (`clases/<slug>/README.md`)

Va justo después de la tabla del encabezado, antes de «Lo que vas a lograr». Formato fijo:

```markdown
## Lo esencial (sin tecnicismos)

**La idea:** dos o tres frases, sin siglas.

**Piénsalo como:** la comparación del glosario.

**Palabras nuevas:** [término 1](../../GLOSARIO.md), [término 2](../../GLOSARIO.md) (máximo 3).

**Hazlo sin programar (≈10 min):** una actividad que se hace leyendo, escribiendo texto normal, presionando ▶ en Colab o haciendo clic en una página web. Nunca la terminal.

**Qué te llevas:** una frase con lo que ahora puedes hacer o decidir.
```

En las clases de laboratorio (4.1 a 4.4, 5.2, 5.3, 6.1) agrega una línea más:

```markdown
**Tu crédito:** esta práctica usa ≈N min de la sesión única del laboratorio (ver [LABORATORIO.md](../../LABORATORIO.md)). Si paras por hoy, pulsa **Stop** y vuelve pronto; al terminar el laboratorio, **Delete**.
```

Ideas de actividades sin programar, según el tipo de clase:

- **Conceptual:** clasificar 5 ejemplos («¿esto es un agente o un chatbot?»), completar una tabla, decidir qué permitirías.
- **Notebook:** abrirlo en Colab, presionar ▶ en orden y responder 3 preguntas sobre lo que ves. Sin leer el código.
- **Laboratorio:** hacer los pasos con clics en el tablero del laboratorio (chat, Automations, OpenShell TUI) y anotar lo que pasó.
- **Escritura:** redactar un `SOUL.md`, una skill o una regla de seguridad en español normal. Es configuración real, no un ejercicio de juguete.
