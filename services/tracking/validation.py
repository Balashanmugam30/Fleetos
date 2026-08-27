"""
Fleetos Telemetry Validation Module
Module Boundary: services/tracking/validation.py
"""

import datetime
from typing import Tuple
from services.tracking.models import TrackingPosition

class TelemetryValidationError(ValueError):
    """Exception raised when telemetry data fails validation."""
    pass

def validate_telemetry_position(pos: TrackingPosition) -> TrackingPosition:
    """
    Validates latitude, longitude, speed, heading, and timestamp.
    Normalizes values where appropriate.
    """
    if not pos.vehicle_id or not isinstance(pos.vehicle_id, str):
        raise TelemetryValidationError("vehicle_id must be a non-empty string.")

    if not (-90.0 <= pos.latitude <= 90.0):
        raise TelemetryValidationError(f"Invalid latitude: {pos.latitude}. Must be between -90 and 90.")

    if not (-180.0 <= pos.longitude <= 180.0):
        raise TelemetryValidationError(f"Invalid longitude: {pos.longitude}. Must be between -180 and 180.")

    if pos.speed_kmh < 0.0:
        raise TelemetryValidationError(f"Speed cannot be negative: {pos.speed_kmh}.")

    # Normalize heading to [0, 360)
    pos.heading_degrees = pos.heading_degrees % 360.0
    if pos.heading_degrees < 0.0:
        pos.heading_degrees += 360.0

    # Ensure timezone aware recorded_at
    if pos.recorded_at.tzinfo is None:
        pos.recorded_at = pos.recorded_at.replace(tzinfo=datetime.timezone.utc)

    if pos.received_at.tzinfo is None:
        pos.received_at = pos.received_at.replace(tzinfo=datetime.timezone.utc)

    return pos
