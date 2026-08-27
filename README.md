# FLEETOS — Agentic Multimodal Fleet Intelligence Platform

Product Definition: *Fleetos is an agentic multimodal fleet intelligence platform that optimizes lorry assignments and delivery routes, tracks fleet movement, continuously reacts to operational changes, communicates with drivers through a real telephone-based AI voice agent, and uses computer vision and augmented reality to visualize fleet state in the physical world.*

Short Tagline: *Fleetos doesn't just plan the trip. It watches the fleet, listens to the drivers, and changes the plan when reality changes.*

Core Operational Loop: **SEE → HEAR → THINK → OPTIMIZE → ACT → UPDATE**  
Voice Agent: **ATLAS**  
Anchor Moment: **THE TRUCK TELLS FLEETOS IT HAS A PROBLEM.**  
Hackathon Target: **Problem Statement #1 — Smart Lorry Load & Route Optimization System**

---

## 1. System Overview & Key Features

- **Fleet Control Tower Dashboard**: Bright, modern enterprise logistics interface (`apps/web`) presenting real-time vehicle routes, load capacities, delivery deadlines, and event streams.
- **ATLAS AI Voice Telephony**: Outbound PSTN phone call gateway via Vapi & Twilio connecting ATLAS directly to physical mobile phones (`+91`) for driver status updates.
- **Deterministic Optimization Engine**: Powered by Google OR-Tools CP-SAT VRP solver (`services/optimizer`) for load allocation, capacities, fuel efficiency (km/L), and deadline risk minimization.
- **Cinemorph-Inspired AR View**: Real-time camera overlay anchoring fleet telemetry and risk indicators onto physical lorry targets (`apps/ar` & `apps/web/ar`).

---

## 2. Monorepo Repository Structure

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

---

## 3. Quick Start & Local Development

See the [Local Setup Guide](docs/development/local-setup.md) for full instructions.

```bash
# 1. Install Monorepo dependencies
pnpm install

# 2. Run FastAPI Backend Server (Port 8000)
pnpm dev:api

# 3. Run Web Command Tower (Port 3000)
pnpm dev:web
```

---

## 4. Master Phase Status Matrix

See [`PHASE_STATUS.md`](PHASE_STATUS.md) for master phase governance and detailed component readiness tables.
