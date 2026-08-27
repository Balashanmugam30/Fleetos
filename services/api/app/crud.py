"""
Fleetos Async SQLAlchemy Database CRUD Repositories & State Transition Guardrails
Module Boundary: services/api/app/crud.py
"""

import uuid
import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from services.api.app import models, schemas

# Valid Shipment Status Transitions
VALID_SHIPMENT_TRANSITIONS = {
    "UNASSIGNED": {"ASSIGNED", "CANCELLED"},
    "ASSIGNED": {"PICKED_UP", "CANCELLED", "AT_RISK", "UNASSIGNED"},
    "PICKED_UP": {"IN_TRANSIT", "CANCELLED", "AT_RISK"},
    "IN_TRANSIT": {"DELIVERED", "CANCELLED", "AT_RISK"},
    "AT_RISK": {"IN_TRANSIT", "CANCELLED", "DELIVERED", "ASSIGNED"},
    "DELIVERED": set(),  # Terminal state
    "CANCELLED": set()   # Terminal state
}

# --- Driver CRUD ---
async def get_drivers(db: AsyncSession, availability_status: Optional[str] = None) -> List[models.DriverModel]:
    query = select(models.DriverModel)
    if availability_status:
        query = query.where(models.DriverModel.availability_status == availability_status)
    result = await db.execute(query)
    return list(result.scalars().all())

async def get_driver(db: AsyncSession, driver_id: str) -> Optional[models.DriverModel]:
    result = await db.execute(select(models.DriverModel).where(models.DriverModel.id == driver_id))
    return result.scalar_one_or_none()

async def create_driver(db: AsyncSession, driver: schemas.DriverCreate) -> models.DriverModel:
    db_driver = models.DriverModel(**driver.model_dump())
    db.add(db_driver)
    await db.commit()
    await db.refresh(db_driver)
    return db_driver

async def update_driver(db: AsyncSession, driver_id: str, update_data: schemas.DriverUpdate) -> Optional[models.DriverModel]:
    db_driver = await get_driver(db, driver_id)
    if not db_driver:
        return None
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_driver, key, value)
    await db.commit()
    await db.refresh(db_driver)
    return db_driver

# --- Lorry CRUD ---
async def get_lorries(db: AsyncSession, status: Optional[str] = None) -> List[models.LorryModel]:
    query = select(models.LorryModel)
    if status:
        query = query.where(models.LorryModel.status == status)
    result = await db.execute(query)
    return list(result.scalars().all())

async def get_lorry(db: AsyncSession, lorry_id: str) -> Optional[models.LorryModel]:
    result = await db.execute(select(models.LorryModel).where(models.LorryModel.id == lorry_id))
    return result.scalar_one_or_none()

async def create_lorry(db: AsyncSession, lorry: schemas.LorryCreate) -> models.LorryModel:
    db_lorry = models.LorryModel(**lorry.model_dump())
    db.add(db_lorry)
    await db.commit()
    await db.refresh(db_lorry)
    return db_lorry

async def update_lorry(db: AsyncSession, lorry_id: str, update_data: schemas.LorryUpdate) -> Optional[models.LorryModel]:
    db_lorry = await get_lorry(db, lorry_id)
    if not db_lorry:
        return None
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_lorry, key, value)
    await db.commit()
    await db.refresh(db_lorry)
    return db_lorry

# --- Shipment CRUD ---
async def get_shipments(
    db: AsyncSession, 
    status: Optional[str] = None, 
    priority: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> List[models.ShipmentModel]:
    query = select(models.ShipmentModel)
    if status:
        query = query.where(models.ShipmentModel.status == status)
    if priority:
        query = query.where(models.ShipmentModel.priority == priority)
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    return list(result.scalars().all())

async def get_shipment(db: AsyncSession, shipment_id: str) -> Optional[models.ShipmentModel]:
    result = await db.execute(select(models.ShipmentModel).where(models.ShipmentModel.id == shipment_id))
    return result.scalar_one_or_none()

async def create_shipment(db: AsyncSession, shipment: schemas.ShipmentCreate) -> models.ShipmentModel:
    db_shipment = models.ShipmentModel(**shipment.model_dump())
    db.add(db_shipment)
    await db.commit()
    await db.refresh(db_shipment)
    return db_shipment

async def update_shipment(db: AsyncSession, shipment_id: str, update_data: schemas.ShipmentUpdate) -> Optional[models.ShipmentModel]:
    db_shipment = await get_shipment(db, shipment_id)
    if not db_shipment:
        return None
    
    # Enforce Status Transition State Machine Rules
    if update_data.status and update_data.status != db_shipment.status:
        allowed = VALID_SHIPMENT_TRANSITIONS.get(db_shipment.status, set())
        if update_data.status not in allowed:
            raise ValueError(f"Invalid shipment status transition from '{db_shipment.status}' to '{update_data.status}'")

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_shipment, key, value)
    
    await db.commit()
    await db.refresh(db_shipment)
    return db_shipment

