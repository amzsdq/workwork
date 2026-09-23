# Runtime Evidence Processor — Implementation Spec

Purpose: replace repeated manual protocol-audit work with a deterministic data-processing implementation that validates strict runtime evidence and derives boundary state without treating model-authored time as authoritative.

## Inputs
- `state/events.log` JSONL
- `runtime-boundary/*/start.json`
- `runtime-boundary/*/close.json`
- raw GitHub marker comment resources when IDs are present
- `state/current.json` only as a consistency target, never as raw evidence

## Required normalized record
For each probe:
- probe_id, case_id, workload_profile
- target_runtime_sec
- clock_protocol
- start_marker_comment_id / start_marker_created_at
- end_marker_comment_id / end_marker_created_at
- worked_sec_recomputed
- worked_sec_recorded
- marker_pair_valid_recomputed
- scheduler_write_ok / scheduler_state_ok
- clean_close / checkpoint_saved
- forced_stop_or_timeout / non_duration_failure / duration_failure
- substantive_unit_count / active_work_sec / productive_ratio
- result_recorded / result_recomputed
- boundary_effect_recorded / boundary_effect_recomputed
- anomalies[]

## Deterministic rules
1. If either raw server marker timestamp is absent, exact-duration classification is `CLOCK_EVIDENCE_INVALID`.
2. Recompute `WORKED` exclusively as END.created_at - START.created_at.
3. Recorded model/local elapsed fields never repair or override server-marker WORKED.
4. `WORKED < target` with valid pair and clean voluntary close => `UNDER_TARGET`, boundary effect NONE.
5. `WORKED >= target` + valid pair + sustained substantive evidence + durable close + scheduler verified + no duration-attributable forced stop => `CLEAN_PASS_PENDING_WAKE`.
6. Retrospective continuation can promote pending pass to `CLEAN_PASS_WAKE_OK`; wake lateness is separate from wake existence.
7. Independent provider/network/GitHub/scheduler cause => `NON_DURATION_FAIL`, boundary effect NONE.
8. Near/after-target forced termination or close loss without independent cause => `DURATION_FAIL_CANDIDATE`; require profile-controlled reproduction before hard boundary promotion.
9. Pre-server-clock records are `LEGACY_SUPPORTING` and cannot move current strict server-clock bounds.
10. Simulation/replay records never alter empirical bounds.

## Derived outputs
- server_clock_safe_lower_bound
- server_clock_failure_boundary candidate/confirmed
- per-profile clean/fail counts
- marker validity rate
- under-target workload-source diagnostics
- completion-envelope samples
- workload-profile coverage
- consistency diff against `state/current.json` and `EVIDENCE_TABLE.md`

## Validation corpus
Processor must reproduce current canonical facts:
- R3: 652s UNDER_TARGET
- R4: 736s UNDER_TARGET
- R5: CLOCK_EVIDENCE_INVALID/NON_DURATION_FAIL
- R6: 975s UNDER_TARGET
- strict server-clock lower bound unresolved
- strict server-clock failure boundary unresolved

## Non-goals
- no scheduler mutation
- no model/local clock inference
- no promotion from legacy elapsed values
- no synthetic runtime evidence generation

This specification is an implementation/data-processing task source for Phase A and a reusable control component for later cap/policy validation.
