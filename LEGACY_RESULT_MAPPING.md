# Legacy Runtime Result Mapping

Purpose: normalize historical labels without rewriting raw evidence or accidentally promoting pre-server-clock timing into current strict evidence.

Canonical current vocabulary is defined in `TIMING_EVENT_SCHEMA.md`.

## Safe label mappings
- CLEAN_PASS_PENDING_WAKE_OK -> CLEAN_PASS_PENDING_WAKE
- PASS_PENDING_WAKE_OK -> CLEAN_PASS_PENDING_WAKE only when the historical raw record itself supports target/close/prearm under its then-current protocol
- CLEAN_PASS_WAKE_OK -> CLEAN_PASS_WAKE_OK, with legacy WAKE_OK meaning continuation observed; exact wake timeliness unresolved unless independently trustworthy
- UNDER_TARGET_INSUFFICIENT_WORK -> UNDER_TARGET
- NON_DURATION_FAILURE -> NON_DURATION_FAIL

## Final clock boundary
Any run completed before `GITHUB_SERVER_MARKER_V1` activation is `LEGACY_SUPPORTING_EVIDENCE` for new strict promotion, even if its historical label maps cleanly. Historical elapsed/time strings must not be reinterpreted as current authoritative WORKED.

Only a valid new START/END raw GitHub server marker pair can establish strict WORKED for post-activation boundary/cap promotion.

## Do not auto-map
- INCOMPLETE_CLOSE_NOT_STRICT_PASS: inspect raw evidence; missing close alone does not prove UNDER_TARGET or duration failure.
- generic FAIL/FAILED: attribution required.
- start/checkpoint-only ACTIVE: inspect target/close/independent cause; otherwise AMBIGUOUS or justified UNDER_TARGET.
- CLOCK_EVIDENCE_INVALID: remains no-boundary-effect; model/local time cannot repair it.
- simulated/logic-test results: never enter empirical counters.

## Rule
Normalization is derived analysis only. Historical raw files and events retain original labels. Boundary movement must be traceable to authoritative evidence plus explicit normalization rationale.
