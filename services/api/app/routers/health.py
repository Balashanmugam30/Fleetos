"""
Fleetos Health & Database Readiness Routers
Module Boundary: services/api/app/routers/health.py
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from services.api.app.db.database import get_db, async_engine
from services.api.app.schemas import HealthResponse, DBHealthResponse, VersionResponse
from services.api.app.config import settings

router = APIRouter(prefix="/api/v1", tags=["Health & Version"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok",
        service="fleetos-api",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT
    )

@router.get("/health/db", response_model=DBHealthResponse)
async def db_health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return DBHealthResponse(
            status="ok",
            database="connected",
            engine=str(async_engine.url.drivername),
            environment=settings.ENVIRONMENT
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connectivity check failed: {str(e)}"
        )

@router.get("/version", response_model=VersionResponse)
async def version_info():
    return VersionResponse(
        name="Fleetos Agentic Multimodal Fleet Intelligence Platform",
        version=settings.APP_VERSION,
        core_loop="SEE → HEAR → THINK → OPTIMIZE → ACT → UPDATE",
        voice_agent="ATLAS",
        optimization_solver="Google OR-Tools Routing Solver / RoutingModel"
    )
