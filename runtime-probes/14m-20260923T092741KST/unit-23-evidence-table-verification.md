# Unit 23 — Evidence-table verification

Probe: STRICT-14M-20260923T092741KST

Post-repair verification confirms EVIDENCE_TABLE.md now faithfully reports the canonical 12m pass and current 14m target. The stale-derived-state defect discovered at probe start is closed.

This means a successor reading only durable state + canonical ledger + derived table will no longer be told contradictory next targets.
