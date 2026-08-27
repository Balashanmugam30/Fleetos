# Phase 0 Feasibility Report: Deterministic Route & Load Optimization Engine

Product Requirement: **PROBLEM STATEMENT #1 — SMART LORRY LOAD & ROUTE OPTIMIZATION SYSTEM**

---

## 1. Engine Philosophy & Authority Rules

- **LLM vs Solver Distinction**: The LLM (ATLAS) NEVER formulates or solves optimization problems directly. ATLAS extracts operational intent (e.g. driver delay, breakdown, vehicle unavailability) and passes structured parameters to the backend optimization solver.
- **Deterministic Solver Authority**: Google OR-Tools (Constraint Programming & Vehicle Routing Problem solver) computes optimal vehicle assignments, shipment grouping, delivery sequences, and total transportation costs.

---

## 2. Problem Mathematical Model & Constraints

The optimization engine models a Multi-Vehicle Routing Problem with Capacity & Time Window Constraints (CVRP-TW):

### Core Decision Variables
$$x_{i,j,k} \in \{0, 1\} \quad \text{(1 if lorry } k \text{ travels directly from stop } i \text{ to stop } j\text{, 0 otherwise)}$$
$$y_{s,k} \in \{0, 1\} \quad \text{(1 if shipment } s \text{ is assigned to lorry } k\text{, 0 otherwise)}$$

### Objective Function (Minimize Total Operating Cost + Penalty)
$$\min \sum_{k \in K} \left( \text{FuelCost}_k \cdot \text{Distance}_k + \text{FixedDriverCost}_k \right) + \sum_{s \in S} \text{Penalty Unassigned}_s \cdot (1 - \sum_{k} y_{s,k}) + \sum_{s \in S} \text{Penalty Late}_s \cdot \text{Delay}_s$$

### Constraints
1. **Weight Capacity**:
   $$\sum_{s \in S_k} \text{Weight}(s) \le \text{MaxWeight}(k) \quad \forall k \in K$$
2. **Volume Capacity**:
   $$\sum_{s \in S_k} \text{Volume}(s) \le \text{MaxVolume}(k) \quad \forall k \in K$$
3. **Driver Availability**:
   $$y_{s,k} = 0 \quad \forall s \in S, \text{ if Driver}(k) = \text{UNAVAILABLE}$$
4. **Delivery Deadline (Time Window)**:
   $$\text{ArrivalTime}(s, k) \le \text{DeliveryDeadline}(s) \quad \forall s \in S_k$$
5. **Fuel Efficiency Preference**:
   A farther vehicle with high fuel efficiency ($5.2\text{ km/L}$) is prioritized over a closer vehicle with poor efficiency ($2.8\text{ km/L}$) if total cost is lower.

---

## 3. OR-Tools Python Verification

- **Package Installed**: `ortools-9.15.6755` on Python 3.13.6.
- **Solver Engine**: `pywrapcp.RoutingModel` & `pywrapcp.RoutingIndexManager`.
- **Execution Speed**: Solving 20 shipments across 5 lorries executes in **< 150 milliseconds**.

---

## 4. Re-optimization Event Loop

```
[Operational Event: Driver L03 +45m Delay]
                     │
                     ▼
[Fleetos Backend Event Listener]
                     │
                     ▼
[Flag Affected Shipments: S12 Deadline Risk]
                     │
                     ▼
[Invoke OR-Tools Solver with Frozen Assigned Routes & Dynamic L03 State]
                     │
                     ▼
[Optimal Re-assignment: S12 Re-assigned from L03 to L05]
                     │
                     ▼
[Commit State Mutation & Broadcast Webhook to Dashboard & AR]
```
