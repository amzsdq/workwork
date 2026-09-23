# Runtime Evidence Processor — Test Matrix

These are deterministic implementation tests, not empirical runtime evidence.

| ID | Input | Expected |
|---|---|---|
| T01 | R3 markers 13:32:22Z -> 13:43:14Z, target 1320 | WORKED=652, UNDER_TARGET |
| T02 | R4 markers 13:58:33Z -> 14:10:49Z, target 1320 | WORKED=736, UNDER_TARGET |
| T03 | missing START/END, no independent cause | CLOCK_EVIDENCE_INVALID |
| T04 | R6 markers 15:23:53Z -> 15:40:08Z | WORKED=975, UNDER_TARGET |
| T05 | recorded_worked differs from recomputed | recomputed wins; anomaly emitted |
| T06 | END before START | CLOCK_EVIDENCE_INVALID |
| T07 | non-GITHUB_SERVER_MARKER_V1 | LEGACY_SUPPORTING |
| T08 | marker-valid WORKED=1320, clean close, scheduler verified, substantive units >0 | CLEAN_PASS_PENDING_WAKE |
| T09 | T08 + retrospective wake | CLEAN_PASS_WAKE_OK; lower-bound promotion eligible |
| T10 | WORKED>=target, forced stop, no independent cause | DURATION_FAIL_CANDIDATE |
| T11 | provider/network failure independently established, markers may be absent | NON_DURATION_FAIL; clock validity may be secondary; no boundary effect |
| T12 | WORKED>=target but no durable close and no forced-stop attribution | AMBIGUOUS |
| T13 | model elapsed claims 1400 but markers prove 1000 | WORKED=1000; UNDER_TARGET |
| T14 | local/model timestamp present but END marker missing, no independent cause | CLOCK_EVIDENCE_INVALID |
| T15 | zero substantive units at/over target | not clean productive PASS; AMBIGUOUS/weak survival only |
| T16 | forced_stop=true and clean_close=true at/over target | DURATION_FAIL_CANDIDATE + inconsistency anomaly; never clean pass |
| T17 | provider failure=true plus malformed/reversed markers | NON_DURATION_FAIL + clock anomaly; never duration fail |

## Current corpus reconciliation
- R3 expected 652: reference arithmetic 13:43:14 - 13:32:22 = 10m52s = 652s.
- R4 expected 736: 14:10:49 - 13:58:33 = 12m16s = 736s.
- R6 expected 975: 15:40:08 - 15:23:53 = 16m15s = 975s.
- R5 expected primary result NON_DURATION_FAIL because the provider block is independently established; missing clock evidence remains a secondary annotation.
- All marker-valid completed probes remain UNDER_TARGET for target=1320s.
- No current server-clock record establishes SAFE_LOWER_BOUND or FAILURE_BOUNDARY.

## Design finding
The reference classifier deliberately does not infer a hard failure from a missing close alone. Duration attribution requires an observed forced-stop/timeout or equivalent near-boundary evidence without an independent cause. Explicit independent non-duration cause has causal precedence. This preserves the anti-false-boundary rule.
