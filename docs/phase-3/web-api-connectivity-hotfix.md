# Fleetos Phase 3 Web/API Connectivity Hotfix Report

Product: **Fleetos**  
Scope: **Server-Side Fetch Failures & Local Service Connectivity Recovery**

---

## 1. Observed Errors & Symptoms
- **Symptom**: Navigating to data-backed routes (`/fleet`, `/shipments`) in Next.js produced `[ Server ] Error: fetch failed` at `apps/web/lib/api.ts` during server-side rendering.
- **Impact**: Next.js Server Component pages threw unhandled exceptions when attempting to fetch backend data.

---

## 2. Root Cause Analysis
1. **Primary Root Cause**: The FastAPI backend server process (`services/api/app/main.py`) was not running on port 8000 when Next.js Server Components executed server-side `fetch()`, causing Node.js to reject with `ECONNREFUSED`.
2. **Secondary Root Cause**: Node 22 on Windows resolves `localhost` to IPv6 (`::1:8000`) before IPv4 (`127.0.0.1:8000`), requiring explicit IPv4 binding (`127.0.0.1` / `0.0.0.0`).
3. **Tertiary Root Cause**: Unhandled network exceptions in `apps/web/lib/api.ts` bubbled up into Server Component page renders rather than displaying a clean, user-friendly offline status state.

---

## 3. Remediation Actions
1. **FastAPI Backend Startup**: Started FastAPI server on port 8000 (`python -m uvicorn services.api.app.main:app --host 0.0.0.0 --port 8000`).
2. **Resilience Fetch Helper**: Created `safeFleetosFetch()` in `apps/web/lib/api.ts` with explicit `API_BASE_URL = process.env.API_BASE_URL || process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000"`.
3. **UI Error Boundaries & Offline Banners**: Updated `/fleet` and `/shipments` pages to display bright, professional amber warning banners if the backend is offline, while rendering real persisted L01-L05 and S01-S12 database records when online.
4. **KPI Dashboard Data Binding**: Bound `/dashboard` KPI counters to real API health and database counts via `Promise.all([fetchLorries(), fetchShipments(), fetchDBHealth()])`.

---

## 4. Verified Connectivity
- `http://127.0.0.1:8000/api/v1/health` => Status 200
- `http://127.0.0.1:8000/api/v1/health/db` => Status 200
- `http://127.0.0.1:8000/api/v1/lorries` => Status 200 (5 Lorries)
- `http://127.0.0.1:8000/api/v1/shipments` => Status 200 (12 Shipments)
- `http://localhost:3000/fleet` => Status 200 (Real L01-L05 records rendered)
- `http://localhost:3000/shipments` => Status 200 (Real S01-S12 records rendered)

---

## 5. Test Suite Verification
- **Python Backend & Optimizer Tests**: `python -m pytest` passed 11/11 tests (100%).
- **Next.js Production Build**: `pnpm --filter web build` compiled 9/9 static & dynamic pages with exit code 0.
