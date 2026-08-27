/**
 * Fleetos Canonical Data Contracts
 * Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
 */

export type LorryStatus = 'IDLE' | 'EN_ROUTE' | 'LOADING' | 'UNAVAILABLE' | 'DELAYED' | 'MAINTENANCE';
export type DriverAvailability = 'AVAILABLE' | 'ON_DUTY' | 'ON_BREAK' | 'UNAVAILABLE';
export type ShipmentStatus = 'UNASSIGNED' | 'ASSIGNED' | 'IN_TRANSIT' | 'DELIVERED' | 'REJECTED';
export type ShipmentPriority = 'LOW' | 'NORMAL' | 'HIGH' | 'URGENT';
export type DeadlineRiskLevel = 'NONE' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type EventSeverity = 'INFO' | 'WARNING' | 'CRITICAL';
export type EventSource = 'ATLAS_VOICE' | 'DISPATCHER_WEB' | 'AR_VIEW' | 'SYSTEM_MONITOR';

export interface LocationCoordinates {
  address: string;
  latitude: number;
  longitude: number;
}

export interface Lorry {
  id: string; // e.g. "L01", "L03"
  registrationNumber: string;
  maxWeightKg: number;
  maxVolumeM3: number;
  currentLatitude: number;
  currentLongitude: number;
  fuelEfficiencyKmLiter: number;
  driverId: string | null;
  status: LorryStatus;
  currentRouteId: string | null;
}

export interface Driver {
  id: string; // e.g. "D01"
  name: string;
  phoneNumber: string; // Masked e.g. "+91-98765-XXXXX"
  availabilityStatus: DriverAvailability;
  currentLorryId: string | null;
}

export interface Shipment {
  id: string; // e.g. "S01", "S12"
  weightKg: number;
  volumeM3: number;
  pickupLocation: LocationCoordinates;
  destination: LocationCoordinates;
  deliveryDeadline: string; // ISO 8601 Timestamp
  priority: ShipmentPriority;
  status: ShipmentStatus;
}

export interface Assignment {
  id: string;
  shipmentId: string;
  lorryId: string;
  sequence: number;
  assignmentReason: string;
  createdAt: string;
}

export interface RouteStop {
  sequence: number;
  type: 'PICKUP' | 'DELIVERY';
  shipmentId: string;
  location: LocationCoordinates;
  estimatedArrival: string;
  deadline: string;
  completed: boolean;
}

export interface Route {
  id: string;
  lorryId: string;
  stops: RouteStop[];
  distanceMeters: number;
  estimatedDurationSeconds: number;
  fuelEstimateLiters: number;
  costEstimate: number;
  deadlineRisk: DeadlineRiskLevel;
}

export interface OperationalEvent {
  id: string;
  type: string; // e.g. "DRIVER_DELAY_REPORTED", "VEHICLE_BREAKDOWN_REPORTED"
  source: EventSource;
  severity: EventSeverity;
  lorryId: string | null;
  shipmentId: string | null;
  timestamp: string;
  payload: Record<string, any>;
  resolutionStatus: 'PENDING' | 'REOPTIMIZED' | 'RESOLVED' | 'IGNORED';
}

export interface PhoneCallRecord {
  id: string;
  driverId: string | null;
  lorryId: string | null;
  callType: 'OUTBOUND_DISPATCH' | 'INBOUND_REPORT' | 'REPLACEMENT_OFFER';
  direction: 'OUTBOUND' | 'INBOUND';
  status: 'QUEUED' | 'RINGING' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED' | 'NO_ANSWER';
  startedAt: string | null;
  endedAt: string | null;
  transcriptReference: string | null;
  eventId: string | null;
}

export interface OptimizationRun {
  id: string;
  timestamp: string;
  triggerReason: string;
  status: 'OPTIMAL' | 'FEASIBLE' | 'INFEASIBLE';
  inputSnapshotReference: string;
  totalCost: number;
  totalFuelLiters: number;
  deadlineViolationsCount: number;
  unassignedShipments: Array<{ shipmentId: string; reason: string }>;
}

export interface ARDetection {
  id: string;
  entityType: 'LORRY' | 'SHIPMENT' | 'PALLET';
  entityId: string;
  detectionMethod: 'MARKER_IMAGE' | 'QR_CODE' | 'COMPUTER_VISION';
  timestamp: string;
  confidence: number;
}

export interface TrackingPosition {
  lorryId: string;
  latitude: number;
  longitude: number;
  timestamp: string;
  speedKmH: number;
  headingDegrees: number;
  status: LorryStatus;
}
