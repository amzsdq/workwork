# R8 Large Genuine Workload Corpus

Probe: PROBE-22M-SERVERCLOCK-20260924-R8
Case: SC-A22-CLOCK-01
Profile: W3_MIXED_IO

Purpose: avoid repeating exhausted protocol audits. This probe extended the runtime evidence processor into a reusable end-to-end implementation/migration corpus.

## Completed decision-bearing units
1. Canonical normalized Probe schema expanded with case/profile, immutable marker IDs, productive evidence and retrospective-wake fields.
2. Validation/anomaly rules hardened for missing marker identity, productive-ratio misuse and active-work overflow.
3. Existing event-ledger/current-state/evidence-table authority ordering rechecked against the implementation.
4. Duplicate reconciliation added: exact duplicate idempotent; conflicting duplicate rejected; no field-wise merge.
5. Marker raw-fetch trust boundary specified: IDs, body role/probe identity, raw server created_at and monotonicity.
6. Boundary aggregation rule kept conservative: only CLEAN_PASS_WAKE_OK eligible for coarse lower-bound movement; failure candidate not auto-confirmed.
7. Completion-envelope extraction reconciled with two-endpoint close semantics; no fabricated current-protocol close sample.
8. Admission evidence remains separate from strict clock and is not prematurely promoted.
9. Migration path specified without rewriting historical raw evidence.
10. Regression corpus upgraded to schema v2, adds marker IDs, R7 and a missing-marker-ID edge case; tests expanded T01-T26.
11. Concurrency-safe terminal synchronization specified using optimistic SHA re-read/reconcile rather than overwrite.
12. Canonical consistency audit completed; six material implementation/control gaps were repaired or explicitly gated.

## Artifacts changed/added
- `runtime/RUNTIME_EVIDENCE_PROCESSOR_REFERENCE.py`
- `runtime/RUNTIME_EVIDENCE_PROCESSOR_PIPELINE.md`
- `runtime/RUNTIME_EVIDENCE_PROCESSOR_DATASET.json`
- `runtime/RUNTIME_EVIDENCE_PROCESSOR_SPEC.md`
- `runtime/RUNTIME_EVIDENCE_PROCESSOR_TESTS.md`
- `runtime/RUNTIME_EVIDENCE_PROCESSOR_ACCEPTANCE.md`
- `runtime/R8_SCHEMA_CONSISTENCY_AUDIT.md`
- `runtime-boundary/PROBE-22M-SERVERCLOCK-20260924-R8/start.json`

## Pre-END close checkpoint
All planned nonredundant units are complete. Further work on the same processor in this invocation would primarily repeat already settled rules rather than add decision value. Per non-padding invariant, close now and let raw GitHub END marker determine whether this run reached 1320s.

Clock START comment id: 5799384221
Clock START server created_at: 2026-09-23T17:15:25Z
