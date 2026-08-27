"""
Fleetos Tracking Service Master Orchestrator
Module Boundary: services/tracking/service.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

import uuid
import datetime
from typing import Dict, List, Optional
from services.tracking.models import (
    TrackingPosition,
    VehicleTrackingState,
    TrackingStatus,
    TrackingFreshness,
)
from services.tracking.validation import validate_telemetry_position
from services.tracking.provider import TrackingProvider
from services.tracking.simulator import SimulatorTrackingProvider

class TrackingService:
    """Master Tracking Service managing telemetry ingest, freshness, and status."""

    def __init__(self, provider: Optional[TrackingProvider] = None):
        self.provider = provider or SimulatorTrackingProvider()
        self.states: Dict[str, VehicleTrackingState] = {}
        self.positions_history: Dict[str, List[TrackingPosition]] = {}
        self.events_log: List[Dict] = []
        self.live_threshold_seconds = 30.0
        self.recent_threshold_seconds = 120.0
        self.stale_threshold_seconds = 300.0
        self.movement_threshold_kmh = 2.0

    def calculate_freshness(self, telemetry_age_seconds: float) -> TrackingFreshness:
        if telemetry_age_seconds <= self.live_threshold_seconds:
            return TrackingFreshness.LIVE
        elif telemetry_age_seconds <= self.recent_threshold_seconds:
            return TrackingFreshness.RECENT
        elif telemetry_age_seconds <= self.stale_threshold_seconds:
            return TrackingFreshness.STALE
        else:
            return TrackingFreshness.OFFLINE

    def calculate_status(self, speed_kmh: float, freshness: TrackingFreshness) -> TrackingStatus:
        if freshness == TrackingFreshness.OFFLINE:
            return TrackingStatus.OFFLINE
        if speed_kmh > self.movement_threshold_kmh:
            return TrackingStatus.MOVING
        else:
            return TrackingStatus.STOPPED

    def ingest_position(self, pos: TrackingPosition) -> VehicleTrackingState:
        # Validate telemetry payload
        valid_pos = validate_telemetry_position(pos)
        vehicle_id = valid_pos.vehicle_id

        now = datetime.datetime.now(datetime.timezone.utc)
        rec_at = valid_pos.recorded_at
        if rec_at.tzinfo is None:
            rec_at = rec_at.replace(tzinfo=datetime.timezone.utc)

        age_seconds = max(0.0, (now - rec_at).total_seconds())
        freshness = self.calculate_freshness(age_seconds)
        status = self.calculate_status(valid_pos.speed_kmh, freshness)

        previous_state = self.states.get(vehicle_id)

        new_state = VehicleTrackingState(
            vehicle_id=vehicle_id,
            driver_id=f"D0{vehicle_id[-1]}" if vehicle_id.startswith("L0") else None,
            latitude=valid_pos.latitude,
            longitude=valid_pos.longitude,
            speed_kmh=valid_pos.speed_kmh,
            heading_degrees=valid_pos.heading_degrees,
            status=status,
            freshness=freshness,
            last_update_at=rec_at,
            telemetry_age_seconds=round(age_seconds, 1),
            source=valid_pos.source,
            active_route_id=f"R-{vehicle_id}"
        )

        self.states[vehicle_id] = new_state

        if vehicle_id not in self.positions_history:
            self.positions_history[vehicle_id] = []
        self.positions_history[vehicle_id].append(valid_pos)
        if len(self.positions_history[vehicle_id]) > 200:
            self.positions_history[vehicle_id].pop(0)

        # Detect Lifecycle State Transitions & Deduplicate Events
        if previous_state:
            # Movement transition
            if previous_state.status != TrackingStatus.MOVING and status == TrackingStatus.MOVING:
                self._record_event(
                    event_type="VEHICLE_STARTED_MOVING",
                    vehicle_id=vehicle_id,
                    payload={"speed_kmh": valid_pos.speed_kmh, "latitude": valid_pos.latitude, "longitude": valid_pos.longitude}
                )
            elif previous_state.status == TrackingStatus.MOVING and status == TrackingStatus.STOPPED:
                self._record_event(
                    event_type="VEHICLE_STOPPED",
                    vehicle_id=vehicle_id,
                    payload={"latitude": valid_pos.latitude, "longitude": valid_pos.longitude}
                )

            # Freshness transitions
            if previous_state.freshness != TrackingFreshness.STALE and freshness == TrackingFreshness.STALE:
                self._record_event(
                    event_type="VEHICLE_TRACKING_STALE",
                    vehicle_id=vehicle_id,
                    severity="WARNING",
                    payload={"telemetry_age_seconds": age_seconds}
                )
            elif previous_state.freshness in [TrackingFreshness.STALE, TrackingFreshness.OFFLINE] and freshness == TrackingFreshness.LIVE:
                self._record_event(
                    event_type="VEHICLE_TRACKING_RECOVERED",
                    vehicle_id=vehicle_id,
                    payload={"telemetry_age_seconds": age_seconds}
                )
        else:
            # Initial ingestion event
            if status == TrackingStatus.MOVING:
                self._record_event(
                    event_type="VEHICLE_STARTED_MOVING",
                    vehicle_id=vehicle_id,
                    payload={"speed_kmh": valid_pos.speed_kmh}
                )

        return new_state

    def _record_event(self, event_type: str, vehicle_id: str, payload: dict, severity: str = "INFO"):
        event = {
            "id": f"EVT-{uuid.uuid4().hex[:8].upper()}",
            "event_type": event_type,
            "source": "TRACKING_ENGINE",
            "severity": severity,
            "lorry_id": vehicle_id,
            "shipment_id": None,
            "payload_json": payload,
            "resolution_status": "PENDING",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self.events_log.insert(0, event)
        if len(self.events_log) > 100:
            self.events_log.pop()

    def get_latest_state(self, vehicle_id: str) -> Optional[VehicleTrackingState]:
        state = self.states.get(vehicle_id)
        if state:
            now = datetime.datetime.now(datetime.timezone.utc)
            age = max(0.0, (now - state.last_update_at).total_seconds())
            state.telemetry_age_seconds = round(age, 1)
            state.freshness = self.calculate_freshness(age)
            state.status = self.calculate_status(state.speed_kmh, state.freshness)
        return state

    def get_all_latest_states(self) -> List[VehicleTrackingState]:
        # Pull from provider if simulator or active provider is running
        latest_positions = self.provider.get_latest_positions()
        for pos in latest_positions:
            self.ingest_position(pos)
        return list(self.states.values())

    def get_history(self, vehicle_id: str, limit: int = 50) -> List[TrackingPosition]:
        return self.positions_history.get(vehicle_id, [])[-limit:]
