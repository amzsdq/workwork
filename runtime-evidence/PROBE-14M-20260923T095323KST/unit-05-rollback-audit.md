# Unit 05 — Rollback-policy audit

Probe: PROBE-14M-20260923T095323KST

Rollback semantics correctly separate runtime-boundary failures from admission overshoot and too-small-gap failures. This prevents a later concurrency/gap experiment from falsely lowering a validated runtime cap.

For the present Phase-A probe, rollback remains inactive because no operating cap has yet been promoted.
