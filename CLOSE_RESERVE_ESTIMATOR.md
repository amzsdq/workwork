# Close Reserve Estimator

Purpose: estimate how much runtime must remain for durable close + scheduler rearm, without pretending sparse samples are precise.

## Observation
For each timing probe, when directly observable, record:
- `pre_close_ts`
- `scheduler_write_start_ts`
- `scheduler_write_end_ts`
- `checkpoint_write_sec` if separately observable
- `scheduler_write_sec`
- `close_overhead_sec = scheduler_write_end_ts - pre_close_ts`

Do not infer missing timestamps.

## Sparse-sample rule
Let N be the number of valid direct `close_overhead_sec` observations.

- N=0: reserve is UNKNOWN. Do not use a numeric reserve to promote a cap.
- N=1..4: report median and max; use max as the provisional observed close-overhead reference, explicitly LOW_CONFIDENCE.
- N>=5: report median, p80 (nearest-rank), max, and sample count. The policy-stage fixed reserve candidate is `max(p80, median + observed_jitter_allowance)`; max remains diagnostic rather than automatically becoming the reserve.

`observed_jitter_allowance` must come from repeated close observations (for example upper-minus-median spread), not an invented constant.

## Separation from safety margin
`close_overhead` and `safety_margin` are different:
- close_overhead estimates expected time required to persist/rearm/verify;
- safety_margin covers uncertainty in runtime ceiling, task-duration estimate error, and close-time variance.

Do not double-count the same observed variance in both terms.

## Phase-C use
For an admission decision at elapsed E with estimated next unit D:

`predicted_finish = E + D + close_reserve + safety_margin`

P3/P4 may admit the unit only when predicted_finish is below HARD_CAP. Record the estimate and actual outcome so estimate error can be measured.

## Promotion discipline
No operating cap or adaptive policy is promoted solely because the estimator exists. Runtime-boundary evidence remains primary. This estimator only converts that boundary into a repeatable close/admission rule.