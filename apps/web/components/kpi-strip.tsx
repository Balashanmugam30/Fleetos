"use client";

import React from "react";
import { Truck, Activity, Clock, AlertTriangle, Package, ShieldCheck } from "lucide-react";
import { VehicleTrackingState } from "@/lib/api";

interface KpiStripProps {
  totalVehicles: number;
  trackingStates: VehicleTrackingState[];
  totalShipments: number;
  atRiskShipmentsCount?: number;
}

export function KpiStrip({ totalVehicles, trackingStates, totalShipments, atRiskShipmentsCount = 1 }: KpiStripProps) {
  const movingCount = trackingStates.filter((s) => s.status === "MOVING").length;
  const stoppedCount = trackingStates.filter((s) => s.status === "STOPPED" || s.status === "IDLE").length;
  const staleCount = trackingStates.filter((s) => s.freshness === "STALE" || s.freshness === "OFFLINE").length;
  const reportingCount = trackingStates.length || totalVehicles;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Active Fleet KPI */}
      <div className="logistics-card p-5">
        <div className="flex items-center justify-between text-slate-500 mb-2">
          <span className="text-xs font-semibold">Active Fleet</span>
          <Truck className="w-4 h-4 text-brand-600" />
        </div>
        <span className="text-2xl font-bold text-slate-900">{totalVehicles || 5} Vehicles</span>
        <div className="flex justify-between items-center text-xs text-slate-400 mt-1">
          <span>L01 – L05 Scenario</span>
          <span className="font-semibold text-emerald-700">{reportingCount}/{totalVehicles || 5} Live</span>
        </div>
      </div>

      {/* Moving Vehicles KPI */}
      <div className="logistics-card p-5">
        <div className="flex items-center justify-between text-slate-500 mb-2">
          <span className="text-xs font-semibold">Moving Vehicles</span>
          <Activity className="w-4 h-4 text-blue-600" />
        </div>
        <span className="text-2xl font-bold text-blue-600">{movingCount} Moving</span>
        <span className="block text-xs text-slate-400 mt-1">Telemetry Speed &gt; 2.0 km/h</span>
      </div>

      {/* Stopped / Idle KPI */}
      <div className="logistics-card p-5">
        <div className="flex items-center justify-between text-slate-500 mb-2">
          <span className="text-xs font-semibold">Stopped / Idle</span>
          <Clock className="w-4 h-4 text-emerald-600" />
        </div>
        <span className="text-2xl font-bold text-emerald-600">{stoppedCount} Vehicles</span>
        <span className="block text-xs text-slate-400 mt-1">{staleCount > 0 ? `${staleCount} Telemetry Stale` : "0 Telemetry Stale"}</span>
      </div>

      {/* Load Volume & At-Risk Shipments KPI */}
      <div className="logistics-card p-5">
        <div className="flex items-center justify-between text-slate-500 mb-2">
          <span className="text-xs font-semibold">Total Load Volume</span>
          <Package className="w-4 h-4 text-brand-600" />
        </div>
        <span className="text-2xl font-bold text-slate-900">{totalShipments || 12} Shipments</span>
        <div className="flex justify-between items-center text-xs mt-1">
          <span className="text-slate-400">Target Loads</span>
          <span className="font-bold text-amber-600">{atRiskShipmentsCount} At-Risk (S12)</span>
        </div>
      </div>
    </div>
  );
}
