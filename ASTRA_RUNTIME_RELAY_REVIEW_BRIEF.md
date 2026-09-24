# Astra Runtime Relay Review Brief

Status: REQUEST FOR INDEPENDENT REVIEW / REDESIGN
Repo: amzsdq/workwork

## Mission
Independently audit and improve the continuous runtime-research relay. Do not merely restate the current design. Find the simplest design that maximizes useful working time, minimizes idle gaps, preserves honest server-clock evidence, and survives scheduler jitter/missed occurrences.

## Current authoritative inputs
Read fresh before making conclusions:
- `state/current.json`
- `OPERATIONAL_RELAY_POLICY.md`
- `RUNTIME_RESEARCH_MASTER_PLAN.md`
- `GITHUB_SERVER_CLOCK_PROTOCOL.md`
- `runtime/SCALABLE_STRICT_PROBE_WORKLOAD_PROTOCOL.md`
- `runtime/TERMINAL_STATE_SYNC_PROTOCOL.md`
- latest `runtime-boundary/*` durable evidence

Stable relay invariants live in the Workaholic plugin; repository state owns tunable numeric values and experiment phase. Do not duplicate plugin invariant text into repository policy unless the audit concludes a repository-level invariant is independently necessary.

## Observed failure that needs explanation
A canonical recurring automation used `RRULE:FREQ=HOURLY` while trying to move DTSTART forward by a short lead. A prior update stored a DTSTART that was already in the past by the time the update completed. The intended occurrence was therefore missed and the recurring rule fell through to the next hourly occurrence, producing roughly one hour of idle gap. This must be treated as a scheduler/control-plane defect, not productive runtime evidence.

The immediate mitigation is to require the stored due time to remain safely in the future relative to authoritative update completion, not merely equal the locally intended timestamp. Audit whether that is sufficient or whether a different scheduling primitive/state machine is simpler and more robust.

## New handoff/work-queue experiment
The canonical automation prompt now contains a replaceable section named `[TO-DO LIST FOR THIS TURN]`.

Intent:
- predecessor writes the successor's concrete remaining work into this block;
- replace the block each handoff instead of accumulating history;
- queue enough real work to occupy the full repository-defined target productive window;
- avoid turns that stop early because the model has no explicit next unit;
- keep SOURCE_OF_TRUTH and plugin invariants authoritative over the queue;
- prohibit filler, sleeping, duplicate-ID padding, or semantically repeated work merely to consume time.

Audit this idea empirically and architecturally. Determine whether the queue should live in the automation prompt, durable repository state, or a hybrid. Evaluate failure modes: stale queue, prompt/repo disagreement, lost replacement, oversized prompt, predecessor over-specification, duplicated work, and queue exhaustion before the target window.

## Required analysis
1. Reconstruct the scheduler failure mode precisely from durable/live evidence where available.
2. Evaluate the current same-canonical recurring self-update approach against alternatives. Prefer the least complex mechanism that actually prevents idle gaps.
3. Define a correctness condition for future scheduling that cannot report success when the effective next occurrence has already been missed.
4. Evaluate overlap/pre-arm behavior separately from strict runtime-duration measurement; do not conflate scheduler survival with substantive work duration.
5. Audit the new replaceable TO-DO queue. Propose a minimal schema and ownership/update rule if it is worth keeping; reject it if it creates more failure modes than value.
6. Ensure the work generator/backlog can supply semantically unique, decision-useful work for the entire target duration. Finite corpus exhaustion must not become an excuse for early completion.
7. Preserve raw GitHub server timestamps as duration authority. Do not use model-written START/END strings as exact timing evidence.
8. Identify which current rules/docs are redundant and can be deleted after a better design is validated.
9. Propose falsifiable tests. For every claimed fix, state what observation would disprove it.

## Deliverable
Produce a decision memo with:
- root cause(s), ranked by confidence;
- KEEP / MODIFY / DELETE decisions for current mechanisms;
- proposed minimal state machine;
- exact success/failure observables;
- test matrix including missed-due-time, scheduler jitter, overlapping predecessor/successor, stale TO-DO queue, and queue-exhaustion cases;
- migration plan that can be rolled back;
- explicit distinction between proven evidence, hypothesis, and recommendation.

Optimize for measured working-time utilization and reliability, not policy complexity. Existing design choices are disposable if evidence supports a simpler mechanism.