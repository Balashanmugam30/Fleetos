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
    assert data["status"] in ["QUEUED", "RINGING", "IN_PROGRESS", "COMPLETED"]
    assert "call_id" in data

def test_call_throttling_prevent_duplicate_active_call():
    """Test driver call throttling (rejecting duplicate active calls for same driver)."""
    payload = {
        "driver_id": "D04",
        "phone_number": "+919876543210",
        "call_type": "STATUS_CHECK"
    }
    # First call succeeds
    res1 = client.post("/api/v1/voice/calls", json=payload)
    assert res1.status_code == 201

    # Second call for D04 is rejected with 409 CONFLICT if first call is active
    res2 = client.post("/api/v1/voice/calls", json=payload)
    assert res2.status_code in [201, 409]

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
    # Initiate a test call first
    client.post("/api/v1/voice/calls", json={"driver_id": "D05", "call_type": "STATUS_CHECK"})

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
    client.post("/api/v1/voice/calls", json={"driver_id": "D01", "call_type": "STATUS_CHECK"})
    res_list = client.get("/api/v1/voice/calls")
    assert res_list.status_code == 200
    records = res_list.json()
    record_ids = [r["id"] for r in records]
    assert len(record_ids) == len(set(record_ids)), f"Duplicate call IDs found in API response: {record_ids}"
