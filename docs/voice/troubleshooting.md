# Fleetos Voice Agent Troubleshooting & Diagnostics Guide

Product: **Fleetos**

---

## Diagnostic Checklist & Solutions

### 1. `VAPI_API_KEY` or `VAPI_PHONE_NUMBER_ID` Missing
- **Symptom**: `GET /api/v1/voice/health` shows `"configured": false`, `mode: "DEMO"`.
- **Solution**: Add valid Vapi credentials to `.env` file and restart server.

### 2. Active Call Conflict (`HTTP 409 CONFLICT`)
- **Symptom**: `Driver D03 already has an active call in progress.`
- **Solution**: Wait for active call to transition to `COMPLETED` / `FAILED` or complete call lifecycle.

### 3. Public Webhook URL Configuration
- **Symptom**: Tool execution callbacks do not reach local FastAPI server.
- **Solution**: Launch an HTTPS tunnel (e.g. `ngrok http 8000`), update `VOICE_WEBHOOK_BASE_URL` in `.env`, and configure Vapi server URL.

### 4. Indian Mobile Calling (+91) Restrictions
- **Symptom**: Twilio/Vapi call fails on outbound dispatch to +91 numbers.
- **Solution**: Ensure Twilio account Geo Permissions include India (+91), caller ID is verified, and number format uses E.164 (`+91XXXXXXXXXX`).
