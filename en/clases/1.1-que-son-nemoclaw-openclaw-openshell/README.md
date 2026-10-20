# 1.1 · What NemoClaw, OpenClaw and OpenShell are

> 🇪🇸 Original Spanish guide: [`clases/1.1-que-son-nemoclaw-openclaw-openshell/README.md`](../../../clases/1.1-que-son-nemoclaw-openclaw-openshell/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Goal: understand what an agent is and what each piece of the stack does before you touch any code.

| | |
|---|---|
| **Video length** | ≈6 min |
| **Practice** | Guided, in the browser (no code, ≈20 min) |
| **Skill** | Place each piece of the stack: OpenClaw, OpenShell and NemoClaw |
| **Materials** | [Slides](slides.html) · [FAQ (Spanish)](../../../FAQ.md) |

## What you'll achieve

- Explain in your own words what an AI agent is: a model inside a loop, with tools and memory.
- Tell apart OpenClaw (the agent), OpenShell (the sandbox and the gateway) and NemoClaw (the blueprint and the CLI that ties them together).
- Know what you'll build across the 20 classes and what you need for each module.

## Before you start

- A desktop browser (Chrome, Edge or Firefox). From Module 4 on you'll need its developer tools, so don't take this course on your phone.
- Nothing else. This class needs no account, no GPU and no installs.

## The key ideas

### What an agent is

A **language model** (LLM) on its own takes text in and returns text. An **agent** is that model placed inside a **loop** (a cycle that repeats):

1. **Observe**: it reads the request and what has happened so far (its memory).
2. **Decide**: the model picks the next step: answer, or use a tool (a function your code runs on its behalf).
3. **Act**: your code runs the tool and hands the result back.
4. **Stop?**: if it's done, it answers; if not, it goes back to step 1.

The problem: an agent with tools can read files, run commands and connect to the internet. If someone tricks it with an instruction hidden in a document, it can do real damage. That's why this course is about **agent security**.

### The three pieces

The definitions come from the [NemoClaw documentation](https://docs.nvidia.com/nemoclaw/latest/) (the *Ecosystem* page):

| Piece | What it is | Analogy |
|---|---|---|
| **OpenClaw** | The agent: the assistant with its runtime, tools, memory and behavior, inside the container. It's a third-party project ([openclaw.ai](https://openclaw.ai)). It doesn't define the sandbox. | The employee |
| **OpenShell** | NVIDIA's runtime environment: it creates and watches the **sandbox** (an isolated container), enforces network, file and process policies, and routes inference (the calls to the model). It has a **gateway** on the host and the `openshell` CLI. | The office with locks and a guard at the door |
| **NemoClaw** | NVIDIA's reference stack: the `nemoclaw` CLI, a **versioned blueprint** (a YAML package with the exact versions, the image and the policies) and a plugin for OpenClaw. It sets up and runs everything above. | The contractor who builds the office and hires the employee |

Three things people often mix up:

- **NemoClaw is not a model.** Models (Nemotron, for example) live on build.nvidia.com and you call them through an API.
- **OpenShell works without NemoClaw.** NemoClaw adds a stricter policy, a hardened image and blueprint verification on top.
- **Your API key never enters the sandbox.** OpenShell keeps it outside and injects it into the outbound request to the model.

### The flow, as text

```text
You (operator)
  │  nemoclaw onboard · nemoclaw <name> connect · nemoclaw <name> status
  ▼
nemoclaw (CLI on the host) ──── reads the versioned blueprint (YAML with pinned versions)
  │  calls the openshell CLI
  ▼
OpenShell gateway (host) ── policies · inference routes · credentials
  │  creates and watches
  ▼
Sandbox (container, user "sandbox"; only /sandbox and /tmp are writable)
  └── OpenClaw (the agent) + NemoClaw plugin
        │ wants to talk to the model         │ wants to reach the internet
        ▼                                     ▼
  inference route → build.nvidia.com     network policy: everything blocked
  (the key is added outside the sandbox)  except what's on the list
```

### What you'll build: the "Soporte NemoClaw" project

Throughout the course you build **Soporte NemoClaw** (NemoClaw Support), an agent that answers students' questions about NemoClaw, Brev and the course itself, using the course FAQ as its knowledge base. It grows class by class:

| Module | What you add |
|---|---|
| 2 | A chat loop with memory, the ReAct pattern and real tools (`buscar_faq` (FAQ search), `estimar_costo_brev` (Brev cost estimate)) |
| 3 | A triage router, RAG over the FAQ with citations, and subagents that put together a diagnostic report |
| 4 | You deploy it in OpenClaw as a skill inside the Brev lab, with a scheduled task |
| 5 | You analyze its risks and write its sandbox policy |
| 6 | You build your skill library and see how to run it on your own machine |

### The map of the 20 classes

| Module | Class | Practice |
|---|---|---|
| **1 · Set up your environment** | 1.1 What NemoClaw, OpenClaw and OpenShell are | Browser |
| | 1.2 Create your NVIDIA Build account and API key | Browser |
| | 1.3 Configure model routes and diagnose errors | Notebook |
| **2 · The basic loop** | 2.1 From a single call to the agent loop | Notebook |
| | 2.2 Reasoning with the ReAct pattern | Notebook |
| | 2.3 Turn functions into tools | Notebook |
| **3 · Coordinate, ground and plan** | 3.1 Route work across several calls | Notebook |
| | 3.2 RAG to ground answers in your sources | Notebook |
| | 3.3 Deep agents that spawn subagents | Notebook |
| | 3.4 Observe and debug your agent with traces | Notebook |
| **4 · Take your agent to NemoClaw** | 4.1 Launch the NemoClaw lab on Brev | Lab |
| | 4.2 Explore the OpenClaw gateway and workspace | Lab |
| | 4.3 Agents in continuous and scheduled operation | Lab |
| | 4.4 Swap OpenClaw for Hermes in NemoClaw | Lab |
| **5 · Secure the agent with OpenShell** | 5.1 The lethal trifecta and the risk surface | Slides |
| | 5.2 Identities and limits with OpenShell | Lab |
| | 5.3 Restrict tools, files and network | Lab |
| **6 · Extend your practice** | 6.1 Compare modern agent CLIs | Lab |
| | 6.2 Build your skill library | Notebook |
| | 6.3 Next steps and local deployment | Slides |

What you need at each stage:

- **Modules 1 to 3**: a free NVIDIA Build API key and Python (Colab or your own machine). You don't need a GPU.
- **Modules 4 to 6**: a [Brev](https://brev.nvidia.com/) account to launch the lab (a cloud machine with NemoClaw already installed) and a desktop browser.

## Step by step (guided practice in the browser)

### 1. Tour the course home page

1. Open the [course home page](../../../index.html): it's the link under the video, and from there you can reach all the course materials. It's in Spanish; there's also an [English overview](../../index.html) with the same class-by-class map.
2. Read **"¿No programas? Este curso también es para ti"** ("Don't code? This course is for you too"). It makes three points: every class opens with «Lo esencial» (The essentials: the idea in plain words and an activity with no coding), the notebooks run with one click in Colab even before you have an API key, and the lab runs from the browser, with nothing to install.
3. Scroll down to **"Cómo funciona el curso"** (How the course works) and find the three stages: your access to models (a free `nvapi-` API key, all you need for Modules 1 to 3), the notebooks in Colab or on your machine, and the real lab on Brev from Module 4 on.
4. Look at **"El stack en un vistazo"** (The stack at a glance): one card per piece (OpenClaw, the agent; OpenShell, the sandbox; NemoClaw, the blueprint) and a diagram showing that your API key stays outside the sandbox. Compare it with the "three pieces" table above.
5. Read **"Proyecto del curso: «Soporte NemoClaw»"** (Course project): it shows how the agent grows from Module 2 to Module 6.
6. Scroll down to **"Clase por clase"** (Class by class): 6 modules and 20 classes. Each card shows the length, what you'll learn and its links: **Guía** (the class guide, like this page), **Diapositivas** (slides) and, depending on the class, **Colab** (the notebook, which opens in your browser) or **Recetario** (the lab's command recipes). Compare it with the table above and find class 1.3: it's the first one with a Colab button.
7. Read **"Los errores que más vas a ver"** (The errors you'll see most). It holds the golden rule: on a 401 or 403, check your key and your account; on a 404 or 410, check the model name; on a 429, wait a few seconds and retry.
8. Find the support pages: the **Glosario** (glossary, button at the top), **Tu laboratorio en Brev** (your Brev lab: the «plan del laboratorio» link in the first section, covering what it costs and how to make your credit last) and the **Preguntas frecuentes** (FAQ), with more than 50 solved cases. Bookmark the home page.

You should see: at the top, the course title with the buttons "Empieza con la clase 1.1" (Start with class 1.1), "Consigue tu API key" (Get your API key), "Laboratorio en Brev" (Brev lab), "Preguntas frecuentes" and "Glosario", and the line "6 módulos · 20 clases".

### 2. Tour the NemoClaw repository

1. Open <https://github.com/NVIDIA/NemoClaw> and read the top of the README.
2. Find the sentence that defines the project. You should see something like: an open source reference stack for running agents more safely inside OpenShell sandboxes.
3. Notice the **alpha / early preview** label. NemoClaw ships new versions every 1 to 3 days. That's why the lab always uses a pinned version.
4. Find the `nemoclaw-blueprint/` folder and open `blueprint.yaml`. You don't need to understand all of it. Find:
   - the minimum and maximum OpenShell versions,
   - the minimum OpenClaw version,
   - the inference profiles (`components.inference.profiles`), which point to `https://integrate.api.nvidia.com/v1`.

### 3. Tour the documentation

1. Open <https://docs.nvidia.com/nemoclaw/latest/>.
2. Find the **Ecosystem** page (in the *About* section). It has the table with the scope of OpenClaw, OpenShell and NemoClaw that we summarized above.
3. Find **How it works**. Locate the table of **protection layers**: network, filesystem, process and inference. Write down which ones you can change on the fly (network and inference) and which ones are locked when the sandbox is created (filesystem and process). You'll use this in Module 5.

### 4. Fill in your map

Copy this table into your notes and fill it in with your own words:

| Piece | What it does | Where you'll see it in the course |
|---|---|---|
| Model (Nemotron) | | |
| OpenClaw | | |
| OpenShell | | |
| NemoClaw | | |
| Brev | | |

## Check that it worked

- [ ] I can explain in one sentence what separates a model call from an agent.
- [ ] I know which piece is the agent, which is the sandbox and which is the blueprint.
- [ ] I found the "Clase por clase" (class by class) section on the course home page and I know which links each card has.
- [ ] I found `blueprint.yaml` in the NemoClaw repo.
- [ ] I know which modules need Brev and which only need an API key.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| I search for "NemoClaw" as a model on build.nvidia.com and can't call it through the API | NemoClaw isn't a model: it's a blueprint and a CLI. build.nvidia.com has a **blueprint card**, not a chat endpoint | To call a model, use a Nemotron model (class 1.2). You use NemoClaw in the lab |
| I think I need a GPU to get started | Modules 1 to 3 call NVIDIA-hosted models through an API | You only need the free key. The GPU arrives with Brev in Module 4, and it isn't yours: it's in the cloud |
| Instructions from a blog post don't match the NemoClaw repo | NemoClaw is in alpha and changes every few days | Trust the official README and documentation, and the lab's pinned version |

## Challenge

Write a paragraph of at most 5 lines that explains to a classmate what happens when OpenClaw tries to reach a website that isn't in the policy.

**Success criteria:** your paragraph names the three pieces with their correct roles, says the connection is blocked by default, and says where the API key lives (outside the sandbox).

## Project milestone

There's no code yet. Your milestone is the **Soporte NemoClaw map**: in your notes, draw the flow diagram above and mark where each part of the project will live:

- The Python loop (Modules 2 and 3): outside any sandbox, in your notebook.
- The `soporte-nemoclaw` skill (NemoClaw support skill) and the FAQ (Module 4): inside the OpenClaw workspace, in the sandbox.
- The policy that contains it (Module 5): in OpenShell.

## Resources

- [Course home page (Spanish)](../../../index.html), [English overview](../../index.html), [glossary (Spanish)](../../../GLOSARIO.md) and [your Brev lab (Spanish)](../../../LABORATORIO.md)
- Home page of the NVIDIA DLI course. This class is based on it (Apache-2.0).
- [NVIDIA's course repository: NVDLI/NemoClawDLI](https://github.com/NVDLI/NemoClawDLI)
- [NemoClaw repository](https://github.com/NVIDIA/NemoClaw) and its [documentation](https://docs.nvidia.com/nemoclaw/latest/)
- [OpenShell repository](https://github.com/NVIDIA/OpenShell)
- [OpenClaw](https://openclaw.ai)
- [Course FAQ (Spanish)](../../../FAQ.md)

---
*Based on the home page of the NVIDIA DLI course "Securing Agents with OpenShell and NemoClaw" (Apache-2.0) and on the NemoClaw documentation.*
