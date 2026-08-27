# Fleetos Environment Configuration Guide

Product: **Fleetos**

---

## Configuration Environment Variables

| Variable | Default Value | Scope | Description |
| :--- | :--- | :--- | :--- |
| `API_BASE_URL` | `http://127.0.0.1:8000` | Server-side Next.js | Base REST API URL for server component data fetching |
| `NEXT_PUBLIC_API_BASE_URL` | `http://127.0.0.1:8000` | Client-side Next.js | Base REST API URL for client-side fetches |
| `TRACKING_PROVIDER` | `simulator` | FastAPI | Active tracking provider (`simulator` or `gps`) |
| `TRACKING_UPDATE_INTERVAL_SECONDS` | `5` | FastAPI | Simulator update interval in seconds |
| `TRACKING_LIVE_THRESHOLD_SECONDS` | `30` | FastAPI | Telemetry age threshold for `LIVE` status |
| `TRACKING_STALE_THRESHOLD_SECONDS` | `300` | FastAPI | Telemetry age threshold for `STALE` status |
