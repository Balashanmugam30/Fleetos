"""
Fleetos Sarvam Voice Agent Integration CLI Runner
Module Boundary: scripts/run_sarvam_agent_test.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

import sys
import os
import asyncio
import json
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.voice.sarvam_config import sarvam_config

async def execute_sarvam_health_and_dispatch():
    print("=== FLEETOS SARVAM VOICE AGENT CLI TEST ===")
    print(f"Sarvam Configured: {sarvam_config.is_sarvam_configured}")
    print(f"Twilio Configured: {sarvam_config.is_twilio_configured}")
    print(f"Real PSTN Ready: {sarvam_config.is_real_pstn_ready}")

    base_url = "http://127.0.0.1:8000"

    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1. Health check
        health_resp = await client.get(f"{base_url}/api/v1/voice/health")
        print("\n1. Voice Health Response:")
        print(json.dumps(health_resp.json(), indent=2))

        # 2. Outbound Call Dispatch (STATUS_CHECK for D03)
        call_payload = {
            "driver_id": "D03",
            "call_type": "STATUS_CHECK"
        }
        dispatch_resp = await client.post(f"{base_url}/api/v1/voice/calls", json=call_payload)
        print("\n2. Call Dispatch Response:")
        print(json.dumps(dispatch_resp.json(), indent=2))

if __name__ == "__main__":
    asyncio.run(execute_sarvam_health_and_dispatch())
