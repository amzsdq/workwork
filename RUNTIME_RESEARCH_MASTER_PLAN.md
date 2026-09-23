# Runtime Research Master Plan

Status: CANONICAL EXECUTION ROADMAP
Repo: amzsdq/workwork

## Objective
Empirically find maximum safe substantive-work duration and simplest reproducible handoff/admission policy near it with high long-run useful utilization.

Evidence authority: raw GitHub START/END marker REST resources -> raw per-probe evidence -> event ledger -> current state -> derived summaries.

## Final clock invariant
`WORKED = END_MARKER.created_at - START_MARKER.created_at` from raw GitHub server timestamps only. Model/local times are non-authoritative. Invalid pair => CLOCK_EVIDENCE_INVALID. Pre-protocol timing is legacy supporting only.

## Three axes
SURVIVAL_BOUNDARY, PRODUCTIVE_WINDOW, COMPLETION_ENVELOPE.

Strict probes use server markers:
- START -> WORK_START = prearm/setup overhead
- WORK_START -> PRE_CLOSE = productive window
- PRE_CLOSE -> END = close overhead
- START -> END = authoritative WORKED

No sleeping/idle/no-op padding. However, exhaustion of a hand-written backlog is NOT a normal close condition before the timing/admission policy enters PRE_CLOSE. Use the scalable deterministic workload source in `runtime/RUNTIME_STRESS_WORKLOAD_GENERATOR.py` and `runtime/SCALABLE_STRICT_PROBE_WORKLOAD_PROTOCOL.md` to continue generating unique, decision-relevant units until the close policy says to stop.

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
- R5: NON_DURATION_FAIL with clock-invalid secondary annotation; START marker provider-blocked.
- R6: 975s UNDER_TARGET, valid pair, 59 useful units, repository/control audit corpus exhausted.
- R7: **251s UNDER_TARGET**, valid pair, 47 substantive implementation/data-processing units. R7 deliberately changed workload class away from repeated document audit and delivered a reusable deterministic runtime evidence processor, regression dataset/tests, raw-pair integrity design/audit, boundary aggregation, anomaly policy, and Phase-B bridge. Two classifier precedence defects were found and repaired. The implementation completed naturally before 1320s and was not padded.

The prior R3/R4/R6/R7/R8 UNDER_TARGET sequence exposed a harness defect: hand-written workloads were allowed to terminate the probe. That measured backlog exhaustion rather than the runtime boundary.

FIXED POLICY:
- workload exhaustion before PRE_CLOSE is no longer a normal terminal condition;
- when a batch finishes, request the next unique deterministic batch;
- duplicate case IDs do not count;
- normal close is driven by the timing/admission policy, not by finite-corpus exhaustion;
- immutable per-probe terminal/event records are canonical; shared projections use conflict-safe reconciliation.

After strict 22m clean PASS + retrospective WAKE_OK, continue +2m coarse ascent with rotated profiles. First credible duration failure creates profile-specific F; refine ~1m.

## Phase B
At least 5 clean marker-valid runs near candidate with representative W3/W5/(W4 or W6)/W7 coverage and explicit safety margin. Current-protocol close samples are required; legacy 32s sample is supporting only. The R7 evidence processor is the preferred deterministic audit layer for future validation, but its outputs never replace raw marker evidence.

## Phase C
Compare P1-P4; simplest practically equivalent wins. Controlled overlap remains KEEP/TEST/NOT_PROMOTED and deferred. Future exact handoff timing requires authoritative server-side endpoints. Canonical future owner record is root `handoff-state.json`.

## Phase D
Gap optimization +3m -> +2m -> +1m after cap stabilizes.

## Phase E
Parallel probe remains deferred/supporting-only until Phase A/B gate.

## Study case SC-A22-CLOCK-01
PASS: valid marker pair, WORKED>=1320s, sustained substantive W3 work, durable close checkpoint, scheduler WRITE_OK/STATE_OK, no duration-attributable forced stop. Then CLEAN_PASS_PENDING_WAKE; retrospective wake advances lower bound.

UNDER_TARGET: valid pair, WORKED<1320s, boundary unchanged. Under the fixed harness, voluntary UNDER_TARGET due only to finite-workload exhaustion is a HARNESS_DEFECT and must not recur; load the next unique generator batch instead. UNDER_TARGET remains valid for genuine user stop, independent blocking condition, or intentional safety close.
CLOCK_EVIDENCE_INVALID/NON_DURATION_FAIL: no boundary effect.
DURATION_FAIL_CANDIDATE: profile-controlled refinement.

## Current execution pointer
CURRENT_CASE_ID = SC-A22-CLOCK-01
ACTIVE_PROBE_ID = none
LATEST_TERMINAL_PROBE = PROBE-22M-SERVERCLOCK-20260924-R7
LATEST_TERMINAL_RESULT = UNDER_TARGET
LATEST_WORKED = 251s

Immediate objective after user resumes automation: run the next 22m strict probe with the scalable deterministic workload loop. Do not voluntarily close because a batch finished. Continue unique decision-relevant units until PRE_CLOSE is triggered by the timing/admission policy. Use START/WORK_START/PRE_CLOSE/END raw GitHub server markers and conflict-safe terminal synchronization.

## Completion gate
Final outputs remain server-clock lower/failure bounds, operating/productive caps, cutoff/hard cap, current-protocol close overhead, safety margin, next-task admission, validation confidence/count, workload coverage, rollback, selected gap.
