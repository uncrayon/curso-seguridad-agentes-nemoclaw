# 1.2 · Create your NVIDIA Build account and API key

> 🇪🇸 Original Spanish guide: [`clases/1.2-cuenta-y-api-key-nvidia-build/README.md`](../../../clases/1.2-cuenta-y-api-key-nvidia-build/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Goal: have an `nvapi-` API key stored safely and a first model call that answers.

| | |
|---|---|
| **Video length** | ≈6 min |
| **Practice** | Guided, in the browser and the terminal (≈20 min) |
| **Skill** | Manage API usage in NVIDIA Build |
| **Materials** | [Slides](slides.html) · [FAQ (Spanish)](../../../FAQ.md) |

## What you'll achieve

- Create your free account on build.nvidia.com and generate your `nvapi-` API key.
- Store the key in three correct places (`.env`, an environment variable and Colab Secrets) without it ending up on GitHub.
- Make your first `curl` calls to `/v1/models` and `/v1/chat/completions`, and know what to do if you leak the key.

## Before you start

- An email address you can access and a phone for SMS verification (read the first common error if you're outside the US).
- A terminal: Terminal on macOS, a Linux terminal, or on Windows **Git Bash** or **WSL**. If you only have PowerShell, there's a variant below.
- `curl` and `python3` installed (`curl --version` and `python3 --version`).
- To store the key in `.env`: a clone of the course repo.

> **Tip:** create your account and your key **before** you start the course. If phone verification fails, the fix can take a few days.

## Step by step

### 1. Create your NVIDIA Build account

1. Open <https://build.nvidia.com/?ncid=ref-dli-146986>.
2. Click the sign-in button and create an NVIDIA account with your email (or sign in with one you already have).
3. Confirm your email with the link you receive.
4. If at some point it asks you to verify your phone (it may be when you create the account or when you generate the key), enter your number with the country code, then the SMS code.

You should see: the build.nvidia.com model catalog with you signed in (your avatar at the top right).

### 2. Generate your API key

1. Open your account menu and go to the **API Keys** page. You can also open a model's page, for example Nemotron, and use the button to generate your API key (it may say *Generate API Key* or *Get API Key*).
2. Generate a new key. If it lets you name it, use something like `curso-platzi-nemoclaw`. If it lets you choose an expiration, pick a short one: you'll regenerate it when you finish the course. If you don't see those options, go on to the next step.
3. Copy the key **right then**. It starts with `nvapi-` and it's long.

You should see: text like `nvapi-xxxxxxxx…`. Treat it like a password.

> ⚠️ Never paste your key into a notebook you'll share, a chat message, a screenshot or a commit.

### 3. Store it properly (pick based on where you work)

#### Option A · `.env` file (for your machine)

The repo ships an `.env.example` file at the root with the course's four variables:

| Variable | What it's for | Default value |
|---|---|---|
| `NVIDIA_API_KEY` | Your key | (yours) |
| `NVIDIA_BASE_URL` | The endpoint | `https://integrate.api.nvidia.com/v1` |
| `NVIDIA_MODEL` | The chat model | `nvidia/nemotron-3.5-lightning-30b-a3b` |
| `NVIDIA_EMBED_MODEL` | The embedding model | `nvidia/nemotron-3-embed-1b` |

```bash
# from the root of the course repo
cp .env.example .env
# open .env in your editor and replace nvapi-xxxxxxxx… with your real key
git check-ignore .env      # must print ".env": it means git ignores it
```

You should see: `.env` printed by `git check-ignore`. If it prints nothing, **don't commit**, and check that `.gitignore` has the line `.env`.

#### Option B · Environment variable (for the terminal)

To keep the key out of your terminal history, read it without displaying it:

```bash
read -rs NVIDIA_API_KEY && export NVIDIA_API_KEY   # paste the key and press Enter (it won't show)
echo "${NVIDIA_API_KEY:0:6}…"                      # must print nvapi-…
```

The variable only exists in **that** terminal. If you open another tab, you have to do it again.

#### Option C · Google Colab Secrets

1. In Colab, open the left panel and click the key icon 🔑 (**Secrets**).
2. Add a secret with the exact name `NVIDIA_API_KEY` and paste your key as the value.
3. Turn on the **notebook access** toggle.

The course notebooks read it on their own with `userdata.get("NVIDIA_API_KEY")`.

#### What about NVIDIA's course page?

There, you paste the key into the setup panel on the course home page. The page stores it in `sessionStorage`: **it's cleared when you close the tab**. That's why it asks for it again each time you open the course in a new tab. The URL and the model are remembered.

#### A different name for NemoClaw

In the course notebooks the variable is called `NVIDIA_API_KEY`. The NemoClaw installer, which you'll use if you run it on your own machine (class 6.3), uses another name: `NVIDIA_INFERENCE_API_KEY`. It's the same key in a different variable.

### 4. First call: list the models

`/v1/models` doesn't spend tokens. It's the cheapest way to check that you can reach the endpoint.

```bash
curl -s https://integrate.api.nvidia.com/v1/models \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  | python3 -c "import sys, json; ids = [m['id'] for m in json.load(sys.stdin)['data']]; print(len(ids), 'modelos'); print('nvidia/nemotron-3.5-lightning-30b-a3b' in ids)"
```

You should see: a model count (printed as `<N> modelos`) and `True` (the course model is in the catalog).

### 5. First call to the chat model

```bash
curl -s https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
    "messages": [{"role": "user", "content": "Greet a Platzi student in one sentence."}],
    "max_tokens": 1024
  }' | python3 -m json.tool
```

You should see a JSON response with, among other things:

- `choices[0].message.content`: the greeting.
- `choices[0].finish_reason`: `"stop"` (it finished cleanly).
- `usage`: `prompt_tokens`, `completion_tokens` and `total_tokens`. That's what you spent.

Why `max_tokens: 1024` for a single sentence? The course model **reasons before it answers**, and that reasoning also spends tokens. With a very low limit, the answer can come back empty with `finish_reason: "length"`. You'll trigger this on purpose in class 1.3.

**PowerShell variant (Windows):**

```powershell
$env:NVIDIA_API_KEY = Read-Host "Paste your key"
$body = @{ model = "nvidia/nemotron-3.5-lightning-30b-a3b"; max_tokens = 1024;
           messages = @(@{ role = "user"; content = "Say hello in one sentence." }) } | ConvertTo-Json -Depth 5
Invoke-RestMethod -Uri "https://integrate.api.nvidia.com/v1/chat/completions" -Method Post `
  -Headers @{ Authorization = "Bearer $env:NVIDIA_API_KEY" } -ContentType "application/json" -Body $body
```

### 6. Watch your credits and your limits

- The free NVIDIA Build account gives you access to hosted models with **usage limits**: credits or requests per minute. The numbers change over time: check your usage and credits in your build.nvidia.com account.
- When you go over the per-minute limit, the API returns **429**. Wait and retry (in 1.3 you write a retry with backoff).
- What burns the most: loops with no step limit, running cells in rapid bursts, and huge `max_tokens`. In "Agent Fundamentals" your loop will always have a maximum number of steps.
- Free models **change**. A retired model returns **410**. It happened to NVIDIA's course with `nvidia/nemotron-3-nano-30b-a3b`. That's why the model lives in a variable (`NVIDIA_MODEL`) and isn't hard-coded.

### 7. If you leak your key

If your key showed up in a commit, a screenshot, a shared notebook or a chat:

1. Go to **API Keys** on build.nvidia.com and **revoke** (delete) that key. The button may say *Revoke* or *Delete*, or show as a trash-can icon.
2. Generate a new one.
3. Update it everywhere: `.env`, your environment variables, Colab Secrets and, if you already used it there, NemoClaw (class 6.3).
4. If you pushed it to GitHub, deleting the file **isn't enough**: the key stays in the history. Revoking it is what protects you.

## Check that it worked

- [ ] I have a key that starts with `nvapi-`.
- [ ] `git check-ignore .env` prints `.env` (or I use Colab Secrets).
- [ ] `/v1/models` returned a list and `True`.
- [ ] The chat call answered with `finish_reason: "stop"` and I saw the `usage` block.
- [ ] I know where to revoke my key if I leak it.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| Phone verification fails with your Latin American number, or you see "number has requested too many" | Known SMS verification issue with numbers outside the US (NemoClaw issues [#201](https://github.com/NVIDIA/NemoClaw/issues/201) and #214). It's not a NemoClaw bug and it's not your fault | Email help@build.nvidia.com with your registered email, the numbers you tried and screenshots, or use developer.nvidia.com/support. Do it days ahead of time |
| `curl` returns **401** | The variable is empty in this terminal (you opened another tab), or the key has quotes or spaces | `echo "${NVIDIA_API_KEY:0:6}"` must print `nvapi-`. If it's empty, redo step 3B |
| `curl` returns **404** | The model ID has a typo, or the URL doesn't end in `/v1/...` | Copy the ID from the `/v1/models` list. Check the full URL |
| `"content": null` or empty, and `"finish_reason": "length"` | `max_tokens` too low: the model spent it all reasoning | Raise `max_tokens` to 1024 or more |
| The API returns **429** | You went over the requests-per-minute limit | Wait a few seconds and try again. Don't fire requests in bursts |
| NVIDIA's course page asks for the key again | The key is stored in `sessionStorage` and is cleared when you close the tab | That's for security. Paste it again in the panel on the course home page |
| In PowerShell, `curl -H ...` fails with a parameter error | In Windows PowerShell, `curl` is an alias for `Invoke-WebRequest` | Use the `Invoke-RestMethod` variant, or `curl.exe`, or Git Bash |
| `KeyError: 'data'` when listing models | The response was an error (for example, a 401), not a list | Remove the `python3 -c` part and look at the error JSON |

## Challenge

Make the chat call answer in **fewer than 15 words** and spend **fewer output tokens** than your first call, without coming back empty.

**Success criteria:** `finish_reason` is `"stop"`, the content isn't empty, and `usage.completion_tokens` is lower than in your first call. Hint: change the prompt, not just `max_tokens`.

## Project milestone

Soporte NemoClaw (NemoClaw Support) now has **credentials**. Your `.env` (or your Colab Secrets) with the four variables is what every notebook in the project will read, from class 1.3 to 6.2. And you already have the first answer the agent will know how to give: "What do I do if my key leaked?". You'll find it in the course FAQ.

## Resources

- [NVIDIA Build](https://build.nvidia.com/?ncid=ref-dli-146986): model catalog and your API keys
- Home page of the NVIDIA DLI course, "Entering Your API Key" section. This class is based on it (Apache-2.0).
- [NemoClaw issue #201: phone verification](https://github.com/NVIDIA/NemoClaw/issues/201)
- [Credential rotation in NemoClaw](https://docs.nvidia.com/nemoclaw/latest/) (the *Credential Rotation* page, for when you use NemoClaw locally)
- [Course FAQ (Spanish)](../../../FAQ.md)

---
*Based on the home page of the NVIDIA DLI course "Securing Agents with OpenShell and NemoClaw" (Apache-2.0).*
