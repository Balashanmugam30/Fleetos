# Fleetos Monorepo Contribution & Architectural Guidelines

Product: **Fleetos**

---

## Core Engineering Rules

1. **Deterministic Optimization**: The LLM (ATLAS) NEVER invents vehicle routes or load assignments. Google OR-Tools is authoritative for all optimization math.
2. **Bright Professional UI Policy**: Fleetos UI must maintain a bright, clean, enterprise logistics software visual theme. Dark hacker, cyberpunk, or neon themes are prohibited.
3. **No Hardcoded Secrets**: Secrets (Vapi API keys, Twilio SID/tokens, database passwords) must never be committed to Git.
4. **Canonical Entity IDs**: Use `L01-L05` for Lorries, `D01-D05` for Drivers, and `S01-S12` for Shipments in seed datasets.
5. **Real Telephony Goal**: The primary target for ATLAS is a real PSTN telephone call ringing a physical mobile device. Do not silently downgrade this to a browser voice chat widget.
