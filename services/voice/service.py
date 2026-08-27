"""
Fleetos Voice Service Orchestrator
Module Boundary: services/voice/service.py
"""

import uuid
import datetime
from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from services.voice.models import OutboundCallRequest, CallRecord, CallStatus, CallType, VoiceHealthResponse
from services.voice.provider import VoiceProvider
from services.voice.vapi import VapiVoiceProvider
from services.voice.simulator import DemoVoiceProvider
from services.voice.twilio_provider import TwilioConversationRelayProvider
from services.voice.sarvam_provider import SarvamVoiceProvider
from services.voice.sarvam_config import sarvam_config
from services.voice.twilio_config import twilio_config
from services.voice.config import voice_config
from services.api.app import crud

class VoiceService:
    """Master Voice Operations Service Orchestrator."""

    def __init__(self):
        self._call_records: Dict[str, CallRecord] = {}
        self._active_driver_calls: Dict[str, str] = {}  # driver_id -> call_id

    def get_provider(self, requested_provider: Optional[str] = None) -> VoiceProvider:
        prov_name = (requested_provider or voice_config.active_provider).lower()
        if prov_name in ["sarvam", "real"]:
            if sarvam_config.is_sarvam_configured:
                return SarvamVoiceProvider()
            elif requested_provider in ["sarvam", "real"]:
                raise ValueError("Sarvam Voice Agent credentials are not configured in .env (SARVAM_API_KEY required).")
            return DemoVoiceProvider()

        elif prov_name == "twilio":
            if twilio_config.is_twilio_configured:
                return TwilioConversationRelayProvider()
            elif requested_provider == "twilio":
                raise ValueError("Twilio credentials are not configured in .env.")
            return DemoVoiceProvider()

        elif prov_name in ["vapi", "legacy-vapi"]:
            if voice_config.is_real_vapi_configured:
                return VapiVoiceProvider()
            elif requested_provider in ["vapi", "legacy-vapi"]:
                raise ValueError("Vapi credentials are not configured in .env.")
            return DemoVoiceProvider()

        return DemoVoiceProvider()

    async def initiate_driver_call(
        self,
        request: OutboundCallRequest,
        db: Optional[AsyncSession] = None,
        provider_name: Optional[str] = None
    ) -> CallRecord:
        d_id = request.driver_id.upper().strip()

        # Enforce Driver Call Throttling (1 active call per driver)
        existing_call_id = self._active_driver_calls.get(d_id)
        if existing_call_id and existing_call_id in self._call_records:
            existing_rec = self._call_records[existing_call_id]
            if existing_rec.status in [CallStatus.QUEUED, CallStatus.RINGING, CallStatus.IN_PROGRESS]:
                raise ValueError(f"Driver {d_id} already has an active call in progress ({existing_rec.id}).")

        # Resolve Driver Details & Assigned Lorry
        lorry_id = f"L0{d_id[-1]}" if d_id[-1].isdigit() else "L03"
        phone_number = "+919876543210"

        if db:
            driver = await crud.get_driver(db, d_id)
            if driver:
                if driver.phone_number:
                    phone_number = driver.phone_number
                if driver.current_lorry_id:
                    lorry_id = driver.current_lorry_id

        context = {
            "driver_id": d_id,
            "lorry_id": lorry_id,
            "phone_number": phone_number,
            "call_type": request.call_type.value,
            "language": getattr(request, "custom_variables", {}).get("language", sarvam_config.sarvam_default_language)
        }

        active_prov = self.get_provider(provider_name)
        call_record = await active_prov.initiate_outbound_call(request, context, db=db)

        # Store in local record memory under canonical call_record.id
        self._call_records[call_record.id] = call_record
        if call_record.status in [CallStatus.QUEUED, CallStatus.RINGING, CallStatus.IN_PROGRESS]:
            self._active_driver_calls[d_id] = call_record.id

        # Persist Call Record in PostgreSQL / SQLite DB if session available
        if db:
            try:
                from services.api.app.schemas import CallCreate
                call_create = CallCreate(
                    id=call_record.id,
                    provider=call_record.provider,
                    driver_id=d_id,
                    lorry_id=lorry_id,
                    call_type=request.call_type.value,
                    status=call_record.status.value,
                    phone_number=phone_number,
                    event_id=call_record.event_id,
                    transcript=call_record.transcript,
                    outcome_summary=call_record.outcome_summary,
                    duration_seconds=call_record.duration_seconds
                )
                db_rec = await crud.create_call(db, call_create)
                if db_rec.id != call_record.id:
                    old_id = call_record.id
                    self._call_records.pop(old_id, None)
                    call_record.id = db_rec.id
                    self._call_records[db_rec.id] = call_record
            except Exception as err:
                print(f"Warning: Failed to persist CallRecord to DB: {err}")

        return call_record

    def get_call_records(self, limit: int = 50) -> List[CallRecord]:
        deduped: Dict[str, CallRecord] = {}
        for r in self._call_records.values():
            deduped[r.id] = r
        records = list(deduped.values())
        records.sort(key=lambda r: r.created_at, reverse=True)
        return records[:limit]

    def get_call_record_by_id(self, call_id: str) -> Optional[CallRecord]:
        return self._call_records.get(call_id)

    def get_health(self) -> VoiceHealthResponse:
        is_sarvam_ok = sarvam_config.is_sarvam_configured
        is_twilio_ok = sarvam_config.is_twilio_configured
        is_real = sarvam_config.is_real_pstn_ready

        base_url = sarvam_config.webhook_base_url.rstrip('/')
        return VoiceHealthResponse(
            provider="sarvam" if is_sarvam_ok else "demo",
            mode="REAL" if is_real else "DEMO",
            configured=is_real,
            sarvam_configured=is_sarvam_ok,
            twilio_configured=is_twilio_ok,
            openai_configured=bool(voice_config.is_openai_configured),
            public_webhook_configured=sarvam_config.is_public_webhook_configured,
            websocket_configured=True,
            outbound_ready=is_real,
            tool_ready=True,
            real_pstn_ready=is_real,
            provider_reachable=True,
            real_pstn_verified=is_real,
            webhook_url=f"{base_url}/api/v1/voice/sarvam/tools/report-delay"
        )

voice_service = VoiceService()
