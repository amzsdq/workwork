# Maximum Safe Runtime + Reproducible Handoff Policy Research

## Research question
What is the maximum empirically safe substantive-work duration for one automation invocation, and what handoff/admission policy reliably reproduces near that optimum over many turns?

## Final clock invariant
All new strict runtime measurements use `GITHUB_SERVER_CLOCK_PROTOCOL.md`:
`WORKED = END_MARKER.created_at - START_MARKER.created_at`

Both timestamps are raw GitHub server values from immutable issue #1 comments. Model/local time strings never classify duration. Invalid marker pair => CLOCK_EVIDENCE_INVALID. Historical pre-protocol timing is supporting only.

## Phase A — boundary search
1. Purposeful bounded test-generated workload is valid when it advances/validates this research; idle/sleep/no-op padding is excluded.
2. Create START_MARKER first. Fetch raw server created_at.
3. Immediately prearm the same recurring automation for `START_MARKER.created_at + target_runtime + planned_gap`; Phase-A baseline planned gap is +3m. Verify returned DTSTART/RRULE/enabled state.
4. Perform sustained substantive work across the declared workload profile.
5. At close: finish substantive work, persist durable close checkpoint, create END_MARKER, fetch raw server created_at, compute strict WORKED. Terminal ledger/state/table synchronization follows END and is outside WORKED.
6. Clean PASS requires marker-valid WORKED >= target, verified prearm, sustained substantive work, durable close checkpoint, and no duration-attributable forced stop.
7. Clean close is CLEAN_PASS_PENDING_WAKE until retrospective continuation observation; only then may server-clock lower bound and next coarse target advance.
8. Separate duration failures from provider/tool/network/scheduler failures.
9. First credible duration failure creates a profile-specific upper candidate; refine at about 1m with profile fixed.
10. If no boundary appears, report only a lower bound and keep ascending.

## Phase B — operating-cap validation
Production cap is not max observed success. Require repeated marker-valid evidence, initially >=5 clean runs at/near candidate, representative profiles, durable close, continuation observation where measurable, and explicit safety margin below credible failure region.

Current-protocol close-reserve evidence is distinct from legacy samples. Pre-END close/checkpoint overhead and post-END terminal-sync overhead are separate quantities.

## Phase C — policy generalization
Compare:
- P1 FIXED_THRESHOLD
- P2 SOFT_CUTOFF_PLUS_HARD_CAP
- P3 ESTIMATED_NEXT_TASK_ADMISSION
- P4 ADAPTIVE_ADMISSION

P3/P4 may use an in-flight control elapsed estimate, but that estimate is not strict WORKED. Final empirical policy outcome is reconciled after END_MARKER against authoritative server evidence.

Prefer the simplest policy practically equivalent on useful-work utilization, clean-close preservation, continuation, overshoot/lost-finalization, early-handoff waste, and robustness.

## Cross-profile generalization
A single profile may advance exploratory lower bound after strict wake confirmation, but final universal cap requires representative profile replication near candidate. If one realistic profile is materially worse, use worst credible risk or profile-aware admission only when justified.

## Phase D — prearmed gap optimization
After runtime/cap policy stabilizes, hold it approximately fixed and test planned gap from +3m toward +2m/+1m.

Definition uses authoritative start:
`planned_gap = PREARM_NEXT - (START_MARKER.created_at + target_runtime)`.

Actual idle gap/wake lateness count quantitatively only when both endpoints are trustworthy server-side observations. Model-authored timestamps do not qualify.

Choose the smallest gap that preserves clean close and stable continuation without materially higher overlap/missed-wake risk.

## Final output
SERVER_CLOCK_SAFE_LOWER_BOUND, FAILURE_BOUNDARY or unresolved, OPERATING_CAP, PRODUCTIVE_CAP, SOFT_CUTOFF, HARD_CAP, current-protocol CLOSE_OVERHEAD, SAFETY_MARGIN, NEXT_TASK_ADMISSION, validation confidence/count, workload coverage, rollback, selected planned gap.
