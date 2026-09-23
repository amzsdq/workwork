# W2 write/checkpoint-heavy batch 01

Purpose: exercise repeated durable-write preparation and checkpoint integrity under the strict 18-minute runtime class.

## Generated verification units
1. Reconcile strict state: safe lower bound 16m; boundary unresolved; next target 18m.
2. Verify scheduler contract: same automation, recurring RRULE, exact schedule, enabled.
3. Verify pre-arm arithmetic: 18m target + 3m gap = 21m from invocation start.
4. Verify close reserve: final 60s reserved for durable close rather than new task admission.
5. Classify scheduler write as control-plane evidence, not substantive workload.
6. Classify this batch as TEST_GENERATED substantive experimental work.
7. Preserve parallel probe as deferred; do not promote survival evidence.
8. Maintain duration-failure isolation from GitHub/provider errors.
9. Require clean close checkpoint before candidate PASS.
10. Require next invocation retrospective WAKE_OK before strict promotion.
11. Record actual elapsed independently of target runtime.
12. Record overshoot as max(actual-target,0).
13. Record close overhead separately when observable.
14. Record idle gap only when observable rather than infer it.
15. Keep failure boundary null absent credible duration-related termination.
16. Do not mutate scheduler at normal close.
17. On clean 18m + WAKE_OK, advance safe lower bound to 18m.
18. After promotion, next coarse target is 20m.
19. A 20m credible duration failure would bracket boundary in (18m,20m].
20. Boundary refinement should then move to approximately 1m resolution.

Batch result: internal invariants consistent; no duration failure observed at this checkpoint.