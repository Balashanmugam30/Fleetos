# Phase 0 Security Baseline & Governance Protocol

Product Name: **Fleetos**

---

## 1. Secrets Management & Source Control Rules

1. **NO Hardcoded Secrets**: Secrets (API keys, database password strings, private tokens) MUST NEVER be committed to Git or printed in terminal logs, artifacts, screenshots, or generated documentation.
2. **Environment Variable Template**: All required configuration key names are documented in `.env.example`. Local `.env` files are added to `.gitignore`.
3. **Secret Masking**: Phone numbers and private tokens rendered in UI screens or log files must be strictly masked (e.g. `+91-98765-*****`, `vapi_key_****`).

---

## 2. API Endpoint Authentication & Webhook Validation

1. **Vapi Webhook Authorization**: Webhook callbacks from Vapi (`/api/v1/voice/vapi-webhook`) must be validated against `VAPI_SERVER_SECRET` or secret authorization header verification.
2. **Server-Side Mutation Guardrails**: Dangerous state mutations (re-assignment, status override, route cancellation) requested via ATLAS voice tool calls or Web Dashboard MUST pass server-side parameter validation before database commit.
3. **CORS Policy**: FastAPI backend enforces strict allowed origin lists (`http://localhost:3000`, `https://*.vercel.app`).
4. **Input Sanitization**: Pydantic models validate all incoming JSON body parameters, enforcing integer bounds for weight/volume and regex matching for IDs and E.164 phone numbers.

---

## 3. Data Privacy & Compliance Baseline

- **Synthetic Hackathon Demo Data**: All lorry numbers, driver names, phone numbers, and shipment locations used in baseline demo datasets are purely synthetic.
- **Data Minimization**: Voice call transcripts and tool payloads store operational logistics telemetry only. Personal identifying information (PII) is excluded.
