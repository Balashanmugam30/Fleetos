"use client";

import { useState } from "react";
import { triggerOptimization } from "@/lib/api";
import { Cpu, ShieldCheck, Play, CheckCircle2, AlertTriangle, Fuel, DollarSign, Route } from "lucide-react";

export default function OptimizationPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleRunOptimization = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await triggerOptimization("MANUAL_REOPTIMIZE");
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Failed to execute OR-Tools solver");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Deterministic Optimization Control</h1>
          <p className="text-sm text-slate-500">Google OR-Tools Routing Solver / RoutingModel VRP Engine Control.</p>
        </div>
        <button
          onClick={handleRunOptimization}
          disabled={loading}
          className="inline-flex items-center px-4 py-2 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-semibold text-sm rounded-lg shadow-sm transition-colors"
        >
          <Play className="w-4 h-4 mr-2" />
          {loading ? "Solving VRP..." : "Run Optimization Solver"}
        </button>
      </div>

      {/* Overview Card */}
      <div className="logistics-card p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div className="flex items-center space-x-3">
            <Cpu className="w-6 h-6 text-emerald-600" />
            <div>
              <h3 className="text-base font-bold text-slate-900">Google OR-Tools Routing Solver / RoutingModel</h3>
              <p className="text-xs text-slate-500">Python 3.13 Wheel Package `ortools-9.15.6755` Active</p>
            </div>
          </div>
          <span className="px-3 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full text-xs font-bold flex items-center">
            <ShieldCheck className="w-3.5 h-3.5 mr-1" />
            Authoritative Solver
          </span>
        </div>

        <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-600 space-y-2">
          <p><strong className="text-slate-900">Mathematical Abstraction:</strong> Multi-Vehicle Routing Problem with Capacity & Time Windows (CVRP-TW)</p>
          <p><strong className="text-slate-900">Constraints Evaluated:</strong> Peak Concurrent Weight Limit, Peak Concurrent Volume Limit, Delivery Deadlines, Driver Availability, Vehicle Fuel Efficiency (km/L), Priority Penalties</p>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-xs text-red-800 flex items-center">
          <AlertTriangle className="w-4 h-4 mr-2 text-red-600" />
          {error}
        </div>
      )}

      {result && (
        <div className="space-y-6 animate-fade-in">
          {/* Solver Summary Metrics */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="logistics-card p-4">
              <span className="text-xs text-slate-400 block">Solver Status</span>
              <span className="text-lg font-bold text-emerald-600 flex items-center mt-1">
                <CheckCircle2 className="w-4 h-4 mr-1 text-emerald-500" />
                {result.status}
              </span>
            </div>
            <div className="logistics-card p-4">
              <span className="text-xs text-slate-400 block">Total Transport Cost</span>
              <span className="text-lg font-bold text-slate-900 flex items-center mt-1">
                <DollarSign className="w-4 h-4 text-slate-500" />
                ${result.metrics.total_cost.toFixed(2)}
              </span>
            </div>
            <div className="logistics-card p-4">
              <span className="text-xs text-slate-400 block">Total Fuel Consumption</span>
              <span className="text-lg font-bold text-slate-900 flex items-center mt-1">
                <Fuel className="w-4 h-4 text-amber-500 mr-1" />
                {result.metrics.total_fuel_liters.toFixed(1)} L
              </span>
            </div>
            <div className="logistics-card p-4">
              <span className="text-xs text-slate-400 block">Assigned / Total</span>
              <span className="text-lg font-bold text-slate-900 mt-1">
                {result.metrics.assigned_count} / {result.metrics.total_shipments_count} Loads
              </span>
            </div>
          </div>

          {/* Assigned Routes */}
          <div className="logistics-card p-6 space-y-4">
            <h3 className="text-base font-bold text-slate-900 flex items-center">
              <Route className="w-5 h-5 mr-2 text-brand-600" />
              Calculated Vehicle Delivery Routes ({result.routes.length} Active Vehicles)
            </h3>
            <div className="space-y-4">
              {result.routes.map((route: any) => (
                <div key={route.lorry_id} className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-3">
                  <div className="flex justify-between items-center text-xs border-b border-slate-200 pb-2">
                    <span className="font-bold text-slate-900 text-sm">Lorry {route.lorry_id} ({route.vehicle_registration})</span>
                    <div className="space-x-3 text-slate-600">
                      <span>Dist: {(route.distance_meters / 1000).toFixed(1)} km</span>
                      <span>Fuel: {route.fuel_estimate_liters} L</span>
                      <span className="font-bold text-slate-900">Cost: ${route.total_cost}</span>
                    </div>
                  </div>

                  <div className="space-y-1 text-xs text-slate-600">
                    <strong className="text-slate-900 block mb-1">Stops Sequence:</strong>
                    {route.stops.map((stop: any) => (
                      <div key={stop.sequence} className="flex justify-between py-1 border-b border-slate-100 last:border-0">
                        <span>
                          <span className="font-mono text-slate-400 mr-2">#{stop.sequence}</span>
                          <span className="font-semibold text-slate-800">{stop.type}</span>: {stop.address} {stop.shipment_id ? `(${stop.shipment_id})` : ''}
                        </span>
                        <span className="text-slate-500">{new Date(stop.estimated_arrival).toLocaleTimeString()}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Unassigned Shipments Reasons */}
          {result.unassigned_shipments.length > 0 && (
            <div className="logistics-card p-6 space-y-3">
              <h3 className="text-base font-bold text-red-600 flex items-center">
                <AlertTriangle className="w-5 h-5 mr-2" />
                Unassigned Shipments Rejection Explanations ({result.unassigned_shipments.length})
              </h3>
              <div className="space-y-2">
                {result.unassigned_shipments.map((u: any) => (
                  <div key={u.shipment_id} className="p-3 bg-red-50 border border-red-200 rounded-lg text-xs text-red-900 space-y-1">
                    <div className="flex justify-between font-bold">
                      <span>Shipment {u.shipment_id}</span>
                      <span className="px-2 py-0.5 bg-red-100 rounded text-red-800 font-mono">{u.primary_reason_code}</span>
                    </div>
                    <p>{u.reason_description}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
