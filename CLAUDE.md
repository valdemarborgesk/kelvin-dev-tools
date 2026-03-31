# Kelvin Dev Tools

Read **[AGENTS.md](AGENTS.md)** for the full developer guide, tool reference, and workflow.

## First Run Check

Before doing anything else, verify the environment is set up:

```bash
test -d venv && venv/bin/kelvin --version 2>/dev/null
```

If the venv doesn't exist or the kelvin CLI is not found, run setup first:

```bash
bash scripts/setup.sh
```

Then activate: `source venv/bin/activate`

## Skills

Skills are in `.claude/skills/`. They activate automatically when matching user intent, or can be invoked explicitly via slash commands (`/app-deploy`, `/assets`, etc.).

## Universal Rules

- **NEVER use interactive scripts** — they hang in all environments.
- **ALWAYS use the venv** — `source venv/bin/activate` or `venv/bin/python`, `venv/bin/kelvin`.
- **API base path** — `/api/v4` (not `/api/v1`).
- **ASK before** deploying or deleting resources.
