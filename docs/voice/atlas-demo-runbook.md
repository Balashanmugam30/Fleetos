# Fleetos Phase 6 ATLAS Voice Agent Demonstration Runbook

Product: **Fleetos** (Agentic Multimodal Fleet Intelligence Platform)

---

## Step-by-Step Hackathon Demonstration Script

### 1. Open Voice Operations Center
1. Open `http://localhost:3000/ai` or click **Open ATLAS Voice Operations Center** from `/dashboard`.
2. Observe the **Readiness Banner** showing mode (`REAL VOICE` or `DEMO TELEPHONY MODE`) and Webhook URL.

### 2. Dispatch Outbound Call
1. Select **Driver D03 (Vikram Singh — Lorry L03)** in the call launcher.
2. Select purpose **STATUS_CHECK** or **DELAY_REPORT**.
3. Click **Dispatch ATLAS Call to D03**.
4. Observe the **Call History Matrix** updating with call record `IN_PROGRESS` or `COMPLETED`.

### 3. Demonstrate ATLAS Tool Execution & Event Linkage
1. In `DEMO TELEMETRY MODE` or live Vapi call, ATLAS converses with the driver and asks if loading is on schedule.
2. Driver reports a **45-minute loading delay**.
3. ATLAS confirms the delay and invokes the `report_delay` tool.
4. Backend executes `report_delay`, creating a `DRIVER_DELAY_REPORTED` event (Source: `ATLAS_VOICE`).
5. Open `http://localhost:3000/events` or `/dashboard` to observe the new `DRIVER_DELAY_REPORTED` event live on the Control Tower event stream!
