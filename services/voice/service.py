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
from services.voice.config import voice_config
from services.api.app import crud

class VoiceService:
    """Master Voice Operations Service Orchestrator."""

    def __init__(self):
        self._call_records: Dict[str, CallRecord] = {}
        self._active_driver_calls: Dict[str, str] = {}  # driver_id -> call_id

    def get_provider(self, requested_provider: Optional[str] = None) -> VoiceProvider:
        prov_name = (requested_provider or voice_config.active_provider).lower()
        if prov_name == "vapi" and voice_config.is_real_vapi_configured:
            return VapiVoiceProvider()
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
            if driver and driver.phone_number:
                phone_number = driver.phone_number

        context = {
            "driver_id": d_id,
            "lorry_id": lorry_id,
            "phone_number": phone_number,
            "call_type": request.call_type.value
        }

        active_prov = self.get_provider(provider_name)
        call_record = active_prov.initiate_outbound_call(request, context)

        # Store in local record memory
        self._call_records[call_record.id] = call_record
        if call_record.status in [CallStatus.QUEUED, CallStatus.RINGING, CallStatus.IN_PROGRESS]:
            self._active_driver_calls[d_id] = call_record.id

        # Persist Call Record in PostgreSQL / SQLite DB if session available
        if db:
            try:
                from services.api.app.schemas import CallCreate
                call_create = CallCreate(
                    driver_id=d_id,
                    lorry_id=lorry_id,
                    call_type=request.call_type.value,
                    status=call_record.status.value,
                    phone_number=phone_number
                )
                db_rec = await crud.create_call(db, call_create)
                call_record.id = db_rec.id
                self._call_records[db_rec.id] = call_record
            except Exception as err:
                print(f"Warning: Failed to persist CallRecord to DB: {err}")

        return call_record

    def get_call_records(self, limit: int = 50) -> List[CallRecord]:
        records = list(self._call_records.values())
        records.sort(key=lambda r: r.created_at, reverse=True)
        return records[:limit]

    def get_call_record_by_id(self, call_id: str) -> Optional[CallRecord]:
        return self._call_records.get(call_id)

    def get_health(self) -> VoiceHealthResponse:
        prov = voice_config.active_provider
        is_configured = voice_config.is_real_vapi_configured
        return VoiceHealthResponse(
            provider="vapi" if is_configured else "demo",
            mode="REAL" if is_configured else "DEMO",
            configured=is_configured,
            provider_reachable=True,
            real_pstn_verified=False,
            webhook_url=f"{voice_config.webhook_base_url}/api/v1/voice/webhooks/vapi"
        )

voice_service = VoiceService()
