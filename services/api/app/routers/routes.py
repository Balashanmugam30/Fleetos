"""
Fleetos Routes REST Router
Module Boundary: services/api/app/routers/routes.py
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from services.api.app.db.database import get_db
from services.api.app import crud, schemas

router = APIRouter(prefix="/api/v1/routes", tags=["Routes"])

@router.get("", response_model=List[schemas.RouteResponse])
async def list_routes(db: AsyncSession = Depends(get_db)):
    return await crud.get_routes(db)

@router.get("/{route_id}", response_model=schemas.RouteResponse)
async def get_route(route_id: str, db: AsyncSession = Depends(get_db)):
    route = await crud.get_route(db, route_id)
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Route '{route_id}' not found.")
    return route
