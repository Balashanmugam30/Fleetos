# Fleetos Sarvam Voice Agents & Twilio Telephony Setup Guide

Product: **Fleetos** (Agentic Multimodal Fleet Intelligence Platform)  
Voice Agent: **ATLAS**

---

## Sarvam Voice Agents + Twilio Telephony Architecture

To perform outbound PSTN voice calls to driver mobile phones, Fleetos integrates **Sarvam Voice Agents** with **Twilio Telephony**.

### 1. Sarvam Dashboard Configuration (One-Time Setup)

1. **Twilio Telephony Connection**:
   - Navigate to **Sarvam Voice Agents Dashboard** $\rightarrow$ **Deploy** $\rightarrow$ **Phone Numbers** $\rightarrow$ **Add Connection**.
   - Select **Twilio**.
   - Enter your Twilio credentials:
     - `Account SID`: `TWILIO_ACCOUNT_SID`
     - `Auth Token`: `TWILIO_AUTH_TOKEN`
   - Connect your Twilio Phone Number (`TWILIO_PHONE_NUMBER`).

2. **ATLAS Voice Agent Assignment**:
   - Assign the **ATLAS** logistics agent to the connected Twilio Phone Number.
   - Configure System Prompt, Language (`Tamil`, `Hindi`, `English`, `AUTO`), and API Tool Endpoint:
     - Tool Name: `report_delay`
     - Tool Endpoint URL: `https://<your-public-tunnel-url>/api/v1/voice/sarvam/tools/report-delay`
     - Authentication Header: `X-Sarvam-Tool-Secret: <SARVAM_TOOL_SECRET>`

3. **Outbound Campaign / Agent Dispatch**:
   - Copy your `Agent ID` (`SARVAM_AGENT_ID`), `Deployment ID` (`SARVAM_DEPLOYMENT_ID`), and `Campaign ID` (`SARVAM_CAMPAIGN_ID`) into `.env`.

---

## Required Environment Variables in `.env`

```env
# Sarvam Voice Agents API
SARVAM_API_KEY=your_sarvam_api_key_here
SARVAM_AGENT_ID=your_sarvam_agent_id
SARVAM_DEPLOYMENT_ID=your_sarvam_deployment_id
SARVAM_CAMPAIGN_ID=your_sarvam_campaign_id
SARVAM_OUTBOUND_ENDPOINT=https://api.sarvam.ai/agents/your_agent_id/calls
SARVAM_DEFAULT_LANGUAGE=hi-IN
SARVAM_WEBHOOK_BASE_URL=https://inquire-shortly-independent-sheer.trycloudflare.com
SARVAM_TOOL_SECRET=fleetos_sarvam_tool_sec_2026

# Twilio Telephony Ingress
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+17372212163

# Active Voice Provider Flag
VOICE_PROVIDER=sarvam
```
