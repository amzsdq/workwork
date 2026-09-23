# Runtime Classification Test Vectors

Purpose: logic-only regression cases for the runtime boundary classifier. These are not empirical runtime evidence and cannot move SAFE_LOWER_BOUND or FAILURE_BOUNDARY.

| Case | Observation | Terminal result | Separate annotation | Boundary effect |
|---|---|---|---|---|
| V1 | target reached by valid server marker pair, prearm verified, durable clean close, next wake not yet observed | CLEAN_PASS_PENDING_WAKE | wake_observed=false | none until retrospective wake |
| V2 | V1 plus next actual invocation confirms the prearmed continuation | CLEAN_PASS_WAKE_OK | wake_observed=true; wake timeliness separate | SAFE_LOWER_BOUND may advance to target |
| V3 | valid marker pair proves WORKED below target; substantive work ended cleanly | UNDER_TARGET | execution cause required | none |
| V4 | invocation disappears and evidence cannot distinguish voluntary fragmentation from runtime cut-off | AMBIGUOUS | attribution unresolved | none; investigate/repeat |
| V5 | near/after target execution is cut off before durable close, valid prearm, no independent cause | DURATION_FAIL_CANDIDATE | failure profile fixed for refinement | create/confirm upper-bound candidate |
| V6 | GitHub/network/provider error explicitly prevents close independently of elapsed runtime | NON_DURATION_FAIL | independent cause recorded | none |
| V7 | prearm scheduler write/state verification fails before substantive workload | NON_DURATION_FAIL | scheduler-layer cause | none |
| V8 | target reached and close succeeds but intended continuation is not retrospectively established | CLEAN_PASS_PENDING_WAKE | wake_layer_anomaly=true | no strict lower-bound advance |
| V9 | marker-valid target reached/close succeeds but useful-work density is sparse | CLEAN_PASS_PENDING_WAKE | productive_evidence=WEAK | survival evidence only; no operating/productive cap |
| V10 | high useful-work density reaches target but final durable close is lost near boundary without independent cause | DURATION_FAIL_CANDIDATE | completion_envelope_failure=true | bracket/refine profile-controlled |
| V11 | marker-valid close succeeds after target with measurable strict-WORKED overshoot | CLEAN_PASS_PENDING_WAKE | overshoot sample recorded | survival pending wake; informs envelope |
| V12 | simulated policy case predicts success/failure | SIMULATION_ONLY | logic test only | never changes empirical boundary |
| V13 | START or END marker missing, raw server created_at unavailable, or marker pair invalid | CLOCK_EVIDENCE_INVALID | exact WORKED unavailable regardless of model/local time claims | none; retry after clock evidence is valid |

## Invariants
1. Model/local time never repairs V13; only a valid GitHub server marker pair can establish strict WORKED.
2. Missing close alone is not automatically a duration failure when the invocation may have fragmented early.
3. Explicit independent non-duration cause dominates duration attribution.
4. Strict coarse advancement requires marker-valid clean close plus retrospective continuation observation.
5. Wake observation and wake timeliness are separate annotations.
6. Survival and productive-evidence quality are separate axes.
7. Completion-envelope failure near the boundary is duration-relevant when independent causes are absent.
8. Simulation/logic cases never alter empirical counters.
