# R4 scheduler-last-writer risk review

## Context

Historical overlap work exposed a concurrent-control anomaly risk. During strict runtime boundary search, scheduler state must not be contaminated by competing writes.

## R4 controls

- The same automation was pre-armed exactly once after START.
- No normal-close scheduler mutation is permitted.
- Parallel and overlap experiments are deferred.
- The prearmed schedule remains the continuation source unless an external actor changes it.

## Failure interpretation

If a later read shows the scheduler state differs from the verified pre-arm without an R4 write, classify the anomaly as control/provider/external interference first. It is not direct evidence of runtime duration failure.

## Phase C implication

The overlap candidate's single-owner + generation-fencing rule exists specifically to prevent last-writer-wins corruption. That mechanism must be validated separately after the single-invocation boundary is characterized.
