# Unit 05 — Derived evidence repair

Probe: STRICT-14M-20260923T092741KST

Repaired EVIDENCE_TABLE.md to match canonical state/events.log:
- 12m clean timing passes: 1
- observed elapsed: 761s
- clean close/checkpoint/scheduler state: verified in canonical event
- safe lower bound: 12m, not a production cap
- current strict target: 14m

This was a necessary reproducibility repair discovered by the active W3 mixed-I/O probe. No historical canonical event was rewritten.
