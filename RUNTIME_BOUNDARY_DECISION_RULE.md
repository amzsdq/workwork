# Runtime Boundary Decision Rule

Purpose: prevent false promotion of a runtime limit from sparse or misclassified evidence while keeping Phase A efficient.

## Evidence states per target class
Each target runtime class has four counters:
- `clean_pass`: substantive run reached the class and closed durably with scheduler state verified.
- `duration_fail`: credible near/after-target close-loss or forced termination without independent non-duration cause.
- `non_duration_fail`: explicit independent GitHub/network/tool/provider failure.
- `under_target`: substantive work ended before the class; informative for workload generation but not boundary evidence.

Only `clean_pass` and `duration_fail` affect the runtime boundary. `non_duration_fail` and `under_target` do not move it.

## Coarse ascent
- A single clean pass at target T is enough to move the *probe target* to T+2m.
- It is not enough to promote T as a production cap.
- `SAFE_LOWER_BOUND` may be reported as the highest class with at least one clean timing pass, explicitly marked as a lower-bound observation rather than a validated cap.

## Failure handling
A first credible duration failure at F creates `FAILURE_BOUNDARY_CANDIDATE=F`, not a final boundary.
- If the immediately lower tested class L has a clean pass, refine inside [L,F].
- If the failure is ambiguous, repeat F once before narrowing.
- If an independent failure cause is found, reclassify as `non_duration_fail` and continue the prior search.

## Refinement
Use approximately 1-minute target classes between last clean L and first credible failed F.
- Clean midpoint raises L.
- Credible duration failure lowers F.
- Continue until the bracket is about 1 minute or finer, subject to available evidence.

## Operating-cap promotion
`max_observed_success` is never automatically the operating cap.

A candidate operating cap C requires initially:
- >=5 clean closes at/near C,
- no unresolved duration failure at or below C,
- preserved checkpoint and final RRULE scheduler write on each counted pass,
- observed next wake for the prior run where measurable,
- explicit safety margin below the credible failure boundary.

If variance in close overhead or elapsed runtime is large, widen the safety margin rather than increasing policy complexity first.

## Close-reserve measurement
For every timing pass record `pre_close_ts`, `scheduler_write_start_ts`, and `scheduler_write_end_ts` when practical.

`close_overhead_sec = scheduler_write_end_ts - pre_close_ts`

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
