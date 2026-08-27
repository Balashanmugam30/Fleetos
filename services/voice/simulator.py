"""
Fleetos Offline Demo Voice Simulator Provider
Module Boundary: services/voice/simulator.py
"""

import uuid
import datetime
from typing import Dict, Any, Optional
from services.voice.provider import VoiceProvider
from services.voice.models import OutboundCallRequest, CallRecord, CallStatus

class DemoVoiceProvider(VoiceProvider):
    """Offline Demo Voice Simulator Adapter."""

    def __init__(self):
        self._simulated_calls: Dict[str, CallRecord] = {}

    def initiate_outbound_call(self, request: OutboundCallRequest, context: Dict[str, Any]) -> CallRecord:
        call_id = f"demo_call_{uuid.uuid4().hex[:8]}"
        lorry_id = context.get("lorry_id", "L03")

        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        record = CallRecord(
            id=call_id,
            call_id=call_id,
            driver_id=request.driver_id,
            lorry_id=lorry_id,
            call_type=request.call_type,
            direction="OUTBOUND",
            status=CallStatus.IN_PROGRESS,
            provider="DEMO",
            external_call_id=f"ext_{call_id}",
            duration_seconds=32,
            transcript=f"ATLAS: Hello, driver {request.driver_id}. Are you on schedule? Driver: Loading is taking 45 mins longer. ATLAS: Recording 45-minute delay.",
            outcome_summary="Simulated 45-minute loading delay reported for Lorry L03.",
            created_at=now_str,
            updated_at=now_str
        )
        self._simulated_calls[call_id] = record
        return record

    def get_call_status(self, external_call_id: str) -> Optional[CallStatus]:
        for rec in self._simulated_calls.values():
            if rec.external_call_id == external_call_id or rec.call_id == external_call_id:
                return rec.status
        return CallStatus.COMPLETED

    def get_health(self) -> Dict[str, Any]:
        return {
            "provider": "demo",
            "mode": "DEMO",
            "configured": True,
            "provider_reachable": True,
            "real_pstn_verified": False
        }
