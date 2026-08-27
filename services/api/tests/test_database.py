"""
Fleetos Phase 2 Database & CRUD API Automated Test Suite
Module Boundary: services/api/tests/test_database.py
"""

import sys
import os
import uuid
import pytest
import datetime
import asyncio
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from services.api.app.main import app
from services.api.app.db.database import init_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    asyncio.run(init_db())
    yield

def test_health_endpoints():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    response = client.get("/api/v1/health/db")
    assert response.status_code == 200
    assert response.json()["database"] == "connected"

def test_version_endpoint():
    response = client.get("/api/v1/version")
    assert response.status_code == 200
    data = response.json()
    assert "Routing Solver / RoutingModel" in data["optimization_solver"]

def test_driver_crud():
    unique_id = f"D_test_{uuid.uuid4().hex[:6]}"
    driver_data = {
        "id": unique_id,
        "name": "Test Driver",
        "phone_number": "+919876599999",
        "availability_status": "AVAILABLE"
    }
    # Create Driver
    res = client.post("/api/v1/drivers", json=driver_data)
    assert res.status_code == 201
    assert res.json()["id"] == unique_id

    # Get Driver
    res = client.get(f"/api/v1/drivers/{unique_id}")
    assert res.status_code == 200
    assert res.json()["name"] == "Test Driver"

    # Patch Driver Status
    res = client.patch(f"/api/v1/drivers/{unique_id}", json={"availability_status": "ON_DUTY"})
    assert res.status_code == 200
    assert res.json()["availability_status"] == "ON_DUTY"

def test_lorry_crud_and_validation():
    unique_id = f"L_test_{uuid.uuid4().hex[:6]}"
    unique_reg = f"TEST-{uuid.uuid4().hex[:6].upper()}"
    lorry_data = {
        "id": unique_id,
        "registration_number": unique_reg,
        "max_weight_kg": 10000.0,
        "max_volume_m3": 40.0,
        "fuel_efficiency_km_l": 4.0,
        "current_latitude": 12.9716,
        "current_longitude": 77.5946,
        "status": "IDLE"
    }
    # Create Lorry
    res = client.post("/api/v1/lorries", json=lorry_data)
    assert res.status_code == 201
    assert res.json()["id"] == unique_id

    # Invalid Weight Validation (gt=0)
    invalid_lorry = lorry_data.copy()
    invalid_lorry["id"] = f"L_inv_{uuid.uuid4().hex[:6]}"
    invalid_lorry["registration_number"] = f"INV-{uuid.uuid4().hex[:6]}"
    invalid_lorry["max_weight_kg"] = -500.0
    res = client.post("/api/v1/lorries", json=invalid_lorry)
    assert res.status_code == 422  # Pydantic validation error

def test_shipment_crud_and_status_transitions():
    unique_id = f"S_test_{uuid.uuid4().hex[:6]}"
    shipment_data = {
        "id": unique_id,
        "weight_kg": 2000.0,
        "volume_m3": 8.0,
        "pickup_address": "Test Pickup",
        "pickup_latitude": 13.0827,
        "pickup_longitude": 80.2707,
        "destination_address": "Test Destination",
        "destination_latitude": 12.8399,
        "destination_longitude": 77.6770,
        "delivery_deadline": "2026-08-30T18:00:00Z",
        "priority": "HIGH",
        "status": "UNASSIGNED"
    }
    # Create Shipment
    res = client.post("/api/v1/shipments", json=shipment_data)
    assert res.status_code == 201
    assert res.json()["id"] == unique_id

    # Valid Transition: UNASSIGNED -> ASSIGNED
    res = client.patch(f"/api/v1/shipments/{unique_id}", json={"status": "ASSIGNED"})
    assert res.status_code == 200
    assert res.json()["status"] == "ASSIGNED"

    # Invalid State Transition: ASSIGNED -> PENDING (Not allowed)
    res = client.patch(f"/api/v1/shipments/{unique_id}", json={"status": "PENDING"})
    assert res.status_code == 400
    assert "Invalid shipment status transition" in res.json()["detail"]

def test_event_persistence():
    event_data = {
        "event_type": "DRIVER_DELAY_REPORTED",
        "source": "ATLAS_VOICE",
        "severity": "WARNING",
        "lorry_id": "L03",
        "payload_json": {"delay_minutes": 45, "reason": "traffic"}
    }
    res = client.post("/api/v1/events", json=event_data)
    assert res.status_code == 201
    assert res.json()["event_type"] == "DRIVER_DELAY_REPORTED"

    # List Events
    res = client.get("/api/v1/events")
    assert res.status_code == 200
    assert len(res.json()) >= 1
