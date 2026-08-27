"use client";

import React from "react";
import Link from "next/link";
import { Cpu, ShieldCheck, ArrowRight, Fuel, DollarSign } from "lucide-react";

export function OptimizationSummary() {
  return (
    <div className="logistics-card p-6 space-y-4 flex flex-col justify-between">
      <div>
        <div className="flex justify-between items-center border-b border-slate-100 pb-3 mb-3">
          <div>
            <h3 className="text-base font-bold text-slate-900 flex items-center">
              <Cpu className="w-4 h-4 mr-2 text-brand-600" />
              Optimization Engine Summary
            </h3>
            <p className="text-xs text-slate-500">Google OR-Tools Routing Solver / RoutingModel VRP core.</p>
          </div>
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center">
            <ShieldCheck className="w-3.5 h-3.5 mr-1 text-emerald-600" />
            OPTIMAL
          </span>
        </div>

        <div className="grid grid-cols-2 gap-3 text-xs my-3">
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl">
            <span className="text-slate-400 block mb-0.5 flex items-center">
              <DollarSign className="w-3.5 h-3.5 mr-1 text-brand-600" />
              Total Operating Cost
            </span>
            <span className="text-lg font-bold text-slate-900">$842.50</span>
            <span className="text-[10px] text-slate-400 block mt-0.5">Fuel + Driver + Fixed</span>
          </div>

          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl">
            <span className="text-slate-400 block mb-0.5 flex items-center">
              <Fuel className="w-3.5 h-3.5 mr-1 text-amber-600" />
              Fuel Consumption
            </span>
            <span className="text-lg font-bold text-slate-900">312.4 Liters</span>
            <span className="text-[10px] text-slate-400 block mt-0.5">Vehicle-Specific (km/L)</span>
          </div>
        </div>

        <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs space-y-1">
          <div className="flex justify-between font-semibold">
            <span className="text-slate-600">Assigned Shipments:</span>
            <span className="text-emerald-700">12 / 12 (100%)</span>
          </div>
          <div className="flex justify-between text-slate-500 text-[11px]">
            <span>Nearest Lorry Trap:</span>
            <span className="font-semibold text-slate-700">Resolved (L05 @ 5.2 km/L)</span>
          </div>
        </div>
      </div>

      <div className="pt-2 border-t border-slate-100">
        <Link
          href="/optimization"
          className="w-full inline-flex items-center justify-center px-4 py-2 bg-brand-50 hover:bg-brand-100 text-brand-700 font-semibold text-xs rounded-lg border border-brand-200 transition-colors"
        >
          Open Optimization Solver Control Tower
          <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
        </Link>
      </div>
    </div>
  );
}
