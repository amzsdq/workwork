# Unit 08 — Reproducibility audit

Probe: PROBE-14M-20260923T095323KST

A fresh worker can reconstruct the active research decision from durable files alone:
1. state/current.json => strict mode, lower bound 12m, next target 14m.
2. PROBE_EXECUTION_PLAN.md => 14m uses W3 MIXED_IO.
3. RUNTIME_BOUNDARY_DECISION_RULE.md => one clean pass advances coarse target but not production cap.
4. RUNTIME_MEASUREMENT_PROTOCOL.md => next invocation must provide retrospective wake evidence.
5. runtime-evidence/.../start.json => this probe's start and pre-armed successor time.

Result: continuation is reproducible without relying on chat transcript.
