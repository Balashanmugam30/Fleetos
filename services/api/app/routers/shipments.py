"""
Fleetos Shipments REST Router
Module Boundary: services/api/app/routers/shipments.py
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.app.db.database import get_db
from services.api.app import crud, schemas

router = APIRouter(prefix="/api/v1/shipments", tags=["Shipments"])

@router.get("", response_model=List[schemas.ShipmentResponse])
async def list_shipments(
    status_filter: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_shipments(db, status=status_filter, priority=priority, limit=limit, offset=offset)

@router.get("/{shipment_id}", response_model=schemas.ShipmentResponse)
async def get_shipment(shipment_id: str, db: AsyncSession = Depends(get_db)):
    shipment = await crud.get_shipment(db, shipment_id)
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shipment '{shipment_id}' not found.")
    return shipment

@router.post("", response_model=schemas.ShipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment(shipment: schemas.ShipmentCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_shipment(db, shipment.id)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Shipment with ID '{shipment.id}' already exists.")
    return await crud.create_shipment(db, shipment)

@router.patch("/{shipment_id}", response_model=schemas.ShipmentResponse)
async def update_shipment(shipment_id: str, update_data: schemas.ShipmentUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated = await crud.update_shipment(db, shipment_id, update_data)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shipment '{shipment_id}' not found.")
        return updated
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
