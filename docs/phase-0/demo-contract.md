# Phase 0 Contract: Fleetos Canonical Demo & Anchor Moment

Product Name: **Fleetos**

---

## 1. Canonical Demo Dataset Specification

### Vehicles (Lorries L01 – L05)

| Lorry ID | Reg Number | Max Weight (kg) | Max Volume ($m^3$) | Fuel Efficiency | Current Location | Driver | Initial Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **L01** | KA-01-EQ-1001 | 10,000 | 45.0 | 3.5 km/L | Bengaluru Hub | Driver Anand | EN_ROUTE |
| **L02** | KA-01-EQ-1002 | 15,000 | 60.0 | 2.8 km/L | Hosur Depot | Driver Suresh | EN_ROUTE |
| **L03** | TN-02-AB-3003 | 8,000 | 35.0 | 4.2 km/L | Chennai Central | Driver Rajesh | EN_ROUTE |
| **L04** | AP-03-CD-4004 | 12,000 | 50.0 | 3.0 km/L | Vijayawada Hub | Driver Vikram | UNAVAILABLE |
| **L05** | TN-09-XY-5005 | 14,000 | 55.0 | 5.2 km/L | Vellore Logistics | Driver Karthik | AVAILABLE |

### Key Shipments (S01 – S12) Focus Set

- **S01 – S11**: Baseline distributed fleet loads.
- **S12 (High Priority Target Shipment)**:
  - Weight: 3,500 kg
  - Volume: 14.0 $m^3$
  - Destination: Bengaluru Tech Park
  - Delivery Deadline: **Strict 18:00 IST** (Tight time window!)
  - Initial Assignment: **Lorry L03** (Driver Rajesh)

---

## 2. Canonical Demo Scenario Timeline

```
[00:00] INITIALIZATION
        • System loads 5 Lorries (L01-L05) and 12 Shipments (S01-S12).
        • OR-Tools calculates baseline optimal assignments.
        • L03 is assigned Shipment S12 (ETA 17:30 IST, meeting 18:00 deadline).

[00:30] AR SCANNING & ANCHOR MOMENT TRIGGER
        • User opens AR View (or WebAR overlay) and scans L03 reference marker.
        • AR overlays live status card: "L03 | Driver: Rajesh | Assigned: S12 | ETA: 17:30 | Status: EN_ROUTE".
        • User asks ATLAS: "What's happening with Lorry L03?"

[01:00] REAL TELEPHONY OUTBOUND VOICE CALL
        • Fleetos backend triggers Vapi API outbound call to Driver Rajesh (+91XXXXXXXXXX).
        • Physical Mobile Phone rings. User/Tester answers.
        • ATLAS speaks: "Hello Rajesh, this is ATLAS from Fleetos. Are you still on schedule for Shipment S12?"
        • Driver replies: "No, loading at Chennai terminal is delayed by 45 minutes."

[01:45] EVENT EXTRACTION & RE-OPTIMIZATION LOOP
        • ATLAS invokes `report_delay(lorry_id="L03", delay_minutes=45, reason="loading_delay")`.
        • Fleetos Backend updates L03 arrival prediction to 18:15 IST (DEADLINE BREACH RISK!).
        • OR-Tools Optimization Engine triggers automatic re-optimization.
        • OR-Tools detects L05 (Driver Karthik, 5.2 km/L, high capacity) is available at Vellore.
        • Optimal reassignment: **Shipment S12 reassigned from L03 to L05**.

[02:15] MULTIMODAL STATE UPDATE & CONFIRMATION
        • Fleetos places outbound notification call to Driver Karthik (L05) confirming reassignment.
        • Command Dashboard updates route visualization line from L03 to L05.
        • AR View on L03 updates live status badge: "S12 REASSIGNED TO L05 DUE TO DELAY".
        • Timeline displays complete event trail: Delay Event → Risk Flag → OR-Tools Re-optimization → Driver Call Confirmation.
```

---

## 3. Guarantees & Fallback Rules

- **Determinism**: The demo dataset produces identical, repeatable optimization decisions.
- **Fail-Safe Mode**: If telephony PSTN is offline, the Web Audio Simulator reproduces the exact webhook payloads without breaking dashboard or AR state.
