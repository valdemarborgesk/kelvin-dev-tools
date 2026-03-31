---
name: kelvin-docs
description: "Look up Kelvin platform concepts, SDK, API, or development documentation. Auto-activates when the user asks about Kelvin platform topics like assets, datastreams, apps, workloads, SDK usage, or API endpoints."
user-invocable: false
---

# Kelvin Platform Knowledge Base

Platform documentation lives in the `docs/` directory.

## Locating the Docs

```bash
ls docs/ 2>/dev/null || echo "Docs directory not found"
```

## Query Strategy

| Question Type | Where to Look |
|---------------|---------------|
| Concepts (what is an asset, datastream, app) | `docs/concepts/` |
| REST API endpoints (create asset, list workloads) | `docs/api/endpoints/` |
| API schemas (data structures) | `docs/api/schemas/` |
| Python SDK (KelvinApp, stream_filter, entry points) | `docs/sdk/` |
| How-to guides (deploy app, test, configure) | `docs/how-to/development/` |

## Search Priority

1. **Concepts first** — for "what is X?" questions
2. **How-to guides** — for "how do I X?" questions
3. **API endpoints** — for REST API questions
4. **SDK classes** — for Python code questions

## Reading the Docs

Documentation files are JSON with the schema:
```json
{
  "id": "...",
  "title": "...",
  "type": "...",
  "category": "...",
  "content": "full content text",
  "summary": "brief summary",
  "code_examples": [...],
  "related": [...],
  "tags": [...]
}
```

- Use `summary` for quick answers, `content` for detailed ones.
- For API endpoints: check `metadata.method`, `metadata.path`, `metadata.parameters`, `metadata.request_body`.

## Important: API Conventions

When the docs reference REST API endpoints:
- Base path: `/api/v4`
- List endpoints use `/list` suffix
- Response data in `data` key, NOT `items`
- Use the REST API tools (`tools/assets.py`, etc.) for live queries

## Rules

- Read `docs/agents.md` first if you need guidance on how to search the docs.
- Prefer `summary` for quick answers, full `content` when the user needs detail.
