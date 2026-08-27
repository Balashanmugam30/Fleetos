"""
Fleetos Telephony & Voice Provider Adapter Boundary
Module Boundary: services/voice
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel

class OutboundCallRequest(BaseModel):
    driver_id: str
    phone_number: str
    assistant_id: Optional[str] = None
    custom_variables: Dict[str, Any] = {}

class CallResponse(BaseModel):
    call_id: str
    status: str
    provider: str

class VoiceProvider:
    """Abstract Telephony Provider Adapter."""
    def initiate_outbound_call(self, request: OutboundCallRequest) -> CallResponse:
        raise NotImplementedError()

class VapiVoiceProvider(VoiceProvider):
    """Vapi + Twilio PSTN Outbound Calling Adapter."""
    def __init__(self, api_key: str, phone_number_id: str):
        self.api_key = api_key
        self.phone_number_id = phone_number_id

    def initiate_outbound_call(self, request: OutboundCallRequest) -> CallResponse:
        # Vapi API integration target for Phase 7
        return CallResponse(call_id="vapi_pending_01", status="QUEUED", provider="VAPI")

class DemoVoiceProvider(VoiceProvider):
    """Offline Demo Voice Simulator Provider."""
    def initiate_outbound_call(self, request: OutboundCallRequest) -> CallResponse:
        return CallResponse(call_id="demo_call_01", status="SIMULATED", provider="DEMO_SIMULATOR")
