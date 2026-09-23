# Runtime Evidence Table

Only directly observed timing evidence may affect the runtime boundary. `state/events.log` is canonical. This table is a derived audit aid and must agree with the canonical ledger and fresh `state/current.json`.

| Target | Probe | Result | Actual elapsed | Useful work | Profile | Clean close | Scheduler verified | Next wake | Boundary effect |
|---|---|---|---:|---:|---|---|---|---|---|
| 10m | historical | PRIOR_OPERATIONAL_BASELINE | unknown | unknown | historical | prior operational evidence | unknown | unknown | historical baseline |
| 12m | canonical timing pass | CLEAN_PASS_WITH_CONCURRENT_CONTROL_ANOMALY | 761s | active mixed-load window; exact useful seconds not claimed | TEST_GENERATED_MIXED_LOAD | yes | WRITE_OK / STATE_OK | unresolved in original event | SAFE_LOWER_BOUND=12m historical transition |
| 14m | PROBE-14M-20260923T103723KST | CLEAN_PASS_WAKE_OK | 928s | exact active-work seconds not claimed | W3_MIXED_IO_CLOSE_RESERVE | yes | WRITE_OK / STATE_OK | continuation observed | SAFE_LOWER_BOUND=14m |
| 16m | PROBE-16M-20260923T121600KST | CLEAN_PASS_WAKE_OK | >=996s | exact active-work seconds not claimed | W4_REASONING_HEAVY | yes | WRITE_OK / STATE_OK | continuation observed | SAFE_LOWER_BOUND=16m |
| 18m | PROBE-18M-20260923T192315KST | UNDER_TARGET | not established | not established | W2_WRITE_CHECKPOINT_HEAVY | no | WRITE_OK / STATE_OK | prearmed; not PASS evidence | NONE |
| 18m | PROBE-18M-20260923T200017KST | CLEAN_PASS_WAKE_OK | target 1080s reached; exact close-end elapsed unclaimed | goal-directed window 1075.783s (99.61% of target window); direct active seconds unknown; 78 useful units | W2_WRITE_CHECKPOINT_HEAVY | yes | WRITE_OK / STATE_OK | observed 20:21:38, 21s after prearmed wake | SAFE_LOWER_BOUND=18m |

## Current empirical conclusion

- SAFE_LOWER_BOUND: **18m** under the existing strict continuation-observed rule.
- Credible duration failures: **0**.
- FAILURE_BOUNDARY: **unresolved**.
- The 20:00:17 W2 probe reached the 18m target at 20:18:17 with sustained goal-directed work, clean durable close, and the next invocation was observed at 20:21:38, 21s after the prearmed 20:21:17 wake.
- Direct active-work seconds/productive_ratio are not fabricated; the directly bounded goal-directed window is 1075.783s, 99.61% of the 1080s target window, with 78 heterogeneous useful units.
- Exact close overhead for this 18m probe remains unclaimed because direct close-end instrumentation was not durably persisted; the prior directly measured 32s close-overhead sample remains the only direct sample in current state.
- Production OPERATING_CAP, PRODUCTIVE_CAP, SOFT_CUTOFF, HARD_CAP, CLOSE_RESERVE, and SAFETY_MARGIN are still **not promoted**.
- NEXT_CASE: **SC-A20-01**, target **20m**, profile **W6_LARGE_UNIT**.

## Evidence anchors

- 14m clean close: `runtime/probes/PROBE-14M-20260923T103723KST/close.json`
- 16m clean close: `runtime/probes/PROBE-16M-20260923T123236KST/close.json`
- prior 18m under-target evidence: `runtime-boundary/PROBE-18M-20260923T192315KST/start.json`
- 18m clean pass: `runtime-boundary/PROBE-18M-20260923T200017KST/close.json`

This table is derived. Raw per-probe evidence plus `state/events.log` and fresh `state/current.json` remain authoritative.
