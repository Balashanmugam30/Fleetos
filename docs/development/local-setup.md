# Fleetos Local Development Setup Guide

Welcome to the local development guide for **Fleetos** (Agentic Multimodal Fleet Intelligence Platform).

---

## Prerequisites

1. **Node.js**: v22.0+ (`node -v`)
2. **pnpm**: v10.0+ (`pnpm -v`)
3. **Python**: v3.13.0+ (`python --version`)
4. **Git**: v2.40+ (`git --version`)

---

## 1. Monorepo Setup

```bash
# Clone the repository
git clone https://github.com/Balashanmugam30/Fleetos.git
cd Fleetos

# Install Node dependencies across monorepo workspace
pnpm install

# Setup environment variables
cp .env.example .env
```

---

## 2. Python Environment & Backend Setup

```bash
# Create Python virtual environment (Optional but recommended)
python -m venv .venv
# Windows PowerShell activation:
.venv\Scripts\Activate.ps1

# Install required Python dependencies
pip install -r requirements.txt

# Run FastAPI backend server (Port 8000)
pnpm run dev:api
```

---

## 3. Web Dashboard Shell (Port 3000)

```bash
# Run Next.js web application
pnpm run dev:web
```

Access the Web Control Tower at `http://localhost:3000`.

---

## 4. Verification Commands

- **Web Application Build**: `pnpm run build:web`
- **FastAPI Endpoints Test**: `python -c "import requests; print(requests.get('http://localhost:8000/api/v1/health').json())"`
- **OR-Tools Package Check**: `python -c "import ortools; print('OR-Tools version:', ortools.__version__)"`
