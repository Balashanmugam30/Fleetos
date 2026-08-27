"""
Fleetos System API Response Schemas
Module Boundary: services/api/app/schemas.py
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "fleetos-api"
    version: str = "0.1.0"
    environment: str = "development"

class VersionResponse(BaseModel):
    name: str = "Fleetos Agentic Multimodal Fleet Intelligence Platform"
    version: str = "0.1.0"
    core_loop: str = "SEE → HEAR → THINK → OPTIMIZE → ACT → UPDATE"
    voice_agent: str = "ATLAS"

class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)

class ErrorResponse(BaseModel):
    error: ErrorDetail
