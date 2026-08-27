# ATLAS Agent Tool Execution Specification

Product: **Fleetos**  
Module Boundary: `services/agent/tool_executor.py`

---

## Tool Registry Matrix

| Tool Name | Type | Description | Primary Output / Event |
| :--- | :--- | :--- | :--- |
| `get_fleet_status` | Read | Returns active, moving, stopped, and stale vehicle summary | `{ total_vehicles, moving_vehicles, tracking_health }` |
| `get_lorry_status` | Read | Returns telemetry position, speed, heading, status for `lorry_id` | `{ lorry_id, speed_kmh, status, active_route_id }` |
| `get_driver_status` | Read | Returns driver details and lorry assignment | `{ driver_id, name, phone_number, assigned_lorry_id }` |
| `report_delay` | Controlled Write | Records driver delay and creates event | `DRIVER_DELAY_REPORTED` event |
| `report_breakdown` | Controlled Write | Records emergency breakdown and creates event | `DRIVER_BREAKDOWN_REPORTED` event |
| `confirm_delivery` | Controlled Write | Confirms shipment delivery | `DELIVERY_CONFIRMED` event |
| `explain_assignment` | Read | Returns OR-Tools VRP optimization explanation | `{ shipment_id, assigned_lorry_id, reason }` |

---

## Primary Scenario: `report_delay` Execution
- **Trigger**: Driver reports a 45-minute loading delay over PSTN call.
- **Payload**: `{"lorry_id": "L03", "delay_minutes": 45, "reason": "LOADING_DELAY"}`
- **Execution**: Validates `L03`, verifies positive integer delay, creates `DRIVER_DELAY_REPORTED` event (Source: `ATLAS_VOICE`, Severity: `WARNING`), and updates operational state.
- **Output**: `{"success": true, "event_id": "evt_...", "lorry_id": "L03", "delay_minutes": 45}`.
