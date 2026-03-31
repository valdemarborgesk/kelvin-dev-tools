# Kelvin Dev Tools — Setup

You are setting up a developer environment for building Kelvin SmartApps. Follow these steps in order. Wait for each step to complete before moving on. The user may not be technical — use plain language and guide them through everything.

## Step 0: Make sure you are in Code mode

**You MUST be running in Claude Code (CLI or Desktop Code mode) to execute commands.** If you are in a regular Claude chat, you cannot run bash commands.

If the user is in a regular Claude Desktop chat, tell them:

> To set this up, I need to be able to run commands on your machine. Please:
> 1. Click the **Code** tab at the top of Claude Desktop
> 2. Select **any folder** as the working directory (your home folder is fine)
> 3. Then paste these instructions again or ask me to set up Kelvin Dev Tools

Do not proceed until you can execute bash commands.

## Step 1: Ask the user about their current state

Before doing anything, ask the user:

> **Is this a fresh install, or have you already set up the Kelvin Dev Tools before?**
>
> 1. **Fresh install** — I haven't set anything up yet
> 2. **Already set up** — I've done this before
> 3. **Not sure**

Based on their answer:

- **Fresh install** → go to Step 2
- **Already set up** → ask: **"Do you remember where the folder is? For example ~/work/kelvin-dev-tools, or on your Desktop?"**. Once they give you a path, verify it:

```bash
REPO_PATH="<the path they gave you>"
[ -f "$REPO_PATH/AGENTS.md" ] && echo "REPO=ok" || echo "REPO=not_found"
[ -x "$REPO_PATH/venv/bin/kelvin" ] && echo "VENV=ok" || echo "VENV=missing"
TOKEN=$("$REPO_PATH/venv/bin/kelvin" auth token 2>/dev/null | grep '^ey' | tail -1)
[ -n "$TOKEN" ] && echo "AUTH=ok" || echo "AUTH=not_logged_in"
which docker >/dev/null 2>&1 && docker info >/dev/null 2>&1 && echo "DOCKER=ok" || echo "DOCKER=missing_or_stopped"
```

Then skip to the first incomplete step:

| Status | Skip to |
|--------|---------|
| REPO not found at that path | Ask them to double-check, or go to Step 2 |
| REPO ok, VENV missing | Step 3 |
| REPO ok, VENV ok, AUTH not logged in | Step 4 |
| REPO ok, VENV ok, AUTH ok | Step 6 |

- **Not sure** → search for it:

```bash
find /Users -maxdepth 4 -name "AGENTS.md" -path "*/kelvin-dev-tools/*" 2>/dev/null
```

If found, show the path and confirm with the user. If not found, treat as fresh install.

**IMPORTANT:** From this point on, remember the repo location as `REPO_PATH` and use it in every command. Replace `<REPO_PATH>` with the actual path in all subsequent steps.

## Step 2: Prerequisites and clone

Check what's available:

```bash
which python3 && python3 --version
which git && git --version
which docker && docker --version
```

If anything is missing, tell the user what to install and **wait for them to confirm** before continuing:
- **Python 3.9+**: `brew install python3` (or download from python.org)
- **Git**: `brew install git` (or Xcode command line tools: `xcode-select --install`)
- **Docker**: Download Docker Desktop from docker.com

Then clone:

```bash
mkdir -p ~/work && cd ~/work
git clone --recursive git@github.com:kelvininc/kelvin-dev-tools.git
```

If the clone fails with "Permission denied (publickey)", try HTTPS:

```bash
git clone --recursive https://github.com/kelvininc/kelvin-dev-tools.git
```

After cloning, set `REPO_PATH` to the full path where it landed (e.g., `~/work/kelvin-dev-tools`).

## Step 3: Run setup

```bash
cd <REPO_PATH> && bash scripts/setup.sh
```

This creates the Python virtual environment, installs the Kelvin SDK, and initializes documentation. Wait for it to finish and verify there are no errors.

## Step 4: First login

Ask the user: **"What is the URL of your Kelvin environment?"** (it looks like `https://something.kelvin.ai` or `https://something.kelvininc.com`)

If they give a short name instead of a URL, try to resolve it from `config.json`:

```bash
python3 -c "import json; envs={e['name']:e['url'] for e in json.load(open('<REPO_PATH>/config.json')).get('environments',[])}; name='<what-they-said>'; print(f'https://{envs[name]}' if name in envs else 'NOT_FOUND')"
```

If not found, ask them for the full URL.

Then run the login dialog — this pops up native macOS windows for the user to enter their credentials (password is masked):

```bash
<REPO_PATH>/venv/bin/python <REPO_PATH>/scripts/auth-dialog.py https://<resolved-url>
```

Tell the user:

> A login window will pop up — enter your Kelvin email and password. Your password won't be visible as you type it.

**Wait for the script to complete.** It should print "Successfully logged on". Then verify:

```bash
source <REPO_PATH>/venv/bin/activate && kelvin auth token 2>/dev/null | grep '^ey' | tail -1
```

If a token is returned, login succeeded. If not, ask them to try again.

## Step 5: Verify

Run a quick check:

```bash
source <REPO_PATH>/venv/bin/activate && kelvin workload list 2>&1 | head -5
```

If workloads are listed, everything is working. If it errors, troubleshoot (likely auth issue — go back to step 4).

## Step 6: Done

Tell the user the exact folder path they need to remember, then:

> **Setup complete!** Here's how to use it from now on:
>
> 1. Open **Claude Desktop**
> 2. Click **Code** → **Select folder** → pick **<REPO_PATH>**
> 3. Start chatting!
>
> Things you can ask me:
> - "Create a new app called pump-monitor"
> - "Deploy my app"
> - "List all assets on my environment"
> - "Is data flowing for pump-01?"
> - "Show me the workload logs"
> - "What clusters are available?"
> - "What is a data stream?"
>
> You won't need to run this setup again.
