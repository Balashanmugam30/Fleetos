"""
Fleetos Optimization Service Master Orchestrator
Module Boundary: services/optimizer/service.py
"""

import time
import uuid
import datetime
from typing import List, Dict, Any, Tuple
from services.optimizer.models import (
    OptimizationInput, OptimizationResult, OptimizationMetrics
)
from services.optimizer.feasibility import run_preflight_feasibility_checks
from services.optimizer.routing import solve_vrp_routing_model
from services.optimizer.validation import validate_optimization_solution

class OptimizationService:
    """
    Master Orchestrator for Fleetos Deterministic Multi-Lorry Optimization Engine.
    Executes pre-flight checks, OR-Tools RoutingModel solving, post-solution validation, and metrics compilation.
    """
    @staticmethod
    def run_optimization(input_data: OptimizationInput, trigger_reason: str = "MANUAL_REOPTIMIZE") -> OptimizationResult:
        start_time_ms = time.time() * 1000.0
        run_id = f"opt_run_{uuid.uuid4().hex[:8]}"

        # 1. Pre-flight Feasibility Diagnostics
        feasible_shipments, preflight_unassigned = run_preflight_feasibility_checks(input_data)

        # 2. OR-Tools RoutingModel VRP Solver
        solver_status, routes, assignments, solver_unassigned = solve_vrp_routing_model(input_data, feasible_shipments)

        # Combine all unassigned reasons
        all_unassigned = preflight_unassigned + solver_unassigned

        # 3. Post-Solution Independent Solution Validation
        if routes:
            validate_optimization_solution(input_data, routes, assignments)

        solve_duration_ms = round(time.time() * 1000.0 - start_time_ms, 2)

        # 4. Aggregate Metrics
        total_cost = round(sum(r.total_cost for r in routes), 2)
        total_distance = round(sum(r.distance_meters for r in routes), 1)
        total_fuel = round(sum(r.fuel_estimate_liters for r in routes), 2)
        assigned_count = len(assignments)
        unassigned_count = len(all_unassigned)
        vehicles_used = len(routes)
        deadline_violations = sum(
            1 for r in routes for s in r.stops if s.deadline_status == "MISSED"
        )

        metrics = OptimizationMetrics(
            total_cost=total_cost,
            total_distance_meters=total_distance,
            total_fuel_liters=total_fuel,
            total_shipments_count=len(input_data.shipments),
            assigned_count=assigned_count,
            unassigned_count=unassigned_count,
            deadline_violations_count=deadline_violations,
            vehicles_used_count=vehicles_used,
            solve_duration_ms=solve_duration_ms
        )

        explanations = [asg.explanation for asg in assignments]

        return OptimizationResult(
            run_id=run_id,
            status=solver_status,
            trigger_reason=trigger_reason,
            routing_provider="ESTIMATED_HAVERSINE",
            metrics=metrics,
            assignments=assignments,
            routes=routes,
            unassigned_shipments=all_unassigned,
            explanations=explanations
        )
