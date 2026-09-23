# Runtime Classification Test Vectors

Purpose: logic-only regression cases for the runtime boundary classifier. These are not empirical runtime evidence and cannot move SAFE_LOWER_BOUND or FAILURE_BOUNDARY.

| Case | Observation | Terminal result | Separate annotation | Boundary effect |
|---|---|---|---|---|
| V1 | target reached, prearm verified, durable clean close, next wake not yet observed | CLEAN_PASS_PENDING_WAKE | wake_observed=false | none until retrospective wake |
| V2 | V1 plus next actual invocation confirms the prearmed continuation | CLEAN_PASS_WAKE_OK | wake_observed=true; wake timeliness measured separately | SAFE_LOWER_BOUND may advance to target; next coarse case may start |
| V3 | substantive work ends before target with clean close | UNDER_TARGET | execution cause required | none |
| V4 | invocation disappears before target and no evidence distinguishes voluntary fragmentation from runtime cut-off | AMBIGUOUS | attribution unresolved | none; investigate/repeat |
| V5 | near/after target execution is cut off before durable close, prearm was valid, no independent tool/provider cause | DURATION_FAIL_CANDIDATE | failure profile fixed for refinement | create/confirm upper boundary candidate |
| V6 | GitHub/network/provider error explicitly prevents close, independent of elapsed runtime | NON_DURATION_FAIL | independent cause recorded | none; retry same class after cause handling |
| V7 | prearm scheduler write/state verification fails before substantive workload | NON_DURATION_FAIL | scheduler-layer cause | none; do not interpret as runtime boundary |
| V8 | target reached and close succeeds, but the intended continuation is not retrospectively established | CLEAN_PASS_PENDING_WAKE | wake_layer_anomaly=true | do not advance strict SAFE_LOWER_BOUND; diagnose wake layer |
| V9 | clean close exists but useful-work density is sparse | CLEAN_PASS_PENDING_WAKE | productive_evidence=WEAK | survival evidence only; cannot justify operating/productive cap |
| V10 | high useful-work density reaches target but final durable close is lost near boundary without independent cause | DURATION_FAIL_CANDIDATE | completion_envelope_failure=true | bracket/refine with profile controlled |
| V11 | close succeeds after target with measurable overshoot | CLEAN_PASS_PENDING_WAKE | overshoot sample recorded | survival pending wake; overshoot informs completion envelope |
| V12 | a simulated policy case predicts success/failure | SIMULATION_ONLY | logic test only | never changes empirical boundary |

## Invariants

1. Missing close by itself is not automatically a duration failure when the invocation may have voluntarily fragmented early.
2. An explicit independent non-duration cause dominates duration attribution.
3. Strict coarse advancement requires both clean close and retrospective continuation observation under the current protocol.
4. Wake observation and wake timeliness are separate annotations.
5. Survival result and productive-evidence quality are separate axes; do not invent compound terminal enums for productivity.
6. Completion-envelope failure near the boundary is duration-relevant even if useful work before the close was dense.
7. Simulation and synthetic classifier cases never alter empirical counters.
