# Fleetos Real-Time Tracking Engine Architecture

Product: **Fleetos** (Agentic Multimodal Fleet Intelligence Platform)  
Module Boundary: `services/tracking`

---

## 1. Tracking Engine Overview & Authority Boundary
The Fleetos Tracking Engine ingests, normalizes, validates, and evaluates vehicle position telemetry in real-time.

```
                         FLEETOS
                            │
                ┌───────────┴───────────┐
                │                       │
          Next.js Web              FastAPI API
                │                       │
        ┌───────┼────────┐       ┌──────┼─────────┐
        │       │        │       │      │         │
    Dashboard Fleet   Routes  Tracking Events  Optimizer
        │       │        │       │      │         │
        └───────┴────────┴───────┴──────┴─────────┘
                                │
                         Tracking Service
                                │
                     ┌──────────┴──────────┐
                     │                     │
                Simulator              Future GPS
                     │                  Provider
                     └──────────┬──────────┘
                                │
                         Tracking Database
                                │
                    Latest State + History
```

> [!IMPORTANT]
> **Optimization Authority Boundary**: Google OR-Tools Routing Solver (`RoutingModel`) remains strictly authoritative for vehicle routing and assignment decisions. Telemetry feeds the visual tracking engine and event monitoring; it does not override solver decisions.

---

## 2. Telemetry Validation Rules
1. **Latitude**: `-90.0 <= latitude <= 90.0`
2. **Longitude**: `-180.0 <= longitude <= 180.0`
3. **Speed**: `speed_kmh >= 0.0`
4. **Heading**: Normalized to `0.0 <= heading_degrees < 360.0`

---

## 3. Telemetry Freshness Model
- **LIVE**: Telemetry age $\le 30$ seconds (Green indicator).
- **RECENT**: Telemetry age $31 - 120$ seconds (Yellow indicator).
- **STALE**: Telemetry age $121 - 300$ seconds (Amber indicator).
- **OFFLINE**: Telemetry age $> 300$ seconds (Red indicator).

---

## 4. Vehicle Status Classification
- **MOVING**: `speed_kmh > 2.0` and Freshness $\neq$ `OFFLINE`.
- **STOPPED**: `speed_kmh <= 2.0` and Freshness $\neq$ `OFFLINE`.
- **OFFLINE**: Freshness $=$ `OFFLINE`.

---

## 5. Lifecycle Event Generation & Deduplication
Events are emitted on status transitions to prevent duplicate spamming:
- `VEHICLE_STARTED_MOVING` (emitted on `STOPPED` $\rightarrow$ `MOVING`)
- `VEHICLE_STOPPED` (emitted on `MOVING` $\rightarrow$ `STOPPED`)
- `VEHICLE_TRACKING_STALE` (emitted when Freshness becomes `STALE`)
- `VEHICLE_TRACKING_RECOVERED` (emitted when Freshness returns to `LIVE`)
