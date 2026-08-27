"""
Fleetos Sarvam Multilingual Voice Agent Provider
Module Boundary: services/voice/sarvam_provider.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

import uuid
import datetime
from typing import Dict, Any, Optional
import httpx
from services.voice.provider import VoiceProvider
from services.voice.models import OutboundCallRequest, CallRecord, CallStatus, CallType
from services.voice.sarvam_config import sarvam_config

class SarvamVoiceProvider(VoiceProvider):
    """Sarvam Indic Voice Agents Multilingual Outbound Telephony Provider."""

    def __init__(self):
        self._active_calls: Dict[str, CallRecord] = {}

    def get_outbound_endpoint(self) -> str:
        """Resolves official Sarvam Voice Agent outbound API endpoint."""
        if sarvam_config.sarvam_outbound_endpoint:
            return sarvam_config.sarvam_outbound_endpoint

        base_url = sarvam_config.sarvam_api_base_url.rstrip('/')
        if sarvam_config.sarvam_campaign_id:
            return f"{base_url}/campaigns/{sarvam_config.sarvam_campaign_id}/calls"
        elif sarvam_config.sarvam_agent_id:
            return f"{base_url}/agents/{sarvam_config.sarvam_agent_id}/calls"
        
        # Official fallback endpoint for Sarvam Voice Agents
        return f"{base_url}/voice/outbound-calls"

    async def initiate_outbound_call(
        self,
        request: OutboundCallRequest,
        context: Dict[str, Any],
        db: Optional[Any] = None
    ) -> CallRecord:
        call_id = f"sarvam_call_{uuid.uuid4().hex[:8]}"
        driver_id = request.driver_id.upper().strip()
        lorry_id = str(context.get("lorry_id") or f"L0{driver_id[-1]}").upper().strip()
        phone_number = request.phone_number or context.get("phone_number", "+919876543210")
        language = context.get("language") or getattr(request, "language", sarvam_config.sarvam_default_language)

        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()

        if not sarvam_config.is_sarvam_configured:
            raise ValueError("Sarvam Voice Agent credentials are not configured in .env (SARVAM_API_KEY required).")

        sarvam_url = self.get_outbound_endpoint()

        call_payload = {
            "agent_id": sarvam_config.sarvam_agent_id or "atlas-logistics-agent",
            "deployment_id": sarvam_config.sarvam_deployment_id,
            "campaign_id": sarvam_config.sarvam_campaign_id,
            "phone_number": phone_number,
            "language": language,
            "custom_metadata": {
                "call_id": call_id,
                "driver_id": driver_id,
                "lorry_id": lorry_id,
                "call_type": request.call_type.value,
                "tool_webhook_url": f"{sarvam_config.webhook_base_url.rstrip('/')}/api/v1/voice/sarvam/tools/report-delay"
            }
        }

        headers = {
            "api-subscription-key": sarvam_config.sarvam_api_key,
            "Authorization": f"Bearer {sarvam_config.sarvam_api_key}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(sarvam_url, json=call_payload, headers=headers)

            if resp.status_code not in [200, 201, 202]:
                err_msg = resp.json().get("message", resp.text) if resp.content else f"HTTP {resp.status_code}"
                raise RuntimeError(f"Sarvam Voice Call Dispatch Failed (HTTP {resp.status_code}): {err_msg}")

            result_json = resp.json()
            external_sid = result_json.get("call_id") or result_json.get("id") or result_json.get("campaign_id")
            if not external_sid:
                external_sid = f"sarvam_sid_{uuid.uuid4().hex[:10]}"

        except Exception as err:
            raise RuntimeError(f"Sarvam Outbound API Error: {err}")

        record = CallRecord(
            id=call_id,
            call_id=call_id,
            driver_id=driver_id,
            lorry_id=lorry_id,
            call_type=request.call_type,
            direction="OUTBOUND",
            status=CallStatus.RINGING,
            provider="SARVAM",
            external_call_id=external_sid,
            started_at=now_str,
            created_at=now_str,
            updated_at=now_str
        )
        self._active_calls[call_id] = record
        return record

    def get_call_status(self, external_call_id: str) -> Optional[CallStatus]:
        for rec in self._active_calls.values():
            if rec.external_call_id == external_call_id or rec.call_id == external_call_id:
                return rec.status
        return CallStatus.COMPLETED

    def get_health(self) -> Dict[str, Any]:
        return {
            "provider": "sarvam",
            "mode": "REAL" if sarvam_config.is_real_pstn_ready else "DEMO",
            "configured": sarvam_config.is_real_pstn_ready,
            "provider_reachable": True,
            "real_pstn_verified": sarvam_config.is_real_pstn_ready
        }
