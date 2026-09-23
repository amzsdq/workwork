# R4 external-ceiling classification design

## Problem

If the platform imposes a hard invocation ceiling, a run may terminate because of that ceiling. This is duration-related for operational purposes, but evidence must distinguish it from unrelated provider/tool outages.

## Credible external runtime ceiling indicators

- repeated termination at a similar WORKED region across otherwise healthy runs,
- no independent GitHub/network/scheduler failure,
- loss occurs despite bounded substantive workload and valid start evidence,
- profile-controlled repeats reproduce the region,
- close reserve cannot be completed when work is admitted beyond that region.

## Non-ceiling indicators

- isolated connector failure,
- GitHub API outage/rate failure,
- scheduler write failure at start,
- voluntary early close,
- invalid/missing clock evidence caused by an independent service failure.

## Boundary treatment

A reproducible platform invocation ceiling is a credible duration boundary for the operating system even if the internal mechanism is opaque. It should be refined and safety-margined like other duration failures.

## R4

No such ceiling evidence has appeared yet. Failure boundary remains unresolved.
