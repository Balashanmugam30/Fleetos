"""
Fleetos Twilio ConversationRelay Voice Automated Test Suite
Module Boundary: services/api/tests/test_twilio_voice.py
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from services.api.app.main import app
from services.voice.twilio_config import twilio_config
from services.voice.atlas_engine import atlas_engine

client = TestClient(app)

def test_twilio_config_defaults():
    """Test Twilio configuration properties and default safety states."""
    assert hasattr(twilio_config, "is_twilio_configured")
    assert hasattr(twilio_config, "is_openai_configured")
    assert hasattr(twilio_config, "is_real_pstn_ready")

def test_twiml_connect_endpoint():
    """Test POST /api/v1/voice/twilio/connect returns valid ConversationRelay TwiML."""
    response = client.post("/api/v1/voice/twilio/connect?call_id=test_123&driver_id=D03&lorry_id=L03&call_type=STATUS_CHECK")
    assert response.status_code == 200
    assert "xml" in response.headers.get("content-type", "")
    content = response.text
    assert "<ConversationRelay" in content
    assert 'name="call_id"' in content
    assert 'name="driver_id"' in content
    assert 'name="lorry_id"' in content

def test_twilio_status_callback():
    """Test POST /api/v1/voice/twilio/status status normalization."""
    payload = {
        "CallSid": "CA_test_sid_999",
        "CallStatus": "in-progress"
    }
    response = client.post("/api/v1/voice/twilio/status", data=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["mapped_status"] == "IN_PROGRESS"

def test_atlas_engine_fallback_report_delay():
    """Test AtlasEngine executes report_delay tool and returns confirmation text."""
    import asyncio
    from services.api.app.db.database import AsyncSessionLocal

    async def run():
        async with AsyncSessionLocal() as db:
            conv = [{"role": "user", "content": "I am 45 minutes late due to loading delay."}]
            res = await atlas_engine.generate_response(conv, driver_id="D03", lorry_id="L03", call_type="DELAY_REPORT", db=db)
            assert "text" in res
            assert "45" in res["text"] or "Fleetos" in res["text"]
            assert res["tool_executed"] == "report_delay"
            assert res["tool_result"] is not None
            assert res["tool_result"]["event_type"] == "DRIVER_DELAY_REPORTED"

    asyncio.run(run())
