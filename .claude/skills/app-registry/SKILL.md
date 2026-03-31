---
name: app-registry
description: "Browse the Kelvin app registry. Use when the user wants to see what apps are available, check app versions, download an app, or delete an old version."
argument-hint: "list|show|search|download|delete [app-name]"
---

# App Registry

Browse and manage applications in the platform's app registry via the SDK CLI.

## Steps

1. Verify auth:

```bash
source venv/bin/activate
kelvin auth token 2>/dev/null | grep '^ey' | tail -1
```

2. Determine the operation:

**List all apps:**
```bash
kelvin apps list
```

**Search for an app:**
```bash
kelvin apps search --name <search-term>
```

**Show app details** (versions, config):
```bash
kelvin apps show <app-name>
```

**Download an app** (get source from registry):
```bash
kelvin apps download <app-name> [--app-dir <output-path>]
```

**Delete an app version** (ASK before executing):
```bash
kelvin apps delete <app-name>
```

## Rules

- ALWAYS use the venv.
- ASK before deleting apps from the registry.
- `kelvin apps show` displays available versions — useful for checking what's deployed.
- When troubleshooting version conflicts, use `show` to see all versions.
