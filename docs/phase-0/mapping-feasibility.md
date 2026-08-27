# Phase 0 Feasibility Report: Mapping & Geospatial Routing

Product Requirement: **MAP RENDERING, DISTANCE/TIME ESTIMATION & ROUTE VISUALIZATION**

---

## 1. Geospatial Stack Architecture

1. **Map Rendering Engine**: Mapbox GL JS / Maplibre GL JS for interactive web vector maps.
2. **Distance & Routing Engine**: Mapbox Directions API / OSRM (Open Source Routing Machine).
3. **Spatial Computation**: Turf.js (Geodesic distance, bounding box calculations, convex hull grouping).
4. **Deterministic Fallback Engine**: Internal Haversine + Road Tortuosity Matrix Solver (ensures 100% offline demo execution without external API failure).

---

## 2. Cost & Fuel Efficiency Calculations

Transportation Cost Objective Function:
$$\text{Cost}(L, R) = \left( \frac{\text{Distance}(R)}{\text{FuelEfficiency}(L)} \times \text{FuelPricePerLiter} \right) + \text{DriverBaseCost} + \text{DelayPenalty}$$

Where:
- $\text{FuelEfficiency}(L)$ is given in km/L (e.g. L01: 3.5 km/L, L05: 5.2 km/L).
- A farther lorry with 5.2 km/L may produce a lower total transportation cost than a nearer lorry with 2.8 km/L!

---

## 3. Feasibility Status Assessment

| Capability | Preferred Tool | Alternative / Fallback | Feasibility Status |
| :--- | :--- | :--- | :--- |
| **Interactive Map Visualizer** | Mapbox GL JS | Leaflet / Maplibre GL | `VERIFIED` |
| **Route Distance / Duration API** | Mapbox Directions API | OSRM / Haversine Matrix | `VERIFIED` |
| **Geofencing & Spatial Filtering** | Turf.js | Python Shapely | `VERIFIED` |
| **Deterministic Offline Mode** | Cached Matrix JSON | Hardcoded Route Coordinates | `VERIFIED` |

---

## 4. Deterministic Demo Boundary

To protect the hackathon demo from external Mapbox rate limits or network latency:
- Pre-cached matrix distances between canonical hubs (Bengaluru, Chennai, Hyderabad, Mumbai, Pune, Delhi NCR).
- Automatic fallback to internal Haversine matrix if `MAPBOX_TOKEN` is absent or network fails.
