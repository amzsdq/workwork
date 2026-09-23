# Runtime Evidence Table

Only directly observed timing evidence may affect the runtime boundary. `state/events.log` is canonical. This table is a derived audit aid and must agree with the canonical ledger and fresh `state/current.json`.

| Target | Probe | Result | Actual elapsed | Useful work | Profile | Clean close | Scheduler verified | Next wake | Boundary effect |
|---|---|---|---:|---:|---|---|---|---|---|
| 10m | historical | PRIOR_OPERATIONAL_BASELINE | unknown | unknown | historical | prior operational evidence | unknown | unknown | historical baseline |
| 12m | setup series | UNDER_TARGET / SETUP | various/unknown | various/unknown | mixed setup | no | n/a | n/a | NONE |
| 12m | canonical timing pass | CLEAN_PASS_WITH_CONCURRENT_CONTROL_ANOMALY | 761s | active mixed-load window; exact useful seconds not claimed | TEST_GENERATED_MIXED_LOAD | yes | WRITE_OK / STATE_OK | unresolved in original event | SAFE_LOWER_BOUND=12m |
| 14m | PROBE-14M-20260923T095323KST | UNDER_TARGET_INSUFFICIENT_WORK | not claimed | 33 work units | W3_MIXED_IO | yes | WRITE_OK / STATE_OK | pending | NONE |
| 14m | PROBE-14M-20260923T100949KST | INCOMPLETE_CLOSE_NOT_STRICT_PASS | target-class work present; exact terminal elapsed not used | 181 durable batches observed | W3_MIXED_IO_EXPANDED_BACKLOG | no durable close | WRITE_OK / STATE_OK | n/a for strict PASS | NONE |
| 14m | PROBE-14M-20260923T103723KST | CLEAN_PASS_WAKE_OK | 928s | exact active-work seconds not claimed | W3_MIXED_IO_CLOSE_RESERVE | yes | WRITE_OK / STATE_OK | WAKE_OK at 11:56:30 KST | SAFE_LOWER_BOUND=14m |
| 16m | PROBE-16M-20260923T121600KST | CLEAN_PASS_WAKE_OK | >=996s | exact active-work seconds not claimed | W4_REASONING_HEAVY | yes | WRITE_OK / STATE_OK | WAKE_OK at 12:49:47 KST | SAFE_LOWER_BOUND=16m |
| 18m | PROBE-18M-20260923T192315KST | UNDER_TARGET | not established | not established | W2_WRITE_CHECKPOINT_HEAVY | no | WRITE_OK / STATE_OK | prearmed; not used as PASS evidence | NONE |

## Current empirical conclusion

- SAFE_LOWER_BOUND: **16m**.
- Credible duration failures: **0**.
- FAILURE_BOUNDARY: **unresolved**.
- Current strict empirical target: **18m W2 WRITE_CHECKPOINT_HEAVY**.
- The 19:23:15 18m probe is classified UNDER_TARGET because only start evidence persisted; missing close alone is not a duration failure.
- Next 18m attempt must sustain useful work and capture SURVIVAL_BOUNDARY + PRODUCTIVE_WINDOW + COMPLETION_ENVELOPE evidence.
- Production operating cap is still **not promoted**.

## Evidence anchors

- 14m clean close: `runtime/probes/PROBE-14M-20260923T103723KST/close.json`
- 14m WAKE_OK state transition: commit `214b091d23869276b03218acd3cd3f7777917001`
- 16m clean close: `runtime/probes/PROBE-16M-20260923T123236KST/close.json`
- 16m WAKE_OK state transition: commit `bfdea28516886ebcea28d8207af95d521ea63757`
- 18m under-target classification: `runtime-boundary/PROBE-18M-20260923T192315KST/start.json`

This table is derived. Raw per-probe evidence plus `state/events.log` and fresh `state/current.json` remain authoritative.
