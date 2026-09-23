# Runtime Research Master Plan

Status: CANONICAL EXECUTION ROADMAP
Repo: amzsdq/workwork

## 1. Research objective

Answer two questions with empirical evidence:

1. What is the maximum empirically safe substantive-work duration for one automation invocation?
2. What is the simplest reproducible handoff/admission policy that operates near that limit with high long-run useful-work utilization without materially increasing forced-stop/run-out risk?

This document is the execution map. Detailed protocols remain in:
- `MAX_SAFE_RUNTIME_RESEARCH.md`
- `RUNTIME_BOUNDARY_DECISION_RULE.md`
- `RUNTIME_WORKLOAD_PROFILES.md`
- `RUNTIME_STRESS_WORKLOAD_MATRIX.md`
- `PROBE_EXECUTION_PLAN.md`

Evidence authority remains:
1. raw per-probe evidence,
2. `state/events.log`,
3. `state/current.json` as the mutable current pointer,
4. derived summaries such as `EVIDENCE_TABLE.md`.

A derived summary must never override raw/canonical evidence.

## 2. Anti-drift rule

Every invocation must answer exactly three questions before doing work:

1. What study case is active?
2. What observation will make that case terminal?
3. What exact next case follows each possible terminal result?

Do not repeat a target merely because `next_strict_target_minutes` is unchanged.

If an earlier probe for the active study case has START/checkpoint evidence but no terminal close classification, first classify that incomplete probe from durable evidence as one of:
- CLEAN_PASS_PENDING_WAKE
- UNDER_TARGET
- DURATION_FAIL_CANDIDATE
- NON_DURATION_FAIL
- AMBIGUOUS

Only then decide whether a repeat is justified.

A new probe must add decision value. Start-only repetition is not decision value.

### Terminal-classification write invariant

Whenever a study case reaches a terminal classification or a retrospective WAKE_OK changes its boundary effect, update the following as one logical transaction before advancing the case:

1. raw per-probe terminal evidence,
2. `state/events.log`,
3. `state/current.json`,
4. `EVIDENCE_TABLE.md` as the derived audit view.

After the writes, re-read all three shared-state views and verify that they agree on:
- latest terminal probe/result,
- SAFE_LOWER_BOUND,
- FAILURE_BOUNDARY,
- current/next target,
- current_case_id / next_case_id.

If any of these disagree, the case is not considered fully closed and the next study case must not start until reconciliation is complete.

A tool/provider failure that prevents this synchronization is NON_DURATION_FAIL and must not alter the runtime boundary.

## 2A. Three-axis runtime objective

A runtime target is not useful merely because the invocation survives until that timestamp. Every empirical probe must characterize three distinct axes:

### A. SURVIVAL_BOUNDARY
How long the invocation can remain active without a duration-attributable forced stop or timeout.

### B. PRODUCTIVE_WINDOW
How much of the invocation is spent on genuine goal-directed work.

Measure at minimum:
- actual_elapsed_sec
- active_work_sec when directly supportable
- productive_ratio only when active_work_sec is directly supportable
- goal_directed_window_sec / goal_directed_ratio when necessary tool I/O cannot be separated
- substantive_unit_count
- workload_profile

Do not manufacture work to inflate active time. The workload must contribute to the runtime research goal or directly validate its control/evidence logic.

### C. COMPLETION_ENVELOPE
How late useful work can continue while still preserving enough time for a reliable durable close.

Measure:
- last_normal_task_admit_ts when observable
- pre_close_ts
- close_end_ts
- close_overhead_sec
- overshoot_sec
- clean_close
- checkpoint_saved

The purpose is to identify:
- HARD_CAP = the empirically safe outer wall-clock limit,
- SOFT_CUTOFF = the latest region where normal work should still be admitted,
- CLOSE_RESERVE = realistic close overhead plus safety margin,
- PRODUCTIVE_CAP = the useful-work operating window before close reserve begins.

A probe that reaches the duration target with very low productive work is survival evidence but weak operating-policy evidence.
A probe with high productive work but no clean close is not an acceptable operating point.

