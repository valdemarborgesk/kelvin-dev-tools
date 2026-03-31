---
name: check-data
description: "Query timeseries data to verify data is flowing. Use when the user wants to check data, verify data flow, see if an asset has data, or debug missing data."
argument-hint: "<asset-name> [datastream] on <environment>"
---

# Check Data Flow

Query timeseries data to verify that data is flowing correctly for an asset.

## Steps

1. Verify auth:

```bash
source venv/bin/activate
kelvin auth token 2>/dev/null | grep '^ey' | tail -1
```

2. If the user specifies an asset but not a data stream, first list the available data streams:

```bash
venv/bin/python tools/datastreams.py --env <env> list --asset <asset-name>
```

3. Check latest data point:

```bash
venv/bin/python tools/timeseries.py --env <env> latest --asset <asset-name> --datastream <ds>
```

4. If no recent data, query a wider range (last 24 hours):

```bash
venv/bin/python tools/timeseries.py --env <env> query --asset <asset-name> --datastream <ds> --start 24h
```

5. Report findings:
   - **Data is flowing** — show latest timestamp and value
   - **No data in last 24h** — possible issues:
     - Workload stopped (check with `kelvin workload show`)
     - Asset offline
     - Data stream misconfigured (check data stream config)
     - App not publishing to this data stream

## Rules

- ALWAYS use the venv.
- If checking multiple data streams, check them one at a time.
- Suggest troubleshooting steps based on findings (check logs, check workload, check config).
