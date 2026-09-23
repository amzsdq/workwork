# Runtime Research Master Plan

Status: CANONICAL EXECUTION ROADMAP
Repo: amzsdq/workwork

## Objective
Empirically find maximum safe substantive-work duration and simplest reproducible handoff/admission policy near it with high long-run useful utilization.

Evidence authority: raw GitHub START/END marker REST resources -> raw per-probe evidence -> event ledger -> current state -> derived summaries.

## Final clock invariant
`WORKED = END_MARKER.created_at - START_MARKER.created_at` from raw GitHub server timestamps only. Model/local times are non-authoritative. Invalid pair => CLOCK_EVIDENCE_INVALID. Pre-protocol timing is legacy supporting only.

## Three axes
SURVIVAL_BOUNDARY, PRODUCTIVE_WINDOW, COMPLETION_ENVELOPE. No padding; every repeat needs a genuinely useful workload corpus large enough for target.

## Phase A — boundary search
- LEGACY_EXPLORATORY_LOWER_BOUND = 20m
- SERVER_CLOCK_SAFE_LOWER_BOUND = unresolved
- FAILURE_BOUNDARY = unresolved
- active target = 22m
- planned gap = +3m
- profile = W3 MIXED_IO

Server-clock attempts:
- R3: 652s UNDER_TARGET, useful queue exhausted.
- R4: 736s UNDER_TARGET, larger protocol-analysis work saturated.
- R5: CLOCK_EVIDENCE_INVALID / NON_DURATION_FAIL, START marker provider-blocked.
- R6: **975s UNDER_TARGET**, valid START/END pair, 59 decision-relevant W3 units, clean durable close, verified prearm, no duration failure. R6 materially expanded the corpus and repaired clock semantics, completion-envelope semantics, classification coverage, handoff control path, legacy contamination, rollback/policy schemas, and reproducibility. Repository-protocol/control-document audit work then naturally saturated before 1320s.

R6 proves the prior workload-source defect was reduced but not eliminated. Another repository-protocol audit repeat would now be redundant churn and is forbidden. The next 22m repeat requires a genuinely larger **implementation/data-processing task source** directly relevant to runtime/control research that can naturally sustain >=1320s.

After strict 22m clean PASS + retrospective WAKE_OK, continue +2m coarse ascent with rotated profiles. First credible duration failure creates profile-specific F; refine ~1m.

## Phase B
At least 5 clean marker-valid runs near candidate with representative W3/W5/(W4 or W6)/W7 coverage and explicit safety margin. Current-protocol close samples are required; legacy 32s sample is supporting only.

## Phase C
Compare P1-P4; simplest practically equivalent wins. Controlled overlap remains KEEP/TEST/NOT_PROMOTED and deferred. Future exact handoff timing requires authoritative server-side endpoints. Canonical future owner record is root `handoff-state.json`.

## Phase D
Gap optimization +3m -> +2m -> +1m after cap stabilizes.

## Phase E
Parallel probe remains deferred/supporting-only until Phase A/B gate.

## Study case SC-A22-CLOCK-01
PASS: valid marker pair, WORKED>=1320s, sustained substantive W3 work, durable close checkpoint, scheduler WRITE_OK/STATE_OK, no duration-attributable forced stop. Then CLEAN_PASS_PENDING_WAKE; retrospective wake advances lower bound.

UNDER_TARGET: valid pair, WORKED<1320s, boundary unchanged; repeat only after correcting workload cause.
CLOCK_EVIDENCE_INVALID/NON_DURATION_FAIL: no boundary effect.
DURATION_FAIL_CANDIDATE: profile-controlled refinement.

## Current execution pointer
CURRENT_CASE_ID = SC-A22-CLOCK-01
ACTIVE_PROBE_ID = none
LATEST_TERMINAL_PROBE = PROBE-22M-SERVERCLOCK-20260924-R6
LATEST_TERMINAL_RESULT = UNDER_TARGET
LATEST_WORKED = 975s

Immediate objective: source/construct a genuinely larger implementation or data-processing W3 task directly useful to runtime/control research before another 22m strict probe. Do not repeat protocol-document audit work merely to consume time.

## Completion gate
Final outputs remain server-clock lower/failure bounds, operating/productive caps, cutoff/hard cap, current-protocol close overhead, safety margin, next-task admission, validation confidence/count, workload coverage, rollback, selected gap.