During Phase A, collect all three axes on the same probes whenever possible so later Phase B/C does not need to repeat avoidable experiments.

## 3. Phase gates

### Phase A — runtime boundary search

Current state:
- SAFE_LOWER_BOUND = 16m
- FAILURE_BOUNDARY = unresolved
- active target = 18m
- planned_gap = +3m
- current profile = W2 WRITE_CHECKPOINT_HEAVY

Coarse ascent:
- 18m: W2 WRITE_CHECKPOINT_HEAVY
- 20m: W6 LARGE_UNIT
- then +2m while clean, rotating profiles per workload protocol.

Exit from coarse ascent:
- first credible duration-related failure creates a boundary candidate F,
- last lower clean class is L,
- move to refinement.

Refinement:
- test approximately 1m classes inside [L,F],
- keep the failure-producing workload profile fixed during the first refinement sequence so duration is not confounded with workload shape,
- if the lower clean anchor L was established under a different profile, obtain a same-profile lower-anchor run when needed before claiming a profile-specific bracket,
- continue until the same-profile bracket is about 1m or finer,
- ambiguous failure at F must be repeated once before narrowing.

Interpretation of a failure discovered while profiles are rotating:
- initially treat it as a failure for that target/profile pair, not automatically a universal duration boundary,
- refine with the same profile to determine whether duration is the driver,
- cross-profile replication near the candidate cap determines whether the final cap can be universal.

Boundary-search stop condition:
- either a credible refined failure boundary exists for at least one realistic profile and its implication for the operating cap is characterized,
- or no boundary is found and the program reports only a safe lower bound while continuing ascent.

### Phase B — operating-cap validation

Do not equate max observed success with the operating cap.

Choose a candidate cap below the credible failure boundary using:
- observed close overhead,
- elapsed/overshoot variance,
- safety margin,
- worst credible representative workload profile.

Promotion gate:
- at least 5 clean runs at/near the candidate,
- no unresolved duration failure at or below candidate,
- scheduler WRITE_OK/STATE_OK,
- durable close checkpoint,
- retrospective WAKE_OK where observable,
- representative profile coverage.

Minimum profile coverage near candidate:
- W3 MIXED_IO
- W5 MICRO_UNIT_CHAIN
- at least one of W4 REASONING_HEAVY or W6 LARGE_UNIT
- W7 CLOSE_HEAVY for close-reserve characterization

### Phase C — handoff/admission policy comparison

Compare in increasing complexity:
- P1 FIXED_THRESHOLD
- P2 SOFT_CUTOFF_PLUS_HARD_CAP
- P3 ESTIMATED_NEXT_TASK_ADMISSION
- P4 ADAPTIVE_ADMISSION

First use replay/simulation over observed task-duration and close-overhead samples. Then live-test only policies that plausibly improve the objective.

Promotion rule:
prefer the simplest policy whose observed utilization and continuation reliability are practically indistinguishable from more complex alternatives.

Required outputs:
- SOFT_CUTOFF
- HARD_CAP
- CLOSE_OVERHEAD
- SAFETY_MARGIN
- NEXT_TASK_ADMISSION rule
- rollback rule

### Phase D — planned-gap optimization

Only after runtime cap/policy are stable enough.

Hold runtime policy approximately fixed and test:
- +3m baseline
- +2m
- +1m if stable
- intermediate/larger gap only when evidence warrants

Choose the smallest planned gap that preserves clean close + stable next wake without materially higher overlap/miss/failure risk.

### Phase E — deferred cooperative parallel research

Only after Phase A boundary characterization and Phase B operating-cap validation are sufficiently complete.

Resume `PARALLEL-A14-B4-02` as supporting/cooperative-utilization research.
Parallel survival evidence must never be promoted into strict runtime PASS evidence.

## 4. Study-case queue

### SC-A18-01 — close the 18m decision
Purpose:
Produce one terminal empirical classification for the 18m W2 class.

Before starting a new 18m probe:
- inspect all existing 18m probe evidence,
- classify any incomplete prior 18m probe,
- do not create another start-only probe if the previous one can already be classified.

