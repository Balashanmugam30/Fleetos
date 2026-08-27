"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { PhoneCall, ShieldCheck, ArrowRight, Globe } from "lucide-react";
import { VoiceHealth, CallRecord, fetchVoiceHealth, initiateDriverCall, fetchCallRecords } from "@/lib/api";

export function AtlasVoiceCard() {
  const [health, setHealth] = useState<VoiceHealth | null>(null);
  const [callRecords, setCallRecords] = useState<CallRecord[]>([]);
  const [selectedDriver, setSelectedDriver] = useState<string>("D03");
  const [calling, setCalling] = useState<boolean>(false);
  const [lastCallOutcome, setLastCallOutcome] = useState<string | null>(null);

  const loadVoiceData = async () => {
    try {
      const [hRes, cRes] = await Promise.all([
        fetchVoiceHealth(),
        fetchCallRecords(5)
      ]);
      setHealth(hRes);
      setCallRecords(cRes);
    } catch (err) {
      console.error("Error loading voice card data:", err);
    }
  };

  useEffect(() => {
    loadVoiceData();
    const interval = setInterval(loadVoiceData, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleCallDriver = async () => {
    setCalling(true);
    setLastCallOutcome(null);
    try {
      const record = await initiateDriverCall(selectedDriver, "STATUS_CHECK", "Routine dispatcher status check");
      if (record) {
        setLastCallOutcome(`Call initiated to ${record.driver_id} (Status: ${record.status})`);
      }
      await loadVoiceData();
    } catch (err: any) {
      setLastCallOutcome(`Call failed: ${err.message || "Conflict or network error"}`);
    } finally {
      setCalling(false);
    }
  };

  const isRealMode = health?.mode === "REAL" && health?.configured;
  const latestCall = callRecords[0] || null;

  return (
    <div className="logistics-card p-6 space-y-4 flex flex-col justify-between">
      <div>
        <div className="flex justify-between items-center border-b border-slate-100 pb-3 mb-3">
          <div>
            <h3 className="text-base font-bold text-slate-900 flex items-center">
              <Globe className="w-4 h-4 mr-2 text-brand-600" />
              ATLAS — SARVAM VOICE AGENT
            </h3>
            <p className="text-xs text-slate-500">Sarvam Multilingual Indic AI & Twilio PSTN call dispatch.</p>
          </div>

          <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
            isRealMode ? "bg-emerald-50 text-emerald-700 border border-emerald-200" : "bg-blue-50 text-blue-700 border border-blue-200"
          }`}>
            {isRealMode ? "SARVAM REAL VOICE ACTIVE" : "DEMO TELEPHONY MODE"}
          </span>
        </div>

        {/* Quick Driver Dispatch Control Bar */}
        <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-2 text-xs">
          <div className="flex justify-between items-center">
            <span className="font-semibold text-slate-700">Dispatch Outbound Call:</span>
            <select
              value={selectedDriver}
              onChange={(e) => setSelectedDriver(e.target.value)}
              className="bg-white border border-slate-300 rounded px-2 py-1 font-semibold text-slate-900 text-xs"
            >
              <option value="D01">Driver D01 (Lorry L01)</option>
              <option value="D02">Driver D02 (Lorry L02)</option>
              <option value="D03">Driver D03 (Lorry L03)</option>
              <option value="D04">Driver D04 (Lorry L04)</option>
              <option value="D05">Driver D05 (Lorry L05)</option>
            </select>
          </div>

          <button
            onClick={handleCallDriver}
            disabled={calling}
            className="w-full inline-flex items-center justify-center px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors disabled:opacity-50"
          >
            <PhoneCall className="w-3.5 h-3.5 mr-1.5" />
            {calling ? "Connecting ATLAS..." : `Call ${selectedDriver} with ATLAS`}
          </button>

          {lastCallOutcome && (
            <p className="text-[11px] font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 p-2 rounded text-center">
              {lastCallOutcome}
            </p>
          )}
        </div>

        {/* Recent Call Status */}
        {latestCall && (
          <div className="mt-3 p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1 text-xs">
            <div className="flex justify-between font-semibold">
              <span className="text-slate-600">Last Outbound Call:</span>
              <span className="text-brand-600">{latestCall.driver_id} ({latestCall.call_type})</span>
            </div>
            <div className="flex justify-between text-slate-500 text-[11px]">
              <span>Provider: {latestCall.provider} | Status: {latestCall.status}</span>
              <span className="font-mono text-slate-400">{new Date(latestCall.created_at).toLocaleTimeString()}</span>
            </div>
          </div>
        )}
      </div>

      <div className="pt-2 border-t border-slate-100">
        <Link
          href="/ai"
          className="w-full inline-flex items-center justify-center px-4 py-2 bg-brand-50 hover:bg-brand-100 text-brand-700 font-semibold text-xs rounded-lg border border-brand-200 transition-colors"
        >
          Open ATLAS Voice Operations Center
          <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
        </Link>
      </div>
    </div>
  );
}
