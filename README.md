# workwork

Durable workspace for this ChatGPT RRULE relay.

## Single research objective
Find the maximum empirically safe useful-work duration per automation invocation **and** the control policy that repeatedly reproduces near-optimal turns without materially increasing run-out/forced-termination risk.

The final output is not a single number. It must be an operational policy that can be reused by other relay workers.

## Why this matters
With a 10-minute work floor and ~3-minute relay gap, idealized duty cycle is only 10/(10+3) ≈ 76.9% before scheduler jitter and failures. Longer safe turns can materially improve utilization, but pushing too close to the runtime ceiling can lose the final checkpoint/scheduler write and reduce real availability.

The optimization target is long-run useful-work utilization, not merely the longest single observed run.

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

## Phase A — find the runtime boundary
Start from the existing operational 10-minute baseline, treated as prior evidence rather than a newly proven ceiling.

Coarse ascent:
12 → 14 → 16 → 18 → 20 → continue +2 minutes while clean.

A target may advance after a clean completed run with final checkpoint + scheduler write intact. Any forced termination, missing close, or duration-correlated inability to complete the final handoff creates an upper-bound candidate.

Once a credible failure boundary appears, narrow the interval between the last clean target and first failed target using ~1-minute steps.

## Phase B — validate an operating cap
Do not equate the longest one-off success with the operating limit.

A candidate operating cap should:
- have at least 5 clean repeated runs at that class,
- preserve the final durable checkpoint and scheduler write,
- leave a non-trivial margin below the first credible failure boundary,
- improve expected long-run duty cycle after observed wake failures/jitter are included.

If no failure boundary has been observed yet, continue ascent rather than declaring a maximum.

## Phase C — generalize into a reproducible control policy
After the boundary is sufficiently characterized, compare ways to reproduce near-optimal runtime.

Candidate policy families:
1. Fixed threshold:
   - before SOFT_CUTOFF: continue next useful unit
   - at/after SOFT_CUTOFF: prepare handoff
2. Soft cutoff + hard cap:
   - before SOFT_CUTOFF: continue normally
   - after SOFT_CUTOFF: only bounded small units
   - at HARD_CAP: no new work; close
3. Estimated-next-task admission:
   - continue only if elapsed + estimated_next_task + close_overhead + safety_margin < HARD_CAP
4. Adaptive admission:
   - same as estimated admission, but update close-overhead/safety margin from recent evidence.

Do not assume the most complex policy is best. Compare actual utilization, clean-close rate, overshoot rate, and control overhead.

## Final deliverable
The final reusable rule should look like:
- SAFE_LIMIT / credible failure boundary
- SOFT_CUTOFF
- HARD_CAP
- SAFETY_MARGIN
- CLOSE_OVERHEAD estimate
- NEXT_TASK_ADMISSION rule
- evidence/confidence and observed failure modes

Example shape only:
`if elapsed + estimated_next_task + close_overhead + safety_margin < hard_cap: continue; else: handoff`

The numerical values must come from evidence, not from the example.

## Decision metrics
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
- close_overhead_sec
- next_task_estimate_sec when a policy trial uses it
- overshoot_sec
- policy_variant during Phase C

## Durable state
- `state/events.log` — canonical append-only experiment history.
- `state/current.json` — derived current experiment state; rebuildable.
- `MAX_SAFE_RUNTIME_RESEARCH.md` — experiment/decision protocol.

Never rewrite historical event meaning. Never persist credentials, cookies, session state, private URLs, or secrets.
