import { Settings as SettingsIcon, Database, MapPin, Key } from "lucide-react";

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Platform Settings</h1>
        <p className="text-sm text-slate-500">API endpoints, provider credentials status, and demo configuration.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="logistics-card p-6 space-y-3">
          <div className="flex items-center space-x-2 text-slate-900 font-bold">
            <Key className="w-4 h-4 text-brand-600" />
            <h3>Telephony Integration Keys</h3>
          </div>
          <p className="text-xs text-slate-500">Vapi & Twilio API keys are isolated server-side in <code className="bg-slate-100 px-1 py-0.5 rounded">.env</code>.</p>
        </div>

        <div className="logistics-card p-6 space-y-3">
          <div className="flex items-center space-x-2 text-slate-900 font-bold">
            <MapPin className="w-4 h-4 text-brand-600" />
            <h3>Mapping & Spatial Provider</h3>
          </div>
          <p className="text-xs text-slate-500">Mapbox GL Token with Haversine Matrix Fallback.</p>
        </div>
      </div>
    </div>
  );
}
