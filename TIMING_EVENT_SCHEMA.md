# Timing Event Schema

## Required clock points
- `start_ts`: first timestamp obtained after source-of-truth restoration and immediately before substantive probe work.
- `target_cross_ts`: first observed timestamp at or after target class, if reached.
- `pre_close_ts`: timestamp immediately after the last substantive checkpoint and before final close sequence.
- `scheduler_write_start_ts`: timestamp immediately before final scheduler mutation.
- `scheduler_write_end_ts`: timestamp immediately after scheduler mutation returns.
- `next_invocation_start_ts`: next invocation's observed start, used retrospectively for WAKE_OK/idle-gap evidence.

## Derived durations
- `actual_elapsed_sec = scheduler_write_end_ts - start_ts`
- `useful_work_sec`: sum of bounded substantive work intervals when separately observable; otherwise null rather than guessed.
- `close_overhead_sec = scheduler_write_end_ts - pre_close_ts`
- `overshoot_sec = max(0, actual_elapsed_sec - target_runtime_min*60)`
- `idle_gap_sec`: only when prior close and next invocation start are both trustworthy.

## Classification fields
- `target_runtime_min`
- `result`: CLEAN_PASS | UNDER_TARGET | DURATION_FAIL | NON_DURATION_FAIL | AMBIGUOUS
- `clean_close`
- `checkpoint_saved`
- `scheduler_write_ok`
- `scheduler_state_ok`
- `forced_stop_or_timeout`
- `non_duration_failure`
- `prior_next_wake_observed`
- `policy_variant` (Phase C only)

## Evidence rule
A value that was not directly observed must be null, not estimated after the fact. Estimated next-task duration is permitted only as an explicit estimate field during Phase C and must not replace actual duration evidence.
