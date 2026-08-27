import { Truck, ShieldCheck } from "lucide-react";

export default function FleetPage() {
  const lorries = [
    { id: "L01", reg: "KA-01-EQ-1001", cap: "10,000 kg / 45 m³", fuel: "3.5 km/L", driver: "Driver Anand", status: "EN_ROUTE" },
    { id: "L02", reg: "KA-01-EQ-1002", cap: "15,000 kg / 60 m³", fuel: "2.8 km/L", driver: "Driver Suresh", status: "EN_ROUTE" },
    { id: "L03", reg: "TN-02-AB-3003", cap: "8,000 kg / 35 m³", fuel: "4.2 km/L", driver: "Driver Rajesh", status: "EN_ROUTE" },
    { id: "L04", reg: "AP-03-CD-4004", cap: "12,000 kg / 50 m³", fuel: "3.0 km/L", driver: "Driver Vikram", status: "UNAVAILABLE" },
    { id: "L05", reg: "TN-09-XY-5005", cap: "14,000 kg / 55 m³", fuel: "5.2 km/L", driver: "Driver Karthik", status: "IDLE" },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Fleet Management</h1>
        <p className="text-sm text-slate-500">Lorry capacity, driver assignment, fuel efficiency & availability matrix.</p>
      </div>

      <div className="logistics-card overflow-hidden">
        <table className="min-w-full divide-y divide-slate-200 text-left text-sm">
          <thead className="bg-slate-50 text-slate-500 font-semibold text-xs uppercase tracking-wider">
            <tr>
              <th className="px-6 py-3">Lorry ID</th>
              <th className="px-6 py-3">Registration</th>
              <th className="px-6 py-3">Capacity (Weight / Vol)</th>
              <th className="px-6 py-3">Fuel Efficiency</th>
              <th className="px-6 py-3">Assigned Driver</th>
              <th className="px-6 py-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 bg-white text-slate-700">
            {lorries.map((l) => (
              <tr key={l.id} className="hover:bg-slate-50 transition-colors">
                <td className="px-6 py-4 font-bold text-slate-900 flex items-center">
                  <Truck className="w-4 h-4 mr-2 text-brand-600" />
                  {l.id}
                </td>
                <td className="px-6 py-4 font-mono text-xs">{l.reg}</td>
                <td className="px-6 py-4">{l.cap}</td>
                <td className="px-6 py-4 font-semibold text-slate-900">{l.fuel}</td>
                <td className="px-6 py-4">{l.driver}</td>
                <td className="px-6 py-4">
                  <span className={`inline-flex px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                    l.status === 'EN_ROUTE' ? 'bg-blue-50 text-blue-700 border border-blue-200' :
                    l.status === 'IDLE' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' :
                    'bg-slate-100 text-slate-600 border border-slate-200'
                  }`}>
                    {l.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
