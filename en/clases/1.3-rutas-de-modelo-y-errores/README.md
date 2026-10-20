# 1.3 · Configure model routes and diagnose errors

> 🇪🇸 Original Spanish guide: [`clases/1.3-rutas-de-modelo-y-errores/README.md`](../../../clases/1.3-rutas-de-modelo-y-errores/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Goal: leave your environment verified (chat, tools and embeddings) and know how to read any API error.

| | |
|---|---|
| **Video length** | ≈7 min |
| **Practice** | Notebook [`1.3-rutas-de-modelo-y-errores.ipynb` (Spanish)](../../../clases/1.3-rutas-de-modelo-y-errores/1.3-rutas-de-modelo-y-errores.ipynb) (≈30 min) |
| **Skill** | Configure model routes; diagnose 401, 403, 404, 429 and 5xx errors |
| **Materials** | [Slides](slides.html) · [FAQ (Spanish)](../../../FAQ.md) |

## What you'll achieve

- Configure the two routes the whole course uses, **chat** and **embeddings**, in NVIDIA's course panel and in Python.
- Run the **course doctor**: a notebook that checks your key, models, chat, tools and embeddings, measures latency and shows `usage`.
- Trigger and fix the 401, 404 and `finish_reason=length` errors, and retry a 429 with backoff.

## Before you start

- Your `nvapi-` API key from class 1.2, stored in `.env`, in an environment variable or in Colab Secrets.
- One of these two options:
  - **Google Colab**: upload the notebook or open it from GitHub. The first cell installs everything.
  - **Your machine**: Python 3.10 or later and, from the repo root:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab clases/1.3-rutas-de-modelo-y-errores/
```

No key yet? The notebook still runs in **MOCK mode** (simulated answers and errors) and tells you at the end what's missing.

## The key ideas

### A model route = base URL + model ID + key

| Route | Base URL | Model | What it's for |
|---|---|---|---|
| **Chat** | `https://integrate.api.nvidia.com/v1` | `nvidia/nemotron-3.5-lightning-30b-a3b` | Conversation and tools (Modules 2 to 6) |
| **Embeddings** | `https://integrate.api.nvidia.com/v1` | `nvidia/nemotron-3-embed-1b` | Turning text into vectors for RAG (class 3.2) |

In Python you configure them with `NVIDIA_BASE_URL`, `NVIDIA_MODEL`, `NVIDIA_EMBED_MODEL` and `NVIDIA_API_KEY` (see `.env.example` at the repo root).

### The setup panel in NVIDIA's course

It's on the course home page (the **"Entering Your API Key"** section) and also in lesson 1a. Its fields:

| Field | Default value | What it does |
|---|---|---|
| **Chat API base URL** | `https://integrate.api.nvidia.com/v1` | Where the calls go. HTTPS, ending in `/v1` |
| **Chat model ID** | `nvidia/nemotron-3.5-lightning-30b-a3b` | The model that answers |
| **Chat API bearer key** | — | Your `nvapi-` key. It lives in `sessionStorage`: it's cleared when you close the tab |
| **Use the NVIDIA DLI browser relay** | On, on the course page | CORS relay: it forwards your calls to the NVIDIA API so a static page can make them. It doesn't give you a key or model access |
| **Embedding route (persistent and independent)** (dropdown) | Same URL · `nvidia/nemotron-3-embed-1b` | A separate route; if you don't give it a key, it uses the chat key |
| **Request handling** (dropdown) | Wait 60 s (5–300) · retries 0 (0–5) | Retries only apply to network failures, 429 and 5xx |
| **Save & verify** button | — | Checks the `nvapi-` prefix and makes a test call. If it works, you'll see "✓ Connected." |

## Step by step

### 1. Configure the panel in NVIDIA's course

1. Open <https://nvdli.github.io/NemoClawDLI/nemoclaw/index.html> and scroll down to **"Entering Your API Key"**.
2. Leave the base URL and the model as they are. Paste your key into the key field.
3. Open **Embedding route** and confirm the model is `nvidia/nemotron-3-embed-1b`.
4. Open **Request handling**: leave the wait at 60 s and raise retries to 2.
5. Click **Save & verify**.

You should see: "✓ Connected." with the model's reply, and in the top bar the key pill with a check mark ("Key set ✓"). Below it, a summary: "✓ API key available in this tab", the chat route and the embedding route.

### 2. Open the notebook and run the setup

1. Open [`1.3-rutas-de-modelo-y-errores.ipynb` (Spanish)](../../../clases/1.3-rutas-de-modelo-y-errores/1.3-rutas-de-modelo-y-errores.ipynb).
2. Run the first three cells.

You should see: `Modo: EN VIVO · nvidia/nemotron-3.5-lightning-30b-a3b` (live mode), or `MOCK` if there's no key, and `Doctor listo` (doctor ready).

### 3. Run the doctor's five checks

Run sections 1 to 6 in order. Each one prints a line (the notebook output is in Spanish):

```text
✅ key: nvapi-…abcd (<N> caracteres)
✅ modelos: /models responde y nvidia/nemotron-3.5-lightning-30b-a3b está en el catálogo
✅ chat: respondió en <X> s
✅ tools: el modelo pidió buscar_faq con argumentos JSON válidos
✅ embeddings: vector de <N> dimensiones
```

That is: the key and its length, `/models` answers and lists the course model, chat answered in X seconds, the model requested `buscar_faq` (FAQ search) with valid JSON arguments, and the embedding vector's dimensions.

(Your numbers will differ: key length, latency and vector dimensions.)

In section 4, look at the `usage` block (input and output tokens) and the latency.

### 4. Break your environment on purpose

In section 7 you trigger three failures and read them with `diagnostico()` (diagnosis):

```python
# fake key → 401
OpenAI(base_url=BASE_URL, api_key="nvapi-ESTA-KEY-ES-FALSA-000000000000").chat.completions.create(...)
# nonexistent model → 404
chat([{"role": "user", "content": "hola"}], model="nvidia/modelo-que-no-existe")
# tiny max_tokens → finish_reason="length"
chat([{"role": "user", "content": "Explica qué es un agente de IA."}], max_tokens=8)
```

You should see: for the 401, "Key rechazada: revisa que NVIDIA_API_KEY sea la key completa…" (key rejected: check that `NVIDIA_API_KEY` is the full key); for the 404, "Ese modelo o esa ruta no existen…" (that model or route doesn't exist); and for the third, `finish_reason: length` with empty or truncated content.

### 5. Retry a 429 with backoff

Section 8 defines `con_reintentos()` (with retries): it waits 1 s, 2 s, 4 s… (and honors `Retry-After` if it arrives), only for 429, 5xx and network failures. You should see:

```text
   ⏳ intento 1 falló con 429; espero 0.21 s
   ⏳ intento 2 falló con 429; espero 0.41 s
Caso 429: respuesta al tercer intento
Caso 401:
   ✋ No reintento (intento 1): 401 · Key rechazada: …
```

In other words: attempts 1 and 2 fail with 429 and it waits a little longer each time; the 429 case gets an answer on the third attempt; the 401 case is never retried.

### 6. Read the verdict

The last cell prints **✅ entorno listo** (environment ready) or the list of checks that failed, each with its fix.

### API error table

| Code | What it means | Retry? | What to do |
|---|---|---|---|
| **401** | Key rejected | Never | Full key, with `nvapi-`, no quotes or spaces. If you regenerated it, the old one no longer works |
| **403** | Valid key without access to that model or route | No | Check your account on build.nvidia.com or use another model |
| **404** | Model or route doesn't exist | No | Copy the exact ID from `/v1/models`; `BASE_URL` must end in `/v1` |
| **410** | Model retired from the free endpoint | No | Change `NVIDIA_MODEL` to a current model |
| **429** | Rate limit | Yes, with a wait | Exponential backoff; don't run cells in bursts |
| **5xx** | Server failure or model starting up | Yes, with a wait | Retry in 30–60 s; if it persists, try another model |
| `finish_reason="length"` | `max_tokens` ran out | — | Raise `max_tokens` |

More wait time or more retries **never** fix a 401 or a 403.

## Check that it worked

- [ ] "Save & verify" on NVIDIA's page showed "✓ Connected.".
- [ ] The notebook ended in **✅ entorno listo** (environment ready), or I know exactly what I'm missing.
- [ ] I saw the latency and the `usage` block of a call.
- [ ] I triggered a 401, a 404 and a `finish_reason=length`, and understood each diagnosis.
- [ ] I know which errors get retried (429, 5xx) and which don't (401, 403, 404, 410).

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| The notebook says `Modo: MOCK` even though you created `.env` | `.env` isn't at the repo root, or you opened Jupyter from another folder, or you didn't restart the kernel | Put `.env` at the repo root (next to `.env.example`) and restart the kernel. In Colab, use Secrets |
| In Colab: `Modo: MOCK` even though you created the secret | The name isn't exactly `NVIDIA_API_KEY`, or notebook access isn't turned on | Check the name and the toggle in the 🔑 panel and run everything again |
| `401 · Key rechazada` (key rejected) | Key incomplete, with quotes, with spaces, or revoked | Section 1 of the notebook tells you which one. Copy the key again |
| `404 · Ese modelo o esa ruta no existen` (that model or route doesn't exist) | Model ID copied wrong, or `BASE_URL` without `/v1` | Copy the ID from the list in section 3 |
| `⚠ finish_reason=length sin contenido` (no content) | `max_tokens` too low for a model that reasons | Raise `max_tokens` (1024 or more) |
| On NVIDIA's page: "Key should start with nvapi-" | You pasted something else, or the key has a leading space | Copy the full key from build.nvidia.com |
| On NVIDIA's page: "Connection failed: …" when saving | The connection test failed; the panel rolls back your changes | Read the message: 401/403 is the key; 429, wait; 5xx, the provider or the relay. Try again once |
| "Model API base URL must use HTTPS" or 404 on everything | You changed the base URL by mistake | Reset it to `https://integrate.api.nvidia.com/v1` |
| The tools cell says the model answered with text instead of requesting the tool | The model sometimes skips the tool, or you picked a model without tool support | Run the cell once more; if it persists, go back to the default model |

## Challenge

Turn the notebook into a single `doctor()` function that runs the five checks and returns the environment report.

**Success criteria:** with your normal setup it ends in "✅ entorno listo"; with `MODEL = "nvidia/nemotron-3.5-lightning"` (incomplete ID) the report marks `modelos` and `chat` as failed and the fix mentions the exact ID; and the report never contains your key.

## Project milestone

Soporte NemoClaw (NemoClaw Support) gets its first piece of code: **`reporte_entorno()`** (environment report, section 10 of the notebook). It returns a secret-free summary: Python version, mode, routes, the status of each check and latency. It's what a student will paste when asking for help, and in class 3.3 the Soporte NemoClaw subagents will read it to put together a diagnosis. Save your function.

## Resources

- Home page and setup panel of the NVIDIA DLI course. This class is based on them (Apache-2.0).
- [NVIDIA Build: model catalog](https://build.nvidia.com/?ncid=ref-dli-146986)
- [NemoClawDLI issue #106: the retired model that returned 410](https://github.com/NVDLI/NemoClawDLI/issues/106)
- [Course FAQ (Spanish)](../../../FAQ.md)

---
*Based on the home page and setup panel of the NVIDIA DLI course "Securing Agents with OpenShell and NemoClaw" (Apache-2.0).*
