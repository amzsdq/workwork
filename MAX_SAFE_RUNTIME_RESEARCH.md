# Maximum Safe Runtime + Reproducible Handoff Policy Research

## Research question
What is the maximum empirically safe substantive-work duration for one automation invocation, and what handoff/admission policy reliably reproduces near that optimum over many turns?

## Final clock invariant
All strict measurements use raw GitHub issue #1 marker resources. `WORKED = END_MARKER.created_at - START_MARKER.created_at`. Model/local time strings never classify duration. Human reports show raw UTC plus KST, but KST is display-only.

## Harness V2 workload invariant
Finite backlog exhaustion is not a valid normal-close trigger. Use `runtime/RUNTIME_STRESS_WORKLOAD_GENERATOR.py` to process unique decision-relevant units continuously while timing/admission permits. Persist batch checkpoints, reject duplicate IDs, and never sleep/idle/no-op to consume time.

## Authoritative intervals
- PREARM_OVERHEAD = WORK_START - START
- PRODUCTIVE_WINDOW = PRE_CLOSE - WORK_START
- CLOSE_OVERHEAD = END - PRE_CLOSE
- WORKED = END - START

All endpoints are raw GitHub `created_at` values. Productive-marker ordering failure invalidates that derived interval but must not fabricate a duration or crash the main START/END classification.

## Phase A — boundary search
1. Resolve fresh case/probe identity.
2. Create START_MARKER and raw-fetch it.
3. Prearm the same recurring automation for START + target + planned gap; baseline gap +3m. Verify scheduler state.
4. Create/raw-fetch WORK_START immediately before substantive work.
5. Continuously process unique useful batches. Use raw PROGRESS markers for authoritative in-flight control elapsed when admission/close decisions require it.
6. Stop admitting new work only when authoritative timing/admission enters close reserve or on genuine blocking/failure/user stop.
7. Create/raw-fetch PRE_CLOSE, persist durable close checkpoint/finalization, then create/raw-fetch END.
8. Compute all strict intervals only from raw server timestamps.
9. Persist immutable terminal evidence and immutable per-probe event before mutable projection reconciliation.
10. Clean PASS requires marker-valid WORKED>=target, sustained substantive work, durable close, scheduler WRITE_OK/STATE_OK, and no duration-attributable forced stop. It remains PENDING_WAKE until retrospective continuation.
11. First credible duration failure is profile-specific and requires controlled refinement before a hard boundary.

Current strict fact: R9 proved SERVER_CLOCK_SAFE_LOWER_BOUND=22m after retrospective WAKE_OK. Current coarse target is 24m; failure boundary remains unresolved.

## Terminal synchronization
Raw markers -> immutable `runtime-boundary/<PROBE>/terminal.json` -> immutable `state/events/<PROBE>.json` are empirical truth. Shared `state/current.json`, `state/events.log`, and `EVIDENCE_TABLE.md` are mutable projections reconciled with fresh-SHA CAS. Projection conflicts are bookkeeping NON_DURATION_FAIL and do not erase valid terminal truth.

## Phase B — operating-cap validation
Production cap is not max observed success. Require initially >=5 clean marker-valid runs at/near candidate, representative workload profiles, current-protocol completion-envelope samples, continuation evidence where measurable, and explicit safety margin below credible failure region.

## Phase C — policy generalization
Compare P1 fixed threshold, P2 soft cutoff + hard cap, P3 estimated-next-task admission, P4 adaptive admission. Candidate admission rule: `estimated_next_task_sec + close_reserve_sec <= remaining_budget_sec`. Prefer the simplest policy practically equivalent on useful utilization and clean-close preservation.

## Phase D — planned-gap optimization
Only after runtime/cap stabilization, test +3m toward +2m/+1m. `planned_gap = PREARM_NEXT - (START_MARKER.created_at + target_runtime)`. Quantitative wake-gap claims require trustworthy server-side endpoints.

## Final output
SERVER_CLOCK_SAFE_LOWER_BOUND, FAILURE_BOUNDARY or unresolved, OPERATING_CAP, PRODUCTIVE_CAP, SOFT_CUTOFF, HARD_CAP, current-protocol CLOSE_OVERHEAD, SAFETY_MARGIN, NEXT_TASK_ADMISSION, validation confidence/count, workload coverage, rollback, selected planned gap.
