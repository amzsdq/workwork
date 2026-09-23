# SHADOW READY evidence

A SHADOW_SUCCESSOR is READY only after it has read the current authority record, restored the latest predecessor checkpoint/state needed for continuation, and prepared a concrete non-duplicating next unit.

Canonical authority record: repository-root `handoff-state.json`.

## Required immutable READY fields
- successor_invocation_id
- predecessor_invocation_id
- authority_generation_observed
- proposed_next_unit
- source_files_read
- scheduler_mutated=false
- authoritative_side_effects_performed=false

Timing used for empirical optimization must come from authoritative server-side timestamps where feasible. Model-authored timestamp strings are non-authoritative metadata. If no authoritative timing exists, mark the metric unresolved.

## ACTIVE_OWNER acceptance checklist
1. Fresh-read `handoff-state.json`.
2. Confirm this invocation is still active_invocation_id and generation matches local owner generation.
3. Confirm READY names this invocation as predecessor and observed expected generation.
4. Finish/checkpoint current smallest safe unit; start no new normal unit.
5. Fresh-read `handoff-state.json` again and CAS-update using exact blob SHA: generation+1, active_invocation_id=successor, predecessor_invocation_id=this owner, successor_invocation_id=successor, status=TRANSFERRED.
6. Persist immutable transfer evidence.
7. Perform no further authoritative work or scheduler mutation.

## Successor acceptance checklist
1. Fresh-read `handoff-state.json`.
2. Confirm active_invocation_id equals successor and generation is exactly predecessor_generation+1.
3. Persist ACCEPTED evidence.
4. Become ACTIVE_OWNER and begin prepared unit.
5. Immediately pre-arm next successor under S1.

Any stale SHA, generation mismatch, ambiguous READY, duplicate owner, or scheduler write by SHADOW makes the handoff non-clean and requires recovery.
