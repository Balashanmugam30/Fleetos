/**
 * Fleetos API Client & Resilience Layer
 * Module Boundary: apps/web/lib/api.ts
 * Connects Next.js Web Dashboard UI to FastAPI REST Backend Services
 */

const API_BASE_URL = process.env.API_BASE_URL || process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export interface Lorry {
  id: string;
  registration_number: string;
  max_weight_kg: number;
  max_volume_m3: number;
  current_latitude: number;
  current_longitude: number;
  current_speed_km_h?: number;
  current_heading_degrees?: number;
  fuel_efficiency_km_l: number;
  driver_id: string | null;
  status: string;
  current_route_id: string | null;
}

export interface Driver {
  id: string;
  name: string;
  phone_number: string;
  availability_status: string;
  current_lorry_id: string | null;
}

export interface Shipment {
  id: string;
  weight_kg: number;
  volume_m3: number;
  pickup_address: string;
  destination_address: string;
  delivery_deadline: string;
  priority: string;
  status: string;
}

export interface OperationalEvent {
  id: string;
  event_type: string;
  source: string;
  severity: string;
  lorry_id: string | null;
  shipment_id: string | null;
  payload_json: Record<string, any>;
  resolution_status: string;
  created_at: string;
}

export interface VehicleTrackingState {
  vehicle_id: string;
  driver_id: string | null;
  latitude: number;
  longitude: number;
  speed_kmh: number;
  heading_degrees: number;
  status: "MOVING" | "STOPPED" | "IDLE" | "OFFLINE" | "UNKNOWN";
  freshness: "LIVE" | "RECENT" | "STALE" | "OFFLINE";
  last_update_at: string;
  telemetry_age_seconds: number;
  source: string;
  active_route_id: string | null;
}

export interface TrackingPosition {
  vehicle_id: string;
  latitude: number;
  longitude: number;
  speed_kmh: number;
  heading_degrees: number;
  recorded_at: string;
  received_at: string;
  source: string;
}

export interface SimulatorStatus {
  running: boolean;
  update_interval_seconds: number;
  simulated_vehicles_count: number;
  last_update_time: string | null;
}

export interface ApiFetchResult<T> {
  data: T | null;
  error: string | null;
  status: "success" | "offline" | "error";
}

async function safeFleetosFetch<T>(path: string, options: RequestInit = {}): Promise<ApiFetchResult<T>> {
  const url = `${API_BASE_URL}${path}`;
  try {
    const res = await fetch(url, {
      cache: "no-store",
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
    });

    if (!res.ok) {
      return {
        data: null,
        error: `HTTP ${res.status}: ${res.statusText}`,
        status: "error",
      };
    }

    const data = await res.json();
    return {
      data,
      error: null,
      status: "success",
    };
  } catch (err: any) {
    console.warn(`[Fleetos API Client] Connection to ${url} failed: ${err.message}`);
    return {
      data: null,
      error: `Unable to connect to Fleetos API at ${API_BASE_URL}.`,
      status: "offline",
    };
  }
}

export async function fetchHealth() {
  const result = await safeFleetosFetch<{ status: string; service: string; version: string }>("/api/v1/health");
  return result.data || { status: "offline", service: "fleetos-api", version: "0.2.0" };
}

export async function fetchDBHealth() {
  const result = await safeFleetosFetch<{ status: string; database: string }>("/api/v1/health/db");
  return result.data || { status: "offline", database: "disconnected" };
}

export async function fetchLorries(): Promise<Lorry[]> {
  const result = await safeFleetosFetch<Lorry[]>("/api/v1/lorries");
  return result.data || [];
}

export async function fetchShipments(): Promise<Shipment[]> {
  const result = await safeFleetosFetch<Shipment[]>("/api/v1/shipments");
  return result.data || [];
}

export async function fetchEvents(): Promise<OperationalEvent[]> {
  const result = await safeFleetosFetch<OperationalEvent[]>("/api/v1/events");
  return result.data || [];
}

export async function fetchLatestTracking(): Promise<VehicleTrackingState[]> {
  const result = await safeFleetosFetch<VehicleTrackingState[]>("/api/v1/tracking/latest");
  return result.data || [];
}

export async function fetchVehicleTracking(vehicleId: string): Promise<VehicleTrackingState | null> {
  const result = await safeFleetosFetch<VehicleTrackingState>(`/api/v1/tracking/vehicles/${vehicleId}`);
  return result.data;
}

export async function fetchTrackingHistory(vehicleId: string, limit = 50): Promise<TrackingPosition[]> {
  const result = await safeFleetosFetch<TrackingPosition[]>(`/api/v1/tracking/vehicles/${vehicleId}/history?limit=${limit}`);
  return result.data || [];
}

export async function startTrackingSimulator(): Promise<SimulatorStatus | null> {
  const result = await safeFleetosFetch<SimulatorStatus>("/api/v1/tracking/simulator/start", { method: "POST" });
  return result.data;
}

export async function stopTrackingSimulator(): Promise<SimulatorStatus | null> {
  const result = await safeFleetosFetch<SimulatorStatus>("/api/v1/tracking/simulator/stop", { method: "POST" });
  return result.data;
}

export async function fetchTrackingSimulatorStatus(): Promise<SimulatorStatus | null> {
  const result = await safeFleetosFetch<SimulatorStatus>("/api/v1/tracking/simulator/status");
  return result.data;
}

export async function triggerOptimization(triggerReason = "MANUAL_REOPTIMIZE") {
  const url = `${API_BASE_URL}/api/v1/optimization/run?trigger_reason=${encodeURIComponent(triggerReason)}`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
  });
  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Optimization failed: ${res.status} - ${errorText}`);
  }
  return await res.json();
}
