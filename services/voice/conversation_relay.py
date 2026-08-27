"""
Fleetos Twilio ConversationRelay WebSocket & TwiML Gateway
Module Boundary: services/voice/conversation_relay.py
"""

import json
import datetime
from typing import Dict, Any, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.voice.twilio_config import twilio_config
from services.voice.models import CallStatus, CallType
from services.voice.service import voice_service
from services.voice.atlas_engine import atlas_engine
from services.api.app.db.database import AsyncSessionLocal

router = APIRouter(prefix="/api/v1/voice/twilio", tags=["Twilio ConversationRelay Gateway"])

@router.post("/connect")
async def generate_twim_connect(request: Request):
    """Generates TwiML connecting the call to Twilio ConversationRelay WebSocket."""
    params = request.query_params
    call_id = params.get("call_id", "demo_call")
    driver_id = params.get("driver_id", "D03")
    lorry_id = params.get("lorry_id", "L03")
    call_type = params.get("call_type", "STATUS_CHECK")

    base_url = twilio_config.webhook_base_url.replace("http://", "ws://").replace("https://", "wss://").rstrip('/')
    ws_url = f"{base_url}/api/v1/voice/twilio/relay"

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <ConversationRelay url="{ws_url}" voice="en-US-Journey-F" dtmfDetection="true" interruptible="true">
            <Parameter name="call_id" value="{call_id}" />
            <Parameter name="driver_id" value="{driver_id}" />
            <Parameter name="lorry_id" value="{lorry_id}" />
            <Parameter name="call_type" value="{call_type}" />
        </ConversationRelay>
    </Connect>
</Response>"""
    return Response(content=twiml, media_type="application/xml")

@router.post("/status")
async def handle_twilio_status_callback(request: Request):
    """Normalizes Twilio call status events into Fleetos CallStatus."""
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    call_status = form_data.get("CallStatus", "").lower()

    new_status = CallStatus.IN_PROGRESS
    if call_status in ["queued", "initiated"]:
        new_status = CallStatus.QUEUED
    elif call_status in ["ringing"]:
        new_status = CallStatus.RINGING
    elif call_status in ["in-progress", "answered"]:
        new_status = CallStatus.IN_PROGRESS
    elif call_status in ["completed"]:
        new_status = CallStatus.COMPLETED
    elif call_status in ["busy", "no-answer", "canceled"]:
        new_status = CallStatus.NO_ANSWER
    elif call_status in ["failed"]:
        new_status = CallStatus.FAILED

    # Update in-memory call records if matching call SID exists
    for rec in voice_service.get_call_records(100):
        if rec.external_call_id == call_sid:
            rec.status = new_status
            rec.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
            break

    return {"status": "ok", "call_sid": call_sid, "mapped_status": new_status}

@router.websocket("/relay")
async def handle_conversation_relay_websocket(websocket: WebSocket):
    """Handles real-time Twilio ConversationRelay WebSocket streaming."""
    await websocket.accept()

    call_id: Optional[str] = None
    driver_id: str = "D03"
    lorry_id: str = "L03"
    call_type: str = "STATUS_CHECK"
    conversation_history: list = []
    transcript_lines: list = []
    last_event_id: Optional[str] = None
    last_outcome_summary: str = "Outbound ATLAS voice call completed."
    start_time = datetime.datetime.now(datetime.timezone.utc)

    try:
        while True:
            raw_data = await websocket.receive_text()
            if not raw_data:
                continue

            try:
                msg = json.loads(raw_data)
            except Exception:
                continue

            msg_type = msg.get("type")

            if msg_type == "setup":
                custom_params = msg.get("customParameters", {})
                call_id = custom_params.get("call_id")
                driver_id = custom_params.get("driver_id", "D03")
                lorry_id = custom_params.get("lorry_id", "L03")
                call_type = custom_params.get("call_type", "STATUS_CHECK")

                welcome_text = f"Hello, driver {driver_id}. This is ATLAS from Fleetos calling regarding Lorry {lorry_id}. Are you on schedule?"
                transcript_lines.append(f"ATLAS: {welcome_text}")
                conversation_history.append({"role": "assistant", "content": welcome_text})

                # Send initial greeting speech token
                await websocket.send_text(json.dumps({
                    "type": "text",
                    "token": welcome_text,
                    "last": True
                }))

            elif msg_type == "prompt":
                driver_speech = msg.get("voicePrompt", "").strip()
                if not driver_speech:
                    continue

                transcript_lines.append(f"Driver {driver_id}: {driver_speech}")
                conversation_history.append({"role": "user", "content": driver_speech})

                async with AsyncSessionLocal() as db:
                    res = await atlas_engine.generate_response(
                        conversation_history=conversation_history,
                        driver_id=driver_id,
                        lorry_id=lorry_id,
                        call_type=call_type,
                        db=db
                    )

                ai_text = res["text"]
                transcript_lines.append(f"ATLAS: {ai_text}")
                conversation_history.append({"role": "assistant", "content": ai_text})

                if res.get("tool_result") and isinstance(res["tool_result"], dict):
                    if res["tool_result"].get("event_id"):
                        last_event_id = res["tool_result"]["event_id"]
                    if res["tool_result"].get("message"):
                        last_outcome_summary = res["tool_result"]["message"]

                # Send AI text back to ConversationRelay
                await websocket.send_text(json.dumps({
                    "type": "text",
                    "token": ai_text,
                    "last": True
                }))

            elif msg_type == "interrupt":
                # Handle driver speech interruption cleanly
                pass

            elif msg_type == "disconnect":
                break

    except WebSocketDisconnect:
        pass
    except Exception as err:
        print(f"Warning: Exception in ConversationRelay WebSocket: {err}")
    finally:
        end_time = datetime.datetime.now(datetime.timezone.utc)
        duration = max(1, int((end_time - start_time).total_seconds()))

        # Complete and update call record
        if call_id:
            rec = voice_service.get_call_record_by_id(call_id)
            if rec:
                rec.status = CallStatus.COMPLETED
                rec.duration_seconds = duration
                rec.ended_at = end_time.isoformat()
                rec.transcript = "\n".join(transcript_lines)
                rec.outcome_summary = last_outcome_summary
                if last_event_id:
                    rec.event_id = last_event_id

                # Save updated call record in database
                async with AsyncSessionLocal() as db:
                    try:
                        from services.api.app.schemas import CallCreate
                        call_create = CallCreate(
                            id=rec.id,
                            provider=rec.provider,
                            driver_id=driver_id,
                            lorry_id=lorry_id,
                            call_type=call_type,
                            status="COMPLETED",
                            event_id=rec.event_id,
                            transcript=rec.transcript,
                            outcome_summary=rec.outcome_summary,
                            duration_seconds=rec.duration_seconds
                        )
                        await crud.create_call(db, call_create)
                    except Exception as db_err:
                        print(f"Warning: Failed updating DB call record on disconnect: {db_err}")
