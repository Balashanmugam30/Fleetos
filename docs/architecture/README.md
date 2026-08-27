# FLEETOS System Architecture & Design Specification

Product Name: **Fleetos**  
Product Definition: *Fleetos is an agentic multimodal fleet intelligence platform that optimizes lorry assignments and delivery routes, continuously reacts to operational changes, communicates with drivers through a real telephone-based AI voice agent, and uses computer vision and augmented reality to visualize fleet state in the physical world.*

Short Tagline: *Fleetos is a logistics control system that does not just plan the route — it keeps the fleet optimized when reality changes.*

Core Principle: **SEE → HEAR → THINK → OPTIMIZE → ACT → UPDATE**

---

## 1. System Architecture Diagram

```
                FLEETOS
                   |
    +--------------+---------------+
    |              |               |
    v              v               v
Dashboard       ATLAS          AR/Vision
Control Tower   Voice AI       Experience
    |              |               |
    +--------------+---------------+
                   |
                   v
            Agent Orchestrator
                   |
          +--------+--------+
          |                 |
          v                 v
    Event Intelligence   Fleet Tools
          |                 |
          +--------+--------+
                   |
                   v
          Optimization Engine
                   |
         +---------+---------+
         |         |         |
         v         v         v
     Assignment  Grouping  Routing
         |         |         |
         +---------+---------+
                   |
              Cost / ETA / Risk
                   |
                   v
               Fleet State
```

---

## 2. Core Authority Boundaries & Directives

1. **LLM is NOT the Authoritative Optimizer**: Natural language models interpret operational context, extract structured arguments, invoke backend tools, and summarize operational states for human drivers and dispatchers. LLMs do not calculate optimal VRP routes or invent assignments.
2. **Database is Authoritative for State**: PostgreSQL / Supabase stores canonical representations of Lorries, Drivers, Shipments, Routes, Events, Calls, and Optimization Runs.
3. **Optimization Engine is Authoritative for Route/Assignment Decisions**: Google OR-Tools deterministically computes feasible, cost-minimal vehicle routing solutions subject to weight, volume, time window, driver availability, and fuel constraints.
4. **Voice Agent (ATLAS) is an Interface/Action Orchestrator**: ATLAS executes tool calls back into Fleetos backend webhooks and triggers state mutations subject to backend validation.
5. **AR is a Real-World Visualization/Interface Layer**: Augmented Reality overlays real-time backend state onto physical lorry/shipment reference targets. AR queries the exact same API as the web dashboard.

---

## 3. Directional Integration Data Flows

### Voice Flow (PSTN Telephony)
`Fleetos Backend → Vapi Outbound REST API → Telephony Gateway (Twilio) → Carrier/PSTN → Physical Mobile Phone → AI Voice Conversation (ATLAS) → Vapi Tool Call / Webhook → Fleetos Agent Webhook → OR-Tools Re-optimization → Fleet Database Mutation → Real-Time Dashboard & AR Notification`

### AR Flow (Visual Camera Overlay)
`Camera Stream → Reference Image / Marker Detection (ARKit / MindAR WebAR) → Target ID Extraction (e.g. L03) → Fleetos REST/WebSocket API → Fetch Live Fleet State → RealityKit / Three.js 3D Visual Card Overlay → Interactive Real-Time State Display`

---

## 4. Canonical Data Schemas

### Lorry
```typescript
interface Lorry {
  id: string; // e.g. "L01", "L03"
  registrationNumber: string;
  maxWeight: number; // kg
  maxVolume: number; // m^3
  currentLatitude: number;
  currentLongitude: number;
  fuelEfficiency: number; // km/L
  driverId: string | null;
  status: 'IDLE' | 'EN_ROUTE' | 'LOADING' | 'UNAVAILABLE' | 'DELAYED' | 'MAINTENANCE';
  currentRouteId: string | null;
}
```

### Driver
```typescript
interface Driver {
  id: string;
  name: string;
  phoneNumber: string; // e.g. "+91XXXXXXXXXX" (Masked in UI)
  availability: 'AVAILABLE' | 'ON_DUTY' | 'ON_BREAK' | 'UNAVAILABLE';
  currentLorryId: string | null;
}
```

### Shipment
```typescript
interface Shipment {
  id: string; // e.g. "S01", "S12"
  weight: number; // kg
  volume: number; // m^3
  pickupLocation: { address: string; lat: number; lng: number };
  destination: { address: string; lat: number; lng: number };
  deliveryDeadline: string; // ISO 8601 Timestamp
  priority: 'LOW' | 'NORMAL' | 'HIGH' | 'URGENT';
  status: 'UNASSIGNED' | 'ASSIGNED' | 'IN_TRANSIT' | 'DELIVERED' | 'REJECTED';
}
```

### Assignment
```typescript
interface Assignment {
  id: string;
  shipmentId: string;
  lorryId: string;
  sequence: number;
  reason: string;
  createdAt: string;
}
```

### Route
```typescript
interface Route {
  id: string;
  lorryId: string;
  stops: Array<{
    type: 'PICKUP' | 'DELIVERY';
    shipmentId: string;
    location: { lat: number; lng: number; address: string };
    estimatedArrival: string;
    deadline: string;
  }>;
  distanceKm: number;
  estimatedDurationMinutes: number;
  fuelEstimateLiters: number;
  costEstimate: number;
  deadlineRisk: 'NONE' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
}
```

### Event
```typescript
interface OperationalEvent {
  id: string;
  type: 'DRIVER_DELAY' | 'LOADING_DELAY' | 'VEHICLE_BREAKDOWN' | 'SHIPMENT_CANCELLED' | 'URGENT_SHIPMENT_ADDED' | 'DRIVER_UNAVAILABLE';
  lorryId: string | null;
  shipmentId: string | null;
  severity: 'INFO' | 'WARNING' | 'CRITICAL';
  timestamp: string;
  structuredPayload: Record<string, any>;
  source: 'ATLAS_VOICE' | 'DISPATCHER_WEB' | 'AR_VIEW' | 'SYSTEM_MONITOR';
  resolutionStatus: 'PENDING' | 'REOPTIMIZED' | 'RESOLVED' | 'IGNORED';
}
```

### Call
```typescript
interface PhoneCallRecord {
  id: string;
  lorryId: string | null;
  driverId: string | null;
  callType: 'OUTBOUND_DISPATCH' | 'INBOUND_REPORT' | 'REPLACEMENT_OFFER';
  direction: 'OUTBOUND' | 'INBOUND';
  status: 'QUEUED' | 'RINGING' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED' | 'NO_ANSWER';
  startedAt: string | null;
  endedAt: string | null;
  transcriptReference: string | null;
  extractedEventId: string | null;
}
```

### OptimizationRun
```typescript
interface OptimizationRun {
  id: string;
  timestamp: string;
  trigger: 'INITIAL_PLAN' | 'EVENT_DRIVER_DELAY' | 'EVENT_BREAKDOWN' | 'MANUAL_OVERRIDE';
  inputSnapshotReference: string;
  result: 'FEASIBLE' | 'OPTIMAL' | 'INFEASIBLE';
  totalCost: number;
  totalFuelLiters: number;
  deadlineViolationsCount: number;
  unassignedShipments: Array<{ shipmentId: string; reason: string }>;
}
```

### ARSession
```typescript
interface ARSession {
  id: string;
  detectedEntityId: string;
  entityType: 'LORRY' | 'SHIPMENT' | 'PALLET';
  detectionTime: string;
  currentView: 'SUMMARY' | 'LOAD_DETAILS' | 'ROUTE_RISK' | 'DRIVER_STATUS';
}
```
