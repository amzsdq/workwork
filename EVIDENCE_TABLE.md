# Runtime Evidence Table

Only directly observed timing evidence may affect the runtime boundary.

| Target | Result | Actual elapsed | Useful work | Clean close | Scheduler verified | Next wake | Boundary effect |
|---|---|---:|---:|---|---|---|---|
| 10m | PRIOR_OPERATIONAL_BASELINE | unknown | unknown | prior operational evidence | unknown | unknown | SAFE_LOWER_BOUND remains 10m, not formally revalidated here |
| 12m | SETUP / UNDER_TARGET | unknown | unknown | no | n/a | n/a | NONE |
| 12m | UNDER_TARGET_INSUFFICIENT_WORK | unknown | unknown | no | n/a | n/a | NONE |
| 12m | UNDER_TARGET | timestamp suspect | unknown | no | n/a | n/a | NONE; excluded from timing evidence |
| 12m | UNDER_TARGET | 26s | 20s | no | n/a | n/a | NONE |

## Current empirical conclusion
- SAFE_LOWER_BOUND: 10m from prior operational evidence only.
- 12m clean timing passes: 0.
- Credible duration failures: 0.
- FAILURE_BOUNDARY: unresolved.
- Next empirical target: 12m.

This table is a derived audit aid. `state/events.log` remains canonical append-only evidence.
