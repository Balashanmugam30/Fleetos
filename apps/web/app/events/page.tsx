import { Activity } from "lucide-react";

export default function EventsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Operational Event Timeline</h1>
        <p className="text-sm text-slate-500">Live feed of driver delays, vehicle breakdowns, ATLAS tool calls, and re-optimization events.</p>
      </div>

      <div className="logistics-card p-6">
        <div className="flex items-center space-x-3 mb-6">
          <Activity className="w-5 h-5 text-brand-600" />
          <h3 className="text-base font-bold text-slate-900">Event Stream Audit Log</h3>
        </div>
        <div className="border-l-2 border-slate-200 pl-4 space-y-6 text-xs text-slate-600">
          <div>
            <span className="font-bold text-slate-900 block text-sm">DRIVER_DELAY_REPORTED</span>
            <span className="text-slate-400">Source: ATLAS_VOICE | Lorry: L03 | Payload: +45m loading delay</span>
            <span className="inline-block mt-1 px-2 py-0.5 bg-amber-50 text-amber-700 rounded border border-amber-200">
              Triggered Deadline Risk Check
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
