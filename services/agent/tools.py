"""
Fleetos ATLAS Agent Tool Registry Definitions
Module Boundary: services/agent
"""

from typing import Dict, Any, List
from pydantic import BaseModel

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
    requires_confirmation: bool = False
    is_mutation: bool = False

ATLAS_TOOL_REGISTRY: List[ToolDefinition] = [
    ToolDefinition(
        name="get_fleet_status",
        description="Retrieve current active fleet summary statistics.",
        parameters={"type": "object", "properties": {}},
        is_mutation=False
    ),
    ToolDefinition(
        name="get_lorry_status",
        description="Fetch current operational telemetry for a specific lorry.",
        parameters={"type": "object", "properties": {"lorry_id": {"type": "string"}}, "required": ["lorry_id"]},
        is_mutation=False
    ),
    ToolDefinition(
        name="report_delay",
        description="Report a driver delay or loading delay for a lorry.",
        parameters={
            "type": "object",
            "properties": {
                "lorry_id": {"type": "string"},
                "delay_minutes": {"type": "integer"},
                "reason": {"type": "string"}
            },
            "required": ["lorry_id", "delay_minutes"]
        },
        requires_confirmation=False,
        is_mutation=True
    ),
    ToolDefinition(
        name="report_breakdown",
        description="Report a vehicle breakdown event.",
        parameters={
            "type": "object",
            "properties": {
                "lorry_id": {"type": "string"},
                "location": {"type": "string"},
                "severity": {"type": "string", "enum": ["MINOR", "CRITICAL"]}
            },
            "required": ["lorry_id", "location"]
        },
        requires_confirmation=True,
        is_mutation=True
    ),
    ToolDefinition(
        name="reoptimize_fleet",
        description="Trigger OR-Tools VRP re-optimization algorithm.",
        parameters={
            "type": "object",
            "properties": {"trigger": {"type": "string"}},
            "required": ["trigger"]
        },
        is_mutation=True
    ),
    ToolDefinition(
        name="initiate_driver_call",
        description="Trigger an outbound Vapi/Twilio PSTN phone call to a driver.",
        parameters={
            "type": "object",
            "properties": {
                "driver_id": {"type": "string"},
                "phone_number": {"type": "string"},
                "reason": {"type": "string"}
            },
            "required": ["driver_id", "phone_number"]
        },
        requires_confirmation=True,
        is_mutation=True
    )
]
