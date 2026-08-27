"""
Fleetos ATLAS Agent Tool Declarations & Schemas
Module Boundary: services/agent/tool_registry.py
"""

from typing import Dict, Any, List

ATLAS_TOOL_DECLARATIONS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_fleet_status",
            "description": "Retrieves real-time fleet telemetry summary KPI state.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_lorry_status",
            "description": "Retrieves live telemetry, speed, coordinates, and status for a specific lorry (L01-L05).",
            "parameters": {
                "type": "object",
                "properties": {
                    "lorry_id": {"type": "string", "description": "Lorry identifier (e.g. L03)"}
                },
                "required": ["lorry_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_driver_status",
            "description": "Retrieves assigned driver details, phone number, and lorry assignment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "driver_id": {"type": "string", "description": "Driver identifier (e.g. D03)"}
                },
                "required": ["driver_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "report_delay",
            "description": "Records an operational delay for a lorry and generates a DRIVER_DELAY_REPORTED event.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lorry_id": {"type": "string", "description": "Lorry identifier (e.g. L03)"},
                    "delay_minutes": {"type": "integer", "description": "Delay duration in minutes (e.g. 45)"},
                    "reason": {"type": "string", "description": "Reason: LOADING_DELAY, TRAFFIC, BREAKDOWN, WEATHER, OTHER"}
                },
                "required": ["lorry_id", "delay_minutes"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "report_breakdown",
            "description": "Records a vehicle breakdown emergency and generates a DRIVER_BREAKDOWN_REPORTED event.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lorry_id": {"type": "string", "description": "Lorry identifier (e.g. L03)"},
                    "description": {"type": "string", "description": "Breakdown description"}
                },
                "required": ["lorry_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "confirm_delivery",
            "description": "Confirms that a shipment has been delivered safely.",
            "parameters": {
                "type": "object",
                "properties": {
                    "shipment_id": {"type": "string", "description": "Shipment identifier (e.g. S12)"}
                },
                "required": ["shipment_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "explain_assignment",
            "description": "Provides structured VRP optimization explanation for why a shipment was assigned to a vehicle.",
            "parameters": {
                "type": "object",
                "properties": {
                    "shipment_id": {"type": "string", "description": "Shipment identifier (e.g. S12)"}
                },
                "required": ["shipment_id"]
            }
        }
    }
]
