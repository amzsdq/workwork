# Unit 07 — Evidence-table audit

Probe: PROBE-14M-20260923T095323KST

Current derived table is consistent with state: one strict 12m clean timing pass, zero credible duration failures, unresolved upper boundary, strict next target 14m W3 MIXED_IO.

Important limitation retained: the table is derived; canonical append-only timing evidence remains the authoritative source. This 14m probe must not update SAFE_LOWER_BOUND until durable close is completed.
