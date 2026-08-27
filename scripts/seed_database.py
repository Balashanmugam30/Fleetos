"""
Fleetos Canonical Database Seeder Script
Script Path: scripts/seed_database.py
"""

import sys
import os
import json
import asyncio
import datetime

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.api.app.db.database import AsyncSessionLocal, init_db
from services.api.app import models

async def seed_database(force_reset: bool = True):
    print("Initializing Fleetos database schema...")
    await init_db()

    seed_file = os.path.join("database", "seed", "demo_seed.json")
    if not os.path.exists(seed_file):
        print(f"Error: Seed file '{seed_file}' not found.")
        return

    with open(seed_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    async with AsyncSessionLocal() as db:
        if force_reset:
            print("Cleaning existing demo records...")
            await db.execute(models.TrackingPositionModel.__table__.delete())
            await db.execute(models.CallModel.__table__.delete())
            await db.execute(models.EventModel.__table__.delete())
            await db.execute(models.RouteStopModel.__table__.delete())
            await db.execute(models.AssignmentModel.__table__.delete())
            await db.execute(models.RouteModel.__table__.delete())
            await db.execute(models.ShipmentModel.__table__.delete())
            await db.execute(models.LorryModel.__table__.delete())
            await db.execute(models.DriverModel.__table__.delete())
            await db.commit()

        print(f"Seeding {len(data['drivers'])} drivers...")
        for d in data["drivers"]:
            driver = models.DriverModel(
                id=d["id"],
                name=d["name"],
                phone_number=d["phoneNumber"],
                availability_status=d["availabilityStatus"],
                current_lorry_id=d.get("currentLorryId")
            )
            db.add(driver)
        await db.commit()

        print(f"Seeding {len(data['lorries'])} lorries...")
        for l in data["lorries"]:
            lorry = models.LorryModel(
                id=l["id"],
                registration_number=l["registrationNumber"],
                max_weight_kg=l["maxWeightKg"],
                max_volume_m3=l["maxVolumeM3"],
                current_latitude=l["currentLatitude"],
                current_longitude=l["currentLongitude"],
                current_speed_km_h=l.get("currentSpeedKmH", 0.0),
                current_heading_degrees=l.get("currentHeadingDegrees", 0.0),
                fuel_efficiency_km_l=l["fuelEfficiencyKmLiter"],
                driver_id=l.get("driverId"),
                status=l["status"],
                current_route_id=l.get("currentRouteId")
            )
            db.add(lorry)
        await db.commit()

        print(f"Seeding {len(data['shipments'])} shipments (S01-S12)...")
        for s in data["shipments"]:
            deadline_dt = datetime.datetime.fromisoformat(s["deliveryDeadline"].replace("Z", "+00:00"))
            shipment = models.ShipmentModel(
                id=s["id"],
                weight_kg=s["weightKg"],
                volume_m3=s["volumeM3"],
                pickup_address=s["pickupLocation"]["address"],
                pickup_latitude=s["pickupLocation"]["latitude"],
                pickup_longitude=s["pickupLocation"]["longitude"],
                destination_address=s["destination"]["address"],
                destination_latitude=s["destination"]["latitude"],
                destination_longitude=s["destination"]["longitude"],
                delivery_deadline=deadline_dt,
                priority=s["priority"],
                status=s["status"]
            )
            db.add(shipment)
        await db.commit()

        print("Seeding baseline initial assignments and events...")
        # Create baseline initial assignment for S12 on L03
        assignment_s12 = models.AssignmentModel(
            id="asg_s12_l03",
            shipment_id="S12",
            lorry_id="L03",
            sequence=1,
            assignment_reason="Baseline Plan: Urgent shipment assigned to L03",
            status="ACTIVE"
        )
        db.add(assignment_s12)

        # Create baseline initial event
        evt_init = models.EventModel(
            id="evt_baseline_01",
            event_type="SHIPMENT_CREATED",
            source="SYSTEM",
            severity="INFO",
            shipment_id="S12",
            payload_json={"message": "Urgent Shipment S12 created and assigned to L03"},
            resolution_status="RESOLVED"
        )
        db.add(evt_init)
        await db.commit()

        print("Database seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_database(force_reset=True))
