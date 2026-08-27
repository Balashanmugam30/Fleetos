import { fetchShipments, Shipment } from "@/lib/api";
import { Package, Clock, ShieldCheck } from "lucide-react";

export const revalidate = 0; // Disable static caching for real-time shipment data

export default async function ShipmentsPage() {
  const shipments: Shipment[] = await fetchShipments();

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Shipment Tracker</h1>
          <p className="text-sm text-slate-500">Persisted load weight, volume, delivery deadline & priority tracking.</p>
        </div>
        <div className="flex items-center space-x-2 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-lg">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>Real Database Persisted ({shipments.length} Loads)</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {shipments.map((s) => (
          <div key={s.id} className="logistics-card p-5 space-y-3">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center space-x-2.5">
                <div className="w-8 h-8 bg-brand-50 border border-brand-200 text-brand-600 rounded-lg flex items-center justify-center font-bold text-xs">
                  {s.id}
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Shipment {s.id}</h3>
                  <p className="text-xs text-slate-500">{s.pickup_address} → {s.destination_address}</p>
                </div>
              </div>
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                s.priority === 'URGENT' ? 'bg-red-50 text-red-700 border border-red-200' :
                s.priority === 'HIGH' ? 'bg-amber-50 text-amber-700 border border-amber-200' :
                'bg-slate-100 text-slate-700 border border-slate-200'
              }`}>
                {s.priority}
              </span>
            </div>

            <div className="grid grid-cols-3 gap-2 text-xs">
              <div className="p-2 bg-slate-50 border border-slate-200 rounded-lg">
                <span className="text-slate-400 block">Weight</span>
                <span className="font-bold text-slate-900">{s.weight_kg.toLocaleString()} kg</span>
              </div>
              <div className="p-2 bg-slate-50 border border-slate-200 rounded-lg">
                <span className="text-slate-400 block">Volume</span>
                <span className="font-bold text-slate-900">{s.volume_m3} m³</span>
              </div>
              <div className="p-2 bg-slate-50 border border-slate-200 rounded-lg">
                <span className="text-slate-400 block">Status</span>
                <span className="font-bold text-brand-600">{s.status}</span>
              </div>
            </div>

            <div className="flex items-center text-xs text-slate-500 pt-1">
              <Clock className="w-3.5 h-3.5 mr-1 text-slate-400" />
              <span>Deadline: {new Date(s.delivery_deadline).toLocaleString()}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
