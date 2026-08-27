"""
Fleetos Sarvam Report Delay Tool Execution CLI Runner
Module Boundary: scripts/run_sarvam_delay_test.py
Product: Fleetos (Agentic Multimodal Fleet Intelligence Platform)
"""

import sys
import os
import asyncio
import json
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.voice.sarvam_config import sarvam_config

async def execute_sarvam_tool_delay():
    print("=== FLEETOS SARVAM TOOL EXECUTION CLI TEST ===")
    base_url = "http://127.0.0.1:8000"

    payload = {
        "driver_id": "D03",
        "lorry_id": "L03",
        "delay_minutes": 45,
        "reason": "LOADING_DELAY",
        "tool_call_id": "cli_sarvam_tc_45min"
    }

    headers = {
        "Content-Type": "application/json",
        "X-Sarvam-Tool-Secret": sarvam_config.sarvam_tool_secret
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            f"{base_url}/api/v1/voice/sarvam/tools/report-delay",
            json=payload,
            headers=headers
        )
        print("\n1. Sarvam Tool Report Delay Response:")
        print(f"HTTP Status: {resp.status_code}")
        print(json.dumps(resp.json(), indent=2))

        # Verify Event Ledger update
        events_resp = await client.get(f"{base_url}/api/v1/events")
        events = events_resp.json()
        delay_events = [e for e in events if e.get("event_type") == "DRIVER_DELAY_REPORTED"]
        print(f"\n2. Total DRIVER_DELAY_REPORTED Events in Ledger: {len(delay_events)}")
        if delay_events:
            print("Latest Delay Event:", json.dumps(delay_events[0], indent=2))

if __name__ == "__main__":
    asyncio.run(execute_sarvam_tool_delay())
