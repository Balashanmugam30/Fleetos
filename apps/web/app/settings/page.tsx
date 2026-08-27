"use client";

import React, { useState, useEffect } from "react";
import { Key, MapPin, PhoneCall, ShieldCheck, CheckCircle2, XCircle } from "lucide-react";
import { fetchVoiceHealth, VoiceHealth } from "@/lib/api";

export default function SettingsPage() {
  const [health, setHealth] = useState<VoiceHealth | null>(null);

  useEffect(() => {
    fetchVoiceHealth().then(setHealth).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Platform Settings & Operations Readiness</h1>
        <p className="text-sm text-slate-500">API endpoints, Twilio ConversationRelay telephony, OpenAI ATLAS engine & demo configuration.</p>
      </div>

      {/* Voice Telephony Readiness Panel */}
      <div className="logistics-card p-6 space-y-4">
        <div className="flex justify-between items-center border-b border-slate-100 pb-3">
          <div>
            <h3 className="text-base font-bold text-slate-900 flex items-center">
              <PhoneCall className="w-4 h-4 mr-2 text-brand-600" />
              ATLAS — Twilio ConversationRelay Voice Configuration
            </h3>
            <p className="text-xs text-slate-500">PSTN telephony ingress, OpenAI reasoning model & WebSocket stream readiness.</p>
          </div>

          <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
            health?.mode === "REAL" ? "bg-emerald-50 text-emerald-700 border border-emerald-200" : "bg-blue-50 text-blue-700 border border-blue-200"
          }`}>
            {health?.mode === "REAL" ? "PSTN REAL MODE READY" : "DEMO TELEPHONY MODE"}
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-xs">
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
            <div className="flex justify-between items-center font-semibold">
              <span className="text-slate-600">Twilio Account:</span>
              {health?.twilio_configured ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <XCircle className="w-4 h-4 text-slate-400" />}
            </div>
            <p className="text-[11px] text-slate-500">{health?.twilio_configured ? "Account SID & Auth Token Set" : "Using Demo Telephony"}</p>
          </div>

          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
            <div className="flex justify-between items-center font-semibold">
              <span className="text-slate-600">OpenAI ATLAS Engine:</span>
              {health?.openai_configured ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <XCircle className="w-4 h-4 text-slate-400" />}
            </div>
            <p className="text-[11px] text-slate-500">{health?.openai_configured ? "API Key Configured" : "Fallback Responses"}</p>
          </div>

          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
            <div className="flex justify-between items-center font-semibold">
              <span className="text-slate-600">Public Webhook:</span>
              {health?.public_webhook_configured ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <XCircle className="w-4 h-4 text-slate-400" />}
            </div>
            <p className="text-[11px] text-slate-500">{health?.public_webhook_configured ? "Public Ingress Active" : "Local HTTP Endpoint"}</p>
          </div>

          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
            <div className="flex justify-between items-center font-semibold">
              <span className="text-slate-600">WebSocket Relay:</span>
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            </div>
            <p className="text-[11px] text-slate-500">wss:// ConversationRelay</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="logistics-card p-6 space-y-3">
          <div className="flex items-center space-x-2 text-slate-900 font-bold">
            <Key className="w-4 h-4 text-brand-600" />
            <h3>Telephony Integration Keys</h3>
          </div>
          <p className="text-xs text-slate-500">Twilio Account SID, Auth Token & OpenAI credentials are isolated server-side in <code className="bg-slate-100 px-1 py-0.5 rounded">.env</code>.</p>
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
