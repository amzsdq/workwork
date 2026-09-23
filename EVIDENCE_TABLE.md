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
| 22m | PROBE-22M-20260923T220655KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_PENDING_WAKE | pre-protocol target timing is not current clock authority | W3_MIXED_IO | supporting only; cannot promote strict bound |
| 22m | PROBE-22M-SERVERCLOCK-20260923-R3 | GITHUB_SERVER_MARKER_V1 | ACTIVE | START marker server time 2026-09-23T13:32:22Z; END pending | W3_MIXED_IO | NONE_ACTIVE |

## Current empirical conclusion

- LEGACY_EXPLORATORY_LOWER_BOUND: **20m**.
- SERVER_CLOCK_SAFE_LOWER_BOUND: **unresolved** until a valid `GITHUB_SERVER_MARKER_V1` strict pass plus retrospective WAKE_OK is completed.
- SERVER_CLOCK_FAILURE_BOUNDARY: **unresolved**.
- Credible duration failures under the new server-clock protocol: **0**.
- Current strict case: **SC-A22-CLOCK-01**.
- Active probe: **PROBE-22M-SERVERCLOCK-20260923-R3**. Do not start a duplicate while its START marker remains unmatched by a terminal END marker/classification.
- Current START marker: issue comment `5795782562`, raw server `created_at=2026-09-23T13:32:22Z`.
- Scheduler prearm was verified for server-derived target+gap wake at `2026-09-23T13:57:22Z`.
- Direct active-work seconds/productive_ratio remain uninstrumented and will not be fabricated. Durable checkpoints record sustained W3 decision-relevant work.
- Pre-protocol runs remain useful for workload/profile/supporting context but cannot alone advance a new strict duration bound or cap.
- Production OPERATING_CAP, PRODUCTIVE_CAP, SOFT_CUTOFF, HARD_CAP, CLOSE_RESERVE, and SAFETY_MARGIN remain **not promoted**.

## Clock evidence anchors

- Protocol: `GITHUB_SERVER_CLOCK_PROTOCOL.md`
- Clock lane: GitHub issue #1, `[CLOCK] Runtime Work Duration Markers`
- Clock-lane validation comment: issue comment `5795611991`
- Active START marker: issue comment `5795782562`
- Canonical active evidence: `runtime-boundary/PROBE-22M-SERVERCLOCK-20260923-R3/`

This table is derived. Raw marker REST resources, raw per-probe evidence, `state/events.log`, and fresh `state/current.json` govern strict classification.
