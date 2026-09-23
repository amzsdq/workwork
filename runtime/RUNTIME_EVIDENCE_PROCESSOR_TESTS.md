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
| T11 | provider/network failure independently established, markers may be absent | NON_DURATION_FAIL; no boundary effect |
| T12 | WORKED>=target but no durable close and no forced-stop attribution | AMBIGUOUS |
| T13 | model elapsed claims 1400 but markers prove 1000 | WORKED=1000; UNDER_TARGET |
| T14 | local/model timestamp present but END marker missing, no independent cause | CLOCK_EVIDENCE_INVALID |
| T15 | zero substantive units at/over target | AMBIGUOUS/weak survival only |
| T16 | forced_stop=true and clean_close=true at/over target | DURATION_FAIL_CANDIDATE + inconsistency anomaly |
| T17 | provider failure=true plus malformed/reversed markers | NON_DURATION_FAIL + clock anomaly |
| T18 | timestamp pair exists but START marker ID missing | CLOCK_EVIDENCE_INVALID + MARKER_ID_PAIR_INCOMPLETE |
| T19 | productive_ratio set but direct active_work_sec null | classification preserved + PRODUCTIVE_RATIO_WITHOUT_DIRECT_ACTIVE_WORK anomaly |
| T20 | active_work_sec > WORKED | classification preserved + ACTIVE_WORK_EXCEEDS_WORKED anomaly |
| T21 | exact duplicate normalized probe records | idempotently collapse to one |
| T22 | conflicting duplicate normalized probe records | reject with CONFLICTING_DUPLICATE_PROBE; never merge fields |
| T23 | R7 raw pair 15:50:42Z -> 15:54:53Z | WORKED=251, UNDER_TARGET |
| T24 | CLEAN_PASS_PENDING_WAKE with wake_observed=false | remains pending, no bound effect |
| T25 | CLEAN_PASS_PENDING_WAKE with wake_observed=true | CLEAN_PASS_WAKE_OK, promotion eligible |
| T26 | DURATION_FAIL_CANDIDATE in pure aggregation | candidate count increments, confirmed failure boundary remains null |

## Current corpus reconciliation
- R3 = 652s UNDER_TARGET.
- R4 = 736s UNDER_TARGET.
- R6 = 975s UNDER_TARGET.
- R7 = 251s UNDER_TARGET.
- R5 = NON_DURATION_FAIL because provider block is independently established; missing clock evidence is secondary.
- All marker-valid completed probes remain UNDER_TARGET for target=1320s.
- No current server-clock record establishes SAFE_LOWER_BOUND or FAILURE_BOUNDARY.

## Integrity acceptance
Raw-fetch adapter must additionally verify returned marker IDs and marker bodies match the requested probe/role. The pure classifier consumes only normalized records after that trust-boundary check.

## Design finding
The processor does not infer a hard failure from a missing close alone. Duration attribution requires observed forced-stop/timeout or equivalent near-boundary evidence without an independent cause. Explicit independent non-duration cause has causal precedence. Conflicting duplicate evidence fails closed instead of being merged into a stronger-looking synthetic record.
