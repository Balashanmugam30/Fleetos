"""
Fleetos Voice Call Models & Schemas
Module Boundary: services/voice/models.py
"""

from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import datetime

class CallType(str, Enum):
    STATUS_CHECK = "STATUS_CHECK"
    DELAY_REPORT = "DELAY_REPORT"
    BREAKDOWN_REPORT = "BREAKDOWN_REPORT"
    ASSIGNMENT_CONFIRMATION = "ASSIGNMENT_CONFIRMATION"
    DELIVERY_CONFIRMATION = "DELIVERY_CONFIRMATION"

class CallStatus(str, Enum):
    QUEUED = "QUEUED"
    RINGING = "RINGING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    NO_ANSWER = "NO_ANSWER"
    CANCELLED = "CANCELLED"

class OutboundCallRequest(BaseModel):
    driver_id: str
    phone_number: Optional[str] = None
    call_type: CallType = CallType.STATUS_CHECK
    assistant_id: Optional[str] = None
    context_notes: Optional[str] = None
    custom_variables: Dict[str, Any] = {}

class CallRecord(BaseModel):
    id: str
    call_id: str
    driver_id: str
    lorry_id: Optional[str] = None
    call_type: CallType
    direction: str = "OUTBOUND"
    status: CallStatus
    provider: str  # 'VAPI' | 'DEMO'
    external_call_id: Optional[str] = None
    duration_seconds: int = 0
    event_id: Optional[str] = None
    transcript: Optional[str] = None
    outcome_summary: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

class VoiceHealthResponse(BaseModel):
    provider: str
    mode: str  # 'REAL' | 'DEMO'
    configured: bool
    sarvam_configured: bool = False
    twilio_configured: bool = False
    twilio_credentials_valid: bool = False
    twilio_trial_voice_available: bool = False
    twilio_provisioned_number_count: int = 0
    sarvam_number_imported: bool = False
    openai_configured: bool = False
    public_webhook_configured: bool = False
    websocket_configured: bool = False
    outbound_ready: bool = False
    tool_ready: bool = False
    real_pstn_ready: bool = False
    provider_reachable: bool = True
    real_pstn_verified: bool = False
    webhook_url: str
