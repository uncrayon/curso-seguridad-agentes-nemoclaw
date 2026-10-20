# 1.1 · What NemoClaw, OpenClaw and OpenShell are

> 🇪🇸 Original Spanish guide: [`clases/1.1-que-son-nemoclaw-openclaw-openshell/README.md`](../../../clases/1.1-que-son-nemoclaw-openclaw-openshell/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Goal: understand what an agent is and what each piece of the stack does before you touch any code.

| | |
|---|---|
| **Video length** | ≈6 min |
| **Practice** | Guided, in the browser (no code, ≈20 min) |
| **Skill** | Place each piece of the stack: OpenClaw, OpenShell and NemoClaw |
| **NVIDIA lesson** | [Course home](https://nvdli.github.io/NemoClawDLI/nemoclaw/index.html) |
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

| Module | Class | Practice | NVIDIA lesson |
|---|---|---|---|
| **1 · Set up your environment** | 1.1 What NemoClaw, OpenClaw and OpenShell are | Browser | Course home |
| | 1.2 Create your NVIDIA Build account and API key | Browser | Course home |
| | 1.3 Configure model routes and diagnose errors | Notebook | Course home |
| **2 · The basic loop** | 2.1 From a single call to the agent loop | Notebook | 1a Loop |
| | 2.2 Reasoning with the ReAct pattern | Notebook | 1b ReAct |
| | 2.3 Turn functions into tools | Notebook | 1c Tools |
| **3 · Coordinate, ground and plan** | 3.1 Route work across several calls | Notebook | 2a Workflows |
| | 3.2 RAG to ground answers in your sources | Notebook | 2b RAG |
| | 3.3 Deep agents that spawn subagents | Notebook | 2c Deep Agents |
| | 3.4 Observe and debug your agent with traces | Notebook | (new) |
| **4 · Take your agent to NemoClaw** | 4.1 Launch the NemoClaw lab on Brev | Lab | 3a Kickstart |
| | 4.2 Explore the OpenClaw gateway and workspace | Lab | 3b OpenClaw |
| | 4.3 Agents in continuous and scheduled operation | Lab | 3c Always-On |
| | 4.4 Swap OpenClaw for Hermes in NemoClaw | Lab | (new) |
| **5 · Secure the agent with OpenShell** | 5.1 The lethal trifecta and the risk surface | Slides | 4a OpenShell |
| | 5.2 Identities and limits with OpenShell | Lab | 4a OpenShell |
| | 5.3 Restrict tools, files and network | Lab | 4a OpenShell |
| **6 · Extend your practice** | 6.1 Compare modern agent CLIs | Lab | 4b Modern CLIs |
| | 6.2 Build your skill library | Notebook | 3c Always-On |
| | 6.3 Next steps and local deployment | Slides | 4c Going Further |

What you need at each stage:

- **Modules 1 to 3**: a free NVIDIA Build API key and Python (Colab or your own machine). You don't need a GPU.
- **Modules 4 to 6**: a [Brev](https://brev.nvidia.com/) account to launch the lab (a cloud machine with NemoClaw already installed) and a desktop browser.

## Step by step (guided practice in the browser)

### 1. Tour NVIDIA's course home page

1. Open <https://nvdli.github.io/NemoClawDLI/nemoclaw/index.html>.
2. If it shows up in another language, use the page's language menu and pick English.
3. Find the **"What this course runs on"** section. You should see three cards:
   - **Models · build.nvidia.com**: the Nemotron models you call with your `nvapi-` key.
   - **Agent stack · NemoClaw launchable on Brev**: the lab for Modules 4 to 6 of our course.
   - **Search · Materials catalog**: the course glossary and articles.
4. Scroll down to the module cards. NVIDIA's course has **4 modules of 3 pages each** (about 4 hours). Our course reorganizes them into **6 modules and 20 classes**: compare with the table above.
5. Open the **"Entering Your API Key"** section. Don't paste anything yet: just find the fields. You'll set them up in class 1.3.
6. Open the **"If a model request fails"** section and read it. It holds the golden rule: on a 401 or 403, check your credentials; on a 429, wait; on a 5xx, the provider may be the problem.

You should see: a page with the NemoClaw mascot holding the OpenShell shield, the course abstract and the learning objectives.

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
- [ ] I found the "Entering Your API Key" section on NVIDIA's course home page.
- [ ] I found `blueprint.yaml` in the NemoClaw repo.
- [ ] I know which modules need Brev and which only need an API key.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| I search for "NemoClaw" as a model on build.nvidia.com and can't call it through the API | NemoClaw isn't a model: it's a blueprint and a CLI. build.nvidia.com has a **blueprint card**, not a chat endpoint | To call a model, use a Nemotron model (class 1.2). You use NemoClaw in the lab |
| NVIDIA's course home page shows up in Spanish or another language | You opened a localized URL (for example, one with `/es/`) or the browser remembered another language | Use <https://nvdli.github.io/NemoClawDLI/nemoclaw/index.html> or the language menu |
| "NVIDIA's Modules 3 and 4 ask me for a launchable" and the numbering confuses me | NVIDIA has 4 modules; we have 6. Their Module 3 is our Module 4 | Use the "NVIDIA lesson" column in the 20-class table |
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

- [NVIDIA DLI course: home](https://nvdli.github.io/NemoClawDLI/nemoclaw/index.html) (NVIDIA, Apache-2.0)
- [NVIDIA's course repository: NVDLI/NemoClawDLI](https://github.com/NVDLI/NemoClawDLI)
- [NemoClaw repository](https://github.com/NVIDIA/NemoClaw) and its [documentation](https://docs.nvidia.com/nemoclaw/latest/)
- [OpenShell repository](https://github.com/NVIDIA/OpenShell)
- [OpenClaw](https://openclaw.ai)
- [Course FAQ (Spanish)](../../../FAQ.md)

---
*Based on the home page of the NVIDIA DLI course "Securing Agents with OpenShell and NemoClaw" (Apache-2.0) and on the NemoClaw documentation.*
