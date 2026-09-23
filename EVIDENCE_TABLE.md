# Runtime Evidence Table

Strict timing authority: `WORKED = END_MARKER.created_at - START_MARKER.created_at` using raw GitHub server issue-comment timestamps.

| Target | Probe | Clock class | Result | Duration status | Profile | Boundary effect |
|---|---|---|---|---|---|---|
| 10m | historical | LEGACY_PRE_SERVER_CLOCK | PRIOR_OPERATIONAL_BASELINE | exact WORKED not current authority | historical | supporting only |
| 12m | canonical timing pass | LEGACY_PRE_SERVER_CLOCK | prior clean timing evidence | historical timing only | mixed | supporting only |
| 14m | PROBE-14M-20260923T103723KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_WAKE_OK | historical timing only | W3 | supporting only |
| 16m | PROBE-16M-20260923T121600KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_WAKE_OK | historical timing only | W4 | supporting only |
| 18m | PROBE-18M-20260923T200017KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_WAKE_OK | historical timing only | W2 | supporting only |
| 20m | PROBE-20M-20260923T210435KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_WAKE_OK | historical timing only | W6 | legacy exploratory lower bound only |
| 22m | PROBE-22M-20260923T220655KST | LEGACY_PRE_SERVER_CLOCK | prior CLEAN_PASS_PENDING_WAKE | historical timing only | W3 | supporting only |
| 22m | PROBE-22M-SERVERCLOCK-20260923-R3 | GITHUB_SERVER_MARKER_V1 | UNDER_TARGET | WORKED=652s valid pair | W3 | NONE |
| 22m | PROBE-22M-SERVERCLOCK-20260923-R4 | GITHUB_SERVER_MARKER_V1 | UNDER_TARGET | WORKED=736s valid pair | W3 | NONE |
| 22m | PROBE-22M-SERVERCLOCK-20260923-R5 | GITHUB_SERVER_MARKER_V1 | NON_DURATION_FAIL / clock invalid secondary | START blocked; no WORKED | W3 | NONE |
| 22m | PROBE-22M-SERVERCLOCK-20260924-R6 | GITHUB_SERVER_MARKER_V1 | UNDER_TARGET | START 15:23:53Z / END 15:40:08Z / WORKED=975s valid pair | W3 | NONE |
| 22m | PROBE-22M-SERVERCLOCK-20260924-R7 | GITHUB_SERVER_MARKER_V1 | UNDER_TARGET | START 15:50:42Z / END 15:54:53Z / WORKED=251s valid pair | W3 implementation/data processing | NONE |

## Current conclusion
- LEGACY_EXPLORATORY_LOWER_BOUND: 20m.
- SERVER_CLOCK_SAFE_LOWER_BOUND: unresolved.
- SERVER_CLOCK_FAILURE_BOUNDARY: unresolved.
- Credible server-clock duration failures: 0.
- Current case: SC-A22-CLOCK-01.
- R3/R4/R6/R7 are valid-marker UNDER_TARGET outcomes and do not move either strict boundary.
- R7 satisfied the requirement to switch away from repeated protocol-document audit: it implemented a deterministic runtime evidence processor, regression corpus/tests, raw-pair integrity verification, and boundary aggregation. The useful implementation completed naturally at 251s, so it was closed rather than padded.
- R5 is an independently established NON_DURATION_FAIL; missing clock evidence is secondary and has no boundary effect.
- Raw GitHub REST pairs for R3/R4/R6 were re-fetched during R7 and exactly matched persisted timestamps/WORKED.
- The remaining Phase-A bottleneck is workload-source scale: next repeat requires a genuinely useful executable/data-processing task that naturally sustains >=1320s. Completed processor work must not be repeated as padding.
- Direct active_work_sec/productive_ratio remain unknown.
- Current-protocol pre-END close sample count remains 0; legacy 32s is supporting only; configured 60s reserve remains provisional.
- OPERATING_CAP, PRODUCTIVE_CAP, SOFT_CUTOFF, HARD_CAP, CLOSE_RESERVE, SAFETY_MARGIN remain not promoted.

R7 raw close: `runtime-boundary/PROBE-22M-SERVERCLOCK-20260924-R7/close.json`.
Implementation assets: `runtime/RUNTIME_EVIDENCE_PROCESSOR_*`, `runtime/RUNTIME_RAW_PAIR_AUDIT_R7.md`.

This table is derived; raw marker REST resources, per-probe evidence, event ledger, and fresh current state govern strict classification.
