"""
Fleetos Google OR-Tools Routing Solver / RoutingModel Engine
Module Boundary: services/optimizer/routing.py
"""

import math
import datetime
from typing import List, Dict, Any, Tuple, Optional
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from services.optimizer.models import (
    OptimizationInput, VehicleInput, ShipmentInput, 
    RouteResult, StopResult, AssignmentResult, UnassignedReason, ensure_utc
)
from services.optimizer.matrix import (
    LocationNode, HaversineTravelTimeProvider, TravelMatrix
)
from services.optimizer.cost import calculate_route_cost_breakdown
from services.optimizer.explain import generate_assignment_explanation

def solve_vrp_routing_model(
    input_data: OptimizationInput,
    feasible_shipments: List[ShipmentInput]
) -> Tuple[str, List[RouteResult], List[AssignmentResult], List[UnassignedReason]]:
    """
    Solve Multi-Vehicle Routing Problem with Capacity & Time Window Constraints (CVRP-TW)
    using Google OR-Tools RoutingIndexManager & RoutingModel.
    """
    available_vehicles = [v for v in input_data.vehicles if v.driver_available and v.status != "UNAVAILABLE"]
    start_time_utc = ensure_utc(input_data.start_time)

    if not available_vehicles or not feasible_shipments:
        unassigned = [
            UnassignedReason(
                shipment_id=s.id,
                assigned=False,
                primary_reason_code="NO_FEASIBLE_VEHICLE",
                reason_description="No feasible vehicles or shipments available for optimization."
            )
            for s in feasible_shipments
        ]
        return "FEASIBLE", [], [], unassigned

    # 1. Build Location Nodes List
    nodes: List[LocationNode] = []
    
    # Depots (0 .. num_vehicles - 1)
    for v in available_vehicles:
        nodes.append(LocationNode(id=f"depot_{v.id}", latitude=v.start_latitude, longitude=v.start_longitude))

    # Shipment Pickups (num_vehicles .. num_vehicles + num_shipments - 1)
    for s in feasible_shipments:
        nodes.append(LocationNode(id=f"pickup_{s.id}", latitude=s.pickup_latitude, longitude=s.pickup_longitude))

    # Shipment Deliveries (num_vehicles + num_shipments .. num_vehicles + 2*num_shipments - 1)
    for s in feasible_shipments:
        nodes.append(LocationNode(id=f"delivery_{s.id}", latitude=s.destination_latitude, longitude=s.destination_longitude))

    # 2. Compute Travel Matrix
    matrix_provider = HaversineTravelTimeProvider()
    matrix = matrix_provider.compute_matrix(nodes, speed_km_h=input_data.config.default_speed_km_h)

    num_vehicles = len(available_vehicles)
    num_shipments = len(feasible_shipments)
    
    starts = list(range(num_vehicles))
    ends = list(range(num_vehicles))

    # 3. Create RoutingIndexManager & RoutingModel
    manager = pywrapcp.RoutingIndexManager(len(nodes), num_vehicles, starts, ends)
    routing = pywrapcp.RoutingModel(manager)

    num_indices = manager.GetNumberOfIndices()
    def safe_node(index: int) -> int:
        if index < 0 or index >= num_indices:
            return 0
        try:
            node = manager.IndexToNode(index)
            return node if node >= 0 else 0
        except Exception:
            return 0

    # 4. Distance Arc Cost Evaluator
    def distance_callback(from_index: int, to_index: int) -> int:
        from_node = safe_node(from_index)
        to_node = safe_node(to_index)
        return int(matrix.distances_meters.get((from_node, to_node), 0.0))

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # 5. Weight Capacity Dimension
    def weight_demand_callback(from_index: int) -> int:
        from_node = safe_node(from_index)
        if num_vehicles <= from_node < num_vehicles + num_shipments:
            shipment_idx = from_node - num_vehicles
            return int(feasible_shipments[shipment_idx].weight_kg)
        elif num_vehicles + num_shipments <= from_node < num_vehicles + 2 * num_shipments:
            shipment_idx = from_node - (num_vehicles + num_shipments)
            return -int(feasible_shipments[shipment_idx].weight_kg)
        return 0

    weight_callback_index = routing.RegisterUnaryTransitCallback(weight_demand_callback)
    weight_capacities = [int(v.max_weight_kg) for v in available_vehicles]
    routing.AddDimensionWithVehicleCapacity(
        weight_callback_index,
        0,
        weight_capacities,
        True,
        "Weight"
    )

    # 6. Volume Capacity Dimension
    def volume_demand_callback(from_index: int) -> int:
        from_node = safe_node(from_index)
        if num_vehicles <= from_node < num_vehicles + num_shipments:
            shipment_idx = from_node - num_vehicles
            return int(feasible_shipments[shipment_idx].volume_m3 * 100)
        elif num_vehicles + num_shipments <= from_node < num_vehicles + 2 * num_shipments:
            shipment_idx = from_node - (num_vehicles + num_shipments)
            return -int(feasible_shipments[shipment_idx].volume_m3 * 100)
        return 0

    volume_callback_index = routing.RegisterUnaryTransitCallback(volume_demand_callback)
    volume_capacities = [int(v.max_volume_m3 * 100) for v in available_vehicles]
    routing.AddDimensionWithVehicleCapacity(
        volume_callback_index,
        0,
        volume_capacities,
        True,
        "Volume"
    )

    # 7. Time Dimension & Pickup-Delivery Constraints
    def time_callback(from_index: int, to_index: int) -> int:
        from_node = safe_node(from_index)
        to_node = safe_node(to_index)
        transit_sec = matrix.durations_seconds.get((from_node, to_node), 0)
        
        if num_vehicles <= from_node < num_vehicles + num_shipments:
            transit_sec += input_data.config.service_time_pickup_seconds
        elif num_vehicles + num_shipments <= from_node < num_vehicles + 2 * num_shipments:
            transit_sec += input_data.config.service_time_delivery_seconds

        return transit_sec

    time_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.AddDimension(
        time_callback_index,
        86400,
        86400 * 7,
        True,
        "Time"
    )
    time_dimension = routing.GetDimensionOrDie("Time")

    # Add Pickup & Delivery Pairs, Same-Vehicle Constraints & Delivery Deadlines
    for i in range(num_shipments):
        pickup_index = manager.NodeToIndex(num_vehicles + i)
        delivery_index = manager.NodeToIndex(num_vehicles + num_shipments + i)
        shipment = feasible_shipments[i]
        deadline_utc = ensure_utc(shipment.delivery_deadline)

        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index))
        routing.solver().Add(time_dimension.CumulVar(pickup_index) <= time_dimension.CumulVar(delivery_index))

        # Delivery Deadline Constraint
        deadline_offset_seconds = int((deadline_utc - start_time_utc).total_seconds())
        if deadline_offset_seconds > 0:
            time_dimension.CumulVar(delivery_index).SetRange(0, deadline_offset_seconds)

        # Disjunction penalties on pickup and delivery nodes separately
        priority_weight = int(input_data.config.priority_penalties.get(shipment.priority, 1000.0))
        penalty = 100_000_000 + (priority_weight * 10_000)
        routing.AddDisjunction([pickup_index], penalty)
        routing.AddDisjunction([delivery_index], penalty)

    # 8. Set Search Parameters & Solve
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    search_params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_params.time_limit.seconds = input_data.config.solve_timeout_seconds

    solution = routing.SolveWithParameters(search_params)

    if not solution:
        unassigned = [
            UnassignedReason(
                shipment_id=s.id,
                assigned=False,
                primary_reason_code="NO_FEASIBLE_ROUTE",
                reason_description="OR-Tools solver could not find a feasible routing solution satisfying all constraints."
            )
            for s in feasible_shipments
        ]
        return "INFEASIBLE", [], [], unassigned

    # 9. Extract Solution & Construct Routes
    routes: List[RouteResult] = []
    assignments: List[AssignmentResult] = []
    unassigned: List[UnassignedReason] = []
    assigned_shipment_ids = set()

    for v_idx in range(num_vehicles):
        vehicle = available_vehicles[v_idx]
        index = routing.Start(v_idx)
        
        stops: List[StopResult] = []
        stop_seq = 1
        route_dist_m = 0.0
        route_dur_sec = 0
        peak_weight = 0.0
        peak_volume = 0.0
        curr_weight = 0.0
        curr_volume = 0.0

        # Start Depot Stop
        stops.append(StopResult(
            sequence=stop_seq,
            type="START",
            latitude=vehicle.start_latitude,
            longitude=vehicle.start_longitude,
            address=f"Depot {vehicle.id}",
            estimated_arrival=start_time_utc
        ))

        while not routing.IsEnd(index):
            prev_index = index
            index = solution.Value(routing.NextVar(index))
            node_idx = manager.IndexToNode(index)
            prev_node_idx = manager.IndexToNode(prev_index)

            step_dist = matrix.distances_meters.get((prev_node_idx, node_idx), 0.0)
            step_dur = matrix.durations_seconds.get((prev_node_idx, node_idx), 0)
            
            route_dist_m += step_dist
            route_dur_sec += step_dur

            arr_time = start_time_utc + datetime.timedelta(seconds=route_dur_sec)

            if num_vehicles <= node_idx < num_vehicles + num_shipments:
                s_idx = node_idx - num_vehicles
                shipment = feasible_shipments[s_idx]
                curr_weight += shipment.weight_kg
                curr_volume += shipment.volume_m3
                peak_weight = max(peak_weight, curr_weight)
                peak_volume = max(peak_volume, curr_volume)

                stop_seq += 1
                stops.append(StopResult(
                    sequence=stop_seq,
                    type="PICKUP",
                    shipment_id=shipment.id,
                    latitude=shipment.pickup_latitude,
                    longitude=shipment.pickup_longitude,
                    address=shipment.pickup_address,
                    estimated_arrival=arr_time
                ))

            elif num_vehicles + num_shipments <= node_idx < num_vehicles + 2 * num_shipments:
                s_idx = node_idx - (num_vehicles + num_shipments)
                shipment = feasible_shipments[s_idx]
                curr_weight -= shipment.weight_kg
                curr_volume -= shipment.volume_m3
                assigned_shipment_ids.add(shipment.id)
                deadline_utc = ensure_utc(shipment.delivery_deadline)

                slack_min = (deadline_utc - arr_time).total_seconds() / 60.0
                d_status = "SAFE" if slack_min > 60 else "TIGHT" if slack_min >= 0 else "MISSED"

                stop_seq += 1
                stops.append(StopResult(
                    sequence=stop_seq,
                    type="DELIVERY",
                    shipment_id=shipment.id,
                    latitude=shipment.destination_latitude,
                    longitude=shipment.destination_longitude,
                    address=shipment.destination_address,
                    estimated_arrival=arr_time,
                    deadline=deadline_utc,
                    deadline_slack_minutes=round(slack_min, 1),
                    deadline_status=d_status
                ))

                assignments.append(AssignmentResult(
                    shipment_id=shipment.id,
                    lorry_id=vehicle.id,
                    sequence=stop_seq,
                    pickup_stop_sequence=stop_seq - 1,
                    delivery_stop_sequence=stop_seq,
                    estimated_delivery_time=arr_time,
                    deadline=deadline_utc,
                    assignment_reason=f"Assigned to {vehicle.id} by OR-Tools RoutingModel (Fuel: {vehicle.fuel_efficiency_km_l} km/L)",
                    explanation={}
                ))

        if len(stops) > 1:
            fuel_liters, fuel_cost, driver_cost, fixed_cost, total_cost = calculate_route_cost_breakdown(
                route_dist_m, route_dur_sec, vehicle.fuel_efficiency_km_l, input_data.config
            )
            weight_util = (peak_weight / vehicle.max_weight_kg * 100.0) if vehicle.max_weight_kg > 0 else 0.0
            volume_util = (peak_volume / vehicle.max_volume_m3 * 100.0) if vehicle.max_volume_m3 > 0 else 0.0

            routes.append(RouteResult(
                lorry_id=vehicle.id,
                driver_id=vehicle.id.replace("L", "D"),
                vehicle_registration=vehicle.registration_number,
                stops=stops,
                distance_meters=round(route_dist_m, 1),
                estimated_duration_seconds=route_dur_sec,
                fuel_estimate_liters=fuel_liters,
                fuel_cost=fuel_cost,
                driver_cost=driver_cost,
                fixed_cost=fixed_cost,
                total_cost=total_cost,
                peak_weight_kg=peak_weight,
                peak_volume_m3=peak_volume,
                weight_utilization_percent=round(weight_util, 1),
                volume_utilization_percent=round(volume_util, 1),
                deadline_risk="NONE"
            ))

    for s in feasible_shipments:
        if s.id not in assigned_shipment_ids:
            unassigned.append(UnassignedReason(
                shipment_id=s.id,
                assigned=False,
                primary_reason_code="CAPACITY_OR_DEADLINE_INFEASIBLE",
                reason_description=f"Shipment {s.id} could not be placed on any route without violating weight, volume, or delivery deadline constraints."
            ))

    for asg in assignments:
        asg.explanation = generate_assignment_explanation(asg.shipment_id, asg.lorry_id, routes, input_data)

    solver_status = "OPTIMAL" if not unassigned else "FEASIBLE"
    return solver_status, routes, assignments, unassigned
