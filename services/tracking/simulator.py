"""
Fleetos Deterministic GPS Telemetry Simulator
Module Boundary: services/tracking/simulator.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

import math
import datetime
from typing import Dict, List, Optional
from services.tracking.models import TrackingPosition
from services.tracking.provider import TrackingProvider

class SimulatedVehicleRoute:
    def __init__(
        self,
        vehicle_id: str,
        waypoints: List[tuple[float, float]],
        speed_kmh: float,
        status_pattern: str = "MOVING"
    ):
        self.vehicle_id = vehicle_id
        self.waypoints = waypoints
        self.target_speed = speed_kmh
        self.status_pattern = status_pattern
        self.current_waypoint_index = 0
        self.progress_ratio = 0.0  # 0.0 to 1.0 between current and next waypoint
        self.lat = waypoints[0][0]
        self.lng = waypoints[0][1]
        self.heading = 90.0
        self.current_speed = 0.0 if status_pattern in ["STOPPED", "IDLE"] else speed_kmh
        self.history: List[TrackingPosition] = []

    def step(self, delta_seconds: float = 5.0) -> TrackingPosition:
        now = datetime.datetime.now(datetime.timezone.utc)
        
        if self.status_pattern in ["STOPPED", "IDLE"]:
            self.current_speed = 0.0
            pos = TrackingPosition(
                vehicle_id=self.vehicle_id,
                latitude=self.lat,
                longitude=self.lng,
                speed_kmh=0.0,
                heading_degrees=self.heading,
                recorded_at=now,
                received_at=now,
                source="SIMULATOR"
            )
            self.history.append(pos)
            if len(self.history) > 200:
                self.history.pop(0)
            return pos

        # Calculate movement step along current segment
        p1 = self.waypoints[self.current_waypoint_index]
        next_idx = (self.current_waypoint_index + 1) % len(self.waypoints)
        p2 = self.waypoints[next_idx]

        # Calculate bearing / heading
        d_lat = p2[0] - p1[0]
        d_lng = p2[1] - p1[1]
        angle = math.atan2(d_lng, d_lat)
        self.heading = (math.degrees(angle) + 360) % 360

        # Increment progress ratio
        # Distance approx per lat/lng degree ~ 111 km
        segment_dist_km = math.sqrt(d_lat**2 + d_lng**2) * 111.0
        if segment_dist_km < 0.001:
            segment_dist_km = 0.001

        step_dist_km = (self.target_speed / 3600.0) * delta_seconds
        step_ratio = step_dist_km / segment_dist_km

        self.progress_ratio += step_ratio

        if self.progress_ratio >= 1.0:
            self.progress_ratio = 0.0
            self.current_waypoint_index = next_idx
            self.lat = p2[0]
            self.lng = p2[1]
        else:
            self.lat = p1[0] + d_lat * self.progress_ratio
            self.lng = p1[1] + d_lng * self.progress_ratio

        self.current_speed = self.target_speed

        pos = TrackingPosition(
            vehicle_id=self.vehicle_id,
            latitude=round(self.lat, 6),
            longitude=round(self.lng, 6),
            speed_kmh=round(self.current_speed, 1),
            heading_degrees=round(self.heading, 1),
            recorded_at=now,
            received_at=now,
            source="SIMULATOR"
        )

        self.history.append(pos)
        if len(self.history) > 200:
            self.history.pop(0)

        return pos

class SimulatorTrackingProvider(TrackingProvider):
    """Deterministic Simulator Provider for Lorries L01-L05."""

    def __init__(self):
        self.is_running = False
        self.update_interval_seconds = 5
        self.routes: Dict[str, SimulatedVehicleRoute] = {
            "L01": SimulatedVehicleRoute(
                vehicle_id="L01",
                waypoints=[(12.9716, 77.5946), (12.7903, 77.8323), (12.5266, 78.2146), (12.9165, 79.1325), (13.0839, 80.2925)],
                speed_kmh=55.0,
                status_pattern="MOVING"
            ),
            "L02": SimulatedVehicleRoute(
                vehicle_id="L02",
                waypoints=[(12.9716, 77.5946), (12.7209, 77.2796), (12.5223, 76.8974), (12.2958, 76.6394)],
                speed_kmh=48.0,
                status_pattern="MOVING"
            ),
            "L03": SimulatedVehicleRoute(
                vehicle_id="L03",
                waypoints=[(13.0839, 80.2925), (12.9667, 79.9500), (12.9165, 79.1325)],
                speed_kmh=60.0,
                status_pattern="MOVING"
            ),
            "L04": SimulatedVehicleRoute(
                vehicle_id="L04",
                waypoints=[(12.9165, 79.1325), (12.9170, 79.1330)],
                speed_kmh=0.0,
                status_pattern="STOPPED"
            ),
            "L05": SimulatedVehicleRoute(
                vehicle_id="L05",
                waypoints=[(12.9165, 79.1325), (12.7903, 77.8323), (12.8399, 77.6770)],
                speed_kmh=52.0,
                status_pattern="MOVING"
            ),
        }
        self.last_update_time: Optional[datetime.datetime] = None

    def start(self) -> None:
        self.is_running = True

    def stop(self) -> None:
        self.is_running = False

    def step_simulation(self) -> List[TrackingPosition]:
        """Steps all vehicles forward deterministically."""
        positions = []
        for vehicle_id, route in self.routes.items():
            pos = route.step(delta_seconds=self.update_interval_seconds)
            positions.append(pos)
        self.last_update_time = datetime.datetime.now(datetime.timezone.utc)
        return positions

    def get_latest_positions(self) -> List[TrackingPosition]:
        if self.is_running:
            return self.step_simulation()
        
        # If stopped, return latest calculated positions without advancing
        results = []
        now = datetime.datetime.now(datetime.timezone.utc)
        for route in self.routes.values():
            if route.history:
                results.append(route.history[-1])
            else:
                results.append(TrackingPosition(
                    vehicle_id=route.vehicle_id,
                    latitude=route.lat,
                    longitude=route.lng,
                    speed_kmh=route.current_speed,
                    heading_degrees=route.heading,
                    recorded_at=now,
                    received_at=now,
                    source="SIMULATOR"
                ))
        return results

    def get_vehicle_position(self, vehicle_id: str) -> Optional[TrackingPosition]:
        route = self.routes.get(vehicle_id)
        if not route:
            return None
        if route.history:
            return route.history[-1]
        now = datetime.datetime.now(datetime.timezone.utc)
        return TrackingPosition(
            vehicle_id=vehicle_id,
            latitude=route.lat,
            longitude=route.lng,
            speed_kmh=route.current_speed,
            heading_degrees=route.heading,
            recorded_at=now,
            received_at=now,
            source="SIMULATOR"
        )

    def get_recent_positions(self, vehicle_id: str, limit: int = 50) -> List[TrackingPosition]:
        route = self.routes.get(vehicle_id)
        if not route:
            return []
        return route.history[-limit:]
