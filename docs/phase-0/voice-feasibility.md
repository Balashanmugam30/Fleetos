# Phase 0 Feasibility Report: Real Mobile Phone Telephony & Outbound Voice Calling

Product Requirement: **REAL OUTBOUND TELEPHONE CALL TO PHYSICAL MOBILE PHONE**  
Target Voice Agent: **ATLAS** (Fleetos Multimodal Operational Logistics Agent)

---

## 1. Intended Telephony Architecture

```
Fleetos Backend (FastAPI)
   │ (Trigger outbound call via POST /call)
   ▼
Vapi AI REST API (api.vapi.ai/call)
   │ (SIP / Telephony Bridge)
   ▼
Twilio PSTN Gateway
   │ (Carrier Interconnect)
   ▼
Indian PSTN / Carrier Network
   │ (Ring Physical Phone)
   ▼
Driver Physical Mobile Device (+91XXXXXXXXXX)
   │ (Real-Time Audio Stream)
   ▼
Vapi Audio Pipeline (STT → LLM ATLAS → TTS)
   │ (Tool Call triggered during conversation)
   ▼
Vapi Custom Tool Webhook (POST to Fleetos Server URL)
   │ (Process delay event & re-optimize)
   ▼
Fleetos Optimization Engine & Database State Update
```

---

## 2. Official API & Configuration Requirements

### Vapi Outbound API Endpoint (`POST https://api.vapi.ai/call`)
```json
{
  "assistantId": "ast_atlas_fleetos_01",
  "phoneNumberId": "phone_twilio_vapi_01",
  "customer": {
    "number": "+919876543210",
    "name": "Driver Rajesh"
  },
  "assistantOverrides": {
    "variableValues": {
      "lorry_id": "L03",
      "assigned_shipments": "S12, S04"
    }
  }
}
```

### Vapi Custom Server URL (Tool Call Integration)
When ATLAS invokes a tool (e.g. `report_delay`), Vapi sends an HTTP POST request to Fleetos backend:
```json
{
  "message": {
    "type": "tool-calls",
    "toolCalls": [
      {
        "id": "call_123",
        "function": {
          "name": "report_delay",
          "arguments": {
            "lorry_id": "L03",
            "delay_minutes": 45,
            "reason": "loading_delay"
          }
        }
      }
    ]
  }
}
```

---

## 3. Regulatory & Carrier Analysis: India (+91 PSTN)

1. **Twilio India Outbound Policy**:
   - Outbound calls to Indian mobile numbers (+91) via Twilio must originate from an authorized international (e.g., US/UK) number or an approved Indian telemarketing series number.
   - **Twilio Geo-Permissions**: International Outbound Calling to India must be explicitly enabled in the Twilio Console.
2. **Trial Account Restrictions**:
   - For trial accounts (Twilio / Vapi), target Indian mobile numbers must be pre-added to **Twilio Verified Caller IDs**.
3. **TRAI / UCC Regulations**:
   - Automated voice calls must comply with Telecom Regulatory Authority of India (TRAI) guidelines regarding Unsolicited Commercial Communications (UCC). For operational driver dispatch calls, explicit driver opt-in context is established.
4. **Estimated Costs**:
   - Vapi AI Telephony: ~$0.05 / minute.
   - Twilio PSTN Outbound Call to India: ~$0.03 – $0.10 / minute.
   - Total Estimated Call Cost: ~$0.08 – $0.15 / minute.

---

## 4. Feasibility Status Assessment

| Feasibility Criterion | Status | Empirical / Regulatory Evidence |
| :--- | :--- | :--- |
| **Vapi REST API Outbound Support** | `VERIFIED` | Vapi official docs (`POST /call` with `phoneNumberId` & `customer.number`). |
| **Vapi Custom Tool Webhooks** | `VERIFIED` | Vapi Server URL tool calls post structured JSON to backend endpoints. |
| **PSTN Calling to Indian Mobile (+91)** | `PARTIALLY VERIFIED` | Architecturally valid via Twilio international PSTN routing. Requires user account keys & verified destination number. |
| **Real-time Two-way AI Conversation** | `VERIFIED` | Vapi WebRTC / SIP pipeline supports ultra-low latency STT-LLM-TTS. |

---

## 5. Controlled Validation Protocol

To run a minimal live test during development:
1. Populate `VAPI_API_KEY`, `VAPI_PHONE_NUMBER_ID`, `VAPI_ASSISTANT_ID`, and `TWILIO_ACCOUNT_SID` in `.env`.
2. Ensure target test mobile number is added to Twilio Verified Caller IDs.
3. Trigger test call script: `python scripts/test_voice_call.py --phone +91XXXXXXXXXX`.
4. Confirm:
   - Physical phone rings.
   - Two-way voice audio functions.
   - ATLAS interprets delay input ("45 minutes late").
   - Backend webhook receives `report_delay` tool call.

---

## 6. Fallback Hierarchy

- **LEVEL 1 (Primary Target)**: Real Vapi → Twilio → Indian Mobile PSTN call.
- **LEVEL 2 (Alternative Telephony)**: Real Vapi call using alternate verified telephony provider / local SIP trunk.
- **LEVEL 3 (Demo Simulator)**: Clearly labeled Interactive Audio / Event Flow Simulator in the Web Dashboard (strictly labeled as Demo Simulator, never pretended to be PSTN).
