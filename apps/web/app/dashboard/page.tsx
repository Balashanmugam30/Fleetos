import { Truck, Package, Activity, AlertTriangle, ShieldCheck } from "lucide-react";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Header Title */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Fleet Control Tower</h1>
          <p className="text-sm text-slate-500">Real-time multimodal logistics intelligence and event monitor.</p>
        </div>
        <div className="inline-flex items-center px-3 py-1 bg-amber-50 border border-amber-200 text-amber-800 rounded-lg text-xs font-semibold">
          <AlertTriangle className="w-3.5 h-3.5 mr-1 text-amber-600" />
          Phase 1 Integration Placeholder Mode
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="logistics-card p-5">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold">Active Lorries</span>
            <Truck className="w-4 h-4 text-brand-600" />
          </div>
          <span className="text-2xl font-bold text-slate-900">5 Vehicles</span>
          <span className="block text-xs text-slate-400 mt-1">L01 – L05 Baseline Scenario</span>
        </div>

        <div className="logistics-card p-5">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold">Total Load Volume</span>
            <Package className="w-4 h-4 text-brand-600" />
          </div>
          <span className="text-2xl font-bold text-slate-900">12 Shipments</span>
          <span className="block text-xs text-slate-400 mt-1">S01 – S12 Target Loads</span>
        </div>

        <div className="logistics-card p-5">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold">Deadline Risk</span>
            <Activity className="w-4 h-4 text-amber-500" />
          </div>
          <span className="text-2xl font-bold text-amber-600">S12 (18:00 IST)</span>
          <span className="block text-xs text-slate-400 mt-1">Monitored for delay re-optimization</span>
        </div>

        <div className="logistics-card p-5">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold">Optimization Engine</span>
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
          </div>
          <span className="text-2xl font-bold text-emerald-600">OR-Tools 9.15</span>
          <span className="block text-xs text-slate-400 mt-1">CP-SAT VRP Engine Ready</span>
        </div>
      </div>

      {/* Map & Event Feed Containers */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 logistics-card p-6 min-h-[380px] flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-900 mb-1">Live Fleet Vector Map</h3>
            <p className="text-xs text-slate-500">Mapbox GL vector rendering container for real-time lorry routes.</p>
          </div>
          <div className="my-6 py-16 bg-slate-100 border border-dashed border-slate-300 rounded-xl flex flex-col items-center justify-center text-slate-400">
            <Truck className="w-8 h-8 mb-2 text-slate-300" />
            <span className="text-sm font-medium">Map telemetry provider active. Vector routes will render in Phase 4.</span>
          </div>
          <div className="flex justify-between items-center text-xs text-slate-500 border-t border-slate-100 pt-3">
            <span>Mapbox GL JS Ready</span>
            <span>Deterministic Matrix Fallback: Active</span>
          </div>
        </div>

        <div className="logistics-card p-6 min-h-[380px] flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-900 mb-1">Operational Event Stream</h3>
            <p className="text-xs text-slate-500">Real-time driver delay, breakdown & re-optimization log.</p>
          </div>
          <div className="my-4 space-y-3">
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-600">
              <span className="font-semibold text-slate-900 block mb-0.5">Phase 1 Foundation Ready</span>
              Event stream listener configured for ATLAS voice tool callbacks.
            </div>
          </div>
          <div className="text-xs text-slate-400 border-t border-slate-100 pt-3">
            Event Taxonomy: Defined in `services/events/taxonomy.py`
          </div>
        </div>
      </div>
    </div>
  );
}
