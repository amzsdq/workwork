# workwork

Durable workspace for this ChatGPT RRULE relay.

## Objective
Apply and validate the minimal RRULE relay core with maximum continuation reliability and minimum idle/control overhead.

## Normal relay contract
- Reuse the same automation for normal continuation; do not create a replacement.
- Keep a complete recurring VEVENT containing `RRULE:FREQ=HOURLY`.
- Do not use DTSTART-only one-shot or `dtstart_offset_json`.
- Normal clean path uses one final scheduler mutation per turn.
- Compute `FINAL_NEXT` immediately before that write from actual current time. Current promoted experimental baseline: about +3 minutes.
- Treat +3 minutes as an empirical baseline, not a platform guarantee.
- Inspect the scheduler update return object for expected DTSTART, RRULE presence, and enabled=true. Do not add a redundant clean-path metadata read.
- Restore from the smallest durable tail first; broaden reads only for ambiguity, boundary/promotion, rollback, or recovery.
- Every active invocation should contain substantive authorized work; do not manufacture busywork.
- Keep clean-success evidence compact and exception evidence explicit.
- Preserve Git history as a recovery source.

## Durable state
- `state/events.log` — canonical append-only truth.
- `state/current.json` — derived snapshot; rebuildable from events.
- `state/README.md` — state/recovery semantics.

Never rewrite historical events to merge new state. Never persist credentials, cookies, session state, private URLs, or secrets.

## Clean turn
1. Read the latest checkpoint/event tail.
2. Restore the active task or unfinished trial.
3. Perform substantive work.
4. Append the minimal durable event/checkpoint.
5. Immediately before close, compute FINAL_NEXT using the current lead-time baseline.
6. Update the same automation once using complete VEVENT + recurring RRULE, keeping it enabled.
7. Validate the update return object; stop.

## Research priority
Prefer failure/recovery evidence over adding orchestration:
1. missed-wake fault injection
2. duplicate-invocation fault injection
3. scheduler-write failure injection
4. GitHub write/read recovery
5. stale-checkpoint recovery
6. concurrent authority collision
7. long relay soak test
8. useful-work duty-cycle measurement
