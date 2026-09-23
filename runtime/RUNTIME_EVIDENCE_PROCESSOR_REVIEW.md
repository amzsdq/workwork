# Runtime Evidence Processor — Review Findings

## Reconciled empirical records
The normalized processor corpus independently recomputes:
- R3: 652s, UNDER_TARGET
- R4: 736s, UNDER_TARGET
- R6: 975s, UNDER_TARGET
- R5: independent provider failure with unavailable clock pair; boundary effect NONE

No server-clock empirical record currently advances a strict lower bound or establishes a failure boundary.

## Implementation defects found and repaired during R7
1. **Causal precedence bug** in the first classifier draft: missing markers were classified CLOCK_EVIDENCE_INVALID before checking an independently established non-duration failure. Canonical R5 semantics require the independent provider cause to remain NON_DURATION_FAIL, with clock invalidity as a secondary annotation. The reference implementation now checks `non_duration_failure` first.
2. **Forced-stop precedence bug**: inconsistent input could contain both `clean_close=true` and `forced_stop_or_timeout=true`, causing a clean pass if clean-close checks ran first. Forced stop now takes precedence and emits an inconsistency anomaly when both are present.
3. **Recorded WORKED mismatch**: processor recomputes WORKED and emits an anomaly rather than trusting recorded elapsed values.

## Remaining implementation gap
The reference module is intentionally pure and does not yet fetch raw marker REST resources itself. Production-grade processing should resolve comment IDs to raw GitHub resources and compare fetched server `created_at` against persisted copies before classification. Until that exists, persisted marker timestamps are regression inputs, not a replacement for the canonical raw REST evidence hierarchy.

## Research value
This implementation is directly useful beyond the 22m probe: it reduces future manual classification drift, makes legacy contamination explicit, and provides a deterministic base for Phase B cap validation and Phase C policy replay. It does not itself count as empirical boundary evidence.
