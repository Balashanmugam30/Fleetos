"""
Fleetos Voice Agent Configuration Management
Module Boundary: services/voice/config.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

import os
from pydantic import BaseModel

class VoiceConfig(BaseModel):
    vapi_api_key: str = os.getenv("VAPI_API_KEY", "")
    vapi_phone_number_id: str = os.getenv("VAPI_PHONE_NUMBER_ID", "")
    vapi_assistant_id: str = os.getenv("VAPI_ASSISTANT_ID", "")
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_phone_number: str = os.getenv("TWILIO_PHONE_NUMBER", "")
    webhook_base_url: str = os.getenv("VOICE_WEBHOOK_BASE_URL", os.getenv("TWILIO_WEBHOOK_BASE_URL", "http://127.0.0.1:8000"))
    active_provider: str = os.getenv("VOICE_PROVIDER", os.getenv("ATLAS_PROVIDER", "twilio")).lower()  # 'twilio' | 'demo' | 'vapi'

    @property
    def is_real_vapi_configured(self) -> bool:
        return bool(self.vapi_api_key and self.vapi_phone_number_id)

    @property
    def is_twilio_configured(self) -> bool:
        return bool(self.twilio_account_sid and self.twilio_auth_token and self.twilio_phone_number)

    @property
    def is_openai_configured(self) -> bool:
        return bool(os.getenv("OPENAI_API_KEY", ""))

voice_config = VoiceConfig()
