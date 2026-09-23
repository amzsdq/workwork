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
- worked_sec_recomputed / worked_sec_recorded
- marker_pair_valid_recomputed
- scheduler_write_ok / scheduler_state_ok
- clean_close / checkpoint_saved
- forced_stop_or_timeout / non_duration_failure
- substantive_unit_count / active_work_sec / productive_ratio
- prior_next_wake_observed
- result_recorded / result_recomputed
- boundary_effect_recorded / boundary_effect_recomputed
- anomalies[]

## Marker integrity gate
A normalized strict record is not authoritative merely because it contains two timestamp strings. Before classification, a raw-fetch adapter must verify:
1. START and END immutable comment IDs are both present;
2. both raw GitHub comment resources are fetchable;
3. returned IDs match requested IDs;
4. marker bodies identify START/END roles and the same expected probe_id/case_id;
5. raw server `created_at` values parse and END >= START.

Only after this gate may the normalized raw timestamps be passed to the pure classifier. Persisted/cached timestamps are audit copies, not a replacement for raw marker verification when making a new strict promotion.

## Deterministic rules
1. Missing marker identity or timestamp pair => `CLOCK_EVIDENCE_INVALID`, unless an independently established non-duration cause has causal precedence.
2. Recompute `WORKED` exclusively as END.created_at - START.created_at.
3. Recorded model/local elapsed fields never repair or override server-marker WORKED.
4. `WORKED < target` => `UNDER_TARGET`, boundary effect NONE. Clean close is recorded separately; UNDER_TARGET never promotes a bound.
5. `WORKED >= target` + valid pair + sustained substantive evidence + durable close + scheduler verified + no duration-attributable forced stop => `CLEAN_PASS_PENDING_WAKE`.
6. Retrospective continuation can promote pending pass to `CLEAN_PASS_WAKE_OK`; wake lateness is separate from wake existence.
7. Independent provider/network/GitHub/scheduler cause => `NON_DURATION_FAIL`, boundary effect NONE.
8. Near/after-target forced termination or close loss without independent cause => `DURATION_FAIL_CANDIDATE`; require profile-controlled reproduction before hard boundary promotion.
9. Pre-server-clock records are `LEGACY_SUPPORTING` and cannot move current strict server-clock bounds.
10. Simulation/replay records never alter empirical bounds.
11. Conflicting duplicate records for one probe must be rejected, never field-wise merged.
12. `productive_ratio` requires defensible direct `active_work_sec`; goal-directed wall-clock windows remain separately labeled.

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
- R5: NON_DURATION_FAIL with clock-invalid secondary annotation
- R6: 975s UNDER_TARGET
- R7: 251s UNDER_TARGET
- strict server-clock lower bound unresolved
- strict server-clock failure boundary unresolved

## Terminal synchronization
Terminal evidence, `state/events.log`, `state/current.json`, and `EVIDENCE_TABLE.md` are a logical transaction implemented with optimistic concurrency. A SHA conflict requires fresh read + reconciliation; never blind overwrite. Terminal synchronization is complete only after all four surfaces are re-read and agree on probe/result/bounds/case.

## Non-goals
- no scheduler mutation
- no model/local clock inference
- no promotion from legacy elapsed values
- no synthetic runtime evidence generation
- no silent mutation of empirical truth from a derived processor

See `runtime/RUNTIME_EVIDENCE_PROCESSOR_PIPELINE.md` for end-to-end reconciliation and migration rules.
