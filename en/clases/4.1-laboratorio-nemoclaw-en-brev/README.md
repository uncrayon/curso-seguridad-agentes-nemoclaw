# 4.1 · Spin up the NemoClaw lab on Brev

> 🇪🇸 Original Spanish guide: [`clases/4.1-laboratorio-nemoclaw-en-brev/README.md`](../../../clases/4.1-laboratorio-nemoclaw-en-brev/README.md). Slides, notebooks, cookbooks and video are in Spanish.

Deploy the NemoClaw launchable on Brev, connect from the browser and from the terminal, verify the 4 routes, and learn to pause it without burning extra credits.

| | |
|---|---|
| Video length | ≈9 min |
| Practice | Lab on Brev: NVIDIA course page + terminal ([cookbook.md (Spanish)](../../../clases/4.1-laboratorio-nemoclaw-en-brev/cookbook.md)) |
| Skill | Deploy NemoClaw on Brev |

Materials: [slides](slides.html) · [terminal cookbook (Spanish)](../../../clases/4.1-laboratorio-nemoclaw-en-brev/cookbook.md) · [FAQ (Spanish)](../../../FAQ.md)

> Based on lesson 03a-kickstart from the NVIDIA DLI course (Apache-2.0).

## What you'll achieve

- Have your own NemoClaw lab running on Brev: OpenClaw (the agent) inside OpenShell (the sandbox).
- Connect in two ways: from the NVIDIA course page (browser) and from your terminal with the `brev` CLI.
- Stop and resume the instance, knowing what each state costs.

## Before you start

- Your `nvapi-` API key from class 1.2, saved in the NVIDIA course page panel (we use it for the control step).
- A desktop browser with developer tools: Chrome, Edge, Brave, Firefox, or Safari. It doesn't work from a phone.
- An NVIDIA account (the same one you use for build.nvidia.com) to sign in to Brev.
- For the terminal route: macOS, Linux, or Windows with WSL (Ubuntu 22.04 or later). The `brev` CLI doesn't run on native Windows.
- 20 unhurried minutes: the deployment takes 5 to 15 minutes.

The pieces you're about to spin up, one sentence each:

| Piece | What it does |
|---|---|
| Model endpoint | Turns a prompt into text. It remembers nothing between calls. |
| OpenClaw | The agent (the *harness*): it keeps the session history, a file workspace, and the tools. |
| OpenShell | The sandbox: it limits which files, network, and processes the agent can reach. |
| NemoClaw | The blueprint that configures OpenClaw inside OpenShell. |

## Step by step

### Part A · Deploy the launchable

1. **Sign in to Brev.** Open https://brev.nvidia.com and sign in with your NVIDIA account.
   You should see: the Brev console with sections like **GPUs**, **Launchables**, and **Billing**.

