"""
Fleetos Twilio ConversationRelay & OpenAI Configuration Management
Module Boundary: services/voice/twilio_config.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

import os
from pydantic import BaseModel

class TwilioConfig(BaseModel):
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_phone_number: str = os.getenv("TWILIO_PHONE_NUMBER", "")
    webhook_base_url: str = os.getenv("TWILIO_WEBHOOK_BASE_URL", os.getenv("VOICE_WEBHOOK_BASE_URL", "http://127.0.0.1:8000"))
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    atlas_provider: str = os.getenv("VOICE_PROVIDER", os.getenv("ATLAS_PROVIDER", "twilio")).lower()

    @property
    def is_twilio_configured(self) -> bool:
        return bool(self.twilio_account_sid and self.twilio_auth_token and self.twilio_phone_number)

    @property
    def is_openai_configured(self) -> bool:
        return bool(self.openai_api_key)

    @property
    def is_public_webhook_configured(self) -> bool:
        url = self.webhook_base_url.lower()
        return "trycloudflare.com" in url or "ngrok" in url or "https://" in url

    @property
    def is_real_pstn_ready(self) -> bool:
        return self.is_twilio_configured and self.is_openai_configured and self.is_public_webhook_configured

twilio_config = TwilioConfig()
