# workwork

Durable workspace for this ChatGPT RRULE relay.

## Single research objective
Determine the maximum safe useful-work duration per automation invocation before runtime/turn termination risk becomes operationally unacceptable, given a recurring RRULE relay whose current promoted next-wake lead-time baseline is about +3 minutes.

The optimization target is long-run useful-work utilization, not merely the longest single observed run.

## Why this matters
With a 10-minute work floor and ~3-minute relay gap, idealized duty cycle is only 10/(10+3) ≈ 76.9% before scheduler jitter and failures. Longer safe turns can materially improve utilization, but pushing too close to the runtime ceiling can lose the final checkpoint/scheduler write and reduce real availability.

## Research contract
- Reuse the same automation for normal continuation; no replacement automation.
- Keep a complete recurring VEVENT containing `RRULE:FREQ=HOURLY`.
- Do not use DTSTART-only one-shot or `dtstart_offset_json`.
- Normal clean path performs one final scheduler mutation per turn.
- Current lead-time baseline is ~+3 minutes and remains an empirical baseline, not a platform guarantee.
- Measure real elapsed runtime and useful work separately. Never pad, sleep, or invent busywork just to hit a duration target.
- A run is only a clean timing PASS if substantive work occurred, durable evidence was saved, and the final recurring scheduler write returned the intended DTSTART/RRULE/enabled state.
- WRITE_OK is not future WAKE_OK.
- Any platform/tool failure not plausibly caused by turn duration must be classified separately rather than counted as a timeout boundary.
- Git history and `state/events.log` are recovery evidence.

## Adaptive search
Start from the existing operational 10-minute baseline, treated as prior evidence rather than a newly proven ceiling.

### Phase A — coarse ascent
Test target useful-work/elapsed classes upward in roughly 2-minute steps:
12 → 14 → 16 → 18 → 20 → continue +2 minutes while clean.

A target may advance after a clean completed run with final checkpoint + scheduler write intact. Any forced termination, missing close, or duration-correlated inability to complete the final handoff creates an upper-bound candidate.

### Phase B — boundary refinement
Once a first credible failure boundary appears, narrow the interval between the last clean target and the first failed target using ~1-minute steps.

### Phase C — safety validation
Do not equate the longest one-off success with the operating limit. Validate the proposed operating cap over repeated runs. Prefer a cap that:
- has at least 5 clean repeated runs at that class,
- preserves the final durable checkpoint and scheduler write,
- leaves a non-trivial margin below the first credible failure boundary,
- improves expected long-run duty cycle after observed wake failures/jitter are included.

If no failure boundary has been observed yet, continue ascent rather than declaring a maximum.

## Decision metric
Track at minimum:
- target_runtime_min
- actual_elapsed_sec
- useful_work_sec
- clean_close
- checkpoint_saved
- scheduler_write_ok
- scheduler_state_ok
- next_wake_observed on the following invocation
- forced_stop_or_timeout
- non_duration_failure
- idle_gap_sec when observable

The final recommendation is not `max_observed_success`. It is the highest empirically supported operating duration with an explicit safety margin and better expected useful-work utilization.

## Durable state
- `state/events.log` — canonical append-only experiment history.
- `state/current.json` — derived current experiment state; rebuildable.
- `MAX_SAFE_RUNTIME_RESEARCH.md` — experiment/decision protocol.

Never rewrite historical events to merge new state. Never persist credentials, cookies, session state, private URLs, or secrets.
