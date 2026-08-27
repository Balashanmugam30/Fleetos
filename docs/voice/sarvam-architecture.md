# Fleetos Sarvam Voice Agents Integration Architecture

Product: **Fleetos** (Agentic Multimodal Fleet Intelligence Platform)  
Voice Agent: **ATLAS**  
Phase: **Phase 6 — Multilingual Indian-Language AI Telephone Operations**

---

## High-Level System Architecture

Fleetos uses **Sarvam Voice Agents** as its primary conversational AI intelligence layer, paired with **Twilio Telephony** for PSTN mobile calls to drivers and **Fleetos Operational Tools** for real-time fleet state mutation.

```
┌─────────────────────────┐       ┌─────────────────────────┐       ┌─────────────────────────┐
│     Fleetos Web UI      │ ────> │  FastAPI Voice Router   │ ────> │    Sarvam Voice API     │
│   (/ai Ops Center)      │       │ (/api/v1/voice/calls)   │       │ (Voice Agent Campaign)  │
└─────────────────────────┘       └─────────────────────────┘       └────────────┬────────────┘
                                                                                 │
                                                                                 ▼
┌─────────────────────────┐       ┌─────────────────────────┐       ┌─────────────────────────┐
│   Driver Mobile Phone   │ <───> │ Twilio PSTN Telephony   │ <───> │ Sarvam Indic AI Engine  │
│  (+91... Tamil/Hindi/En)│       │   (Outbound Calling)    │       │ (ASR/TTS/NLU Reasoning) │
└─────────────────────────┘       └─────────────────────────┘       └────────────┬────────────┘
                                                                                 │
                                                                                 ▼
                                                                    ┌─────────────────────────┐
                                                                    │   Fleetos Sarvam Tool   │
                                                                    │    API Endpoint (POST   │
                                                                    │  /sarvam/tools/report)  │
                                                                    └────────────┬────────────┘
                                                                                 │
                                                                                 ▼
                                                                    ┌─────────────────────────┐
                                                                    │  Fleetos Event Ledger   │
                                                                    │(DRIVER_DELAY_REPORTED)  │
                                                                    └─────────────────────────┘
```

---

## Architectural Responsibility Separation

1. **Fleetos Core Platform**:
   - Master authority for Driver, Lorry, Shipment, Route, and Optimization state.
   - Executes operational tools via `services/agent/tool_executor.py`.
   - Records immutable audit events in the `events` table (`DRIVER_DELAY_REPORTED`).

2. **Sarvam Voice Agents**:
   - Handles Indic speech recognition (ASR), natural language understanding (NLU), turn-taking, code-mixing, and text-to-speech (TTS).
   - Triggers Fleetos API tools over HTTPS when drivers report operational updates.

3. **Twilio Telephony**:
   - Connects PSTN telephone calls between Sarvam Voice Agent and driver mobile phones (+91...).
