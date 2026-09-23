# Runtime Research Master Plan

Status: CANONICAL EXECUTION ROADMAP
Repo: amzsdq/workwork

## Objective
Empirically find maximum safe substantive-work duration and simplest reproducible handoff/admission policy near it with high long-run useful utilization.

Evidence authority: raw GitHub marker REST -> immutable per-probe terminal/event -> mutable projections.

## Final clock invariant
`WORKED = END_MARKER.created_at - START_MARKER.created_at` from raw GitHub server timestamps only. Model/local times are non-authoritative.

## Three axes
START→WORK_START prearm; WORK_START→PRE_CLOSE productive window; PRE_CLOSE→END close overhead; START→END authoritative WORKED.

Harness V2 forbids finite-backlog close and ID-only pseudo-uniqueness. Workload must remain semantically decision-relevant; generator V2 varies causal/numeric conditions across epochs.

## Phase A — boundary search
- LEGACY_EXPLORATORY_LOWER_BOUND = 20m
- SERVER_CLOCK_SURVIVAL_OBSERVATION = **>=22m02s** (R9 clean clock/close)
- STRICT_SUBSTANTIVE_SAFE_LOWER_BOUND = **revalidation pending** after posthoc generator-v1 semantic-repeat audit
- FAILURE_BOUNDARY = unresolved
- active target = **24m**
- planned gap = +3m
- active profile = ROTATED_STRICT_PROFILE

R3/R4/R6/R7/R8 under-target and R5 provider failure do not define a duration failure boundary.

### R9 clock result and posthoc workload audit
R9 raw server markers prove WORKED=1322s, productive window=1257s, close overhead=57s, clean durable close, scheduler OK, and retrospective WAKE_OK. This remains valid survival/completion evidence.

However generator-v1 later proved to have only 720 semantic Cartesian scenarios per cycle while changing IDs across epochs. Thus the recorded >=2048 ID-unique units overstated decision-unique workload. The clock observation is not erased, but strict substantive-work lower-bound promotion based solely on R9 is pending revalidation/supersession.

### Current 24m probe
`SC-A24-CLOCK+` uses semantic generator V2. A clean raw-marker WORKED>=1440s with sustained semantically unique work, durable close, scheduler OK, and retrospective WAKE_OK supersedes the R9 workload-quality concern and can establish a >=24m strict lower bound. Credible duration-attributable failure remains profile-specific pending controlled refinement.

## Phase B — cap validation
Require initially >=5 clean marker-valid runs near candidate, representative profiles, current-protocol completion-envelope samples, explicit safety margin. Longest one-off success never automatically becomes operating cap.

## Phase C — admission/handoff policy
Compare P1-P4. Candidate rule: `estimated_next_task_sec + close_reserve_sec <= remaining_budget_sec`. Controlled overlap remains deferred KEEP/TEST/NOT_PROMOTED.

## Phase D
Gap optimization +3m -> +2m -> +1m after cap stabilization.

## Phase E
Parallel research deferred until Phase A/B gate.

## Current execution pointer
CURRENT_CASE_ID = SC-A24-CLOCK+
ACTIVE_TARGET = 24m
LATEST_TERMINAL_PROBE = PROBE-22M-SERVERCLOCK-20260924-R9
LATEST_TERMINAL_CLOCK_RESULT = CLEAN_PASS_WAKE_OK
LATEST_WORKED = 1322s
STRICT_SUBSTANTIVE_SAFE_LOWER_BOUND = REVALIDATION_PENDING
FAILURE_BOUNDARY = unresolved

## Completion gate
Final outputs: strict server-clock lower/failure bounds, operating/productive caps, soft cutoff/hard cap, close overhead, safety margin, admission rule, validation confidence/count, workload coverage, rollback, selected gap.
