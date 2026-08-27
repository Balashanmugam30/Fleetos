"""
Fleetos Drivers REST Router
Module Boundary: services/api/app/routers/drivers.py
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.app.db.database import get_db
from services.api.app import crud, schemas

router = APIRouter(prefix="/api/v1/drivers", tags=["Drivers"])

@router.get("", response_model=List[schemas.DriverResponse])
async def list_drivers(availability_status: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_drivers(db, availability_status=availability_status)

@router.get("/{driver_id}", response_model=schemas.DriverResponse)
async def get_driver(driver_id: str, db: AsyncSession = Depends(get_db)):
    driver = await crud.get_driver(db, driver_id)
    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Driver '{driver_id}' not found.")
    return driver

@router.post("", response_model=schemas.DriverResponse, status_code=status.HTTP_201_CREATED)
async def create_driver(driver: schemas.DriverCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_driver(db, driver.id)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Driver with ID '{driver.id}' already exists.")
    return await crud.create_driver(db, driver)

@router.patch("/{driver_id}", response_model=schemas.DriverResponse)
async def update_driver(driver_id: str, update_data: schemas.DriverUpdate, db: AsyncSession = Depends(get_db)):
    updated = await crud.update_driver(db, driver_id, update_data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Driver '{driver_id}' not found.")
    return updated
