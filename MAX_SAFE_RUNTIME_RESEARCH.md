# Maximum Safe Runtime + Reproducible Handoff Policy Research

## Research question
What is the maximum empirically safe substantive-work duration for one ChatGPT Automation RRULE relay invocation, and what handoff/admission policy most reliably reproduces near that optimum over many turns?

This is one integrated research problem:
1. characterize the runtime failure boundary,
2. choose a safe operating cap,
3. derive a repeatable policy that uses as much of that cap as practical.

## Current operating context
- Previous operating floor: about 10 minutes of work before handoff.
- Current promoted relay lead-time baseline: about +3 minutes.
- A simplistic 10m work / 3m gap cycle has idealized duty cycle 76.9% before jitter/failures.
- Longer turns improve theoretical duty cycle, but a failed final checkpoint/rearm can make expected availability worse.

## Phase A — boundary search
1. Use substantive work only; no sleeping/padding.
2. Record actual start, useful work, close time.
3. Coarse ascent from prior 10m baseline in about +2m classes.
4. Clean PASS requires substantive work + durable checkpoint + successful final same-automation RRULE update + correct returned DTSTART/RRULE/enabled state.
5. Next invocation provides retrospective WAKE_OK evidence.
6. Separate duration-related failures from unrelated tool/network/provider failures.
7. First credible duration-related failure brackets the upper boundary.
8. Refine the bracket at ~1m resolution.
9. If no boundary is observed, report only a lower bound and keep ascending.

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
