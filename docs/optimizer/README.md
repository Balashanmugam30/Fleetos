# Fleetos Optimization Engine (Google OR-Tools Routing Solver / RoutingModel)

Product: **Fleetos**  
Engine Abstraction: **Google OR-Tools Routing Solver / RoutingModel (`RoutingIndexManager`, `RoutingModel`)**

---

## Engine Overview & Architecture

The Fleetos Optimization Engine is the authoritative mathematical core of Fleetos. It formulates and solves the Multi-Vehicle Routing Problem with Capacity & Time Windows (CVRP-TW).

### Core Components
1. `models.py`: Normalized input/output data schemas (`VehicleInput`, `ShipmentInput`, `ObjectiveConfig`, `OptimizationResult`).
2. `matrix.py`: Distance & duration matrix provider (`HaversineTravelTimeProvider`).
3. `feasibility.py`: Pre-flight cheap feasibility diagnostics (weight, volume, driver availability, deadline pre-checks).
4. `cost.py`: Vehicle-specific fuel modeling (`distance / fuel_efficiency_km_l`), driver cost, fixed vehicle cost.
5. `explain.py`: Non-hallucinated structured JSON explanation generator.
6. `validation.py`: Independent post-solution physical constraint validator.
7. `routing.py`: OR-Tools `RoutingModel` engine with capacity dimensions, time dimension, and pickup-delivery constraints.
8. `service.py`: `OptimizationService` master orchestrator.
