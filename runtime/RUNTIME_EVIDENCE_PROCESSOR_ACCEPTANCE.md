# Runtime Evidence Processor — Acceptance and Promotion Gates

Status: implementation candidate; deterministic audit layer only, never empirical authority by itself.

## A. Clock integrity
Raw marker resolver validates immutable comment ID, START/END role, probe ID, case ID, protocol, raw GitHub server `created_at`, and monotonic pair. Cached repository timestamps are comparison copies only.

## B. Classification determinism
Recomputed WORKED always overrides cached/model/local elapsed values. Fixed normalized input produces identical result, anomalies and boundary effect.

## C. Causal precedence
Independent provider/network/GitHub/scheduler failure cannot create a duration boundary. Forced-stop/timeout at/after target without independent cause outranks contradictory clean-close flags and becomes DURATION_FAIL_CANDIDATE.

## D. Duplicate safety
Identical duplicate records are idempotent. Conflicting duplicates fail closed. Field-wise merging is prohibited because it can fabricate a complete marker pair, clean close, or scheduler verification from incompatible records.

## E. Boundary safety
Only CLEAN_PASS_WAKE_OK can make a target eligible for coarse server-clock safe-lower-bound advancement. A failure candidate is not a confirmed failure boundary until profile-controlled reproduction/bracketing. Legacy, synthetic, UNDER_TARGET, NON_DURATION_FAIL, CLOCK_EVIDENCE_INVALID and AMBIGUOUS records cannot move strict bounds.

## F. Productive evidence
`productive_ratio` is accepted only with defensible direct `active_work_sec`. Goal-directed wall-clock windows remain separately named. Zero substantive units cannot satisfy productive clean PASS.

## G. Completion envelope
Pre-END close reserve samples require compatible trustworthy endpoints. Post-END synchronization is control overhead, not WORKED. Legacy close samples cannot increase current-protocol reserve sample N.

## H. Terminal synchronization
Raw terminal evidence -> events.log -> current.json -> EVIDENCE_TABLE.md is a logical transaction implemented with optimistic concurrency. SHA conflict => fresh read + reconcile, never blind overwrite. Promotion is blocked until re-read shows all four surfaces agree.

## I. Regression corpus
Processor must reproduce:
- R3 = 652 UNDER_TARGET
- R4 = 736 UNDER_TARGET
- R5 = NON_DURATION_FAIL, clock-invalid secondary
- R6 = 975 UNDER_TARGET
- R7 = 251 UNDER_TARGET

Before R8 terminal evidence the expected derived strict state remains:
- SERVER_CLOCK_SAFE_LOWER_BOUND = unresolved
- SERVER_CLOCK_FAILURE_BOUNDARY = unresolved
- duration failure candidates = 0

Synthetic edge tests include exact-target pass, duration-fail candidate, reversed timestamps, recorded-WORKED mismatch, zero-substantive-work, provider failure, missing marker identity, productive-ratio misuse, active-work overflow, exact/conflicting duplicates, pending-wake behavior and non-promotion of failure candidates.

## J. Current implementation status
- Pure classifier: implemented and hardened with marker identity and productive-evidence anomalies.
- Duplicate reconciliation: implemented conservatively.
- Regression dataset: schema v2 with marker IDs and R7.
- Test matrix: expanded to T01-T26.
- Raw-pair algorithm/trust boundary: specified.
- Raw-pair manual verification: completed previously for R3/R4/R6; R7 is represented in the corpus.
- End-to-end pipeline and concurrency-safe terminal sync: specified in `runtime/RUNTIME_EVIDENCE_PROCESSOR_PIPELINE.md`.
- Automated connector/REST fetch integration inside repository code: intentionally not present; connector execution is external to the pure module.
- Scheduler mutation: intentionally absent.

## K. Promotion gate
The processor may be the preferred deterministic audit layer once the above checks pass, but raw GitHub marker resources remain empirical Source of Truth. The processor cannot autonomously promote production OPERATING_CAP; Phase-B repeated marker-valid evidence and workload-profile coverage remain mandatory.
