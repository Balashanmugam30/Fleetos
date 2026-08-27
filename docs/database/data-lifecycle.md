# Fleetos Data Lifecycle & State Transition Rules

Product: **Fleetos**

---

## State Transition Guardrails

### Shipment Status Transitions
`UNASSIGNED` → `ASSIGNED` → `PICKED_UP` → `IN_TRANSIT` → `DELIVERED`  
`*` → `AT_RISK` → `IN_TRANSIT` / `DELIVERED`  
`DELIVERED` and `CANCELLED` are terminal states; backwards transitions (e.g. `DELIVERED` → `PENDING`) are rejected with `400 BAD REQUEST`.

### Driver Status Transitions
`AVAILABLE` ↔ `ON_DUTY` ↔ `ON_BREAK` ↔ `UNAVAILABLE`
