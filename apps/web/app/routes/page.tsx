import { Route as RouteIcon } from "lucide-react";

export default function RoutesPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Route & Sequence Monitor</h1>
        <p className="text-sm text-slate-500">Multi-stop delivery sequences, estimated arrival times, fuel calculations, and cost optimization.</p>
      </div>

      <div className="logistics-card p-6 min-h-[300px] flex flex-col justify-between">
        <div className="flex items-center space-x-3 mb-4">
          <div className="w-9 h-9 bg-brand-50 border border-brand-200 text-brand-600 rounded-lg flex items-center justify-center">
            <RouteIcon className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900">Route Sequencing Engine</h3>
            <p className="text-xs text-slate-500">Phase 1 Route Contract Scaffolded</p>
          </div>
        </div>
        <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-600 space-y-2">
          <p><strong className="text-slate-900">Baseline Canonical Route:</strong> Chennai Port → Vellore Hub → Bengaluru Electronic City</p>
          <p><strong className="text-slate-900">Distance Estimation:</strong> ~345 km | <strong className="text-slate-900">Fuel Estimate:</strong> 66.3 Liters (L05 @ 5.2 km/L)</p>
        </div>
      </div>
    </div>
  );
}
