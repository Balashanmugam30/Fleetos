"use client";

import React, { useState, useEffect } from "react";
import { fetchLorries, fetchLatestTracking, Lorry, VehicleTrackingState } from "@/lib/api";
import { Truck, ShieldCheck, AlertCircle, Navigation, Activity } from "lucide-react";

export default function FleetPage() {
  const [lorries, setLorries] = useState<Lorry[]>([]);
  const [trackingStates, setTrackingStates] = useState<VehicleTrackingState[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const loadFleetData = async () => {
    try {
      const [lRes, trackRes] = await Promise.all([
        fetchLorries(),
        fetchLatestTracking()
      ]);
      setLorries(lRes);
      setTrackingStates(trackRes);
    } catch (err) {
      console.error("Error loading fleet data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFleetData();
    const interval = setInterval(loadFleetData, 5000);
    return () => clearInterval(interval);
  }, []);

  // Merge database lorries with live tracking state
  const trackingMap = new Map(trackingStates.map((s) => [s.vehicle_id, s]));

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Fleet Management & Telemetry Matrix</h1>
          <p className="text-sm text-slate-500">Live vehicle capacity, GPS position vectors, speed, heading & telemetry freshness.</p>
        </div>
        <div className="flex items-center space-x-2 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-lg">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>Real-Time Telemetry Stream Active</span>
        </div>
      </div>

      {lorries.length === 0 && !loading && (
        <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 text-amber-600 flex-shrink-0" />
          <span>No live lorry records loaded. Ensure FastAPI backend is running on port 8000.</span>
        </div>
      )}

      <div className="logistics-card overflow-hidden">
        <table className="min-w-full divide-y divide-slate-200 text-left text-sm">
          <thead className="bg-slate-50 text-slate-500 font-semibold text-xs uppercase tracking-wider">
            <tr>
              <th className="px-6 py-3">Lorry ID</th>
              <th className="px-6 py-3">Registration</th>
              <th className="px-6 py-3">Capacity</th>
              <th className="px-6 py-3">Speed & Heading</th>
              <th className="px-6 py-3">Position (Lat, Lng)</th>
              <th className="px-6 py-3">Tracking Status</th>
              <th className="px-6 py-3">Freshness</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 bg-white text-slate-700">
            {lorries.length > 0 ? (
              lorries.map((l) => {
                const track = trackingMap.get(l.id);
                const status = track?.status || l.status || "IDLE";
                const freshness = track?.freshness || "LIVE";
                const speed = track?.speed_kmh ?? l.current_speed_km_h ?? 0.0;
                const heading = track?.heading_degrees ?? l.current_heading_degrees ?? 0.0;
                const lat = track?.latitude ?? l.current_latitude;
                const lng = track?.longitude ?? l.current_longitude;

                return (
                  <tr key={l.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-6 py-4 font-bold text-slate-900 flex items-center">
                      <Truck className={`w-4 h-4 mr-2 ${status === 'MOVING' ? 'text-brand-600 animate-pulse' : 'text-slate-400'}`} />
                      {l.id}
                    </td>
                    <td className="px-6 py-4 font-mono text-xs">{l.registration_number}</td>
                    <td className="px-6 py-4 text-xs">{l.max_weight_kg.toLocaleString()} kg / {l.max_volume_m3} m³</td>
                    <td className="px-6 py-4 font-semibold text-slate-900 text-xs">
                      {speed} km/h <span className="text-slate-400 font-normal">({heading}°)</span>
                    </td>
                    <td className="px-6 py-4 font-mono text-xs text-slate-500">
                      {lat.toFixed(4)}, {lng.toFixed(4)}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                        status === 'MOVING' ? 'bg-blue-50 text-blue-700 border border-blue-200' :
                        status === 'STOPPED' ? 'bg-slate-100 text-slate-700 border border-slate-200' :
                        'bg-amber-50 text-amber-700 border border-amber-200'
                      }`}>
                        {status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex px-2 py-0.5 rounded text-xs font-semibold ${
                        freshness === 'LIVE' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' :
                        freshness === 'RECENT' ? 'bg-amber-50 text-amber-700 border border-amber-200' :
                        'bg-red-50 text-red-700 border border-red-200'
                      }`}>
                        {freshness}
                      </span>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={7} className="px-6 py-8 text-center text-slate-400 text-xs">
                  No lorry telemetry retrieved from backend API. Start simulator or seed database.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
