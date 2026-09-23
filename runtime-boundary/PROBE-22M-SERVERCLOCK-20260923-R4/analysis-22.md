# R4 evidence quality hierarchy audit

## Strong evidence

- raw GitHub issue-comment START/END created_at for WORKED,
- scheduler update returned state for pre-arm correctness,
- durable raw close evidence,
- server-side commit/comment existence for corroborating work/state transitions.

## Medium/supporting evidence

- legacy pre-clock clean-run observations,
- historical wake lateness samples,
- durable qualitative analyses of workload shape and failure causality.

## Weak/non-authoritative evidence

- model-authored clock strings,
- inferred elapsed time without marker pair,
- a missing close file by itself,
- derived summary rows that disagree with raw evidence.

## Rule

Boundary movement must be based on strong evidence only. Medium evidence can choose the next experiment or explain causality. Weak evidence cannot promote or lower the boundary.

## R4 status implication

Until END_MARKER exists, R4 is ACTIVE and cannot be called a 22m pass regardless of how many substantive outputs have been produced.
