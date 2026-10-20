## Most problems aren't agent problems

:::diagrama c13-causas

Notes:
Clicks 1 to 3: the three causes of almost everything (badly copied key, a typo in the model ID, a usage limit). Click 4: NVIDIA answers with a numbered message, like an ATM. Click 5: today we trigger them on purpose and leave the environment verified before Module 2. The goal is that nobody panics over a 401 again.

---

## A model route

:::diagrama c13-ruta-postal

Notes:
The route is an office's postal address. Click 1: the address (base URL, https://integrate.api.nvidia.com/v1). Click 2: the addressee (model ID). Click 3: your signature (the key). Click 4: the course's two routes; embeddings use nvidia/nemotron-3-embed-1b at the same address. Click 5: if a detail is wrong, the letter comes back. In Python: NVIDIA_BASE_URL, NVIDIA_MODEL, NVIDIA_EMBED_MODEL, NVIDIA_API_KEY.

---

## The NVIDIA course panel

:::diagrama c13-panel

Notes:
Click 1: the route's three details (address and model come filled in; the key is kept in sessionStorage). Click 2: the CORS relay checkbox; it gives no key and no access, it only forwards (Python doesn't need it). Click 3: the Embedding route and Request handling dropdowns (60 s wait, 0 to 5 retries; set it to 2). Click 4: Save & verify runs a real test. Click 5: the key is cleared when the tab closes.

---

## The course doctor

:::diagrama c13-doctor

Notes:
Click 1: the notebook and its setup cells. Click 2: LIVE if it found the key; MOCK if not (simulated answers, with simulated errors). Clicks 3 to 7: the five checks (key format, GET /v1/models, chat with latency and usage, the buscar_faq tool, an embedding vector). Click 8: the verdict, "✅ entorno listo" or precise instructions.

---

## Break your environment on purpose

:::diagrama c13-rompe

Notes:
One row per click: fake key → 401; nonexistent model → 404; max_tokens=8 → finish_reason="length" and empty content. The third one isn't an exception: it's an incomplete 200 response. Click 4: diagnostico(e) turns each error into "what happened + what to do". [VERIFY IN LAB] 401 and not 403; 404 and not 400 or 422.

---

## The error table

:::diagrama c13-avisos

Notes:
The ATM messages. Clicks 1 to 4: the ones you fix (401, 403, 404, 410): retrying won't help. Clicks 5 and 6: the ones that fix themselves with a wait (429 and 5xx). Click 7: more waiting or more retries never fix a 401.

---

## Retry with backoff

:::diagrama c13-backoff

Notes:
Clicks 1 to 3: two 429s and success on the third attempt, waiting twice as long each time. Click 4: always with a cap on attempts. Click 5: a 401 is never retried. Only 429, 5xx and network failures are retried; if Retry-After arrives, honor it. The openai client already retries twice (max_retries=2); the code is in section 8 of the notebook.

---

## Common errors

| You see | Do this |
|---|---|
| `Modo: MOCK` even though you saved your key | Check the `NVIDIA_API_KEY` secret and notebook access |
| "Key should start with nvapi-" | Copy the full key, no spaces |
| Empty answer and `length` | Give it more room: raise `max_tokens` |
| "Connection failed" in the panel | Read the number: 401/403 your key · 429 wait · 5xx NVIDIA |

Notes:
If you work on your own machine and get MOCK with .env created: the .env goes at the repo root and you must restart the kernel.

---

## Project milestone

:::diagrama c13-reporte

.lead Soporte NemoClaw gets its first piece: `reporte_entorno()`

Notes:
Click 1: the doctor. Click 2: the secret-free report (Python, mode, routes, checks, latency). Click 3: students paste it when asking for help; in 3.3 the subagents read it to diagnose. Click 4: the notebook's assert guarantees the key never shows up in the report.
