# Phase 0 Feasibility Report: Augmented Reality (AR) & Computer Vision

Product Requirement: **CINEMORPH-INSPIRED LIVE CAMERA + AR ANCHORED FLEET INFORMATION**  
Target Systems: Native iOS (`apps/ar` - Swift/ARKit/RealityKit) & WebAR (`apps/web/ar` - MindAR/Three.js)

---

## 1. Cinemorph Design Philosophy Adaptation

Fleetos adapts core architectural lessons from Cinemorph:

1. **Continuous Camera View**: The camera remains active continuously; loading/processing states overlay gracefully without blocking the viewfinder.
2. **Explicit State Transitions**: Transitions (`AR_IDLE` → `SCANNING` → `IDENTIFIED` → `LOADING_STATE` → `AR_ACTIVE` → `INTERACTION`) are visual and instantaneous.
3. **Progressive Content Delivery**: Base telemetry loads instantly, followed by live backend state (re-assignments, risk scores, voice call updates).
4. **Anchor Moment Centric**: AR visualizes the core anchor moment: *"The truck tells Fleetos it has a problem."*

---

## 2. Hardware Environment Audit & Dual-Path Architecture

| Execution Environment | Tooling / Framework | Capability Status | Implementation Role |
| :--- | :--- | :--- | :--- |
| **Local Host Machine (Windows 11)** | Browser WebAR / MindAR / Three.js | `VERIFIED & OPERATIONAL` | Primary local development & cross-platform web demo |
| **iOS Mobile Device** | Swift / ARKit / RealityKit | `STRUCTURED IN REPO` | Production native iOS AR client (`apps/ar`) |

### Native iOS AR Path (`apps/ar`)
- **Technology**: Swift 5, SwiftUI, ARKit (`ARImageAnchor`), RealityKit (`Entity`, `AnchorEntity`).
- **Target Marker**: Reference Image Detection (`Fleetos_Lorry_Marker.png`, `L03_Reference.jpg`).
- **Data Binding**: Async HTTP GET `/api/v1/lorries/{lorry_id}` to fetch live backend state.

### WebAR Browser Path (`apps/web/ar`)
- **Technology**: Next.js React, MindAR / WebXR, Three.js, HTML5 Camera Stream.
- **Target Marker**: MindAR Compiled Image Target or QR/Barcode marker.
- **Data Binding**: Direct WebSocket / REST connection to Fleetos API.

---

## 3. AR State Machine & UI Lifecycle

```
[AR_IDLE] ──(User opens AR)──> [SCANNING] ──(Detect Lorry Marker L03)──> [IDENTIFIED]
                                                                            │
[AR_ACTIVE] <──(Overlay 3D Card)── [LOADING_STATE] <──(Fetch Fleet API)─────┘
     │
     ├──> [UPDATE: Driver Delayed (+45m)] ──> Animate Red Risk Indicator
     └──> [UPDATE: Reassigned S12 -> L05] ──> Animate Route Transfer Card
```

---

## 4. Feasibility Status Assessment

| Feasibility Criterion | Status | Evidence & Notes |
| :--- | :--- | :--- |
| **Marker / Reference Image Detection** | `VERIFIED` | MindAR WebAR & ARKit `ARImageAnchor` both support zero-latency 2D image target recognition. |
| **Real-time Data Binding** | `VERIFIED` | Unified API backend serves identical payload to both Web Dashboard and AR visualizers. |
| **Camera Viewfinder Non-blocking** | `VERIFIED` | WebGL canvas overlays floating HUD panels without interrupting video stream. |
| **Native iOS Build on Host Machine** | `BLOCKED (Local)` | Local Windows machine lacks Xcode CLI; `apps/ar` code target maintained cleanly in repo for iOS Xcode compilation. |

---

## 5. Fallback Hierarchy for AR

- **LEVEL 1 (Primary Native)**: Swift + ARKit + RealityKit native iOS app (`apps/ar`) running on physical iPhone.
- **LEVEL 2 (Primary Web)**: WebAR Live Camera view with MindAR / Three.js 3D tracking inside `apps/web/ar`.
- **LEVEL 3 (Interactive Camera Simulator)**: Live camera feed with bounding box HUD overlay in Web Dashboard.
