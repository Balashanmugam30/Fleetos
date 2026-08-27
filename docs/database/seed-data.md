# Fleetos Canonical Seed Data & Scenario Guide

Product: **Fleetos**

---

## Canonical Seed Scenario Coverage (`database/seed/demo_seed.json`)

- **5 Lorries (L01 – L05)**:
  - L01: KA-01-EQ-1001 (10,000 kg / 45 m³, 3.5 km/L, Bengaluru)
  - L02: KA-01-EQ-1002 (15,000 kg / 60 m³, 2.8 km/L, Hosur)
  - L03: TN-02-AB-3003 (8,000 kg / 35 m³, 4.2 km/L, Chennai)
  - L04: AP-03-CD-4004 (12,000 kg / 50 m³, 3.0 km/L, Vijayawada - UNAVAILABLE)
  - L05: TN-09-XY-5005 (14,000 kg / 55 m³, 5.2 km/L, Vellore - IDLE & AVAILABLE)

- **12 Shipments (S01 – S12)**:
  - S01 & S02: Same-destination cluster (Chennai -> Bengaluru Electronic City)
  - S03: High priority load (Hosur -> Sriperumbudur)
  - S11: Heavy weight load (7,500 kg)
  - S12: Target anchor shipment (Urgent, strict 18:00 IST deadline)
