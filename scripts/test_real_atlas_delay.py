"""
Fleetos Real ATLAS Delay Report Call Test Script
Module Boundary: scripts/test_real_atlas_delay.py
"""

import sys
import os
import time
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    print("=== FLEETOS REAL ATLAS DELAY REPORT CALL DISPATCH TEST ===")
    base_url = "http://127.0.0.1:8000"

    payload = {
        "driver_id": "D03",
        "call_type": "DELAY_REPORT",
        "context_notes": "Driver reporting a 45-minute loading delay for Lorry L03"
    }

    print("\nDispatching DELAY_REPORT call for Driver D03 (Lorry L03)...")
    try:
        call_resp = httpx.post(f"{base_url}/api/v1/voice/calls", json=payload)
        print("Call Response Code:", call_resp.status_code)
        rec = call_resp.json()
        print("Call ID:", rec.get("id"))
        print("Status:", rec.get("status"))
        print("Provider:", rec.get("provider"))
        print("Call SID:", rec.get("external_call_id"))
        print("Initial Event ID:", rec.get("event_id"))
        print("\nMonitoring call progression for 15 seconds...")

        for i in range(3):
            time.sleep(5)
            detail_resp = httpx.get(f"{base_url}/api/v1/voice/calls/{rec.get('id')}")
            det = detail_resp.json()
            print(f"[{i*5 + 5}s] Status: {det.get('status')}, Duration: {det.get('duration_seconds')}s, Event ID: {det.get('event_id')}")

    except Exception as err:
        print("Error dispatching delay report call:", err)

if __name__ == "__main__":
    main()
