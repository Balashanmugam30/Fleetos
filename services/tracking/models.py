"""
Fleetos Tracking Domain Models
Module Boundary: services/tracking/models.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

def utcnow() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

class TrackingStatus(str, Enum):
    MOVING = "MOVING"
    STOPPED = "STOPPED"
    IDLE = "IDLE"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"

class TrackingFreshness(str, Enum):
    LIVE = "LIVE"          # 0 - 30 seconds
    RECENT = "RECENT"      # 31 - 120 seconds
    STALE = "STALE"        # 121 - 300 seconds
    OFFLINE = "OFFLINE"    # > 300 seconds

class TrackingPosition(BaseModel):
    vehicle_id: str = Field(..., description="Lorry/Vehicle unique identifier")
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    speed_kmh: float = Field(default=0.0, ge=0.0)
    heading_degrees: float = Field(default=0.0, ge=0.0, lt=360.0)
    recorded_at: datetime.datetime = Field(default_factory=utcnow)
    received_at: datetime.datetime = Field(default_factory=utcnow)
    source: str = Field(default="SIMULATOR")
    accuracy_meters: Optional[float] = Field(default=5.0)

class VehicleTrackingState(BaseModel):
    vehicle_id: str
    driver_id: Optional[str] = None
    latitude: float
    longitude: float
    speed_kmh: float = 0.0
    heading_degrees: float = 0.0
    status: TrackingStatus = TrackingStatus.UNKNOWN
    freshness: TrackingFreshness = TrackingFreshness.OFFLINE
    last_update_at: datetime.datetime
    telemetry_age_seconds: float = 0.0
    source: str = "SIMULATOR"
    active_route_id: Optional[str] = None
