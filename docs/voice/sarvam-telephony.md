# Fleetos Sarvam Voice Agents & Twilio Telephony Setup Guide

Product: **Fleetos** (Agentic Multimodal Fleet Intelligence Platform)  
Voice Agent: **ATLAS**  
Telephony Readiness: **REAL PSTN BLOCKED — requires a provisioned/importable telephony number.**

---

## Twilio Trial Account Sandbox vs. Provisioned Phone Numbers

### 1. Twilio Trial Account Inventory Limitation
When testing with a Twilio trial account:
- Twilio credentials: **VALID**
- Twilio Try Out Voice: **WORKING**
- Twilio provisioned `IncomingPhoneNumbers`: **0**
- Sarvam Twilio connection: **CONNECTED**
- Sarvam importable phone number: **NOT AVAILABLE**
- Sarvam outbound campaign: **NOT VERIFIED**
- Fleetos Sarvam tool endpoint: **WORKING**
- `report_delay`: **WORKING**
- `pytest`: **34 PASSED**
- Next.js build: **PASSED**
- `real_pstn_ready`: **FALSE**
- Actual real Sarvam → Twilio → mobile call: **NOT VERIFIED**

---

## Technical Prerequisites for Live Sarvam Outbound PSTN Calling

To connect a live phone number to Sarvam Voice Agents:
1. **Twilio Account Upgrade**: Upgrade the Twilio account from trial status.
2. **Provisioned Phone Number**: Purchase a dedicated Twilio phone number ($1/month).
3. **Sarvam BYO Twilio Import**:
   - Navigate to **Sarvam Voice Agents Dashboard** $\rightarrow$ **Deploy** $\rightarrow$ **Phone Numbers** $\rightarrow$ **Add Connection** $\rightarrow$ **Twilio**.
   - Enter `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`.
   - Select the provisioned Twilio phone number.
4. **Environment Variables**:
   ```env
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_PHONE_NUMBER=+17372212163
   TWILIO_PROVISIONED_NUMBER_COUNT=1
   SARVAM_API_KEY=your_sarvam_api_key
   SARVAM_AGENT_ID=your_sarvam_agent_id
   SARVAM_DEPLOYMENT_ID=your_sarvam_deployment_id
   SARVAM_CAMPAIGN_ID=your_sarvam_campaign_id
   VOICE_PROVIDER=sarvam
   ```

---

## Fleetos Diagnostic Health Endpoint Behavior

When running in trial mode without a provisioned phone number, `GET /api/v1/voice/health` returns:

```json
{
  "provider": "demo",
  "mode": "DEMO",
  "configured": false,
  "twilio_credentials_valid": true,
  "twilio_trial_voice_available": true,
  "twilio_provisioned_number_count": 0,
  "sarvam_number_imported": false,
  "outbound_ready": false,
  "real_pstn_ready": false
}
```

Fleetos safely runs in **Demo Telephony Mode**, allowing full operational simulation, tool execution, and Control Tower updates without making unverified claims of real PSTN readiness.
