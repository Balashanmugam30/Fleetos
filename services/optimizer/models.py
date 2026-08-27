"""
Fleetos Optimization Engine Data Models & Schemas
Module Boundary: services/optimizer/models.py
"""

import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

def ensure_utc(dt: datetime.datetime) -> datetime.datetime:
    """Ensure datetime is timezone-aware UTC."""
    if dt is None:
        return datetime.datetime.now(datetime.timezone.utc)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc)

class ObjectiveConfig(BaseModel):
    fuel_price_per_liter: float = 1.05
    driver_cost_per_hour: float = 18.0
    cost_per_km: float = 0.45
    fixed_vehicle_cost: float = 50.0
    deadline_penalty: float = 5000.0
    priority_penalties: Dict[str, float] = Field(
        default_factory=lambda: {
            "URGENT": 10000.0,
            "HIGH": 5000.0,
            "NORMAL": 1000.0,
            "LOW": 200.0
        }
    )
    solve_timeout_seconds: int = 10
    time_limit_seconds: int = 10
    default_speed_km_h: float = 50.0
    service_time_pickup_seconds: int = 900
    service_time_delivery_seconds: int = 900

class VehicleInput(BaseModel):
    id: str
    registration_number: str
    start_latitude: float
    start_longitude: float
    max_weight_kg: float
    max_volume_m3: float
    fuel_efficiency_km_l: float
    driver_available: bool = True
    status: str = "AVAILABLE"

class ShipmentInput(BaseModel):
    id: str
    weight_kg: float
    volume_m3: float
    pickup_address: str
    pickup_latitude: float
    pickup_longitude: float
    destination_address: str
    destination_latitude: float
    destination_longitude: float
    delivery_deadline: datetime.datetime
    priority: str = "NORMAL"

class OptimizationInput(BaseModel):
    vehicles: List[VehicleInput]
    shipments: List[ShipmentInput]
    start_time: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    config: ObjectiveConfig = Field(default_factory=ObjectiveConfig)
    mode: str = "BASELINE"

class StopResult(BaseModel):
    sequence: int
    type: str
    shipment_id: Optional[str] = None
    latitude: float
    longitude: float
    address: str
    estimated_arrival: datetime.datetime
    deadline: Optional[datetime.datetime] = None
    deadline_slack_minutes: Optional[float] = None
    deadline_status: str = "SAFE"

class RouteResult(BaseModel):
    lorry_id: str
    driver_id: Optional[str] = None
    vehicle_registration: str
    stops: List[StopResult]
    distance_meters: float
    estimated_duration_seconds: int
    fuel_estimate_liters: float
    fuel_cost: float
    driver_cost: float
    fixed_cost: float
    total_cost: float
    peak_weight_kg: float
    peak_volume_m3: float
    weight_utilization_percent: float
    volume_utilization_percent: float
    deadline_risk: str = "NONE"

class AssignmentResult(BaseModel):
    shipment_id: str
    lorry_id: str
    sequence: int
    pickup_stop_sequence: int
    delivery_stop_sequence: int
    estimated_delivery_time: datetime.datetime
    deadline: datetime.datetime
    assignment_reason: str
    explanation: Dict[str, Any] = Field(default_factory=dict)

class UnassignedReason(BaseModel):
    shipment_id: str
    assigned: bool = False
    primary_reason_code: str
    reason_description: str
    contributing_constraints: List[str] = Field(default_factory=list)

class OptimizationMetrics(BaseModel):
    total_cost: float
    total_distance_meters: float
    total_fuel_liters: float
    total_shipments_count: int
    assigned_count: int
    unassigned_count: int
    deadline_violations_count: int
    vehicles_used_count: int
    solve_duration_ms: float

class OptimizationResult(BaseModel):
    run_id: str
    status: str
    trigger_reason: str
    routing_provider: str = "ESTIMATED_HAVERSINE"
    metrics: OptimizationMetrics
    assignments: List[AssignmentResult]
    routes: List[RouteResult]
    unassigned_shipments: List[UnassignedReason]
    explanations: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
