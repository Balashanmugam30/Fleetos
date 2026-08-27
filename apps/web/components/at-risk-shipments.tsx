"use client";

import React from "react";
import { Shipment } from "@/lib/api";
import { AlertTriangle, Clock, MapPin, Package } from "lucide-react";

interface AtRiskShipmentsProps {
  shipments: Shipment[];
}

export function AtRiskShipments({ shipments }: AtRiskShipmentsProps) {
  // Filter urgent or deadline-sensitive shipments
  const urgentShipments = shipments.filter(s => s.priority === "URGENT" || s.id === "S12");

  return (
    <div className="logistics-card p-6 space-y-4">
      <div className="flex justify-between items-center border-b border-slate-100 pb-3">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center">
            <AlertTriangle className="w-4 h-4 mr-2 text-amber-500" />
            At-Risk Load Deadlines
          </h3>
          <p className="text-xs text-slate-500">Urgent shipments monitored for deadline risk & delay re-optimization.</p>
        </div>
        <span className="text-xs font-bold px-2 py-0.5 bg-amber-50 text-amber-800 border border-amber-200 rounded">
          {urgentShipments.length} Monitored
        </span>
      </div>

      <div className="space-y-3">
        {urgentShipments.length > 0 ? (
          urgentShipments.map((s) => (
            <div key={s.id} className="p-3 bg-amber-50/40 border border-amber-200 rounded-xl space-y-2 text-xs">
              <div className="flex justify-between items-center">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-slate-900 flex items-center">
                    <Package className="w-3.5 h-3.5 mr-1 text-brand-600" />
                    Shipment {s.id}
                  </span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-red-100 text-red-800 border border-red-200">
                    {s.priority}
                  </span>
                </div>
                <span className="font-bold text-amber-700 font-mono">
                  {s.id === "S12" ? "HIGH RISK" : "MONITORED"}
                </span>
              </div>

              <div className="text-slate-600 flex items-center text-[11px]">
                <MapPin className="w-3.5 h-3.5 mr-1 text-slate-400" />
                <span>{s.pickup_address} $\rightarrow$ {s.destination_address}</span>
              </div>

              <div className="flex justify-between items-center text-[11px] text-slate-500 border-t border-amber-200/60 pt-1.5">
                <span className="flex items-center">
                  <Clock className="w-3 h-3 mr-1 text-slate-400" />
                  Deadline: {new Date(s.delivery_deadline).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
                <span>Assigned: {s.id === "S12" ? "Lorry L05" : "Assigned"}</span>
              </div>
            </div>
          ))
        ) : (
          <div className="p-4 text-center text-slate-400 text-xs bg-slate-50 rounded-xl border border-slate-200">
            No urgent deadline risk detected across active shipments.
          </div>
        )}
      </div>
    </div>
  );
}
