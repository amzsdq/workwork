# Intentional Overlap Probe

## Goal
Determine what happens when the same recurring ChatGPT Automation is scheduled to wake before its current invocation is expected to finish.

Primary classifications:
- CONCURRENT: second invocation starts while first invocation continues producing evidence.
- PREEMPTED: second invocation starts and the first invocation stops at or immediately before that wake.
- SERIALIZED_OR_DEFERRED: the second invocation does not actually start until after the first invocation closes.
- MISSED_WAKE: scheduled overlap wake is not observed.
- INCONCLUSIVE: evidence is insufficient.

## Probe parameters
- probe_id: OVERLAP-15M-WAKE12M-01
- primary target runtime: 15 minutes
- pre-armed next wake offset: 12 minutes from PRIMARY_START
- nominal overlap: 3 minutes
- workload: TEST_GENERATED_MIXED_LOAD
- recurrence: same automation, RRULE:FREQ=HOURLY

This is a deliberate overlap stress test. The usual positive-gap rule is temporarily suspended for this probe only.

## Evidence model
Do not append concurrent evidence into one shared file. Use independent immutable files under:
`overlap/OVERLAP-15M-WAKE12M-01/`

Expected artifacts:
- primary-start.json
- primary-heartbeat-<seq>.json
- primary-end.json
- secondary-start-<timestamp>.json
- secondary-observation-<timestamp>.json
- result.json (created only after classification)

Each evidence file records actual observed KST/UTC timestamps and the invocation role.

## Primary invocation
1. Capture PRIMARY_START immediately.
2. Create primary-start.json.
3. Compute OVERLAP_WAKE = PRIMARY_START + 12 minutes.
4. Immediately update the SAME automation to OVERLAP_WAKE with complete recurring VEVENT and enabled=true.
5. Verify the returned schedule object.
6. Run TEST_GENERATED_MIXED_LOAD continuously toward a 15-minute target.
7. Create heartbeat files periodically during useful test work, with a target cadence of roughly 1-2 minutes when practical. Heartbeats are experimental evidence, not a reason to idle.
8. If still alive after the scheduled OVERLAP_WAKE, create at least one heartbeat as soon as practical after the due time.
9. At normal close near/after 15m, create primary-end.json.
10. Do not mutate the scheduler again at primary close.

## Secondary/overlap invocation
A wake that observes primary-start.json but no primary-end.json treats itself as the overlap observer.
1. Capture SECONDARY_START and create its own secondary-start file.
2. Do not overwrite primary files.
3. Inspect the latest primary heartbeat timestamps.
4. Perform bounded observation/analysis and re-read the overlap directory for evidence created after SECONDARY_START.
5. Classification:
   - CONCURRENT if primary heartbeat/end evidence has a timestamp later than SECONDARY_START.
   - SERIALIZED_OR_DEFERRED if primary-end predates SECONDARY_START.
   - PREEMPTED_CANDIDATE if primary evidence was fresh immediately before the due time but no primary evidence appears after SECONDARY_START.
   - MISSED_WAKE if no secondary invocation occurs near the pre-armed due and later evidence proves the primary closed normally.
   - otherwise INCONCLUSIVE.
6. Persist result.json only when evidence is sufficient; otherwise persist a secondary-observation file.
7. After the overlap observation is safely persisted, the experiment may restore a non-overlapping schedule for continuation.

## Append-only / conflict rule
Concurrent invocations must never race to rewrite one shared evidence file. Create new per-invocation/per-heartbeat files. Shared derived state can be reconciled later from these immutable artifacts.

## Safety
This probe is intentionally allowed to interrupt or overlap the primary test. No production data is involved. If the relay stops, the user can manually revive it from the durable overlap artifacts.
