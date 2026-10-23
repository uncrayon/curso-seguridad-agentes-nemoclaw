# Agentes Seguros con NemoClaw

**Platzi × NVIDIA Deep Learning Institute** · Curso práctico en español · Instructor: Ulises Rayón

👉 **Abre el curso aquí: https://uncrayon.github.io/curso-seguridad-agentes-nemoclaw/**

Vas a entender qué es un agente de IA, construir uno paso a paso, llevarlo a un laboratorio real con **NVIDIA NemoClaw** y encerrarlo de forma segura con **OpenShell**. No necesitas saber programar: cada clase empieza con **«Lo esencial»**, en palabras simples, con una actividad que haces sin código. Quien ya programa tiene todo el detalle técnico en la misma página.

## Cómo tomar el curso

1. Mira el video de la clase en Platzi.
2. Abre la página de la clase en el [sitio del curso](https://uncrayon.github.io/curso-seguridad-agentes-nemoclaw/): ahí están «Lo esencial», las diapositivas, la práctica y el glosario.
3. Los notebooks se abren en Colab con un clic y funcionan aunque todavía no tengas API key.
4. Desde el módulo «Crea tu agente con NemoClaw» usas un laboratorio en la nube (Brev). Antes, lee [Tu laboratorio en Brev](https://uncrayon.github.io/curso-seguridad-agentes-nemoclaw/LABORATORIO.html) para que te alcance el crédito.

¿Una palabra nueva? Está en el [glosario](https://uncrayon.github.io/curso-seguridad-agentes-nemoclaw/GLOSARIO.html). ¿Algo falla? Revisa las [preguntas frecuentes](https://uncrayon.github.io/curso-seguridad-agentes-nemoclaw/FAQ.html).

## Para quien programa

Todo el sitio se genera desde este repositorio:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r tools/requirements.txt
python3 tools/build_all.py          # notebooks, diapositivas, páginas de las guías y portada
python3 tools/check_notebooks.py    # corre los notebooks sin API key (modo simulado)
```

| Carpeta | Qué tiene |
|---|---|
| `clases/<clase>/` | Guía (`README.md` → `index.html`), diapositivas (`slides.md` → `slides.html`), notebook o recetario de terminal |
| `en/` | Portada, guías y diapositivas en inglés |
| `datos/faq/` | La FAQ del curso, que el agente del proyecto usa como base de conocimiento |
| `skill-library/` | Skills de ejemplo para la clase 6.2 (material complementario) |
| `assets/` | Estilos (Platzi Sinapsis), tipografías, íconos y scripts de las diapositivas |
| `tools/` | Los generadores del sitio y de los notebooks |

## Créditos

Basado en el curso open source [«Securing Agents with OpenShell and NemoClaw»](https://github.com/NVDLI/NemoClawDLI) de NVIDIA Deep Learning Institute (Apache-2.0) y en [NVIDIA NemoClaw](https://github.com/NVIDIA/NemoClaw). Los notebooks, guías, diapositivas, glosario y FAQ son material original de Platzi que sigue el orden y los conceptos del curso de NVIDIA. NVIDIA, NemoClaw y OpenShell son marcas de NVIDIA Corporation; este no es un producto oficial de NVIDIA. Platzi y su logotipo son marcas de Platzi.
