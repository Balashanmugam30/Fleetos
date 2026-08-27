"""
Fleetos Backend Tracking Provider Boundary
Module Boundary: services/tracking/provider.py
"""

from typing import List, Optional
from services.tracking.models import TrackingPosition

class TrackingProvider:
    """Abstract Vehicle Telemetry Tracking Provider Interface."""
    
    def get_latest_positions(self) -> List[TrackingPosition]:
        raise NotImplementedError()

    def get_vehicle_position(self, vehicle_id: str) -> Optional[TrackingPosition]:
        raise NotImplementedError()

    def get_recent_positions(self, vehicle_id: str, limit: int = 50) -> List[TrackingPosition]:
        raise NotImplementedError()

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass
