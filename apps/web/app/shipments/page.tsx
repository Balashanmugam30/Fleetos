"use client";

import React, { useState, useEffect } from "react";
import { fetchShipments, fetchLatestTracking, Shipment, VehicleTrackingState } from "@/lib/api";
import { Package, Clock, ShieldCheck, AlertCircle, Filter, MapPin, Truck } from "lucide-react";

export default function ShipmentsPage() {
  const [shipments, setShipments] = useState<Shipment[]>([]);
  const [trackingStates, setTrackingStates] = useState<VehicleTrackingState[]>([]);
  const [priorityFilter, setPriorityFilter] = useState<string>("ALL");
  const [loading, setLoading] = useState<boolean>(true);

  const loadShipmentData = async () => {
    try {
      const [sRes, trackRes] = await Promise.all([
        fetchShipments(),
        fetchLatestTracking()
      ]);
      setShipments(sRes);
      setTrackingStates(trackRes);
    } catch (err) {
      console.error("Error loading shipment data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadShipmentData();
    const interval = setInterval(loadShipmentData, 5000);
    return () => clearInterval(interval);
  }, []);

  const filteredShipments = shipments.filter((s) => {
    if (priorityFilter === "ALL") return true;
    return s.priority === priorityFilter;
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Shipment Management Tracker</h1>
          <p className="text-sm text-slate-500">Persisted load weight, volume, delivery deadline & priority tracking matrix.</p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1 bg-white border border-slate-200 p-1 rounded-xl text-xs">
            {["ALL", "URGENT", "HIGH", "NORMAL"].map((p) => (
              <button
                key={p}
                onClick={() => setPriorityFilter(p)}
                className={`px-3 py-1.5 rounded-lg font-semibold transition-colors ${
                  priorityFilter === p ? "bg-brand-600 text-white shadow-sm" : "text-slate-600 hover:bg-slate-100"
                }`}
              >
                {p}
              </button>
            ))}
          </div>

          <div className="flex items-center space-x-2 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-lg">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Database Persisted ({filteredShipments.length} Loads)</span>
          </div>
        </div>
      </div>

      {shipments.length === 0 && !loading && (
        <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 text-amber-600 flex-shrink-0" />
          <span>No live shipment records loaded. Ensure FastAPI backend is running on port 8000.</span>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredShipments.map((s) => (
          <div key={s.id} className="logistics-card p-5 space-y-3">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center space-x-2.5">
                <div className="w-8 h-8 bg-brand-50 border border-brand-200 text-brand-600 rounded-lg flex items-center justify-center font-bold text-xs">
                  {s.id}
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Shipment {s.id}</h3>
                  <p className="text-xs text-slate-500 flex items-center mt-0.5">
                    <MapPin className="w-3 h-3 mr-1 text-slate-400" />
                    {s.pickup_address} $\rightarrow$ {s.destination_address}
                  </p>
                </div>
              </div>
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                s.priority === 'URGENT' ? 'bg-red-50 text-red-700 border border-red-200' :
                s.priority === 'HIGH' ? 'bg-amber-50 text-amber-700 border border-amber-200' :
                'bg-slate-100 text-slate-700 border border-slate-200'
              }`}>
                {s.priority}
              </span>
            </div>

            <div className="grid grid-cols-3 gap-2 text-xs">
              <div className="p-2 bg-slate-50 border border-slate-200 rounded-lg">
                <span className="text-slate-400 block text-[11px]">Weight</span>
                <span className="font-bold text-slate-900">{s.weight_kg.toLocaleString()} kg</span>
              </div>
              <div className="p-2 bg-slate-50 border border-slate-200 rounded-lg">
                <span className="text-slate-400 block text-[11px]">Volume</span>
                <span className="font-bold text-slate-900">{s.volume_m3} m³</span>
              </div>
              <div className="p-2 bg-slate-50 border border-slate-200 rounded-lg">
                <span className="text-slate-400 block text-[11px]">Status</span>
                <span className="font-bold text-brand-600">{s.status}</span>
              </div>
            </div>

            <div className="flex justify-between items-center text-xs text-slate-500 pt-1">
              <span className="flex items-center">
                <Clock className="w-3.5 h-3.5 mr-1 text-slate-400" />
                Deadline: {new Date(s.delivery_deadline).toLocaleString()}
              </span>
              <span className="font-semibold text-slate-700 flex items-center">
                <Truck className="w-3.5 h-3.5 mr-1 text-brand-600" />
                Assigned: {s.id === "S12" ? "L05" : "L01"}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
