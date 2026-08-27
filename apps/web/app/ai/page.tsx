import { PhoneCall, ShieldAlert } from "lucide-react";

export default function AIPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">ATLAS Operational Voice AI</h1>
        <p className="text-sm text-slate-500">Real PSTN outbound telephony call dispatch and driver voice agent integration.</p>
      </div>

      <div className="logistics-card p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div className="flex items-center space-x-3">
            <PhoneCall className="w-6 h-6 text-brand-600" />
            <div>
              <h3 className="text-base font-bold text-slate-900">ATLAS Voice Telephony Gateway</h3>
              <p className="text-xs text-slate-500">Vapi Outbound REST API + Twilio PSTN Gateway</p>
            </div>
          </div>
          <span className="px-3 py-1 bg-blue-50 text-blue-700 border border-blue-200 rounded-full text-xs font-bold">
            Real PSTN Target
          </span>
        </div>

        <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-800 flex items-start space-x-2">
          <ShieldAlert className="w-4 h-4 text-amber-600 mt-0.5 shrink-0" />
          <div>
            <strong className="block font-semibold">Real Mobile Calling Configuration Required:</strong>
            To trigger live outbound phone calls to physical Indian mobile numbers (+91), provide <code className="bg-amber-100 px-1 py-0.5 rounded text-amber-900">VAPI_API_KEY</code> and <code className="bg-amber-100 px-1 py-0.5 rounded text-amber-900">TWILIO_ACCOUNT_SID</code> in your local <code className="bg-amber-100 px-1 py-0.5 rounded text-amber-900">.env</code> configuration file.
          </div>
        </div>
      </div>
    </div>
  );
}
