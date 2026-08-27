# Fleetos Vapi + Twilio PSTN Integration Guide

Product: **Fleetos**  
Module Boundary: `services/voice/vapi.py`

---

## Configuration Setup (.env)
```env
# Telephony Credentials (Keep in local .env only)
VAPI_API_KEY=your_vapi_private_api_key
VAPI_PHONE_NUMBER_ID=your_vapi_phone_number_id
VAPI_ASSISTANT_ID=your_vapi_assistant_id
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+91XXXXXXXXXX
VOICE_WEBHOOK_BASE_URL=https://your-public-tunnel-host.ngrok-free.app
VOICE_PROVIDER=vapi
```

---

## Outbound Dispatch Sequence
1. Dispatcher initiates call via `POST /api/v1/voice/calls`.
2. `VapiVoiceProvider` formats JSON payload:
   ```json
   {
     "phoneNumberId": "VAPI_PHONE_NUMBER_ID",
     "customer": { "number": "+919876543210", "name": "Driver D03" },
     "assistantId": "VAPI_ASSISTANT_ID",
     "assistantOverrides": {
       "variableValues": {
         "driver_id": "D03",
         "lorry_id": "L03",
         "call_type": "STATUS_CHECK"
       }
     }
   }
   ```
3. Dispatches HTTP POST to `https://api.vapi.ai/call/phone` with `Authorization: Bearer VAPI_API_KEY`.
4. Twilio gateway routes call to driver's physical mobile phone (+91).
5. Tool execution callbacks hit `POST /api/v1/voice/webhooks/vapi`.
