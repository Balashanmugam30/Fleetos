# Fleetos Control Tower Architecture

Product: **Fleetos**  
Module Boundary: `apps/web`

---

## Component Architecture

```
                    apps/web/app/dashboard/page.tsx
                                  │
    ┌─────────────────────────────┼─────────────────────────────┐
    │                             │                             │
KpiStrip                   FleetMap & Detail            SimulatorControls
    │                             │                             │
    └─────────────────────────────┼─────────────────────────────┘
                                  │
      ┌───────────────────────────┼───────────────────────────┐
      │                           │                           │
EventStream              AtRiskShipments             OptimizationSummary
```

### Component Boundaries
- `apps/web/components/fleet-map.tsx`: Reusable map visualizer with vector coordinate markers and vehicle selection handlers.
- `apps/web/components/vehicle-detail-panel.tsx`: Profile side panel for active lorry.
- `apps/web/components/kpi-strip.tsx`: Real-time KPI strip.
- `apps/web/components/simulator-controls.tsx`: Development GPS simulator control bar.
- `apps/web/components/event-stream.tsx`: Structured operational event feed.
- `apps/web/components/at-risk-shipments.tsx`: Shipment deadline monitoring.
- `apps/web/components/optimization-summary.tsx`: OR-Tools solver summary card.
