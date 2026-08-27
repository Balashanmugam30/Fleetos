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
import { VehicleDetailPanel } from "@/components/vehicle-detail-panel";
import { KpiStrip } from "@/components/kpi-strip";
import { SimulatorControls } from "@/components/simulator-controls";
import { EventStream } from "@/components/event-stream";
import { AtRiskShipments } from "@/components/at-risk-shipments";
import { OptimizationSummary } from "@/components/optimization-summary";
import { AtlasVoiceCard } from "@/components/atlas-voice-card";
import { AlertCircle, ShieldCheck, RefreshCw } from "lucide-react";

export default function DashboardPage() {
  const [lorries, setLorries] = useState<Lorry[]>([]);
  const [shipments, setShipments] = useState<Shipment[]>([]);
  const [dbStatus, setDbStatus] = useState<string>("ok");
  const [trackingStates, setTrackingStates] = useState<VehicleTrackingState[]>([]);
  const [events, setEvents] = useState<OperationalEvent[]>([]);
  const [simStatus, setSimStatus] = useState<SimulatorStatus | null>(null);
  const [selectedVehicleId, setSelectedVehicleId] = useState<string>("L01");
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
      console.error("Error loading Control Tower data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000); // 5-second polling interval
    return () => clearInterval(interval);
  }, []);

  const handleStartSim = async () => {
    setLoading(true);
    await startTrackingSimulator();
    await loadData();
  };

  const handleStopSim = async () => {
    setLoading(true);
    await stopTrackingSimulator();
    await loadData();
  };

  const selectedTrackingState = trackingStates.find((s) => s.vehicle_id === selectedVehicleId) || trackingStates[0] || null;
  const selectedLorry = lorries.find((l) => l.id === selectedVehicleId) || lorries[0] || null;

  return (
    <div className="space-y-6">
      {/* Control Tower Title & Status Header */}
      <div className="flex flex-wrap justify-between items-center gap-4 bg-white border border-slate-200 p-6 rounded-2xl shadow-sm">
        <div>
          <div className="inline-flex items-center space-x-2 px-3 py-1 bg-brand-50 border border-brand-200 text-brand-700 rounded-full text-xs font-semibold mb-2">
            <span>SEE → HEAR → THINK → OPTIMIZE → ACT → UPDATE</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Fleet Control Tower & Operations Center
          </h1>
          <p className="text-sm text-slate-500">
            Real-time multimodal logistics intelligence, vector telemetry map, and operational event stream.
          </p>
        </div>

        <div className="flex items-center space-x-3 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3.5 py-2 rounded-xl">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>{dbStatus === "ok" ? "Backend Database Active" : "API Offline Mode"}</span>
        </div>
      </div>

      {/* Development GPS Simulator Control Panel */}
      <SimulatorControls
        simulatorStatus={simStatus}
        onStart={handleStartSim}
        onStop={handleStopSim}
        isLoading={loading}
      />

      {/* Real-Time KPI Summary Strip */}
      <KpiStrip
        totalVehicles={lorries.length || 5}
        trackingStates={trackingStates}
        totalShipments={shipments.length || 12}
        atRiskShipmentsCount={1}
      />

      {/* Main Grid: Live Vector Map + Vehicle Telemetry Detail Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <FleetMap
            trackingStates={trackingStates}
            selectedVehicleId={selectedVehicleId}
            onSelectVehicle={(id) => setSelectedVehicleId(id)}
          />
        </div>

        <div className="lg:col-span-1">
          <VehicleDetailPanel
            trackingState={selectedTrackingState}
            lorry={selectedLorry}
          />
        </div>
      </div>

      {/* Operational Bottom Grid: Event Stream + ATLAS Voice Agent + Optimization Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <EventStream events={events} />
        </div>

        <div className="lg:col-span-1">
          <AtlasVoiceCard />
        </div>

        <div className="lg:col-span-1">
          <OptimizationSummary />
        </div>
      </div>
    </div>
  );
}
