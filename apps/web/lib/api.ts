/**
 * Fleetos API Client
 * Connects Web Dashboard UI to FastAPI REST Backend Services
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export interface Lorry {
  id: string;
  registration_number: string;
  max_weight_kg: number;
  max_volume_m3: number;
  current_latitude: number;
  current_longitude: number;
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

export async function fetchHealth() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/health`, { cache: 'no-store' });
    if (!res.ok) throw new Error("Health check failed");
    return await res.json();
  } catch (err) {
    return { status: "offline", error: String(err) };
  }
}

export async function fetchDBHealth() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/health/db`, { cache: 'no-store' });
    if (!res.ok) throw new Error("DB Health check failed");
    return await res.json();
  } catch (err) {
    return { status: "offline", database: "disconnected" };
  }
}

export async function fetchLorries(): Promise<Lorry[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/lorries`, { cache: 'no-store' });
    if (!res.ok) throw new Error("Failed to fetch lorries");
    return await res.json();
  } catch (err) {
    console.error("Error fetching lorries:", err);
    return [];
  }
}

export async function fetchShipments(): Promise<Shipment[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/shipments`, { cache: 'no-store' });
    if (!res.ok) throw new Error("Failed to fetch shipments");
    return await res.json();
  } catch (err) {
    console.error("Error fetching shipments:", err);
    return [];
  }
}

export async function fetchEvents(): Promise<OperationalEvent[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/events`, { cache: 'no-store' });
    if (!res.ok) throw new Error("Failed to fetch events");
    return await res.json();
  } catch (err) {
    console.error("Error fetching events:", err);
    return [];
  }
}
