"""
Fleetos Lorries REST Router
Module Boundary: services/api/app/routers/lorries.py
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.app.db.database import get_db
from services.api.app import crud, schemas

router = APIRouter(prefix="/api/v1/lorries", tags=["Lorries"])

@router.get("", response_model=List[schemas.LorryResponse])
async def list_lorries(status: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_lorries(db, status=status)

@router.get("/{lorry_id}", response_model=schemas.LorryResponse)
async def get_lorry(lorry_id: str, db: AsyncSession = Depends(get_db)):
    lorry = await crud.get_lorry(db, lorry_id)
    if not lorry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lorry '{lorry_id}' not found.")
    return lorry

@router.post("", response_model=schemas.LorryResponse, status_code=status.HTTP_201_CREATED)
async def create_lorry(lorry: schemas.LorryCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_lorry(db, lorry.id)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Lorry with ID '{lorry.id}' already exists.")
    return await crud.create_lorry(db, lorry)

@router.patch("/{lorry_id}", response_model=schemas.LorryResponse)
async def update_lorry(lorry_id: str, update_data: schemas.LorryUpdate, db: AsyncSession = Depends(get_db)):
    updated = await crud.update_lorry(db, lorry_id, update_data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lorry '{lorry_id}' not found.")
    return updated
