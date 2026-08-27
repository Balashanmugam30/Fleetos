# Fleetos Operational Cost & Fuel Model

Product: **Fleetos**

---

## Formulas

### 1. Fuel Consumption (Liters)
$$\text{Fuel (Liters)} = \frac{\text{Distance (km)}}{\text{Fuel Efficiency (km/L)}}$$

### 2. Operational Cost Breakdown
$$\text{Total Cost} = \text{Fuel Cost} + \text{Driver Cost} + \text{Distance Cost} + \text{Fixed Vehicle Cost}$$

where:
- $\text{Fuel Cost} = \text{Fuel (Liters)} \times \text{Fuel Price per Liter}$
- $\text{Driver Cost} = \left(\frac{\text{Duration (seconds)}}{3600}\right) \times \text{Driver Cost per Hour}$
- $\text{Distance Cost} = \text{Distance (km)} \times \text{Cost per Km}$
- $\text{Fixed Cost} = \$50.00$ per dispatched vehicle
