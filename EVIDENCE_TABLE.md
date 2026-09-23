# Runtime Evidence Table

Strict timing authority: `WORKED = END_MARKER.created_at - START_MARKER.created_at` from raw GitHub server timestamps.

Strict workload authority: Harness V2 requires sustained decision-relevant work. Identity uniqueness alone is insufficient; generator-v2 tracks semantic uniqueness.

| Probe | Server WORKED | Result | Workload/harness interpretation | Boundary effect |
|---|---:|---|---|---|
| R3 | 652s | UNDER_TARGET | pre-fixed-harness finite workload exhausted | NONE |
| R4 | 736s | UNDER_TARGET | pre-fixed-harness finite workload exhausted | NONE |
| R5 | n/a | NON_DURATION_FAIL | provider/clock setup failure | NONE |
| R6 | 975s | UNDER_TARGET | pre-fixed-harness finite workload exhausted | NONE |
| R7 | 251s | UNDER_TARGET | pre-fixed-harness finite workload exhausted | NONE |
| R8 | 182s | UNDER_TARGET | pre-fixed-harness finite workload exhausted; event recovered | NONE |
| R9 | 1322s | CLEAN_PASS_WAKE_OK clock/close | server clock valid; productive window 1257s; close 57s. Posthoc audit found generator-v1 repeated the same 720 semantic scenarios while changing IDs, so >=2048 ID-unique must not be read as >=2048 decision-unique | **22m survival observation retained; strict substantive-work lower-bound promotion requires revalidation/supersession** |

## Current strict state
- SERVER_CLOCK_SURVIVAL_OBSERVATION: **>=22m02s** (R9), valid raw clock and clean close.
- STRICT SUBSTANTIVE-WORK SAFE LOWER BOUND: **revalidation pending** after generator-v1 semantic-repeat discovery; a clean semantically-valid 24m+ probe can supersede the concern.
- FAILURE_BOUNDARY: unresolved; credible duration failures: 0.
- R9 START: `2026-09-23T17:47:04Z` (`2026-09-24 02:47:04 KST`).
- R9 WORK_START: `2026-09-23T17:47:12Z` (`2026-09-24 02:47:12 KST`).
- R9 PRE_CLOSE: `2026-09-23T18:08:09Z` (`2026-09-24 03:08:09 KST`).
- R9 END: `2026-09-23T18:09:06Z` (`2026-09-24 03:09:06 KST`).
- R9 WORKED 1322s; PRODUCTIVE_WINDOW 1257s; CLOSE_OVERHEAD 57s; retrospective WAKE_OK observed.
- Current case: `SC-A24-CLOCK+`, target 24m, semantic generator V2.

Posthoc audit: `runtime-boundary/PROBE-22M-SERVERCLOCK-20260924-R9/posthoc-workload-audit.json`. Pending projection reconciliation is recorded separately. Raw markers and immutable per-probe evidence remain authoritative.
