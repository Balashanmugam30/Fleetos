"""
Fleetos Fuel Consumption & Operational Cost Modeling
Module Boundary: services/optimizer/cost.py
"""

from typing import Dict, Any, Tuple
from services.optimizer.models import ObjectiveConfig

def calculate_route_cost_breakdown(
    distance_meters: float,
    duration_seconds: int,
    fuel_efficiency_km_l: float,
    config: ObjectiveConfig
) -> Tuple[float, float, float, float, float]:
    """
    Calculate vehicle-specific fuel liters, fuel cost, driver cost, fixed cost, and total operating cost.
    Returns:
        (fuel_liters, fuel_cost, driver_cost, fixed_cost, total_cost)
    """
    distance_km = distance_meters / 1000.0
    
    # Fuel consumption formula: Distance (km) / Fuel Efficiency (km/L)
    fuel_liters = distance_km / fuel_efficiency_km_l if fuel_efficiency_km_l > 0 else 0.0
    fuel_cost = fuel_liters * config.fuel_price_per_liter

    # Driver cost: (Duration in hours) * Driver Cost per hour
    duration_hours = duration_seconds / 3600.0
    driver_cost = duration_hours * config.driver_cost_per_hour

    # Distance variable cost
    distance_cost = distance_km * config.cost_per_km

    # Fixed vehicle cost applied whenever vehicle is dispatched
    fixed_cost = config.fixed_vehicle_cost if distance_meters > 0 else 0.0

    total_cost = fuel_cost + driver_cost + distance_cost + fixed_cost

    return (
        round(fuel_liters, 2),
        round(fuel_cost, 2),
        round(driver_cost, 2),
        round(fixed_cost, 2),
        round(total_cost, 2)
    )
