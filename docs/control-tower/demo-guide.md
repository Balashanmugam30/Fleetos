# Fleetos Phase 5 Control Tower Hackathon Demonstration Guide

Product: **Fleetos** (Agentic Multimodal Fleet Intelligence Platform)

---

## Step-by-Step Demo Script

### 1. Launch Services
```bash
# Terminal 1: Start FastAPI Backend
python -m uvicorn services.api.app.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start Next.js Control Tower Dashboard
pnpm --filter web dev
```

### 2. Open Control Tower UI
Open `http://localhost:3000/dashboard` in a browser.

### 3. Demonstrate GPS Telemetry Simulation
1. Click **Start Simulator** in the Control Panel.
2. Observe vehicle markers (L01, L02, L03, L05) moving in real-time on the `FleetMap` canvas.
3. Observe **Moving Vehicles** counter increment to `4` in the KPI strip.
4. Click vehicle marker **L03** on the map.
5. Observe the **Vehicle Telemetry Detail Panel** updating with L03 speed (60 km/h), heading, coordinates, driver, and capacity.
6. Scroll to **Operational Event Stream** and observe `VEHICLE_STARTED_MOVING` events logged.
7. Click **Stop Simulator** and observe telemetry degrading to `STALE` after the freshness threshold.

### 4. Demonstrate Optimization & Routing Integration
1. Click **Open Optimization Solver Control Tower** or navigate to `/optimization`.
2. Click **Run Optimization Solver** to invoke Google OR-Tools Routing Solver.
3. Observe solver output (`STATUS: OPTIMAL`), assigned routes, total operating cost ($842.50), and fuel estimate (312.4 L).
