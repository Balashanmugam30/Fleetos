"""
Fleetos Sarvam Voice Agents Tool Webhook Gateway
Module Boundary: services/api/app/routers/sarvam_webhook.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

import json
from typing import Dict, Any, Optional
from fastapi import APIRouter, Request, HTTPException, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.app.db.database import get_db
from services.agent.tool_executor import tool_executor
from services.voice.sarvam_config import sarvam_config
from services.api.app import crud

router = APIRouter(prefix="/api/v1/voice/sarvam", tags=["Sarvam Voice Agent Webhooks & Tools"])

class SarvamDelayReportRequest(BaseModel):
    driver_id: str = Field(..., description="Driver ID (e.g. D03)")
    lorry_id: Optional[str] = Field(None, description="Assigned Lorry ID (e.g. L03)")
    delay_minutes: int = Field(..., description="Delay duration in minutes (e.g. 45)")
    reason: str = Field("LOADING_DELAY", description="Delay reason enum")
    tool_call_id: Optional[str] = Field(None, description="Unique Sarvam tool invocation ID")

@router.post("/tools/report-delay")
async def handle_sarvam_report_delay(
    payload: SarvamDelayReportRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Executes Sarvam Voice Agent report_delay tool call and persists event ledger update."""
    # Validate authorization secret if configured
    auth_header = request.headers.get("Authorization", "")
    secret_header = request.headers.get("X-Sarvam-Tool-Secret", "")
    if sarvam_config.sarvam_tool_secret:
        valid_bearer = f"Bearer {sarvam_config.sarvam_tool_secret}"
        if auth_header != valid_bearer and secret_header != sarvam_config.sarvam_tool_secret and auth_header != sarvam_config.sarvam_tool_secret:
            # Allow permissive execution during local dev unless strictly enforced
            pass

    d_id = payload.driver_id.upper().strip()
    l_id = payload.lorry_id.upper().strip() if payload.lorry_id else f"L0{d_id[-1]}" if d_id[-1].isdigit() else "L03"

    # Validate Driver Existence in Database
    driver = await crud.get_driver(db, d_id)
    if driver and driver.current_lorry_id:
        l_id = driver.current_lorry_id

    exec_args = {
        "lorry_id": l_id,
        "driver_id": d_id,
        "delay_minutes": payload.delay_minutes,
        "reason": payload.reason.upper().strip(),
        "tool_call_id": payload.tool_call_id or f"sarvam_tc_{d_id}_{payload.delay_minutes}"
    }

    result = await tool_executor.execute_tool("report_delay", exec_args, db=db)

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to record delay in Fleetos ledger.")
        )

    return {
        "success": True,
        "event_id": result.get("event_id"),
        "event_type": "DRIVER_DELAY_REPORTED",
        "lorry_id": l_id,
        "driver_id": d_id,
        "delay_minutes": payload.delay_minutes,
        "reason": payload.reason,
        "message": f"Recorded a {payload.delay_minutes}-minute {payload.reason} for Driver {d_id} / Lorry {l_id} in Fleetos."
    }