2. **Check your organization.** In Brev, credits and instances belong to an *organization*, not to your user. If you were invited to several (for example, your company's and your personal one), check which one is active before you deploy. `[VERIFY IN LAB: where the organization selector is in the console, and whether a new account gets a personal organization automatically]`

3. **Check your credits.** Go to **Billing**. There you see your balance, and you can redeem a code under **Credits → Redeem a credit code**. The NVIDIA course page says NVIDIA covers the cost of Brev for a limited time with a USD 1 credit for the first 25,000 users (one per person), enough for the 4 modules. `[VERIFY IN LAB: whether the credit is still available, and whether it applies automatically or has to be redeemed]`

   **Warning:** Don't turn on *auto-recharge* if you're working with prepaid credits.

4. **Open the NemoClaw launchable:**
   https://brev.nvidia.com/launchable/deploy/now?launchableID=env-3Azt0aYgVNFEuz7opyx3gscmowS&ncid=ref-dli-759990

   You should see: the deployment page with the instance type, the provider, and the hourly cost. According to NVIDIA's public reports (September-October 2026), it's a **CPU-only** `n2d-standard-4` instance (4 vCPU, 16 GiB of RAM) on Google Cloud, marked as **Free**. You don't need a GPU: the model runs in NVIDIA's cloud. `[VERIFY IN LAB: instance type, price, disk size, and whether it shows as Free]`

5. **Deploy.** Click the deploy button (in the previous version it was called **Deploy NemoClaw**). Leave the tab open. `[VERIFY IN LAB: exact button text]`
   You should see: a side panel with the progress. The instance goes through the states `DEPLOYING` → `STARTING` → `RUNNING`. Plan for 5 to 15 minutes: Brev creates the machine in 1-2 minutes, and the agent setup takes about 5 more.

6. **Set up the agent if it asks you to.** The launchable UI changes often. You'll see one of these two things:
   - **A wizard with three options** (SET UP IN THIS BROWSER, SET UP OVER SSH, SET UP WITH MY CODING AGENT). Choose **SET UP IN THIS BROWSER**, keep **OpenClaw** as the agent and **NVIDIA Cloud** as the provider, paste your `nvapi-` key, and create the agent. It ends with a message like "AGENT CREATED SUCCESSFULLY".
   - **A dashboard** with a **my-assistant** card already running. Click **Chat with Agent**.

   `[VERIFY IN LAB: which of the two flows the launchable shows on recording day]`

   **Warning:** During setup, **don't reload the tab** and **don't click RETRY**, even if you see a red card: if the activity log keeps moving, the step did work, and RETRY rebuilds the whole sandbox.

7. **Copy your launchable URL.** It's the address of the NemoClaw app and has this shape (the domain depends on the access provider):
   - `https://nemoclaw-<id>.brevlab.com`
   - `https://nemoclaw-<id>.apps.run.brev.nvidia.com`
   - `https://nemoclaw-<id>.gobrev.dev`

   Screenshot: the address bar of the NemoClaw tab with the `nemoclaw-…` host highlighted. `[VERIFY IN LAB: where in the Brev console this URL appears]`

### Part B · Connect from the browser (NVIDIA course page)

The course page lives on `nvdli.github.io`, a different domain from your launchable. That's why it needs two things: the **base URL** and your **access session** (a browser cookie).

8. **Open the lesson** [Connect NemoClaw](https://nvdli.github.io/NemoClawDLI/nemoclaw/03a-kickstart.html) and scroll down to **Start the launchable → Inspect all four connection routes**. You'll see the **Connect NemoClaw** panel with two fields: **Base URL** and **Access session**.

9. **Paste the base URL** from step 7. The page keeps only the origin (it removes paths like `/onboard`).

10. **Read this before you copy the cookie.**

    > **A session cookie is a password.** Whoever has it can act as you on that launchable until it expires.
    > 1. Paste it **only** into the **Access session** field on the course page. Never in a chat, an issue, a screenshot, or a video.
    > 2. The page keeps it only in that tab (`sessionStorage`) and deletes it when you close the tab.
    > 3. When you're done, sign out of Brev and stop the instance.
    > 4. If you record your screen, blur the value.

11. **Copy the right cookie.** In the launchable tab (signed in), open the developer tools and look for the cookie that matches your URL's domain:

    | Your URL contains | Cookie to copy |
    |---|---|
    | `brevlab.com` | `CF_Authorization` |
    | `apps.run.brev.nvidia.com` | `_pomerium` |
    | `gobrev.dev` | `__Host-skybridge-brev-prd` |

    - **Chrome, Edge, or Brave:** `F12` (or `Cmd+Opt+I` on Mac) → **Application** tab → **Storage → Cookies** → choose the launchable origin → find the cookie → double-click the **Value** cell → copy.
    - **Firefox:** `F12` → **Storage** tab → **Cookies** → launchable origin → select the row → double-click the value → copy.
    - **Safari:** first turn on **Settings → Advanced → Show features for web developers**. Then `Cmd+Opt+I` → **Storage** tab → **Cookies** → launchable origin → copy the value.

    Copy **only the full Value**. Don't copy the whole `Cookie` header or the cookie name.

12. **Paste the value into Access session and click Test connection.** The page runs 4 checks in order:

    | Route | What it checks |
    |---|---|
    | Agent metadata (`GET /api/agent`) | That your session is valid. The page gets the **gateway token** from here (don't type it yourself). |
    | Gateway (WebSocket `/cli/gateway`) | That the OpenClaw gateway responds and accepts the token. |
    | Terminal (WebSocket `/ws/terminal`) | That there's an operator terminal on the machine. |
    | Health (`GET /healthz`) | That the runtime is healthy. |

    You should see: `Connection ready. Metadata, gateway, terminal, and health checks passed.` and the pill at the top showing **OpenClaw ✓**.
    If you see `OpenClaw is starting. Retrying in N seconds.`, wait: the page retries on its own for up to 30 minutes.

13. **Run the control: a direct model call, with no agent.** In **Step 1 · Establish the model-only control**, use **Probe active model endpoint** and then **Hello chat**.
    You should see: a normal answer from the `nvidia/nemotron-3.5-lightning-30b-a3b` model. No tools, no memory. This is your baseline.

14. **Run an agent turn through the gateway.** In **Step 2**, open the **Gateway · WebSocket protocol, step by step** flow:
    1. Run the **Open the gateway connection** node (**▶ Run** button).
    2. Run **Call models.list and cron.list**. You should see the list of models and `cron jobs: (none)`.
    3. Open the code for **Send a chat message (streaming)**. The **last** uncommented `message = …` line is the one that gets sent. Leave it as is or change it to:
       ```js
       message = "Use your exec tool to run `whoami` and `pwd` in your sandbox, then tell me in one sentence which user you are and where you are.";
       ```
    4. Run the node.

    You should see: `⚙️` rows (each one is a tool call with its arguments) and `✓` rows (the result). The answer mentions the `sandbox` user and the `/sandbox` folder. `[VERIFY IN LAB: exact output of whoami and pwd]`

15. **Prove that memory lives in the `sessionKey`.** In **Step 3 · Compare conversation history**, click **▶ Run all** in the **Compare conversation history before and after reset** flow:
    - **Plant a fresh fact:** gives the agent a `CODE-…` code and asks it not to write it to files.
    - **Recall without replanting:** the agent remembers it.
    - **Reset, then recall again:** calls `sessions.reset`, and the agent no longer knows it.
    - **Remove only this flow's sessions:** cleans up what it created.

    You should see: `recalled` with the code before the reset, and "unknown" (or equivalent) after. The only thing the client sends is the session key: the gateway rebuilds the conversation on the server side.

### Part C · Connect from your terminal

The full commands, with their expected output and what to do if they fail, are in the [cookbook (Spanish)](../../../clases/4.1-laboratorio-nemoclaw-en-brev/cookbook.md). The summary:

16. **Install the Brev CLI and sign in:**
    ```bash
    # macOS
    brew install brevdev/homebrew-brev/brev
    # Linux or WSL (no sudo)
    bash -c "$(curl -fsSL https://raw.githubusercontent.com/brevdev/brev-cli/main/bin/install-latest.sh)"

    brev --version
    brev login
    ```

17. **Find your instance and get in:**
    ```bash
    brev ls
    brev shell <instancia>      # without --host
    ```
    You should see: your instance (`<instancia>`) in the `RUNNING` state and, after `brev shell`, a prompt inside the Brev machine.

    **Warning:** Don't use `brev shell <instancia> --host` with this launchable: it hangs until it times out (a known NemoClaw issue with CLI ≥ v0.6.331).

18. **Check the stack from inside the machine:**
    ```bash
    nemoclaw list
    nemoclaw status
    openshell sandbox list
    nemoclaw my-assistant status
    ```
    You should see: your sandbox (usually `my-assistant`) in the `Ready` state and the inference route `healthy`. If your sandbox has a different name, use the one `nemoclaw list` shows in every command. `[VERIFY IN LAB: sandbox name in the launchable]`

19. **Open the OpenClaw dashboard on your computer** (optional). In a local terminal, leave the tunnel running:
    ```bash
    brev port-forward <instancia> -p 18789:18789
    ```
    In the `brev shell` terminal, ask for the authenticated URL:
    ```bash
    nemoclaw my-assistant dashboard-url --quiet
    ```
    Open that URL in your browser. It contains the gateway token after `#token=`: treat it like a password.

### Part D · Pause, resume, and don't overspend

20. **Understand the three states:**

    | State | Compute | Disk | Your data |
    |---|---|---|---|
    | Running (`RUNNING`) | Billed per hour | Billed | Still there |
    | Stopped (`STOPPED`) | Not billed | **Still billed** | Kept (except `/tmp`) |
    | Deleted | Nothing | Nothing | **Lost forever** |

    Disk costs USD 0.0001314 per GB-hour. With a 100 GB disk, a week stopped costs about USD 2.2. `[VERIFY IN LAB: actual disk size of the launchable]`

21. **Stop the instance at the end of every study session.** In the console: **GPUs** → your instance → **Stop**. Or from your terminal:
    ```bash
    brev stop <instancia>
    brev ls
    ```
    If you see `instance "<nombre>" does not support stop.`, that instance type can't be paused: back up your workspace (cookbook recipe 11) and delete it with `brev delete <instancia>`. `[VERIFY IN LAB: whether the launchable instance is stoppable]`

22. **Resume and verify again:**
    ```bash
    brev start <instancia>
    brev refresh
    brev shell <instancia>
    nemoclaw my-assistant status
    ```
    Then go back to the course page: your cookie has probably expired, so copy a new one (step 11) and repeat **Test connection**.

    Heads-up: if the provider has no capacity, `brev start` fails and your data stays out of reach until capacity comes back. With a CPU instance it's rare, but it happens.

## Check that it worked

- [ ] `brev ls` shows your instance in `RUNNING`.
- [ ] **Test connection** shows `Connection ready` with all 4 routes green.
- [ ] The direct model control answers without tools.
- [ ] The gateway turn shows an `exec` `⚙️` row and its `✓` result.
- [ ] The planted code is remembered before the reset and forgotten after.
- [ ] From `brev shell`, `openshell sandbox list` shows your sandbox in `Ready`.
- [ ] You know how to stop your instance, and you left it `STOPPED` when you finished.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `OpenClaw is starting. Retrying in N seconds. Use Stop to cancel.` | The runtime is still starting (`/api/agent` returns 503 `starting`). | Wait. The page retries on its own for up to 30 min. If more than 15 min go by, check the Brev console. |
| The port 80 URL shows `503 … no_healthy_upstream` even though Brev says HEALTHY | Intermittent failure of the launchable proxy. | Wait a couple of minutes and reload. If it persists, deploy a new instance. |
| The NemoClaw check returns 502 or times out | A 502 alone doesn't tell you the cause. | Open the check that failed and read its evidence. Then use **Health check** (the *Detect & recover* flow). Use **Recover** only if the health check shows a configuration or session problem. |
| **OpenClaw ⚠** pill or `no challenge arrived within 30s. Open the launchable, then retry with a fresh matching access session` | Your session cookie expired or belongs to another launchable. | Open the launchable, sign in, copy the new **Value** of the right cookie, and run **Test connection** again. |
| `The launchable needs a fresh <cookie> browser session.` | You pasted the whole header, a different cookie, or nothing. | Copy only the **Value** of the cookie that matches your domain (table in step 11). |
| `You have run out of credits ...` even though you do have credits | Another Brev organization is active. | `brev ls orgs` and then `brev set <org>`. In the console, switch organizations. |
| `ssh: Could not resolve hostname <instancia>` even after running `brev refresh` | Brev's `Include` line ended up inside a `Host` block in your `~/.ssh/config`. | Back up `~/.ssh/config` and move the `Include … .brev/ssh_config` line to the top, before the first `Host`. Cookbook recipe 12. |
| `brev shell <instancia> --host` hangs | Known problem with the `--host` route on this launchable. | Use `brev shell <instancia>` without `--host`. |
| Red card with **RETRY** or progress stuck at 0 % during setup | A visual bug in the launchable UI. | Look at the activity log. If it's moving, do nothing. Don't click **RETRY**: it rebuilds the sandbox. |
| The chat gets no answer and times out; `exec` never shows up | `toolSearch` is on: the model loops on `tool_search_code`. | **Health check** reads the real value. If it shows `tools.toolSearch: true` (or `tools.toolSearch is ON`), **Recover** turns it off with `config.patch`. |
| `brev start` fails after a pause | The provider has no capacity for that instance type. | Wait and retry. If it's urgent, delete and deploy again (you lose any data you didn't back up). |
| A tutorial tells you to use `nemoclaw deploy` | That command was removed in NemoClaw v0.0.117. | Don't use it. In this course we deploy with the Brev launchable. |

## Challenge

**Pause and come back in under 10 minutes.** Stop your instance, resume it, and get everything green again.

Success criteria: `brev ls` showed `STOPPED` and then `RUNNING`, `nemoclaw my-assistant status` reports inference as `healthy`, and **Test connection** shows `Connection ready` again. Write down how long each step took and what you had to redo (hint: the cookie).

## Project milestone

Your **Soporte NemoClaw** (NemoClaw Support) agent now has a home. Before you teach it anything, measure how it answers "out of the box":

1. In the gateway turn (step 14), send this student question:
   ```js
   message = "A student says: 'My notebook returns HTTP 401 when I call the model'. What do you tell them? Answer in English, in 5 lines at most.";
   ```
2. Save the answer in your repo as `proyecto/linea-base-4.1.md` (baseline), together with your instance name, the sandbox name, and the hourly cost you saw on Brev.

In class 4.3 you'll install the `soporte-nemoclaw` skill with the course FAQ and compare against this baseline.

## Resources

- [Lesson 03a · Connect NemoClaw (NVIDIA DLI)](https://nvdli.github.io/NemoClawDLI/nemoclaw/03a-kickstart.html)
- [NemoClaw launchable on Brev](https://brev.nvidia.com/launchable/deploy/now?launchableID=env-3Azt0aYgVNFEuz7opyx3gscmowS&ncid=ref-dli-759990)
- [Brev · Quickstart](https://docs.nvidia.com/brev/latest/getting-started/quickstart.md) and [CLI: connectivity](https://docs.nvidia.com/brev/latest/cli/connectivity.md)
- [Brev · Instances: states and billing](https://docs.nvidia.com/brev/latest/concepts/gpu-instances.md) and [Launchables pricing](https://www.nvidia.com/en-us/launchables/pricing)
- [NemoClaw · Deploy to a headless server (includes Brev)](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/deployment/deploy-to-headless-server.md)
- [NemoClaw · Troubleshooting](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/reference/troubleshooting.md)
- Reference issues: [NemoClaw #13090](https://github.com/NVIDIA/NemoClaw/issues/13090) (hostname), [#11534](https://github.com/NVIDIA/NemoClaw/issues/11534) (`--host`), [#11535](https://github.com/NVIDIA/NemoClaw/issues/11535) (503), [#11536](https://github.com/NVIDIA/NemoClaw/issues/11536) (RETRY), [brev-cli #390](https://github.com/brevdev/brev-cli/issues/390) (organization)
