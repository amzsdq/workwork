# Runtime Evidence Table

Only directly observed timing evidence may affect the runtime boundary. `state/events.log` is canonical.

| Target | Result | Actual elapsed | Useful work | Clean close | Scheduler verified | Next wake | Boundary effect |
|---|---|---:|---:|---|---|---|---|
| 10m | PRIOR_OPERATIONAL_BASELINE | unknown | unknown | prior operational evidence | unknown | unknown | historical baseline |
| 12m | SETUP / UNDER_TARGET | unknown | unknown | no | n/a | n/a | NONE |
| 12m | UNDER_TARGET_INSUFFICIENT_WORK | unknown | unknown | no | n/a | n/a | NONE |
| 12m | UNDER_TARGET | timestamp suspect | unknown | no | n/a | n/a | NONE; excluded |
| 12m | UNDER_TARGET | 26s | 20s | no | n/a | n/a | NONE |
| 12m | CLEAN_PASS_WITH_CONCURRENT_CONTROL_ANOMALY | 761s | active mixed-load window; exact useful seconds not claimed | yes | write/state OK | retrospective wake unresolved in event | SAFE_LOWER_BOUND=12m; continue 14m after control reconciliation |

## Current empirical conclusion
- SAFE_LOWER_BOUND: 12m from one canonical clean timing pass, explicitly not a production cap.
- 12m clean timing passes: 1.
- Credible duration failures: 0.
- FAILURE_BOUNDARY: unresolved.
- Current strict empirical target: 14m W3 MIXED_IO.
- The 12m pass had a concurrent control-plane anomaly, but the canonical event records clean close, durable checkpoint, scheduler write/state OK, and no duration/non-duration failure; subsequent control reconciliation is complete in current state.

This table is a derived audit aid. `state/events.log` remains canonical append-only evidence.
