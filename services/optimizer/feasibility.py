"""
Fleetos Pre-Flight Feasibility & Diagnostic Pre-Checker
Module Boundary: services/optimizer/feasibility.py
"""

import datetime
from typing import List, Tuple, Dict, Optional
from services.optimizer.models import OptimizationInput, UnassignedReason, ShipmentInput, VehicleInput, ensure_utc
from services.optimizer.matrix import haversine_distance_meters, ROAD_TORTUOSITY_FACTOR

def run_preflight_feasibility_checks(
    input_data: OptimizationInput
) -> Tuple[List[ShipmentInput], List[UnassignedReason]]:
    """
    Perform pre-flight cheap feasibility checks before passing data to OR-Tools solver.
    Returns:
        (feasible_shipments, preflight_unassigned_reasons)
    """
    available_vehicles = [v for v in input_data.vehicles if v.driver_available and v.status != "UNAVAILABLE"]

    if not available_vehicles:
        reasons = [
            UnassignedReason(
                shipment_id=s.id,
                assigned=False,
                primary_reason_code="NO_AVAILABLE_DRIVER",
                reason_description="No available drivers found in the active fleet.",
                contributing_constraints=["DRIVER_UNAVAILABLE"]
            )
            for s in input_data.shipments
        ]
        return [], reasons

    max_fleet_weight = max(v.max_weight_kg for v in available_vehicles)
    max_fleet_volume = max(v.max_volume_m3 for v in available_vehicles)

    feasible_shipments: List[ShipmentInput] = []
    unassigned_reasons: List[UnassignedReason] = []

    speed_m_s = (input_data.config.default_speed_km_h * 1000.0) / 3600.0
    start_time_utc = ensure_utc(input_data.start_time)

    for s in input_data.shipments:
        reasons_list: List[str] = []
        deadline_utc = ensure_utc(s.delivery_deadline)

        # 1. Weight capacity check
        if s.weight_kg > max_fleet_weight:
            reasons_list.append("WEIGHT_CAPACITY_EXCEEDED")

        # 2. Volume capacity check
        if s.volume_m3 > max_fleet_volume:
            reasons_list.append("VOLUME_CAPACITY_EXCEEDED")

        # 3. Deadline pre-check
        earliest_possible_arrival: Optional[datetime.datetime] = None
        for v in available_vehicles:
            dist_m = haversine_distance_meters(
                v.start_latitude, v.start_longitude,
                s.destination_latitude, s.destination_longitude
            ) * ROAD_TORTUOSITY_FACTOR
            transit_sec = int(dist_m / speed_m_s) if speed_m_s > 0 else 0
            est_arrival = start_time_utc + datetime.timedelta(seconds=transit_sec + input_data.config.service_time_pickup_seconds + input_data.config.service_time_delivery_seconds)
            
            if earliest_possible_arrival is None or est_arrival < earliest_possible_arrival:
                earliest_possible_arrival = est_arrival

        if earliest_possible_arrival and earliest_possible_arrival > deadline_utc:
            reasons_list.append("DEADLINE_INFEASIBLE")

        if reasons_list:
            primary_code = reasons_list[0]
            desc_map = {
                "WEIGHT_CAPACITY_EXCEEDED": f"Shipment weight ({s.weight_kg:,.0f} kg) exceeds maximum fleet lorry capacity ({max_fleet_weight:,.0f} kg).",
                "VOLUME_CAPACITY_EXCEEDED": f"Shipment volume ({s.volume_m3:.1f} m³) exceeds maximum fleet lorry volume capacity ({max_fleet_volume:.1f} m³).",
                "DEADLINE_INFEASIBLE": f"No available vehicle can reach the destination by {deadline_utc.strftime('%H:%M IST')} under current speed constraints."
            }
            unassigned_reasons.append(
                UnassignedReason(
                    shipment_id=s.id,
                    assigned=False,
                    primary_reason_code=primary_code,
                    reason_description=desc_map.get(primary_code, "Shipment failed pre-flight feasibility checks."),
                    contributing_constraints=reasons_list
                )
            )
        else:
            feasible_shipments.append(s)

    return feasible_shipments, unassigned_reasons
