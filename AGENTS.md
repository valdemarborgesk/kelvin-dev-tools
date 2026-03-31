# Kelvin Developer Tools — AI Instructions

## Purpose

This toolkit equips AI agents with everything needed to build, test, deploy, and troubleshoot Kelvin SmartApps. It wraps the Kelvin SDK CLI and provides REST API tools for platform management.

## Target Audience

The user is **not a developer**. They describe what they want in plain language and expect the AI to handle everything. This means:

- **Explain what you're doing** in simple terms before and after each step. Don't just run commands silently. Example: "I'm checking what apps are deployed on beta..." not just running `kelvin workload list`.
- **Never ask technical questions** the user can't answer. Don't ask "what's the cluster name?" — look it up yourself with `tools/clusters.py`. Don't ask "what's the data stream name?" — list them with `tools/datastreams.py`.
- **Read docs and explore before asking the user.** If something fails, check the platform docs (`docs/`), check logs, try alternative approaches. Only ask the user when you genuinely need a human decision (which environment, what the app should do, whether to deploy).
- **Anticipate problems.** If an operation needs a prerequisite (asset type must exist before creating an asset, app must be uploaded before deploying), check and handle it automatically.
- **If the SDK doesn't work, use the API.** Some SDK CLI commands have bugs or require complex config files. The REST API is often more straightforward. See "Known Workarounds" below.
- **Keep it conversational.** Say "Your app is deployed and running!" not "Workload my-app deployed successfully with status running on cluster beta-cluster-01 node beta-node-01."

## Quick Setup

```bash
bash scripts/setup.sh
source venv/bin/activate
kelvin auth login https://<env-url>
```

## Tool Priority

1. **SDK CLI** (`kelvin ...`) — for app build, upload, test, and authentication
2. **REST API tools** (`venv/bin/python tools/...`) — for platform resources and as fallback when the SDK CLI has issues
3. **REST API directly** (curl/python) — when neither of the above covers the need

## The Developer Workflow

End-to-end lifecycle for building a Kelvin SmartApp:

1. **Create** — `kelvin app create --name my-app` (scaffolds project structure)
2. **Develop** — edit `main.py`, `app.yaml`, add dependencies to `requirements.txt`
3. **Test** — `kelvin app test simulator` or `kelvin app test csv --file data.csv`
4. **Upload** — `kelvin app upload --app-dir .` (builds Docker image + pushes to registry)
5. **Deploy** — `kelvin workload deploy --workload-name my-workload --app-config app.yaml --runtime runtime_config.yaml`
6. **Monitor** — `kelvin workload logs my-workload --tail-lines 100`
7. **Verify data** — `venv/bin/python tools/timeseries.py --env <env> latest --asset <name> --datastream <ds>`

## Key Rules

- **NEVER use interactive scripts** — they hang in AI agent environments.
- **ALWAYS use the venv** — `source venv/bin/activate` or use `venv/bin/python`, `venv/bin/kelvin`.
- **ALWAYS dry-run first** for destructive operations.
- **ASK before** deploying to any environment or deleting resources.
- **API base path** — `/api/v4` (not `/api/v1`).
- **If the SDK CLI is giving trouble, check if there's an equivalent API call.** The REST API is often simpler and more reliable. Check `docs/api/endpoints/` for the endpoint reference.
- **SDK version must match the platform.** After login, check for version mismatch warnings (`Current: X Recommended: Y`). If mismatched, install the recommended version: `venv/bin/pip install kelvin-sdk==<recommended>`.
- **Always verify API endpoints against the platform's OpenAPI spec.** After first login, fetch the spec: `venv/bin/python tools/api_spec.py --env <env> fetch`. Before using any unfamiliar endpoint, check it exists: `venv/bin/python tools/api_spec.py --env <env> check /path METHOD`.
- Docker must be running for `kelvin app build`, `kelvin app upload`, and `kelvin app test`.

## Authentication

For first-time login (no stored credentials), use the auth dialog — it pops up native macOS windows so the user can enter credentials without touching Terminal:

```bash
venv/bin/python scripts/auth-dialog.py https://<env-url>
```

For subsequent logins (credentials already in keyring):

```bash
source venv/bin/activate && kelvin auth login https://<env-url>
```

## SDK CLI Reference

| Task | Command |
|------|---------|
| First login (dialog) | `venv/bin/python scripts/auth-dialog.py https://<url>` |
| Login (keyring) | `kelvin auth login https://<url>` |
| Check auth | `kelvin auth token 2>/dev/null \| grep '^ey' \| tail -1` |
| Create app | `kelvin app create --name <name>` |
| Build app | `kelvin app build --app-dir .` |
| Upload app | `kelvin app upload --app-dir .` |
| Test (simulator) | `kelvin app test simulator` |
| Test (CSV) | `kelvin app test csv --file data.csv` |
| Test (generator) | `kelvin app test generator` |
| List platform apps | `kelvin apps list` |
| Show app details | `kelvin apps show <name>` |
| Deploy workload | `kelvin workload deploy --workload-name <n> --app-config app.yaml --runtime runtime_config.yaml` |
| Update workload | `kelvin workload update --workload-name <n> --app-config app.yaml --runtime runtime_config.yaml` |
| View logs | `kelvin workload logs <name> --tail-lines 100` |
| List workloads | `kelvin workload list` |
| Show workload | `kelvin workload show <name>` |
| Start workload | `kelvin workload start <name>` |
| Stop workload | `kelvin workload stop <name>` |
| Undeploy workload | `kelvin workload undeploy <name>` |
| Start workload | `kelvin workload start <name>` |
| Stop workload | `kelvin workload stop <name>` |
| Undeploy workload | `kelvin workload undeploy <name>` |
| Create secret | `kelvin secret create --name <n> --value <v>` |
| List secrets | `kelvin secret list` |
| Update secret | `kelvin secret update --name <n> --value <v>` |
| Delete secret | `kelvin secret delete --name <n>` |
| Search apps | `kelvin apps search --name <term>` |
| Download app | `kelvin apps download <name>` |
| Delete app | `kelvin apps delete <name>` |

