# Fleetos Control Tower User & Architecture Manual

Product: **Fleetos** (Agentic Multimodal Fleet Intelligence Platform)  
Visual Theme: **Bright Enterprise Logistics Control Tower** (Light UI Theme)

---

## 1. Control Tower Dashboard Overview
The Fleetos Control Tower provides a unified real-time operational dashboard for dispatchers and fleet operations managers.

### Layout Hierarchy
1. **Header & Navigation**: Brand title, environment status, `Control Tower Active` indicator.
2. **GPS Simulator Controls**: Toggle live development telemetry streaming (`DEMO TELEMETRY`).
3. **KPI Summary Strip**: Real-time counters for Active Fleet, Moving Vehicles, Stopped/Idle Vehicles, Stale Telemetry, Total Load Volume, and At-Risk Shipments.
4. **Live Vector Telemetry Map (`FleetMap`)**: Vector canvas displaying live lorry markers (L01-L05), speed, heading, freshness badges, and position coordinates.
5. **Vehicle Telemetry Detail Panel (`VehicleDetailPanel`)**: Selected vehicle profile displaying registration, driver ID, speed, heading, coordinates, active route, and capacity.
6. **Operational Event Stream (`EventStream`)**: Log of live tracking lifecycle events (`VEHICLE_STARTED_MOVING`, `VEHICLE_STOPPED`, `VEHICLE_TRACKING_STALE`, etc.) with expandable details.
7. **At-Risk Shipments Monitor**: Deadlines and assigned vehicles for urgent loads (e.g. S12).
8. **Optimization Engine Summary**: Google OR-Tools Routing Solver cost breakdown ($842.50) and fuel estimate (312.4 L).
