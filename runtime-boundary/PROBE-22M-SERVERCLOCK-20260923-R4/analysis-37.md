# R4 terminal schema draft

This schema is prepared before close to minimize terminal bookkeeping latency and mistakes. Values remain unset until authoritative evidence exists.

```json
{
  "probe_id":"PROBE-22M-SERVERCLOCK-20260923-R4",
  "case_id":"SC-A22-CLOCK-01",
  "clock_protocol":"GITHUB_SERVER_MARKER_V1",
  "clock_issue_number":1,
  "start_marker_comment_id":5796189180,
  "start_marker_created_at":"2026-09-23T13:58:33Z",
  "end_marker_comment_id":null,
  "end_marker_created_at":null,
  "worked_sec":null,
  "marker_pair_valid":null,
  "target_runtime_sec":1320,
  "target_reached":null,
  "workload_profile":"W3_MIXED_IO",
  "direct_active_work_sec":null,
  "productive_ratio":null,
  "substantive_unit_count":null,
  "scheduler_write_ok":true,
  "scheduler_state_ok":true,
  "checkpoint_saved":null,
  "clean_close":null,
  "forced_stop_or_timeout":false,
  "non_duration_failure":false,
  "duration_failure_observed":false,
  "terminal_result":null,
  "boundary_effect":null,
  "server_clock_safe_lower_bound_min":null,
  "server_clock_failure_boundary_min":null
}
```

No null classification field may be guessed from model time. Populate only after durable close and raw END fetch.
