-- FLEETOS CANONICAL DATABASE DDL SCHEMA
-- Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)

CREATE TABLE IF NOT EXISTS drivers (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    phone_number VARCHAR(32) NOT NULL,
    availability_status VARCHAR(32) NOT NULL DEFAULT 'AVAILABLE',
    current_lorry_id VARCHAR(64),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lorries (
    id VARCHAR(64) PRIMARY KEY,
    registration_number VARCHAR(32) NOT NULL UNIQUE,
    max_weight_kg NUMERIC(10, 2) NOT NULL,
    max_volume_m3 NUMERIC(10, 2) NOT NULL,
    current_latitude NUMERIC(10, 6) NOT NULL,
    current_longitude NUMERIC(10, 6) NOT NULL,
    fuel_efficiency_km_l NUMERIC(5, 2) NOT NULL,
    driver_id VARCHAR(64) REFERENCES drivers(id),
    status VARCHAR(32) NOT NULL DEFAULT 'IDLE',
    current_route_id VARCHAR(64),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shipments (
    id VARCHAR(64) PRIMARY KEY,
    weight_kg NUMERIC(10, 2) NOT NULL,
    volume_m3 NUMERIC(10, 2) NOT NULL,
    pickup_address TEXT NOT NULL,
    pickup_latitude NUMERIC(10, 6) NOT NULL,
    pickup_longitude NUMERIC(10, 6) NOT NULL,
    destination_address TEXT NOT NULL,
    destination_latitude NUMERIC(10, 6) NOT NULL,
    destination_longitude NUMERIC(10, 6) NOT NULL,
    delivery_deadline TIMESTAMP WITH TIME ZONE NOT NULL,
    priority VARCHAR(16) NOT NULL DEFAULT 'NORMAL',
    status VARCHAR(32) NOT NULL DEFAULT 'UNASSIGNED',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assignments (
    id VARCHAR(64) PRIMARY KEY,
    shipment_id VARCHAR(64) NOT NULL REFERENCES shipments(id),
    lorry_id VARCHAR(64) NOT NULL REFERENCES lorries(id),
    sequence INTEGER NOT NULL DEFAULT 1,
    assignment_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS routes (
    id VARCHAR(64) PRIMARY KEY,
    lorry_id VARCHAR(64) NOT NULL REFERENCES lorries(id),
    distance_meters NUMERIC(12, 2) NOT NULL,
    estimated_duration_seconds INTEGER NOT NULL,
    fuel_estimate_liters NUMERIC(8, 2) NOT NULL,
    cost_estimate NUMERIC(10, 2) NOT NULL,
    deadline_risk VARCHAR(16) NOT NULL DEFAULT 'NONE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS route_stops (
    id VARCHAR(64) PRIMARY KEY,
    route_id VARCHAR(64) NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
    sequence INTEGER NOT NULL,
    stop_type VARCHAR(16) NOT NULL,
    shipment_id VARCHAR(64) REFERENCES shipments(id),
    latitude NUMERIC(10, 6) NOT NULL,
    longitude NUMERIC(10, 6) NOT NULL,
    address TEXT NOT NULL,
    estimated_arrival TIMESTAMP WITH TIME ZONE NOT NULL,
    deadline TIMESTAMP WITH TIME ZONE NOT NULL,
    completed BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS events (
    id VARCHAR(64) PRIMARY KEY,
    event_type VARCHAR(64) NOT NULL,
    source VARCHAR(32) NOT NULL,
    severity VARCHAR(16) NOT NULL DEFAULT 'INFO',
    lorry_id VARCHAR(64) REFERENCES lorries(id),
    shipment_id VARCHAR(64) REFERENCES shipments(id),
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    resolution_status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS calls (
    id VARCHAR(64) PRIMARY KEY,
    driver_id VARCHAR(64) REFERENCES drivers(id),
    lorry_id VARCHAR(64) REFERENCES lorries(id),
    call_type VARCHAR(32) NOT NULL,
    direction VARCHAR(16) NOT NULL DEFAULT 'OUTBOUND',
    status VARCHAR(32) NOT NULL DEFAULT 'QUEUED',
    started_at TIMESTAMP WITH TIME ZONE,
    ended_at TIMESTAMP WITH TIME ZONE,
    transcript_reference TEXT,
    event_id VARCHAR(64) REFERENCES events(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS optimization_runs (
    id VARCHAR(64) PRIMARY KEY,
    trigger_reason VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'OPTIMAL',
    input_snapshot_reference TEXT,
    total_cost NUMERIC(10, 2) NOT NULL,
    total_fuel_liters NUMERIC(8, 2) NOT NULL,
    deadline_violations_count INTEGER DEFAULT 0,
    unassigned_shipments JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tracking_positions (
    id BIGSERIAL PRIMARY KEY,
    lorry_id VARCHAR(64) NOT NULL REFERENCES lorries(id),
    latitude NUMERIC(10, 6) NOT NULL,
    longitude NUMERIC(10, 6) NOT NULL,
    speed_km_h NUMERIC(5, 2) DEFAULT 0.0,
    heading_degrees NUMERIC(5, 2) DEFAULT 0.0,
    status VARCHAR(32) NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
