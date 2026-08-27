# Fleetos Augmented Reality (AR) Implementation Plan

Product Name: **Fleetos**  
Design Inspiration: **Cinemorph AR Experience Framework**

---

## 1. Dual-Path Implementation Architecture

```
                                  FLEETOS AR VISUALIZER
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    ▼                                               ▼
         Native iOS AR Target                              WebAR Browser Target
         (`apps/ar` Monorepo App)                       (`apps/web/ar` Web Component)
   - Swift 5 / ARKit / RealityKit                 - Next.js / MindAR / Three.js
   - Target: iOS ARKit Reference Image            - Target: Web Camera Marker Tracking
   - Output: 3D RealityKit Entity                 - Output: HTML5 / WebGL Floating HUD Card
```

---

## 2. Anchor Marker & Data Overlay Blueprint

### Anchor Target Images
1. **Lorry Marker L03**: Printed AR Reference Image / Vehicle Side Plate (`L03_Reference_Marker.png`).
2. **Shipment Label S12**: Pallet QR/Barcode Reference Target (`S12_Pallet_Marker.png`).

### Visual AR Cards Rendered on Anchor

```
┌────────────────────────────────────────────────────────┐
│  🚛 FLEETOS OPERATIONAL TELEMETRY                     │
├────────────────────────────────────────────────────────┤
│  Lorry ID: L03                                        │
│  Driver: Rajesh (+91-98765-XXXXX)                     │
│  Weight Capacity: 4,500 / 8,000 kg  [████████░░░] 56%  │
│  Volume Capacity: 18.0 / 35.0 m^3   [█████░░░░░] 51%  │
│  Assigned Shipments: S12 (Strict 18:00 IST Deadline)  │
│                                                        │
│  [STATUS BADGE]: 🟡 DELAYED (+45m)                    │
│  [OPTIMIZATION ACTION]: 🔴 S12 REASSIGNED TO L05       │
└────────────────────────────────────────────────────────┘
```

---

## 3. WebAR Component Implementation (`apps/web/ar/page.tsx`)

```tsx
"use client";

import React, { useEffect, useRef, useState } from "react";

export default function ARCameraOverlay() {
  const [detectedTarget, setDetectedTarget] = useState<string | null>(null);
  const [fleetData, setFleetData] = useState<any>(null);

  useEffect(() => {
    // MindAR / Three.js initialization and target tracking setup
  }, []);

  return (
    <div className="relative w-full h-screen bg-black overflow-hidden">
      {/* Live Video Viewfinder */}
      <video id="ar-viewfinder" className="absolute inset-0 w-full h-full object-cover" autoPlay playsInline muted />

      {/* Floating AR HUD Overlay */}
      {detectedTarget && fleetData && (
        <div className="absolute top-12 left-6 right-6 p-4 bg-black/80 backdrop-blur-md rounded-xl border border-cyan-500/40 text-white shadow-2xl animate-fade-in">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-cyan-400">LORRY TARGET: {detectedTarget}</h2>
            <span className="px-3 py-1 bg-amber-500/20 text-amber-400 text-xs font-semibold rounded-full border border-amber-500/40">
              {fleetData.status}
            </span>
          </div>
          <p className="text-sm text-gray-300 mt-2">Driver: {fleetData.driverName}</p>
          <p className="text-xs text-gray-400 mt-1">Assigned: {fleetData.assignedShipments.join(", ")}</p>
        </div>
      )}
    </div>
  );
}
```
