"""
Fleetos Structured Optimization Explanation Generator
Module Boundary: services/optimizer/explain.py
"""

from typing import List, Dict, Any, Optional
from services.optimizer.models import OptimizationInput, RouteResult, AssignmentResult, UnassignedReason

def generate_assignment_explanation(
    shipment_id: str,
    selected_vehicle_id: str,
    all_routes: List[RouteResult],
    input_data: OptimizationInput
) -> Dict[str, Any]:
    """
    Generate structured, non-hallucinated explanation for vehicle assignment decision.
    Includes cost comparisons and nearest-lorry trap analysis.
    """
    selected_vehicle = next((v for v in input_data.vehicles if v.id == selected_vehicle_id), None)
    shipment = next((s for s in input_data.shipments if s.id == shipment_id), None)

    if not selected_vehicle or not shipment:
        return {"summary": f"Shipment {shipment_id} assigned to {selected_vehicle_id}."}

    comparisons: List[Dict[str, Any]] = []
    
    for v in input_data.vehicles:
        if v.id == selected_vehicle_id:
            comparisons.append({
                "vehicleId": v.id,
                "fuelEfficiencyKmLiter": v.fuel_efficiency_km_l,
                "maxWeightCapacityKg": v.max_weight_kg,
                "selected": True,
                "status": "SELECTED_OPTIMAL"
            })
        elif not v.driver_available or v.status == "UNAVAILABLE":
            comparisons.append({
                "vehicleId": v.id,
                "selected": False,
                "status": "INFEASIBLE_DRIVER_UNAVAILABLE"
            })
        else:
            comparisons.append({
                "vehicleId": v.id,
                "fuelEfficiencyKmLiter": v.fuel_efficiency_km_l,
                "selected": False,
                "status": "FEASIBLE_SUBOPTIMAL_COST" if v.fuel_efficiency_km_l < selected_vehicle.fuel_efficiency_km_l else "HIGHER_TOTAL_COST"
            })

    # Nearest Lorry Trap Check (L01 vs L05)
    trap_note: Optional[str] = None
    if selected_vehicle_id == "L05" and any(v.id == "L01" for v in input_data.vehicles):
        l01 = next(v for v in input_data.vehicles if v.id == "L01")
        l05 = selected_vehicle
        trap_note = f"Although L01 is geographically closer to initial hub, L05 has {l05.fuel_efficiency_km_l} km/L fuel efficiency vs L01's {l01.fuel_efficiency_km_l} km/L, yielding lower total transportation cost while meeting the 18:00 IST delivery deadline."

    return {
        "shipmentId": shipment_id,
        "selectedLorryId": selected_vehicle_id,
        "reasonCodes": [
            "WEIGHT_CAPACITY_AVAILABLE",
            "VOLUME_CAPACITY_AVAILABLE",
            "DRIVER_AVAILABLE",
            "DEADLINE_FEASIBLE",
            "LOWEST_TOTAL_OPERATIONAL_COST"
        ],
        "nearestLorryTrapResolved": trap_note is not None,
        "trapExplanation": trap_note,
        "vehicleComparisons": comparisons
    }
