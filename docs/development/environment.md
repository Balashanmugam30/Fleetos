# Fleetos Environment Configuration Guide

Product: **Fleetos**

---

## Environment Variable Schema & Boundaries

All environment variables must be declared in `.env.example` before being used in application code.

### 1. Server-Only Environment Variables (Private)

- `VAPI_API_KEY`: Secret authentication token for Vapi AI telephony API.
- `TWILIO_ACCOUNT_SID`: Secret SID for Twilio PSTN gateway.
- `TWILIO_AUTH_TOKEN`: Secret authentication token for Twilio.
- `DATABASE_URL`: PostgreSQL connection URI string.
- `OPENAI_API_KEY` / `GEMINI_API_KEY`: LLM provider API credentials.

### 2. Client-Exposed Environment Variables (Public)

- `NEXT_PUBLIC_MAPBOX_TOKEN`: Mapbox GL public map access token.
- `NEXT_PUBLIC_API_BASE_URL`: Public REST backend endpoint (e.g. `http://localhost:8000`).
