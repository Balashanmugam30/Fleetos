"use client";

import React, { useState, useEffect } from "react";
import { fetchEvents, OperationalEvent } from "@/lib/api";
import { EventStream } from "@/components/event-stream";
import { Activity, ShieldCheck, Filter } from "lucide-react";

export default function EventsPage() {
  const [events, setEvents] = useState<OperationalEvent[]>([]);
  const [severityFilter, setSeverityFilter] = useState<string>("ALL");
  const [loading, setLoading] = useState<boolean>(true);

  const loadEventData = async () => {
    try {
      const evtRes = await fetchEvents();
      setEvents(evtRes);
    } catch (err) {
      console.error("Error loading events:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEventData();
    const interval = setInterval(loadEventData, 5000);
    return () => clearInterval(interval);
  }, []);

  const filteredEvents = events.filter((e) => {
    if (severityFilter === "ALL") return true;
    return e.severity === severityFilter;
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Operational Event Stream & Timeline</h1>
          <p className="text-sm text-slate-500">Real-time driver delay, breakdown, tracking state transitions & re-optimization log.</p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1 bg-white border border-slate-200 p-1 rounded-xl text-xs">
            {["ALL", "INFO", "WARNING", "CRITICAL"].map((sev) => (
              <button
                key={sev}
                onClick={() => setSeverityFilter(sev)}
                className={`px-3 py-1.5 rounded-lg font-semibold transition-colors ${
                  severityFilter === sev ? "bg-brand-600 text-white shadow-sm" : "text-slate-600 hover:bg-slate-100"
                }`}
              >
                {sev}
              </button>
            ))}
          </div>

          <div className="flex items-center space-x-2 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-lg">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Event Taxonomy Verified ({filteredEvents.length})</span>
          </div>
        </div>
      </div>

      <EventStream events={filteredEvents} />
    </div>
  );
}
