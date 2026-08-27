# Fleetos Anchor Moment Blueprint: "The Truck Tells Fleetos It Has a Problem"

Product Name: **Fleetos**  
Core Principle: **SEE → HEAR → THINK → OPTIMIZE → ACT → UPDATE**

---

## 1. The Core Narrative

In traditional logistics control towers, vehicle delays are discovered hours after they happen, leading to missed delivery deadlines, wasted driver shifts, and inflated fuel costs.

**Fleetos introduces a continuous multimodal feedback loop:**
When a vehicle encounters an operational disruption (loading delay, traffic congestion, driver unavailability), the truck directly triggers Fleetos re-optimization via real-time PSTN AI voice interaction and visual AR confirmation.

---

## 2. Step-by-Step Anchor Moment Execution Script

### Phase 1: Visual Scanning (SEE)
- **Action**: User opens Fleetos AR View on mobile device or web browser and points camera at Lorry L03 marker.
- **Visual**: AR View identifies target `L03` instantaneously. Visual floating HUD card anchors above the lorry model.
- **HUD Data**: Displays Lorry ID `L03`, Driver `Rajesh`, Assigned Shipment `S12` (Deadline: 18:00 IST), Status: `EN_ROUTE`.

### Phase 2: Telephony Interaction (HEAR)
- **Action**: Fleetos triggers outbound PSTN telephone call to Driver Rajesh (+91XXXXXXXXXX).
- **Physical Device**: Physical mobile phone rings. User/Tester answers.
- **Audio Conversation**:
  - **ATLAS**: *"Hello Rajesh, this is ATLAS from Fleetos. Are you on schedule for Shipment S12?"*
  - **Driver (User)**: *"No, loading at Chennai terminal is delayed by 45 minutes."*
  - **ATLAS**: *"Understood. Recording a 45-minute loading delay for Lorry L03."*

### Phase 3: Intelligence & Re-optimization (THINK → OPTIMIZE)
- **Backend Action**: ATLAS executes tool call `report_delay(lorry_id="L03", delay_minutes=45, reason="loading_delay")`.
- **Constraint Check**: Fleetos predicts L03 arrival at 18:15 IST (DEADLINE VIOLATION for S12!).
- **OR-Tools Solver**: Deterministically solves VRP. Identifies Lorry L05 (Driver Karthik, 5.2 km/L, available in Vellore) as optimal replacement vehicle.
- **Reassignment**: Shipment S12 reassigned from L03 to L05. Zero deadline violations!

### Phase 4: Multimodal Synchronized Update (ACT → UPDATE)
- **PSTN Confirmation**: ATLAS calls Driver Karthik (L05) confirming new assignment.
- **Web Command Dashboard**: The live vector map updates the route line for S12 from L03 to L05. Timeline logs the complete event sequence.
- **AR Experience**: The floating AR card on L03 dynamically turns yellow/red with badge: `S12 REASSIGNED TO L05 DUE TO DELAY`.
- **Result**: The audience witnesses a live phone call trigger a deterministic backend solver re-assignment, reflected in real-time on both map and camera overlays!
