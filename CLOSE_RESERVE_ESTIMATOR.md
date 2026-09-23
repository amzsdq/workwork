# Close Reserve Estimator

Purpose: estimate how much budget must remain for the durable close checkpoint before authoritative END_MARKER, while separately observing post-END terminal-sync overhead.

## Final-clock semantics
Strict WORKED always ends at raw GitHub `END_MARKER.created_at`. Therefore separate:
- `pre_end_close_overhead`: necessary close/checkpoint work before END_MARKER;
- `post_end_sync_overhead`: terminal evidence/event/state/table synchronization after END, outside WORKED.

Do not collapse the two into a single strict duration endpoint.

## Observation
When directly observable with compatible trustworthy clocks, record:
- last normal task admission evidence;
- pre-close checkpoint start;
- END_MARKER server timestamp;
- pre-end close/checkpoint overhead;
- post-END operational-sync end and overhead;
- prearm overhead separately;
- workload profile.

Do not infer missing timestamps. Pre-server-clock close samples remain legacy supporting only unless their timing source is independently trustworthy for the secondary metric; they cannot establish strict WORKED.

## Sparse-sample rule
For N valid direct **current-protocol** pre-end close samples:
- N=0: current-protocol reserve UNKNOWN; no numeric reserve promotion.
- N=1..4: report median/max and LOW_CONFIDENCE provisional reference.
- N>=5: report median, p80 nearest-rank, max, count; candidate fixed reserve may use observed upper behavior plus separately justified uncertainty.

Legacy samples are reported separately and do not increase current-protocol N.

## Profile handling
Track by profile and pooled. If realistic profiles differ materially, use worst credible profile for a universal reserve or adopt profile-aware reserve only when utilization benefit justifies complexity.

## Separation from safety margin
Close reserve covers expected pre-END close/checkpoint work. Safety margin covers uncertainty in runtime ceiling, unit-duration estimation, and close variance. Do not double-count the same variance.

## Phase-C use
A future admission decision may use:
`predicted_finish = elapsed_control_estimate + estimated_next_unit + close_reserve + safety_margin`

The in-flight elapsed estimate is control guidance, not final strict WORKED. Final empirical outcome is reconciled after END_MARKER.

## Promotion discipline
No cap/reserve/adaptive policy is promoted because the estimator exists. Runtime-boundary and repeated current-protocol completion evidence dominate.
