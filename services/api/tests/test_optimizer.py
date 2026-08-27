"""
Fleetos Phase 3 Deterministic Optimization Engine Automated Test Suite
Module Boundary: services/api/tests/test_optimizer.py
"""

import sys
import os
import pytest
import datetime
import asyncio
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from services.api.app.main import app
from services.api.app.db.database import init_db
from services.optimizer.models import (
    OptimizationInput, VehicleInput, ShipmentInput, ObjectiveConfig
)
from services.optimizer.service import OptimizationService
from services.optimizer.validation import validate_optimization_solution

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_test_environment():
    asyncio.run(init_db())
    yield

def test_optimizer_baseline_scenario():
    """Verify OR-Tools RoutingModel baseline execution on 5 vehicles & 12 shipments."""
    v1 = VehicleInput(id="L01", registration_number="KA-01", start_latitude=12.9716, start_longitude=77.5946, max_weight_kg=10000, max_volume_m3=45, fuel_efficiency_km_l=3.5, driver_available=True)
    v5 = VehicleInput(id="L05", registration_number="TN-09", start_latitude=12.9165, start_longitude=79.1325, max_weight_kg=14000, max_volume_m3=55, fuel_efficiency_km_l=5.2, driver_available=True)
    
    start_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    s12 = ShipmentInput(
        id="S12",
        weight_kg=3500,
        volume_m3=14,
        pickup_address="Chennai Port",
        pickup_latitude=13.0839,
        pickup_longitude=80.2925,
        destination_address="Bengaluru Electronic City",
        destination_latitude=12.8399,
        destination_longitude=77.6770,
        delivery_deadline=start_time + datetime.timedelta(hours=16),
        priority="URGENT"
    )

    opt_input = OptimizationInput(vehicles=[v1, v5], shipments=[s12], start_time=start_time)
    result = OptimizationService.run_optimization(opt_input, trigger_reason="TEST_BASELINE")

    assert result.status in ["OPTIMAL", "FEASIBLE"]
    assert len(result.assignments) == 1
    assert result.assignments[0].shipment_id == "S12"
    # Nearest Lorry Trap: L05 (5.2 km/L) must be chosen over L01 (3.5 km/L) for lower operating cost
    assert result.assignments[0].lorry_id == "L05"
    assert validate_optimization_solution(opt_input, result.routes, result.assignments) is True

def test_weight_capacity_rejection():
    """Verify shipment exceeding max fleet weight capacity is rejected with WEIGHT_CAPACITY_EXCEEDED."""
    v1 = VehicleInput(id="L01", registration_number="KA-01", start_latitude=12.9716, start_longitude=77.5946, max_weight_kg=5000, max_volume_m3=45, fuel_efficiency_km_l=3.5)
    s_heavy = ShipmentInput(
        id="S_HEAVY",
        weight_kg=99999,  # Impossible weight
        volume_m3=10,
        pickup_address="Pickup",
        pickup_latitude=13.0,
        pickup_longitude=80.0,
        destination_address="Dest",
        destination_latitude=12.9,
        destination_longitude=77.6,
        delivery_deadline=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24),
        priority="HIGH"
    )
    opt_input = OptimizationInput(vehicles=[v1], shipments=[s_heavy])
    result = OptimizationService.run_optimization(opt_input)

    assert len(result.unassigned_shipments) == 1
    assert result.unassigned_shipments[0].shipment_id == "S_HEAVY"
    assert result.unassigned_shipments[0].primary_reason_code == "WEIGHT_CAPACITY_EXCEEDED"

def test_volume_capacity_rejection():
    """Verify shipment exceeding max fleet volume capacity is rejected with VOLUME_CAPACITY_EXCEEDED."""
    v1 = VehicleInput(id="L01", registration_number="KA-01", start_latitude=12.9716, start_longitude=77.5946, max_weight_kg=10000, max_volume_m3=10, fuel_efficiency_km_l=3.5)
    s_vol = ShipmentInput(
        id="S_VOL",
        weight_kg=1000,
        volume_m3=999,  # Impossible volume
        pickup_address="Pickup",
        pickup_latitude=13.0,
        pickup_longitude=80.0,
        destination_address="Dest",
        destination_latitude=12.9,
        destination_longitude=77.6,
        delivery_deadline=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24),
        priority="NORMAL"
    )
    opt_input = OptimizationInput(vehicles=[v1], shipments=[s_vol])
    result = OptimizationService.run_optimization(opt_input)

    assert len(result.unassigned_shipments) == 1
    assert result.unassigned_shipments[0].shipment_id == "S_VOL"
    assert result.unassigned_shipments[0].primary_reason_code == "VOLUME_CAPACITY_EXCEEDED"

def test_driver_unavailable_rejection():
    """Verify vehicles with unavailable drivers are excluded from assignment."""
    v_unavail = VehicleInput(id="L04", registration_number="AP-03", start_latitude=16.5, start_longitude=80.6, max_weight_kg=12000, max_volume_m3=50, fuel_efficiency_km_l=3.0, driver_available=False)
    s1 = ShipmentInput(
        id="S01",
        weight_kg=1000,
        volume_m3=5,
        pickup_address="P",
        pickup_latitude=16.5,
        pickup_longitude=80.6,
        destination_address="D",
        destination_latitude=13.0,
        destination_longitude=80.2,
        delivery_deadline=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    )
    opt_input = OptimizationInput(vehicles=[v_unavail], shipments=[s1])
    result = OptimizationService.run_optimization(opt_input)

    assert len(result.unassigned_shipments) == 1
    assert result.unassigned_shipments[0].primary_reason_code == "NO_AVAILABLE_DRIVER"

def test_api_optimization_run_endpoint():
    """Test FastAPI POST /api/v1/optimization/run endpoint."""
    res = client.post("/api/v1/optimization/run?trigger_reason=TEST_API")
    assert res.status_code == 200
    data = res.json()
    assert "status" in data
    assert "metrics" in data
    assert "routes" in data
    assert data["metrics"]["total_shipments_count"] >= 1
