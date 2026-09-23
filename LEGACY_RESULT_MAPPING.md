# Legacy Runtime Result Mapping

Purpose: normalize historical labels for analysis without rewriting historical raw evidence.

Canonical current terminal result vocabulary is defined in `TIMING_EVENT_SCHEMA.md`.

## Safe mappings

- `CLEAN_PASS_PENDING_WAKE_OK` -> `CLEAN_PASS_PENDING_WAKE`
- `PASS_PENDING_WAKE_OK` -> `CLEAN_PASS_PENDING_WAKE` when raw evidence also shows target reached + clean close + verified prearm
- `CLEAN_PASS_WAKE_OK` -> `CLEAN_PASS_WAKE_OK` but interpret legacy WAKE_OK as continuation-observed; wake timeliness remains separate/unresolved unless directly evidenced
- `UNDER_TARGET_INSUFFICIENT_WORK` -> `UNDER_TARGET`
- `NON_DURATION_FAILURE` -> `NON_DURATION_FAIL`

## Do not auto-map

- `INCOMPLETE_CLOSE_NOT_STRICT_PASS`: inspect raw evidence. Missing close alone does not prove UNDER_TARGET or DURATION_FAIL_CANDIDATE.
- generic `FAIL` / `FAILED`: attribution required.
- start/checkpoint-only `ACTIVE` records: inspect whether the target was reached and whether independent failure evidence exists; otherwise AMBIGUOUS or UNDER_TARGET only when justified.
- any simulated/logic-test result: never enter empirical counters.

## Rule

Normalization is a derived analytical view only. Historical raw files and `state/events.log` retain their original labels. Boundary movement must be traceable to raw evidence plus the normalization rationale; never silently rewrite historical meaning.
