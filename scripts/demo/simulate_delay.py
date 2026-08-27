"""
Fleetos Driver Delay Event Simulation Script
Script Path: scripts/demo/simulate_delay.py
"""

import sys
import requests

def simulate_delay(lorry_id="L03", delay_minutes=45, reason="loading_delay"):
    print(f"Simulating driver delay event for Lorry {lorry_id} (+{delay_minutes}m)...")
    payload = {
        "event_id": f"evt_sim_{lorry_id}",
        "event_type": "DRIVER_DELAY_REPORTED",
        "source": "ATLAS_VOICE",
        "lorry_id": lorry_id,
        "payload": {
            "delay_minutes": delay_minutes,
            "reason": reason
        }
    }
    print("Simulated event payload constructed:")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    import json
    simulate_delay()
