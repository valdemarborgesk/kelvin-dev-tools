# Kelvin Dev Tools

Read **[AGENTS.md](AGENTS.md)** for the full developer guide, tool reference, and workflow.

## First Run Check

Before doing anything else, detect the OS and verify the environment is set up:

```bash
python3 -c "import platform; print(platform.system())" 2>/dev/null || python -c "import platform; print(platform.system())"
```

Then check the venv (use `venv/bin/kelvin` on macOS/Linux, `venv\Scripts\kelvin.exe` on Windows):

```bash
test -d venv && venv/bin/kelvin --version 2>/dev/null
```

If the venv doesn't exist or the kelvin CLI is not found, run setup first:

```bash
python3 scripts/setup.py    # macOS/Linux
python scripts/setup.py     # Windows
```

Then activate: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)

## Skills

Skills are in `.claude/skills/`. They activate automatically when matching user intent, or can be invoked explicitly via slash commands (`/app-deploy`, `/assets`, etc.).

## Universal Rules

- **NEVER use interactive scripts** — they hang in all environments.
- **ALWAYS use the venv** — `source venv/bin/activate` or `venv/bin/python`, `venv/bin/kelvin`.
- **API base path** — `/api/v4` (not `/api/v1`).
- **ASK before** deploying or deleting resources.
