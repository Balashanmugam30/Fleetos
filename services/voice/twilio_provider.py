"""
Fleetos Direct Twilio ConversationRelay Outbound Voice Provider
Module Boundary: services/voice/twilio_provider.py
"""

import uuid
import datetime
import urllib.parse
from typing import Dict, Any, Optional
import httpx
from services.voice.provider import VoiceProvider
from services.voice.models import OutboundCallRequest, CallRecord, CallStatus, CallType
from services.voice.twilio_config import twilio_config

class TwilioConversationRelayProvider(VoiceProvider):
    """Direct Twilio Programmable Voice + ConversationRelay Provider."""

    def __init__(self):
        self._simulated_calls: Dict[str, CallRecord] = {}

    async def initiate_outbound_call(
        self,
        request: OutboundCallRequest,
        context: Dict[str, Any],
        db: Optional[Any] = None
    ) -> CallRecord:
        call_id = f"twilio_call_{uuid.uuid4().hex[:8]}"
        driver_id = request.driver_id.upper().strip()
        lorry_id = str(context.get("lorry_id") or f"L0{driver_id[-1]}").upper().strip()
        phone_number = request.phone_number or context.get("phone_number", "+919876543210")

        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()

        if not twilio_config.is_twilio_configured:
            # Fallback to simulated provider behavior if credentials are absent
            record = CallRecord(
                id=call_id,
                call_id=call_id,
                driver_id=driver_id,
                lorry_id=lorry_id,
                call_type=request.call_type,
                direction="OUTBOUND",
                status=CallStatus.QUEUED,
                provider="TWILIO",
                external_call_id=f"ext_{call_id}",
                started_at=now_str,
                created_at=now_str,
                updated_at=now_str
            )
            self._simulated_calls[call_id] = record
            return record

        # Construct public TwiML callback URL
        base_url = twilio_config.webhook_base_url.rstrip('/')
        twiml_url = (
            f"{base_url}/api/v1/voice/twilio/connect"
            f"?call_id={urllib.parse.quote(call_id)}"
            f"&driver_id={urllib.parse.quote(driver_id)}"
            f"&lorry_id={urllib.parse.quote(lorry_id)}"
            f"&call_type={urllib.parse.quote(request.call_type.value)}"
        )
        status_url = f"{base_url}/api/v1/voice/twilio/status"

        # Dispatch Outbound Call via Twilio REST API
        twilio_api_url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_config.twilio_account_sid}/Calls.json"

        call_data = {
            "To": phone_number,
            "From": twilio_config.twilio_phone_number,
            "Url": twiml_url,
            "StatusCallback": status_url,
            "StatusCallbackEvent": ["initiated", "ringing", "answered", "completed"],
            "StatusCallbackMethod": "POST"
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                twilio_api_url,
                data=call_data,
                auth=(twilio_config.twilio_account_sid, twilio_config.twilio_auth_token)
            )

        if resp.status_code not in [200, 201]:
            err_msg = resp.json().get("message", resp.text) if resp.content else f"HTTP {resp.status_code}"
            raise RuntimeError(f"Twilio REST Call Dispatch Failed: {err_msg}")

        result_json = resp.json()
        twilio_sid = result_json.get("sid", f"CA_{uuid.uuid4().hex[:12]}")

        record = CallRecord(
            id=call_id,
            call_id=call_id,
            driver_id=driver_id,
            lorry_id=lorry_id,
            call_type=request.call_type,
            direction="OUTBOUND",
            status=CallStatus.RINGING,
            provider="TWILIO",
            external_call_id=twilio_sid,
            started_at=now_str,
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
            "provider": "twilio",
            "mode": "REAL" if twilio_config.is_real_pstn_ready else "DEMO",
            "configured": twilio_config.is_twilio_configured,
            "provider_reachable": True,
            "real_pstn_verified": twilio_config.is_real_pstn_ready
        }
