# Unit 06 — Reproducibility audit

Probe: STRICT-14M-20260923T092741KST

A fresh worker can now reconstruct the boundary search from durable files as follows:
1. state/current.json: mode STRICT_DURATION, last strict clean 12m, next strict target 14m, parallel work deferred.
2. state/events.log: canonical 12m clean timing event with elapsed 761s and 32s close overhead.
3. EVIDENCE_TABLE.md: reconciled derived summary matching the canonical event.
4. RUNTIME_WORKLOAD_PROFILES.md: 14m profile W3 MIXED_IO.
5. MAX_SAFE_RUNTIME_RESEARCH.md + RUNTIME_BOUNDARY_DECISION_RULE.md: one clean 14m pass may advance coarse target to 16m but cannot promote production cap.
6. This probe directory: immutable start and bounded work-unit evidence.

No dependency on chat-body reconstruction is required for these facts.

Remaining requirement for this probe: continue substantive W3 work until the 14m target is directly crossed, then durable close and classification.
