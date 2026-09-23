# Unit 18 — Measurement-gap audit

Probe: STRICT-14M-20260923T092741KST

One instrumentation limitation is explicit: the automation runtime supplied run_start_ts, and scheduler update success is durable, but this run did not capture separate direct prearm_write_start_ts/prearm_write_end_ts clock readings. Therefore prearm_overhead_sec must remain unknown rather than inferred from tool latency metadata.

This does not invalidate clean-pass eligibility because the required scheduler state was verified; it only means prearm overhead cannot be used as a quantitative sample from this run.

Close timing should still capture direct pre_close/close_end when target is reached.