## REST API Tools

For platform resources the SDK CLI cannot manage (assets, data streams, timeseries):

| Tool | Purpose | Example |
|------|---------|---------|
| `tools/assets.py` | Asset + asset type CRUD | `venv/bin/python tools/assets.py --env <env> list` |
| `tools/datastreams.py` | Data stream CRUD | `venv/bin/python tools/datastreams.py --env <env> list --asset pump-01` |
| `tools/timeseries.py` | Query timeseries data | `venv/bin/python tools/timeseries.py --env <env> latest --asset pump-01 --datastream pressure` |
| `tools/clusters.py` | Cluster + node info | `venv/bin/python tools/clusters.py --env <env> list` |
| `tools/api_spec.py` | Fetch + verify API endpoints | `venv/bin/python tools/api_spec.py --env <env> fetch` |

All tools accept `--env <name>` (resolved from `config.json`) or `--url <full-url>`.

## Environment Configuration

Environments are listed in `config.json`. To add a new one, append:

```json
{"name": "my-env", "url": "my-env.kelvin.ai"}
```

## API Conventions

When making direct REST API calls:

- Base path: `/api/v4`
- List endpoints use a `/list` suffix (e.g., `/api/v4/assets/list`)
- Response data is in the `data` key (not `items`). Parse with `.get('data', [])`
- Pagination: use `page_size=200` and check `pagination.next_page`
- Auth: `Authorization: Bearer <token>` header

## App Configuration Reference

### app.yaml

The app manifest defines inputs, outputs, parameters, and schedules. Created by `kelvin app create`.

### runtime_config.yaml

Created manually before deployment. Example:

```yaml
cluster_name: my-cluster
node_name: my-node
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

Key rules:
- `resources` must be a YAML **list** (not a dict)
- `environment_vars` must be a YAML **list**
- Use `null` not `None` for empty values

## Platform Documentation

For concepts, API schemas, SDK classes, and how-to guides:

| Topic | Path |
|-------|------|
| Concepts (assets, data streams, apps) | `docs/concepts/` |
| REST API endpoints | `docs/api/endpoints/` |
| API schemas | `docs/api/schemas/` |
| Python SDK (KelvinApp, filters, streams) | `docs/sdk/` |
| Development how-to guides | `docs/how-to/development/` |

See `docs/agents.md` for detailed query strategies.

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| "No current session" | Not authenticated | `kelvin auth login https://<url>` or `scripts/auth-dialog.py` for first time |
| 401 Unauthorized | Token expired | Re-run `kelvin auth login` |
| "Checking stored credentials... Aborted" | No keyring credentials | Run `venv/bin/python scripts/auth-dialog.py https://<url>` |
| "Asset type not found" | Missing prerequisite | Create asset type first via `tools/assets.py` |
| Docker errors on build/test | Docker not running | Start Docker Desktop / daemon |
| "Version already exists" | App version collision | Increment version in `app.yaml` |
| Empty workload logs | Workload not started | `kelvin workload start <name>` |
| `legacy_error` | Old platform version | Some API endpoints unavailable; check SDK version compatibility |
| No data flowing | App not publishing | Check workload logs for errors, verify data stream config |
| `kelvin workload deploy` fails or requires complex yaml | SDK CLI deploy can be finicky | Use the REST API instead (see Known Workarounds) |

## Known Workarounds

### Workload deploy via API (instead of SDK CLI)

The SDK CLI `kelvin workload deploy` requires a `runtime_config.yaml` file and can be finicky. The REST API is more straightforward. Use this when the CLI gives you trouble:

**Create a workload:**
```bash
TOKEN=$(kelvin auth token 2>/dev/null | grep '^ey' | tail -1)
curl -s -X POST "https://<env-url>/api/v4/apps/workloads/create" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "<workload-name>",
    "app_name": "<app-name>",
    "app_version": "<version>",
    "cluster_name": "<cluster>",
    "node_name": "<node>"
  }'
```

**Update a workload:**
```bash
curl -s -X POST "https://<env-url>/api/v4/apps/workloads/<workload-name>/patch" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"app_version": "<new-version>"}'
```

**Start/stop a workload:**
```bash
curl -s -X POST "https://<env-url>/api/v4/apps/workloads/start" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"names": ["<workload-name>"]}'
```

To find the cluster and node names, use `venv/bin/python tools/clusters.py --env <env> list` and `nodes`.

### General approach when something doesn't work

1. **Check the logs** — `kelvin workload logs <name>` or the command output
2. **Read the docs** — search `docs/` for the relevant topic
3. **Try the API** — the REST API at `/api/v4` often works when the SDK CLI doesn't
4. **Don't ask the user technical questions** — figure it out yourself or explain the problem in simple terms
