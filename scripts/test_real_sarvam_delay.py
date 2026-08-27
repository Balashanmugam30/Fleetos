"""
Fleetos Real Sarvam Delay Tool Execution Script
Module Boundary: scripts/test_real_sarvam_delay.py
"""

import sys
import os
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    print("=== FLEETOS REAL SARVAM TOOL ENDPOINT DELAY REPORT TEST ===")
    base_url = "http://127.0.0.1:8000"

    payload = {
        "driver_id": "D03",
        "lorry_id": "L03",
        "delay_minutes": 45,
        "reason": "LOADING_DELAY",
        "tool_call_id": "sarvam_cli_test_100"
    }

    print("\nExecuting POST /api/v1/voice/sarvam/tools/report-delay...")
    try:
        resp = httpx.post(f"{base_url}/api/v1/voice/sarvam/tools/report-delay", json=payload)
        print("Response Code:", resp.status_code)
        res_data = resp.json()
        print("Success:", res_data.get("success"))
        print("Event ID:", res_data.get("event_id"))
        print("Event Type:", res_data.get("event_type"))
        print("Message:", res_data.get("message"))
    except Exception as err:
        print("Error executing Sarvam tool endpoint:", err)

if __name__ == "__main__":
    main()
