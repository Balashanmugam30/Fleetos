"""
Fleetos Sarvam Multilingual Voice Agent Configuration Management
Module Boundary: services/voice/sarvam_config.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

import os
from pydantic import BaseModel

class SarvamConfig(BaseModel):
    sarvam_api_key: str = os.getenv("SARVAM_API_KEY", "")
    sarvam_agent_id: str = os.getenv("SARVAM_AGENT_ID", "")
    sarvam_deployment_id: str = os.getenv("SARVAM_DEPLOYMENT_ID", "")
    sarvam_api_base_url: str = os.getenv("SARVAM_API_BASE_URL", "https://api.sarvam.ai")
    sarvam_default_language: str = os.getenv("SARVAM_DEFAULT_LANGUAGE", "hi-IN")
    webhook_base_url: str = os.getenv("SARVAM_WEBHOOK_BASE_URL", os.getenv("VOICE_WEBHOOK_BASE_URL", "http://127.0.0.1:8000"))
    sarvam_tool_secret: str = os.getenv("SARVAM_TOOL_SECRET", "fleetos_sarvam_tool_sec_2026")

    # Twilio Telephony Credentials
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_phone_number: str = os.getenv("TWILIO_PHONE_NUMBER", "")

    active_provider: str = os.getenv("VOICE_PROVIDER", os.getenv("ATLAS_PROVIDER", "sarvam")).lower()

    @property
    def is_sarvam_configured(self) -> bool:
        return bool(self.sarvam_api_key)

    @property
    def is_twilio_configured(self) -> bool:
        return bool(self.twilio_account_sid and self.twilio_auth_token and self.twilio_phone_number)

    @property
    def is_public_webhook_configured(self) -> bool:
        url = self.webhook_base_url.lower()
        return "trycloudflare.com" in url or "ngrok" in url or "https://" in url

    @property
    def is_real_pstn_ready(self) -> bool:
        return self.is_sarvam_configured and self.is_twilio_configured and self.is_public_webhook_configured

sarvam_config = SarvamConfig()
