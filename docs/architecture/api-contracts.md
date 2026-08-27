# Fleetos REST API & Webhook Specifications

Product: **Fleetos**

---

## Endpoint Contract Overview

All application API endpoints are versioned under `/api/v1/`.

### System Health & Version
- `GET /health` / `GET /api/v1/health`: Returns system status, service name, version, and environment.
- `GET /api/v1/version`: Returns platform metadata, core loop, and voice agent name.

### Core Domain Resources (Phases 2-5)
- `GET /api/v1/lorries`: List all active lorries and current telemetry.
- `GET /api/v1/shipments`: List all shipments, deadlines, and priorities.
- `GET /api/v1/routes`: Retrieve calculated routes and delivery sequences.
- `POST /api/v1/optimization/run`: Trigger Google OR-Tools VRP solver re-optimization.
- `POST /api/v1/voice/vapi-webhook`: Webhook endpoint processing Vapi tool calls (e.g. `report_delay`).
