"""
Fleetos Distance & Travel Time Matrix Pre-Computation Module
Module Boundary: services/optimizer/matrix.py
"""

import math
from typing import List, Tuple, Dict
from pydantic import BaseModel

EARTH_RADIUS_METERS = 6371000.0
ROAD_TORTUOSITY_FACTOR = 1.25  # Road distance multiplier over straight-line Haversine

class LocationNode(BaseModel):
    id: str
    latitude: float
    longitude: float

class TravelMatrix(BaseModel):
    node_ids: List[str]
    distances_meters: Dict[Tuple[int, int], float]
    durations_seconds: Dict[Tuple[int, int], int]
    provider_name: str = "ESTIMATED_HAVERSINE"

class TravelTimeProvider:
    """Abstract Travel Matrix Provider Interface."""
    def compute_matrix(self, nodes: List[LocationNode], speed_km_h: float = 50.0) -> TravelMatrix:
        raise NotImplementedError()

def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate Geodesic Haversine distance in meters between two lat/lng coordinates."""
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return EARTH_RADIUS_METERS * c

class HaversineTravelTimeProvider(TravelTimeProvider):
    """Deterministic Haversine + Road Tortuosity Matrix Provider."""
    def compute_matrix(self, nodes: List[LocationNode], speed_km_h: float = 50.0) -> TravelMatrix:
        n = len(nodes)
        distances: Dict[Tuple[int, int], float] = {}
        durations: Dict[Tuple[int, int], int] = {}
        speed_m_s = (speed_km_h * 1000.0) / 3600.0

        node_ids = [node.id for node in nodes]

        for i in range(n):
            for j in range(n):
                if i == j:
                    distances[(i, j)] = 0.0
                    durations[(i, j)] = 0
                else:
                    direct_m = haversine_distance_meters(
                        nodes[i].latitude, nodes[i].longitude,
                        nodes[j].latitude, nodes[j].longitude
                    )
                    road_m = direct_m * ROAD_TORTUOSITY_FACTOR
                    distances[(i, j)] = road_m
                    durations[(i, j)] = int(road_m / speed_m_s) if speed_m_s > 0 else 0

        return TravelMatrix(
            node_ids=node_ids,
            distances_meters=distances,
            durations_seconds=durations,
            provider_name="ESTIMATED_HAVERSINE"
        )
