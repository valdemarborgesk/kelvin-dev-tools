---
name: app-create
description: "Scaffold a new Kelvin SmartApp project. Use when the user wants to create a new app, start a new project, or generate app boilerplate."
argument-hint: <app-name> [--app-type app|importer|exporter|docker]
---

# Create Kelvin App

Scaffold a new Kelvin SmartApp project using the SDK CLI.

## Steps

1. Verify the SDK is available:

```bash
source venv/bin/activate && kelvin --version
```

2. Create the app:

```bash
kelvin app create --name <app-name> [--app-type <type>] [--app-dir <path>]
```

Default app type is `app` (SmartApp). Other types: `importer`, `exporter`, `docker`.

3. The SDK generates the project structure:
   - `main.py` — main application logic with KelvinApp callbacks
   - `app.yaml` — app manifest (inputs, outputs, parameters, schedules)
   - `requirements.txt` — Python dependencies
   - `Dockerfile` — container build instructions

4. Explain the key files to the user and suggest next steps:
   - Edit `main.py` to implement the app logic
   - Edit `app.yaml` to define data streams, parameters, and configuration
   - Add dependencies to `requirements.txt`

## Rules

- App names must be lowercase alphanumeric with hyphens or underscores.
- Don't create apps in the kelvin-dev-tools root — create in a separate directory or the user's project directory.
- After creation, point the user to `kelvin-ai-docs/docs-ai/how-to/development/` for development guides.
- ALWAYS use the venv.
