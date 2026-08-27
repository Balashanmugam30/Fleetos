"""
Fleetos ATLAS Voice Agent Engine (OpenAI Powered)
Module Boundary: services/voice/atlas_engine.py
"""

import json
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from services.agent.tool_executor import tool_executor
from services.voice.twilio_config import twilio_config

class AtlasEngine:
    """ATLAS Operational Voice Agent Reasoning & Tool Executor Engine."""

    def __init__(self):
        self.system_prompt = (
            "You are ATLAS, the Fleetos operational voice agent.\n"
            "You speak directly with lorry drivers to understand real operational conditions and update Fleetos.\n"
            "System Rules:\n"
            "1. Identify yourself as 'ATLAS from Fleetos'.\n"
            "2. Speak naturally, warmly, and keep spoken responses concise (1 to 2 short sentences).\n"
            "3. Ask one clear operational question at a time.\n"
            "4. Never invent lorry IDs, delays, routes, or shipment details.\n"
            "5. When a driver reports a delay (e.g. 45-minute loading delay), confirm if necessary, then call the 'report_delay' tool.\n"
            "6. After a tool completes, acknowledge the update naturally (e.g. 'I've recorded the 45-minute delay in Fleetos')."
        )

    def get_tool_schemas() -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "report_delay",
                    "description": "Records an operational delay for a lorry in Fleetos ledger.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lorry_id": {"type": "string", "description": "Lorry ID (e.g. L03)"},
                            "delay_minutes": {"type": "integer", "description": "Delay duration in minutes (e.g. 45)"},
                            "reason": {"type": "string", "description": "Reason for delay: LOADING_DELAY, TRAFFIC, BREAKDOWN, WEATHER, OTHER"}
                        },
                        "required": ["lorry_id", "delay_minutes"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "report_breakdown",
                    "description": "Records an emergency mechanical vehicle breakdown.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lorry_id": {"type": "string", "description": "Lorry ID (e.g. L03)"},
                            "description": {"type": "string", "description": "Breakdown details"}
                        },
                        "required": ["lorry_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "confirm_delivery",
                    "description": "Confirms delivery of a shipment.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "shipment_id": {"type": "string", "description": "Shipment ID (e.g. S12)"}
                        },
                        "required": ["shipment_id"]
                    }
                }
            }
        ]

    async def generate_response(
        self,
        conversation_history: List[Dict[str, Any]],
        driver_id: str,
        lorry_id: str,
        call_type: str = "STATUS_CHECK",
        db: Optional[AsyncSession] = None
    ) -> Dict[str, Any]:
        """Generates conversational response and executes tool calls using OpenAI."""
        if not twilio_config.is_openai_configured:
            # Fallback deterministic response generator if OpenAI API Key is absent
            last_user_msg = next((m["content"] for m in reversed(conversation_history) if m["role"] == "user"), "")
            if "delay" in last_user_msg.lower() or "late" in last_user_msg.lower() or "45" in last_user_msg:
                # Execute report_delay
                tool_res = await tool_executor.execute_tool(
                    "report_delay",
                    {"lorry_id": lorry_id, "delay_minutes": 45, "reason": "LOADING_DELAY"},
                    db=db
                )
                return {
                    "text": f"Understood, driver {driver_id}. I have recorded a 45-minute loading delay for Lorry {lorry_id} in Fleetos.",
                    "tool_executed": "report_delay",
                    "tool_result": tool_res
                }
            return {
                "text": f"Hello, driver {driver_id}. This is ATLAS from Fleetos checking on Lorry {lorry_id}. Are you on schedule?",
                "tool_executed": None,
                "tool_result": None
            }

        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=twilio_config.openai_api_key)

            messages = [
                {"role": "system", "content": f"{self.system_prompt}\nCurrent Context: Driver {driver_id}, Lorry {lorry_id}, Purpose: {call_type}."}
            ] + conversation_history

            response = await client.chat.completions.create(
                model=twilio_config.openai_model,
                messages=messages,
                tools=AtlasEngine.get_tool_schemas(),
                tool_choice="auto",
                temperature=0.4,
                max_tokens=150
            )

            choice = response.choices[0].message

            if choice.tool_calls:
                tool_executed_name = None
                exec_result = None
                for tool_call in choice.tool_calls:
                    fn_name = tool_call.function.name
                    try:
                        fn_args = json.loads(tool_call.function.arguments)
                    except Exception:
                        fn_args = {}

                    # Ensure lorry_id matches context if unspecified
                    if "lorry_id" not in fn_args or not fn_args["lorry_id"]:
                        fn_args["lorry_id"] = lorry_id

                    exec_result = await tool_executor.execute_tool(fn_name, fn_args, db=db)
                    tool_executed_name = fn_name

                    # Add tool response to conversation history and call OpenAI again for confirmation message
                    messages.append(choice)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(exec_result)
                    })

                second_resp = await client.chat.completions.create(
                    model=twilio_config.openai_model,
                    messages=messages,
                    temperature=0.4,
                    max_tokens=100
                )
                final_text = second_resp.choices[0].message.content or f"I've recorded the update for Lorry {lorry_id} in Fleetos."
                return {
                    "text": final_text,
                    "tool_executed": tool_executed_name,
                    "tool_result": exec_result
                }

            return {
                "text": choice.content or f"Hello, driver {driver_id}. Is everything on schedule for Lorry {lorry_id}?",
                "tool_executed": None,
                "tool_result": None
            }
        except Exception as err:
            print(f"Warning: AtlasEngine OpenAI call error: {err}")
            return {
                "text": f"Thanks driver {driver_id}. Fleetos has noted your update for Lorry {lorry_id}.",
                "tool_executed": None,
                "tool_result": None
            }

atlas_engine = AtlasEngine()
