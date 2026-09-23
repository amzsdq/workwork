# Unit 04 — Canonical ledger resolution

Probe: STRICT-14M-20260923T092741KST

Read canonical state/events.log directly.

Resolution:
- The canonical ledger contains a 12m RUNTIME_PROBE event at 2026-09-23T01:12:38+09:00.
- result=CLEAN_PASS_WITH_CONCURRENT_CONTROL_ANOMALY
- actual_elapsed_sec=761
- clean_close=true
- checkpoint_saved=true
- scheduler_write_ok=true
- scheduler_state_ok=true
- forced_stop_or_timeout=false
- non_duration_failure=false
- close_overhead_sec=32
- safe_lower_bound_min=12
- next explicitly says to reconcile the control-plane conflict and continue ascent at 14m.

Therefore state/current.json's 12m lower-bound claim is supported by canonical append-only evidence. EVIDENCE_TABLE.md is stale and should be repaired after this active probe without changing the historical event.

This resolves the provenance concern raised in Unit 01 and justifies continuing the requested strict 14m class.
