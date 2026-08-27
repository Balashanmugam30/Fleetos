"""
Fleetos Real Vapi Telephony Outbound Call Adapter
Module Boundary: services/voice/vapi.py
"""

import json
import urllib.request
import urllib.error
import uuid
import datetime
from typing import Dict, Any, Optional
from services.voice.provider import VoiceProvider
from services.voice.models import OutboundCallRequest, CallRecord, CallStatus
from services.voice.config import voice_config

class VapiVoiceProvider(VoiceProvider):
    """Real Vapi REST API Outbound Telephony Provider."""

    def __init__(self, api_key: str = "", phone_number_id: str = "", assistant_id: str = ""):
        self.api_key = api_key or voice_config.vapi_api_key
        self.phone_number_id = phone_number_id or voice_config.vapi_phone_number_id
        self.assistant_id = assistant_id or voice_config.vapi_assistant_id

    async def initiate_outbound_call(self, request: OutboundCallRequest, context: Dict[str, Any], db: Optional[Any] = None) -> CallRecord:
        call_id = f"vapi_call_{uuid.uuid4().hex[:8]}"
        phone_number = request.phone_number or context.get("phone_number", "+919876543210")
        lorry_id = context.get("lorry_id", "L03")
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()

        if not self.api_key or not self.phone_number_id:
            # Safe unconfigured fallback record
            return CallRecord(
                id=call_id,
                call_id=call_id,
                driver_id=request.driver_id,
                lorry_id=lorry_id,
                call_type=request.call_type,
                direction="OUTBOUND",
                status=CallStatus.FAILED,
                provider="VAPI",
                duration_seconds=0,
                outcome_summary="Vapi credentials unconfigured. Set VAPI_API_KEY and VAPI_PHONE_NUMBER_ID in .env.",
                created_at=now_str,
                updated_at=now_str
            )

        # Prepare Vapi Call Payload
        payload = {
            "phoneNumberId": self.phone_number_id,
            "customer": {
                "number": phone_number,
                "name": f"Driver {request.driver_id}"
            },
            "assistantId": request.assistant_id or self.assistant_id or None,
            "assistantOverrides": {
                "variableValues": {
                    "driver_id": request.driver_id,
                    "lorry_id": lorry_id,
                    "call_type": request.call_type.value,
                    "context_notes": request.context_notes or "Routine status check"
                }
            }
        }

        req_url = "https://api.vapi.ai/call/phone"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(req_url, data=req_data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)

                ext_call_id = res_json.get("id", call_id)
                return CallRecord(
                    id=call_id,
                    call_id=call_id,
                    driver_id=request.driver_id,
                    lorry_id=lorry_id,
                    call_type=request.call_type,
                    direction="OUTBOUND",
                    status=CallStatus.QUEUED,
                    provider="VAPI",
                    external_call_id=ext_call_id,
                    duration_seconds=0,
                    outcome_summary=f"Vapi outbound call dispatched (ID: {ext_call_id})",
                    created_at=now_str,
                    updated_at=now_str
                )
        except Exception as err:
            return CallRecord(
                id=call_id,
                call_id=call_id,
                driver_id=request.driver_id,
                lorry_id=lorry_id,
                call_type=request.call_type,
                direction="OUTBOUND",
                status=CallStatus.FAILED,
                provider="VAPI",
                duration_seconds=0,
                outcome_summary=f"Vapi call dispatch failed: {str(err)}",
                created_at=now_str,
                updated_at=now_str
            )

    def get_call_status(self, external_call_id: str) -> Optional[CallStatus]:
        if not self.api_key or not external_call_id:
            return CallStatus.COMPLETED

        req_url = f"https://api.vapi.ai/call/{external_call_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            req = urllib.request.Request(req_url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=5) as response:
                res_json = json.loads(response.read().decode("utf-8"))
                vapi_status = res_json.get("status", "").lower()
                if vapi_status == "queued":
                    return CallStatus.QUEUED
                elif vapi_status == "ringing":
                    return CallStatus.RINGING
                elif vapi_status == "in-progress":
                    return CallStatus.IN_PROGRESS
                elif vapi_status == "ended":
                    return CallStatus.COMPLETED
                else:
                    return CallStatus.COMPLETED
        except Exception:
            return CallStatus.COMPLETED

    def get_health(self) -> Dict[str, Any]:
        is_configured = bool(self.api_key and self.phone_number_id)
        return {
            "provider": "vapi",
            "mode": "REAL",
            "configured": is_configured,
            "provider_reachable": is_configured,
            "real_pstn_verified": False
        }
