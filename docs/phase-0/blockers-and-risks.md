# Phase 0 Blockers & Risk Registry

Product Name: **Fleetos**

---

## Identified Risk Registry & Mitigation Strategies

### Risk 1: Twilio / Vapi Outbound Telephony Calling to Indian PSTN (+91)
- **Category**: Telephony / Carrier Regulation
- **Severity**: `HIGH`
- **Description**: Telecom Regulatory Authority of India (TRAI) and Twilio Geo-Permissions restrict unverified international outbound calling to Indian mobile numbers. Trial accounts restrict calling to verified caller IDs.
- **Mitigation**:
  1. Verify target phone number in Twilio Verified Caller IDs during development.
  2. Enable International Calling Geo-Permissions for India (+91) in Twilio Console.
  3. Support E.164 phone formatting (`+91XXXXXXXXXX`).
- **Fallback Plan**: Interactive Web Audio Simulator in Dashboard (`LEVEL 3`) clearly labeled as Demo Simulator.

### Risk 2: Host Environment Machine Constraints for Native iOS Swift/ARKit Compilation
- **Category**: Development Hardware
- **Severity**: `MEDIUM`
- **Description**: Development host machine is Windows 11 Home (no native `xcodebuild` / `swift` CLI tools). Native iOS compilation requires macOS Xcode.
- **Mitigation**:
  1. Maintain clean native iOS project workspace (`apps/ar`) using Swift/ARKit/RealityKit ready for compilation on macOS.
  2. Build high-performance WebAR camera overlay using MindAR + Three.js (`apps/web/ar`) for local browser execution and live cross-platform testing.
- **Fallback Plan**: WebAR MindAR / Three.js live camera marker tracker inside `apps/web/ar`.

### Risk 3: LLM Non-Determinism in Route Optimization
- **Category**: Algorithmic Integrity
- **Severity**: `HIGH`
- **Description**: Allowing an LLM to invent vehicle routes or compute spatial assignments causes hallucinated, infeasible, and non-deterministic logistics decisions.
- **Mitigation**: Strict authority boundary lock. The LLM (ATLAS) is strictly an interface/extractor. Deterministic Google OR-Tools Routing Solver / RoutingModel handles 100% of route and load calculations.
- **Fallback Plan**: Deterministic pre-computed fallback matrix if OR-Tools solver encounters unexpected parameter errors.

### Risk 4: Mapbox API Rate Limits & Offline Network Latency
- **Category**: External Service Dependency
- **Severity**: `LOW`
- **Description**: External map tile loading or route matrix requests could fail during live demo if network drops.
- **Mitigation**: Pre-cached distance and travel-time matrix between canonical hubs; internal Haversine distance calculator.
- **Fallback Plan**: Automatic switch to internal offline matrix mode when `MAPBOX_TOKEN` is missing or offline.

---

## Blockers Summary Matrix

| Blocker ID | Description | Status | Resolution |
| :--- | :--- | :--- | :--- |
| `BLK-01` | Missing `ortools` in Python 3.13 | `RESOLVED` | Successfully installed `ortools-9.15.6755` via pip. |
| `BLK-02` | Native Xcode build on Windows host | `MITIGATED` | Monorepo target `apps/ar` prepared for iOS; WebAR `apps/web/ar` deployed for web. |
| `BLK-03` | Twilio India PSTN Credentials required for live calls | `PENDING KEY` | Architecturally verified; live call requires user API key in `.env`. |
