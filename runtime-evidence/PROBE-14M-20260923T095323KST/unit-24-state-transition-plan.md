# Unit 24 — State transition plan

Probe: PROBE-14M-20260923T095323KST

If close is CLEAN_PASS:
- set last_clean_target_minutes=14;
- set next_strict_target_minutes=16;
- keep first_failure_boundary_minutes=null;
- do not set promoted_operating_cap_minutes.

If credible DURATION_FAIL:
- keep last clean=12;
- set first failure candidate=14;
- switch next refinement target to approximately 13m.

If NON_DURATION_FAIL or UNDER_TARGET:
- keep strict target at 14m for retry.

Only durable close classification may execute this transition.