# --- Assignment CRUD ---
async def create_assignment(db: AsyncSession, assignment_data: schemas.AssignmentCreate) -> models.AssignmentModel:
    # 1. Validate Shipment Exists
    shipment = await get_shipment(db, assignment_data.shipment_id)
    if not shipment:
        raise ValueError(f"Shipment '{assignment_data.shipment_id}' does not exist.")

    # 2. Validate Lorry Exists
    lorry = await get_lorry(db, assignment_data.lorry_id)
    if not lorry:
        raise ValueError(f"Lorry '{assignment_data.lorry_id}' does not exist.")

    # 3. Check for conflicting active assignment
    existing_active = await db.execute(
        select(models.AssignmentModel).where(
            models.AssignmentModel.shipment_id == assignment_data.shipment_id,
            models.AssignmentModel.status == "ACTIVE"
        )
    )
    if existing_active.scalar_one_or_none():
        raise ValueError(f"Shipment '{assignment_data.shipment_id}' already has an active assignment.")

    assignment_id = assignment_data.id or f"asg_{uuid.uuid4().hex[:8]}"
    db_assignment = models.AssignmentModel(
        id=assignment_id,
        shipment_id=assignment_data.shipment_id,
        lorry_id=assignment_data.lorry_id,
        route_id=assignment_data.route_id,
        sequence=assignment_data.sequence,
        assignment_reason=assignment_data.assignment_reason,
        status="ACTIVE"
    )

    # Update Shipment status
    shipment.status = "ASSIGNED"
    db.add(db_assignment)
    await db.commit()
    await db.refresh(db_assignment)
    return db_assignment

async def get_assignments(db: AsyncSession) -> List[models.AssignmentModel]:
    result = await db.execute(select(models.AssignmentModel))
    return list(result.scalars().all())

# --- Route CRUD ---
async def get_routes(db: AsyncSession) -> List[models.RouteModel]:
    result = await db.execute(select(models.RouteModel))
    return list(result.scalars().all())

async def get_route(db: AsyncSession, route_id: str) -> Optional[models.RouteModel]:
    result = await db.execute(select(models.RouteModel).where(models.RouteModel.id == route_id))
    return result.scalar_one_or_none()

# --- Event CRUD ---
async def create_event(db: AsyncSession, event_data: schemas.EventCreate) -> models.EventModel:
    event_id = event_data.id or f"evt_{uuid.uuid4().hex[:8]}"
    db_event = models.EventModel(
        id=event_id,
        event_type=event_data.event_type,
        source=event_data.source,
        severity=event_data.severity,
        lorry_id=event_data.lorry_id,
        driver_id=event_data.driver_id,
        shipment_id=event_data.shipment_id,
        payload_json=event_data.payload_json,
        resolution_status=event_data.resolution_status
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event

async def get_events(db: AsyncSession, limit: int = 50) -> List[models.EventModel]:
    result = await db.execute(select(models.EventModel).order_by(models.EventModel.created_at.desc()).limit(limit))
    return list(result.scalars().all())

# --- Call CRUD ---
async def create_call(db: AsyncSession, call_data: schemas.CallCreate) -> models.CallModel:
    call_id = call_data.id or f"call_{uuid.uuid4().hex[:8]}"
    db_call = models.CallModel(
        id=call_id,
        provider=call_data.provider,
        driver_id=call_data.driver_id,
        lorry_id=call_data.lorry_id,
        direction=call_data.direction,
        call_type=call_data.call_type,
        status="QUEUED"
    )
    db.add(db_call)
    await db.commit()
    await db.refresh(db_call)
    return db_call

async def get_calls(db: AsyncSession) -> List[models.CallModel]:
    result = await db.execute(select(models.CallModel).order_by(models.CallModel.created_at.desc()))
    return list(result.scalars().all())

# --- Optimization Run CRUD ---
async def get_optimization_runs(db: AsyncSession) -> List[models.OptimizationRunModel]:
    result = await db.execute(select(models.OptimizationRunModel).order_by(models.OptimizationRunModel.created_at.desc()))
    return list(result.scalars().all())

# --- Tracking Position CRUD ---
async def create_tracking_position(db: AsyncSession, pos_data: schemas.TrackingPositionCreate) -> models.TrackingPositionModel:
    db_pos = models.TrackingPositionModel(**pos_data.model_dump())
    db.add(db_pos)
    await db.commit()
    await db.refresh(db_pos)
    return db_pos

async def get_tracking_positions(db: AsyncSession, lorry_id: str, limit: int = 50) -> List[models.TrackingPositionModel]:
    result = await db.execute(
        select(models.TrackingPositionModel)
        .where(models.TrackingPositionModel.lorry_id == lorry_id)
        .order_by(models.TrackingPositionModel.recorded_at.desc())
        .limit(limit)
    )
    return list(result.scalars().all())
