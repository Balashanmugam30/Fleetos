# Fleetos Database Schema Specification

Product: **Fleetos**  
Database Technology: PostgreSQL / Supabase & SQLite async engine (`SQLAlchemy 2.x`)

---

## Entity Relationship Blueprint

```
                      +-------------------+
                      |      drivers      |
                      +-------------------+
                               |
                               | 1:N
                               v
                      +-------------------+
                      |      lorries      |
                      +-------------------+
                         |             |
                     1:N |             | 1:N
                         v             v
       +-------------------+         +-------------------+
       |    assignments    |         |      routes       |
       +-------------------+         +-------------------+
                 |                             |
             N:1 |                             | 1:N
                 v                             v
       +-------------------+         +-------------------+
       |     shipments     |         |    route_stops    |
       +-------------------+         +-------------------+
```

---

## Table Definitions

### 1. `drivers`
- `id` (VARCHAR 64, PK): e.g. `D01`, `D05`
- `name` (VARCHAR 128): Full driver name
- `phone_number` (VARCHAR 32): E.164 phone format e.g. `+919876510001`
- `availability_status` (VARCHAR 32): `AVAILABLE`, `ON_DUTY`, `ON_BREAK`, `UNAVAILABLE`
- `current_lorry_id` (VARCHAR 64): FK to `lorries.id`

### 2. `lorries`
- `id` (VARCHAR 64, PK): e.g. `L01`, `L03`, `L05`
- `registration_number` (VARCHAR 32, Unique)
- `max_weight_kg` (FLOAT, > 0)
- `max_volume_m3` (FLOAT, > 0)
- `current_latitude` (FLOAT), `current_longitude` (FLOAT)
- `fuel_efficiency_km_l` (FLOAT, > 0): Fuel consumption in km/L
- `driver_id` (VARCHAR 64, FK to `drivers.id`)
- `status` (VARCHAR 32): `IDLE`, `EN_ROUTE`, `LOADING`, `UNAVAILABLE`, `DELAYED`

### 3. `shipments`
- `id` (VARCHAR 64, PK): e.g. `S01` to `S12`
- `weight_kg` (FLOAT, > 0), `volume_m3` (FLOAT, > 0)
- `pickup_address` (TEXT), `pickup_latitude` (FLOAT), `pickup_longitude` (FLOAT)
- `destination_address` (TEXT), `destination_latitude` (FLOAT), `destination_longitude` (FLOAT)
- `delivery_deadline` (TIMESTAMP WITH TIME ZONE)
- `priority` (VARCHAR 16): `LOW`, `NORMAL`, `HIGH`, `URGENT`
- `status` (VARCHAR 32): `UNASSIGNED`, `ASSIGNED`, `PICKED_UP`, `IN_TRANSIT`, `DELIVERED`, `CANCELLED`, `AT_RISK`

### 4. `assignments`
- `id` (VARCHAR 64, PK): e.g. `asg_s12_l03`
- `shipment_id` (VARCHAR 64, FK to `shipments.id`)
- `lorry_id` (VARCHAR 64, FK to `lorries.id`)
- `sequence` (INTEGER)
- `assignment_reason` (TEXT)
- `status` (VARCHAR 32): `ACTIVE`, `COMPLETED`, `CANCELLED`, `REASSIGNED`

### 5. `events`
- `id` (VARCHAR 64, PK): e.g. `evt_delay_01`
- `event_type` (VARCHAR 64): e.g. `DRIVER_DELAY_REPORTED`, `SHIPMENT_REASSIGNED`
- `source` (VARCHAR 32): `ATLAS_VOICE`, `DISPATCHER_WEB`, `AR_VIEW`, `SYSTEM`
- `severity` (VARCHAR 16): `INFO`, `WARNING`, `CRITICAL`
- `payload_json` (JSONB)
- `resolution_status` (VARCHAR 32): `PENDING`, `REOPTIMIZED`, `RESOLVED`

### 6. Supporting Tables
- `routes`, `route_stops`, `calls`, `optimization_runs`, `tracking_positions`.
