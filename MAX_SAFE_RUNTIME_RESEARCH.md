# Maximum Safe Runtime Research

## Question
How long should one ChatGPT Automation RRULE relay invocation keep doing substantive work before voluntarily handing off, so that long-run useful-work utilization is maximized without materially increasing run-out/forced-termination risk?

## Current operating context
- Previous operating floor: about 10 minutes of work before handoff.
- Current promoted relay lead-time baseline: about +3 minutes.
- Therefore a simplistic 10m work / 3m gap cycle has an idealized duty cycle of 76.9%, before jitter and failures.
- Extending work time increases idealized duty cycle:
  - 12m / (12m+3m) = 80.0%
  - 15m / (15m+3m) = 83.3%
  - 18m / (18m+3m) = 85.7%
  - 20m / (20m+3m) = 87.0%
But if the longer turn misses its final checkpoint or rearm because the runtime ceiling is crossed, expected utilization can get worse. The research must therefore optimize expected availability, not raw turn length.

## Experimental method
1. Use only substantive work relevant to this runtime/utilization research or directly supporting relay instrumentation/reliability. No sleeping or fake work.
2. Record actual start and actual close times.
3. Coarse ascent from the prior 10m baseline using approximately +2m target classes.
4. A clean PASS requires:
   - substantive work completed,
   - durable checkpoint/event saved,
   - final same-automation recurring RRULE update returned success,
   - returned state contains intended DTSTART, RRULE:FREQ=HOURLY, and enabled=true.
5. On the next actual invocation, retroactively classify the prior run's WAKE_OK.
6. A suspected runtime-limit failure must be separated from unrelated network/GitHub/tool/provider failures.
7. First credible failure establishes an upper-bound candidate; refine with ~1m classes between last clean and first failed.
8. Candidate production cap needs repeated clean evidence, initially 5 clean runs at that class.
9. Keep explicit safety margin below the first credible failure boundary. If evidence suggests high variance, increase the margin.
10. Compare expected duty cycle using observed run success and wake behavior, not only T/(T+3).

## Promotion rule
Do not promote a maximum-safe operating cap until both are true:
- a meaningful upper boundary or saturation region has been probed, and
- the proposed cap has repeated clean closes with preserved continuation.

If no credible upper boundary has been found, report only a lower bound: e.g. `SAFE_AT_LEAST_16M_UNDER_TEST_CONDITIONS`.

## Permitted supporting development
Small changes are allowed when they directly improve this experiment's measurement quality, continuation safety, or ability to distinguish timeout failures from unrelated failures. Avoid unrelated feature work or orchestration expansion.
