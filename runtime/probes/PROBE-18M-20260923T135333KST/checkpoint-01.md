# Strict 18m W2 checkpoint 01

Probe: PROBE-18M-20260923T135333KST
Profile: W2_WRITE_CHECKPOINT_HEAVY

Substantive work completed:
- Loaded fresh canonical runtime state and reconciled stale prompt fields against durable state.
- Confirmed strict safe lower bound is 16m and 18m is the active next target.
- Confirmed no first failure boundary is recorded.
- Pre-armed the same recurring automation for target + 3m and validated returned scheduler state.
- Created durable start evidence for this probe.
- Tested a structured high-density checkpoint write; provider safety gate rejected that write. Classified as a non-duration tool/provider event, not a runtime-boundary failure.
- Reduced checkpoint representation and continued durable-write workload rather than treating the rejected write as duration evidence.

Measurement state:
- target_runtime_min: 18
- workload_profile: W2_WRITE_CHECKPOINT_HEAVY
- load_origin: TEST_GENERATED
- scheduler_write_ok: true
- scheduler_state_ok: true
- checkpoint_saved: true
- forced_stop_or_timeout: false
- non_duration_failure: true (one GitHub write safety-gate rejection; recovered)
- clean_close: pending

The probe remains active; this checkpoint is not a PASS claim.