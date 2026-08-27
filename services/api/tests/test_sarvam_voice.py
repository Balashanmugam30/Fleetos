"""
Fleetos Sarvam Multilingual Voice Agent Automated Test Suite
Module Boundary: services/api/tests/test_sarvam_voice.py
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from services.api.app.main import app
from services.voice.sarvam_config import sarvam_config

client = TestClient(app)

def test_sarvam_config_defaults():
    """Test Sarvam configuration properties and fallback properties."""
    assert hasattr(sarvam_config, "is_sarvam_configured")
    assert hasattr(sarvam_config, "is_twilio_configured")
    assert hasattr(sarvam_config, "is_real_pstn_ready")
    assert sarvam_config.sarvam_api_base_url == "https://api.sarvam.ai"

def test_sarvam_tool_report_delay_endpoint():
    """Test POST /api/v1/voice/sarvam/tools/report-delay tool execution."""
    payload = {
        "driver_id": "D03",
        "lorry_id": "L03",
        "delay_minutes": 45,
        "reason": "LOADING_DELAY",
        "tool_call_id": "test_sarvam_tc_999"
    }
    response = client.post("/api/v1/voice/sarvam/tools/report-delay", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["driver_id"] == "D03"
    assert data["lorry_id"] == "L03"
    assert data["delay_minutes"] == 45
    assert data["event_type"] == "DRIVER_DELAY_REPORTED"
    assert data["event_id"] is not None

def test_sarvam_tool_report_delay_idempotency():
    """Test replaying the exact same tool_call_id returns existing event without creating duplicate."""
    payload = {
        "driver_id": "D03",
        "lorry_id": "L03",
        "delay_minutes": 45,
        "reason": "LOADING_DELAY",
        "tool_call_id": "test_sarvam_tc_idempotent_100"
    }
    resp1 = client.post("/api/v1/voice/sarvam/tools/report-delay", json=payload)
    assert resp1.status_code == 200
    evt_id_1 = resp1.json()["event_id"]

    resp2 = client.post("/api/v1/voice/sarvam/tools/report-delay", json=payload)
    assert resp2.status_code == 200
    evt_id_2 = resp2.json()["event_id"]

    assert evt_id_1 == evt_id_2, f"Idempotency failed: {evt_id_1} != {evt_id_2}"
