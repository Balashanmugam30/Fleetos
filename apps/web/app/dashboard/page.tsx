"use client";

import React, { useState, useEffect } from "react";
import {
  fetchLorries,
  fetchShipments,
  fetchDBHealth,
  fetchLatestTracking,
  fetchEvents,
  fetchTrackingSimulatorStatus,
  startTrackingSimulator,
  stopTrackingSimulator,
  VehicleTrackingState,
  Lorry,
  Shipment,
  OperationalEvent,
  SimulatorStatus
} from "@/lib/api";
import { FleetMap } from "@/components/fleet-map";
import {
  Truck,
  Package,
  Activity,
  ShieldCheck,
  Play,
  Square,
  RefreshCw,
  AlertTriangle,
  CheckCircle2,
  Clock
} from "lucide-react";

export default function DashboardPage() {
  const [lorries, setLorries] = useState<Lorry[]>([]);
  const [shipments, setShipments] = useState<Shipment[]>([]);
  const [dbStatus, setDbStatus] = useState<string>("ok");
  const [trackingStates, setTrackingStates] = useState<VehicleTrackingState[]>([]);
  const [events, setEvents] = useState<OperationalEvent[]>([]);
  const [simStatus, setSimStatus] = useState<SimulatorStatus | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const loadData = async () => {
    try {
      const [lRes, sRes, dbRes, trackRes, evtRes, simRes] = await Promise.all([
        fetchLorries(),
        fetchShipments(),
        fetchDBHealth(),
        fetchLatestTracking(),
        fetchEvents(),
        fetchTrackingSimulatorStatus()
      ]);

      setLorries(lRes);
      setShipments(sRes);
      setDbStatus(dbRes.status);
      setTrackingStates(trackRes);
      setEvents(evtRes);
      setSimStatus(simRes);
    } catch (err) {
      console.error("Error loading dashboard data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000); // 5-second real-time polling
    return () => clearInterval(interval);
  }, []);

  const handleStartSim = async () => {
    await startTrackingSimulator();
    await loadData();
  };

  const handleStopSim = async () => {
    await stopTrackingSimulator();
    await loadData();
  };

  const movingCount = trackingStates.filter((s) => s.status === "MOVING").length;
  const stoppedCount = trackingStates.filter((s) => s.status === "STOPPED" || s.status === "IDLE").length;
  const staleCount = trackingStates.filter((s) => s.freshness === "STALE" || s.freshness === "OFFLINE").length;

  return (
    <div className="space-y-6">
      {/* Header & Simulator Control Tower Banner */}
      <div className="flex flex-wrap justify-between items-center gap-4 bg-white border border-slate-200 p-6 rounded-2xl shadow-sm">
        <div>
          <div className="inline-flex items-center space-x-2 px-3 py-1 bg-brand-50 border border-brand-200 text-brand-700 rounded-full text-xs font-semibold mb-2">
            <span>SEE → HEAR → THINK → OPTIMIZE → ACT → UPDATE</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900">Fleet Control Tower & Tracking Engine</h1>
          <p className="text-sm text-slate-500">Real-time vehicle position telemetry, speed vector tracking, and status matrix.</p>
        </div>

        {/* Development GPS Simulator Control Panel */}
        <div className="flex items-center space-x-3 bg-slate-50 p-3 rounded-xl border border-slate-200">
          <div className="text-right text-xs">
            <span className="block font-bold text-slate-900">GPS Simulator</span>
            <span className={`text-[11px] font-semibold ${simStatus?.running ? "text-emerald-600" : "text-slate-400"}`}>
              {simStatus?.running ? "RUNNING (DEMO TELEMETRY)" : "STOPPED"}
            </span>
          </div>

          {simStatus?.running ? (
            <button
              onClick={handleStopSim}
              className="inline-flex items-center px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors"
            >
              <Square className="w-3.5 h-3.5 mr-1 fill-white" />
              Stop Simulator
            </button>
          ) : (
            <button
              onClick={handleStartSim}
              className="inline-flex items-center px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors"
            >
              <Play className="w-3.5 h-3.5 mr-1 fill-white" />
              Start Simulator
            </button>
          )}
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="logistics-card p-5">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold">Active Fleet</span>
            <Truck className="w-4 h-4 text-brand-600" />
          </div>
          <span className="text-2xl font-bold text-slate-900">{lorries.length || 5} Vehicles</span>
          <span className="block text-xs text-slate-400 mt-1">L01 – L05 Reporting</span>
        </div>

        <div className="logistics-card p-5">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold">Moving Vehicles</span>
            <Activity className="w-4 h-4 text-blue-600" />
          </div>
          <span className="text-2xl font-bold text-blue-600">{movingCount} Moving</span>
          <span className="block text-xs text-slate-400 mt-1">Speed &gt; 2.0 km/h</span>
        </div>

        <div className="logistics-card p-5">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold">Stopped / Idle</span>
            <Clock className="w-4 h-4 text-emerald-600" />
          </div>
          <span className="text-2xl font-bold text-emerald-600">{stoppedCount} Vehicles</span>
          <span className="block text-xs text-slate-400 mt-1">Speed = 0 km/h</span>
        </div>

        <div className="logistics-card p-5">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold">Freshness Alert</span>
            <AlertTriangle className="w-4 h-4 text-amber-500" />
          </div>
          <span className="text-2xl font-bold text-amber-600">{staleCount} Stale/Offline</span>
          <span className="block text-xs text-slate-400 mt-1">Telemetry age &gt; 120s</span>
        </div>
      </div>

      {/* Live Vector Telemetry Map Component */}
      <FleetMap trackingStates={trackingStates} />

      {/* Operational Event Stream Grid */}
      <div className="logistics-card p-6 space-y-4">
        <div className="flex justify-between items-center border-b border-slate-100 pb-3">
          <div>
            <h3 className="text-base font-bold text-slate-900">Operational Event Stream</h3>
            <p className="text-xs text-slate-500">Live tracking lifecycle transitions & delay event log.</p>
          </div>
          <span className="text-xs font-mono text-slate-400">Total Events: {events.length}</span>
        </div>

        <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
          {events.length > 0 ? (
            events.slice(0, 8).map((evt) => (
              <div key={evt.id} className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs flex justify-between items-center">
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                    evt.event_type.includes("MOVING") ? "bg-blue-100 text-blue-800" :
                    evt.event_type.includes("STOPPED") ? "bg-slate-200 text-slate-800" :
                    "bg-amber-100 text-amber-800"
                  }`}>
                    {evt.event_type}
                  </span>
                  <span className="font-semibold text-slate-900">{evt.lorry_id ? `Lorry ${evt.lorry_id}` : "System"}</span>
                </div>
                <span className="text-slate-400 font-mono text-[11px]">{new Date(evt.created_at).toLocaleTimeString()}</span>
              </div>
            ))
          ) : (
            <div className="p-4 text-center text-slate-400 text-xs">
              No tracking lifecycle events logged yet. Start simulator to generate movement events.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
