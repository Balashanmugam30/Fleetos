"""
Fleetos Backend Tracking Provider Boundary
Module Boundary: services/tracking
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class TelemetryPosition(BaseModel):
    lorry_id: str
    latitude: float
    longitude: float
    timestamp: str
    speed_km_h: float = 0.0
    heading_degrees: float = 0.0
    status: str = "EN_ROUTE"

class TrackingProvider:
    """Abstract Vehicle Telemetry Tracking Provider Interface."""
    def get_position(self, lorry_id: str) -> Optional[TelemetryPosition]:
        raise NotImplementedError()

    def get_all_positions(self) -> List[TelemetryPosition]:
        raise NotImplementedError()

class SimulatorTrackingProvider(TrackingProvider):
    """Backend-Driven GPS Simulation Provider for Demos."""
    def get_position(self, lorry_id: str) -> Optional[TelemetryPosition]:
        return TelemetryPosition(
            lorry_id=lorry_id,
            latitude=12.9716,
            longitude=77.5946,
            timestamp="2026-08-27T17:45:00Z",
            speed_km_h=55.4,
            heading_degrees=90.0,
            status="EN_ROUTE"
        )

    def get_all_positions(self) -> List[TelemetryPosition]:
        return [self.get_position("L01")]
