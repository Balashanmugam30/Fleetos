"""
Fleetos Telephony & Voice Provider Adapter Interface
Module Boundary: services/voice/provider.py
"""

from typing import Dict, Any, Optional
from services.voice.models import OutboundCallRequest, CallRecord, CallStatus

class VoiceProvider:
    """Abstract Telephony Provider Adapter."""

    def initiate_outbound_call(self, request: OutboundCallRequest, context: Dict[str, Any]) -> CallRecord:
        raise NotImplementedError()

    def get_call_status(self, external_call_id: str) -> Optional[CallStatus]:
        raise NotImplementedError()

    def get_health(self) -> Dict[str, Any]:
        raise NotImplementedError()
