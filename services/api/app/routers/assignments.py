"""
Fleetos Assignments REST Router
Module Boundary: services/api/app/routers/assignments.py
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.app.db.database import get_db
from services.api.app import crud, schemas

router = APIRouter(prefix="/api/v1/assignments", tags=["Assignments"])

@router.get("", response_model=List[schemas.AssignmentResponse])
async def list_assignments(db: AsyncSession = Depends(get_db)):
    return await crud.get_assignments(db)

@router.post("", response_model=schemas.AssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(assignment: schemas.AssignmentCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_assignment(db, assignment)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
