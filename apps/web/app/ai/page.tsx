"use client";

import React, { useState, useEffect } from "react";
import {
  fetchVoiceHealth,
  initiateDriverCall,
  fetchCallRecords,
  fetchEvents,
  VoiceHealth,
  CallRecord,
  OperationalEvent
} from "@/lib/api";
import { PhoneCall, ShieldCheck, Globe, Activity, CheckCircle2, AlertTriangle } from "lucide-react";

export default function AIPage() {
  const [health, setHealth] = useState<VoiceHealth | null>(null);
  const [callRecords, setCallRecords] = useState<CallRecord[]>([]);
  const [events, setEvents] = useState<OperationalEvent[]>([]);
  const [selectedDriver, setSelectedDriver] = useState<string>("D03");
  const [selectedType, setSelectedType] = useState<string>("STATUS_CHECK");
  const [selectedLanguage, setSelectedLanguage] = useState<string>("AUTO");
  const [contextNotes, setContextNotes] = useState<string>("Routine status check on current load progression");
  const [calling, setCalling] = useState<boolean>(false);
  const [outcomeMessage, setOutcomeMessage] = useState<string | null>(null);

  const loadData = async () => {
    try {
      const [hRes, cRes, eRes] = await Promise.all([
        fetchVoiceHealth(),
        fetchCallRecords(20),
        fetchEvents()
      ]);
      const dedupedCalls = (cRes || []).filter((call, index, self) =>
        index === self.findIndex((t) => t.id === call.id)
      );
      setHealth(hRes);
      setCallRecords(dedupedCalls);
      setEvents(eRes.filter(e => e.source === "ATLAS_VOICE" || e.event_type.includes("CALL") || e.event_type.includes("DELAY")));
    } catch (err) {
      console.error("Error loading ATLAS Voice Operations data:", err);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleDispatchCall = async (e: React.FormEvent) => {
    e.preventDefault();
    setCalling(true);
    setOutcomeMessage(null);
    try {
      const record = await initiateDriverCall(selectedDriver, selectedType, contextNotes);
      if (record) {
        setOutcomeMessage(`Call dispatched successfully! Call ID: ${record.id} (Status: ${record.status})`);
      }
      await loadData();
    } catch (err: any) {
      setOutcomeMessage(`Call dispatch error: ${err.message || "Driver already has an active call in progress."}`);
    } finally {
      setCalling(false);
    }
  };

  const isRealMode = health?.mode === "REAL" && health?.configured;
  const isTrialSandbox = health?.twilio_credentials_valid && (health?.twilio_provisioned_number_count === 0);

  return (
    <div className="space-y-6">
      {/* Header & Readiness Banner */}
      <div className="flex flex-wrap justify-between items-center gap-4 bg-white border border-slate-200 p-6 rounded-2xl shadow-sm">
        <div>
          <div className="inline-flex items-center space-x-2 px-3 py-1 bg-brand-50 border border-brand-200 text-brand-700 rounded-full text-xs font-semibold mb-2">
            <span>SEE → HEAR → THINK → OPTIMIZE → ACT → UPDATE</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center">
            <Globe className="w-6 h-6 mr-2 text-brand-600" />
            ATLAS — Sarvam Multilingual Voice Agent Operations Center
          </h1>
          <p className="text-sm text-slate-500">
            Sarvam Indic AI Voice Agent, Twilio PSTN telephony, multilingual code-mixing & Fleetos tool execution.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className={`flex items-center space-x-2 text-xs font-semibold px-3.5 py-2 rounded-xl border ${
            isRealMode ? "bg-emerald-50 text-emerald-700 border-emerald-200" : "bg-blue-50 text-blue-700 border-blue-200"
          }`}>
            <ShieldCheck className="w-4 h-4" />
            <span>{isRealMode ? "SARVAM REAL VOICE ACTIVE" : "DEMO TELEPHONY MODE"}</span>
          </div>
        </div>
      </div>

      {/* Trial Phone Sandbox Informational Alert */}
      {isTrialSandbox && (
        <div className="p-4 bg-amber-50 border border-amber-200 rounded-2xl text-xs space-y-1">
          <div className="flex items-center space-x-2 font-bold text-amber-900">
            <AlertTriangle className="w-4 h-4 text-amber-600 flex-shrink-0" />
            <span>Twilio Trial Account Detected (IncomingPhoneNumbers = 0)</span>
          </div>
          <p className="text-amber-800 leading-relaxed pl-6">
            Twilio "Try Out Voice" sandbox numbers cannot be imported into Sarvam Voice Agents because Twilio's Inventory API returns 0 provisioned phone numbers. Importing into Sarvam requires a provisioned Twilio phone number ($1/mo). Fleetos is running safely in <strong>Demo Telephony Mode</strong>.
          </p>
        </div>
      )}

      {/* Driver Outbound Call Launcher Form */}
      <div className="logistics-card p-6 space-y-4">
        <div className="flex justify-between items-center border-b border-slate-100 pb-3">
          <div>
            <h3 className="text-base font-bold text-slate-900 flex items-center">
              <PhoneCall className="w-4 h-4 mr-2 text-brand-600" />
              Dispatch Outbound Multilingual Driver Call
            </h3>
            <p className="text-xs text-slate-500">Initiate an automated Sarvam Indic conversational call to a driver's mobile phone.</p>
          </div>

          <span className="text-xs font-mono text-slate-500 bg-slate-100 px-2.5 py-1 rounded border border-slate-200">
            Target Region: India (+91)
          </span>
        </div>

        <form onSubmit={handleDispatchCall} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Target Driver</label>
              <select
                value={selectedDriver}
                onChange={(e) => setSelectedDriver(e.target.value)}
                className="w-full bg-white border border-slate-300 rounded-lg p-2.5 text-xs font-semibold text-slate-900"
              >
                <option value="D01">Driver D01 (Rajesh Kumar — Lorry L01)</option>
                <option value="D02">Driver D02 (Suresh V — Lorry L02)</option>
                <option value="D03">Driver D03 (Vikram Singh — Lorry L03)</option>
                <option value="D04">Driver D04 (Arun Prasad — Lorry L04)</option>
                <option value="D05">Driver D05 (Karthik R — Lorry L05)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Indic Voice Language</label>
              <select
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="w-full bg-white border border-slate-300 rounded-lg p-2.5 text-xs font-semibold text-slate-900"
              >
                <option value="AUTO">AUTO (Automatic Detection / Code-Mixing)</option>
                <option value="ta-IN">Tamil (தமிழ் / Tanglish)</option>
                <option value="hi-IN">Hindi (हिंदी / Hinglish)</option>
                <option value="en-IN">English (Indian Accent)</option>
                <option value="te-IN">Telugu (తెలుగు)</option>
                <option value="kn-IN">Kannada (ಕನ್ನಡ)</option>
                <option value="ml-IN">Malayalam (മലയാളം)</option>
                <option value="bn-IN">Bengali (বাংলা)</option>
                <option value="mr-IN">Marathi (मराठी)</option>
                <option value="gu-IN">Gujarati (ગુજરાતી)</option>
                <option value="pa-IN">Punjabi (ਪੰਜਾਬੀ)</option>
                <option value="or-IN">Odia (ଓଡ଼ିଆ)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Call Purpose / Scenario</label>
              <select
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                className="w-full bg-white border border-slate-300 rounded-lg p-2.5 text-xs font-semibold text-slate-900"
              >
                <option value="STATUS_CHECK">STATUS_CHECK (Routine delivery progress)</option>
                <option value="DELAY_REPORT">DELAY_REPORT (Report loading or traffic delay)</option>
                <option value="BREAKDOWN_REPORT">BREAKDOWN_REPORT (Emergency vehicle failure)</option>
                <option value="ASSIGNMENT_CONFIRMATION">ASSIGNMENT_CONFIRMATION (Confirm next route)</option>
                <option value="DELIVERY_CONFIRMATION">DELIVERY_CONFIRMATION (Confirm load delivered)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Context Notes for ATLAS</label>
              <input
                type="text"
                value={contextNotes}
                onChange={(e) => setContextNotes(e.target.value)}
                className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs text-slate-900"
                placeholder="e.g. Check ETA for S12 delivery in Coimbatore"
              />
            </div>
          </div>

          <div className="flex justify-between items-center pt-2">
            <span className="text-xs text-slate-400 font-mono">
              Active Provider: {isRealMode ? "SARVAM REAL VOICE" : "DEMO TELEPHONY MODE"}
            </span>

            <button
              type="submit"
              disabled={calling}
              className="inline-flex items-center px-5 py-2.5 bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs rounded-xl shadow-sm transition-colors disabled:opacity-50"
            >
              <PhoneCall className="w-4 h-4 mr-2" />
              {calling ? "Connecting ATLAS Call..." : `Dispatch ATLAS Call to ${selectedDriver}`}
            </button>
          </div>
        </form>

        {outcomeMessage && (
          <div className={`p-3 rounded-xl text-xs font-semibold flex items-center space-x-2 ${
            outcomeMessage.includes("error") ? "bg-red-50 text-red-700 border border-red-200" : "bg-emerald-50 text-emerald-700 border border-emerald-200"
          }`}>
            <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
            <span>{outcomeMessage}</span>
          </div>
        )}
      </div>

      {/* Call History Matrix */}
      <div className="logistics-card p-6 space-y-4">
        <div className="flex justify-between items-center border-b border-slate-100 pb-3">
          <div>
            <h3 className="text-base font-bold text-slate-900">ATLAS Telephony Call History</h3>
            <p className="text-xs text-slate-500">Log of dispatched voice calls, status, provider, and tool outcomes.</p>
          </div>
          <span className="text-xs font-mono text-slate-500">Total Calls: {callRecords.length}</span>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 text-left text-xs">
            <thead className="bg-slate-50 text-slate-500 font-semibold uppercase tracking-wider">
              <tr>
                <th className="px-4 py-2.5">Call ID</th>
                <th className="px-4 py-2.5">Driver</th>
                <th className="px-4 py-2.5">Lorry</th>
                <th className="px-4 py-2.5">Purpose</th>
                <th className="px-4 py-2.5">Provider</th>
                <th className="px-4 py-2.5">Status</th>
                <th className="px-4 py-2.5">Duration</th>
                <th className="px-4 py-2.5">Dispatched At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 bg-white text-slate-700">
              {callRecords.length > 0 ? (
                callRecords.map((c) => (
                  <tr key={c.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-4 py-3 font-mono font-bold text-slate-900">{c.id}</td>
                    <td className="px-4 py-3 font-semibold">{c.driver_id}</td>
                    <td className="px-4 py-3 font-semibold text-brand-600">{c.lorry_id || (c.driver_id ? `L0${c.driver_id.slice(-1)}` : "L01")}</td>
                    <td className="px-4 py-3">{c.call_type}</td>
                    <td className="px-4 py-3 font-mono">{c.provider}</td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex px-2 py-0.5 rounded text-[11px] font-bold ${
                        c.status === "COMPLETED" ? "bg-emerald-50 text-emerald-700 border border-emerald-200" :
                        c.status === "IN_PROGRESS" || c.status === "RINGING" ? "bg-blue-50 text-blue-700 border border-blue-200 animate-pulse" :
                        "bg-red-50 text-red-700 border border-red-200"
                      }`}>
                        {c.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-mono">{c.duration_seconds}s</td>
                    <td className="px-4 py-3 font-mono text-slate-400">{new Date(c.created_at).toLocaleTimeString()}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={8} className="px-4 py-8 text-center text-slate-400 text-xs">
                    No voice calls dispatched yet. Click "Dispatch ATLAS Call" above to initiate a call.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
