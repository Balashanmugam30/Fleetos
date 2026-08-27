"""
Fleetos Deterministic Optimization Engine Interface
Module Boundary: services/optimizer/interface.py
"""

from typing import List, Dict, Any, Optional
from services.optimizer.models import OptimizationInput, OptimizationResult
from services.optimizer.service import OptimizationService

class OptimizerInterface:
    """
    Interface for Google OR-Tools Routing Solver / RoutingModel Engine.
    The LLM (ATLAS) NEVER formulates routes or solves VRP math.
    This deterministic solver engine is authoritative.
    """
    def solve(self, input_data: OptimizationInput, trigger_reason: str = "MANUAL_REOPTIMIZE") -> OptimizationResult:
        return OptimizationService.run_optimization(input_data, trigger_reason=trigger_reason)
