"""
Fleetos Operational Event Taxonomy & Structure
Module Boundary: services/events/taxonomy.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import datetime

class EventType(str, Enum):
    # Tracking Lifecycle Events
    VEHICLE_LOCATION_UPDATED = "VEHICLE_LOCATION_UPDATED"
    VEHICLE_STARTED_MOVING = "VEHICLE_STARTED_MOVING"
    VEHICLE_STOPPED = "VEHICLE_STOPPED"
    VEHICLE_IDLE = "VEHICLE_IDLE"
    VEHICLE_TRACKING_STALE = "VEHICLE_TRACKING_STALE"
    VEHICLE_TRACKING_OFFLINE = "VEHICLE_TRACKING_OFFLINE"
    VEHICLE_TRACKING_RECOVERED = "VEHICLE_TRACKING_RECOVERED"

    # Driver & Voice Agent Events
    DRIVER_DELAY_REPORTED = "DRIVER_DELAY_REPORTED"
    DRIVER_BREAKDOWN_REPORTED = "DRIVER_BREAKDOWN_REPORTED"
    DRIVER_UNAVAILABLE = "DRIVER_UNAVAILABLE"
    DRIVER_AVAILABLE = "DRIVER_AVAILABLE"
    LOADING_DELAY = "LOADING_DELAY"

    # Shipment & Routing Events
    SHIPMENT_CREATED = "SHIPMENT_CREATED"
    SHIPMENT_CANCELLED = "SHIPMENT_CANCELLED"
    SHIPMENT_PRIORITY_CHANGED = "SHIPMENT_PRIORITY_CHANGED"
    DELIVERY_DEADLINE_RISK = "DELIVERY_DEADLINE_RISK"
    SHIPMENT_REASSIGNED = "SHIPMENT_REASSIGNED"
    ROUTE_REOPTIMIZED = "ROUTE_REOPTIMIZED"
    DELIVERY_CONFIRMED = "DELIVERY_CONFIRMED"

    # AR & Voice Events
    AR_LORRY_IDENTIFIED = "AR_LORRY_IDENTIFIED"
    AR_SHIPMENT_IDENTIFIED = "AR_SHIPMENT_IDENTIFIED"
    CALL_STARTED = "CALL_STARTED"
    CALL_COMPLETED = "CALL_COMPLETED"
    CALL_FAILED = "CALL_FAILED"

class OperationalEventPayload(BaseModel):
    event_id: str
    event_type: EventType
    source: str  # 'TRACKING_ENGINE' | 'ATLAS_VOICE' | 'DISPATCHER_WEB' | 'AR_VIEW' | 'SYSTEM_MONITOR'
    severity: str = "INFO"  # 'INFO' | 'WARNING' | 'CRITICAL'
    lorry_id: Optional[str] = None
    shipment_id: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    payload: Dict[str, Any] = {}
    resolution_status: str = "PENDING"
