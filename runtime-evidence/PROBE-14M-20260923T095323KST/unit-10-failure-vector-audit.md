# Unit 10 — Failure-vector audit

Probe: PROBE-14M-20260923T095323KST

Boundary effects remain mutually exclusive:
- CLEAN_PASS => may raise exploratory lower bound.
- DURATION_FAIL => may create/narrow failure-boundary candidate.
- NON_DURATION_FAIL => no boundary movement.
- UNDER_TARGET => no boundary movement.
- ambiguous close loss => repeat before narrowing unless later evidence establishes cause.
- scheduler-state mismatch at start => control failure, not runtime safety evidence.
- missing retrospective wake with otherwise clean close => continuation/gap evidence issue; do not silently convert to duration failure.

No classification ambiguity requiring protocol repair was found.
