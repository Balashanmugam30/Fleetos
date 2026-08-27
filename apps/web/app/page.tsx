import Link from "next/link";
import { Truck, PhoneCall, Cpu, Camera, ArrowRight, CheckCircle2 } from "lucide-react";

export default function HomePage() {
  return (
    <div className="space-y-8">
      {/* Hero Banner */}
      <div className="bg-white border border-slate-200 rounded-2xl p-8 sm:p-12 shadow-sm">
        <div className="max-w-3xl space-y-4">
          <div className="inline-flex items-center space-x-2 px-3 py-1 bg-brand-50 border border-brand-200 rounded-full text-brand-700 text-xs font-semibold">
            <span>Agentic Multimodal Fleet Intelligence Platform</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            Fleetos doesn&apos;t just plan the trip. It watches the fleet, listens to the drivers, and changes the plan when reality changes.
          </h1>
          <p className="text-base sm:text-lg text-slate-600 leading-relaxed">
            A unified operating intelligence layer for logistics powered by deterministic Google OR-Tools optimization, ATLAS AI voice telephony, and augmented reality visualization.
          </p>
          <div className="pt-4 flex flex-wrap gap-4">
            <Link
              href="/dashboard"
              className="inline-flex items-center px-5 py-2.5 bg-brand-600 hover:bg-brand-700 text-white font-semibold text-sm rounded-lg shadow-sm transition-colors"
            >
              Open Command Tower
              <ArrowRight className="w-4 h-4 ml-2" />
            </Link>
            <Link
              href="/ai"
              className="inline-flex items-center px-5 py-2.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold text-sm rounded-lg shadow-sm transition-colors"
            >
              <PhoneCall className="w-4 h-4 mr-2 text-brand-600" />
              ATLAS Telephony Agent
            </Link>
          </div>
        </div>
      </div>

      {/* Core Loop Architecture Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="logistics-card p-6 space-y-3">
          <div className="w-10 h-10 bg-blue-50 border border-blue-200 text-blue-600 rounded-lg flex items-center justify-center font-bold">
            <Camera className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-slate-900">1. SEE — Visual AR Overlay</h3>
          <p className="text-sm text-slate-600">
            Cinemorph-inspired camera overlays anchor live lorry telemetry, risk badges, and assigned shipments directly in physical space.
          </p>
        </div>

        <div className="logistics-card p-6 space-y-3">
          <div className="w-10 h-10 bg-purple-50 border border-purple-200 text-purple-600 rounded-lg flex items-center justify-center font-bold">
            <PhoneCall className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-slate-900">2. HEAR — ATLAS Voice AI</h3>
          <p className="text-sm text-slate-600">
            Outbound PSTN telephone calling via Vapi & Twilio directly to drivers&apos; mobile phones to extract real-time delay events.
          </p>
        </div>

        <div className="logistics-card p-6 space-y-3">
          <div className="w-10 h-10 bg-emerald-50 border border-emerald-200 text-emerald-600 rounded-lg flex items-center justify-center font-bold">
            <Cpu className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-slate-900">3. OPTIMIZE — Deterministic VRP</h3>
          <p className="text-sm text-slate-600">
            Google OR-Tools solver algorithm deterministically optimizes multi-vehicle load allocation, capacities, fuel efficiency, and deadlines.
          </p>
        </div>
      </div>

      {/* Phase 1 Verification Status */}
      <div className="logistics-card p-6 space-y-4">
        <h2 className="text-lg font-bold text-slate-900 flex items-center">
          <CheckCircle2 className="w-5 h-5 text-emerald-500 mr-2" />
          Phase 1 Foundation Readiness Status
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-medium text-slate-600">
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
            <span className="block text-slate-400">FastAPI Server</span>
            <span className="font-semibold text-emerald-700">Operational</span>
          </div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
            <span className="block text-slate-400">OR-Tools 9.15</span>
            <span className="font-semibold text-emerald-700">Verified</span>
          </div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
            <span className="block text-slate-400">Vapi/Twilio Gateway</span>
            <span className="font-semibold text-emerald-700">Contract Ready</span>
          </div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
            <span className="block text-slate-400">WebAR Component</span>
            <span className="font-semibold text-emerald-700">Scaffolded</span>
          </div>
        </div>
      </div>
    </div>
  );
}
