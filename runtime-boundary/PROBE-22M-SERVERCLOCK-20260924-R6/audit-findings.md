# R6 W3 Mixed-I/O Audit Findings

Probe: PROBE-22M-SERVERCLOCK-20260924-R6
Case: SC-A22-CLOCK-01

## Decision-relevant findings

1. **Clock protocol vs measurement protocol semantic conflict**
   - `GITHUB_SERVER_CLOCK_PROTOCOL.md` makes issue-comment START/END server `created_at` authoritative for WORKED and places terminal ledger synchronization after END, outside WORKED.
   - `RUNTIME_MEASUREMENT_PROTOCOL.md` still defines `actual_elapsed_sec = close_end_ts - run_start_ts` and operational close endpoint after terminal-sync verification.
   - Resolution required: treat these older elapsed/close-end formulas as secondary completion-envelope instrumentation only; they must not be used as strict WORKED or override the END marker boundary.

2. **Completion-envelope endpoint mismatch**
   - `COMPLETION_ENVELOPE_METHOD.md` says reliable close endpoint is after terminal-sync writes and verification.
   - Final clock protocol ends WORKED before terminal ledger synchronization.
   - This is not necessarily wrong if two endpoints are explicitly named: `measured_work_end=END_MARKER.created_at` and `operational_sync_end` as secondary post-END completion evidence. Current prose risks conflating them.

3. **Legacy close-overhead contamination risk**
   - `COMPLETION_ENVELOPE_EVIDENCE.md` retains a 32s direct close sample from pre-server-clock evidence.
   - It may remain legacy supporting completion-envelope evidence, but must not be presented as if measured under GITHUB_SERVER_MARKER_V1. Current state already calls the 60s reserve provisional; retain that restriction.

4. **Boundary decision rule is clock-consistent**
   - `RUNTIME_BOUNDARY_DECISION_RULE.md` correctly gates strict classification on valid START/END raw server markers and gives CLOCK_EVIDENCE_INVALID no boundary effect.

5. **Classification vectors need a clock-invalid regression case**
   - `RUNTIME_CLASSIFICATION_TEST_VECTORS.md` has V1-V12 but no explicit missing/invalid marker-pair case despite the final clock invariant. Add a logic-only vector for CLOCK_EVIDENCE_INVALID.

6. **R5 is absent from derived evidence table**
   - `state/events.log` records R5 CLOCK_EVIDENCE_INVALID/NON_DURATION_FAIL, while `EVIDENCE_TABLE.md` stops at R4. Derived table should include R5 to preserve terminal-sync visibility, without changing boundary.

7. **Current R6 workload is materially larger than R3/R4 protocol-only work**
   - The corpus spans cross-document semantic reconciliation, classifier regression coverage, legacy contamination, completion-envelope definitions, rollback/policy dependencies, and final state reconciliation. These are direct control/evidence correctness tasks, not padding.

## Required repairs before R6 terminal close

- Clarify authoritative WORKED vs secondary post-END operational-sync endpoint in measurement/completion docs.
- Add CLOCK_EVIDENCE_INVALID regression vector.
- Add R5 to EVIDENCE_TABLE.
- Preserve all pre-server-clock timing as legacy/supporting only.
- Do not promote close reserve/cap from these documentation repairs.
