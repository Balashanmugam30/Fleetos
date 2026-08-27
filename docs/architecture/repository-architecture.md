# Fleetos Repository Monorepo Architecture

Product: **Fleetos**

---

## Service Boundaries & Monorepo Structure

```
Fleetos Monorepo
├── apps/
│   ├── web/                      # Next.js 15 Web Command Tower & WebAR Overlay
│   └── ar/                       # Swift / ARKit / RealityKit Native iOS App
├── services/
│   ├── api/                      # FastAPI Gateway & Vapi Telephony Webhook Router
│   ├── optimizer/                # Google OR-Tools VRP Solver Module
│   ├── agent/                    # ATLAS AI Voice Agent Tool Registry & Intent Handler
│   ├── voice/                    # Vapi / Twilio Telephony Provider Adapters
│   ├── events/                   # Operational Event Taxonomy & Payload Definitions
│   ├── vision/                   # OpenCV & Document OCR Recognition Interfaces
│   └── tracking/                 # Backend GPS Telemetry & Simulation Provider
├── database/
│   ├── schema/                   # PostgreSQL DDL Schemas
│   └── seed/                     # Canonical Seed Fixtures (L01-L05, S01-S12)
├── shared/
│   └── types/                    # Shared TypeScript Domain Data Contracts
├── docs/                         # Architecture & Developer Documentation
└── scripts/                      # Developer Setup & Demo Control Scripts
```
