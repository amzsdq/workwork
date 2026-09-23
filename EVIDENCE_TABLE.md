# Runtime Evidence Table

Strict timing authority:
`WORKED = END_MARKER.created_at - START_MARKER.created_at`
using only raw GitHub server `created_at` values from issue #1 marker comments.

| Target | Probe | Clock class | Result | Duration status | Profile | Boundary effect |
|---|---|---|---|---|---|---|
| 10m | historical | LEGACY_PRE_SERVER_CLOCK | PRIOR_OPERATIONAL_BASELINE | exact WORKED not current authority | historical | supporting only |
| 12m | canonical timing pass | LEGACY_PRE_SERVER_CLOCK | prior clean timing evidence | historical timing only | TEST_GENERATED_MIXED_LOAD | supporting only |
| 14m | PROBE-14M-20260923T103723KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_WAKE_OK | historical timing only | W3 | supporting only |
| 16m | PROBE-16M-20260923T121600KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_WAKE_OK | historical timing only | W4 | supporting only |
| 18m | PROBE-18M-20260923T200017KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_WAKE_OK | historical timing only | W2 | supporting only |
| 20m | PROBE-20M-20260923T210435KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_WAKE_OK | historical timing only | W6 | legacy exploratory lower bound only |
| 22m | PROBE-22M-20260923T220655KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_PENDING_WAKE | historical timing only | W3 | supporting only |
| 22m | PROBE-22M-SERVERCLOCK-20260923-R3 | GITHUB_SERVER_MARKER_V1 | UNDER_TARGET | WORKED=652s / valid marker pair | W3 | NONE |
| 22m | PROBE-22M-SERVERCLOCK-20260923-R4 | GITHUB_SERVER_MARKER_V1 | UNDER_TARGET | WORKED=736s / valid marker pair | W3 | NONE |
| 22m | PROBE-22M-SERVERCLOCK-20260923-R5 | GITHUB_SERVER_MARKER_V1 | CLOCK_EVIDENCE_INVALID / NON_DURATION_FAIL | START marker blocked; no WORKED | W3 | NONE |
| 22m | PROBE-22M-SERVERCLOCK-20260924-R6 | GITHUB_SERVER_MARKER_V1 | ACTIVE | START comment 5797598302 / server 2026-09-23T15:23:53Z; END pending | W3 | NONE_ACTIVE |

## Current conclusion
- LEGACY_EXPLORATORY_LOWER_BOUND: 20m.
- SERVER_CLOCK_SAFE_LOWER_BOUND: unresolved.
- SERVER_CLOCK_FAILURE_BOUNDARY: unresolved.
- Credible server-clock duration failures: 0.
- Current strict case: SC-A22-CLOCK-01.
- R3/R4 were workload-design UNDER_TARGET runs, not duration failures.
- R5 was independent clock-provider failure with no boundary effect.
- R6 is active with a materially larger genuine W3 corpus and verified +3m prearm. Do not start a duplicate.
- Direct active_work_sec/productive_ratio remain uninstrumented; do not fabricate them.
- The historical 32s close sample is legacy supporting only; close reserve remains provisional/not promoted.
- OPERATING_CAP, PRODUCTIVE_CAP, SOFT_CUTOFF, HARD_CAP, CLOSE_RESERVE, SAFETY_MARGIN remain not promoted.

## R6 durable anchors
- start: `runtime-boundary/PROBE-22M-SERVERCLOCK-20260924-R6/start.json`
- audit findings: `runtime-boundary/PROBE-22M-SERVERCLOCK-20260924-R6/audit-findings.md`
- checkpoints 01-04 under the same probe directory

This table is derived. Raw marker REST resources, per-probe evidence, event ledger, and fresh current state govern strict classification.
