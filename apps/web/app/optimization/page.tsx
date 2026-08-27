import { Cpu, ShieldCheck } from "lucide-react";

export default function OptimizationPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Deterministic Optimization Control</h1>
        <p className="text-sm text-slate-500">Google OR-Tools CP-SAT vehicle routing engine status and execution triggers.</p>
      </div>

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
          <p><strong className="text-slate-900">Mathematical Model:</strong> Multi-Vehicle Routing Problem with Capacity & Time Windows (CVRP-TW)</p>
          <p><strong className="text-slate-900">Constraints Evaluated:</strong> Lorry Weight Limit, Volume Capacity, Time Windows (Deadlines), Driver Availability, Fuel Efficiency (km/L), Priority Penalties</p>
        </div>
      </div>
    </div>
  );
}
