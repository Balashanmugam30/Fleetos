# Fleetos Tracking REST API Specification

Product: **Fleetos**  
Base Path: `/api/v1/tracking`

---

## Endpoints

### 1. `GET /api/v1/tracking/latest`
Returns latest vehicle tracking states for all active lorries (L01-L05).

**Response Schema**: `List[VehicleTrackingState]`

### 2. `GET /api/v1/tracking/vehicles/{vehicle_id}`
Returns the latest tracking state for a specific lorry.

### 3. `GET /api/v1/tracking/vehicles/{vehicle_id}/history`
Returns recent location history for a specific lorry.

### 4. `POST /api/v1/tracking/ingest`
Ingests a new position update object.

### 5. `POST /api/v1/tracking/simulator/start`
Starts the development GPS tracking simulator.

### 6. `POST /api/v1/tracking/simulator/stop`
Stops the development GPS tracking simulator.

### 7. `GET /api/v1/tracking/simulator/status`
Returns the status of the development GPS simulator.
