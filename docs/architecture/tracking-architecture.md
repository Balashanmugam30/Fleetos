# Fleetos Real-Time Tracking & Telemetry Architecture

Product: **Fleetos**

---

## Tracking Strategy

Vehicle movement is backed by an authoritative backend state stream rather than frontend-only animations.

```
GPS Hardware / Telemetry Simulator
   │
   ▼
Fleetos Backend Tracking Service (`services/tracking`)
   │
   ▼
FastAPI WebSocket / Server-Sent Events (SSE) Stream
   │
   ├──> Web Control Tower Vector Map (Mapbox GL)
   └──> AR Camera Visualizer Overlay
```
