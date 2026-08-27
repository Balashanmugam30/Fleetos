"use client";

import React, { useState } from "react";
import { VehicleTrackingState } from "@/lib/api";
import { Truck, Navigation, Activity, Clock, ShieldCheck, MapPin } from "lucide-react";

interface FleetMapProps {
  trackingStates: VehicleTrackingState[];
  selectedVehicleId?: string | null;
  onSelectVehicle?: (vehicleId: string) => void;
}

export function FleetMap({ trackingStates, selectedVehicleId, onSelectVehicle }: FleetMapProps) {
  const [activeVehicleId, setActiveVehicleId] = useState<string | null>(selectedVehicleId || "L01");

  const selectedState = trackingStates.find((s) => s.vehicle_id === activeVehicleId) || trackingStates[0];

  const handleSelect = (id: string) => {
    setActiveVehicleId(id);
    if (onSelectVehicle) onSelectVehicle(id);
  };

  return (
    <div className="logistics-card p-6 space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center">
            <Navigation className="w-4 h-4 mr-2 text-brand-600" />
            Live Fleet Vector Telemetry Map
          </h3>
          <p className="text-xs text-slate-500">Real-time GPS coordinates, speed vectors, and telemetry freshness.</p>
        </div>
        <div className="flex items-center space-x-2 text-xs font-semibold text-brand-700 bg-brand-50 border border-brand-200 px-3 py-1 rounded-lg">
          <ShieldCheck className="w-3.5 h-3.5 text-brand-600" />
          <span>Mapbox Vector Telemetry Active</span>
        </div>
      </div>

      {/* Map Telemetry Canvas Area */}
      <div className="relative w-full h-80 bg-slate-900 rounded-xl overflow-hidden border border-slate-800 p-4 text-white flex flex-col justify-between shadow-inner">
        {/* Subtle Grid Map Lines */}
        <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#ffffff_1px,transparent_1px)] [background-size:16px_16px] pointer-events-none" />

        {/* Map Top Status Bar */}
        <div className="relative z-10 flex justify-between items-center text-xs font-mono text-slate-400 bg-slate-950/80 px-3 py-1.5 rounded-lg border border-slate-800 backdrop-blur-sm">
          <span>REGION: SOUTH INDIA CORRIDOR (BLR-MAA)</span>
          <span>VEHICLES REPORTING: {trackingStates.length} / 5</span>
        </div>

        {/* Vehicle Markers Overlay */}
        <div className="relative z-10 my-auto grid grid-cols-2 sm:grid-cols-5 gap-3">
          {trackingStates.map((state) => {
            const isSelected = state.vehicle_id === activeVehicleId;
            const isMoving = state.status === "MOVING";
            const isLive = state.freshness === "LIVE";

            return (
              <button
                key={state.vehicle_id}
                onClick={() => handleSelect(state.vehicle_id)}
                className={`p-3 rounded-lg border text-left transition-all ${
                  isSelected
                    ? "bg-brand-600/30 border-brand-400 text-white shadow-lg ring-2 ring-brand-500/50"
                    : "bg-slate-800/80 hover:bg-slate-800 border-slate-700 text-slate-300"
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-sm flex items-center">
                    <Truck className={`w-4 h-4 mr-1 ${isMoving ? "text-brand-400 animate-pulse" : "text-slate-400"}`} />
                    {state.vehicle_id}
                  </span>
                  <span className={`w-2 h-2 rounded-full ${
                    isLive ? "bg-emerald-400" : state.freshness === "RECENT" ? "bg-amber-400" : "bg-red-400"
                  }`} />
                </div>

                <div className="text-[11px] font-mono text-slate-400 space-y-0.5">
                  <div>{state.latitude.toFixed(4)}, {state.longitude.toFixed(4)}</div>
                  <div className="flex justify-between font-semibold text-slate-200">
                    <span>{state.speed_kmh} km/h</span>
                    <span>{state.heading_degrees}°</span>
                  </div>
                </div>
              </button>
            );
          })}
        </div>

        {/* Map Bottom Information Bar */}
        {selectedState && (
          <div className="relative z-10 bg-slate-950/90 p-3 rounded-lg border border-slate-800 flex flex-wrap items-center justify-between text-xs backdrop-blur-sm">
            <div className="flex items-center space-x-3">
              <MapPin className="w-4 h-4 text-brand-400" />
              <div>
                <span className="font-bold text-white mr-2">Selected: {selectedState.vehicle_id}</span>
                <span className="text-slate-400 font-mono">({selectedState.latitude.toFixed(6)}, {selectedState.longitude.toFixed(6)})</span>
              </div>
            </div>

            <div className="flex items-center space-x-3 text-slate-300">
              <span className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                selectedState.status === "MOVING" ? "bg-blue-500/20 text-blue-300 border border-blue-500/30" : "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
              }`}>
                {selectedState.status}
              </span>
              <span className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                selectedState.freshness === "LIVE" ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30" : "bg-amber-500/20 text-amber-300 border border-amber-500/30"
              }`}>
                {selectedState.freshness} ({selectedState.telemetry_age_seconds}s ago)
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
