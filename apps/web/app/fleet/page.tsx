import { fetchLorries, Lorry } from "@/lib/api";
import { Truck, ShieldCheck, RefreshCw } from "lucide-react";

export const revalidate = 0; // Disable static caching for real-time fleet data

export default async function FleetPage() {
  const lorries: Lorry[] = await fetchLorries();

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Fleet Management</h1>
          <p className="text-sm text-slate-500">Live vehicle capacity, assigned drivers, fuel efficiency & status matrix.</p>
        </div>
        <div className="flex items-center space-x-2 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-lg">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>Real Backend Database Persisted</span>
        </div>
      </div>

      <div className="logistics-card overflow-hidden">
        <table className="min-w-full divide-y divide-slate-200 text-left text-sm">
          <thead className="bg-slate-50 text-slate-500 font-semibold text-xs uppercase tracking-wider">
            <tr>
              <th className="px-6 py-3">Lorry ID</th>
              <th className="px-6 py-3">Registration</th>
              <th className="px-6 py-3">Capacity (Weight / Vol)</th>
              <th className="px-6 py-3">Fuel Efficiency</th>
              <th className="px-6 py-3">Driver ID</th>
              <th className="px-6 py-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 bg-white text-slate-700">
            {lorries.length > 0 ? (
              lorries.map((l) => (
                <tr key={l.id} className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-4 font-bold text-slate-900 flex items-center">
                    <Truck className="w-4 h-4 mr-2 text-brand-600" />
                    {l.id}
                  </td>
                  <td className="px-6 py-4 font-mono text-xs">{l.registration_number}</td>
                  <td className="px-6 py-4">{l.max_weight_kg.toLocaleString()} kg / {l.max_volume_m3} m³</td>
                  <td className="px-6 py-4 font-semibold text-slate-900">{l.fuel_efficiency_km_l} km/L</td>
                  <td className="px-6 py-4">{l.driver_id || "Unassigned"}</td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                      l.status === 'EN_ROUTE' ? 'bg-blue-50 text-blue-700 border border-blue-200' :
                      l.status === 'IDLE' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' :
                      l.status === 'LOADING' ? 'bg-amber-50 text-amber-700 border border-amber-200' :
                      'bg-slate-100 text-slate-600 border border-slate-200'
                    }`}>
                      {l.status}
                    </span>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={6} className="px-6 py-8 text-center text-slate-400">
                  No lorry records retrieved from backend API. Run <code className="bg-slate-100 px-1 py-0.5 rounded">python scripts/seed_database.py</code> to populate.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
