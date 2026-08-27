"""
Fleetos FastAPI Master Server
Module Boundary: services/api/app/main.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services.api.app.config import settings
from services.api.app.schemas import HealthResponse, VersionResponse, ErrorResponse, ErrorDetail

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Fleetos Agentic Multimodal Fleet Intelligence Platform REST & Webhook Gateway"
)

# Configure Security CORS Policies
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected server error occurred.",
                details={"path": str(request.url.path)}
            )
        ).model_dump()
    )

@app.get("/health", response_model=HealthResponse, tags=["Health"])
@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
async def get_health():
    return HealthResponse(
        status="ok",
        service="fleetos-api",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT
    )

@app.get("/api/v1/version", response_model=VersionResponse, tags=["Version"])
async def get_version():
    return VersionResponse(
        name="Fleetos Agentic Multimodal Fleet Intelligence Platform",
        version=settings.APP_VERSION,
        core_loop="SEE → HEAR → THINK → OPTIMIZE → ACT → UPDATE",
        voice_agent="ATLAS"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("services.api.app.main:app", host="0.0.0.0", port=8000, reload=True)
