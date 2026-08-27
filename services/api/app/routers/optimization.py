"""
Fleetos Optimization Runs REST Router
Module Boundary: services/api/app/routers/optimization.py
"""

import json
import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.app.db.database import get_db
from services.api.app import crud, models, schemas
from services.optimizer.models import (
    OptimizationInput, VehicleInput, ShipmentInput, ObjectiveConfig
)
from services.optimizer.service import OptimizationService

router = APIRouter(prefix="/api/v1/optimization", tags=["Optimization Runs"])

@router.post("/run", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def run_optimization(
    trigger_reason: str = "MANUAL_REOPTIMIZE",
    mode: str = "BASELINE",
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger Google OR-Tools Routing Solver / RoutingModel VRP optimization engine.
    Reads authoritative active Lorries and Shipments from database, solves VRP, and persists run metrics.
    """
    # 1. Fetch active Lorries from database
    db_lorries = await crud.get_lorries(db)
    if not db_lorries:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No lorries found in database to optimize.")

    # 2. Fetch Shipments from database
    db_shipments = await crud.get_shipments(db)
    if not db_shipments:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No shipments found in database to optimize.")

    # 3. Construct Normalized Vehicle Inputs
    vehicle_inputs = [
        VehicleInput(
            id=l.id,
            registration_number=l.registration_number,
            start_latitude=l.current_latitude,
            start_longitude=l.current_longitude,
            max_weight_kg=l.max_weight_kg,
            max_volume_m3=l.max_volume_m3,
            fuel_efficiency_km_l=l.fuel_efficiency_km_l,
            driver_available=(l.status != "UNAVAILABLE" and l.driver_id is not None),
            status=l.status
        )
        for l in db_lorries
    ]

    # 4. Construct Normalized Shipment Inputs
    shipment_inputs = [
        ShipmentInput(
            id=s.id,
            weight_kg=s.weight_kg,
            volume_m3=s.volume_m3,
            pickup_address=s.pickup_address,
            pickup_latitude=s.pickup_latitude,
            pickup_longitude=s.pickup_longitude,
            destination_address=s.destination_address,
            destination_latitude=s.destination_latitude,
            destination_longitude=s.destination_longitude,
            delivery_deadline=s.delivery_deadline,
            priority=s.priority
        )
        for s in db_shipments
    ]

    opt_input = OptimizationInput(
        vehicles=vehicle_inputs,
        shipments=shipment_inputs,
        config=ObjectiveConfig(),
        mode=mode
    )

    # 5. Run OR-Tools Routing Solver
    result = OptimizationService.run_optimization(opt_input, trigger_reason=trigger_reason)

    # 6. Persist Optimization Run to Database
    db_run = models.OptimizationRunModel(
        id=result.run_id,
        trigger_reason=result.trigger_reason,
        status=result.status,
        total_cost=result.metrics.total_cost,
        total_fuel_liters=result.metrics.total_fuel_liters,
        deadline_violations_count=result.metrics.deadline_violations_count,
        unassigned_count=result.metrics.unassigned_count,
        input_snapshot_json={"vehicles_count": len(vehicle_inputs), "shipments_count": len(shipment_inputs)},
        result_snapshot_json=result.model_dump(mode="json")
    )
    db.add(db_run)
    await db.commit()

    return result.model_dump(mode="json")

@router.get("/runs", response_model=List[schemas.OptimizationRunResponse])
async def list_optimization_runs(db: AsyncSession = Depends(get_db)):
    return await crud.get_optimization_runs(db)
