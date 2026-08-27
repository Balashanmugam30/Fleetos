"""
Fleetos Voice Agent & Telephony REST Router
Module Boundary: services/api/app/routers/voice.py
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.app.db.database import get_db
from services.voice.models import OutboundCallRequest, CallRecord, VoiceHealthResponse
from services.voice.service import voice_service
from services.voice.webhooks import voice_webhook_normalizer

router = APIRouter(prefix="/api/v1/voice", tags=["ATLAS Voice Operations"])

@router.get("/health", response_model=VoiceHealthResponse)
async def get_voice_health():
    """Returns ATLAS Voice Service health and configuration status."""
    return voice_service.get_health()

@router.post("/calls", response_model=CallRecord, status_code=status.HTTP_201_CREATED)
async def initiate_driver_call(
    request: OutboundCallRequest,
    provider: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Initiates an outbound telephony call to a driver."""
    try:
        return await voice_service.initiate_driver_call(request, db=db, provider_name=provider)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Call dispatch failed: {str(err)}")

@router.get("/calls", response_model=List[CallRecord])
async def list_voice_calls(limit: int = 50):
    """Lists recent voice call records."""
    return voice_service.get_call_records(limit=limit)

@router.get("/calls/{call_id}", response_model=CallRecord)
async def get_voice_call_detail(call_id: str):
    """Retrieves specific voice call details."""
    record = voice_service.get_call_record_by_id(call_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Call record '{call_id}' not found.")
    return record

@router.post("/webhooks/vapi")
async def receive_vapi_webhook(payload: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    """Webhook callback endpoint for Vapi status events and tool call execution."""
    try:
        return await voice_webhook_normalizer.process_vapi_webhook(payload, db=db)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Webhook processing error: {str(err)}")
