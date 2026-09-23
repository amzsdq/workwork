# R4 W3 decision analysis

Probe: PROBE-22M-SERVERCLOCK-20260923-R4
Case: SC-A22-CLOCK-01

This is substantive W3 MIXED_IO work for the runtime study, not padding.

## Findings

1. The R3 under-target result is causally clean: a valid GitHub marker pair measured 652s, the invocation closed voluntarily, and no duration-attributable failure occurred. It must remain boundary-neutral.
2. The canonical master plan had a stale execution pointer that still named R3 active despite state/current.json, state/events.log, and EVIDENCE_TABLE.md agreeing that R3 was terminal UNDER_TARGET. R4 repaired that pointer.
3. The server-clock migration creates an intentional evidence reset for strict promotion: legacy 20m remains useful exploratory/supporting evidence, but SERVER_CLOCK_SAFE_LOWER_BOUND remains null until a new marker-valid pass receives retrospective WAKE_OK.
4. A valid 22m R4 clean close will initially be CLEAN_PASS_PENDING_WAKE, not an immediate lower-bound promotion. This avoids conflating survival/close success with continuation success.
5. The current +3m planned gap is held constant during Phase A, which is methodologically correct because changing both runtime target and wake lead would confound boundary inference.
6. The overlap handoff candidate must remain deferred. Its 15/11-13 timing matrix is a Phase C utilization question, not Phase A survival evidence.
7. The observed historical wake lateness values (+4s, +21s, +168s) justify measuring wake behavior separately from WORKED. Wake jitter cannot retroactively alter GitHub marker-derived duration.
8. Completion-envelope metrics are currently weaker than WORKED because close timestamps are not independently server-authoritative. Therefore no CLOSE_RESERVE promotion is justified from the single 32s historical sample.
9. The candidate admission rule `estimated_next_task_sec + close_reserve_sec <= remaining_budget_sec` is analytically sensible but remains unpromoted until Phase C decision-quality evidence exists.
10. R4 uses sparse durable checkpoints to avoid reproducing R3's instrumentation/workload-exhaustion defect. Checkpoints are emitted for state transitions or material findings rather than each micro-unit.

## Phase-A implications

- If R4 WORKED >=1320s, closes cleanly, and has no independent failure: CLEAN_PASS_PENDING_WAKE.
- If R4 ends below 1320s without an independent failure: UNDER_TARGET again; do not infer a boundary.
- If R4 is forcibly terminated before a durable END marker, missing END alone is not automatically a duration failure; causal evidence must be inspected under the decision rule.
- If an independent provider/GitHub/scheduler failure occurs: NON_DURATION_FAIL.
- Only a credible duration-related failure may create the first upper-bound candidate.

## Methodological correction retained

The active pointer is now R4. R3 is terminal history. Future invocations must classify/continue R4 from durable evidence before starting any R5 duplicate.
