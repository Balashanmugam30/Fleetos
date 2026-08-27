"""
Fleetos GPS Tracking Positions REST Router
Module Boundary: services/api/app/routers/tracking.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.app.db.database import get_db
from services.tracking.models import TrackingPosition, VehicleTrackingState
from services.tracking.service import TrackingService
from services.tracking.simulator import SimulatorTrackingProvider

router = APIRouter(prefix="/api/v1/tracking", tags=["Tracking"])

# Global singleton tracking service instance for development/demo
_simulator_provider = SimulatorTrackingProvider()
_tracking_service = TrackingService(provider=_simulator_provider)

@router.get("/latest", response_model=List[VehicleTrackingState])
async def get_latest_tracking_states():
    """Returns the latest tracking states for all active vehicles."""
    return _tracking_service.get_all_latest_states()

@router.get("/vehicles/{vehicle_id}", response_model=VehicleTrackingState)
async def get_vehicle_tracking_state(vehicle_id: str):
    """Returns the latest tracking state for a specific vehicle."""
    state = _tracking_service.get_latest_state(vehicle_id)
    if not state:
        # Pull from provider to check if available
        pos = _simulator_provider.get_vehicle_position(vehicle_id)
        if pos:
            state = _tracking_service.ingest_position(pos)
    if not state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle {vehicle_id} tracking state not found.")
    return state

@router.get("/vehicles/{vehicle_id}/history", response_model=List[TrackingPosition])
async def get_vehicle_tracking_history(vehicle_id: str, limit: int = Query(50, ge=1, le=500)):
    """Returns recent location history for a specific vehicle."""
    return _tracking_service.get_history(vehicle_id, limit=limit)

@router.post("/ingest", response_model=VehicleTrackingState, status_code=status.HTTP_201_CREATED)
async def ingest_tracking_position(pos: TrackingPosition):
    """Ingests a new telemetry position update into the tracking engine."""
    try:
        return _tracking_service.ingest_position(pos)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

@router.post("/simulator/start")
async def start_tracking_simulator():
    """Starts the development GPS tracking simulator."""
    _simulator_provider.start()
    return {"status": "running", "message": "Development GPS tracking simulator started."}

@router.post("/simulator/stop")
async def stop_tracking_simulator():
    """Stops the development GPS tracking simulator."""
    _simulator_provider.stop()
    return {"status": "stopped", "message": "Development GPS tracking simulator stopped."}

@router.get("/simulator/status")
async def get_simulator_status():
    """Returns the status of the development GPS tracking simulator."""
    return {
        "running": _simulator_provider.is_running,
        "update_interval_seconds": _simulator_provider.update_interval_seconds,
        "simulated_vehicles_count": len(_simulator_provider.routes),
        "last_update_time": _simulator_provider.last_update_time.isoformat() if _simulator_provider.last_update_time else None
    }
