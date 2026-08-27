"""
Fleetos Deterministic Optimization Engine Interface
Module Boundary: services/optimizer
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class OptimizationRequest(BaseModel):
    lorries: List[Dict[str, Any]]
    shipments: List[Dict[str, Any]]
    driver_availabilities: Dict[str, str]
    trigger_reason: str

class OptimizationResult(BaseModel):
    status: str  # 'OPTIMAL' | 'FEASIBLE' | 'INFEASIBLE'
    assignments: List[Dict[str, Any]]
    routes: List[Dict[str, Any]]
    total_cost: float
    total_fuel_liters: float
    deadline_violations: int
    unassigned_shipments: List[Dict[str, Any]]

class OptimizerInterface:
    """
    Abstract interface for Google OR-Tools VRP Solver.
    The LLM (ATLAS) NEVER formulates routes or solves VRP math.
    This deterministic solver engine is authoritative.
    """
    def solve(self, request: OptimizationRequest) -> OptimizationResult:
        raise NotImplementedError("Solver module will be implemented in Phase 3.")
