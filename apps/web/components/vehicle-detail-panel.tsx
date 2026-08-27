"use client";

import React from "react";
import { VehicleTrackingState, Lorry } from "@/lib/api";
import { Truck, Navigation, Clock, ShieldCheck, MapPin, User, Package, Gauge } from "lucide-react";

interface VehicleDetailPanelProps {
  trackingState: VehicleTrackingState | null;
  lorry: Lorry | null;
}

export function VehicleDetailPanel({ trackingState, lorry }: VehicleDetailPanelProps) {
  if (!trackingState && !lorry) {
    return (
      <div className="logistics-card p-6 min-h-[380px] flex flex-col justify-center items-center text-slate-400">
        <Truck className="w-10 h-10 mb-2 text-slate-300" />
        <span className="text-sm font-medium">Select a vehicle from the map to view telemetry details.</span>
      </div>
    );
  }

  const vehicleId = trackingState?.vehicle_id || lorry?.id || "L01";
  const regNumber = lorry?.registration_number || `KA-01-EQ-${vehicleId}`;
  const driverId = trackingState?.driver_id || lorry?.driver_id || `D0${vehicleId.slice(-1)}`;
  const status = trackingState?.status || lorry?.status || "IDLE";
  const freshness = trackingState?.freshness || "LIVE";
  const speed = trackingState?.speed_kmh ?? lorry?.current_speed_km_h ?? 0.0;
  const heading = trackingState?.heading_degrees ?? lorry?.current_heading_degrees ?? 0.0;
  const lat = trackingState?.latitude ?? lorry?.current_latitude ?? 12.9716;
  const lng = trackingState?.longitude ?? lorry?.current_longitude ?? 77.5946;
  const telemetryAge = trackingState?.telemetry_age_seconds ?? 0.0;
  const activeRouteId = trackingState?.active_route_id || lorry?.current_route_id || `R-${vehicleId}`;

  return (
    <div className="logistics-card p-6 space-y-4 min-h-[380px] flex flex-col justify-between">
      <div>
        {/* Panel Header */}
        <div className="flex justify-between items-start border-b border-slate-100 pb-3">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-lg font-extrabold text-slate-900">Lorry {vehicleId}</span>
              <span className="font-mono text-xs px-2 py-0.5 bg-slate-100 text-slate-600 rounded border border-slate-200">
                {regNumber}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">Canonical Vehicle Telemetry Profile</p>
          </div>

          <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${
            status === "MOVING" ? "bg-blue-50 text-blue-700 border border-blue-200" :
            status === "STOPPED" ? "bg-slate-100 text-slate-700 border border-slate-200" :
            "bg-amber-50 text-amber-700 border border-amber-200"
          }`}>
            {status}
          </span>
        </div>

        {/* Telemetry Metrics Grid */}
        <div className="grid grid-cols-2 gap-3 my-4">
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
            <span className="text-[11px] font-semibold text-slate-400 flex items-center">
              <Gauge className="w-3.5 h-3.5 mr-1 text-brand-600" />
              Speed & Heading
            </span>
            <span className="text-base font-bold text-slate-900 block">{speed} km/h</span>
            <span className="text-[11px] text-slate-500 block">Bearing: {heading}°</span>
          </div>

          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
            <span className="text-[11px] font-semibold text-slate-400 flex items-center">
              <Clock className="w-3.5 h-3.5 mr-1 text-emerald-600" />
              Freshness
            </span>
            <span className={`text-base font-bold block ${
              freshness === "LIVE" ? "text-emerald-700" : freshness === "RECENT" ? "text-amber-600" : "text-red-600"
            }`}>
              {freshness}
            </span>
            <span className="text-[11px] text-slate-500 block">Age: {telemetryAge}s</span>
          </div>

          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1 col-span-2">
            <span className="text-[11px] font-semibold text-slate-400 flex items-center">
              <MapPin className="w-3.5 h-3.5 mr-1 text-brand-600" />
              GPS Coordinates
            </span>
            <span className="font-mono text-xs font-bold text-slate-900 block">
              {lat.toFixed(6)}, {lng.toFixed(6)}
            </span>
          </div>
        </div>

        {/* Assigned Details List */}
        <div className="space-y-2 text-xs">
          <div className="flex justify-between py-1 border-b border-slate-100">
            <span className="text-slate-500 flex items-center">
              <User className="w-3.5 h-3.5 mr-1.5 text-slate-400" />
              Assigned Driver:
            </span>
            <span className="font-semibold text-slate-900">{driverId}</span>
          </div>

          <div className="flex justify-between py-1 border-b border-slate-100">
            <span className="text-slate-500 flex items-center">
              <Navigation className="w-3.5 h-3.5 mr-1.5 text-slate-400" />
              Active Route:
            </span>
            <span className="font-semibold text-slate-900 font-mono">{activeRouteId}</span>
          </div>

          <div className="flex justify-between py-1">
            <span className="text-slate-500 flex items-center">
              <Package className="w-3.5 h-3.5 mr-1.5 text-slate-400" />
              Vehicle Capacity:
            </span>
            <span className="font-semibold text-slate-900">
              {lorry ? `${lorry.max_weight_kg.toLocaleString()} kg / ${lorry.max_volume_m3} m³` : "12,000 kg / 45 m³"}
            </span>
          </div>
        </div>
      </div>

      <div className="pt-3 border-t border-slate-100 flex justify-between items-center text-[11px] text-slate-400">
        <span>Telemetry Source: SIMULATOR</span>
        <span>ID: {vehicleId}</span>
      </div>
    </div>
  );
}
