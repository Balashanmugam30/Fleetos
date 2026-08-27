"""
Fleetos Computer Vision & Document OCR Interface
Module Boundary: services/vision
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel

class MarkerRecognitionRequest(BaseModel):
    image_base64: str
    target_type: str  # 'LORRY_MARKER' | 'SHIPMENT_LABEL' | 'BILL_OF_LADING'

class RecognitionResult(BaseModel):
    detected: bool
    entity_id: Optional[str] = None
    confidence: float = 0.0
    extracted_metadata: Dict[str, Any] = {}

class VisionInterface:
    """Abstract Computer Vision & Marker Extraction Interface."""
    def process_image(self, request: MarkerRecognitionRequest) -> RecognitionResult:
        raise NotImplementedError("Vision processing will be implemented in Phase 13.")
