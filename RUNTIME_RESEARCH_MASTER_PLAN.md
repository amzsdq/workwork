# Runtime Research Master Plan

Status: CANONICAL EXECUTION ROADMAP
Repo: amzsdq/workwork

## Objective
Empirically find maximum safe substantive-work duration and simplest reproducible handoff/admission policy near it with high long-run useful utilization.

Evidence authority: raw GitHub marker REST resources -> immutable per-probe terminal/event evidence -> mutable projections (`state/current.json`, `state/events.log`, `EVIDENCE_TABLE.md`).

## Final clock invariant
`WORKED = END_MARKER.created_at - START_MARKER.created_at` from raw GitHub server timestamps only. Model/local times are non-authoritative. Invalid pair => CLOCK_EVIDENCE_INVALID. Pre-protocol timing is legacy supporting only.

## Three axes
- START -> WORK_START = prearm/setup overhead
- WORK_START -> PRE_CLOSE = productive window
- PRE_CLOSE -> END = close overhead
- START -> END = authoritative WORKED

No sleep/idle/no-op padding. Finite backlog exhaustion is not a normal close trigger before PRE_CLOSE. Harness V2 continuously supplies unique decision-relevant deterministic units.

## Phase A — boundary search
- LEGACY_EXPLORATORY_LOWER_BOUND = 20m
- SERVER_CLOCK_SAFE_LOWER_BOUND = **22m**
- FAILURE_BOUNDARY = unresolved
- active target = **24m**
- planned gap = +3m
- active profile = ROTATED_STRICT_PROFILE

Historical server-clock under-target R3/R4/R6/R7 and provider-failed R5 exposed the finite-workload harness defect. They do not define a duration failure boundary.

### R9 authoritative 22m result
`PROBE-22M-SERVERCLOCK-20260924-R9`:
- CLEAN_PASS_WAKE_OK
- START 2026-09-23T17:47:04Z
- WORK_START 2026-09-23T17:47:12Z
- PRE_CLOSE 2026-09-23T18:08:09Z
- END 2026-09-23T18:09:06Z
- WORKED 1322s
- productive window 1257s
- close overhead 57s
- >=2048 unique units / >=8 batches / duplicate 0
- durable close and scheduler WRITE_OK/STATE_OK

Therefore SERVER_CLOCK_SAFE_LOWER_BOUND=22m. One success does not promote the production operating cap.

### Current 24m probe
`SC-A24-CLOCK+` is the active study case. Run Harness V2 with a rotated profile. A clean marker-valid WORKED>=1440s + durable close becomes CLEAN_PASS_PENDING_WAKE; only retrospective wake may advance the lower bound to 24m. A credible duration-attributable failure becomes a profile-specific candidate requiring controlled refinement.

## Phase B — cap validation
At least 5 clean marker-valid runs near candidate with representative W3/W5/(W4 or W6)/W7 coverage, current-protocol close samples, and explicit safety margin. Longest one-off success is never automatically the operating cap.

## Phase C — admission/handoff policy
Compare P1-P4; simplest practically equivalent wins. Candidate rule remains `estimated_next_task_sec + close_reserve_sec <= remaining_budget_sec`. Controlled overlap remains KEEP/TEST/NOT_PROMOTED and deferred until runtime boundary/cap validation.

## Phase D — gap optimization
After cap stabilization: +3m -> +2m -> +1m.

## Phase E — parallel research
Deferred/supporting-only until Phase A/B gate.

## Current execution pointer
CURRENT_CASE_ID = SC-A24-CLOCK+
ACTIVE_TARGET = 24m
LATEST_TERMINAL_PROBE = PROBE-22M-SERVERCLOCK-20260924-R9
LATEST_TERMINAL_RESULT = CLEAN_PASS_WAKE_OK
LATEST_WORKED = 1322s
SERVER_CLOCK_SAFE_LOWER_BOUND = 22m
FAILURE_BOUNDARY = unresolved

## Completion gate
Final outputs: server-clock lower/failure bounds, operating/productive caps, soft cutoff/hard cap, current-protocol close overhead, safety margin, next-task admission rule, validation confidence/count, workload coverage, rollback rule, selected gap.
