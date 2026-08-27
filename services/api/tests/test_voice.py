"""
Fleetos ATLAS Voice Agent Automated Test Suite
Module Boundary: services/api/tests/test_voice.py
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from services.api.app.main import app

client = TestClient(app)

def test_voice_health_endpoint():
    """Test voice health and readiness endpoint."""
    response = client.get("/api/v1/voice/health")
    assert response.status_code == 200
    data = response.json()
    assert "provider" in data
    assert "mode" in data
    assert "configured" in data

def test_initiate_driver_call():
    """Test initiating an outbound call to a driver (Demo mode)."""
    payload = {
        "driver_id": "D03",
        "phone_number": "+919876543210",
        "call_type": "STATUS_CHECK"
    }
    response = client.post("/api/v1/voice/calls", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["driver_id"] == "D03"
    assert data["status"] == "COMPLETED"
    assert "call_id" in data

def test_demo_status_check_lifecycle_and_context():
    """Test clean STATUS_CHECK completes without delay event and uses actual driver/lorry context."""
    payload = {
        "driver_id": "D01",
        "call_type": "STATUS_CHECK"
    }
    response = client.post("/api/v1/voice/calls", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["driver_id"] == "D01"
    assert data["lorry_id"] in ["L01", "L03"]
    assert data["status"] == "COMPLETED"
    assert data["duration_seconds"] > 0
    assert data["event_id"] is None
    assert "Routine status check completed" in data["outcome_summary"]
    assert "D01" in data["transcript"]

def test_demo_delay_report_lifecycle_context_and_event():
    """Test DELAY_REPORT executes report_delay tool, creates event, populates event_id, and uses D02/L02 context."""
    payload = {
        "driver_id": "D02",
        "call_type": "DELAY_REPORT"
    }
    response = client.post("/api/v1/voice/calls", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["driver_id"] == "D02"
    assert data["lorry_id"] == "L02"
    assert data["status"] == "COMPLETED"
    assert data["duration_seconds"] == 45
    assert data["event_id"] is not None
    assert "L02" in data["outcome_summary"]
    assert "D02" in data["transcript"]
    assert "L02" in data["transcript"]

    # Verify event exists in GET /api/v1/events
    evt_res = client.get("/api/v1/events")
    assert evt_res.status_code == 200
    events = evt_res.json()
    matching_evt = next((e for e in events if e["id"] == data["event_id"]), None)
    assert matching_evt is not None
    assert matching_evt["event_type"] == "DRIVER_DELAY_REPORTED"
    assert matching_evt["lorry_id"] == "L02"
    assert matching_evt["source"] == "ATLAS_VOICE"

def test_demo_d03_l03_context():
    """Test D03/L03 DELAY_REPORT uses D03/L03 context without generic hardcoding."""
    payload = {
        "driver_id": "D03",
        "call_type": "DELAY_REPORT"
    }
    response = client.post("/api/v1/voice/calls", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["driver_id"] == "D03"
    assert data["lorry_id"] == "L03"
    assert data["status"] == "COMPLETED"
    assert data["event_id"] is not None
    assert "L03" in data["outcome_summary"]
    assert "D03" in data["transcript"]

def test_vapi_webhook_tool_call_execution():
    """Test Vapi webhook tool execution (report_delay creates event)."""
    webhook_payload = {
        "message": {
            "type": "tool-calls",
            "call": {"id": "vapi_test_call_100"},
            "toolCalls": [
                {
                    "id": "tool_call_001",
                    "function": {
                        "name": "report_delay",
                        "arguments": {
                            "lorry_id": "L03",
                            "delay_minutes": 45,
                            "reason": "LOADING_DELAY"
                        }
                    }
                }
            ]
        }
    }
    response = client.post("/api/v1/voice/webhooks/vapi", json=webhook_payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 1
    assert "DRIVER_DELAY_REPORTED" in data["results"][0]["result"] or "L03" in data["results"][0]["result"]

def test_list_and_get_voice_calls():
    """Test listing voice calls and retrieving specific call detail."""
    res_list = client.get("/api/v1/voice/calls")
    assert res_list.status_code == 200
    records = res_list.json()
    assert isinstance(records, list)
    assert len(records) > 0

    target_id = records[0]["id"]
    res_detail = client.get(f"/api/v1/voice/calls/{target_id}")
    assert res_detail.status_code == 200
    assert res_detail.json()["id"] == target_id

def test_no_duplicate_call_records_in_memory_or_api():
    """Regression test ensuring GET /api/v1/voice/calls contains zero duplicate call IDs."""
    res_list = client.get("/api/v1/voice/calls")
    assert res_list.status_code == 200
    records = res_list.json()
    record_ids = [r["id"] for r in records]
    assert len(record_ids) == len(set(record_ids)), f"Duplicate call IDs found in API response: {record_ids}"

def test_polling_does_not_duplicate_events_or_calls():
    """Test repeated GET requests do NOT create duplicate calls or duplicate events."""
    calls_before = len(client.get("/api/v1/voice/calls").json())
    events_before = len(client.get("/api/v1/events").json())

    # Repeated GET requests
    for _ in range(5):
        client.get("/api/v1/voice/calls")
        client.get("/api/v1/events")

    calls_after = len(client.get("/api/v1/voice/calls").json())
    events_after = len(client.get("/api/v1/events").json())

    assert calls_before == calls_after, "Polling GET /api/v1/voice/calls created duplicate call records!"
    assert events_before == events_after, "Polling GET /api/v1/events created duplicate events!"
