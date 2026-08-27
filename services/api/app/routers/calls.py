"""
Fleetos Phone Calls History REST Router
Module Boundary: services/api/app/routers/calls.py
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.app.db.database import get_db
from services.api.app import crud, schemas

router = APIRouter(prefix="/api/v1/calls", tags=["Phone Calls"])

@router.get("", response_model=List[schemas.CallResponse])
async def list_calls(db: AsyncSession = Depends(get_db)):
    return await crud.get_calls(db)

@router.post("", response_model=schemas.CallResponse, status_code=status.HTTP_201_CREATED)
async def create_call(call: schemas.CallCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_call(db, call)
