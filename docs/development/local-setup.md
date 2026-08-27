# Fleetos Local Development & Telephony Tunnel Setup Guide

Product: **Fleetos** (Agentic Multimodal Fleet Intelligence Platform)

---

## Service Architecture & Endpoints

| Service | Port | Endpoint URL | Description |
| :--- | :--- | :--- | :--- |
| **Next.js Web Dashboard** | `3000` | `http://localhost:3000` | React 19 / Next.js 15 Control Tower UI |
| **FastAPI REST API Server** | `8000` | `http://127.0.0.1:8000` | REST API, Database Persistence & Solvers |
| **FastAPI Interactive Docs** | `8000` | `http://127.0.0.1:8000/docs` | Swagger UI API Documentation |
| **Cloudflare Quick Tunnel** | Dynamic | `https://<tunnel-subdomain>.trycloudflare.com` | Public HTTPS Ingress Tunnel for Vapi Webhooks |

---

## Canonical Local Startup Procedure

### 1. Start FastAPI Backend Server (Terminal 1)
```bash
# Seed initial database records (if not already initialized)
python scripts/seed_database.py

# Start FastAPI server on port 8000
python -m uvicorn services.api.app.main:app --host 0.0.0.0 --port 8000
```
> **Governance Note**: Only one FastAPI process should own port 8000. Inspect and avoid duplicate processes using `Get-NetTCPConnection -LocalPort 8000`.

### 2. Start Next.js Web Dashboard (Terminal 2)
```bash
# Start Next.js development server on port 3000
pnpm --filter web dev
```
> **Governance Note**: Only one Next.js dev server should own port 3000.

### 3. Start Cloudflare Quick Tunnel for Vapi Webhooks (Terminal 3)
```bash
# Start Cloudflare Quick Tunnel forwarding to port 8000
cloudflared tunnel --url http://localhost:8000
```
> **Governance Note**: 
> - The Cloudflare Quick Tunnel forwards public HTTPS traffic directly to local FastAPI (`http://localhost:8000`).
> - The tunnel process must remain running for external Vapi voice agent calls and custom tool execution.
> - Quick Tunnel URLs are temporary and change when recreated. When a new URL is generated, update the Vapi Custom Tool Server URL accordingly.
> - The Vapi tool webhook (`POST /api/v1/voice/webhooks/vapi`) accepts `POST` requests. Testing via browser `GET` will return `405 Method Not Allowed`, which is expected.

---

## Key Health & Connectivity Verification Commands

```bash
# Test local FastAPI health
curl http://127.0.0.1:8000/api/v1/health

# Test local Voice health
curl http://127.0.0.1:8000/api/v1/voice/health

# Test public Cloudflare Tunnel health
curl https://<tunnel-subdomain>.trycloudflare.com/api/v1/health

# Test public Cloudflare Tunnel voice health
curl https://<tunnel-subdomain>.trycloudflare.com/api/v1/voice/health
```
