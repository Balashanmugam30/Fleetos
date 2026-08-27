# Fleetos Sarvam Voice Agents Tool Webhook Specification

Product: **Fleetos** (Agentic Multimodal Fleet Intelligence Platform)  
Voice Agent: **ATLAS**

---

## Sarvam API Tool Integration Contract

Sarvam Voice Agents invokes operational tools during driver phone calls via HTTPS POST webhooks.

### Tool Endpoint Specification

- **HTTP Method**: `POST`
- **Path**: `/api/v1/voice/sarvam/tools/report-delay`
- **Full Webhook URL**: `https://<VOICE_WEBHOOK_BASE_URL>/api/v1/voice/sarvam/tools/report-delay`
- **Authentication Header**: `X-Sarvam-Tool-Secret: <FLEETOS_SARVAM_TOOL_SECRET>` or `Authorization: Bearer <FLEETOS_SARVAM_TOOL_SECRET>`

### JSON Request Schema

```json
{
  "driver_id": "D03",
  "lorry_id": "L03",
  "delay_minutes": 45,
  "reason": "LOADING_DELAY",
  "tool_call_id": "tc_sarvam_98765"
}
```

### Supported Reason Enum Values
- `LOADING_DELAY`
- `TRAFFIC`
- `BREAKDOWN`
- `CUSTOMER_DELAY`
- `WEATHER`
- `OTHER`

### JSON Response Schema (HTTP 200 OK)

```json
{
  "success": true,
  "event_id": "evt_9e19ae8c",
  "event_type": "DRIVER_DELAY_REPORTED",
  "lorry_id": "L03",
  "driver_id": "D03",
  "delay_minutes": 45,
  "reason": "LOADING_DELAY",
  "message": "Recorded a 45-minute LOADING_DELAY for Driver D03 / Lorry L03 in Fleetos."
}
```

### Idempotency Guarantee
If Sarvam retries a tool call using the same `tool_call_id`, Fleetos queries the event ledger and returns the existing event payload without creating duplicate database records.
