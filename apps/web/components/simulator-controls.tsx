"use client";

import React from "react";
import { Play, Square, RefreshCw, Radio } from "lucide-react";
import { SimulatorStatus } from "@/lib/api";

interface SimulatorControlsProps {
  simulatorStatus: SimulatorStatus | null;
  onStart: () => void;
  onStop: () => void;
  isLoading?: boolean;
}

export function SimulatorControls({ simulatorStatus, onStart, onStop, isLoading }: SimulatorControlsProps) {
  const isRunning = simulatorStatus?.running ?? false;

  return (
    <div className="flex flex-wrap items-center justify-between gap-3 bg-white border border-slate-200 p-4 rounded-xl shadow-sm">
      <div className="flex items-center space-x-3">
        <div className={`p-2.5 rounded-lg border ${
          isRunning ? "bg-emerald-50 border-emerald-200 text-emerald-600" : "bg-slate-50 border-slate-200 text-slate-400"
        }`}>
          <Radio className={`w-5 h-5 ${isRunning ? "animate-pulse text-emerald-600" : ""}`} />
        </div>

        <div>
          <div className="flex items-center space-x-2">
            <h4 className="text-sm font-bold text-slate-900">GPS Telemetry Simulator</h4>
            <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
              isRunning ? "bg-emerald-100 text-emerald-800 border border-emerald-200" : "bg-slate-100 text-slate-600 border border-slate-200"
            }`}>
              {isRunning ? "DEMO TELEMETRY ACTIVE" : "SIMULATOR STOPPED"}
            </span>
          </div>
          <p className="text-xs text-slate-500">
            {isRunning
              ? `Simulating live vector telemetry for 5 vehicles at ${simulatorStatus?.update_interval_seconds || 5}s intervals.`
              : "Start simulator to generate real-time vehicle movement across South India corridors."}
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-2">
        {isRunning ? (
          <button
            onClick={onStop}
            disabled={isLoading}
            className="inline-flex items-center px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors disabled:opacity-50"
          >
            <Square className="w-3.5 h-3.5 mr-1.5 fill-white" />
            Stop Simulator
          </button>
        ) : (
          <button
            onClick={onStart}
            disabled={isLoading}
            className="inline-flex items-center px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors disabled:opacity-50"
          >
            <Play className="w-3.5 h-3.5 mr-1.5 fill-white" />
            Start Simulator
          </button>
        )}
      </div>
    </div>
  );
}
