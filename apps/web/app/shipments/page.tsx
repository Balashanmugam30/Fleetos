import { Package, Clock } from "lucide-react";

export default function ShipmentsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Shipment Tracker</h1>
        <p className="text-sm text-slate-500">Weight, volume, delivery deadline, priority, and destination tracking.</p>
      </div>

      <div className="logistics-card p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-amber-50 border border-amber-200 text-amber-600 rounded-lg flex items-center justify-center font-bold">
              <Package className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-900">Shipment S12 (Target Anchor Load)</h3>
              <p className="text-xs text-slate-500">Destination: Bengaluru Electronic City | Pickup: Chennai Port</p>
            </div>
          </div>
          <span className="px-3 py-1 bg-red-50 text-red-700 border border-red-200 rounded-full text-xs font-bold flex items-center">
            <Clock className="w-3.5 h-3.5 mr-1" />
            Strict Deadline: 18:00 IST
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
            <span className="text-slate-400 block">Weight Load</span>
            <span className="font-bold text-slate-900 text-sm">3,500 kg</span>
          </div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
            <span className="text-slate-400 block">Volume Load</span>
            <span className="font-bold text-slate-900 text-sm">14.0 m³</span>
          </div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
            <span className="text-slate-400 block">Initial Vehicle</span>
            <span className="font-bold text-slate-900 text-sm">Lorry L03</span>
          </div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
            <span className="text-slate-400 block">Reassignment Target</span>
            <span className="font-bold text-brand-600 text-sm">Lorry L05 (Vellore)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
