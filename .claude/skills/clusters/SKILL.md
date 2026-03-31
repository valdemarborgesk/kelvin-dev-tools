---
name: clusters
description: "List clusters and check cluster health. Use when the user asks about clusters, nodes, infrastructure, or what's available to deploy to."
argument-hint: "list on <environment> | get <cluster-name> | nodes <cluster-name>"
---

# Kelvin Clusters

List and inspect clusters and nodes via the REST API.

## Steps

1. Verify auth:

```bash
source venv/bin/activate
kelvin auth token 2>/dev/null | grep '^ey' | tail -1
```

2. Determine the operation:

**List all clusters:**
```bash
venv/bin/python tools/clusters.py --env <env> list [--search <term>]
```

**Get cluster details:**
```bash
venv/bin/python tools/clusters.py --env <env> get <name>
```

**List nodes in a cluster:**
```bash
venv/bin/python tools/clusters.py --env <env> nodes <cluster-name>
```

3. Highlight any clusters or nodes that are `unreachable`, `not_ready`, or have issues.

4. When the user needs to choose a cluster/node for deployment, present the available options clearly.

## Rules

- ALWAYS use the venv.
- Cluster and node names are needed for `runtime_config.yaml` when deploying workloads.
- If a cluster is unreachable, it cannot be deployed to.
