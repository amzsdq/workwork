# Completion Envelope Method

Purpose: identify how late useful work can continue while still preserving reliable durable close. The answer is not necessarily one scalar minute.

## Key distinction

For a fixed-size micro-task, a single `latest_safe_start` can be estimated. Across heterogeneous tasks, the safe frontier depends on the duration of the next unit:

`remaining_slack = hard_cap - elapsed - close_reserve - safety_margin`

A unit is admissible only when its credible duration estimate fits inside remaining slack.

Therefore the final result should expose both:
- `PRODUCTIVE_CAP`: a conservative scalar latest-normal-work point useful for simple P1/P2 policies; and
- `COMPLETION_ENVELOPE`: a task-size-aware frontier used by P3/P4.

## Evidence to collect

For each near-cap run when directly observable:
- `hard_cap_candidate_sec`
- `last_normal_task_admit_ts`
- `last_unit_estimated_sec` if an estimate existed before admission
- `last_unit_actual_sec` when measurable
- `pre_close_ts`
- `close_end_ts`
- `close_overhead_sec`
- `clean_close`
- `overshoot_sec`
- `workload_profile`

Do not infer last-unit duration after the fact if its boundaries were not observed.

## Experimental sequence

1. First establish direct close-overhead samples and a credible runtime boundary/cap region.
2. Start with a conservative reserve derived from observed close overhead plus safety margin.
3. On repeated near-cap runs, record the actual last admitted useful unit and close result.
4. Compare successful and failed slack values rather than only comparing total invocation duration.
5. If one simple scalar cutoff preserves clean close with little useful-work loss, prefer P1/P2.
6. Use task-size-aware P3 only if variable unit sizes make the scalar cutoff materially wasteful.
7. Use adaptive P4 only if measured tail/variance changes enough that a fixed reserve materially underperforms.

## Interpretation

A clean 18m survival result does not mean work should always continue until 18m. If close requires 40-60s and the next useful unit may take 90s, that unit must be rejected earlier. Conversely, a 10s micro-unit may still be safely admissible later.

The operating objective is therefore not `maximize last task start time`; it is `maximize useful work admitted subject to reliable completion and continuation`.

## Promotion discipline

Do not promote a PRODUCTIVE_CAP or completion-envelope frontier from one close sample. Use repeated direct close samples and representative task-size/workload shapes. Tail behavior matters because one lost durable close can erase the value of late admitted work.
