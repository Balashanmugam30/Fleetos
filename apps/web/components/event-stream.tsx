"use client";

import React, { useState } from "react";
import { OperationalEvent } from "@/lib/api";
import { Activity, ChevronDown, ChevronUp, AlertTriangle, ShieldCheck, Clock } from "lucide-react";

interface EventStreamProps {
  events: OperationalEvent[];
}

export function EventStream({ events }: EventStreamProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const toggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  return (
    <div className="logistics-card p-6 space-y-4">
      <div className="flex justify-between items-center border-b border-slate-100 pb-3">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center">
            <Activity className="w-4 h-4 mr-2 text-brand-600" />
            Operational Event Stream
          </h3>
          <p className="text-xs text-slate-500">Real-time driver delay, tracking transitions & re-optimization log.</p>
        </div>
        <span className="text-xs font-mono text-slate-500 bg-slate-100 px-2.5 py-1 rounded border border-slate-200">
          Total Events: {events.length}
        </span>
      </div>

      <div className="space-y-2.5 max-h-72 overflow-y-auto pr-1">
        {events.length > 0 ? (
          events.slice(0, 10).map((evt) => {
            const isExpanded = expandedId === evt.id;
            const isWarning = evt.severity === "WARNING" || evt.event_type.includes("STALE") || evt.event_type.includes("DELAY");
            const isCritical = evt.severity === "CRITICAL" || evt.event_type.includes("OFFLINE") || evt.event_type.includes("BREAKDOWN");

            return (
              <div
                key={evt.id}
                className={`p-3 rounded-xl border transition-all text-xs ${
                  isCritical ? "bg-red-50/50 border-red-200" :
                  isWarning ? "bg-amber-50/50 border-amber-200" :
                  "bg-slate-50 border-slate-200"
                }`}
              >
                <div className="flex justify-between items-center cursor-pointer" onClick={() => toggleExpand(evt.id)}>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      isCritical ? "bg-red-100 text-red-800" :
                      isWarning ? "bg-amber-100 text-amber-800" :
                      "bg-blue-100 text-blue-800"
                    }`}>
                      {evt.event_type}
                    </span>

                    <span className="font-semibold text-slate-900">
                      {evt.lorry_id ? `Lorry ${evt.lorry_id}` : "Fleet System"}
                    </span>

                    <span className="text-[11px] text-slate-500 hidden sm:inline">
                      Source: {evt.source}
                    </span>
                  </div>

                  <div className="flex items-center space-x-2">
                    <span className="text-slate-400 font-mono text-[11px] flex items-center">
                      <Clock className="w-3 h-3 mr-1 text-slate-400" />
                      {new Date(evt.created_at).toLocaleTimeString()}
                    </span>
                    {isExpanded ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
                  </div>
                </div>

                {isExpanded && (
                  <div className="mt-3 pt-2 border-t border-slate-200/60 font-mono text-[11px] text-slate-600 bg-white/80 p-2.5 rounded-lg border border-slate-200">
                    <div className="flex justify-between text-slate-500 mb-1">
                      <span>EVENT ID: {evt.id}</span>
                      <span>STATUS: {evt.resolution_status}</span>
                    </div>
                    <pre className="text-[10px] text-slate-700 overflow-x-auto">
                      {JSON.stringify(evt.payload_json, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            );
          })
        ) : (
          <div className="p-6 text-center text-slate-400 text-xs bg-slate-50 rounded-xl border border-slate-200">
            No operational events logged yet. Start simulator or update vehicle telemetry to trigger events.
          </div>
        )}
      </div>
    </div>
  );
}
