"""
Fleetos Pydantic API Schemas & Server-Side Validation Rules
Module Boundary: services/api/app/schemas.py
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict
import datetime

# --- Health & Version Schemas ---
class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "fleetos-api"
    version: str = "0.2.0"
    environment: str = "development"

class DBHealthResponse(BaseModel):
    status: str = "ok"
    database: str = "connected"
    engine: str
    environment: str

class VersionResponse(BaseModel):
    name: str = "Fleetos Agentic Multimodal Fleet Intelligence Platform"
    version: str = "0.2.0"
    core_loop: str = "SEE → HEAR → THINK → OPTIMIZE → ACT → UPDATE"
    voice_agent: str = "ATLAS"
    optimization_solver: str = "Google OR-Tools Routing Solver / RoutingModel"

class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)

class ErrorResponse(BaseModel):
    error: ErrorDetail

# --- Driver Schemas ---
class DriverBase(BaseModel):
    name: str
    phone_number: str = Field(..., description="E.164 phone number format e.g. +919876510001")
    availability_status: str = "AVAILABLE"
    current_lorry_id: Optional[str] = None

class DriverCreate(DriverBase):
    id: str

class DriverUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    availability_status: Optional[str] = None
    current_lorry_id: Optional[str] = None

class DriverResponse(DriverBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

# --- Lorry Schemas ---
class LorryBase(BaseModel):
    registration_number: str
    max_weight_kg: float = Field(..., gt=0, description="Max weight capacity in kg must be > 0")
    max_volume_m3: float = Field(..., gt=0, description="Max volume capacity in m3 must be > 0")
    fuel_efficiency_km_l: float = Field(..., gt=0, description="Fuel efficiency in km/L must be > 0")
    current_latitude: float = Field(..., ge=-90.0, le=90.0)
    current_longitude: float = Field(..., ge=-180.0, le=180.0)
    current_speed_km_h: float = 0.0
    current_heading_degrees: float = 0.0
    driver_id: Optional[str] = None
    status: str = "IDLE"
    current_route_id: Optional[str] = None

class LorryCreate(LorryBase):
    id: str

class LorryUpdate(BaseModel):
    registration_number: Optional[str] = None
    max_weight_kg: Optional[float] = None
    max_volume_m3: Optional[float] = None
    fuel_efficiency_km_l: Optional[float] = None
    current_latitude: Optional[float] = None
    current_longitude: Optional[float] = None
    current_speed_km_h: Optional[float] = None
    current_heading_degrees: Optional[float] = None
    driver_id: Optional[str] = None
    status: Optional[str] = None
    current_route_id: Optional[str] = None

class LorryResponse(LorryBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

# --- Shipment Schemas ---
class ShipmentBase(BaseModel):
    weight_kg: float = Field(..., gt=0, description="Weight in kg must be > 0")
    volume_m3: float = Field(..., gt=0, description="Volume in m3 must be > 0")
    pickup_address: str
    pickup_latitude: float = Field(..., ge=-90.0, le=90.0)
    pickup_longitude: float = Field(..., ge=-180.0, le=180.0)
    destination_address: str
    destination_latitude: float = Field(..., ge=-90.0, le=90.0)
    destination_longitude: float = Field(..., ge=-180.0, le=180.0)
    delivery_deadline: datetime.datetime
    priority: str = "NORMAL"
    status: str = "UNASSIGNED"

class ShipmentCreate(ShipmentBase):
    id: str

class ShipmentUpdate(BaseModel):
    weight_kg: Optional[float] = None
    volume_m3: Optional[float] = None
    pickup_address: Optional[str] = None
    pickup_latitude: Optional[float] = None
    pickup_longitude: Optional[float] = None
    destination_address: Optional[str] = None
    destination_latitude: Optional[float] = None
    destination_longitude: Optional[float] = None
    delivery_deadline: Optional[datetime.datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class ShipmentResponse(ShipmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

# --- Assignment Schemas ---
class AssignmentCreate(BaseModel):
    id: Optional[str] = None
    shipment_id: str
    lorry_id: str
    route_id: Optional[str] = None
    sequence: int = 1
    assignment_reason: Optional[str] = "Manual Dispatch Assignment"

class AssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    shipment_id: str
    lorry_id: str
    route_id: Optional[str] = None
    sequence: int
    assignment_reason: Optional[str] = None
    status: str
    created_at: Optional[datetime.datetime] = None

# --- Route Schemas ---
class RouteStopResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    route_id: str
    sequence: int
    stop_type: str
    shipment_id: Optional[str] = None
    latitude: float
    longitude: float
    address: str
    estimated_arrival: datetime.datetime
    deadline: datetime.datetime
    status: str

class RouteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    lorry_id: str
    status: str
    distance_meters: float
    estimated_duration_seconds: int
    fuel_estimate_liters: float
    cost_estimate: float
    deadline_risk: str
    stops: List[RouteStopResponse] = []
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

# --- Operational Event Schemas ---
class EventCreate(BaseModel):
    id: Optional[str] = None
    event_type: str
    source: str = "DISPATCHER_WEB"
    severity: str = "INFO"
    lorry_id: Optional[str] = None
    driver_id: Optional[str] = None
    shipment_id: Optional[str] = None
    payload_json: Dict[str, Any] = Field(default_factory=dict)
    resolution_status: str = "PENDING"

class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    event_type: str
    source: str
    severity: str
    lorry_id: Optional[str] = None
    driver_id: Optional[str] = None
    shipment_id: Optional[str] = None
    payload_json: Dict[str, Any]
    resolution_status: str
    created_at: Optional[datetime.datetime] = None

# --- Phone Call Schemas ---
class CallCreate(BaseModel):
    id: Optional[str] = None
    provider: str = "VAPI"
    driver_id: Optional[str] = None
    lorry_id: Optional[str] = None
    direction: str = "OUTBOUND"
    call_type: str = "STATUS_CHECK"
    status: Optional[str] = "QUEUED"
    phone_number: Optional[str] = None

class CallResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    provider: str
    external_call_id: Optional[str] = None
    driver_id: Optional[str] = None
    lorry_id: Optional[str] = None
    direction: str
    call_type: str
    status: str
    started_at: Optional[datetime.datetime] = None
    ended_at: Optional[datetime.datetime] = None
    transcript_reference: Optional[str] = None
    event_id: Optional[str] = None
    metadata_json: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime.datetime] = None

# --- Optimization Run Schemas ---
class OptimizationRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    trigger_reason: str
    status: str
    total_cost: float
    total_fuel_liters: float
    deadline_violations_count: int
    unassigned_count: int
    input_snapshot_json: Dict[str, Any]
    result_snapshot_json: Dict[str, Any]
    created_at: Optional[datetime.datetime] = None

# --- Tracking Position Schemas ---
class TrackingPositionCreate(BaseModel):
    lorry_id: str
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    speed_km_h: float = 0.0
    heading_degrees: float = 0.0
    status: str = "EN_ROUTE"

class TrackingPositionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lorry_id: str
    latitude: float
    longitude: float
    speed_km_h: float
    heading_degrees: float
    status: str
    recorded_at: Optional[datetime.datetime] = None
