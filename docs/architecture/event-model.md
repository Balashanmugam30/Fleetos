# Fleetos Event Model & Taxonomy Specification

Product: **Fleetos**

---

## Event Architecture

Fleetos uses an event-driven re-optimization pattern inspired by real logistics disruptions.

```json
{
  "eventId": "evt_delay_1001",
  "eventType": "DRIVER_DELAY_REPORTED",
  "source": "ATLAS_VOICE",
  "severity": "WARNING",
  "lorryId": "L03",
  "shipmentId": "S12",
  "timestamp": "2026-08-27T17:45:00Z",
  "payload": {
    "delayMinutes": 45,
    "reason": "loading_delay"
  },
  "resolutionStatus": "REOPTIMIZED"
}
```
