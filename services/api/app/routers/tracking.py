"""
Fleetos GPS Tracking Positions REST Router
Module Boundary: services/api/app/routers/tracking.py
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.app.db.database import get_db
from services.api.app import crud, schemas

router = APIRouter(prefix="/api/v1/tracking", tags=["Tracking"])

@router.get("/{lorry_id}", response_model=List[schemas.TrackingPositionResponse])
async def get_tracking_positions(
    lorry_id: str, 
    limit: int = Query(50, ge=1, le=500), 
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_tracking_positions(db, lorry_id=lorry_id, limit=limit)

@router.post("", response_model=schemas.TrackingPositionResponse, status_code=status.HTTP_201_CREATED)
async def create_tracking_position(
    pos: schemas.TrackingPositionCreate, 
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_tracking_position(db, pos)
