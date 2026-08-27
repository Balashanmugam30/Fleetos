# Fleetos ATLAS Agent & Tool Authority Boundaries

Product: **Fleetos**  
Voice Agent: **ATLAS**

---

## Authority Boundaries

1. **LLM is NOT the Optimizer**: ATLAS interprets natural language, formats backend tool calls, and explains operational decisions. Google OR-Tools is authoritative for all route solving.
2. **Tool Validation**: ATLAS tool executions (e.g. `report_delay`, `report_breakdown`) undergo server-side validation against lorry capacity, time windows, and driver rules before state mutation.
