# Unit 12 — Future policy replay schema

Probe: PROBE-14M-20260923T095323KST

For later P1-P4 comparison, each observed admission decision should retain:
- elapsed_at_admission_sec
- estimated_next_unit_sec
- close_reserve_sec and provenance
- safety_margin_sec and provenance
- hard_cap_sec
- admitted boolean
- actual_unit_sec when observed
- close_started_sec
- final_elapsed_sec
- overshoot_sec
- early_handoff_waste_sec when observable

Replay outputs must be labeled analytical and must never mutate Phase-A empirical counters. This schema is sufficient to compare fixed, soft/hard, estimated-next-task, and adaptive policies on the same observed samples.
