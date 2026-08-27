"""
Fleetos FastAPI Master Application Server
Module Boundary: services/api/app/main.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from services.api.app.config import settings
from services.api.app.db.database import init_db
from services.api.app.schemas import ErrorResponse, ErrorDetail
from services.api.app.routers import (
    health,
    lorries,
    drivers,
    shipments,
    assignments,
    routes,
    events,
    calls,
    optimization,
    tracking,
    voice
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Database DDL Tables on Startup
    await init_db()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Fleetos Agentic Multimodal Fleet Intelligence Platform REST & Webhook Gateway",
    lifespan=lifespan
)

# Configure Security CORS Policies
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Global Exception Handler for Uncaught Server Errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected server error occurred.",
                details={"path": str(request.url.path), "error": str(exc)}
            )
        ).model_dump()
    )

# Register Versioned API Routers
app.include_router(health.router)
app.include_router(lorries.router)
app.include_router(drivers.router)
app.include_router(shipments.router)
app.include_router(assignments.router)
app.include_router(routes.router)
app.include_router(events.router)
app.include_router(calls.router)
app.include_router(optimization.router)
app.include_router(tracking.router)
from services.voice.conversation_relay import router as twilio_router
from services.api.app.routers.sarvam_webhook import router as sarvam_router

app.include_router(voice.router)
app.include_router(twilio_router)
app.include_router(sarvam_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("services.api.app.main:app", host="0.0.0.0", port=8000, reload=True)
