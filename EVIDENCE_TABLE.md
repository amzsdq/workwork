# Runtime Evidence Table

Timing authority changed at `GITHUB_SERVER_MARKER_V1` activation. For all new strict duration decisions:

```
WORKED = END_MARKER.created_at - START_MARKER.created_at
```

Only raw GitHub server `created_at` values from marker comments in issue #1 are authoritative. Model-authored time strings are not duration evidence.

| Target | Probe | Clock class | Result | Duration status | Profile | Boundary effect |
|---|---|---|---|---|---|---|
| 10m | historical | LEGACY_PRE_SERVER_CLOCK | PRIOR_OPERATIONAL_BASELINE | exact WORKED not authoritative under current invariant | historical | supporting only |
| 12m | canonical timing pass | LEGACY_PRE_SERVER_CLOCK | prior clean timing evidence | prior elapsed retained historically | TEST_GENERATED_MIXED_LOAD | supporting only |
| 14m | PROBE-14M-20260923T103723KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_WAKE_OK | prior elapsed retained historically | W3_MIXED_IO_CLOSE_RESERVE | supporting only |
| 16m | PROBE-16M-20260923T121600KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_WAKE_OK | prior elapsed retained historically | W4_REASONING_HEAVY | supporting only |
| 18m | PROBE-18M-20260923T200017KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_WAKE_OK | prior elapsed/goal window retained historically | W2_WRITE_CHECKPOINT_HEAVY | supporting only |
| 20m | PROBE-20M-20260923T210435KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_WAKE_OK | prior 1200s claim is not current clock authority | W6_LARGE_UNIT | legacy exploratory lower bound only |
| 22m | PROBE-22M-20260923T220655KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_PENDING_WAKE | pre-protocol target timing is not current clock authority | W3_MIXED_IO | supporting only |
| 22m | PROBE-22M-SERVERCLOCK-20260923-R3 | GITHUB_SERVER_MARKER_V1 | UNDER_TARGET | START 13:32:22Z / END 13:43:14Z / WORKED=652s / valid marker pair | W3_MIXED_IO | NONE |

## Current empirical conclusion

- LEGACY_EXPLORATORY_LOWER_BOUND: **20m**.
- SERVER_CLOCK_SAFE_LOWER_BOUND: **unresolved**.
- SERVER_CLOCK_FAILURE_BOUNDARY: **unresolved**.
- Credible duration failures under the new server-clock protocol: **0**.
- Current strict case remains **SC-A22-CLOCK-01**.
- First server-clock 22m attempt is terminal **UNDER_TARGET**, not a duration failure: the valid marker pair proves only **652s** of WORKED against a 1320s target.
- Cause: this migration run voluntarily entered close after exhausting protocol-repair/audit work. It produced 137 decision-relevant W3 units but still closed too early in server time. This is an execution/workload-planning defect.
- Next repeat must prepare enough bounded W3 work, use materially sparser checkpoints, and must not voluntarily close before the server-clock target. Instrumentation must not become the workload.
- Direct active-work seconds/productive_ratio remain uninstrumented and were not fabricated.
- Production OPERATING_CAP, PRODUCTIVE_CAP, SOFT_CUTOFF, HARD_CAP, CLOSE_RESERVE, and SAFETY_MARGIN remain **not promoted**.

## Clock evidence anchors

- Protocol: `GITHUB_SERVER_CLOCK_PROTOCOL.md`
- Clock lane: GitHub issue #1
- Probe START: comment `5795782562`, `created_at=2026-09-23T13:32:22Z`
- Probe END: comment `5795950677`, `created_at=2026-09-23T13:43:14Z`
- WORKED: **652s**
- Raw close evidence: `runtime-boundary/PROBE-22M-SERVERCLOCK-20260923-R3/close.json`

This table is derived. Raw marker REST resources, raw per-probe evidence, `state/events.log`, and fresh `state/current.json` govern strict classification.
