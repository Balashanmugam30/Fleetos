"""
Fleetos Optimization Runs History REST Router
Module Boundary: services/api/app/routers/optimization.py
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.app.db.database import get_db
from services.api.app import crud, schemas

router = APIRouter(prefix="/api/v1/optimization", tags=["Optimization Runs"])

@router.get("/runs", response_model=List[schemas.OptimizationRunResponse])
async def list_optimization_runs(db: AsyncSession = Depends(get_db)):
    return await crud.get_optimization_runs(db)
