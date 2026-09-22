# Maximum Safe Runtime + Reproducible Handoff Policy Research

## Research question
What is the maximum empirically safe substantive-work duration for one ChatGPT Automation RRULE relay invocation, and what handoff/admission policy most reliably reproduces near that optimum over many turns?

This is one integrated research problem. Wake scheduling is pre-armed at turn start; planned gap is now an experimental variable:
1. characterize the runtime failure boundary,
2. choose a safe operating cap,
3. derive a repeatable policy that uses as much of that cap as practical.

## Current operating context
- Previous operating floor: about 10 minutes of work before handoff.
- Wake rule: immediately after TURN_START, pre-arm NEXT_WAKE = START_TS + target_runtime + planned_gap. Use planned_gap=3m as the initial baseline because prior relay research found +3m best among tested end-of-turn leads. Do not wait until turn end to schedule the next wake.
- A simplistic 10m work / 3m gap cycle has idealized duty cycle 76.9% before jitter/failures.
- Longer turns improve theoretical duty cycle, but a failed final checkpoint/rearm can make expected availability worse.

## Phase A — boundary search
1. Test-generated workload is valid substantive experimental work when it is deliberately used to exercise runtime behavior and the workload profile is recorded. Idle waiting/sleeping only to consume time remains excluded.
2. Record actual start, useful work, close time.
3. Coarse ascent from prior 10m baseline in about +2m classes.
4. Clean PASS requires a successful same-automation RRULE pre-arm at TURN_START + active target workload + durable close checkpoint. The pre-arm return must contain the intended DTSTART/RRULE/enabled state; no scheduler mutation is performed at normal turn end.
5. Next invocation provides retrospective WAKE_OK evidence.
6. Separate duration-related failures from unrelated tool/network/provider failures.
7. First credible duration-related failure brackets the upper boundary.
8. Refine the bracket at ~1m resolution.
9. If no boundary is observed, report only a lower bound and keep ascending.
10. Apply `RUNTIME_BOUNDARY_DECISION_RULE.md` for evidence classification, failure bracketing, refinement, and cap promotion. A single coarse PASS may advance the next probe but never promotes a production cap.

## Phase B — operating-cap validation
The production cap is not max_observed_success.

Promote a candidate only after repeated evidence, initially at least 5 clean runs at the candidate class, with a meaningful margin below the first credible failure boundary.

Track variance. If close overhead or runtime behavior is noisy, increase safety margin.

## Phase C — policy generalization
Once the boundary/cap is stable enough, experimentally compare control policies.

### P1 Fixed threshold
Continue normal work while elapsed < cutoff. Once cutoff is crossed, stop starting new work and hand off.

### P2 Soft cutoff + hard cap
Before soft cutoff, start normal bounded work. After soft cutoff, admit only short bounded units. At hard cap, start nothing new and close.

### P3 Estimated-next-task admission
Before starting each next unit, estimate its duration.

Continue only if:
`elapsed + estimated_next_task + close_overhead + safety_margin < hard_cap`

Otherwise hand off.

### P4 Adaptive admission
Use P3 but derive close_overhead and safety_margin from recent observed runs rather than fixed constants.

## Policy comparison metrics
- long-run useful_work / wall-clock time
- clean-close rate
- successful next-wake rate
- overshoot beyond intended cap
- lost/incomplete finalization
- unnecessary early handoff
- control/measurement overhead
- estimate error for next-task duration
- robustness across different task-size distributions

## Promotion rule for final policy
Prefer the simplest policy whose observed long-run utilization and continuation reliability are statistically/practically indistinguishable from more complex alternatives.

Do not promote complexity for theoretical elegance alone.

## Final output schema
The final reusable operating contract must include:
- observed safe lower bound
- first credible failure boundary or unresolved status
- promoted operating cap
- soft cutoff
- hard cap
- close-overhead estimate
- safety margin
- next-task admission rule
- required evidence count / confidence
- rollback rule when failure rate rises

## Permitted supporting development
Small changes are allowed only when directly improving:
- timing measurement,
- close-overhead measurement,
- timeout-vs-non-timeout classification,
- task-duration estimation,
- continuation reliability,
- reproducibility of the final policy.

Avoid unrelated orchestration expansion.


## Cross-profile generalization
Runtime safety must be tested across heterogeneous real workload shapes defined in `RUNTIME_WORKLOAD_PROFILES.md`.

A single profile may advance an exploratory lower bound, but a final universal operating cap requires replication across representative workload profiles near the candidate boundary. If a realistic profile has materially worse close behavior or a lower failure boundary, the final policy must account for it rather than averaging the risk away.


## Test-load interpretation
For this study, deliberately generated reasoning/I-O/checkpoint workload is part of the experiment, not padding, when it is bounded, measured, and assigned a workload profile. Older wording that broadly rejects artificial/generated load should be interpreted narrowly as rejecting idle/no-op time consumption, not rejecting purposeful stress workload.


## Phase D — pre-armed gap optimization
After the runtime boundary/operating cap is sufficiently characterized, hold runtime policy approximately fixed and test planned wake gaps.

Definition:
- planned_gap = NEXT_WAKE - (START_TS + target_runtime)
- actual_idle_gap = NEXT_INVOCATION_START - CURRENT_INVOCATION_CLOSE

The planned gap is not the actual idle gap because close overhead and runtime overshoot consume part of it.

Initial sequence:
- baseline planned_gap=3m
- then 2m
- then 1m if continuation remains stable
- consider intermediate or larger values when evidence warrants

Measure:
- prearm_scheduler_write_ok/state_ok
- actual_elapsed_sec
- close_overhead_sec
- actual_idle_gap_sec
- wake jitter
- overlap/concurrent invocation
- missed wake
- incomplete close/checkpoint
- long-run useful-work duty cycle

Promotion rule:
Choose the smallest planned gap that repeatedly preserves clean close + stable next wake without overlap/concurrency or materially higher failure risk. Do not minimize gap independently of runtime safety.
