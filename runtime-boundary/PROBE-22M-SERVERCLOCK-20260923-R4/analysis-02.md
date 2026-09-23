# R4 completion-envelope and policy isolation analysis

## Why this work is decision-relevant

The final program must separate survival, productive window, and completion envelope. This analysis checks whether current evidence supports any cap/cutoff promotion while the 22m survival probe remains active.

## Completion-envelope evidence audit

- Historical direct close-overhead sample count in canonical state is 1, value 32s.
- A single sample is insufficient for a production CLOSE_RESERVE.
- R3 server-clock close proves a clean close existed at 652s WORKED, but its close-overhead duration was not independently server-instrumented.
- Therefore `close_reserve_sec=60` remains provisional configuration only, not an empirical promoted constant.
- No evidence currently supports HARD_CAP, SOFT_CUTOFF, PRODUCTIVE_CAP, or OPERATING_CAP promotion.

## Admission-rule audit

Candidate rule:

`estimated_next_task_sec + close_reserve_sec <= remaining_budget_sec`

This is directionally correct because it converts a fixed cutoff into task-size-aware admission, but it cannot yet be selected because:

1. close_reserve is not sufficiently sampled,
2. estimated-next-task error is not yet measured,
3. Phase A has not located a credible failure boundary,
4. Phase B has not produced repeated near-cap clean closes.

The correct current action is to preserve the rule as ANALYTICALLY_SUPPORTED_NOT_PROMOTED and avoid adding adaptive complexity.

## Wake-gap isolation

The +3m planned gap must remain fixed through this boundary search. Historical wake lateness varies materially, including a 168s observation, but wake lateness is a continuation variable, not a substitute for runtime survival. Optimizing the gap now would make a failure harder to attribute.

## R4 interpretation rules retained

- Server marker WORKED is the only strict duration clock.
- Git commit timestamps are useful evidence that goal-directed repository work occurred after START, but they are not substitutes for END_MARKER.
- A clean END at >=1320s gives CLEAN_PASS_PENDING_WAKE.
- Retrospective wake observation is required before strict lower-bound promotion.
- No live overlap/parallel probe is allowed during this run.
