# Runtime Boundary Decision Rule

Purpose: prevent false promotion of a runtime limit from sparse or misclassified evidence while keeping Phase A efficient.

## Clock validity gate

Before runtime-boundary classification, validate the GitHub server marker pair defined in `GITHUB_SERVER_CLOCK_PROTOCOL.md`.

Required:
- START_MARKER comment ID
- raw START_MARKER.created_at
- END_MARKER comment ID
- raw END_MARKER.created_at
- `WORKED = END_MARKER.created_at - START_MARKER.created_at`
- `marker_pair_valid=true`

Model-authored or inferred time strings are ignored for duration judgment.

If this gate fails, classify the exact-duration evidence as `CLOCK_EVIDENCE_INVALID`. It affects neither lower bound nor failure boundary.

## Evidence states per target/profile class
Treat target runtime and workload profile as a pair during causal interpretation. Each target/profile class has four counters:
- `clean_pass`: a valid GitHub server marker pair proves WORKED reached the class, pre-arm scheduler state was verified, and durable close completed normally.
- `duration_fail`: credible near/after-target close-loss or forced termination without independent non-duration cause.
- `non_duration_fail`: explicit independent GitHub/network/tool/provider failure.
- `under_target`: a valid GitHub server marker pair proves WORKED ended before the class; informative for workload generation but not boundary evidence.
- `clock_evidence_invalid`: exact duration cannot be established from a valid server marker pair; no boundary effect.

Only `clean_pass` and `duration_fail` affect runtime-boundary inference. `non_duration_fail` and `under_target` do not move it.

A clean close is initially `CLEAN_PASS_PENDING_WAKE`. Under the current strict protocol, SAFE_LOWER_BOUND and the next coarse target advance only after the following actual invocation retrospectively confirms WAKE_OK for that pass.

## Coarse ascent
- A single clean pass at target T plus retrospective WAKE_OK is enough to move the exploratory probe target to T+2m.
- It is not enough to promote T as a production cap.
- `SAFE_LOWER_BOUND` may be reported as the highest class with at least one clean timing pass whose next wake was retrospectively observed, explicitly marked as a lower-bound observation rather than a validated universal cap.
- Rotating profiles during coarse ascent broadens exploration but means adjacent target classes are not automatically a causally clean duration bracket.

## Failure handling
A first credible duration failure at F under profile P creates `FAILURE_BOUNDARY_CANDIDATE=(F,P)`, not a final universal boundary.
- If the immediately lower tested class L used the same profile P and has a clean pass, refine inside [L,F] with P fixed.
- If L used a different profile, run the first refinement with P fixed and obtain a same-profile lower anchor when needed before claiming a profile-specific bracket.
- If the failure is ambiguous, repeat F with P fixed once before narrowing.
- If an independent failure cause is found, reclassify as `non_duration_fail` and continue the prior search.

## Refinement
Use approximately 1-minute target classes while holding the failure-producing profile fixed.
- Clean midpoint raises the same-profile lower anchor after retrospective WAKE_OK under the strict protocol.
- Credible duration failure lowers the same-profile upper anchor.
- Continue until the profile-controlled bracket is about 1 minute or finer, subject to available evidence.
- Cross-profile validation near the eventual candidate cap determines whether the final rule can be UNIVERSAL_CAP or must account for profile-dependent risk.

## Operating-cap promotion
`max_observed_success` is never automatically the operating cap.

A candidate operating cap C requires initially:
- >=5 clean closes at/near C,
- no unresolved duration failure at or below C,
- preserved start-of-turn pre-arm RRULE state and final durable checkpoint on each counted pass,
- observed next wake for the prior run where measurable,
- explicit safety margin below the credible failure boundary,
- representative workload-profile coverage sufficient to distinguish a universal cap from profile-specific risk.

If variance in close overhead or elapsed runtime is large, widen the safety margin rather than increasing policy complexity first.

## Close-reserve measurement
For every timing pass record `pre_close_ts` and `close_end_ts` when practical.

`close_overhead_sec = close_end_ts - pre_close_ts`

The scheduler pre-arm happens at START and is not part of close reserve. Track `prearm_overhead_sec` separately.

Until enough observations exist, do not hard-code a close reserve from one sample. Track at least median and upper-tail/max observed close overhead. Phase C may then test whether a fixed reserve is sufficient or adaptive reserve materially improves utilization.

## Policy-stage admission evidence
For P3/P4, every decision to continue should record:
- elapsed time at admission,
- estimated next-unit duration,
- predicted close reserve,
- safety margin,
- actual next-unit duration when observable,
- whether the decision caused overshoot or unnecessary early handoff.

This allows the final policy to be evaluated on decision quality rather than only aggregate runtime.
