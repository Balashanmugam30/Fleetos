"""
Automated Test Suite for Fleetos Tracking Engine & API
Module Boundary: services/api/tests/test_tracking.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

import pytest
import datetime
from fastapi.testclient import TestClient

from services.api.app.main import app
from services.tracking.models import TrackingPosition, TrackingFreshness, TrackingStatus
from services.tracking.validation import validate_telemetry_position, TelemetryValidationError
from services.tracking.service import TrackingService
from services.tracking.simulator import SimulatorTrackingProvider

client = TestClient(app)

def test_telemetry_validation_pass():
    now = datetime.datetime.now(datetime.timezone.utc)
    pos = TrackingPosition(
        vehicle_id="L01",
        latitude=12.9716,
        longitude=77.5946,
        speed_kmh=55.4,
        heading_degrees=90.0,
        recorded_at=now,
        received_at=now
    )
    validated = validate_telemetry_position(pos)
    assert validated.vehicle_id == "L01"
    assert validated.latitude == 12.9716
    assert validated.heading_degrees == 90.0

def test_telemetry_validation_invalid_latitude():
    now = datetime.datetime.now(datetime.timezone.utc)
    with pytest.raises(Exception):
        TrackingPosition(
            vehicle_id="L01",
            latitude=120.0,  # Invalid
            longitude=77.5946,
            recorded_at=now
        )

def test_freshness_thresholds():
    service = TrackingService()
    assert service.calculate_freshness(10.0) == TrackingFreshness.LIVE
    assert service.calculate_freshness(45.0) == TrackingFreshness.RECENT
    assert service.calculate_freshness(200.0) == TrackingFreshness.STALE
    assert service.calculate_freshness(400.0) == TrackingFreshness.OFFLINE

def test_status_transitions_and_events():
    service = TrackingService()
    now = datetime.datetime.now(datetime.timezone.utc)
    
    # 1. Ingest stopped vehicle
    pos1 = TrackingPosition(
        vehicle_id="L01",
        latitude=12.9716,
        longitude=77.5946,
        speed_kmh=0.0,
        recorded_at=now,
        received_at=now
    )
    state1 = service.ingest_position(pos1)
    assert state1.status == TrackingStatus.STOPPED

    # 2. Transition to moving
    pos2 = TrackingPosition(
        vehicle_id="L01",
        latitude=12.9800,
        longitude=77.6000,
        speed_kmh=45.0,
        recorded_at=now,
        received_at=now
    )
    state2 = service.ingest_position(pos2)
    assert state2.status == TrackingStatus.MOVING
    
    # Verify event generated
    assert len(service.events_log) > 0
    assert service.events_log[0]["event_type"] == "VEHICLE_STARTED_MOVING"

def test_simulator_provider():
    sim = SimulatorTrackingProvider()
    sim.start()
    assert sim.is_running is True
    
    positions = sim.get_latest_positions()
    assert len(positions) == 5
    vehicle_ids = {p.vehicle_id for p in positions}
    assert vehicle_ids == {"L01", "L02", "L03", "L04", "L05"}
    
    sim.stop()
    assert sim.is_running is False

def test_tracking_rest_api():
    # Test simulator start
    res_start = client.post("/api/v1/tracking/simulator/start")
    assert res_start.status_code == 200
    assert res_start.json()["status"] == "running"

    # Test simulator status
    res_status = client.get("/api/v1/tracking/simulator/status")
    assert res_status.status_code == 200
    assert res_status.json()["running"] is True

    # Test GET latest states
    res_latest = client.get("/api/v1/tracking/latest")
    assert res_latest.status_code == 200
    states = res_latest.json()
    assert len(states) == 5

    # Test GET vehicle state
    res_l01 = client.get("/api/v1/tracking/vehicles/L01")
    assert res_l01.status_code == 200
    assert res_l01.json()["vehicle_id"] == "L01"

    # Test GET vehicle history
    res_hist = client.get("/api/v1/tracking/vehicles/L01/history")
    assert res_hist.status_code == 200
    assert isinstance(res_hist.json(), list)

    # Test simulator stop
    res_stop = client.post("/api/v1/tracking/simulator/stop")
    assert res_stop.status_code == 200
    assert res_stop.json()["status"] == "stopped"
