# Fleetos 60-Second Hackathon Demo Runbook

Product: **Fleetos** (Agentic Multimodal Fleet Intelligence Platform)  
Voice Agent: **ATLAS** (Sarvam Indic Multilingual AI + Twilio Telephony)

---

## 60-Second Live Hackathon Demo Timeline

| Time Range | Action | Visual / Operational Outcome |
| :--- | :--- | :--- |
| **00:00 – 00:10** | Open Fleetos Control Tower Dashboard (`http://localhost:3000/ai`). | Show **ATLAS — Sarvam Multilingual Voice Operations Center** with Indic language badge. |
| **00:10 – 00:20** | Select Driver **D03 (Vikram Singh — Lorry L03)** and purpose **DELAY_REPORT**. Select language **AUTO** or **Tamil / Hindi**. | Demonstrate live driver resolution from database (`L03`, `+919876543210`). |
| **00:20 – 00:25** | Click **DISPATCH ATLAS CALL**. | Trigger Sarvam Voice Agent outbound dispatch via Twilio PSTN. |
| **00:25 – 00:35** | Driver mobile phone rings live in auditor/judge's presence. | Real PSTN phone ringing. |
| **00:35 – 00:45** | Driver answers and speaks naturally in Tamil/Hindi/English: *"Anna, loading la 45 minutes delay aagudhu."* | Sarvam Indic speech recognition & code-mixing understanding. |
| **00:45 – 00:52** | ATLAS confirms delay and invokes Sarvam API Tool `report_delay`. | Sarvam posts to `POST /api/v1/voice/sarvam/tools/report-delay`. |
| **00:52 – 01:00** | ATLAS speaks confirmation. Control Tower `/events` updates live showing **DRIVER_DELAY_REPORTED (L03, 45 min)**. | Full closed loop: **SEE → HEAR → THINK → OPTIMIZE → ACT → UPDATE**. |
