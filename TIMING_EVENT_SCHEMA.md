# Timing Event Schema

## Authoritative strict clock fields
Every new strict runtime probe records:
- `clock_protocol = GITHUB_SERVER_MARKER_V1`
- `clock_issue_number = 1`
- `start_marker_comment_id`
- `start_marker_created_at` — raw GitHub server value
- `end_marker_comment_id`
- `end_marker_created_at` — raw GitHub server value
- `marker_pair_valid`
- `worked_sec = end_marker_created_at - start_marker_created_at`

`worked_sec` is the only authoritative strict duration. Model/local timestamps never replace it.

## Secondary instrumentation
When directly observable:
- `prearm_write_start_ts` / `prearm_write_end_ts`
- `work_start_ts`
- `last_normal_task_admit_ts`
- `pre_close_ts`
- `operational_sync_end_ts` after post-END terminal synchronization and verification
- `next_invocation_start_ts` retrospectively

Secondary derived fields:
- `active_work_sec` when directly measurable, otherwise null
- `productive_ratio = active_work_sec / worked_sec` only when defensible
- `goal_directed_window_sec` and separately labeled `goal_directed_ratio`
- `substantive_unit_count`
- `prearm_overhead_sec`
- `post_end_sync_overhead_sec` when compatible timestamps exist
- `planned_gap_sec`
- `overshoot_sec = max(0, worked_sec - target_runtime_sec)`
- `actual_idle_gap_sec` / `wake_lateness_sec` only from trustworthy wake evidence

Do not derive strict WORKED from `operational_sync_end_ts`, model-authored start/end strings, scheduler metadata, or legacy `actual_elapsed_sec`.

## Classification fields
- `target_runtime_sec`
- `result`: CLEAN_PASS_PENDING_WAKE | CLEAN_PASS_WAKE_OK | UNDER_TARGET | DURATION_FAIL_CANDIDATE | NON_DURATION_FAIL | CLOCK_EVIDENCE_INVALID | AMBIGUOUS
- `workload_profile`
- `load_origin`: TEST_GENERATED | NATURAL
- `clean_close`
- `checkpoint_saved`
- `prearm_next_ts`
- `planned_gap_sec`
- `prearm_scheduler_write_ok`
- `prearm_scheduler_state_ok`
- `wake_layer_anomaly`
- `productive_evidence_quality`: DIRECT | GOAL_DIRECTED_WINDOW_ONLY | WEAK | UNKNOWN
- `overlap_or_concurrent_wake`
- `forced_stop_or_timeout`
- `non_duration_failure`
- `prior_next_wake_observed`
- `policy_variant` (Phase C only)

## Evidence rule
Unobserved values are null. Purposeful bounded generated workload is valid empirical work when it contributes to the research goal and its profile is recorded. Synthetic classifier/policy cases are logic-only and never move runtime boundaries. Necessary tool latency may appear only in an explicitly labeled goal-directed window, not direct active time.
