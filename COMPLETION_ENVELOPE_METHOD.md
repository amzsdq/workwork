# Completion Envelope Method

Purpose: identify how late useful work can continue while preserving reliable durable close under the final GitHub server-clock invariant.

## Key distinction
For heterogeneous tasks, the safe frontier depends on the duration of the next unit:

`remaining_slack = hard_cap - worked_so_far_estimate - close_reserve - safety_margin`

A unit is admissible only when its credible duration estimate fits inside remaining slack. Any in-flight `worked_so_far_estimate` is control guidance only; final strict WORKED is computed after END from GitHub server markers.

Expose both:
- `PRODUCTIVE_CAP`: conservative scalar latest-normal-work point for simple P1/P2 policies;
- `COMPLETION_ENVELOPE`: task-size-aware frontier for P3/P4.

## Two close endpoints
The final clock invariant separates:

1. `MEASURED_WORK_END = END_MARKER.created_at`.
   - Authoritative endpoint for strict WORKED.
   - Occurs after substantive work and the durable close checkpoint.
   - `WORKED = END_MARKER.created_at - START_MARKER.created_at`.

2. `OPERATIONAL_SYNC_END`.
   - Secondary endpoint after post-END terminal evidence/event/state/table synchronization and consistency verification.
   - This bookkeeping is outside WORKED.
   - It can be measured as control/close-system overhead when timestamps are trustworthy, but never changes END_MARKER or strict duration classification.

This avoids the previous semantic conflict where terminal synchronization both followed END and was also described as the endpoint of elapsed work.

## Evidence to collect
For each near-cap run when directly observable:
- hard-cap candidate;
- last normal task admission evidence;
- estimated/actual last-unit duration when genuinely observed;
- durable close-checkpoint evidence;
- START/END marker IDs and server timestamps;
- strict WORKED;
- post-END operational-sync overhead when directly measurable;
- clean close;
- overshoot relative to target from strict WORKED;
- workload profile.

Do not infer missing unit durations or post-END timings.

## Legacy evidence rule
Pre-`GITHUB_SERVER_MARKER_V1` close-overhead observations may remain historical/supporting evidence if their original clocks were directly observed, but they must be labeled legacy and cannot establish the new strict WORKED boundary or by themselves promote a close reserve.

## Experimental sequence
1. Establish server-clock boundary/cap region.
2. Collect direct completion-envelope samples near that region.
3. Start with a conservative reserve derived from observed close behavior plus separately justified safety margin.
4. Record actual last admitted useful units and close results.
5. Compare successful and failed slack values.
6. Prefer P1/P2 if a scalar cutoff preserves close with little useful-work loss; use P3 only when variable unit sizes materially benefit; use P4 only when adaptive evidence materially improves outcomes.

## Interpretation
A clean survival result does not mean work should always continue until the same point. Admission must reserve enough room for the current unit tail and durable close checkpoint. Post-END ledger synchronization is a separate reliability/control cost and should be monitored without contaminating strict WORKED.

## Promotion discipline
Do not promote PRODUCTIVE_CAP, close reserve, or completion-envelope frontier from one sample. Use repeated direct samples and representative workload shapes; tail behavior matters.
