"""
Fleetos Offline Demo Voice Simulator Provider
Module Boundary: services/voice/simulator.py
"""

import uuid
import datetime
from typing import Dict, Any, Optional
from services.voice.provider import VoiceProvider
from services.voice.models import OutboundCallRequest, CallRecord, CallStatus, CallType
from services.agent.tool_executor import tool_executor

class DemoVoiceProvider(VoiceProvider):
    """Offline Demo Voice Simulator Adapter."""

    def __init__(self):
        self._simulated_calls: Dict[str, CallRecord] = {}

    async def initiate_outbound_call(
        self,
        request: OutboundCallRequest,
        context: Dict[str, Any],
        db: Optional[Any] = None
    ) -> CallRecord:
        call_id = f"demo_call_{uuid.uuid4().hex[:8]}"
        driver_id = request.driver_id.upper().strip()
        lorry_id = str(context.get("lorry_id") or (f"L0{driver_id[-1]}" if driver_id[-1].isdigit() else "L03")).upper().strip()

        now = datetime.datetime.now(datetime.timezone.utc)
        now_str = now.isoformat()

        call_type = request.call_type
        event_id: Optional[str] = None

        if call_type == CallType.STATUS_CHECK:
            duration = 18
            ended_at = (now + datetime.timedelta(seconds=duration)).isoformat()
            transcript = (
                f"ATLAS: Hello, driver {driver_id}. Are you on schedule for Lorry {lorry_id}?\n"
                f"Driver {driver_id}: Yes, I'm on schedule.\n"
                f"ATLAS: Thanks. Fleetos has recorded your status."
            )
            outcome_summary = f"Routine status check completed for Lorry {lorry_id}."
            status = CallStatus.COMPLETED

        elif call_type == CallType.DELAY_REPORT:
            duration = 45
            ended_at = (now + datetime.timedelta(seconds=duration)).isoformat()
            transcript = (
                f"ATLAS: Are you still on schedule for Lorry {lorry_id}?\n"
                f"Driver {driver_id}: I'm 45 minutes late because loading was delayed.\n"
                f"ATLAS: Just to confirm, you're reporting a 45-minute loading delay for {lorry_id}?\n"
                f"Driver {driver_id}: Yes."
            )
            outcome_summary = f"45-minute loading delay reported for Lorry {lorry_id}."

            # Execute backend tool report_delay
            tool_args = {"lorry_id": lorry_id, "delay_minutes": 45, "reason": "LOADING_DELAY"}
            tool_result = await tool_executor.execute_tool("report_delay", tool_args, db=db)
            if isinstance(tool_result, dict) and tool_result.get("success"):
                event_id = tool_result.get("event_id")

            status = CallStatus.COMPLETED

        elif call_type == CallType.BREAKDOWN_REPORT:
            duration = 60
            ended_at = (now + datetime.timedelta(seconds=duration)).isoformat()
            transcript = (
                f"ATLAS: Emergency check for Lorry {lorry_id}. Driver {driver_id}, please state status.\n"
                f"Driver {driver_id}: Vehicle mechanical breakdown on highway.\n"
                f"ATLAS: Dispatching roadside emergency assistance for Lorry {lorry_id} immediately."
            )
            outcome_summary = f"Emergency vehicle breakdown reported for Lorry {lorry_id}."

            # Execute backend tool report_breakdown
            tool_args = {"lorry_id": lorry_id, "description": f"Emergency breakdown reported by driver {driver_id}."}
            tool_result = await tool_executor.execute_tool("report_breakdown", tool_args, db=db)
            if isinstance(tool_result, dict) and tool_result.get("success"):
                event_id = tool_result.get("event_id")

            status = CallStatus.COMPLETED

        elif call_type == CallType.DELIVERY_CONFIRMATION:
            duration = 30
            ended_at = (now + datetime.timedelta(seconds=duration)).isoformat()
            shipment_id = context.get("shipment_id") or "S12"
            transcript = (
                f"ATLAS: Driver {driver_id}, please confirm delivery for shipment {shipment_id} on Lorry {lorry_id}.\n"
                f"Driver {driver_id}: Shipment {shipment_id} has been delivered safely.\n"
                f"ATLAS: Delivery recorded in Fleetos ledger."
            )
            outcome_summary = f"Delivery confirmed for Shipment {shipment_id} on Lorry {lorry_id}."

            # Execute backend tool confirm_delivery
            tool_args = {"shipment_id": shipment_id}
            tool_result = await tool_executor.execute_tool("confirm_delivery", tool_args, db=db)
            if isinstance(tool_result, dict) and tool_result.get("success"):
                event_id = tool_result.get("event_id")

            status = CallStatus.COMPLETED

        else:  # ASSIGNMENT_CONFIRMATION or generic fallback
            duration = 20
            ended_at = (now + datetime.timedelta(seconds=duration)).isoformat()
            transcript = (
                f"ATLAS: Driver {driver_id}, confirming route assignment for Lorry {lorry_id}.\n"
                f"Driver {driver_id}: Confirmed, route received.\n"
                f"ATLAS: Assignment verified."
            )
            outcome_summary = f"Route assignment confirmed for Driver {driver_id} on Lorry {lorry_id}."
            status = CallStatus.COMPLETED

        record = CallRecord(
            id=call_id,
            call_id=call_id,
            driver_id=driver_id,
            lorry_id=lorry_id,
            call_type=call_type,
            direction="OUTBOUND",
            status=status,
            provider="DEMO",
            external_call_id=f"ext_{call_id}",
            started_at=now_str,
            ended_at=ended_at,
            duration_seconds=duration,
            transcript=transcript,
            outcome_summary=outcome_summary,
            event_id=event_id,
            created_at=now_str,
            updated_at=ended_at
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
            "provider": "demo",
            "mode": "DEMO",
            "configured": True,
            "provider_reachable": True,
            "real_pstn_verified": False
        }
