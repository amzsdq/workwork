# Runtime Evidence Table

Strict timing authority:
`WORKED = END_MARKER.created_at - START_MARKER.created_at` from raw GitHub server timestamps.

Strict harness authority:
`STRICT_RUNTIME_HARNESS_V2` with scalable unique workload supply. Finite workload exhaustion before PRE_CLOSE is a harness defect, not runtime-boundary evidence.

| Probe | Server WORKED | Result | Harness-v2 interpretation | Boundary effect |
|---|---:|---|---|---|
| R3 | 652s | UNDER_TARGET | HARNESS_UNDER_TARGET: finite workload exhausted | NONE |
| R4 | 736s | UNDER_TARGET | HARNESS_UNDER_TARGET: finite workload exhausted | NONE |
| R5 | n/a | NON_DURATION_FAIL | NON_DURATION_FAIL | NONE |
| R6 | 975s | UNDER_TARGET | HARNESS_UNDER_TARGET: finite workload exhausted | NONE |
| R7 | 251s | UNDER_TARGET | HARNESS_UNDER_TARGET: finite workload exhausted | NONE |
| R8 | 182s | UNDER_TARGET | HARNESS_UNDER_TARGET: finite workload exhausted; terminal event recovered after 409 | NONE |
| R9 | 1322s | CLEAN_PASS_WAKE_OK | VALID STRICT_RUNTIME_HARNESS_V2; productive window 1257s; close overhead 57s; >=2048 unique units; duplicate 0 | SERVER_CLOCK_SAFE_LOWER_BOUND -> 22m |

## Current strict state

- SERVER_CLOCK_SAFE_LOWER_BOUND: **22 minutes** under GITHUB_SERVER_MARKER_V1.
- FAILURE_BOUNDARY: unresolved.
- Credible duration failures under server-clock protocol: 0.
- R9 START: `2026-09-23T17:47:04Z` (`2026-09-24 02:47:04 KST`).
- R9 WORK_START: `2026-09-23T17:47:12Z` (`2026-09-24 02:47:12 KST`).
- R9 PRE_CLOSE: `2026-09-23T18:08:09Z` (`2026-09-24 03:08:09 KST`).
- R9 END: `2026-09-23T18:09:06Z` (`2026-09-24 03:09:06 KST`).
- R9 WORKED: 1322s; PRODUCTIVE_WINDOW: 1257s; CLOSE_OVERHEAD: 57s.
- R9 retrospective next invocation observed: WAKE_OK. Timeliness/jitter remains separate from duration classification.
- Current case: SC-A24-CLOCK+.
- Next strict target: 24 minutes with rotated profile and the same harness/clock invariants.

Mutable projections are derived views. Immutable per-probe terminal/event evidence plus raw marker REST resources remain authoritative.
