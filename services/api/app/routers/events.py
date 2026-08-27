"""
Fleetos Operational Events REST Router
Module Boundary: services/api/app/routers/events.py
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.app.db.database import get_db
from services.api.app import crud, schemas

router = APIRouter(prefix="/api/v1/events", tags=["Operational Events"])

@router.get("", response_model=List[schemas.EventResponse])
async def list_events(limit: int = Query(50, ge=1, le=500), db: AsyncSession = Depends(get_db)):
    return await crud.get_events(db, limit=limit)

@router.post("", response_model=schemas.EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(event: schemas.EventCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_event(db, event)
