# Fleetos RoutingModel Specification

Engine: **Google OR-Tools Routing Solver / RoutingModel**

---

## 1. Node Mapping Strategy
- Depots: `0 .. num_vehicles - 1`
- Pickups: `num_vehicles .. num_vehicles + num_shipments - 1`
- Deliveries: `num_vehicles + num_shipments .. num_vehicles + 2 * num_shipments - 1`

## 2. Constraint Hierarchy
1. **Weight Capacity Dimension**: Enforces concurrent peak weight load $\le \text{max\_weight\_kg}$.
2. **Volume Capacity Dimension**: Enforces concurrent peak volume load $\le \text{max\_volume\_m3}$.
3. **Time Dimension**: Enforces pickup-before-delivery ordering and delivery deadlines.
4. **Disjunction Penalties**: Scaled penalties (`100,000,000 + priority_weight * 10,000`) ensuring feasible shipments are served over dropping.

## 3. Nearest-Lorry Trap Resolution
Vehicles with superior fuel efficiency (e.g. L05 @ 5.2 km/L in Vellore) are deterministically selected over closer vehicles (e.g. L01 @ 3.5 km/L in Bengaluru) when total operating cost is lower.
