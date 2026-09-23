# R4 measurement-overhead risk audit

## Risk

A runtime experiment can become self-defeating if instrumentation dominates the workload. R3 demonstrated a related failure mode: many protocol/audit units were completed but the finite queue ended before the target.

## R4 controls

- START/END marker operations are mandatory and minimal.
- Scheduler pre-arm occurs once at start and is not rewritten at normal close.
- Mid-run checkpoints are sparse.
- Analysis writes are themselves substantive research outputs, not synthetic heartbeat writes.
- Repeated reads are used only when they validate fresh state or server-side evidence.

## Interpretation

Tool/connector latency is part of the invocation wall-clock environment and therefore naturally included in WORKED. It should not be mislabeled as direct active work. This distinction is why active_work_sec remains null while substantive-unit count and durable goal-directed outputs are retained.

## Final-policy implication

If later evidence shows that high write/checkpoint frequency materially reduces useful-work ratio or close reliability, the operating policy should favor fewer, higher-value durable checkpoints rather than attempting to subtract tool latency from the authoritative wall clock.
