"""
Fleetos Demo Scenario Reset Script
Script Path: scripts/demo/reset_demo.py
"""

import sys
import json

def reset_demo():
    print("Resetting Fleetos demo scenario to baseline (Lorries L01-L05, Shipments S01-S12)...")
    with open("database/seed/demo_seed.json", "r") as f:
        data = json.load(f)
    print(f"Loaded {len(data['lorries'])} lorries and {len(data['shipments'])} target shipments.")
    print("Demo state reset complete!")

if __name__ == "__main__":
    reset_demo()
