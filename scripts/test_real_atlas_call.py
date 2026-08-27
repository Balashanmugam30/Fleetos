"""
Fleetos Real ATLAS Voice Call Verification Script
Module Boundary: scripts/test_real_atlas_call.py
"""

import sys
import os
import time
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    print("=== FLEETOS REAL ATLAS VOICE CALL DISPATCH TEST ===")
    base_url = "http://127.0.0.1:8000"

    # 1. Health check
    try:
        h_resp = httpx.get(f"{base_url}/api/v1/voice/health")
        print("Voice Health:", h_resp.json())
    except Exception as err:
        print("Error connecting to local voice service:", err)
        return

    # 2. Dispatch outbound call for D03
    payload = {
        "driver_id": "D03",
        "call_type": "STATUS_CHECK"
    }

    print("\nDispatching ATLAS call for Driver D03 (Lorry L03)...")
    try:
        call_resp = httpx.post(f"{base_url}/api/v1/voice/calls", json=payload)
        print("Call Response Code:", call_resp.status_code)
        rec = call_resp.json()
        print("Call ID:", rec.get("id"))
        print("Status:", rec.get("status"))
        print("Provider:", rec.get("provider"))
        print("Call SID / Ext ID:", rec.get("external_call_id"))
    except Exception as err:
        print("Error dispatching call:", err)

if __name__ == "__main__":
    main()