PASS:
- target reached,
- substantive W2 workload sustained through the probe rather than a short setup burst,
- active_work_sec and productive_ratio recorded when directly observable; otherwise use explicitly labeled goal-directed window metrics,
- durable close checkpoint,
- scheduler WRITE_OK/STATE_OK,
- no duration-related forced stop,
- completion-envelope timestamps recorded when practical.

Interpretation:
- A clean 18m pass advances SURVIVAL_BOUNDARY evidence after retrospective WAKE_OK.
- Its productive/goal-directed evidence and close-overhead evidence feed PRODUCTIVE_WINDOW / COMPLETION_ENVELOPE characterization.
- Do not treat a low-work survival pass as sufficient evidence for the final operating cap.

Then:
- SAFE_LOWER_BOUND -> 18m after retrospective WAKE_OK,
- NEXT_CASE -> SC-A20-01.

NON_DURATION_FAIL:
- boundary unchanged,
- repeat 18m only after recording the independent cause.

UNDER_TARGET:
- boundary unchanged,
- diagnose why the invocation ended before target,
- repeat only after correcting the execution cause.

DURATION_FAIL_CANDIDATE:
- if credible for W2, candidate interval is [16m,18m] but the 16m anchor was W4,
- NEXT_CASE -> refinement around 17m using W2; obtain a same-profile lower anchor if needed before calling the bracket profile-specific.

### SC-A20-01 — 20m coarse ascent
Profile: W6 LARGE_UNIT.
Entry condition: SC-A18-01 strict clean PASS + WAKE_OK.
Terminal handling follows the same decision rule, with same-profile refinement if a credible failure appears.

### SC-A22+ — generated coarse ascent
Entry condition: prior coarse target strict clean PASS + WAKE_OK.
Target: prior target +2m.
Rotate workload profile.
Continue until first credible duration failure, then refine while controlling profile.

### SC-AR-* — 1m refinement
Generated after first credible duration failure.
Maintain a profile-controlled [L,F] bracket.
Each terminal result must shrink or confirm the bracket rather than mix workload-profile changes into the duration inference.

### SC-B-CAP-* — candidate-cap validation
Run at least 5 clean validations, deliberately covering representative workload profiles.
Do not advance to Phase C until the promotion gate is satisfied.

### SC-C-POLICY-* — policy comparison
Replay first, live test second.
Stop increasing complexity when a simpler policy is practically equivalent.

### SC-D-GAP-* — planned-gap optimization
3m -> 2m -> 1m subject to continuation stability.

### SC-E-PARALLEL-01
Resume deferred `PARALLEL-A14-B4-02` only after Phase A/B gate.

## 5. Per-case record

Every study case should record:

- case_id
- phase
- hypothesis/question
- target_runtime_min
- workload_profile
- controlled variables
- probe_id(s)
- required evidence
- terminal classification
- boundary/cap effect
- next_case_id
- anomaly/non-duration cause
- decision timestamp
- active_work_sec / productive_ratio when directly supportable
- goal_directed_window_sec / goal_directed_ratio when used instead
- substantive_unit_count
- last_normal_task_admit_ts when observable
- pre_close_ts
- close_end_ts
- close_overhead_sec

## 6. Current execution pointer

CURRENT_CASE_ID = SC-A18-01

Immediate objective:
Close the 18m W2 class with a terminal classification. The next useful action is not another generic 18m start; it is to obtain a sustained useful-work 18m W2 run with a valid close/terminal result.

## 7. Final program completion gate

The program is complete only when it can report:

- SAFE_LOWER_BOUND
- FAILURE_BOUNDARY or unresolved
- OPERATING_CAP
- PRODUCTIVE_CAP
- SOFT_CUTOFF
- HARD_CAP
- CLOSE_OVERHEAD
- SAFETY_MARGIN
- NEXT_TASK_ADMISSION rule
- validation confidence/count
- workload-profile coverage
- rollback rule
- selected planned gap

and each value is traceable to durable evidence.
