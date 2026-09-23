# Runtime Classification Test Vectors

Purpose: logic-only regression cases for the runtime boundary classifier. These are not empirical runtime evidence and cannot move SAFE_LOWER_BOUND or FAILURE_BOUNDARY.

| Case | Observation | Classification | Boundary effect |
|---|---|---|---|
| V1 | target reached, prearm verified, durable clean close, next wake not yet observed | CLEAN_PASS_PENDING_WAKE | none until retrospective wake |
| V2 | V1 plus next actual invocation confirms the prearmed wake | CLEAN_PASS_WAKE_OK | SAFE_LOWER_BOUND may advance to target; next coarse case may start |
| V3 | substantive work ends before target with clean close | UNDER_TARGET | none |
| V4 | invocation disappears before target and no evidence distinguishes voluntary fragmentation from runtime cut-off | AMBIGUOUS | none; investigate/repeat |
| V5 | near/after target execution is cut off before durable close, prearm was valid, no independent tool/provider cause | DURATION_FAIL_CANDIDATE | create/confirm upper boundary candidate |
| V6 | GitHub/network/provider error explicitly prevents close, independent of elapsed runtime | NON_DURATION_FAIL | none; retry same class after cause handling |
| V7 | prearm scheduler write/state verification fails before substantive workload | NON_DURATION_FAIL | none; do not interpret as runtime boundary |
| V8 | target reached and close succeeds, but later wake is missing or materially invalid | WAKE_LAYER_FAILURE / not strict WAKE_OK | do not advance strict SAFE_LOWER_BOUND; separate wake-layer diagnosis |
| V9 | clean close exists but active-work density is sparse | CLEAN_PASS_PENDING_WAKE for survival axis; WEAK_PRODUCTIVE_EVIDENCE | survival evidence only; cannot justify operating cap/productive cap |
| V10 | high useful-work density reaches target but final durable close is lost near boundary without independent cause | DURATION_FAIL_CANDIDATE | completion-envelope failure; bracket/refine |
| V11 | close succeeds after target with measurable overshoot | CLEAN_PASS_PENDING_WAKE plus overshoot sample | survival pending wake; overshoot informs completion envelope |
| V12 | a simulated policy case predicts success/failure | SIMULATION_ONLY | never changes empirical boundary |

## Invariants

1. Missing close by itself is not automatically a duration failure when the invocation may have voluntarily fragmented early.
2. An explicit independent non-duration cause dominates duration attribution.
3. Strict coarse advancement requires both clean close and retrospective WAKE_OK.
4. Survival success does not imply productive-window or operating-cap success.
5. Completion-envelope failure near the boundary is duration-relevant even if useful work before the close was dense.
6. Simulation and synthetic classifier cases never alter empirical counters.
