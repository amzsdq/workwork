# Runtime Boundary Decision Rule

Purpose: prevent false promotion from sparse/misclassified evidence while keeping Phase A efficient.

## Clock validity gate
Before strict classification require:
- START_MARKER comment ID and raw server created_at;
- END_MARKER comment ID and raw server created_at;
- WORKED = END - START;
- marker_pair_valid=true.

Model/inferred time is ignored. Missing/invalid pair => CLOCK_EVIDENCE_INVALID, no lower/failure-boundary effect.

## Evidence states
Treat target/profile as a pair:
- clean_pass: valid server marker pair proves WORKED reached class, prearm verified, durable close checkpoint completed normally;
- duration_fail: credible near/after-target close loss/forced termination without independent cause;
- non_duration_fail: explicit independent provider/tool/network/scheduler cause;
- under_target: valid pair proves WORKED below class;
- clock_evidence_invalid: exact duration unavailable.

Only clean_pass and credible duration_fail affect runtime-boundary inference. Clean close is CLEAN_PASS_PENDING_WAKE until retrospective continuation observation; only then may server-clock safe lower bound advance.

## Coarse ascent / refinement
A clean target + retrospective wake advances exploratory target by about +2m but does not promote production cap. First credible duration failure is profile-specific until same-profile bracketing/refinement narrows it near 1m. Cross-profile validation determines universal vs profile-aware final policy.

## Operating-cap promotion
Candidate C initially requires >=5 clean marker-valid closes at/near C, no unresolved duration failure at/below C, verified prearm, durable close, continuation evidence where measurable, explicit safety margin, and representative profiles. Longest one-off success is never automatically the cap.

## Completion-envelope / close reserve
Under `GITHUB_SERVER_CLOCK_PROTOCOL.md`:
- strict measured work ends at END_MARKER.created_at after substantive work + durable close checkpoint;
- terminal ledger/state/table synchronization occurs after END and is outside WORKED.

Therefore distinguish:
1. `pre_end_close_overhead` — checkpoint/finalization work before END, relevant to admission reserve;
2. `post_end_sync_overhead` — bookkeeping/control overhead after END, relevant to long-run utilization/recovery but not strict WORKED.

Record either only when directly observable with compatible trustworthy clocks. Legacy pre-server-clock close observations are supporting-only and do not count toward current-protocol reserve-promotion sample N.

Scheduler prearm occurs after START and is tracked separately.

## Policy-stage admission evidence
For P3/P4 record, when trustworthy:
- control elapsed estimate/timing scope at admission;
- estimated next-unit duration;
- predicted close reserve;
- safety margin;
- actual next-unit duration when observable;
- empirical outcome reconciled after END;
- overshoot or unnecessary early handoff.

This evaluates decision quality without letting in-flight model time become strict duration proof.
