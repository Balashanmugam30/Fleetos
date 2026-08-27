# Phase 0 Technology Stack & Decision Matrix

Product Name: **Fleetos**

---

## Technology Stack Decision Matrix

| Technology | Purpose | Preferred Choice | Alternative Choice | Environment Availability | Verified | Identified Risk | Cost Model | Architectural Decision & Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Web Dashboard** | Command & Control Tower UI | **Next.js 15 (React 19)** | Vite + React | `Node v22.20.0` | `VERIFIED` | SSR Complexity | Open Source | Next.js App Router for fast UI rendering, Tailwind CSS, shadcn/ui. |
| **Frontend Styling** | UI Components & Theme | **Tailwind CSS + shadcn/ui** | Chakra UI / Material UI | `npm / pnpm` | `VERIFIED` | Styling bloat | Open Source | Clean component architecture and rapid prototyping. |
| **Backend API** | REST / Webhook Gateway | **FastAPI (Python 3.13)** | Node.js Express | `Python 3.13.6` | `VERIFIED` | Async loop blocking | Open Source | FastAPI integrates directly with Python OR-Tools solver. |
| **Optimization Solver** | Lorry assignment & VRP | **Google OR-Tools 9.15** | SciPy / Custom Greedy | `pip ortools` | `VERIFIED` | Non-linear constraints | Open Source | Industry-standard OR-Tools Routing Solver / RoutingModel for vehicle routing. |
| **Database & Auth** | Operational State Persistence | **PostgreSQL / Supabase** | SQLite / Redis | `Python SQLAlchemy` | `VERIFIED` | Network latency | Free Tier | Canonical structured storage for Lorries, Drivers, Routes, Events. |
| **AI Voice Telephony** | Driver PSTN Calling Agent | **Vapi AI** | Retell AI / Bland AI | `Vapi REST API` | `PARTIALLY VERIFIED` | PSTN latency / India TRAI | ~$0.05/min | Native tool call webhooks and turn-key outbound telephony. |
| **Telephony Gateway** | PSTN Trunking to India | **Twilio Voice** | Exotel / Local SIP | `Twilio API` | `PARTIALLY VERIFIED` | Carrier verification | ~$0.05-0.10/min | Twilio international outbound routing to Indian PSTN (+91). |
| **Agent LLM Engine** | Intent Extraction & Tool Routing | **OpenAI GPT-4o / Gemini 1.5** | Claude 3.5 Sonnet | `Requests / SDK` | `VERIFIED` | Tool call hallucinations | Usage-based | High structured output accuracy for JSON tool calls. |
| **Augmented Reality (iOS)** | Native Mobile AR View | **Swift / ARKit / RealityKit** | WebAR Fallback | `apps/ar repo target` | `STRUCTURED` | Requires Mac to compile | Open Source | Dedicated iOS native project folder structured in monorepo. |
| **Augmented Reality (Web)** | Cross-platform Browser AR | **MindAR + Three.js** | 8th Wall | `apps/web/ar` | `VERIFIED` | Browser camera permission | Open Source | Zero-install web browser AR camera tracking overlay. |
| **Computer Vision** | Reference Marker Tracking | **OpenCV 4.12** | Roboflow / YOLO | `Python cv2` | `VERIFIED` | Lighting sensitivity | Open Source | Robust reference target identification and marker detection. |
| **Mapping & GIS** | Map rendering & Route Visualization | **Mapbox GL JS + Turf.js** | Leaflet / OpenStreetMap | `npm package` | `VERIFIED` | API rate limits | Free Tier | Interactive web vector maps with deterministic Haversine fallback. |
