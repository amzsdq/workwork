# Unit 14 — Continuation invariant

Probe: PROBE-14M-20260923T095323KST

Required invariant for coarse ascent:
- Scheduler is secured before substantive workload.
- Normal close does not rewrite scheduler.
- Current run classifies runtime/close.
- Following invocation classifies prior wake observation before starting its own target work.
- State advances to a higher target only after durable close classification, never merely because the target clock time was intended.

This prevents a lost-close invocation from falsely advancing the research state.
