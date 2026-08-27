"""
Fleetos SQLAlchemy Declarative ORM Models
Module Boundary: services/api/app/models.py
"""

import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from services.api.app.db.database import Base

def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)

class DriverModel(Base):
    __tablename__ = "drivers"

    id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False)
    phone_number = Column(String(32), nullable=False)
    availability_status = Column(String(32), nullable=False, default="AVAILABLE")
    current_lorry_id = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    lorries = relationship("LorryModel", back_populates="driver", foreign_keys="LorryModel.driver_id")

class LorryModel(Base):
    __tablename__ = "lorries"

    id = Column(String(64), primary_key=True)
    registration_number = Column(String(32), nullable=False, unique=True)
    max_weight_kg = Column(Float, nullable=False)
    max_volume_m3 = Column(Float, nullable=False)
    current_latitude = Column(Float, nullable=False)
    current_longitude = Column(Float, nullable=False)
    current_speed_km_h = Column(Float, default=0.0)
    current_heading_degrees = Column(Float, default=0.0)
    fuel_efficiency_km_l = Column(Float, nullable=False)
    driver_id = Column(String(64), ForeignKey("drivers.id"), nullable=True)
    status = Column(String(32), nullable=False, default="IDLE")
    current_route_id = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    driver = relationship("DriverModel", back_populates="lorries", foreign_keys=[driver_id])
    assignments = relationship("AssignmentModel", back_populates="lorry")

class ShipmentModel(Base):
    __tablename__ = "shipments"

    id = Column(String(64), primary_key=True)
    weight_kg = Column(Float, nullable=False)
    volume_m3 = Column(Float, nullable=False)
    pickup_address = Column(Text, nullable=False)
    pickup_latitude = Column(Float, nullable=False)
    pickup_longitude = Column(Float, nullable=False)
    destination_address = Column(Text, nullable=False)
    destination_latitude = Column(Float, nullable=False)
    destination_longitude = Column(Float, nullable=False)
    delivery_deadline = Column(DateTime(timezone=True), nullable=False)
    priority = Column(String(16), nullable=False, default="NORMAL")
    status = Column(String(32), nullable=False, default="UNASSIGNED")
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    assignments = relationship("AssignmentModel", back_populates="shipment")

class AssignmentModel(Base):
    __tablename__ = "assignments"

    id = Column(String(64), primary_key=True)
    shipment_id = Column(String(64), ForeignKey("shipments.id"), nullable=False)
    lorry_id = Column(String(64), ForeignKey("lorries.id"), nullable=False)
    route_id = Column(String(64), ForeignKey("routes.id"), nullable=True)
    sequence = Column(Integer, nullable=False, default=1)
    assignment_reason = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="ACTIVE")
    created_at = Column(DateTime(timezone=True), default=utcnow)

    shipment = relationship("ShipmentModel", back_populates="assignments")
    lorry = relationship("LorryModel", back_populates="assignments")
    route = relationship("RouteModel", back_populates="assignments")

class RouteModel(Base):
    __tablename__ = "routes"

    id = Column(String(64), primary_key=True)
    lorry_id = Column(String(64), ForeignKey("lorries.id"), nullable=False)
    status = Column(String(32), nullable=False, default="PLANNED")
    distance_meters = Column(Float, nullable=False, default=0.0)
    estimated_duration_seconds = Column(Integer, nullable=False, default=0)
    fuel_estimate_liters = Column(Float, nullable=False, default=0.0)
    cost_estimate = Column(Float, nullable=False, default=0.0)
    deadline_risk = Column(String(16), nullable=False, default="NONE")
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    assignments = relationship("AssignmentModel", back_populates="route")
    stops = relationship("RouteStopModel", back_populates="route", cascade="all, delete-orphan")

class RouteStopModel(Base):
    __tablename__ = "route_stops"

    id = Column(String(64), primary_key=True)
    route_id = Column(String(64), ForeignKey("routes.id", ondelete="CASCADE"), nullable=False)
    sequence = Column(Integer, nullable=False)
    stop_type = Column(String(16), nullable=False)  # 'START' | 'PICKUP' | 'DELIVERY' | 'END'
    shipment_id = Column(String(64), ForeignKey("shipments.id"), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(Text, nullable=False)
    estimated_arrival = Column(DateTime(timezone=True), nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(32), nullable=False, default="PLANNED")
    created_at = Column(DateTime(timezone=True), default=utcnow)

    route = relationship("RouteModel", back_populates="stops")

class EventModel(Base):
    __tablename__ = "events"

    id = Column(String(64), primary_key=True)
    event_type = Column(String(64), nullable=False)
    source = Column(String(32), nullable=False)
    severity = Column(String(16), nullable=False, default="INFO")
    lorry_id = Column(String(64), ForeignKey("lorries.id"), nullable=True)
    driver_id = Column(String(64), ForeignKey("drivers.id"), nullable=True)
    shipment_id = Column(String(64), ForeignKey("shipments.id"), nullable=True)
    payload_json = Column(JSON, nullable=False, default=dict)
    resolution_status = Column(String(32), nullable=False, default="PENDING")
    created_at = Column(DateTime(timezone=True), default=utcnow)

class CallModel(Base):
    __tablename__ = "calls"

    id = Column(String(64), primary_key=True)
    provider = Column(String(32), nullable=False, default="VAPI")
    external_call_id = Column(String(128), nullable=True)
    driver_id = Column(String(64), ForeignKey("drivers.id"), nullable=True)
    lorry_id = Column(String(64), ForeignKey("lorries.id"), nullable=True)
    direction = Column(String(16), nullable=False, default="OUTBOUND")
    call_type = Column(String(32), nullable=False)
    status = Column(String(32), nullable=False, default="QUEUED")
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    transcript_reference = Column(Text, nullable=True)
    event_id = Column(String(64), ForeignKey("events.id"), nullable=True)
    metadata_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=utcnow)

class OptimizationRunModel(Base):
    __tablename__ = "optimization_runs"

    id = Column(String(64), primary_key=True)
    trigger_reason = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False, default="OPTIMAL")
    total_cost = Column(Float, nullable=False, default=0.0)
    total_fuel_liters = Column(Float, nullable=False, default=0.0)
    deadline_violations_count = Column(Integer, nullable=False, default=0)
    unassigned_count = Column(Integer, nullable=False, default=0)
    input_snapshot_json = Column(JSON, nullable=False, default=dict)
    result_snapshot_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=utcnow)

class TrackingPositionModel(Base):
    __tablename__ = "tracking_positions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lorry_id = Column(String(64), ForeignKey("lorries.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed_km_h = Column(Float, nullable=False, default=0.0)
    heading_degrees = Column(Float, nullable=False, default=0.0)
    status = Column(String(32), nullable=False, default="EN_ROUTE")
    recorded_at = Column(DateTime(timezone=True), default=utcnow)
