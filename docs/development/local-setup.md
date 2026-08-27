# Fleetos Local Development Setup Guide

Product: **Fleetos** (Agentic Multimodal Fleet Intelligence Platform)

---

## Service Architecture & Endpoints

| Service | Port | Endpoint URL | Description |
| :--- | :--- | :--- | :--- |
| **Next.js Web Dashboard** | `3000` | `http://localhost:3000` | React 19 / Next.js 15 Control Tower UI |
| **FastAPI REST API Server** | `8000` | `http://127.0.0.1:8000` | REST API, Database Persistence & Solvers |
| **FastAPI Interactive Docs** | `8000` | `http://127.0.0.1:8000/docs` | Swagger UI API Documentation |

---

## Canonical Local Startup Procedure

### 1. Start FastAPI Backend Server (Terminal 1)
```bash
# Seed initial database records (if not already initialized)
python scripts/seed_database.py

# Start FastAPI server on port 8000
python -m uvicorn services.api.app.main:app --host 0.0.0.0 --port 8000
```

### 2. Start Next.js Web Dashboard (Terminal 2)
```bash
# Start Next.js development server on port 3000
pnpm --filter web dev
```

---

## Key Health & Connectivity Check Commands

```bash
# Test FastAPI health
curl http://127.0.0.1:8000/api/v1/health

# Test Database connection
curl http://127.0.0.1:8000/api/v1/health/db

# Test Lorries data endpoint
curl http://127.0.0.1:8000/api/v1/lorries

# Test Shipments data endpoint
curl http://127.0.0.1:8000/api/v1/shipments
```
