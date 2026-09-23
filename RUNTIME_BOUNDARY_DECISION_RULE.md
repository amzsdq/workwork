# Runtime Boundary Decision Rule

Purpose: prevent false promotion from sparse, misclassified, or low-quality workload evidence while keeping Phase A efficient.

## Clock validity gate
Strict classification requires raw START/END IDs + server created_at and `WORKED=END-START`. Model/inferred time is ignored. Invalid pair => CLOCK_EVIDENCE_INVALID, no lower/failure-boundary effect.

## Substantive-work quality gate
A strict **safe substantive-runtime** promotion additionally requires sustained useful work. Under Harness V2, ID uniqueness alone is insufficient: workload must be semantically/decision unique or have justified independent repeat value. Posthoc discovery of ID-only deterministic repetition preserves valid clock survival/close evidence but blocks/reopens the substantive lower-bound promotion until revalidated or superseded.

## Evidence states
Target/profile pair:
- clean_pass: valid clock reaches target, scheduler/prearm verified, sustained substantive-work quality valid, durable clean close;
- duration_fail: credible near/after-target close loss/forced termination without independent cause;
- non_duration_fail: explicit independent provider/tool/network/scheduler cause;
- under_target / harness_under_target: valid clock below target; no failure boundary;
- clock_evidence_invalid: exact duration unavailable;
- harness_quality_invalid: clock may remain valid but strict substantive promotion is blocked.

Clean close is PENDING_WAKE until retrospective continuation; only then may an otherwise eligible lower bound advance.

## Coarse ascent / refinement
Eligible clean target + retrospective wake advances exploratory target by about +2m but not production cap. First credible duration failure remains profile-specific until controlled bracketing/refinement. Cross-profile validation determines universal vs profile-aware policy.

## Operating-cap promotion
Candidate C initially requires >=5 clean current-protocol closes at/near C, no unresolved duration failure at/below C, valid substantive-work quality for counted runs, verified prearm, durable close, continuation evidence where measurable, explicit safety margin, and representative profiles. Longest one-off success never automatically becomes cap.

## Completion envelope / reserve
PRE_CLOSE→END is current-protocol close overhead relevant to reserve. Post-END projection sync is outside WORKED. Legacy close observations do not count toward reserve-promotion N. Scheduler prearm START→WORK_START is tracked separately.

## Admission evidence
For P3/P4 record authoritative control sample, estimated next-unit duration, predicted close reserve, explicit estimation margin when used, actual next-unit duration when observable, outcome, and overshoot/early-handoff. Zero-slack admission is a distinct edge case; analytic replay never mutates empirical runtime bounds.
