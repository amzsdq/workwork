# Runtime Evidence Processor — Implementation Spec

Purpose: deterministic validation/classification of strict runtime evidence without treating model-authored time as authoritative.

## Inputs
- immutable `runtime-boundary/<PROBE_ID>/terminal.json`
- immutable `state/events/<PROBE_ID>.json`
- raw GitHub marker comment resources
- mutable `state/current.json`, `state/events.log`, `EVIDENCE_TABLE.md` only as consistency projections

## Required normalized record
Preserve `probe_id`, `case_id`, `workload_profile`, and **`target_runtime_sec`** through every classification path. Dropping target_runtime_sec is a correctness defect because `derive_bounds` cannot infer the proven lower bound from a clean result without it.

Also preserve clock protocol, START/WORK_START/PRE_CLOSE/END marker IDs and raw-created-at audit copies, scheduler state, clean-close/checkpoint state, forced/non-duration failure state, substantive metrics, wake observation, recorded/recomputed result and anomalies.

## Marker integrity gate
Before a new strict promotion, raw-fetch marker resources and verify IDs, marker roles, probe identity, parseable UTC `created_at`, and monotonic ordering. Persisted timestamps are audit copies, not substitutes for raw verification.

## Deterministic rules
1. Missing START/END identity or timestamp pair => `CLOCK_EVIDENCE_INVALID`, unless an independently established non-duration cause has causal precedence.
2. Recompute `WORKED` exclusively as END.created_at - START.created_at.
3. Recorded model/local elapsed fields never repair or override server-marker WORKED.
4. `WORKED < target` => `UNDER_TARGET`, except finite workload exhaustion under Harness V2 => `HARNESS_UNDER_TARGET`; both have boundary effect NONE.
5. `WORKED >= target` + valid pair + sustained substantive evidence + durable close + scheduler verified + no duration-attributable forced stop => `CLEAN_PASS_PENDING_WAKE`.
6. Retrospective continuation can promote pending pass to `CLEAN_PASS_WAKE_OK`; wake lateness is separate from wake existence.
7. Independent provider/network/GitHub/scheduler cause => `NON_DURATION_FAIL`, boundary effect NONE.
8. Near/after-target forced termination or close loss without independent cause => `DURATION_FAIL_CANDIDATE`; require profile-controlled reproduction before hard boundary promotion.
9. Pre-server-clock records are `LEGACY_SUPPORTING` and cannot move current strict server-clock bounds.
10. Simulation/replay records never alter empirical bounds.
11. Conflicting duplicate records for one probe are rejected, never field-wise merged.
12. `productive_ratio` requires defensible direct `active_work_sec`; server-clock WORK_START→PRE_CLOSE is labeled `productive_window_sec`.
13. Productive marker ordering errors must fail closed as productive-metric invalidity; they must not crash classification or fabricate a productive window.

## Current validation facts
- R3/R4/R6/R7 are pre-Harness-V2 under-target server-clock observations and do not prove a failure boundary.
- R9 (`PROBE-22M-SERVERCLOCK-20260924-R9`) is `CLEAN_PASS_WAKE_OK`, WORKED=1322s, and proves `SERVER_CLOCK_SAFE_LOWER_BOUND=22m`.
- failure boundary remains unresolved.
- next strict case is `SC-A24-CLOCK+` unless fresh canonical state says otherwise.

## Terminal synchronization V2
Canonical truth ordering:
1. raw GitHub marker REST resources;
2. immutable probe terminal file;
3. immutable per-probe event file;
4. mutable projections (`state/current.json`, `state/events.log`, `EVIDENCE_TABLE.md`).

Empirical terminal truth is durable after stages 1–3. Projection lag or a 409 does not erase or reclassify it. Shared projections use fresh-SHA optimistic concurrency; on conflict re-fetch/reconcile/retry up to three times, then persist a pending reconciliation record. Never blind overwrite.

## Derived outputs
- server_clock_safe_lower_bound
- server_clock_failure_boundary candidate/confirmed
- per-profile clean/fail counts
- marker validity rate
- harness under-target diagnostics
- completion-envelope samples
- workload-profile coverage
- consistency diff against mutable projections

## Non-goals
- no model/local clock authority
- no promotion from legacy elapsed values
- no silent mutation of empirical truth from a derived processor
