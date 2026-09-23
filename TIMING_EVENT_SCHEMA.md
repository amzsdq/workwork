# Timing Event Schema

## Required clock points
- `start_ts`: actual invocation start reference.
- `prearm_write_start_ts`: immediately before start-of-turn scheduler mutation.
- `prearm_write_end_ts`: immediately after pre-arm mutation returns.
- `work_start_ts`: immediately after verified pre-arm.
- `last_normal_task_admit_ts`: last observed admission of an ordinary substantive unit when practical.
- `target_cross_ts`: first observed timestamp at or after target class, if reached.
- `pre_close_ts`: immediately before durable close/finalization.
- `close_end_ts`: immediately after final durable close completes.
- `next_invocation_start_ts`: next invocation start, used retrospectively.

## Derived durations
- `actual_elapsed_sec = close_end_ts - start_ts`
- `active_work_sec`: sum of bounded active test-work intervals when separately observable; otherwise null.
- `productive_ratio = active_work_sec / actual_elapsed_sec` only when active_work_sec is directly supportable; otherwise null.
- `goal_directed_window_sec`: continuously goal-directed work window including inseparable necessary tool I/O; report separately from active_work_sec.
- `goal_directed_ratio = goal_directed_window_sec / actual_elapsed_sec` when its endpoints are trustworthy.
- `substantive_unit_count`: completed useful units; density cross-check, not a time substitute.
- `prearm_overhead_sec = prearm_write_end_ts - prearm_write_start_ts`
- `close_overhead_sec = close_end_ts - pre_close_ts`
- `planned_gap_sec = prearm_next_ts - (start_ts + target_runtime_min*60)`
- `overshoot_sec = max(0, actual_elapsed_sec - target_runtime_min*60)`
- `actual_idle_gap_sec`: next_invocation_start_ts - prior close_end_ts when both are trustworthy.

## Classification fields
- `target_runtime_min`
- `result`: CLEAN_PASS_PENDING_WAKE | CLEAN_PASS_WAKE_OK | UNDER_TARGET | DURATION_FAIL | NON_DURATION_FAIL | AMBIGUOUS
- `workload_profile`
- `load_origin`: TEST_GENERATED | NATURAL
- `clean_close`
- `checkpoint_saved`
- `prearm_next_ts`
- `planned_gap_sec`
- `prearm_scheduler_write_ok`
- `prearm_scheduler_state_ok`
- `actual_idle_gap_sec`
- `overlap_or_concurrent_wake`
- `forced_stop_or_timeout`
- `non_duration_failure`
- `prior_next_wake_observed`
- `policy_variant` (Phase C only)

## Evidence rule
A value that was not directly observed must be null, not estimated after the fact. Deliberately generated bounded workload is valid empirical test work when its profile is recorded. Estimated next-task duration is permitted only as an explicit estimate field during Phase C and must not replace actual duration evidence.

Necessary tool/network latency that cannot be separated from goal-directed execution may be included only in `goal_directed_window_sec`, never silently relabeled as direct `active_work_sec`.
