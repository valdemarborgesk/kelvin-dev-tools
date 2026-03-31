---
name: app-deploy
description: "Build, upload, and deploy a Kelvin SmartApp to the platform. Use when the user wants to deploy, publish, push, or release their app."
argument-hint: <app-dir> to <environment> [workload-name]
---

# Deploy Kelvin App

Full deployment workflow: build Docker image, upload to registry, deploy or update workload.

## Steps

1. **Check auth** — verify a valid token exists:

```bash
source venv/bin/activate
kelvin auth token 2>/dev/null | grep '^ey' | tail -1
```

If empty, authenticate first: `kelvin auth login https://<env-url>` (resolve from config.json).

2. **Check Docker** — required for building:

```bash
docker info > /dev/null 2>&1 && echo "Docker OK" || echo "ERROR: Docker not running"
```

3. **Validate app** — confirm `app.yaml` exists in the app directory.

4. **Build and upload** — this builds the Docker image and pushes to the platform registry:

```bash
kelvin app upload --app-dir <app-dir>
```

Wait for this to complete before proceeding.

5. **Check if workload exists**:

```bash
kelvin workload show <workload-name> 2>/dev/null
```

If it exists, this is an **update**. If not, this is a **new deploy**.

6. **Deploy or update**:

New deployment:
```bash
kelvin workload deploy --workload-name <name> --app-config <app-dir>/app.yaml --runtime <app-dir>/runtime_config.yaml
```

Update existing:
```bash
kelvin workload update --workload-name <name> --app-config <app-dir>/app.yaml --runtime <app-dir>/runtime_config.yaml
```

7. **Verify** — wait ~15 seconds, then check status and logs:

```bash
kelvin workload show <name>
kelvin workload logs <name> --tail-lines 20
```

## runtime_config.yaml

If the user doesn't have a `runtime_config.yaml`, help them create one:

```yaml
cluster_name: <cluster>
node_name: <node>
resources:
  - type: cpu
    limit: "500m"
    request: "100m"
  - type: memory
    limit: "256Mi"
    request: "128Mi"
environment_vars:
  - name: LOG_LEVEL
    value: "INFO"
```

Key rules: `resources` must be a YAML list, `environment_vars` must be a list, use `null` not `None`.

## Rules

- **ASK the user before deploying** — confirm the workload name and target environment.
- If upload fails with "unauthorized", re-authenticate.
- If "version already exists", increment the version in app.yaml.
- ALWAYS use the venv.
