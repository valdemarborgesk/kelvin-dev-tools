---
name: secrets
description: "Manage Kelvin platform secrets (API keys, credentials). Use when the user needs to create, list, update, or delete secrets for their app."
argument-hint: "list|create|update|delete [secret-name] on <environment>"
---

# Kelvin Secrets

Manage platform secrets via the SDK CLI. Secrets are encrypted key-value pairs available to workloads at runtime.

## Steps

1. Verify auth:

```bash
source venv/bin/activate
kelvin auth token 2>/dev/null | grep '^ey' | tail -1
```

2. Determine the operation:

**List secrets:**
```bash
kelvin secret list
```

**Create a secret:**
```bash
kelvin secret create --name <secret-name> --value <secret-value>
```

**Update a secret:**
```bash
kelvin secret update --name <secret-name> --value <new-value>
```

**Delete a secret** (ASK before executing):
```bash
kelvin secret delete --name <secret-name>
```

3. To use a secret in an app, reference it in `app.yaml` or `runtime_config.yaml` under environment variables.

## Common Use Cases

- API keys for external services
- Database connection strings
- Authentication credentials
- License keys

## Rules

- ALWAYS use the venv.
- NEVER display secret values in output — only show names.
- ASK before deleting secrets.
- Secret names should be descriptive (e.g., `weather-api-key`, not `key1`).
