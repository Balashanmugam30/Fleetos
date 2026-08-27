# ATLAS Operational AI Voice Agent Architecture

Product: **Fleetos** (Agentic Multimodal Fleet Intelligence Platform)  
Voice Agent Name: **ATLAS**  
Module Boundaries: `services/voice`, `services/agent`

---

## 1. System Architecture & Component Flow

```
HUMAN DRIVER / DISPATCHER
         │
    (PSTN Phone Call)
         │
   Vapi + Twilio Gateway
         │
   (HTTP Webhook Callbacks)
         │
FastAPI Voice Router (/api/v1/voice)
         │
   VoiceService & Normalizer
         │
   ATLAS ToolExecutor Engine
         │
  ┌──────┴────────┬──────────────┐
  │               │              │
Database     Event System    Tracking Engine
(CallRecord) (DRIVER_DELAY)  (L01-L05 State)
```

---

## 2. Core Components
- **`services/voice/config.py`**: Manages environment variables (`VAPI_API_KEY`, `VAPI_PHONE_NUMBER_ID`, `VAPI_ASSISTANT_ID`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`).
- **`services/voice/models.py`**: Standardized schemas for call records and outbound requests.
- **`services/voice/provider.py`**: Abstract `VoiceProvider` interface with `VapiVoiceProvider` and `DemoVoiceProvider`.
- **`services/voice/vapi.py`**: Real Vapi REST API outbound calling adapter (`POST https://api.vapi.ai/call/phone`).
- **`services/voice/simulator.py`**: Offline demo simulator provider.
- **`services/voice/webhooks.py`**: Normalizes status events (`CALL_STARTED`, `CALL_COMPLETED`, etc.) and processes tool call execution.
- **`services/voice/service.py`**: Master orchestrator enforcing 1 active call per driver throttling and call history persistence.
- **`services/agent/tool_registry.py`**: Declarative tool function schemas (`get_fleet_status`, `report_delay`, `report_breakdown`, `confirm_delivery`, `explain_assignment`).
- **`services/agent/tool_executor.py`**: Validated tool execution engine creating operational events.
