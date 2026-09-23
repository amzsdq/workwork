# Runtime Evidence Processor — Acceptance Criteria

The processor is ready to support Phase B/C only when all are true:

1. Raw marker resolver validates comment ID, marker kind, probe ID, case ID, protocol, and server `created_at`.
2. Recomputed WORKED always overrides cached/recorded elapsed values.
3. Independent non-duration causes cannot accidentally create a duration boundary.
4. Forced-stop evidence cannot accidentally be promoted to clean pass due to inconsistent clean-close flags.
5. Missing/invalid raw marker pair cannot be repaired by model/local timestamps.
6. Legacy evidence remains supporting-only.
7. Retrospective wake existence is separate from wake timeliness.
8. Processor emits anomalies instead of silently rewriting raw evidence.
9. Processor never mutates scheduler or empirical raw records.
10. Current regression corpus reproduces R3=652 UNDER_TARGET, R4=736 UNDER_TARGET, R5=NON_DURATION_FAIL with clock-invalid annotation, R6=975 UNDER_TARGET.
11. Synthetic edge tests cover exact target clean pass, duration-fail candidate, reversed timestamps, recorded-WORKED mismatch, zero-substantive-work case, and provider failure.
12. Boundary summary is derived only after per-probe classification and never promotes from simulation-only records.

## Current status after R7 implementation work
- Pure classifier: implemented.
- Regression dataset: implemented.
- Test matrix: specified.
- Raw-pair algorithm: designed.
- Raw-pair manual verification: completed for R3/R4/R6 with exact matches.
- Automated connector/REST fetch integration: not implemented in repository code; connector execution remains external to the pure reference module.
- Scheduler mutation: intentionally absent.

This is a genuine implementation/data-processing component and can be extended without repeating protocol-document audit work.
