# Fleetos Sarvam Voice Agents & Twilio Telephony Setup Guide

Product: **Fleetos** (Agentic Multimodal Fleet Intelligence Platform)  
Voice Agent: **ATLAS**

---

## Twilio Trial Account Sandbox vs. Provisioned Phone Numbers

### 1. Twilio Trial Account Inventory Limitation
When testing with a Twilio trial account:
- Twilio provides a **"Try Out Voice" sandbox test number** (e.g., `+17372212163`) which can dial verified recipient phone numbers (`+91...`).
- However, querying Twilio's REST API endpoint `GET /2010-04-01/Accounts/{SID}/IncomingPhoneNumbers.json` returns an **empty array** (`{"incoming_phone_numbers": []}`) because trial sandbox numbers are shared sandbox pools, not provisioned `IncomingPhoneNumber` resources belonging exclusively to the account.
- When Sarvam Voice Agents executes **BYO Twilio $\rightarrow$ Import Numbers**, Sarvam queries `IncomingPhoneNumbers.json`. Because 0 provisioned numbers exist, Sarvam displays **"No results found"**.

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

Fleetos safely runs in **Demo Telephony Mode**, allowing full operational simulation, tool execution, and Control Tower updates without making false claims of real PSTN readiness.
