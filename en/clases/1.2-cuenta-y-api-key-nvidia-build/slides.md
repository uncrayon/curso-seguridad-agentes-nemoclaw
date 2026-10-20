## Your key to the models

:::diagrama c12-tarjeta

Notes:
The API key is a building's access card. Click 1: you, with your free account. Click 2: the key (starts with nvapi-). Click 3: build.nvidia.com, the catalog of NVIDIA-hosted models (OpenAI-compatible API, address https://integrate.api.nvidia.com/v1). Click 4: Nemotron, the course model. Click 5: treat it like a password. Modules 1 to 3 use this address; you don't need your own GPU.

---

## Create the account and the key

:::diagrama c12-pasos-cuenta

Notes:
One click per step: sign in, confirm your email, generate the key in API Keys, copy it right then and try the model in its page's test box. Click 6: the LATAM warning (NemoClaw issues #201 and #214; support at help@build.nvidia.com with your email, the numbers you tried and screenshots). Menu and button names may vary (Generate API Key or Get API Key); if Nemotron's page has no test box, the first call is made with curl.

---

## Where to store it

:::diagrama c12-donde-guardar

Notes:
Click 1: safe places (password manager, Colab Secrets named NVIDIA_API_KEY, a .env file, NVIDIA's course panel, which keeps it in sessionStorage and clears it when the tab closes). Click 2: where never. Click 3: the Colab steps. Local NemoClaw (6.3) uses a different variable name: NVIDIA_INFERENCE_API_KEY. Same key.

---

## If you prefer the terminal

```bash
cp .env.example .env              # private file: paste your key there
read -rs NVIDIA_API_KEY && export NVIDIA_API_KEY   # or just in this terminal
git check-ignore .env             # must print .env
curl -s https://integrate.api.nvidia.com/v1/models \
  -H "Authorization: Bearer $NVIDIA_API_KEY"       # can I reach it? spends no tokens
```

.lead It's optional. Careful: a new terminal doesn't remember your key; load it again.

Notes:
Live error: 401 in a new terminal tab. Check with echo "${NVIDIA_API_KEY:0:6}" that it starts with nvapi-, export it again and repeat. Listing the models spends no tokens and tells you whether the exact ID exists. The full chat curl is on the class page.

---

## First call to the model

:::diagrama c12-primera-llamada

Notes:
Click 1: your question travels with your key. Click 2: Nemotron thinks before answering (that's why max_tokens is 1024). Clicks 3 to 5: the three fields of the answer: content, finish_reason (stop = finished fine) and usage (tokens in and out). Click 6: what a token is. The /v1/chat/completions curl is on the class page.

---

## Watch your credits

:::diagrama c12-creditos

Notes:
Click 1: your credits, like prepaid phone balance. Click 2: every question spends tokens; if you go over the limit, NVIDIA returns 429. Click 3: wait and retry. Click 4: what burns the most. Click 5: free models change; a retired one returns 410, which is why the model lives in NVIDIA_MODEL and isn't hard-coded. Don't quote credit or requests-per-minute numbers: they change; everyone checks their usage in their build.nvidia.com account.

---

## Common errors

| You see | Do this |
|---|---|
| **401** in a new terminal | Load your key again in that terminal |
| **404** | Copy the model's exact name |
| Empty answer and `length` | Give it more room: raise `max_tokens` |
| NVIDIA's course asks for the key again | Normal: it's cleared when the tab closes |
| The SMS never arrives (LATAM) | Write to help@build.nvidia.com |

Notes:
The exact model name comes from the /v1/models list. The course page keeps the key in sessionStorage.

---

## If you leak your key

:::diagrama c12-filtrada

Notes:
One click per step: it leaked, revoke it in API Keys, generate another and update it everywhere (.env, terminal, Colab and NemoClaw). Click 5: deleting the file from the repo isn't enough because the key stays in the git history. Revoking is the only thing that protects you. Do it as soon as you notice.
