"""
Fleetos Voice Webhook Receiver & Normalizer
Module Boundary: services/voice/webhooks.py
"""

import json
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from services.voice.models import CallStatus
from services.agent.tool_executor import tool_executor

_EXECUTED_TOOL_CALLS: Dict[str, Dict[str, Any]] = {}

class VoiceWebhookNormalizer:
    """Normalizes Vapi webhook callbacks into internal Fleetos events and executes tool calls."""

    async def process_vapi_webhook(self, payload: Dict[str, Any], db: Optional[AsyncSession] = None) -> Dict[str, Any]:
        message_type = payload.get("message", {}).get("type", "")
        call_obj = payload.get("message", {}).get("call", {})
        external_call_id = call_obj.get("id")

        if message_type == "tool-calls":
            tool_calls = payload.get("message", {}).get("toolCalls", [])
            results = []
            for tool_call in tool_calls:
                tool_call_id = tool_call.get("id")
                call_func = tool_call.get("function", {})
                func_name = call_func.get("name", "")
                func_args = call_func.get("arguments", {})
                if isinstance(func_args, str):
                    try:
                        func_args = json.loads(func_args)
                    except Exception:
                        func_args = {}

                # Idempotency Check: Return cached result if same toolCallId is replayed
                if tool_call_id and tool_call_id in _EXECUTED_TOOL_CALLS:
                    cached_res = _EXECUTED_TOOL_CALLS[tool_call_id]
                    results.append({
                        "toolCallId": tool_call_id,
                        "result": json.dumps(cached_res)
                    })
                    continue

                if tool_call_id and isinstance(func_args, dict):
                    func_args["tool_call_id"] = tool_call_id

                tool_result = await tool_executor.execute_tool(func_name, func_args, db)
                if tool_call_id:
                    _EXECUTED_TOOL_CALLS[tool_call_id] = tool_result

                results.append({
                    "toolCallId": tool_call_id,
                    "result": json.dumps(tool_result)
                })

            return {"results": results}

        elif message_type == "status-update":
            status_str = payload.get("message", {}).get("status", "").lower()
            new_status = CallStatus.COMPLETED
            if status_str == "queued":
                new_status = CallStatus.QUEUED
            elif status_str == "ringing":
                new_status = CallStatus.RINGING
            elif status_str == "in-progress":
                new_status = CallStatus.IN_PROGRESS
            elif status_str == "ended":
                new_status = CallStatus.COMPLETED

            return {
                "success": True,
                "external_call_id": external_call_id,
                "status": new_status
            }

        return {"success": True, "message": "Unhandled webhook message type acknowledged safely."}

voice_webhook_normalizer = VoiceWebhookNormalizer()
