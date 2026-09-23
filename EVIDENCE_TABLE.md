# Runtime Evidence Table

Strict timing authority:
`WORKED = END_MARKER.created_at - START_MARKER.created_at` from raw GitHub server timestamps.

Strict harness authority:
`STRICT_RUNTIME_HARNESS_V2` with scalable unique workload supply. Finite workload exhaustion before PRE_CLOSE is a harness defect, not runtime-boundary evidence.

| Probe | Server WORKED | Historical result | Harness-v2 interpretation | Boundary effect |
|---|---:|---|---|---|
| R3 | 652s | UNDER_TARGET | HARNESS_UNDER_TARGET: finite workload exhausted | NONE |
| R4 | 736s | UNDER_TARGET | HARNESS_UNDER_TARGET: finite workload exhausted | NONE |
| R5 | n/a | NON_DURATION_FAIL | NON_DURATION_FAIL | NONE |
| R6 | 975s | UNDER_TARGET | HARNESS_UNDER_TARGET: finite workload exhausted | NONE |
| R7 | 251s | UNDER_TARGET | HARNESS_UNDER_TARGET: finite workload exhausted | NONE |
| R8 | 182s | UNDER_TARGET | HARNESS_UNDER_TARGET: finite workload exhausted; terminal event recovered after 409 | NONE |

## Current strict state

- SERVER_CLOCK_SAFE_LOWER_BOUND: unresolved.
- FAILURE_BOUNDARY: unresolved.
- Credible duration failures under server-clock protocol: 0.
- Current case: SC-A22-CLOCK-01.
- Automation: PAUSED_BY_USER.
- Next probe after explicit user resume must use:
  - `runtime/RUNTIME_STRESS_WORKLOAD_GENERATOR.py`
  - `runtime/SCALABLE_STRICT_PROBE_WORKLOAD_PROTOCOL.md`
  - START / WORK_START / PRE_CLOSE / END raw server markers
  - `runtime/TERMINAL_STATE_SYNC_PROTOCOL.md`
- Normal close must be timing/admission driven. A completed batch loads the next unique batch; it must not close the probe.
- R8 immutable terminal event: `state/events/PROBE-22M-SERVERCLOCK-20260924-R8.json`.

Mutable projections are derived views. Immutable per-probe terminal/event evidence plus raw marker REST resources remain authoritative.
