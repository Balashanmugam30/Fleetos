# Vapi & Twilio PSTN Telephony Plan: Real Outbound Calling Architecture

Product Name: **Fleetos**  
Target Voice Agent: **ATLAS**

---

## 1. System Integration Flow

```
1. Fleetos Backend Event/API Trigger
   └── POST https://api.vapi.ai/call
       Headers: { Authorization: "Bearer VAPI_API_KEY" }
       Body: {
         assistantId: "ast_atlas_01",
         phoneNumberId: "phone_twilio_01",
         customer: { number: "+919876543210" }
       }

2. Vapi Telephony Bridge ──> Twilio SIP Gateway ──> Indian Mobile (+91) Phone Rings

3. Driver answers ──> WebRTC Audio Stream between Driver & Vapi Speech Pipeline

4. Driver says: "I will be 45 minutes late due to loading."

5. Vapi Assistant triggers Tool Call ──> HTTP POST to Fleetos Server URL:
   POST https://<public-backend-url>/api/v1/voice/vapi-webhook
   Body: {
     message: {
       type: "tool-calls",
       toolCalls: [{
         function: {
           name: "report_delay",
           arguments: { lorry_id: "L03", delay_minutes: 45, reason: "loading_delay" }
         }
       }]
     }
   }

6. Fleetos FastAPI Webhook:
   - Validates webhook request headers
   - Executes OR-Tools VRP Solver re-optimization
   - Updates PostgreSQL Database state
   - Emits real-time WebSocket broadcast to Web Dashboard and AR HUD
   - Returns tool response payload back to Vapi:
     { results: [{ toolCallId: "call_123", result: "Reassignment successful. Shipment S12 moved to Lorry L05." }] }

7. Vapi ATLAS speaks response to driver:
   "Thank you Rajesh. Fleetos has reassigned Shipment S12 to Lorry L05 to protect the delivery deadline."
```

---

## 2. Server URL Webhook Code Architecture (`services/api/voice/router.py`)

```python
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import logging

router = APIRouter(prefix="/api/v1/voice", tags=["Voice Telephony"])

@router.post("/vapi-webhook")
async def handle_vapi_webhook(request: Request):
    payload = await request.json()
    message_type = payload.get("message", {}).get("type")
    
    if message_type == "tool-calls":
        tool_calls = payload["message"]["toolCalls"]
        results = []
        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            args = tool_call["function"]["arguments"]
            
            if function_name == "report_delay":
                # Execute delay handling logic
                result = handle_report_delay(args["lorry_id"], args["delay_minutes"], args.get("reason"))
                results.append({"toolCallId": tool_call["id"], "result": result})
                
        return {"results": results}
        
    return {"status": "acknowledged"}
```

---

## 3. Environment Secrets Required

- `VAPI_API_KEY`: Vapi platform API authentication token.
- `VAPI_PHONE_NUMBER_ID`: Provisioned Vapi phone number object ID.
- `VAPI_ASSISTANT_ID`: ATLAS assistant configuration ID.
- `TWILIO_ACCOUNT_SID`: Twilio account identifier.
- `TWILIO_AUTH_TOKEN`: Twilio account auth token.
- `PUBLIC_API_BASE_URL`: Public HTTPS backend URL (e.g., ngrok or Vercel tunnel) for Vapi Server URL callbacks.
