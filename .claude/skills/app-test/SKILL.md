---
name: app-test
description: "Test a Kelvin SmartApp locally before deployment. Use when the user wants to test, simulate, run locally, or validate their app."
argument-hint: [simulator|csv|generator] [--app-dir <path>]
---

# Test Kelvin App

Run a Kelvin SmartApp locally with simulated data. Requires Docker.

## Steps

1. Verify Docker is running:

```bash
docker info > /dev/null 2>&1 && echo "Docker OK" || echo "ERROR: Docker not running"
```

2. Activate the venv:

```bash
source venv/bin/activate
```

3. Choose the test mode:

**Simulator** (default) — generates random data for all app inputs:
```bash
kelvin app test simulator [--app-dir <path>]
```

**CSV** — replays data from a CSV file:
```bash
kelvin app test csv --file <path-to-csv> [--app-dir <path>]
```

**Generator** — uses a custom data generator class:
```bash
kelvin app test generator [--app-dir <path>]
```

4. Watch the output for:
   - Startup messages (app initialized successfully)
   - Data processing output
   - Errors or exceptions

## Common Issues

- **Docker not running** — start Docker Desktop or the docker daemon.
- **Missing dependencies** — check `requirements.txt` has all needed packages.
- **app.yaml errors** — validate YAML syntax and schema.
- **Import errors** — ensure app code is correct and dependencies are installed.

## Rules

- ALWAYS use the venv.
- The `--app-dir` flag is optional — defaults to current directory.
- Point to `kelvin-ai-docs/docs-ai/how-to/development/` for testing guides if the user needs more detail.
