# R4 sparse-checkpoint strategy evaluation

## R3 defect

R3 generated many decision-relevant units but exhausted its finite protocol-repair queue and voluntarily closed at 652s. The defect was not lack of activity; it was coupling turn termination to queue exhaustion instead of the server-clock target.

## R4 correction

R4 decouples unit completion from turn completion:

- finishing one bounded analysis does not imply close,
- another relevant analysis is admitted while the target class remains unresolved,
- durable checkpoints are sparse and grouped by material findings,
- close is permitted only after target-class evidence or an actual failure/blocking condition.

## Why this is not padding

The additional analyses are directly tied to required final outputs: boundary causality, completion reserve, productive-window measurement, cap-promotion gates, scheduler/clock ordering, and handoff isolation. Each changes or validates a research decision.

## Expected effect

This correction should eliminate the specific R3 early-close mechanism without changing the target, workload profile, planned gap, or clock protocol. Therefore R4 is a valid same-case repeat that adds decision value rather than a duplicate start-only probe.
