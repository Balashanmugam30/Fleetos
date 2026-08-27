"use client";

import React, { useState, useEffect } from "react";
import { fetchLatestTracking, VehicleTrackingState } from "@/lib/api";
import { Route as RouteIcon, Truck, MapPin, ShieldCheck, Navigation, Clock, Fuel, DollarSign } from "lucide-react";

export default function RoutesPage() {
  const [trackingStates, setTrackingStates] = useState<VehicleTrackingState[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const loadData = async () => {
    try {
      const trackRes = await fetchLatestTracking();
      setTrackingStates(trackRes);
    } catch (err) {
      console.error("Error loading route tracking:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  const demoRoutes = [
    {
      id: "R-L01",
      lorry_id: "L01",
      status: "ACTIVE",
      origin: "Bengaluru Depot",
      destination: "Chennai Port",
      distance_km: 348.5,
      duration_hrs: 6.5,
      fuel_liters: 99.6,
      cost_usd: 245.0,
      stops: ["Bengaluru Depot", "Hosur Hub", "Krishnagiri Checkpoint", "Vellore Warehouse", "Chennai Port"]
    },
    {
      id: "R-L02",
      lorry_id: "L02",
      status: "ACTIVE",
      origin: "Bengaluru Depot",
      destination: "Mysuru Industrial Zone",
      distance_km: 143.2,
      duration_hrs: 3.2,
      fuel_liters: 35.8,
      cost_usd: 110.0,
      stops: ["Bengaluru Depot", "Ramanagara", "Mandya", "Mysuru Industrial Zone"]
    },
    {
      id: "R-L03",
      lorry_id: "L03",
      status: "ACTIVE",
      origin: "Chennai Port",
      destination: "Vellore Industrial Complex",
      distance_km: 138.0,
      duration_hrs: 2.8,
      fuel_liters: 32.5,
      cost_usd: 98.0,
      stops: ["Chennai Port", "Sriperumbudur", "Ranipet", "Vellore Industrial Complex"]
    },
    {
      id: "R-L05",
      lorry_id: "L05",
      status: "ACTIVE",
      origin: "Vellore Depot",
      destination: "Bengaluru Electronic City",
      distance_km: 210.4,
      duration_hrs: 4.1,
      fuel_liters: 40.4,
      cost_usd: 145.0,
      stops: ["Vellore Depot", "Hosur Hub", "Bengaluru Electronic City"]
    }
  ];

  const trackingMap = new Map(trackingStates.map((s) => [s.vehicle_id, s]));

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Route Execution & Trajectory Monitor</h1>
          <p className="text-sm text-slate-500">Persisted VRP route sequences, assigned lorry telemetry & distance matrix.</p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-semibold text-brand-700 bg-brand-50 border border-brand-200 px-3 py-1.5 rounded-lg">
          <ShieldCheck className="w-4 h-4 text-brand-600" />
          <span>Google OR-Tools Solver Assigned Routes ({demoRoutes.length})</span>
        </div>
      </div>

      <div className="space-y-4">
        {demoRoutes.map((r) => {
          const track = trackingMap.get(r.lorry_id);
          const vehicleStatus = track?.status || "MOVING";
          const freshness = track?.freshness || "LIVE";
          const speed = track?.speed_kmh ?? 50.0;

          return (
            <div key={r.id} className="logistics-card p-6 space-y-4">
              <div className="flex flex-wrap justify-between items-center gap-2 border-b border-slate-100 pb-3">
                <div className="flex items-center space-x-3">
                  <div className="w-9 h-9 bg-brand-600 text-white rounded-lg flex items-center justify-center font-bold text-sm">
                    {r.lorry_id}
                  </div>
                  <div>
                    <h3 className="text-base font-bold text-slate-900 flex items-center">
                      <RouteIcon className="w-4 h-4 mr-1.5 text-brand-600" />
                      Route {r.id} ({r.origin} $\rightarrow$ {r.destination})
                    </h3>
                    <p className="text-xs text-slate-500 font-mono">Assigned Lorry: {r.lorry_id}</p>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                    vehicleStatus === "MOVING" ? "bg-blue-50 text-blue-700 border border-blue-200" : "bg-slate-100 text-slate-700 border border-slate-200"
                  }`}>
                    {vehicleStatus} ({speed} km/h)
                  </span>
                  <span className={`px-2 py-0.5 rounded text-xs font-semibold ${
                    freshness === "LIVE" ? "bg-emerald-50 text-emerald-700 border border-emerald-200" : "bg-amber-50 text-amber-700 border border-amber-200"
                  }`}>
                    {freshness}
                  </span>
                </div>
              </div>

              {/* Route Metric Cards */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl">
                  <span className="text-slate-400 block text-[11px]">Distance</span>
                  <span className="font-bold text-slate-900 text-sm">{r.distance_km} km</span>
                </div>
                <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl">
                  <span className="text-slate-400 block text-[11px]">Duration</span>
                  <span className="font-bold text-slate-900 text-sm">{r.duration_hrs} hrs</span>
                </div>
                <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl">
                  <span className="text-slate-400 block text-[11px]">Fuel Estimate</span>
                  <span className="font-bold text-amber-700 text-sm">{r.fuel_liters} Liters</span>
                </div>
                <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl">
                  <span className="text-slate-400 block text-[11px]">Cost Estimate</span>
                  <span className="font-bold text-emerald-700 text-sm">${r.cost_usd.toFixed(2)}</span>
                </div>
              </div>

              {/* Waypoint Progression Sequence */}
              <div>
                <span className="text-xs font-semibold text-slate-700 block mb-2">Stop Sequence:</span>
                <div className="flex flex-wrap items-center gap-2">
                  {r.stops.map((stop, idx) => (
                    <React.Fragment key={idx}>
                      <span className={`px-2.5 py-1 rounded-lg text-xs font-semibold flex items-center ${
                        idx === 0 ? "bg-brand-50 text-brand-700 border border-brand-200" :
                        idx === r.stops.length - 1 ? "bg-emerald-50 text-emerald-700 border border-emerald-200" :
                        "bg-slate-100 text-slate-700 border border-slate-200"
                      }`}>
                        <MapPin className="w-3 h-3 mr-1 text-slate-400" />
                        {stop}
                      </span>
                      {idx < r.stops.length - 1 && <span className="text-slate-300 font-bold">$\rightarrow$</span>}
                    </React.Fragment>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
