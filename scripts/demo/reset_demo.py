"""
Fleetos Demo Scenario Reset Script (Guarded)
Script Path: scripts/demo/reset_demo.py
"""

import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.seed_database import seed_database

def reset_demo():
    demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"
    if not demo_mode and "--force" not in sys.argv:
        print("Error: Demo reset blocked. Set DEMO_MODE=true or pass --force flag to execute reset.")
        sys.exit(1)

    print("Executing guarded demo reset...")
    asyncio.run(seed_database(force_reset=True))

if __name__ == "__main__":
    reset_demo()
