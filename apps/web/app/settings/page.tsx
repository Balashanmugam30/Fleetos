"use client";

import React, { useState, useEffect } from "react";
import { Key, MapPin, PhoneCall, ShieldCheck, CheckCircle2, XCircle, Globe, AlertTriangle } from "lucide-react";
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
        <p className="text-sm text-slate-500">API endpoints, Sarvam Voice Agent Indic AI, Twilio PSTN telephony & demo configuration.</p>
      </div>

      {/* Voice Telephony Readiness Panel */}
      <div className="logistics-card p-6 space-y-4">
        <div className="flex justify-between items-center border-b border-slate-100 pb-3">
          <div>
            <h3 className="text-base font-bold text-slate-900 flex items-center">
              <Globe className="w-4 h-4 mr-2 text-brand-600" />
              ATLAS — Sarvam Multilingual Voice Agent Configuration
            </h3>
            <p className="text-xs text-slate-500">Sarvam Indic ASR/TTS/NLU voice agents, Twilio PSTN telephony & tool webhook execution.</p>
          </div>

          <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
            health?.mode === "REAL" ? "bg-emerald-50 text-emerald-700 border border-emerald-200" : "bg-blue-50 text-blue-700 border border-blue-200"
          }`}>
            {health?.mode === "REAL" ? "SARVAM REAL MODE READY" : "DEMO TELEPHONY MODE"}
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-xs">
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
            <div className="flex justify-between items-center font-semibold">
              <span className="text-slate-600">Sarvam AI Agent:</span>
              {health?.sarvam_configured ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <XCircle className="w-4 h-4 text-slate-400" />}
            </div>
            <p className="text-[11px] text-slate-500">{health?.sarvam_configured ? "Sarvam API Key Set" : "Using Demo Telephony"}</p>
          </div>

          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
            <div className="flex justify-between items-center font-semibold">
              <span className="text-slate-600">Twilio Telephony:</span>
              {health?.twilio_credentials_valid ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <XCircle className="w-4 h-4 text-slate-400" />}
            </div>
            <p className="text-[11px] text-slate-500">{health?.twilio_credentials_valid ? "Twilio SID & Auth Valid" : "Simulated PSTN"}</p>
          </div>

          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
            <div className="flex justify-between items-center font-semibold">
              <span className="text-slate-600">Provisioned Numbers:</span>
              {health?.twilio_provisioned_number_count ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <AlertTriangle className="w-4 h-4 text-amber-600" />}
            </div>
            <p className="text-[11px] text-slate-500">
              {health?.twilio_provisioned_number_count ? `${health.twilio_provisioned_number_count} Incoming Numbers` : "0 Numbers (Trial Sandbox)"}
            </p>
          </div>

          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
            <div className="flex justify-between items-center font-semibold">
              <span className="text-slate-600">Sarvam Import Status:</span>
              {health?.sarvam_number_imported ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <XCircle className="w-4 h-4 text-slate-400" />}
            </div>
            <p className="text-[11px] text-slate-500">{health?.sarvam_number_imported ? "Number Imported" : "Requires Provisioned Number"}</p>
          </div>
        </div>

        {/* Informational Box for Twilio Trial Phone Limitation */}
        {health?.twilio_credentials_valid && (health?.twilio_provisioned_number_count === 0) && (
          <div className="p-3.5 bg-amber-50 border border-amber-200 rounded-xl text-xs space-y-1">
            <span className="font-bold text-amber-900 flex items-center">
              <AlertTriangle className="w-4 h-4 mr-1.5 text-amber-600" />
              Twilio Trial "Try Out Voice" Sandbox Notice
            </span>
            <p className="text-amber-800 text-[11px] leading-relaxed">
              Twilio trial accounts supply sandbox test numbers which work for Twilio's internal API test flows, but return 0 numbers under Twilio's <code>IncomingPhoneNumbers.json</code> inventory API. Sarvam BYO Twilio requires an exclusive provisioned phone number ($1/mo on an upgraded Twilio account).
            </p>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="logistics-card p-6 space-y-3">
          <div className="flex items-center space-x-2 text-slate-900 font-bold">
            <Key className="w-4 h-4 text-brand-600" />
            <h3>Telephony & AI Integration Keys</h3>
          </div>
          <p className="text-xs text-slate-500">Sarvam API key, Agent ID & Twilio credentials are isolated server-side in <code className="bg-slate-100 px-1 py-0.5 rounded">.env</code>.</p>
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
