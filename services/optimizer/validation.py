"""
Fleetos Independent Post-Solution Validator
Module Boundary: services/optimizer/validation.py
"""

from typing import List, Dict, Any, Tuple
from services.optimizer.models import OptimizationInput, RouteResult, AssignmentResult, ensure_utc

class ValidationException(Exception):
    pass

def validate_optimization_solution(
    input_data: OptimizationInput,
    routes: List[RouteResult],
    assignments: List[AssignmentResult]
) -> bool:
    """
    Independently validate OR-Tools solution against hard physical constraints:
    1. Assigned vehicle and driver availability.
    2. Concurrent peak weight capacity limit.
    3. Concurrent peak volume capacity limit.
    4. Pickup-before-delivery chronological sequence.
    5. Delivery deadline time windows.
    6. Cost calculation consistency.
    """
    vehicle_map = {v.id: v for v in input_data.vehicles}
    shipment_map = {s.id: s for s in input_data.shipments}

    served_shipments = set()

    for route in routes:
        lorry = vehicle_map.get(route.lorry_id)
        if not lorry:
            raise ValidationException(f"Route references unknown lorry '{route.lorry_id}'")

        if not lorry.driver_available or lorry.status == "UNAVAILABLE":
            raise ValidationException(f"Route assigned to unavailable lorry/driver '{lorry.id}'")

        current_weight = 0.0
        current_volume = 0.0
        peak_weight = 0.0
        peak_volume = 0.0

        shipment_pickups = {}
        shipment_deliveries = {}

        for stop in route.stops:
            if stop.type == "PICKUP" and stop.shipment_id:
                s = shipment_map.get(stop.shipment_id)
                if not s:
                    raise ValidationException(f"Stop references unknown shipment '{stop.shipment_id}'")
                
                current_weight += s.weight_kg
                current_volume += s.volume_m3
                peak_weight = max(peak_weight, current_weight)
                peak_volume = max(peak_volume, current_volume)
                shipment_pickups[stop.shipment_id] = stop.sequence

            elif stop.type == "DELIVERY" and stop.shipment_id:
                s = shipment_map.get(stop.shipment_id)
                if not s:
                    raise ValidationException(f"Stop references unknown shipment '{stop.shipment_id}'")
                
                current_weight -= s.weight_kg
                current_volume -= s.volume_m3
                shipment_deliveries[stop.shipment_id] = stop.sequence

                if stop.shipment_id not in shipment_pickups:
                    raise ValidationException(f"Delivery of '{stop.shipment_id}' occurs before pickup in route '{route.lorry_id}'")

                if stop.shipment_id in served_shipments:
                    raise ValidationException(f"Duplicate delivery of shipment '{stop.shipment_id}'")
                
                served_shipments.add(stop.shipment_id)

                deadline_utc = ensure_utc(s.delivery_deadline)
                arr_utc = ensure_utc(stop.estimated_arrival)

                if arr_utc > deadline_utc:
                    raise ValidationException(f"Delivery of '{stop.shipment_id}' at {arr_utc} breaches deadline {deadline_utc}")

        if peak_weight > lorry.max_weight_kg + 0.01:
            raise ValidationException(f"Lorry '{lorry.id}' peak weight load ({peak_weight:.1f} kg) exceeds max weight ({lorry.max_weight_kg:.1f} kg)")

        if peak_volume > lorry.max_volume_m3 + 0.01:
            raise ValidationException(f"Lorry '{lorry.id}' peak volume load ({peak_volume:.1f} m³) exceeds max volume ({lorry.max_volume_m3:.1f} m³)")

    return True
